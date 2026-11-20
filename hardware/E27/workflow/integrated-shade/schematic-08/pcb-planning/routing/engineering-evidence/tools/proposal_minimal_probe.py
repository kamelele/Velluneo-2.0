"""Explicit hypothetical exception proposal, in-memory CAD only; NEVER approval."""
import json,hashlib,math,sys
from pathlib import Path
import pcbnew as k
OUT=Path(__file__).resolve().parent
S=OUT.parent/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC08_prototype'
C=S/'.work/routing/critical-thermal-candidate-05'
sys.path.insert(0,str(OUT.parent/'sc08-route-validator'))
import checker as ch
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_sha=sha(S/'SC08_prototype.kicad_pcb');candidate_sha=sha(C/'SC08_prototype.kicad_pcb')
base=ch.Contract(S)
b=ch.load_native(C/'SC08_prototype.kicad_pcb')
prov=json.loads((C/'routing-authoring.json').read_text())
points=[(107.525,41.905),(107.525,43.65),(105.5,44.15),(104.5,44.0)]
class ProposalChecker(ch.Checker):
    def exception_region(self,e):
        if e['ref']=='U1' and set(e['pins']) == {'2','4'}:
            region=k.SHAPE_POLY_SET(self.courts['U1'])
            region.Inflate(ch.mm(self.proposed_margin-2*ch.ERROR_MM),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,ch.mm(ch.ERROR_MM))
            return region
        return super().exception_region(e)

outputs=[]
for margin in (1.0,1.5,2.0):
    check=ProposalChecker(b,ch.Contract(S),prov);check.proposed_margin=margin;check.collect()
    original=list(check.objects);new=[]
    for index,(p,q) in enumerate(zip(points,points[1:])):
        item=k.PCB_TRACK(b);item.SetStart(k.VECTOR2I(ch.mm(p[0]),ch.mm(p[1])));item.SetEnd(k.VECTOR2I(ch.mm(q[0]),ch.mm(q[1])));item.SetWidth(ch.mm(.6));item.SetLayer(k.F_Cu);item.SetNetCode(b.GetNetsByName()['/DRAIN_BLOCKED'].GetNetCode())
        obj=check.object(item,'track','/DRAIN_BLOCKED','F.Cu',('U1','4'),f'PROPOSAL_DRAIN_{index}');check.objects.append(obj);new.append(obj)
    for obj in new:
        for other in original:
            if obj.layer==other.layer and obj.net!=other.net:check.spacing(obj,other)
    track_findings=list(check.findings);check.findings=[]
    via=k.PCB_VIA(b);via.SetPosition(k.VECTOR2I(ch.mm(104.5),ch.mm(44)));via.SetWidth(ch.mm(.8));via.SetDrill(ch.mm(.3));via.SetViaType(k.VIATYPE_THROUGH);via.SetLayerPair(k.F_Cu,k.B_Cu);via.SetNetCode(b.GetNetsByName()['/DRAIN_BLOCKED'].GetNetCode())
    for layer in ('F.Cu','B.Cu'):
        obj=check.object(via,'via','/DRAIN_BLOCKED',layer,ident='PROPOSAL_DRAIN_VIA')
        for other in original:
            if obj.layer==other.layer and obj.net!=other.net:check.spacing(obj,other)
    outputs.append({'proposed_margin_mm':margin,'changed_exact_pairs_only':[['U1.2','U1.4']],'tracks_pass':not track_findings,'track_findings':track_findings,'via_pass':not check.findings,'via_findings':list(check.findings)})
report={'status':'HYPOTHETICAL_CHANGE_PROPOSAL_REQUIRES_OWNER_DECISION_NOT_APPROVED','native_board_unchanged':sha(S/'SC08_prototype.kicad_pcb')==source_sha,'candidate_unchanged':sha(C/'SC08_prototype.kicad_pcb')==candidate_sha,'source_sha256':source_sha,'candidate_sha256':candidate_sha,'checker_sha256':sha(Path(ch.__file__)),'track_width_mm':.6,'points_mm':points,'via_mm':{'center':[104.5,44.0],'diameter':.8,'drill':.3},'results':outputs,'limits':'Only new F tracks and new F/B via versus existing native pads/tracks/filled zones checked. No CAD saved, no global routing/DRC/thermal/physics qualification. Proposed exact exception extension is NOT active customer policy.'}
(OUT/'drain-minimal-proposal-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
