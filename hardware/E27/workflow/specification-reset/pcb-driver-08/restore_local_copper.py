"""Preserve local decoupling/distribution and clamp return while rerouting moved terminals."""
from pathlib import Path
import pcbnew,json,hashlib
D=Path(__file__).resolve().parent;E=D/'design';B=D.parent/'pcb-route-07';profile=(E/'Velluneo_driver.kicad_pro').read_bytes();src=D/'.work/power-first-ripped.kicad_pcb'
for ext in('.kicad_pro','.kicad_dru','.kicad_sch'):(src.with_suffix(ext)).write_bytes((E/('Velluneo_driver'+ext)).read_bytes())
b=pcbnew.LoadBoard(str(src));mp=json.loads((E/'full-build-result.json').read_text())['logical_to_native_netnames'];nets=b.GetNetsByName();layers=[pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu];plan=json.loads((B/'four-layer-plan.json').read_text());keep=[];g=json.loads((B/'ground-plan.json').read_text())
# Retain exact local branches, not the old long trunk/distribution geometry.
runs=[]
for e in plan['new_elements']:
 if not runs or e['net']!=runs[-1][-1]['net']or e['label']!=runs[-1][-1]['label']or sum((a-z)**2 for a,z in zip(e['a'],runs[-1][-1]['b']))>1e-10:runs.append([])
 runs[-1].append(e)
for run in runs:
 net,label=run[0]['net'],run[0]['label']
 if net=='VDD'and label in{'local_VDD','VDD_fine_escape','bias_VDD'}:keep.extend(run)
 if net=='PRIMARY_GND'and label in{'aux_branch','shunt_return','quiet_ground'}:
  if label=='quiet_ground'and sum((a-z)**2 for a,z in zip(run[0]['a'],[-14.49,24.25]))<1e-8:continue
  keep.extend(dict(e,width=1.8 if label=='shunt_return'and not e['via']else e['width'])for e in run)
for k,es in g['active_routes'].items():
 if g['tasks'][int(k)]['label']!='clamp_bulk_return':continue
 for e in es:keep.append(dict(e,layers=[0,1,2,3]if e['via']else[0 if l==0 else 3 for l in e['layers']]))
def v(p):return pcbnew.VECTOR2I(pcbnew.FromMM(100+p[0]),pcbnew.FromMM(100+p[1]))
seen=set()
for e in keep:
 if e['via']:
  key=(e['net'],*e['a'])
  if key in seen:continue
  seen.add(key);t=pcbnew.PCB_VIA(b);t.SetPosition(v(e['a']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetDrill(pcbnew.FromMM(.3));t.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);t.SetViaType(pcbnew.VIATYPE_THROUGH)
 else:t=pcbnew.PCB_TRACK(b);t.SetStart(v(e['a']));t.SetEnd(v(e['b']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetLayer(layers[e['layers'][0]])
 t.SetNetCode(nets[mp[e['net']]].GetNetCode());b.Add(t)
# Widen the short shunt-to-bulk return without moving its junction.
widen=[]
for t in b.GetTracks():
 if isinstance(t,pcbnew.PCB_VIA)or t.GetNetname()!='/PRIMARY_GND':continue
 if abs(pcbnew.ToMM(t.GetWidth())-1.)<1e-6:
  t.SetWidth(pcbnew.FromMM(1.8))
 if abs(pcbnew.ToMM(t.GetWidth())-1.8)<1e-6:widen.append(dict(a=[pcbnew.ToMM(t.GetStart().x)-100,pcbnew.ToMM(t.GetStart().y)-100],b=[pcbnew.ToMM(t.GetEnd().x)-100,pcbnew.ToMM(t.GetEnd().y)-100],width_mm=1.8))
assert len(widen)==3,widen
out=E/'Velluneo_driver.kicad_pcb';pcbnew.SaveBoard(str(out),b);(E/'Velluneo_driver.kicad_pro').write_bytes(profile)
(D/'protected-local-copper.json').write_text(json.dumps(dict(source_plan_sha256=hashlib.sha256((B/'four-layer-plan.json').read_bytes()).hexdigest(),elements=keep,widened_shunt_return=widen,scope='Existing local bypass, supply distribution and clamp return restored; changed terminal branches remain to route. Shared C1 star retained per exact-device layout guidance.'),indent=2)+'\n');print('Protectedlocalcopper restored; shuntstrap1.8mm',len(widen))
