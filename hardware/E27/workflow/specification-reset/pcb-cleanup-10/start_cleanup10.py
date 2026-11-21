from pathlib import Path
import shutil,json,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';S=P/'pcb-prototype-09';D=P/'pcb-cleanup-10';D.mkdir(exist_ok=True);shutil.copytree(S/'design',D/'design',dirs_exist_ok=True);(D/'checks').mkdir(exist_ok=True);(D/'.work').mkdir(exist_ok=True);(D/'.gitignore').write_text('.work/\n__pycache__/\n*.kicad_prl\n')
shutil.copyfile(P/'pcb-driver-08/extract_geometry.py',D/'extract_geometry.py')
(D/'task-contract.md').write_text('''# CLEANUP10 task contract

Owner asks to smooth visibly jagged tracks, fix current-board toolkit mapping and close demonstrable requirements for prototype procurement. Base538b2dee8e61cf8c944e494fa893732858ed648c. Root solely owns shared CAD/library/configuration writes.33components/81pads/values/MPNs and placement remain; protect measurement branches, C1 return topology, local bypass, numeric3/10/.25/.3/.5mm electrical minima and truthful source pin types. Simplify continuous tracks with clearance-aware straight/45degree routing; no purely decorative image substitute. No rule/waiver/approval manipulation to hide failures. Map current project and separate bare-board preparation evidence from unperformed physical lamp qualification; preserve historical requirements/findings. Pinned toolkit has real scoped-rule/4layer/profile limits; document rather than forge ownership state or relax numeric floors. User authorization covers implementation and GitHub save, not supplier messages, orders, payments or powered tests.

Acceptance: material reduction in segment/staircase count, fresh strict native ERC/DRC/parity and independent intent/topology/coupling checks; explicit current-board hardware contract/preview/conflicts with no manufactured approval; evidence-backed requirement dispositions; updated manufacturing/portable files and actual preview; four independent final roles on frozen candidate; exact GitHub/ZIP verification. Unavailable vendor/physical evidence stays owned/open. Do not claim ready for order if applicable release gates still fail.
''',encoding='utf-8')
print(D)
