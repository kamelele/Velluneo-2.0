from pathlib import Path
import shutil,json,hashlib,subprocess,sys
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-cleanup-10';S=P/'pcb-prototype-09'
# Reuse artifact assembly/actual-CAM preview plumbing, not the old documentation.
s=(W/'package_proto09.py').read_text().replace('pcb-prototype-09','pcb-cleanup-10').replace('56094af47ed5e110168cf27a6763f7251576de9f','538b2dee8e61cf8c944e494fa893732858ed648c').replace('PROTO09','CLEANUP10').replace('Velluneo_prototype09.png','Velluneo_cleanup10.png').replace('poprawiony nadruk','wyprostowane ścieżki').replace('Gerbery i wiercenia sprawdzone • 42 otwory • 17 przelotek do wypełnienia i pokrycia miedzią','647 → 304 odcinki ścieżek • DRC / ERC: 0 • 17 przelotek z pierścieniem 0,20 mm').replace('Zamówienie: po akceptacji wykonania i plików przez producenta. Badania działania i izolacji pozostają otwarte.','Do zamówienia pozostają potwierdzenie producenta i zgodne wdrożenie reguł toolkitu.').replace('W=Path(__file__).resolve().parent;',"W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());")
s=s.replace("s=(W/name).read_text().replace(","s=(W/name).read_text().replace(")
# Only the first executable W assignment is rebased; keep quoted replacement code intact.
source=(W/'package_proto09.py').read_text();broken=s.splitlines();original=source.splitlines()
for i,line in enumerate(broken):
 if "s=(W/name).read_text().replace("in line:broken[i]=next(x for x in original if "s=(W/name).read_text().replace("in x)
s=('\n'.join(broken)+'\n').replace('readiness.json','procurement-status.json').replace("if p.is_file()and not any(x in p.parts", "if p.is_file()and p.suffix!='.kicad_prl'and not any(x in p.parts")
(D/'package_artifacts.py').write_text(s,encoding='utf-8')
# Assembly reference remains same physical parts; retained construction holds apply.
shutil.copyfile(S/'assembly-reference/README.txt',D/'assembly-reference/README.txt')
print('Prepared current preview/ZIP builder')
