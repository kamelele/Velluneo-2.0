"""Concrete, NOT APPROVED, one-pair escape correction candidate. No active edits."""
import json,sys,shutil,hashlib
from pathlib import Path
import pcbnew as k
root=Path(__file__).resolve().parent
S=root/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC08_prototype'
C=S/'.work/routing/critical-thermal-candidate-05'
P=S/'.work/routing/proposed-U1-escape-15mm'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(S/'SC08_prototype.kicad_pcb')=='c503ff1b7660022d665ed4fabbc536c8f05d72899694a1d2da2c8a84ec6357d5'
assert sha(C/'SC08_prototype.kicad_pcb')=='5f82894e6de8fd263dfcb28bf86b09a0b9ea2574095bc47138b61a2c806aaf3a'
assert not P.exists(), 'Preserve previous proposal'
shutil.copytree(C,P)
sys.path.insert(0,str(root/'sc08-route-thermal-plan'))
import native_zone_helpers_owned as zh
assert sha(Path(zh.__file__))=='474a8b0eee2dd6a79514c8f5c2bcd1bc02e7b93453c0e368d3e8ea27685e84ed'
sys.path.insert(0,str(root/'sc08-route-experiment0'))
import adapter as a
W=root/'Velluneo-2.0/hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing'
consumers,sp,receipt=a.validate_customer(S,S/'SC08_prototype.kicad_pcb',W/'authorization-receipt.json')
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(C/'SC08_prototype.kicad_pcb'))
report=json.loads((C/'routing-authoring.json').read_text())
nets=b.GetNetsByName();net='/DRAIN_BLOCKED'
new_tracks=[]
def track(p,q,layer,owner):
    t=k.PCB_TRACK(b);t.SetStart(k.VECTOR2I(*(k.FromMM(v) for v in p)));t.SetEnd(k.VECTOR2I(*(k.FromMM(v) for v in q)));t.SetWidth(k.FromMM(.6));t.SetLayer(layer);t.SetNetCode(nets[net].GetNetCode());b.Add(t)
    new_tracks.append({'uuid':t.m_Uuid.AsString(),'net':net,'layer':b.GetLayerName(layer),'a':list(p),'b':list(q),'width':.6,'owner':owner})
u1=[(107.525,41.905),(107.525,43.65),(105.5,44.15),(104.5,44.0)]
for p,q in zip(u1,u1[1:]):track(p,q,k.F_Cu,['U1','4'])
track((91.015,43),(94,40),k.F_Cu,['D4','1'])
track((94,40),(104.5,44),k.B_Cu,None)
for x,y in [(94,40),(104.5,44)]:
    v=k.PCB_VIA(b);v.SetPosition(k.VECTOR2I(k.FromMM(x),k.FromMM(y)));v.SetWidth(k.FromMM(.8));v.SetDrill(k.FromMM(.3));v.SetViaType(k.VIATYPE_THROUGH);v.SetLayerPair(k.F_Cu,k.B_Cu);v.SetNetCode(nets[net].GetNetCode());b.Add(v)
# Rebuild all four copper zones from actual pads/tracks/vias at the unchanged
# full generic matrix plus0.10mm; zones NEVER inherit any package exception.
for z in list(b.Zones()):
    if not z.GetIsRuleArea():b.Remove(z)
load=lambda p:json.loads((S/p).read_text(encoding='utf-8-sig'))
binding=a.NetBinding(load('pcb-basis/intent-native-net-binding.json'))
_,pads,courts,_=a.export_pcb(S/'SC08_prototype.kicad_pcb',consumers['constraints'])
rules=a.Rules(load('pcb-basis/domain-matrix.json'),load('pcb-basis/routing-and-isolation-proposal.json'),consumers['constraints'],courts,binding,load('pcb-basis/lab-board-boundaries.json'))
zone_areas={}
for name,zn,layer,rect in [('SOURCE-compact','/SOURCE',k.F_Cu,(110.5,35,125.1,49.5)),('U3-front','/DC_RETURN',k.F_Cu,(68,62,88,82)),('U3-back','/DC_RETURN',k.B_Cu,(68,62,88,82))]:
    x0,y0,x1,y1=rect;p=zh.poly_from_rings([[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]])
    items=[pad for f in b.GetFootprints() for pad in f.Pads() if pad.GetLayerSet().Contains(layer)]
    items += [t for t in b.GetTracks() if isinstance(t,k.PCB_VIA) or t.GetLayer()==layer]
    for item in items:
        other=item.GetNetname()
        if not other or other==zn:continue
        q=k.SHAPE_POLY_SET();item.TransformShapeToPolygon(q,layer,0,k.FromMM(.002),k.ERROR_OUTSIDE)
        q.Inflate(k.FromMM(rules.gap(zn,other)+.1),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.002));p.BooleanSubtract(q)
    rings=zh.rings_from_poly(p)
    for oi,vertices in enumerate(rings['outlines_mm']):
        sub=zh.poly_from_rings([vertices],[rings['holes_by_outline_mm'][oi]])
        z=zh.add_solid_zone(b,nets[zn],layer,sub,clearance_mm=.3,min_thickness_mm=.3,name=name+'-'+str(oi))
        zone_areas[z.m_Uuid.AsString()]=sub.Area()
