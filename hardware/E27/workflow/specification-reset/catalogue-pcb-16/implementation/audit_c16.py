from pathlib import Path
import pcbnew as p,json,hashlib,ast
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16';E=D/'design';B=E/'Velluneo_driver.kicad_pcb';b=p.LoadBoard(str(B));copper={p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu};objects=[];parts=[];pads=[];vias=[]
for f in b.GetFootprints():
 parts.append(dict(ref=f.GetReference(),value=f.GetValue(),mpn=f.GetFieldText('MPN'),footprint=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),xy_mm=[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)],side='F.Cu'if f.GetLayer()==p.F_Cu else'B.Cu',rotation_deg=f.GetOrientationDegrees()))
 for q in f.Pads():
  row=dict(id=f.GetReference()+'.'+q.GetNumber(),net=q.GetNetname(),xy_mm=[p.ToMM(q.GetPosition().x),p.ToMM(q.GetPosition().y)],size_mm=[p.ToMM(q.GetSize().x),p.ToMM(q.GetSize().y)],hole_mm=p.ToMM(q.GetDrillSize().x));pads.append(row);objects.append((row['id'],row['net'],q.GetEffectiveShape(q.GetLayer()),set(q.GetLayerSet().Seq())&copper,row))
for i,q in enumerate(b.GetTracks()):
 via=isinstance(q,p.PCB_VIA);l=p.F_Cu if via else q.GetLayer();row=dict(id=('via'if via else'track')+str(i),net=q.GetNetname(),layer=b.GetLayerName(l),a=[p.ToMM(q.GetStart().x),p.ToMM(q.GetStart().y)],b=[p.ToMM(q.GetEnd().x),p.ToMM(q.GetEnd().y)],width_mm=p.ToMM(q.GetWidth(p.F_Cu)if via else q.GetWidth()));objects.append((row['id'],row['net'],q.GetEffectiveShape(l),set(q.GetLayerSet().Seq())&copper,row))
 if via:vias.append(dict(**row,hole_mm=p.ToMM(q.GetDrillValue()),filling_mode=int(q.GetFillingMode()),capping_mode=int(q.GetCappingMode())))
tree=ast.parse((W/'audit_rfq13_native.py').read_text())
for n in tree.body:
 if isinstance(n,ast.FunctionDef)and n.name=='threshold':exec(compile(ast.Module(body=[n],type_ignores=[]),'native threshold','exec'))
results=[]
for scope in json.loads((E/'hardware.json').read_text(encoding='utf-8-sig'))['product']['scoped_clearances']:
 aa=[x for x in objects if x[1]in scope['nets_a']];zz=[x for x in objects if x[1]in scope['nets_b']];best=common=p.FromMM(100);pair=cp=None
 for x in aa:
  for y in zz:
   z=threshold(x[2],y[2],best)
   if z is not None:best=z;pair=[x[4],y[4]]
   if x[3]&y[3]:
    z=threshold(x[2],y[2],common)
    if z is not None:common=z;cp=[x[4],y[4]]
 results.append(dict(id=scope['id'],projected_mm=max(0,best-1)/1e6,same_layer_mm=max(0,common-1)/1e6,projected_pair=pair,same_layer_pair=cp,required_same_layer_mm=scope['min_mm']))
cap=next(f for f in b.GetFootprints()if f.GetReference()=='C1');circle=p.SHAPE_CIRCLE(cap.GetPosition(),p.FromMM(5.25));under=[x[4]for x in objects if cap.GetLayer()in x[3]and x[1]not in('/BULK_POS','/PRIMARY_GND')and not x[0].startswith('C1.')and x[2].Collide(circle,0)]
report=dict(source_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),parts=parts,pads=pads,vias=vias,copper_object_count=len(list(b.GetTracks())),scopes=results,C1_body_side=b.GetLayerName(cap.GetLayer()),C1_body_side_unrelated_copper=under,scope='Actual native effective-shape distances and actual CAD inventory; geometric checks do not prove leakage, EMI, thermal or normative isolation.')
(D/'checks/native-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('native scopes',[(x['id'],x['projected_mm'],x['same_layer_mm'])for x in results],'C1 unrelated',len(under),flush=True)
