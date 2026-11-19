"""Read-only saved-copper preservation, model resolution and projected coupling screens."""
from pathlib import Path
import json,math,hashlib,pcbnew
D=Path(__file__).resolve().parent;S=D/'studies/sense';C=D/'studies/four-layer-comparison'
def data(path):
 b=pcbnew.LoadBoard(str(path));segments=[];vias=[];models=[]
 for t in b.GetTracks():
  if isinstance(t,pcbnew.PCB_VIA):vias.append(dict(net=t.GetNetname(),xy=(pcbnew.ToMM(t.GetPosition().x),pcbnew.ToMM(t.GetPosition().y)),width=pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu)),drill=pcbnew.ToMM(t.GetDrillValue())));continue
  segments.append(dict(net=t.GetNetname(),layer=t.GetLayer(),width=pcbnew.ToMM(t.GetWidth()),a=(pcbnew.ToMM(t.GetStart().x),pcbnew.ToMM(t.GetStart().y)),z=(pcbnew.ToMM(t.GetEnd().x),pcbnew.ToMM(t.GetEnd().y))))
 for f in b.GetFootprints():
  for model in f.Models():
   p=Path(model.m_Filename.replace('${KIPRJMOD}',path.parent.as_posix())).resolve();assert p.exists(),p;models.append(dict(ref=f.GetReference(),path=model.m_Filename,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 return b,segments,vias,models
def pointseg(p,a,z):
 v=[z[i]-a[i]for i in(0,1)];den=sum(q*q for q in v);u=max(0,min(1,sum((p[i]-a[i])*v[i]for i in(0,1))/(den or 1)));return math.dist(p,[a[i]+u*v[i]for i in(0,1)])
def covered(segments,reference):
 failures=[]
 for i,s in enumerate(reference):
  candidates=[t for t in segments if t['net']==s['net']and t['layer']==s['layer']and t['width']>=s['width']-.0001]
  n=max(1,math.ceil(math.dist(s['a'],s['z'])/.025))
  if any(not any(pointseg([s['a'][k]+(s['z'][k]-s['a'][k])*u/n for k in(0,1)],t['a'],t['z'])<.001 for t in candidates)for u in range(n+1)):failures.append(i)
 return failures
seed,ss,sv,sm=data(S/'ground-seed.kicad_pcb');two,ts,tv,tm=data(S/'Velluneo_route07.kicad_pcb');four,fs,fv,fm=data(C/'Velluneo_four_layer_COMPARISON.kicad_pcb')
measurement_seed,measurement_segments,_,_=data(S/'routing-seed.kicad_pcb')
failed=covered(ts,ss);assert not failed,failed
missing_vias=[v for v in sv if not any(t['net']==v['net']and math.dist(t['xy'],v['xy'])<.001 and t['width']>=v['width']-.0001 and abs(t['drill']-v['drill'])<.0001 for t in tv)];assert not missing_vias,missing_vias
retained=[s for s in ts if s['net']not in{'/PRIMARY_GND','/VDD','/DRV'}];assert not covered(fs,retained)
plan=json.loads((D/'four-layer-plan.json').read_text());mapping=json.loads((D/'design/full-build-result.json').read_text())['logical_to_native_netnames'];layer_ids=[pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu]
planned_segments=[dict(net=mapping[e['net']],layer=layer_ids[e['layers'][0]],width=e['width'],a=[100+x for x in e['a']],z=[100+x for x in e['b']])for e in plan['new_elements']if not e['via']]
assert not covered(fs,planned_segments)
for e in plan['new_elements']:
 if e['via']:assert any(t['net']==mapping[e['net']]and math.dist(t['xy'],[100+x for x in e['a']])<.001 and t['width']>=e['width']-.0001 and abs(t['drill']-.3)<.0001 for t in fv)
hv={'Net-(F1-Pad1)','Net-(BR1-AC-Pad2)','Net-(F1-Pad2)','Net-(BR1-AC-Pad4)','/BULK_POS','/DRAIN','Net-(D1-K)','/STARTUP_MID'}
screens=[]
for name,segments in [('two_layer',ts),('four_layer_comparison',fs)]:
 for net in('/SENSE','/CS'):
  # Only the original dedicated measurement conductors, excluding source power feed.
  measure=[s for s in measurement_segments if s['net']==net]
  minima=[]
  for s in measure:
   for t in segments:
    if t['net']not in hv or t['layer']==s['layer']:continue
    n=max(1,math.ceil(math.dist(s['a'],s['z'])/.005))
    distance=min(pointseg([s['a'][k]+(s['z'][k]-s['a'][k])*u/n for k in(0,1)],t['a'],t['z'])for u in range(n+1))-(s['width']+t['width'])/2
    minima.append(distance)
  screens.append(dict(board=name,net=net,measurement_segments=len(measure),length_mm=sum(math.dist(s['a'],s['z'])for s in measure),minimum_sampled_projected_edge_gap_mm=min(minima),sampling_mm=.005,scope='All different-copper-layer HV tracks in this saved candidate. Sampled geometric screen only; not field/EMI/error or dielectric qualification.'))
out=dict(two_layer_board_sha256=hashlib.sha256((S/'Velluneo_route07.kicad_pcb').read_bytes()).hexdigest(),four_layer_board_sha256=hashlib.sha256((C/'Velluneo_four_layer_COMPARISON.kicad_pcb').read_bytes()).hexdigest(),protected_seed_segments=len(ss),protected_seed_vias=len(sv),protected_2layer_copper_coverage_pass=True,coverage_sampling_mm=.025,coverage_centreline_tolerance_mm=.001,retained_four_layer_segments=len(retained),retained_four_layer_copper_coverage_pass=True,planned_four_layer_segments=len(planned_segments),planned_four_layer_copper_coverage_pass=True,models_two_layer=tm,models_four_layer=fm,coupling_screens=screens,scope='Saved copper/model consistency only; geometry does not establish current rating, switching behavior, physical insulation or process acceptance.')
(D/'design/checks/saved-geometry.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(protected_segments=len(ss),protected_vias=len(sv),models=len(tm),coupling=screens)),flush=True)
def branch(a,z):return next(r['length_mm']for r in plan['attempts']if r['a']==a and r['b']==z)
driver=sum(math.dist(t['a'],t['z'])for t in fs if t['net']=='/DRV');assert abs(driver-branch('U1.3','R7.1'))<.0001
metrics=dict(four_layer_board_sha256=out['four_layer_board_sha256'],two_layer_board_sha256=out['two_layer_board_sha256'],four_layer_plan_sha256=hashlib.sha256((D/'four-layer-plan.json').read_bytes()).hexdigest(),four_layer=dict(drv_planar_mm=driver,ic_return_planar_mm=branch('C1.2','U1.5'),bridge_bulk_planar_mm=branch('C1.1','BR1.1'),local_vdd_planar_mm=branch('U1.2','C2.1'),local_ground_planar_mm=branch('C2.2','U1.5')),two_layer=dict(drv_planar_mm=sum(math.dist(t['a'],t['z'])for t in ts if t['net']=='/DRV'),ic_return_planar_mm=json.loads((D/'reserved-return.json').read_text())['current_IC_return_mm']),scope='DRV is summed saved native planar copper and checked against the applied plan. Other named lengths are applied branch-plan lengths whose copper is independently verified in the saved board. No vertical via length, shortest-path, closed-loop area, inductance or operating performance is inferred.')
(D/'route-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
