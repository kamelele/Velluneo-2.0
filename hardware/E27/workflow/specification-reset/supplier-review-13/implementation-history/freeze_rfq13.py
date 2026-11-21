from pathlib import Path
import json, hashlib, shutil
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'supplier-review-13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
# Test appearance probes are local-only; preserve them without publishing alternate views.
for p in (D/'presentation').glob('test-*.png'):shutil.move(str(p),str(D/'.work'/p.name))
H=D/'implementation-history';H.mkdir(exist_ok=True)
names=['start_rfq13.py','refine_rfq13_native.py','tune_rfq13_native.py','shift_rfq13_second.py','adopt_rfq13.py','audit_rfq13_native.py','export_rfq13.py','controls_rfq13.py','mechanical_rfq13.py','polish_rfq13.py','draw_rfq13.py','pdf_qa13.py','rebind_rfq13.py','check_rfq13.py','presentation_rfq13.py','package_rfq13.py','freeze_rfq13.py']
for n in names:shutil.copyfile(W/n,H/n)
(H/'README.md').write_text('''# Actual implementation history, not an automatic replay command

These are the scripts actually used from the original workspace work/ directory.
Their paths resolve relative to that directory and depend on the recorded local
KiCad/toolkit/runtime installations and the C11 baseline. Moving this archive
does not make those local dependencies portable. Use the distributed editable
engineering ZIP for the self-contained KiCad project.

Do not blindly execute the mutation history against the final design: start,
refine, tune and shift were sequential experimental corrections, not idempotent
generators. The initial two DRC probes intentionally exposed unresolved issues;
the final current reports supersede them. Adoption ran once using the actual
pinned preview/apply transaction. No historical source or cache was patched.

The final-state native audit, exports, negative controls and toolkit checks were
actually executed; reports/commands are retained under checks/. The independent
CAM parser required normal access to its local installed library. KiCad renders
required normal filesystem access to the local model files: the restricted
render invocation omitted models and was discarded after visual inspection.
The published renders were regenerated with model access and visually checked.

Runtime for pure Python: CodexPrimaryRuntime.v26-1119-907-0 bundled Python.
Native CAD: KiCad10.0.6 bin/python.exe and kicad-cli.exe. Source runtime_clamp.ps1
from the original workspace for native environment/Git mapping; its obsolete
PcbPy alias must not be used. The exact toolkit manifest is in the project index.
No physical measurement, accepted supplier drawing or standards certificate was
created by these calculations. Those supplier/qualification holds remain open.
''',encoding='utf-8')
idx=R/'hardware/E27/workflow/project-index.md';s=idx.read_text(encoding='utf-8');heading='## Current manufacturer enquiry — RFQ13, 20 November 2026'
if heading not in s:
 s=s.replace('# E27 workflow index\n','# E27 workflow index\n\n'+heading+'''

[RFQ13](specification-reset/supplier-review-13/README.md) is the current selected
45 × 60 mm isolated four-layer, 33-part driver. It reserves the requested finished
30 × 30 × 18 mm T1 body, makes three documented local part moves and strengthens
P/S rules to 10.7 mm through actual pinned-toolkit preview/apply. Fresh native and
portable ERC/DRC/parity are zero; conservative projected P/S copper gap is at least
10.725 mm. Pin/MPN/value identity, measurement copper and separate returns remain.
The unchanged toolkit manifest is b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97.

The seven-page dimensioned review, source-based forming/hole calculations,
independently checked CAM, separate bare-PCB/transformer-assembly/engineering ZIPs,
unsent enquiries, response checklist and both-side native component renders are
supplied. See review-status.json for the actual final review disposition. This
supports technical quotation/DFM, not an order: finished T1/formed-part drawings,
first-article fit, accepted process/films, finished insulation and physical product
qualification remain open. No supplier contact, order, payment, powered testing or
main merge is authorized by this packet. Earlier entries retain historical scope.
''',1);idx.write_text(s,encoding='utf-8')
# Preserve the historical root mapping and append new source inventory only.
hp=P/'hardware.json';h=json.loads(hp.read_text());h['source_files']=[n for n in h['source_files']if not n.startswith('supplier-review-13/')]
excluded={'frozen-files.json','review-status.json','review-record.json','stage-packet.md','integration-record.md','finding-ledger.json'}
for p in sorted(D.rglob('*')):
 if p.is_file() and p.suffix!='.kicad_prl' and not any(t in p.relative_to(D).parts for t in('.work','__pycache__','reviews')) and p.name not in excluded:h['source_files'].append(p.relative_to(P).as_posix())
put(hp,h)
rows=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size)for p in sorted(D.rglob('*'))if p.is_file()and p.suffix!='.kicad_prl'and not any(t in p.relative_to(D).parts for t in('.work','__pycache__','reviews'))and p.name not in excluded]
rows += [dict(path=p.relative_to(R).as_posix(),sha256=sha(p),bytes=p.stat().st_size)for p in(idx,hp)]
body=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
put(D/'frozen-files.json',dict(body_sha256=body,base_commit='0a14df2ea95d2b2b3443585f46e77428671b88d4',files=rows,excluded_lifecycle_files=sorted(excluded),scope='All current packet engineering/delivery files and root inventory/index; only actual review/lifecycle reports and local temporary GUI state excluded.'))
print('Frozen RFQ13',body,len(rows),flush=True)
