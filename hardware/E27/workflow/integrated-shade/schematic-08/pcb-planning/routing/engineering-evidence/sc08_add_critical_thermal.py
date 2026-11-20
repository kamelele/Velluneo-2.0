"""Root-only experimental thermal copper; full matrix clipping before native fill."""
import json,sys,shutil,hashlib
from pathlib import Path
import pcbnew as k
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'sc08-route-thermal-plan'))
import native_zone_helpers_owned as zh
assert hashlib.sha256(Path(zh.__file__).read_bytes()).hexdigest()=='474a8b0eee2dd6a79514c8f5c2bcd1bc02e7b93453c0e368d3e8ea27685e84ed'
sys.path.insert(0,str(root/'sc08-route-experiment0'))
import adapter as a
S=root/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC08_prototype'
W=root/'Velluneo-2.0/hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing'
consumers,sp,receipt=a.validate_customer(S,S/'SC08_prototype.kicad_pcb',W/'authorization-receipt.json')
src=S/'.work/routing/critical-candidate'; out=S/'.work/routing/critical-thermal-candidate-05'
assert a.file_sha(src/'SC08_prototype.kicad_pcb')=='40d07fa7eb6c90ccd3fd94102102e815edcd682150cb9888c57147787b603fa7'
assert not out.exists(), 'Preserve earlier candidate'
shutil.copytree(src,out)
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(src/'SC08_prototype.kicad_pcb'))
print('Loaded critical candidate',flush=True)
load=lambda p:json.loads((S/p).read_text(encoding='utf-8-sig'))
binding=a.NetBinding(load('pcb-basis/intent-native-net-binding.json'))
_,pads,courts,_=a.export_pcb(S/'SC08_prototype.kicad_pcb',consumers['constraints'])
rules=a.Rules(load('pcb-basis/domain-matrix.json'),load('pcb-basis/routing-and-isolation-proposal.json'),consumers['constraints'],courts,binding,load('pcb-basis/lab-board-boundaries.json'))
nets=b.GetNetsByName()
quiet_points=[(115.85,74.6),(111,79.45),(111,84),(88,84),(83,79)]
quiet_records=[]
for aa,bb in zip(quiet_points,quiet_points[1:]):
    t=k.PCB_TRACK(b);t.SetStart(k.VECTOR2I(*(k.FromMM(v) for v in aa)));t.SetEnd(k.VECTOR2I(*(k.FromMM(v) for v in bb)));t.SetWidth(k.FromMM(.3));t.SetLayer(k.B_Cu);t.SetNetCode(nets['/DC_RETURN'].GetNetCode());b.Add(t)
    quiet_records.append({'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'layer':'B.Cu','a':list(aa),'b':list(bb),'width':.3,'owner':None})
# A short B.Cu bridge joins the two front SOURCE regions separated by the quiet
# SENSE_FB branch. It is a narrow track, not a backside switched-node plane.
for x,y in [(113.75,40.5),(120.5,40.5)]:
    v=k.PCB_VIA(b);v.SetPosition(k.VECTOR2I(k.FromMM(x),k.FromMM(y)));v.SetWidth(k.FromMM(.8));v.SetDrill(k.FromMM(.3));v.SetViaType(k.VIATYPE_THROUGH);v.SetLayerPair(k.F_Cu,k.B_Cu);v.SetNetCode(nets['/SOURCE'].GetNetCode());b.Add(v)
t=k.PCB_TRACK(b);t.SetStart(k.VECTOR2I(k.FromMM(113.75),k.FromMM(40.5)));t.SetEnd(k.VECTOR2I(k.FromMM(120.5),k.FromMM(40.5)));t.SetWidth(k.FromMM(.6));t.SetLayer(k.B_Cu);t.SetNetCode(nets['/SOURCE'].GetNetCode());b.Add(t)
quiet_records.append({'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'layer':'B.Cu','a':[113.75,40.5],'b':[120.5,40.5],'width':.6,'owner':None})
for x in (81,83,85):
    for y in (69,72,75):
        v=k.PCB_VIA(b);v.SetPosition(k.VECTOR2I(k.FromMM(x),k.FromMM(y)));v.SetWidth(k.FromMM(.8));v.SetDrill(k.FromMM(.3));v.SetViaType(k.VIATYPE_THROUGH);v.SetLayerPair(k.F_Cu,k.B_Cu);v.SetNetCode(nets['/DC_RETURN'].GetNetCode());b.Add(v)
clipping=[]
for name,net,layer,rect in [('SOURCE-compact','/SOURCE',k.F_Cu,(110.5,35,125.1,49.5)),('U3-front','/DC_RETURN',k.F_Cu,(68,62,88,82)),('U3-back','/DC_RETURN',k.B_Cu,(68,62,88,82))]:
    print('Preparing zone '+name,flush=True)
    x0,y0,x1,y1=rect;p=zh.poly_from_rings([[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]])
    items=[pad for f in b.GetFootprints() for pad in f.Pads() if pad.GetLayerSet().Contains(layer)]
    items += [t for t in b.GetTracks() if isinstance(t,k.PCB_VIA) or t.GetLayer()==layer]
    count=0
    for item in items:
        other=item.GetNetname()
        if not other or other==net:continue
        gap=rules.gap(net,other)
        q=k.SHAPE_POLY_SET();item.TransformShapeToPolygon(q,layer,0,k.FromMM(.002),k.ERROR_OUTSIDE)
        q.Inflate(k.FromMM(gap+.10),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.002))
        p.BooleanSubtract(q);count+=1
    # KiCad's saved zone format must not be given multiple disjoint outer rings.
    # Keep each connected component in its own native zone, preserving its holes.
    rings=zh.rings_from_poly(p)
    for oi,vertices in enumerate(rings['outlines_mm']):
        sub=zh.poly_from_rings([vertices],[rings['holes_by_outline_mm'][oi]])
        zh.add_solid_zone(b,nets[net],layer,sub,clearance_mm=.3,min_thickness_mm=.3,name=name+'-'+str(oi))
    clipping.append({'zone':name,'net':net,'layer':b.GetLayerName(layer),'bbox_mm':rect,'pre_native_fill_area_mm2':p.Area()/1e12,'foreign_objects_considered':count,'matrix_clearance_margin_mm':.10,'package_exceptions_used':False})
print('Filling native zones',flush=True)
fill=zh.refill_and_report(b)
print('Native fill returned',flush=True)
assert fill['fill_return']
expected_outline_areas={z.m_Uuid.AsString():z.Outline().Area() for z in b.Zones() if not z.GetIsRuleArea()}
assert zh.save_skipping_settings(out/'SC08_prototype.kicad_pcb',b)
saved=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(out/'SC08_prototype.kicad_pcb'))
for z in saved.Zones():
    if z.GetIsRuleArea():continue
    assert abs(z.Outline().Area()-expected_outline_areas[z.m_Uuid.AsString()])/1e12<.00001,'Zone outline changed on native save'
    for lay in (k.F_Cu,k.B_Cu):
        if z.IsOnLayer(lay):
            outside=k.SHAPE_POLY_SET(z.GetFilledPolysList(lay));boundary=k.SHAPE_POLY_SET(z.Outline());boundary.Inflate(k.FromMM(.002),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.001));outside.BooleanSubtract(boundary)
            assert outside.IsEmpty(),'Saved filled copper outside saved zone boundary'
report=load('.work/routing/critical-candidate/routing-authoring.json')
report['native_track_provenance'].extend(quiet_records)
records={r['uuid']:r for r in report['native_track_provenance']}
actual={}
for t in saved.GetTracks():
    if isinstance(t,k.PCB_VIA):continue
    actual[t.m_Uuid.AsString()]={'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'layer':saved.GetLayerName(t.GetLayer()),'a':[k.ToMM(t.GetStart().x),k.ToMM(t.GetStart().y)],'b':[k.ToMM(t.GetEnd().x),k.ToMM(t.GetEnd().y)],'width':k.ToMM(t.GetWidth())}
assert set(actual)==set(records)
for uid,v in actual.items():assert all(records[uid][key]==value for key,value in v.items()),uid
report['previous_output_sha256']=report['output_sha256'];report['output_sha256']=a.file_sha(out/'SC08_prototype.kicad_pcb')
report['provenance_rebinding_basis']='All17 original native track records unchanged; four new B.Cu quiet-return segments and one narrow SOURCE bridge explicitly authored with null owners and checked by UUID/net/layer/endpoints/width; no owner reassignment'
a.save(out/'routing-authoring.json',report)
a.save(out/'thermal-copper-authoring.json',{'scope':'Incomplete candidate; not thermal qualification or stage acceptance','clipping':clipping,'native_fill':fill,'original_accepted_board_unchanged':a.file_sha(S/'SC08_prototype.kicad_pcb')==receipt['source_board_sha256'],'output_sha256':report['output_sha256']})
for n in ('SC08_prototype.kicad_pro','SC08_prototype.kicad_dru'):assert a.file_sha(out/n)==a.file_sha(S/n)
print(json.dumps({'candidate_sha256':report['output_sha256'],'thermal_vias':9,'SOURCE_bridge_vias':2,'solid_copper_zones':len(expected_outline_areas),'clipping':clipping,'saved_outline_and_fill_consistent':True,'source_and_profiles_unchanged':True}))
