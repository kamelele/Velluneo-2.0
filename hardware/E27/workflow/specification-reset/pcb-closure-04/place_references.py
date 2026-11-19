"""Relocate visible native reference fields around the same footprints, never hide failures."""
from pathlib import Path
import pcbnew,json,math
D=Path(__file__).resolve().parent;B='Velluneo_specification_reset';board=pcbnew.LoadBoard(str(D/(B+'.kicad_pcb')));assert board
fps={f.GetReference():f for f in board.GetFootprints()}
report=json.loads((D/'checks/before-reference-drc.json').read_text(encoding='utf-8'))
movable=set()
for finding in report['violations']:
 if finding['type'].startswith('silk_'):
  for item in finding['items']:
   desc=item['description']
   if desc.startswith('Reference field of '):movable.add(desc.removeprefix('Reference field of '))
def bbox(obj):
 b=obj.GetBoundingBox();return[pcbnew.ToMM(b.GetX()),pcbnew.ToMM(b.GetY()),pcbnew.ToMM(b.GetRight()),pcbnew.ToMM(b.GetBottom())]
def intersect(a,b,gap=.30):return a[0]<b[2]+gap and b[0]<a[2]+gap and a[1]<b[3]+gap and b[1]<a[3]+gap
def near_circle(a,c):
 x,y,r,w=c;minimum=math.hypot(max(a[0]-x,x-a[2],0),max(a[1]-y,y-a[3],0));maximum=max(math.hypot(xx-x,yy-y)for xx in(a[0],a[2])for yy in(a[1],a[3]))
 return minimum<=r+w/2+.30 and maximum>=r-w/2-.30
obstacles={pcbnew.F_SilkS:[],pcbnew.B_SilkS:[]}
for layer,copper in((pcbnew.F_SilkS,pcbnew.F_Cu),(pcbnew.B_SilkS,pcbnew.B_Cu)):
 for ref,f in fps.items():
  for pad in f.Pads():
   if pad.IsOnLayer(copper):obstacles[layer].append(('box',bbox(pad)))
  for g in f.GraphicalItems():
   if g.GetLayer()!=layer:continue
   if isinstance(g,pcbnew.PCB_SHAPE)and g.GetShape()==pcbnew.SHAPE_T_CIRCLE:
    c=g.GetCenter();obstacles[layer].append(('circle',[pcbnew.ToMM(c.x),pcbnew.ToMM(c.y),pcbnew.ToMM(g.GetRadius()),pcbnew.ToMM(g.GetWidth())]))
   else:obstacles[layer].append(('box',bbox(g)))
  if ref not in movable and f.Reference().GetLayer()==layer and f.Reference().IsVisible():obstacles[layer].append(('box',bbox(f.Reference())))
result=[];unresolved=[]
for ref in sorted(movable):
 f=fps[ref];field=f.Reference();layer=field.GetLayer();assert layer in obstacles
 oldxy=[pcbnew.ToMM(field.GetPosition().x),pcbnew.ToMM(field.GetPosition().y)];oldangle=field.GetTextAngle().AsDegrees();base=[pcbnew.ToMM(f.GetPosition().x),pcbnew.ToMM(f.GetPosition().y)]
 candidates=[]
 for dx in range(-24,25):
  for dy in range(-24,25):
   x,y=base[0]+dx*.25,base[1]+dy*.25;cost=math.dist((x,y),oldxy)+.65*math.dist((x,y),base)
   for angle in(0,90):candidates.append((cost+.02*(angle!=oldangle),x,y,angle))
 candidates.sort();chosen=None
 for score,x,y,angle in candidates:
  field.SetTextAngle(pcbnew.EDA_ANGLE(angle,pcbnew.DEGREES_T));field.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y)));a=bbox(field)
  if a[0]<80.3 or a[2]>119.7 or a[1]<70.3 or a[3]>129.7:continue
  if any(intersect(a,b)if kind=='box'else near_circle(a,b)for kind,b in obstacles[layer]):continue
  chosen=(x,y,angle,a);break
 if chosen is None:
  field.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(oldxy[0]),pcbnew.FromMM(oldxy[1])));field.SetTextAngle(pcbnew.EDA_ANGLE(oldangle,pcbnew.DEGREES_T));unresolved.append(ref)
 else:
  x,y,angle,a=chosen;result.append({'ref':ref,'old_xy_mm':oldxy,'new_xy_mm':[x,y],'old_angle_deg':oldangle,'new_angle_deg':angle,'distance_from_component_origin_mm':math.dist((x,y),base)});obstacles[layer].append(('box',a))
 assert field.IsVisible()
pcbnew.SaveBoard(str(D/(B+'.kicad_pcb')),board)
(D/'reference-adjustments.json').write_text(json.dumps({'method':'Visible native reference fields moved on their original silkscreen side; <=6mm grid offsets from component origin; unchanged text height/thickness and all copper. Final nativeDRC is authoritative.','moves':result,'unresolved_search_refs':unresolved,'no_field_hidden':True},indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'reference_moves':len(result),'unresolved':unresolved}))
