"""Apply one verified six-part placement and rip only affected electrical trees."""
from pathlib import Path
import pcbnew,json,hashlib
D=Path(__file__).resolve().parent;E=D/'design';P=D.parent;src=E/'Velluneo_driver.kicad_pcb';b=pcbnew.LoadBoard(str(src));before=hashlib.sha256(src.read_bytes()).hexdigest()
poses={'R7':(-6.5,9.25,180,'F'),'F1':(14.6,8.7,270,'B'),'J1':(20.1,-2.,90,'F'),'R17':(9.2,-3.,90,'B'),'R1':(7.2,14.5,0,'F'),'R2':(20.,24.,90,'F')};moves=[]
for f in b.GetFootprints():
 if f.GetReference()not in poses:continue
 x,y,angle,side=poses[f.GetReference()];old=dict(x=pcbnew.ToMM(f.GetPosition().x)-100,y=pcbnew.ToMM(f.GetPosition().y)-100,angle=f.GetOrientationDegrees(),side=b.GetLayerName(f.GetLayer()))
 layer=pcbnew.F_Cu if side=='F'else pcbnew.B_Cu
 if f.GetLayer()!=layer:f.Flip(f.GetPosition(),False)
 f.SetOrientationDegrees(angle);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100+x),pcbnew.FromMM(100+y)));moves.append(dict(ref=f.GetReference(),before=old,after=dict(x=x,y=y,angle=angle,side=side)))
for g in b.GetDrawings():
 if g.GetLayer()!=pcbnew.Edge_Cuts:continue
 for get,setter in((g.GetStart,g.SetStart),(g.GetEnd,g.SetEnd)):
  p=get();x=pcbnew.ToMM(p.x)
  if abs(x-78.5)<1e-5:p.x=pcbnew.FromMM(77.5)
  if abs(x-121.5)<1e-5:p.x=pcbnew.FromMM(122.5)
  setter(p)
for z in b.Zones():
 if not z.GetIsRuleArea():continue
 chain=z.Outline().Outline(0)
 for i in range(chain.PointCount()):
  p=chain.CPoint(i);x=pcbnew.ToMM(p.x)
  if abs(x-78.5)<1e-5:p=pcbnew.VECTOR2I(pcbnew.FromMM(77.5),p.y)
  elif abs(x-121.5)<1e-5:p=pcbnew.VECTOR2I(pcbnew.FromMM(122.5),p.y)
  chain.SetPoint(i,p)
# Explicit affected nets; replay local bypass/distribution and primary power branches next.
rip={'/DRV','/GATE','Net-(F1-Pad1)','Net-(F1-Pad2)','Net-(BR1-AC-Pad2)','Net-(BR1-AC-Pad4)','/STARTUP_MID','/VDD','/BULK_POS','Net-(R2-Pad2)'};removed=[]
for t in list(b.GetTracks()):
 if t.GetNetname()in rip:removed.append(t.GetNetname());b.Remove(t)
out=D/'.work/placed-ripped.kicad_pcb';pcbnew.SaveBoard(str(out),b)
(D/'placement-decision.json').write_text(json.dumps(dict(source_sha256=before,board_outline_mm=[45,60],moves=moves,removed_copper_objects=len(removed),ripped_nets=sorted(rip),scope='Selected routine geometry under owner delegation; no graph, values, footprint land or numeric rule change. Fresh saved-board checks required.'),indent=2)+'\n');print('Applied one45x60placement; saved ripped intermediate',flush=True)
