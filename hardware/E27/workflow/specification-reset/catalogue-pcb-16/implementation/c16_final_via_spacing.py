from pathlib import Path
import pcbnew as p,json,math
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16';B=D/'design/Velluneo_driver.kicad_pcb';b=p.LoadBoard(str(B));old=(89.,119.9);origin=(89.45,119.8);a=p.VECTOR2I(p.FromMM(old[0]),p.FromMM(old[1]));via=next(t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)and t.GetNetname()=='/SENSE'and t.GetPosition()==a)
obs=[]
for fp in b.GetFootprints():
 for q in fp.Pads():
  if q.GetNetname()!='/SENSE':obs.append((q.GetEffectiveShape(q.GetLayer()),q.GetLayerSet(),q.GetNetname()))
for q in b.GetTracks():
 if q.GetNetname()!='/SENSE':obs.append((q.GetEffectiveShape(p.F_Cu if isinstance(q,p.PCB_VIA)else q.GetLayer()),q.GetLayerSet(),q.GetNetname()))
candidates=[]
stub=p.PCB_TRACK(b);stub.SetLayer(p.F_Cu);stub.SetWidth(p.FromMM(.3));stub.SetStart(p.VECTOR2I(p.FromMM(origin[0]),p.FromMM(origin[1])))
for xi in range(1780,1799):
 for yi in range(2397,2409):
  x,y=xi*.05,yi*.05;pos=p.VECTOR2I(p.FromMM(x),p.FromMM(y));s=p.SHAPE_CIRCLE(pos,p.FromMM(.4));stub.SetEnd(pos);ss=stub.GetEffectiveShape(p.F_Cu)
  if any(q.Collide(s,p.FromMM(.275))or(l.Contains(p.F_Cu)and q.Collide(ss,p.FromMM(.275)))for q,l,net in obs):continue
  candidates.append((math.dist((x,y),origin),x,y))
assert candidates,'No valid local sense via takeoff';_,x,y=min(candidates);new=(x,y);z=p.VECTOR2I(p.FromMM(x),p.FromMM(y))
for t in b.GetTracks():
 if t.GetNetname()!='/SENSE':continue
 if isinstance(t,p.PCB_VIA)and t.GetPosition()==a:t.SetPosition(z)
 elif not isinstance(t,p.PCB_VIA):
  if t.GetStart()==a:t.SetStart(z)
  if t.GetEnd()==a:t.SetEnd(z)
p.SaveBoard(str(B),b)
j=json.loads((D/'route-plan.json').read_text());oa=[v-100 for v in old];na=[v-100 for v in new]
for q in j['elements']:
 if q['net']=='SENSE':
  if math.dist(q['a'],oa)<1e-6:q['a']=na
  if math.dist(q['b'],oa)<1e-6:q['b']=na
j['post_route_correction']['new_via_mm']=new;j['post_route_correction']['selection']='Native effective-shape scan of local grid, minimum0.275mm other-net clearance for via and front stub; final full native DRC remains authoritative.'
(D/'route-plan.json').write_text(json.dumps(j,indent=2)+'\n');print('Native-shape selected Kelvin takeoff',new)
