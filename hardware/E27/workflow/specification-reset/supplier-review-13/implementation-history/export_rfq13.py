from pathlib import Path
import subprocess,sys,json,shutil
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/supplier-review-13';(D/'assembly-reference').mkdir(exist_ok=True)
s=(W/'export_project11.py').read_text().replace("D=P/'pcb-toolkit-11'","D=P/'supplier-review-13'").replace('pcb-toolkit-11','supplier-review-13')
lines=s.splitlines();out=[];skip=False
for line in lines:
 if skip:skip=False;continue
 if line.startswith('for n in ')and'selected-process.json'in line:
  out.append("shutil.copyfile(P/'pcb-toolkit-11/fabrication/selected-process.json',D/'fabrication/selected-process.json')");skip=True;continue
 out.append(line)
exec(compile('\n'.join(out),str(W/'export_project11.py'),'exec'))
# The CAM parser's template is retained, with only the exact currentpacket binding.
cam=(W/'check_proto09_cam.py').read_text().replace('pcb-prototype-09','supplier-review-13');(W/'check_cam13.py').write_text(cam,encoding='utf-8')
