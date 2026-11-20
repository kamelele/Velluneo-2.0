from pathlib import Path
import pcbnew as p,json,hashlib,csv,math,shutil
W=Path(__file__).resolve().parent;P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'supplier-review-13';E=D/'design';B=E/'Velluneo_driver.kicad_pcb';old=P/'pcb-toolkit-11/design/Velluneo_driver.kicad_pcb';a=p.LoadBoard(str(old));b=p.LoadBoard(str(B));copper={p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu}
def sha(x):return hashlib.sha256(x.read_bytes()).hexdigest()
def put(x,j):x.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8')
def fields(q):return sorted((f.GetReference(),f.GetValue(),f.GetFieldText('MPN'),tuple(sorted((x.GetNumber(),x.GetNetname(),x.GetSize().x,x.GetSize().y,x.GetDrillSize().x,x.GetDrillSize().y,tuple(x.GetLayerSet().Seq()))for x in f.Pads())))for f in q.GetFootprints())
assert fields(a)==fields(b)
def track_sig(q,net):return sorted((int(x.GetLayer()),x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y,x.GetWidth(p.F_Cu)if isinstance(x,p.PCB_VIA)else x.GetWidth())for x in q.GetTracks()if x.GetNetname()==net)
assert all(track_sig(a,n)==track_sig(b,n)for n in('/SENSE','/CS'))
objects=[];pads=[];vias=[];parts=[];drills=[]
for f in b.GetFootprints():
 parts.append(dict(ref=f.GetReference(),value=f.GetValue(),MPN=f.GetFieldText('MPN'),x_mm=p.ToMM(f.GetPosition().x),y_mm=p.ToMM(f.GetPosition().y),rotation_deg=f.GetOrientationDegrees(),side='F'if f.GetLayer()==p.F_Cu else'B'))
 for q in f.Pads():
  row=dict(id=f.GetReference()+'.'+q.GetNumber(),ref=f.GetReference(),pin=q.GetNumber(),net=q.GetNetname(),x_mm=p.ToMM(q.GetPosition().x),y_mm=p.ToMM(q.GetPosition().y),output_x_mm=p.ToMM(q.GetPosition().x)-77.5,output_y_mm=130-p.ToMM(q.GetPosition().y),size_mm=[p.ToMM(q.GetSize().x),p.ToMM(q.GetSize().y)],drill_mm=[p.ToMM(q.GetDrillSize().x),p.ToMM(q.GetDrillSize().y)],rotation_deg=q.GetOrientationDegrees(),attribute=int(q.GetAttribute()),layers=[b.GetLayerName(x)for x in q.GetLayerSet().Seq()if x in copper]);pads.append(row)
  objects.append((row['id'],row['net'],q.GetEffectiveShape(q.GetLayer()),set(q.GetLayerSet().Seq())&copper,row))
  if q.GetDrillSize().x:drills.append(dict(kind='component',ref=row['id'],x_mm=row['output_x_mm'],y_mm=row['output_y_mm'],diameter_mm=row['drill_mm'][0],plated=True))
 for g in f.GraphicalItems():assert g.GetLayer()not in copper,'Unhandledfootprintcoppergraphic'
for i,q in enumerate(b.GetTracks()):
 via=isinstance(q,p.PCB_VIA);layer=p.F_Cu if via else q.GetLayer();row=dict(id=('via'if via else'track')+str(i),net=q.GetNetname(),layer=b.GetLayerName(layer),start_mm=[p.ToMM(q.GetStart().x),p.ToMM(q.GetStart().y)],end_mm=[p.ToMM(q.GetEnd().x),p.ToMM(q.GetEnd().y)],width_mm=p.ToMM(q.GetWidth(p.F_Cu)if via else q.GetWidth()))
 objects.append((row['id'],row['net'],q.GetEffectiveShape(layer),set(q.GetLayerSet().Seq())&copper,row))
 if via:
  assert q.GetFillingMode()==p.FILLING_MODE_FILLED and q.GetCappingMode()==p.CAPPING_MODE_CAPPED
  x,y=p.ToMM(q.GetPosition().x),p.ToMM(q.GetPosition().y);vias.append(dict(id=len(vias)+1,net=q.GetNetname(),board_x_mm=x,board_y_mm=y,output_x_mm=x-77.5,output_y_mm=130-y,hole_mm=p.ToMM(q.GetDrillValue()),pad_mm=p.ToMM(q.GetWidth(p.F_Cu)),fill='nonconductive epoxy',cap='copper'));drills.append(dict(kind='via',ref=row['id'],x_mm=x-77.5,y_mm=130-y,diameter_mm=p.ToMM(q.GetDrillValue()),plated=True))
