"""Saved native geometry for selected process; no supplier or physical qualification."""
from pathlib import Path
import pcbnew,json,math,hashlib,csv
D=Path(__file__).resolve().parent;E=D/'design';P=E/'Velluneo_driver.kicad_pcb';b=pcbnew.LoadBoard(str(P));vias=[t for t in b.GetTracks()if isinstance(t,pcbnew.PCB_VIA)];holes=[];rows=[]
for f in b.GetFootprints():
 for p in f.Pads():
  drill=p.GetDrillSize()
  if drill.x or drill.y:holes.append((f.GetReference()+'.'+p.GetNumber(),p,pcbnew.ToMM(max(drill.x,drill.y))))
for i,v in enumerate(vias):
 x,y=pcbnew.ToMM(v.GetPosition().x),pcbnew.ToMM(v.GetPosition().y);hole=pcbnew.ToMM(v.GetDrillValue());diam=pcbnew.ToMM(v.GetWidth(pcbnew.F_Cu));gaps=[]
 assert v.GetFillingMode()==pcbnew.FILLING_MODE_FILLED and v.GetCappingMode()==pcbnew.CAPPING_MODE_CAPPED
 assert v.TopLayer()==pcbnew.F_Cu and v.BottomLayer()==pcbnew.B_Cu
 for name,p,d in holes:
  q=p.GetPosition();gaps.append((math.hypot(x-pcbnew.ToMM(q.x),y-pcbnew.ToMM(q.y))-(hole+d)/2,name))
 gap,nearest=min(gaps);assert gap>.45,(i,gap,nearest)
 rows.append(dict(id=i+1,net=v.GetNetname(),board_x_mm=x,board_y_mm=y,output_x_mm=x-77.5,output_y_mm=130-y,hole_mm=hole,pad_mm=diam,fill='nonconductive epoxy',cap='copper',minimum_hole_edge_gap_to_component_hole_mm=gap,nearest_component_hole=nearest))
with(D/'designated-filled-vias.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
report=dict(board_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),vias=rows,component_holes=len(holes),component_holes_remain_open=True,minimum_via_hole_to_component_hole_edge_gap_mm=min(r['minimum_hole_edge_gap_to_component_hole_mm']for r in rows),nominal_via_aspect_ratio=1.6/.3,maximum_tolerance_aspect_ratio=1.76/.3,via_annular_ring_mm=.15,origin_board_xy_mm=[77.5,130],output_axes='X right; Y up; same as native position export',scope='Hole-edge screen uses max diameter for oval component holes, conservatively circumscribed. Native designated vias filled/capped; component holes excluded. Detailed vendor confirmation remains required before ordering.')
(E/'checks/process-geometry.json').write_text(json.dumps(report,indent=2)+'\n');print('Vias',len(rows),'min hole edge gap',report['minimum_via_hole_to_component_hole_edge_gap_mm'])
