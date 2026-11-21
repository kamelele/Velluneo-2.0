"""Explicit 43x60 alternative: only Edge.Cuts and corresponding rule-area width."""
from pathlib import Path
import pcbnew,json,hashlib
D=Path(__file__).resolve().parent;out=D/'studies/sense/routing-seed.kicad_pcb';before=hashlib.sha256(out.read_bytes()).hexdigest();b=pcbnew.LoadBoard(str(out))
for f in b.GetFootprints():
 if f.GetReference()=='F1':
  f.SetOrientationDegrees(180);f.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(104),pcbnew.FromMM(107.5)));f.Reference().SetTextAngle(pcbnew.EDA_ANGLE())
 if f.GetReference()=='R4':
  if f.GetLayer()!=pcbnew.B_Cu:f.Flip(f.GetPosition(),False)
  f.SetOrientationDegrees(0);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(104.5),pcbnew.FromMM(115.8)));f.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(107.2),pcbnew.FromMM(115.8)))
 if f.GetReference()=='R10':
  if f.GetLayer()!=pcbnew.F_Cu:f.Flip(f.GetPosition(),False)
  f.SetOrientationDegrees(270);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(82.8),pcbnew.FromMM(102.35)));f.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(82.8),pcbnew.FromMM(107.5)));f.Reference().SetTextAngle(pcbnew.EDA_ANGLE())
for shape in b.GetDrawings():
 if shape.GetLayer()!=pcbnew.Edge_Cuts:continue
 for getter,setter in((shape.GetStart,shape.SetStart),(shape.GetEnd,shape.SetEnd)):
  p=getter();x=pcbnew.ToMM(p.x)
  if abs(x-79.5)<1e-5:p.x=pcbnew.FromMM(78.5)
  elif abs(x-120.5)<1e-5:p.x=pcbnew.FromMM(121.5)
  setter(p)
for z in b.Zones():
 if not z.GetIsRuleArea():continue
 outline=z.Outline().Outline(0)
 for i in range(outline.PointCount()):
  p=outline.CPoint(i);x=pcbnew.ToMM(p.x)
  if abs(x-79.5)<1e-5:p=pcbnew.VECTOR2I(pcbnew.FromMM(78.5),p.y)
  elif abs(x-120.5)<1e-5:p=pcbnew.VECTOR2I(pcbnew.FromMM(121.5),p.y)
  outline.SetPoint(i,p)
pcbnew.SaveBoard(str(out),b)
(D/'layout-alternative.json').write_text(json.dumps(dict(before_sha256=before,after_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),baseline_mm=[41,60],alternative_mm=[43,60],outline_added_each_side_mm=1,component_moves=[dict(ref='R10',from_relative_mm=[0,27.75],to_relative_mm=[-17.2,2.35],side='F',angle_deg=270),dict(ref='F1',centre_relative_mm=[4,11.4],side='B',from_angle_deg=0,to_angle_deg=180),dict(ref='R4',from_relative_mm=[-.5,26.4],from_side='F',to_relative_mm=[4.5,15.8],side='B',angle_deg=0)],other_component_geometry_unchanged=True,rule_area_broadened_with_outline=True,finished_lamp_fit_qualified=False,reason='Reversible routing alternative opens BR1 edge channel, paired groundreference and dividerescape. No finishedfit/stageapproval; fullnativeverificationrequired.'),indent=2)+'\n')
print('widened trial to43x60')
