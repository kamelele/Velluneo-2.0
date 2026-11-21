from pathlib import Path
import json,shutil
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-cleanup-10';S=P/'pcb-prototype-09';E=D/'design';(D/'fabrication').mkdir(exist_ok=True)
process=json.loads((S/'fabrication/selected-process.json').read_text());process.update(via_diameter_mm=.7,nominal_via_ring_mm=.2,source_C09_service_unconfirmed=True);(D/'selected-process.json').write_text(json.dumps(process,indent=2)+'\n')
# Reuse native export code; all files source the current selected C10 design.
src=(W/'prepare_proto09.py').read_text().replace("D=P/'pcb-prototype-09'","D=P/'pcb-cleanup-10'").replace("S=P/'pcb-driver-08'","S=P/'pcb-cleanup-10'").replace("D/'authorization.json'","D/'export-authorization-reference.json'").replace("D/'task-contract.md'","D/'historical-export-contract-not-current.md'").replace('56094af47ed5e110168cf27a6763f7251576de9f','538b2dee8e61cf8c944e494fa893732858ed648c')
src=src.replace("preview_source_sha256=sha(S/'pcb-preview.png')","historical_C09_preview_sha256=sha(P/'pcb-prototype-09/pcb-preview.png')").replace('W=Path(__file__).resolve().parent;',"W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());")
src=src.replace("for name in('selected-process.json','designated-filled-vias.csv'):shutil.copyfile(S/name,D/'fabrication'/name)","shutil.copyfile(D/'selected-process.json',D/'fabrication/selected-process.json')")
(D/'export_native.py').write_text(src);print('Prepared current native exporter')
# Independent CAM checker points to C10; no external library/cache modified.
s=(W/'check_proto09_cam.py').read_text().replace('pcb-prototype-09','pcb-cleanup-10').replace('W=Path(__file__).resolve().parent;',"W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());");(D/'check_cam.py').write_text(s)