fill=zh.refill_and_report(b);assert fill['fill_return']
assert zh.save_skipping_settings(P/'SC08_prototype.kicad_pcb',b)
saved=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(P/'SC08_prototype.kicad_pcb'))
report['native_track_provenance'].extend(new_tracks)
expected={r['uuid']:r for r in report['native_track_provenance']}
actual={}
for t in saved.GetTracks():
    if isinstance(t,k.PCB_VIA):continue
    r={'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'layer':saved.GetLayerName(t.GetLayer()),'a':[k.ToMM(t.GetStart().x),k.ToMM(t.GetStart().y)],'b':[k.ToMM(t.GetEnd().x),k.ToMM(t.GetEnd().y)],'width':k.ToMM(t.GetWidth())};actual[r['uuid']]=r
assert set(actual)==set(expected)
for uid,r in actual.items():assert all(expected[uid][key]==v for key,v in r.items())
for z in saved.Zones():
    if z.GetIsRuleArea():continue
    assert z.Outline().OutlineCount()==1
    assert abs(z.Outline().Area()-zone_areas[z.m_Uuid.AsString()])/1e12<.00001
    for lay in (k.F_Cu,k.B_Cu):
        if not z.IsOnLayer(lay):continue
        outside=k.SHAPE_POLY_SET(z.GetFilledPolysList(lay));edge=k.SHAPE_POLY_SET(z.Outline());edge.Inflate(k.FromMM(.002),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.001));outside.BooleanSubtract(edge);assert outside.IsEmpty()
report['previous_output_sha256']=report['output_sha256'];report['output_sha256']=sha(P/'SC08_prototype.kicad_pcb')
report['candidate_status']='PROPOSAL ONLY: active1mm exception is violated; requires real approval of one-pair1.5mm correction; not complete routing'
report['tracks']=[{key:r[key] for key in ('net','layer','a','b','width','owner')}|{'kind':'track','uuid':r['uuid']} for r in report['native_track_provenance']]
report['vias']=[{'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'point':[k.ToMM(t.GetPosition().x),k.ToMM(t.GetPosition().y)],'diameter':k.ToMM(t.GetWidth(k.F_Cu)),'drill':k.ToMM(t.GetDrillValue())} for t in saved.GetTracks() if isinstance(t,k.PCB_VIA)];report['via_count']=len(report['vias'])
report['remaining_unconnected_items']='Not yet checked on this proposal'
a.save(P/'routing-authoring.json',report)
correction={'status':'PROPOSED_NOT_APPROVED_NOT_ACTIVE','ref':'U1','pins':['2','4'],'nets':['SENSE_FB','DRAIN_BLOCKED'],'before_escape_margin_mm':1.0,'proposed_escape_margin_mm':1.5,'unchanged_local_floor_mm':1.9,'layers':['F.Cu'],'objects':['pad','track'],'all_other_package_exceptions_unchanged':True,'native_minimum_DRAIN_track_width_mm':.6,'generic_spacing_elsewhere_mm':4,'no_via_or_zone_exception':True,'source_zone_reclipped_mm':4.1,'base_accepted_placement_sha256':receipt['source_board_sha256'],'base_partial_candidate_sha256':sha(C/'SC08_prototype.kicad_pcb'),'proposal_board_sha256':report['output_sha256'],'source_profile_unchanged':True,'requires_owner_decision_before_applying':True}
for n in ('SC08_prototype.kicad_pro','SC08_prototype.kicad_dru'):assert sha(P/n)==sha(S/n)
a.save(P/'proposed-correction.json',correction)
print(json.dumps({'proposal_only':True,'board_sha256':report['output_sha256'],'tracks':len(expected),'vias':len(report['vias']),'active_sources_unchanged':sha(S/'SC08_prototype.kicad_pcb')==receipt['source_board_sha256']}))
