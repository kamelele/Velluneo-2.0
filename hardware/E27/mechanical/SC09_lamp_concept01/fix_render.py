from pathlib import Path
import pcbnew as k
R=Path.cwd();S=R/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';O=R/'outputs/SC09_zarowka_3D'
for n in ['closed','cutaway']:
 p=O/f'SC09_lamp_{n}.kicad_pcb';b=k.LoadBoard(str(p))
 for f in b.GetFootprints():
  if f.GetReference()=='CONCEPT':f.SetAttributes(k.FP_THROUGH_HOLE);f.Reference().SetVisible(False);f.Value().SetVisible(False)
 k.SaveBoard(str(p),b);p.write_text(p.read_text().replace('${KIPRJMOD}',S.as_posix()))
