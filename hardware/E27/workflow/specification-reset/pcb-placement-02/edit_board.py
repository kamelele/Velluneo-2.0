"""Edit the real engineering board; preserve native rules, graph, pads and source libraries."""
from pathlib import Path
import pcbnew,json,math,shutil,hashlib
D=Path(__file__).resolve().parent;P=D.parent;OLD=P/'pcb-draft-01';B='Velluneo_specification_reset'
brd=pcbnew.LoadBoard(str(OLD/(B+'.kicad_pcb')));assert brd
proposal=json.loads((D/'placement-proposal.json').read_text(encoding='utf-8'))
positions=proposal['positions'];fps={f.GetReference():f for f in brd.GetFootprints()};assert set(positions)==set(fps)and len(fps)==31
def pt(x,y):return pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))
for ref,c in positions.items():
 f=fps[ref]
 if bool(f.IsFlipped())!=(c['side']=='B'):f.Flip(f.GetPosition(),True)
 f.SetOrientation(pcbnew.EDA_ANGLE(c['angle_deg'],pcbnew.DEGREES_T));f.SetPosition(pt(c['x_mm']+100,c['y_mm']+100))
for suffix in('.kicad_sch','.kicad_pro','.kicad_dru'):
 shutil.copyfile(OLD/(B+suffix),D/(B+suffix))
for table in('fp-lib-table','sym-lib-table'):shutil.copyfile(OLD/table,D/table)
(D/'models').mkdir(exist_ok=True)
for model in(OLD/'models').glob('*.wrl'):shutil.copyfile(model,D/'models'/model.name)
# The copper-free band follows the new pad extents; actual10mmP/S rule stays byte-identical.
pads=[]
for ref,f in fps.items():
 for pad in f.Pads():
  bb=pad.GetBoundingBox();box=[pcbnew.ToMM(bb.GetX()),pcbnew.ToMM(bb.GetY()),pcbnew.ToMM(bb.GetRight()),pcbnew.ToMM(bb.GetBottom())]
  sec=(ref=='T1'and pad.GetNumber()in('6','7','8','9','10'))or ref in{'C4','D3','J2','R11','R12'}
  pads.append((sec,box))
y0=max(b[3]for s,b in pads if s)+.15;y1=min(b[1]for s,b in pads if not s)-.15;assert y1>y0
zones=list(brd.Zones());assert len(zones)==1 and zones[0].GetIsRuleArea()
zone=zones[0];poly=zone.Outline();poly.RemoveAllContours();poly.NewOutline()
for x,y in[(84,y0),(116,y0),(116,y1),(84,y1)]:poly.Append(pcbnew.FromMM(x),pcbnew.FromMM(y))
assert zone.GetDoNotAllowTracks()and zone.GetDoNotAllowVias()and zone.GetDoNotAllowPads()and zone.GetDoNotAllowZoneFills()
pcbnew.SaveBoard(str(D/(B+'.kicad_pcb')),brd)
print(json.dumps({'saved':B+'.kicad_pcb','parts':len(fps),'pads':sum(len(list(f.Pads()))for f in fps.values()),'copper_free_band_Y_mm':[y0,y1],'rules_byte_identical':(D/(B+'.kicad_dru')).read_bytes()==(OLD/(B+'.kicad_dru')).read_bytes()}))
