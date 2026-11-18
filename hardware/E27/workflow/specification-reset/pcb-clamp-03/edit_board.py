"""Edit the real engineering board; preserve native rules, graph, pads and source libraries."""
from pathlib import Path
import pcbnew,json,math,shutil,hashlib
D=Path(__file__).resolve().parent;P=D.parent;OLD=P/'pcb-placement-02';B='Velluneo_specification_reset'
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
# Packet-local library tables are prepared independently, not overwritten.
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
for x,y in[(80,y0),(120,y0),(120,y1),(80,y1)]:poly.Append(pcbnew.FromMM(x),pcbnew.FromMM(y))
assert zone.GetDoNotAllowTracks()and zone.GetDoNotAllowVias()and zone.GetDoNotAllowPads()and zone.GetDoNotAllowZoneFills()
# The explicit wider trial is not a scale operation on component/pad geometry.
for edge in brd.GetDrawings():
 if edge.GetLayer()!=pcbnew.Edge_Cuts:continue
 for getter,setter in((edge.GetStart,edge.SetStart),(edge.GetEnd,edge.SetEnd)):
  p=getter();x=pcbnew.ToMM(p.x);y=pcbnew.ToMM(p.y)
  assert abs(x-84)<1e-6 or abs(x-116)<1e-6
  setter(pt(80 if x<100 else 120,y))
# A named library variant changes only one R9 optional silkscreen line.
f=fps['R9'];c=positions['R9'];assert c['side']=='F' and c['angle_deg']==0
changed=0
for g in f.GraphicalItems():
 if g.GetLayer()!=pcbnew.F_SilkS or not isinstance(g,pcbnew.PCB_SHAPE):continue
 start=g.GetStart();end=g.GetEnd();dx=pcbnew.ToMM(start.x)-100-c['x_mm'];dy=pcbnew.ToMM(start.y)-100-c['y_mm']
 if abs(dx+1.65)<1e-6 and abs(dy-1.15)<1e-6:
  g.SetStart(pt(100+c['x_mm']-.15,100+c['y_mm']+1.15));changed+=1
assert changed==1
f.SetFPID(pcbnew.LIB_ID('Velluneo_Driver','CRCW_1206_NativeReflow_ClippedSilk'))
sch=D/(B+'.kicad_sch');lines=sch.read_text(encoding='utf-8').splitlines(keepends=True);changed=0
for i,line in enumerate(lines):
 if '(property "Reference" "R9"' in line:
  old='Velluneo_Driver:CRCW_1206_NativeReflow';assert line.count(old)==1;lines[i]=line.replace(old,old+'_ClippedSilk');changed+=1
assert changed==1;sch.write_text(''.join(lines),encoding='utf-8',newline='\n')
bom=(OLD/'BOM.csv').read_text(encoding='utf-8').splitlines();out=[]
for line in bom:
 if line.startswith('R9,'):line=line.replace('Velluneo_Driver:CRCW_1206_NativeReflow','Velluneo_Driver:CRCW_1206_NativeReflow_ClippedSilk')
 out.append(line)
(D/'BOM.csv').write_text('\n'.join(out)+'\n',encoding='utf-8',newline='\n')
pcbnew.SaveBoard(str(D/(B+'.kicad_pcb')),brd)
print(json.dumps({'saved':B+'.kicad_pcb','parts':len(fps),'pads':sum(len(list(f.Pads()))for f in fps.values()),'copper_free_band_Y_mm':[y0,y1],'rules_byte_identical':(D/(B+'.kicad_dru')).read_bytes()==(OLD/(B+'.kicad_dru')).read_bytes()}))