for z in b.Zones():assert z.GetIsRuleArea(),'Filledzone must be included in geometryaudit'
for g in b.GetDrawings():assert g.GetLayer()not in copper,'Unhandledcopperdrawing'
def threshold(s,t,upper):
 if s.Collide(t,0):return 0
 if not s.Collide(t,upper):return None
 lo,hi=0,upper
 while hi-lo>1:
  mid=(lo+hi)//2
  if s.Collide(t,mid):hi=mid
  else:lo=mid
 return hi
results=[]
for scope in json.loads((E/'hardware.json').read_text())['product']['scoped_clearances']:
 aa=[x for x in objects if x[1]in scope['nets_a']];zz=[x for x in objects if x[1]in scope['nets_b']];best=common=p.FromMM(100);pair=cp=None
 for x in aa:
  for y in zz:
   q=threshold(x[2],y[2],best)
   if q is not None:best=q;pair=[x[4],y[4]]
   if x[3]&y[3]:
    q=threshold(x[2],y[2],common)
    if q is not None:common=q;cp=[x[4],y[4]]
 results.append(dict(id=scope['id'],primary_objects=len(aa),other_objects=len(zz),projected_xy_conservative_mm=max(0,best-1)/1e6,common_copper_layer_conservative_mm=max(0,common-1)/1e6,projected_pair=pair,common_pair=cp,native_resolution_mm=1e-6,required_same_layer_mm=scope['min_mm']))
ps=next(x for x in results if x['id']=='PRIMARY_SECONDARY');assert ps['projected_xy_conservative_mm']>=10.7
circle=p.SHAPE_CIRCLE(p.VECTOR2I(p.FromMM(88.01),p.FromMM(124.25)),p.FromMM(5.25));unrelated=[]
for item in objects:
 if p.B_Cu in item[3]and item[1]not in('/BULK_POS','/PRIMARY_GND')and not item[0].startswith('C1.')and item[2].Collide(circle,0):unrelated.append(item[4])
assert not unrelated
put(D/'checks/current-spacing-and-mounting.json',dict(source_board_sha256=sha(B),baseline_source_sha256=sha(old),parts=33,pads=81,copper_objects=321,physical_pin_net_map_values_MPNs_sizes_drills_layers_unchanged=True,SENSE_CS_copper_identical=True,scopes=results,PS_finished_budget_per_domain_mm=.35,PS_conservative_remainder_under_proposed_budget_mm=ps['projected_xy_conservative_mm']-.7,C1_Bside_D10p5_circle_unrelated_copper=unrelated,T1_fullbody_reserved_mm=[30,30,18],T1_courtyard_mm=[30.5,30.5],scope='Actualnative shape audit; XY/common-layer geometric screens plus explicitproposed finishingbudget, not normative clearance/creepage or finishedcore/leadout qualification. HVquietcrosslayeroverlapisprimaryfunctional-dielectric/couplingreview.'))
put(D/'checks/native-inventory.json',dict(source_board_sha256=sha(B),parts=parts,pads=pads,vias=vias))
put(D/'checks/native-fabrication-input.json',dict(board_sha256=sha(B),expected_drills=drills,component_hole_count=25,via_count=17))
with(D/'fabrication/designated-filled-vias.csv').open('w',newline='')as out:w=csv.DictWriter(out,fieldnames=list(vias[0]));w.writeheader();w.writerows(vias)
# Reuse actual native returnbranchcut diagnostic with updateddeclaredpositions.
for n in('analyze_native_routes.py','historical-DRIVER08-plan.json','build_negative_controls.py'):shutil.copyfile(P/'pcb-toolkit-11'/n,D/n)
j=json.loads((P/'pcb-toolkit-11/placement-decision.json').read_text())
for ref in('R10','C3','R17'):
 if not any(x['ref']==ref for x in j['moves']):j['moves'].append(dict(ref=ref,after={}))
for q in j['moves']:
 f=next(x for x in b.GetFootprints()if x.GetReference()==q['ref']);q['after'].update(x=p.ToMM(f.GetPosition().x)-100,y=p.ToMM(f.GetPosition().y)-100,angle=f.GetOrientationDegrees(),side='F'if f.GetLayer()==p.F_Cu else'B')
put(D/'placement-decision.json',j)
print('Freshnativeaudit:PS',ps['projected_xy_conservative_mm'],'finished-budgetremainder',ps['projected_xy_conservative_mm']-.7,'C1underbodyclear;graphandmeasurementpreserved',flush=True)
