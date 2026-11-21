from pathlib import Path
import pcbnew,json
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-prototype-09';B=D/'design/Velluneo_driver.kicad_pcb';pro=B.with_suffix('.kicad_pro').read_bytes();b=pcbnew.LoadBoard(str(B));moves={'C4':(91.5,71.1),'R13':(103.2,127.25),'C1':(89.0,117.75)}
for f in b.GetFootprints():
 if f.GetReference()in moves:
  x,y=moves[f.GetReference()];f.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)))
 if f.GetReference()=='R14':
  for g in list(f.GraphicalItems()):
   if g.m_Uuid.AsString()=='0e2f0e9b-d93e-442a-9da6-1118d70f0682':f.Remove(g)
pcbnew.SaveBoard(str(B),b);B.with_suffix('.kicad_pro').write_bytes(pro)
(D/'silkscreen-changes.json').write_text(json.dumps(dict(text_height_mm=1,text_stroke_mm=.15,silk_graphic_stroke_min_mm=.15,silk_clearance_mm=.15,reference_positions_mm=moves,removed_only_overlapping_R14_body_line_uuid='0e2f0e9b-d93e-442a-9da6-1118d70f0682',no_copper_or_pad_change=True),indent=2)+'\n')
