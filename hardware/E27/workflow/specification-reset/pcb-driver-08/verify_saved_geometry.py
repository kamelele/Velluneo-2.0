"""Read-only saved-copper preservation, model resolution and projected coupling screens."""
from pathlib import Path
import json,math,hashlib,pcbnew
D=Path(__file__).resolve().parent;S=D/'design';C=S
def data(path):
 b=pcbnew.LoadBoard(str(path));segments=[];vias=[];models=[]
 for t in b.GetTracks():
  if isinstance(t,pcbnew.PCB_VIA):vias.append(dict(net=t.GetNetname(),xy=(pcbnew.ToMM(t.GetPosition().x),pcbnew.ToMM(t.GetPosition().y)),width=pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu)),drill=pcbnew.ToMM(t.GetDrillValue())));continue
  segments.append(dict(net=t.GetNetname(),layer=t.GetLayer(),width=pcbnew.ToMM(t.GetWidth()),a=(pcbnew.ToMM(t.GetStart().x),pcbnew.ToMM(t.GetStart().y)),z=(pcbnew.ToMM(t.GetEnd().x),pcbnew.ToMM(t.GetEnd().y))))
 for f in (b.GetFootprints()if path.parent==S else []):
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

b,fs,fv,fm=data(S/'Velluneo_driver.kicad_pcb')
source,ss,sv,_=data(D/'evidence/routing-input.kicad_pcb')
assert not covered(fs,ss)
assert all(any(t['net']==v['net']and math.dist(t['xy'],v['xy'])<.001 and abs(t['drill']-v['drill'])<.0001 for t in fv)for v in sv)
plan=json.loads((D/'selected-route-plan.json').read_text());mapping=json.loads((S/'full-build-result.json').read_text())['logical_to_native_netnames'];layer_ids=[pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu]
assert hashlib.sha256((D/'evidence/routing-input.kicad_pcb').read_bytes()).hexdigest()==plan['source_board_sha256']
planned=[dict(net=mapping[e['net']],layer=layer_ids[e['layers'][0]],width=e['width'],a=[100+x for x in e['a']],z=[100+x for x in e['b']])for e in plan['new_elements']if not e['via']]
assert not covered(fs,planned)
for e in plan['new_elements']:
 if e['via']:assert any(t['net']==mapping[e['net']]and math.dist(t['xy'],[100+x for x in e['a']])<.001 and t['width']>=e['width']-.0001 and abs(t['drill']-.3)<.0001 for t in fv)
_,ms,_,_=data(D.parent/'pcb-route-07/studies/sense/routing-seed.kicad_pcb')
hv={'Net-(F1-Pad1)','Net-(BR1-AC-Pad2)','Net-(F1-Pad2)','Net-(BR1-AC-Pad4)','/BULK_POS','/DRAIN','Net-(D1-K)','/STARTUP_MID'}
screens=[]
for net in('/SENSE','/CS'):
 measure=[s for s in ms if s['net']==net];assert not covered(fs,measure)
 gaps=[]
 for s in measure:
  for t in fs:
   if t['net']not in hv or t['layer']==s['layer']:continue
   n=max(1,math.ceil(math.dist(s['a'],s['z'])/.005))
   gaps.append(min(pointseg([s['a'][k]+(s['z'][k]-s['a'][k])*u/n for k in(0,1)],t['a'],t['z'])for u in range(n+1))-(s['width']+t['width'])/2)
  for v in fv:
   if v['net']in hv:gaps.append(pointseg(v['xy'],s['a'],s['z'])-(s['width']+v['width'])/2)
 minimum=min(gaps);assert minimum>=3, (net,minimum)
 screens.append(dict(net=net,segments=len(measure),length_mm=sum(math.dist(s['a'],s['z'])for s in measure),minimum_sampled_projected_edge_gap_mm=minimum,sampling_mm=.005))
sha=hashlib.sha256((S/'Velluneo_driver.kicad_pcb').read_bytes()).hexdigest()
out=dict(board_sha256=sha,source_preserved_segments=len(ss),source_preserved_vias=len(sv),planned_segments_checked=len(planned),all_planned_and_protected_copper_present=True,coverage_sampling_mm=.025,coverage_centreline_tolerance_mm=.001,models=fm,coupling_screens=screens,scope='Projected different-layer HV tracks and all HV vias against dedicated original measurement copper; geometric sampling only, not EMI or insulation certification.')
(S/'checks/saved-geometry.json').write_text(json.dumps(out,indent=2)+'\n')
drv=sum(math.dist(t['a'],t['z'])for t in fs if t['net']=='/DRV');assert abs(drv-next(r['planar_length_mm']for r in plan['attempts']if r['label']=='driver'))<.0001
metrics=dict(board_sha256=sha,plan_sha256=hashlib.sha256((D/'selected-route-plan.json').read_bytes()).hexdigest(),drv_planar_mm=drv,branches=plan['attempts'],scope='Saved native DRV length and applied-plan branches checked against actual saved copper. Planar lengths exclude via barrels; no loop inductance or measured performance inferred.')
(D/'route-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps(dict(protected=len(ss),planned=len(planned),models=len(fm),coupling=screens,drv_mm=drv)))
