"""Explicitly reserve the independently checked return corridor before power routing."""
from pathlib import Path
import pcbnew,json,math,hashlib
D=Path(__file__).resolve().parent;B=D/'studies/sense/routing-seed.kicad_pcb';before=hashlib.sha256(B.read_bytes()).hexdigest();b=pcbnew.LoadBoard(str(B));net=b.GetNetsByName()['/PRIMARY_GND'].GetNetCode()
paths=[('F',[(-14.49,24.25),(-14.6,25.7),(-10.99,28.45),(-6.1,28.45),(-6,27.8)]),('B',[(-6,27.8),(-4.7,27.8),(-4.3,28.2),(-2.9,28.2),(-2.7,28.4),(-2.5,28.4),(-1.9,29),(0.5,29),(0.5,26.6),(3.7,23.4),(3.75,23.4)]),('B',[(3.75,23.4),(3.7,23.4),(3.7,22)]),('F',[(3.7,22),(3.75,22.05)])]
def pt(p):return pcbnew.VECTOR2I(pcbnew.FromMM(p[0]+100),pcbnew.FromMM(p[1]+100))
for layer,points in paths:
 for a,z in zip(points,points[1:]):
  t=pcbnew.PCB_TRACK(b);t.SetStart(pt(a));t.SetEnd(pt(z));t.SetWidth(pcbnew.FromMM(.3));t.SetLayer(pcbnew.F_Cu if layer=='F'else pcbnew.B_Cu);t.SetNetCode(net);b.Add(t)
for p in[(-6,27.8),(3.7,22)]:
 v=pcbnew.PCB_VIA(b);v.SetPosition(pt(p));v.SetWidth(pcbnew.FromMM(.6));v.SetDrill(pcbnew.FromMM(.3));v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);v.SetViaType(pcbnew.VIATYPE_THROUGH);v.SetNetCode(net);b.Add(v)
pcbnew.SaveBoard(str(B),b)
(D/'reserved-return.json').write_text(json.dumps(dict(before_sha256=before,after_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),paths=[dict(layer=l,points_relative_mm=p,planar_length_mm=sum(math.dist(a,z)for a,z in zip(p,p[1:])))for l,p in paths],vias_relative_mm=[[-6,27.8],[3.7,22]],via_diameter_mm=.6,via_drill_mm=.3,track_width_mm=.3,previous_IC_return_mm=38.695127,current_IC_return_mm=sum(math.dist(a,z)for l,p in paths for a,z in zip(p,p[1:])),bulk_junction='C1.2',not_true_negative_Kelvin_at_R9=True,shared_R9_C1_powerstrap_mm=2.7,source_layout='https://www.ti.com/lit/ds/symlink/ucc28700.pdf sections8.3.1.2/11.1',scope='Geometry improvement only. The2.7mmshuntpowerstrap still contributes shared impedance; no measurement-error/EMI/assembly/currentqualification.'),indent=2)+'\n')
print('reserved dedicated return',sum(math.dist(a,z)for l,p in paths for a,z in zip(p,p[1:])))
