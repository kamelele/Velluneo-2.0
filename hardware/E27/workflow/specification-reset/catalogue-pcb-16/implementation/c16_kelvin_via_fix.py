from pathlib import Path
import pcbnew as p,json,math
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16';B=D/'design/Velluneo_driver.kicad_pcb';old=(89.45,119.8);new=(89,119.9);b=p.LoadBoard(str(B));a=p.VECTOR2I(p.FromMM(old[0]),p.FromMM(old[1]));z=p.VECTOR2I(p.FromMM(new[0]),p.FromMM(new[1]));count=0
for t in b.GetTracks():
 if t.GetNetname()!='/SENSE':continue
 if isinstance(t,p.PCB_VIA)and t.GetPosition()==a:t.SetPosition(z);count+=1
 elif not isinstance(t,p.PCB_VIA):
  if t.GetStart()==a:t.SetStart(z)
  if t.GetEnd()==a:t.SetEnd(z)
assert count==1
t=p.PCB_TRACK(b);t.SetStart(a);t.SetEnd(z);t.SetWidth(p.FromMM(.3));t.SetLayer(p.F_Cu);t.SetNet(next(n for n in b.GetNetsByNetcode().values()if n.GetNetname()=='/SENSE'));b.Add(t);p.SaveBoard(str(B),b)
j=json.loads((D/'route-plan.json').read_text());oa=[v-100 for v in old];na=[v-100 for v in new]
def same(v):return math.dist(v,oa)<1e-6
for q in j['elements']:
 if q['net']=='SENSE':
  if same(q['a']):q['a']=na
  if same(q['b']):q['b']=na
j['elements'].append(dict(net='SENSE',a=oa,b=na,width=.3,layers=[0],via=False,family='kelvin',label='R6 Kelvin pad-to-offset-via local correction'))
j['post_route_correction']=dict(old_via_mm=old,new_via_mm=new,reason='Original seed via approached C2 ground corner to0.1315mm; offset to clear0.25mm without changing the shunt Kelvin net or R6 position.',native_DRC_required=True)
(D/'route-plan.json').write_text(json.dumps(j,indent=2)+'\n');print('Kelvin seed via corrected; explicit front pad stub added')
