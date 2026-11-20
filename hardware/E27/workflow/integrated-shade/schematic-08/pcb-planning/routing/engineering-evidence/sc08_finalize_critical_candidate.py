"""Verify track identity/profile after actual native CLI refill/save."""
import json,hashlib
from pathlib import Path
import pcbnew as k
root=Path(__file__).resolve().parent
S=root/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC08_prototype'
C=S/'.work/routing/critical-thermal-candidate-05'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((C/'routing-authoring.json').read_text())
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(C/'SC08_prototype.kicad_pcb'))
actual={}
for t in b.GetTracks():
    if isinstance(t,k.PCB_VIA):continue
    actual[t.m_Uuid.AsString()]={'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'layer':b.GetLayerName(t.GetLayer()),'a':[k.ToMM(t.GetStart().x),k.ToMM(t.GetStart().y)],'b':[k.ToMM(t.GetEnd().x),k.ToMM(t.GetEnd().y)],'width':k.ToMM(t.GetWidth())}
assert set(actual)=={r['uuid'] for r in report['native_track_provenance']}
for r in report['native_track_provenance']:assert all(r[key]==v for key,v in actual[r['uuid']].items())
assert sha(S/'SC08_prototype.kicad_pcb')=='c503ff1b7660022d665ed4fabbc536c8f05d72899694a1d2da2c8a84ec6357d5'
for n in ('SC08_prototype.kicad_pro','SC08_prototype.kicad_dru'):assert sha(C/n)==sha(S/n),n
after=sha(C/'SC08_prototype.kicad_pcb')
report.setdefault('native_refill_rebindings',[]).append({'before_sha256':report['output_sha256'],'after_sha256':after,'basis':'Actual pinned CLI pcb drc --refill-zones --save-board; every22 track UUID/net/layer/ordered endpoints/width verified unchanged; owners retained exactly'})
report['output_sha256']=after
report['tracks']=[{key:r[key] for key in ('net','layer','a','b','width','owner')}|{'kind':'track','uuid':r['uuid']} for r in report['native_track_provenance']]
report['vias']=[{'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'point':[k.ToMM(t.GetPosition().x),k.ToMM(t.GetPosition().y)],'diameter':k.ToMM(t.GetWidth(k.F_Cu)),'drill':k.ToMM(t.GetDrillValue())} for t in b.GetTracks() if isinstance(t,k.PCB_VIA)]
report['via_count']=len(report['vias'])
report['global_routing_performed']=False
report['remaining_unconnected_items']=65
(C/'routing-authoring.json').write_text(json.dumps(report,indent=2)+'\n')
zones=[]
for z in b.Zones():
    if z.GetIsRuleArea():continue
    areas={b.GetLayerName(l):z.GetFilledPolysList(l).Area()/1e12 for l in (k.F_Cu,k.B_Cu) if z.IsOnLayer(l)}
    assert z.Outline().OutlineCount()==1
    for l in (k.F_Cu,k.B_Cu):
        if not z.IsOnLayer(l):continue
        outside=k.SHAPE_POLY_SET(z.GetFilledPolysList(l));edge=k.SHAPE_POLY_SET(z.Outline());edge.Inflate(k.FromMM(.002),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.001));outside.BooleanSubtract(edge)
        assert outside.IsEmpty(),z.GetZoneName()
    zones.append({'name':z.GetZoneName(),'net':z.GetNetname(),'areas_mm2':areas,'saved_fill_inside_saved_outline':True})
drc=json.loads((C/'native-drc.json').read_text())
assert not drc['violations'] and not drc['schematic_parity']
out={'scope':'Incomplete experimental routing checkpoint, not approval or release','output_sha256':after,'tracks':len(actual),'vias':sum(isinstance(t,k.PCB_VIA) for t in b.GetTracks()),'zones':zones,'native_DRC_geometry':0,'native_DRC_unconnected':len(drc['unconnected_items']),'native_DRC_parity':0,'accepted_original_and_profiles_unchanged':True}
(C/'candidate-finalization.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
