"""Root-only integration of already native/refill and matrix-checked saved CAD."""
from pathlib import Path
import json, hashlib, shutil, sys, math
import pcbnew as k
root=Path(__file__).resolve().parent;R=root/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype'
W=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing';F=W/'final-routing';V=S/'routing-verification';F.mkdir(exist_ok=True);V.mkdir(exist_ok=True)
C=S/'.work/routing/route2-final-06';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sys.path.insert(0,str(root/'sc08-route-validator'));import checker
assert sha(C/'SC08_prototype.kicad_pcb')=='bddb0838b0b27a542cdc509b4d621220da3febf53ecc31e799c87fca87a34dad'
assert load(C/'full-matrix-final.json')['passed']
drc=load(C/'native-final-check.json');assert all(not drc[x] for x in ['violations','unconnected_items','schematic_parity'])
b=checker.load_native(C/'SC08_prototype.kicad_pcb');old=checker.load_native(W/'adoption/before-adoption/SC08_prototype.kicad_pcb')
def geom(board):
 out={}
 for f in board.GetFootprints():
  out[f.GetReference()]={'uuid':f.m_Uuid.AsString(),'position':checker.point(f.GetPosition()),'rotation':f.GetOrientationDegrees(),'layer':int(f.GetLayer()),'value':f.GetValue(),'footprint':str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),'properties':{x.GetName():x.GetText() for x in f.GetFields()},'pads':sorted([{'uuid':p.m_Uuid.AsString(),'number':p.GetNumber(),'net':p.GetNetname(),'position':checker.point(p.GetPosition()),'rotation':p.GetOrientationDegrees(),'size':checker.point(p.GetSize()),'drill':checker.point(p.GetDrillSize()),'shape':int(p.GetShape()),'attribute':int(p.GetAttribute()),'layers':list(p.GetLayerSet().Seq())} for p in f.Pads()],key=lambda p:p['uuid'])}
 return out
assert geom(b)==geom(old);assert len(geom(b))==47
for name in ['SC08_prototype.kicad_pro','SC08_prototype.kicad_dru']:assert (C/name).read_bytes()==(S/name).read_bytes()==(W/'adoption/before-adoption'/name).read_bytes()
assert sha(S/'SC08_prototype.kicad_sch')=='824f61643e8026518b8bdd07ab2df40c6d71d79bf3391c722699126a648f0395'
author=load(C/'routing-authoring.json');assert author['output_sha256']==sha(C/'SC08_prototype.kicad_pcb')
assert len(author['native_track_provenance'])==957 and len(author['native_via_provenance'])==54
author['tracks']=author['native_track_provenance'];author['track_count']=957;author['vias']=author['native_via_provenance'];author['via_count']=54
author['integration_status']='Native all-net continuity/parity and full-matrix checks passed; stage approval remains pending.'
author['claims_complete']=True
author['historical_search_events_note']='Search port/deferred events are retained as history; final native DRC and saved-copper matrix establish actual completeness. Root manually routed DC_RETURN and relay branches; redundant newly generated non-target anchors removed without removing accepted seed objects.'
save(V/'routing-authoring.json',author)
check=checker.Checker(b,checker.Contract(S),author);check.collect();assert not check.findings
dc=[o for o in check.objects if o.native_net=='/DC_RETURN']
# Build a geometric graph, with each disjoint filled-zone island independent.
items=[]
for o in dc:
 for i in range(o.shape.OutlineCount()):
  poly=k.SHAPE_POLY_SET();poly.AddOutline(o.shape.COutline(i))
  for h in range(o.shape.HoleCount(i)):poly.AddHole(o.shape.CHole(i,h),0)
  items.append({'object':o,'poly':poly,'island':i})
