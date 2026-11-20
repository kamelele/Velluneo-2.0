from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'jlcpcb-quote-14'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
shutil.copyfile(W/'freeze_jlc14.py',D/'implementation-history/freeze_jlc14.py')
index=R/'hardware/E27/workflow/project-index.md';s=index.read_text(encoding='utf-8');heading='## Current JLCPCB quotation handoff — JLC14, 20 November 2026'
if heading not in s:
 s=s.replace('# E27 workflow index\n','# E27 workflow index\n\n'+heading+'''

[JLC14](specification-reset/jlcpcb-quote-14/README.md) prepares the unchanged RFQ13
isolated 45 × 60 mm driver for a JLCPCB bare-PCB quote plus a separate assembly
feasibility quote, as explicitly selected by the owner. Official JLCPCB instructions
were checked on 20 November 2026. The upload ZIP contains one GKO, four copper,
two mask, two legend, two paste layers, one Excellon XLN, one human drill map and
an auxiliary sk selecting all 17 epoxy-filled/capped vias; 25 insertion holes stay open.
Fresh native ERC/DRC/parity are zero; independent CAM confirms the nine previous
artwork layers are geometrically identical and all holes/SK coordinates agree.

Full/short PCB Remark, exact form settings, a polished unsent support enquiry and
11 technical response IDs are provided. The complete handoff is separate from the
14-member automatic Gerber ZIP. The 33-part MPN list and matching 26-SMT BOM/CPL
are manual quote references: no invented LCSC stock, centroid or feeder corrections.
Standard two-sided PCBA needs a minimum 70 × 70 mm handling/panel proposal, rails
and fiducials, while the finished board stays 45 × 60 mm. Tighter holes/registration,
material/process, custom parts and prior physical/human release holds remain explicit.
No account, upload, supplier message, charge, order, payment or main merge occurred.
The RFQ13 design remains authoritative; toolkit manifest remains
b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97.
''',1);index.write_text(s,encoding='utf-8')
excluded={'frozen-files.json','review-record.json','review-status.json','finding-ledger.json','integration-record.md','stage-packet.md'}
hp=P/'hardware.json';h=json.loads(hp.read_text());h['source_files']=[n for n in h['source_files']if not n.startswith('jlcpcb-quote-14/')]
body=[p for p in sorted(D.rglob('*'))if p.is_file()and p.suffix!='.kicad_prl'and p.name not in excluded and not any(t in p.relative_to(D).parts for t in('.work','__pycache__','reviews'))]
h['source_files'] += [p.relative_to(P).as_posix()for p in body];put(hp,h)
rows=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size)for p in body+[index,hp]]
digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
put(D/'frozen-files.json',dict(body_sha256=digest,files=rows,base_commit='b33e57c78eb3c1d644e3d00e96ccc5e47dc8bcaa',scope='All JLC14 engineering/export/quotation files, helpers and root inventory/index; only localtemporary/GUIstate and final review lifecycle excluded.',excluded_lifecycle_files=sorted(excluded)))
put(D/'review-status.json',dict(ready_for_quotation_handoff=False,pending='Four actual independent final role reviews of frozen body',body_sha256=digest,portal_import_performed=False,supplier_contact=False,supplier_process_confirmed=False,automatic_PCBA_order_ready=False,order_ready=False,human_stage_approval=False))
print('JLC14 frozen',digest,len(rows),flush=True)
