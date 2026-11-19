from pathlib import Path
import pcbnew
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());B=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-cleanup-10/design/Velluneo_driver.kicad_pcb';pro=B.with_suffix('.kicad_pro').read_bytes();b=pcbnew.LoadBoard(str(B));a=pcbnew.VECTOR2I(pcbnew.FromMM(98.475),pcbnew.FromMM(126.025));z=pcbnew.VECTOR2I(pcbnew.FromMM(98.375),pcbnew.FromMM(126.025));count=0
for t in b.GetTracks():
 if t.GetNetname()!='/VDD':continue
 if isinstance(t,pcbnew.PCB_VIA):
  if t.GetPosition()==a:t.SetPosition(z);count+=1
 else:
  if t.GetStart()==a:t.SetStart(z)
  if t.GetEnd()==a:t.SetEnd(z)
assert count==1;pcbnew.SaveBoard(str(B),b);B.with_suffix('.kicad_pro').write_bytes(pro)
