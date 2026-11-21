from pathlib import Path
import pcbnew as p,json
from c16_sexpr import parse,dumps,child
W=Path(__file__).resolve().parent;E=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16/design';B=E/'Velluneo_driver.kicad_pcb';b=p.LoadBoard(str(B))
libs={'Velluneo_Driver':E/'libraries/Velluneo_Driver.pretty','Velluneo_C16':E/'Velluneo_C16.pretty','Velluneo_ECO04':E/'Velluneo_ECO04.pretty'};done={}
for f in b.GetFootprints():
 tht=any(q.GetAttribute()==p.PAD_ATTRIB_PTH for q in f.Pads());f.SetAttributes(p.FP_THROUGH_HOLE if tht else p.FP_SMD);fid=f.GetFPID();lib=libs[str(fid.GetLibNickname())]/(str(fid.GetLibItemName())+'.kicad_mod');attr='through_hole'if tht else'smd'
 if lib in done:assert done[lib]==attr;continue
 done[lib]=attr;t=parse(lib.read_text());node=child(t,'attr')
 if node is None:t.append(['attr',attr])
 else:node[:]=['attr',attr]
 lib.write_text(dumps(t)+'\n',encoding='utf-8',newline='\n')
for q in b.GetTracks():
 if isinstance(q,p.PCB_VIA):q.SetFillingMode(p.FILLING_MODE_FILLED);q.SetCappingMode(p.CAPPING_MODE_CAPPED)
p.SaveBoard(str(B),b);print('native types and filled/capped via requests saved',len(done),'library items')
