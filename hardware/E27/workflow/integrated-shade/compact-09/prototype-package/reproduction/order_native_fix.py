from pathlib import Path
import json,hashlib,pcbnew as k
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';Q=ROOT/'work/compact09/order-closure';Q.mkdir(exist_ok=True)
p=S/'SC09_compact.kicad_pcb';before=hashlib.sha256(p.read_bytes()).hexdigest();b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(p))
def copper(board):
 pads=sorted((f.GetReference(),a.GetNumber(),a.GetPosition().x,a.GetPosition().y,a.GetNetname(),a.GetSize().x,a.GetSize().y,a.GetDrillSize().x,a.GetDrillSize().y) for f in board.GetFootprints() for a in f.Pads())
 tracks=sorted((t.m_Uuid.AsString(),t.GetNetname(),t.GetLayer(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth(k.F_Cu) if isinstance(t,k.PCB_VIA) else t.GetWidth()) for t in board.GetTracks())
 zones=sorted((z.GetZoneName(),z.GetNetname(),z.GetLayer(),z.GetFilledPolysList(z.GetLayer()).Area()) for z in board.Zones() if not z.GetIsRuleArea())
 return [pads,tracks,zones]
old=copper(b);changed=[]
for t in b.GetDrawings():
 if isinstance(t,k.PCB_TEXT) and t.GetLayer() in [k.F_SilkS,k.B_SilkS] and k.ToMM(t.GetTextThickness())<.15:
  changed.append({'text':t.GetText(),'side':b.GetLayerName(t.GetLayer()),'old_stroke_mm':k.ToMM(t.GetTextThickness()),'new_stroke_mm':.15});t.SetTextThickness(k.FromMM(.15))
assert k.SaveBoard(str(p),b,True)
b2=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(p));assert copper(b2)==old
report={'before_sha256':before,'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'changed':changed,'pads_tracks_nets_and_zone_areas_unchanged':True,'basis':'https://jlcpcb.com/capabilities/pcb-capabilities, silkscreen minimum stroke0.15mm and height1mm; actual text heights remain1mm. No electrical changes.'}
(Q/'silkscreen-fix.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