def components(remove_star=False):
 active=[i for i,x in enumerate(items) if not(remove_star and x['object'].kind=='pad' and x['object'].id=='C5.2')];parent={i:i for i in active}
 def find(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 def union(i,j):parent[find(i)]=find(j)
 for n,i in enumerate(active):
  a=items[i];oa=a['object']
  for j in active[n+1:]:
   d=items[j];ob=d['object']
   if oa.layer==ob.layer and checker.close(a['poly'],d['poly'],0):union(i,j)
   elif oa.uuid==ob.uuid and oa.layer!=ob.layer and (oa.kind=='via' or oa.kind=='pad' and oa.source.GetAttribute()==k.PAD_ATTRIB_PTH):union(i,j)
 pins={}
 for i in active:
  o=items[i]['object']
  if o.kind=='pad':pins.setdefault(o.id,set()).add(find(i))
 return pins,len({find(i) for i in active})
pins,normal_components=components();assert normal_components==1,(normal_components,pins)
cut,cut_components=components(True)
main={'BR1.3','C1.2','C2.2','D3.2','D1.2','J2.2','R8.2','R9.2'};quiet={'U2.2','U2.3','C9.2','R15.2','R23.2','U3.2','R17.2','U4.2','U5.2'}
ma=set().union(*(cut[x] for x in main));qu=set().union(*(cut[x] for x in quiet))
assert not(ma&qu),{'main':ma,'quiet':qu,'cut_components':cut_components}
topology={'board_sha256':sha(C/'SC08_prototype.kicad_pcb'),'method':'Actual copper polygons per layer; every disjoint zone island separate; physical PTH/via cross-layer bridges only; remove both C5.2 pad faces/barrel in second pass. Conservative outward native polygon error 0.002 mm, zero contact threshold.','normal_DC_RETURN_components':normal_components,'after_C5_negative_pad_removal_components':cut_components,'main_pins':sorted(main),'quiet_pins':sorted(quiet),'main_and_quiet_separate_without_C5_pad':True,'source_control_branch':'U4.4 SOURCE clamp feed uses 0.3mm track, through .8/.3 via98.9,34 to C3-return via110.3,36.1; R3/R4 relay series resistors remain intact. This control branch is not main switching-current route. Main Source tracks remain0.6mm/plane.','C3_BP_connection_length_mm':math.dist((107.525,38.095),(109.05,35.9)),'U3_thermal_vias':10,'thermal_via_diameter_drill_mm':[.8,.3],'thermal_zone_areas_mm2':[{'net':o.native_net,'layer':o.layer,'area_mm2':o.shape.Area()/1e12,'uuid':o.id} for o in check.objects if o.kind=='zone'],'thetaJA85_K_per_W':'Conditional design target only, not demonstrated by copper or via count.','limits':'No switching waveform, thermal, impulse or fault behavior has been measured.'}
save(V/'return-and-thermal-routing-review.json',topology)
save(V/'placement-invariance.json',{'passed':True,'board_sha256':sha(C/'SC08_prototype.kicad_pcb'),'accepted_placement_board_sha256':sha(W/'adoption/before-adoption/SC08_prototype.kicad_pcb'),'unchanged':'47refs/values/MPN properties/footprint IDs/positions/rotations/layers/UUIDs; all pad numbers/nets/shapes/sizes/drills/rotations/positions/layers/UUIDs; unchanged native pro/dru and schematic.','schematic_sha256':sha(S/'SC08_prototype.kicad_sch'),'tracks':957,'vias':54,'filled_copper_zone_count':sum(not z.GetIsRuleArea() for z in b.Zones()),'managed_rule_area_count':sum(z.GetIsRuleArea() for z in b.Zones())})
assert sha(S/'SC08_prototype.kicad_pcb')=='9db429f38c0c7e3c668fa3d1d3452143365a825cea56a603104573382dd008a9'
shutil.copy2(S/'SC08_prototype.kicad_pcb',W/'adoption/integrated-approved-seed.kicad_pcb')
shutil.copy2(C/'SC08_prototype.kicad_pcb',S/'SC08_prototype.kicad_pcb')
shutil.copy2(C/'native-final-check.json',V/'native-drc.json')
shutil.copy2(C/'thermal-fill-authoring.json',V/'thermal-fill-authoring.json')
for src,dst in [(root/'sc08-route-validator/checker.py',V/'saved_copper_checker.py'),(root/'sc08-routing-adapter/adapter.py',V/'routing_adapter.py'),(root/'sc08-adoption-tool-review/RC-ROUTE-DRAIN-01-closure.json',V/'input-adoption-independent-closure.json'),(root/'sc08-adoption-tool-review/boundary-envelope-review.json',V/'checker-boundary-independent-review.json'),(root/'sc08-adoption-tool-review/tooling-adoption-review.json',V/'tooling-adoption-independent-review.json')]:shutil.copy2(src,dst)
print(json.dumps({'integrated_board_sha256':sha(S/'SC08_prototype.kicad_pcb'),'return_star_verified':True,'normal_DC_components':normal_components,'cut_DC_components':cut_components,'thermal_areas':topology['thermal_zone_areas_mm2']}))

