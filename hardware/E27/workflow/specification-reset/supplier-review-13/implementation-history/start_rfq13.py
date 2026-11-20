from pathlib import Path
import shutil,json,hashlib
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'supplier-review-13';E=D/'design';D.mkdir(exist_ok=True)
shutil.copytree(P/'pcb-toolkit-11/design',E,ignore=shutil.ignore_patterns('.work','__pycache__','*.kicad_prl','release'),dirs_exist_ok=True)
for n in('checks','fabrication','drawings','supplier','evidence','reviews'):(D/n).mkdir(exist_ok=True)
(D/'.gitignore').write_text('.work/\n__pycache__/\n*.kicad_prl\n')
(D/'owner-request.txt').write_text('''Actual owner request in this chat,20November2026Europe/Warsaw:
"no to zrób wszystkie czynnosci które doporwadza nas do miejsca ze bedziemy mogli zapytac producenta o wykoananie"
Additional explicit scope:
"1. Potwierdzić rzeczywiste gabaryty transformatora i elementów z formowanymi wyprowadzeniami.
2. Zamknąć końcowy przegląd izolacji i montażu. ale to tez zrób plus to co napisałem"
Selected current45x60mm isolated33partdriver, notSC08. Prepare/source/check concrete dimensioned supplierreview and manufacturinginquiry materials. No suppliermessage/order/payment or fabricated finishedsample approval authorized.
''',encoding='utf-8')
(D/'task-contract.md').write_text('''# RFQ13 bounded task

Base0a14df2ea95d2b2b3443585f46e77428671b88d4. Root alone writes selected CAD/libraries/contracts. Read-only implementationadvisors separately research transformer, formedparts and isolation. Four independent final contexts review one freeze; implementationadvisors do not grant approval.

Verify manufacturer-dimensional facts, actual native33part81pad304track17via source and full finished-body reservation. Correct only defensible geometry/configuration issues without changing graph/MPNs/physicalpins. Probe stronger finishedspacing margin in isolatedcopies; adopt only actual passingcurrentCAD and genuineToolkit preview/apply, never silentlyweaken3/10rule floors. Preserve originalsource/historicalpackets. Supplier/physicaldimensions not establishedbydocumentation must become explicit drawing/firstarticle acceptance requests, not inventedmeasurements or normativeclaims. Finish insulation/mounting engineeringreview with actualfindings/disposition and required supplier evidence. Full standards notavailable; do not fabricate tables or certification.

Acceptance: current source-bound nativeERC/DRC/parity, current all-layer P/S geometry plus same-layer/functionalinterlayer distinctions, preservedgraph/measurementcopper/C1returns, envelope and finishedhole/forming calculations with provenance, dimensionedreviewPDF visuallychecked, exactbarePCB/engineering/transformer-assembly RFQfiles and Englishunsent request, manifests/CRC/sourcebindings, four actual independent finalroles, GitHubexactverification. Ready-for-enquiry differs from order/energization/finishedlamp qualification; all genuine acceptanceholds remain visible.
''',encoding='utf-8')
print(D)
