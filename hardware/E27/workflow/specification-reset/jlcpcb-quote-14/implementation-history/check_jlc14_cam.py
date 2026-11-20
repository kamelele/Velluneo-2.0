from pathlib import Path
import sys,json,hashlib,warnings,collections
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W/'cam-libs'))
from gerbonara import GerberFile,ExcellonFile
from gerbonara.utils import MM
P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';S=P/'supplier-review-13';D=P/'jlcpcb-quote-14';F=D/'gerbers'
def geometry(f):return collections.Counter(repr(q)for o in f.objects for q in o.to_primitives(unit=MM))
mapping={'GTL':'F_Cu.gtl','G2L':'In1_Cu.g1','G3L':'In2_Cu.g2','GBL':'B_Cu.gbl','GTS':'F_Mask.gts','GBS':'B_Mask.gbs','GTO':'F_Silkscreen.gto','GBO':'B_Silkscreen.gbo','GKO':'Edge_Cuts.gm1'}
reports=[]
for ext,old in mapping.items():
 new=GerberFile.open(F/('Velluneo_JLC14.'+ext));previous=GerberFile.open(S/'fabrication'/('Velluneo_driver-'+old));assert geometry(new)==geometry(previous),ext
 reports.append(dict(layer=ext,objects=len(new.objects),geometric_primitives_equal_RFQ13=True))
for ext in('GTP','GBP'):
 f=GerberFile.open(F/('Velluneo_JLC14.'+ext));assert f.objects;reports.append(dict(layer=ext,objects=len(f.objects),fresh_native_paste_export=True))
outline=GerberFile.open(F/'Velluneo_JLC14.GKO');assert len(outline.objects)==4
vertices=set()
for o in outline.objects:vertices|={(round(o.x1,6),round(o.y1,6)),(round(o.x2,6),round(o.y2,6))}
assert vertices=={(0.,0.),(45.,0.),(45.,60.),(0.,60.)}
with warnings.catch_warnings(record=True)as ws:
 warnings.simplefilter('always');drill=ExcellonFile.open(F/'Velluneo_JLC14.XLN',plated=True)
expected=json.loads((S/'checks/native-fabrication-input.json').read_text());remaining=list(drill.objects);assert len(remaining)==42
for q in expected['expected_drills']:
 found=[i for i,a in enumerate(remaining)if abs(a.aperture.diameter-q['diameter_mm'])<1e-6 and max(abs(a.x-q['x_mm']),abs(a.y-q['y_mm']))<=.000501];assert found,q;remaining.pop(found[0])
assert not remaining
sk=GerberFile.open(F/'Velluneo_JLC14.sk');assert len(sk.objects)==17
vias=json.loads((S/'checks/native-inventory.json').read_text())['vias'];remaining=list(sk.objects)
for v in vias:
 found=[i for i,o in enumerate(remaining)if abs(o.x-v['output_x_mm'])<1e-6 and abs(o.y-v['output_y_mm'])<1e-6 and abs(o.aperture.diameter-.3)<1e-6];assert found,v;remaining.pop(found[0])
assert not remaining and sum(abs(o.aperture.diameter-.3)<1e-6 for o in drill.objects)==17
assert not any(p.suffix.lower().startswith('.gm')for p in F.iterdir())
assert len(list(F.iterdir()))==14
f=json.loads((S/'frozen-files.json').read_text())
# Root index/inventory may be updated only in JLC14 integration; RFQ13 packet files must remain unchanged.
for q in f['files']:
 if '/supplier-review-13/'in q['path']:assert hashlib.sha256((W/'Velluneo-readiness'/q['path']).read_bytes()).hexdigest()==q['sha256']
result=dict(passed=True,parser='gerbonara1.5.0',source_board_sha256=expected['board_sha256'],layers=reports,manufacturing_Gerbers=11,auxiliary_SK_layers=1,SK_flashes=17,SK_all_native_vias_exact=True,all_0p300mm_drills_are_selected_vias=True,component_holes_left_open=25,PTH=42,NPTH=0,outline='OneGKO only;fourclosedsegments;45x60mm;origin0,0',all9_previous_artwork_layers_semantically_identical=True,drills_match_native_within_mm=.000501,other_RFQ13_packet_files_unchanged=True,parser_warnings=[str(v.message)for v in ws],limitations='Independent geometry/drill/SK/layer reconciliation, not vendor portal import, supplier DFM acceptance, functional performance or physical insulation.')
(D/'checks/CAM-validation.json').write_text(json.dumps(result,indent=2)+'\n');print('Independent JLC14 CAM PASS:11manufacturing+1SK,42PTH,17selected,25open,old9artwork identical',flush=True)
