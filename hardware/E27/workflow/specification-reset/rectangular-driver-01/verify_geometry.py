"""Read-only saved rectangle geometry checks, not full 3D, routing or safety."""
from pathlib import Path
import json,itertools,math
D=Path(__file__).resolve().parent;r=json.loads((D/'packing-diagnostic.json').read_text(encoding='utf-8'));inv=json.loads((D.parent/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'));parts={p['ref']:p for p in inv['parts']};W,L=r['board_study_rectangle_mm'];pos=r['positions']
assert len(pos)==31 and sum(len(c['pads'])for c in pos.values())==79
bounds={ref:c['courtyard_bbox_mm']for ref,c in pos.items()};t=pos['T1'];bounds['T1']=[t['x_mm']-15,t['y_mm']-15,t['x_mm']+15,t['y_mm']+15]
def overlap(a,b):return a[0]<b[2]and b[0]<a[2]and a[1]<b[3]and b[1]<a[3]
collisions=[];jointcollisions=[];overruns=[]
for ref,b in bounds.items():
 if not(b[0]>=-W/2 and b[2]<=W/2 and b[1]>=-L/2 and b[3]<=L/2):overruns.append(ref)
for a,b in itertools.combinations(pos,2):
 if pos[a]['side']==pos[b]['side']and overlap(bounds[a],bounds[b]):collisions.append([a,b])
for ref,c in pos.items():
 for p,b in zip(parts[ref]['pads'],c['pads']):
  if not p['tht']:continue
  joint=[b[0]-.4,b[1]-.4,b[2]+.4,b[3]+.4]
  for other,oc in pos.items():
   if other==ref or oc['side']==c['side']:continue
   if overlap(joint,bounds[other]):jointcollisions.append([ref,p['pin'],other])
assert not overruns,overruns
assert not collisions,collisions
assert not jointcollisions,jointcollisions
q=r['actual_saved_pad_bbox_checks'];assert q['working_reserve_pass']and q['edge_working_allowance_pass']
print(json.dumps({'scope':'All savedcourt/allocatedT1boxes inside32x60; samefacecourtcollisions and oppositefaceTHTpad+0.4joint obstacles. No actual3Dheight/leadform/solderstandard/normativeclearance or thermal approval.','assigned':len(pos),'physical_pads':79,'rectangle_mm':[W,L],'court_or_allocation_overruns':overruns,'sameface_box_collisions':collisions,'oppositeface_THT_joint_obstacle_collisions':jointcollisions,'min_PS_projected_bbox_mm':q['min_projected_PS_bbox_distance_mm'],'min_pad_bbox_edge_mm':q['min_copper_bbox_edge_distance_mm'],'T1_finished_allocation_verified':False,'joint_allowance_is_proposal_mm':.4},indent=2))
