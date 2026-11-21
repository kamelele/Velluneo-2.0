from pathlib import Path
import pcbnew as p,math,json
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16';f=D/'design/Velluneo_driver.kicad_pcb';b=p.LoadBoard(str(f))
def mm(v):return p.ToMM(v)
def box(q):
 r=q.GetBoundingBox();return[mm(r.GetX()),mm(r.GetY()),mm(r.GetRight()),mm(r.GetBottom())]
def hits(a,c,g=0):return a[0]<c[2]+g and a[2]>c[0]-g and a[1]<c[3]+g and a[3]>c[1]-g
ob={p.F_SilkS:[],p.B_SilkS:[]};bodies={p.F_SilkS:[],p.B_SilkS:[]};fps=list(b.GetFootprints())
for fp in fps:
 for layer,mask,crt in[(p.F_SilkS,p.F_Mask,p.F_CrtYd),(p.B_SilkS,p.B_Mask,p.B_CrtYd)]:
  for q in fp.Pads():
   if q.IsOnLayer(mask):ob[layer].append(box(q))
  for q in fp.GraphicalItems():
   if q.GetLayer()==layer:ob[layer].append(box(q))
  bb=[box(q)for q in fp.GraphicalItems()if q.GetLayer()==crt]
  if bb:bodies[layer].append([min(q[0]for q in bb),min(q[1]for q in bb),max(q[2]for q in bb),max(q[3]for q in bb)])
for q in b.GetDrawings():
 if q.GetLayer()in ob:ob[q.GetLayer()].append(box(q))
placed=[]
for fp in sorted(fps,key=lambda q:(-len(q.GetReference()),q.GetReference())):
 t=fp.Reference();layer=t.GetLayer();t.SetTextSize(p.VECTOR2I(p.FromMM(1),p.FromMM(1)));t.SetTextThickness(p.FromMM(.15));t.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));center=(mm(fp.GetPosition().x),mm(fp.GetPosition().y));candidates=[(mm(t.GetPosition().x),mm(t.GetPosition().y))]
 for xx in range(157,244):
  for yy in range(142,259):candidates.append((xx*.5,yy*.5))
 best=None
 for x,y in candidates:
  t.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));r=box(t)
  if r[0]<77.7 or r[2]>122.3 or r[1]<70.2 or r[3]>129.8:continue
  if any(hits(r,q,.23)for q in ob[layer]):continue
  cost=math.hypot(x-center[0],y-center[1])+sum(10 for q in bodies[layer]if hits(r,q,.10))
  if best is None or cost<best[0]:best=(cost,x,y,r)
 assert best is not None,fp.GetReference()
 _,x,y,r=best;t.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));ob[layer].append(r);placed.append(dict(ref=fp.GetReference(),xy_mm=[x,y],layer=b.GetLayerName(layer),under_body_penalty=best[0]-math.hypot(x-center[0],y-center[1])))
p.SaveBoard(str(f),b);(D/'checks/silkscreen-placement.json').write_text(json.dumps(dict(scope='Actual reference field placements,1mm/.15mm font; conservative obstacle search then native DRC is authoritative. No silk violations suppressed.',references=placed),indent=2)+'\n');print('placed',len(placed),'reference labels')
