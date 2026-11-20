"""Separate active-contract test and explicit counterfactual ONE-pair proposal."""
import copy,json,hashlib,sys
from pathlib import Path
import pcbnew as k
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'sc08-route-validator'))
import checker
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Path(checker.__file__))=='8878e6b90b8bb1ed78cc5da2c1ad37f1778e34344fa631429cc4a94b084c3491'
S=root/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC08_prototype'
P=S/'.work/routing/proposed-U1-escape-15mm'
board=P/'SC08_prototype.kicad_pcb';prov=P/'routing-authoring.json'
author=json.loads(prov.read_text())
# CLI refill/save may only preserve authored track identity; never refresh owners.
b=checker.load_native(board);records={r['uuid']:r for r in author['native_track_provenance']};actual={}
for t in b.GetTracks():
    if isinstance(t,k.PCB_VIA):continue
    r={'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'layer':b.GetLayerName(t.GetLayer()),'a':[k.ToMM(t.GetStart().x),k.ToMM(t.GetStart().y)],'b':[k.ToMM(t.GetEnd().x),k.ToMM(t.GetEnd().y)],'width':k.ToMM(t.GetWidth())};actual[r['uuid']]=r
assert set(records)==set(actual)
for uid,r in actual.items():assert all(records[uid][key]==value for key,value in r.items())
author['output_sha256']=sha(board);author['remaining_unconnected_items']=64
prov.write_text(json.dumps(author,indent=2)+'\n')
contract=checker.Contract(S)
active=checker.check_saved(board,contract,prov)
(P/'active-contract-check.json').write_text(json.dumps(active,indent=2)+'\n')
assert not active['passed'] and not active.get('stopped'), 'Discriminating control must fail geometrically under active1mm scope'
proposal=copy.deepcopy(contract)
changed=[]
for e in proposal.exceptions:
    if e['ref']=='U1' and set(e['pins'])=={'2','4'}:
        assert e['escape_margin_mm']==1 and e['proposed_drawn_floor_mm']==1.9
        before=copy.deepcopy(e);e['escape_margin_mm']=1.5;changed.append({'before':before,'proposed':copy.deepcopy(e)})
assert len(changed)==1
BaseChecker=checker.Checker
class OnePairProposalChecker(BaseChecker):
    def exception_region(self,e):
        if e['ref']=='U1' and set(e['pins'])=={'2','4'} and e['escape_margin_mm']==1.5:
            region=k.SHAPE_POLY_SET(self.courts['U1'])
            region.Inflate(checker.mm(1.5-2*checker.ERROR_MM),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,checker.mm(checker.ERROR_MM))
            return region
        return super().exception_region(e)
checker.Checker=OnePairProposalChecker
r=checker.check_saved(board,proposal,prov)
assert r['passed'],json.dumps(r.get('findings',r.get('error')))
r['proposed_geometry_passed']=r.pop('passed')
r.update(status='COUNTERFACTUAL_PROPOSAL_ONLY_NOT_APPROVED_NOT_ACTIVE',active_contract_passed=False,proposal_runner_sha256=sha(Path(__file__)),exact_one_pair_change=changed,owner_approval_required=True,qualification=False)
(P/'proposed-contract-check.json').write_text(json.dumps(r,indent=2)+'\n')
zones=[]
for z in b.Zones():
    if z.GetIsRuleArea():continue
    assert z.Outline().OutlineCount()==1
    areas={}
    for lay in (k.F_Cu,k.B_Cu):
        if not z.IsOnLayer(lay):continue
        p=k.SHAPE_POLY_SET(z.GetFilledPolysList(lay));edge=k.SHAPE_POLY_SET(z.Outline());edge.Inflate(k.FromMM(.002),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.001));outside=k.SHAPE_POLY_SET(p);outside.BooleanSubtract(edge);assert outside.IsEmpty();areas[b.GetLayerName(lay)]=p.Area()/1e12
    zones.append({'name':z.GetZoneName(),'net':z.GetNetname(),'filled_areas_mm2':areas,'saved_fill_inside_saved_outline':True})
for n in ('SC08_prototype.kicad_pro','SC08_prototype.kicad_dru'):assert sha(P/n)==sha(S/n)
correction=json.loads((P/'proposed-correction.json').read_text());correction['proposal_board_sha256']=sha(board);correction['active_contract_findings']=len(active['findings']);correction['proposed_contract_findings']=0;correction['native_DRC_geometry']=0;correction['native_DRC_parity']=0;correction['remaining_unconnected_items']=64;correction['tracks']=len(records);correction['vias']=sum(isinstance(t,k.PCB_VIA) for t in b.GetTracks());correction['zones']=zones
(P/'proposed-correction.json').write_text(json.dumps(correction,indent=2)+'\n')
print(json.dumps({'board_sha256':sha(board),'active_contract_passed':False,'active_findings':len(active['findings']),'proposed_geometry_passed':True,'proposed_stats':r['stats'],'tracks':len(records),'vias':correction['vias'],'owner_decision_pending':True}))
