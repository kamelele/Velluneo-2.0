from pathlib import Path
import pcbnew as p
f=Path(__file__).resolve().parent/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16/design/Velluneo_driver.kicad_pcb'
b=p.LoadBoard(str(f));fps={x.GetReference():x for x in b.GetFootprints()}
for r,xy in {'RT1':(104.5,122.1),'R13':(109.5,118.8),'C1':(80.5,127.5),'R8':(89,116.7),'C3':(109.85,101.5),'R3':(110,123.2),'BR1':(113.15,128.4)}.items():
 t=fps[r].Reference();t.SetPosition(p.VECTOR2I(p.FromMM(xy[0]),p.FromMM(xy[1])));t.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
fps['R3'].Reference().SetTextAngle(p.EDA_ANGLE(90,p.DEGREES_T))
for g in list(fps['C4'].GraphicalItems()):
 if g.GetLayer()==p.F_SilkS:
  bb=g.GetBoundingBox()
  if p.ToMM(bb.GetTop())<70.15:fps['C4'].Remove(g)
p.SaveBoard(str(f),b)
