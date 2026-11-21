"""Isolated exploratory current-path coupon, not accepted product routing.
Native DRC remains authoritative; no source/rule exclusion is introduced.
"""
from pathlib import Path
import json,math,heapq,shutil,hashlib,importlib.util,pcbnew
D=Path(__file__).resolve().parent;E=D/'design';S=D/'studies/sense';S.mkdir(parents=True,exist_ok=True);B='Velluneo_sense_exploration';spec=importlib.util.spec_from_file_location('geom',E/'full_geometry.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
board=pcbnew.LoadBoard(str(E/'Velluneo_specification_reset.kicad_pcb'));assert not list(board.GetTracks());fps={f.GetReference():f for f in board.GetFootprints()};pads={f.GetReference()+'.'+p.GetNumber():p for f in fps.values()for p in f.Pads()};added=[];rows=[];grid=.2
def segdist(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))if dx or dy else 0
 return math.dist(p,(a[0]+t*dx,a[1]+t*dy))
def route(label,start,end,width,side='F',start_xy=None,end_xy=None):
 a=start_xy or g.centres[start];z=end_xy or g.centres[end];net=g.pads[start]['net'];assert net==g.pads[end]['net'];cache={}
 def allowed(p):
  x,y=p
  if abs(x)>g.HW-.5-width/2+1e-9 or abs(y)>g.HH-.5-width/2+1e-9:return False
  for key,q in g.pads.items():
   if key in(start,end):continue
   hv=q['net']in g.hv;isquiet=net in g.quiet
   if not(q['tht']or g.pos[q['ref']]['side']==side or q['domain']=='S'):continue
   limit=10 if q['domain']=='S'else 3 if(hv and isquiet)else .25
   bb=q['box'];dist=math.hypot(max(bb[0]-x,x-bb[2],0),max(bb[1]-y,y-bb[3],0))
   if dist<limit+width/2-1e-8:return False
  for old in added:
   if old['net']==net or old['side']!=side:continue
   if segdist(p,old['a'],old['b'])<.25+(width+old['width'])/2-1e-8:return False
  return True
 def oksegment(p,q):
  n=max(1,math.ceil(math.dist(p,q)/.05));return all(allowed((p[0]+(q[0]-p[0])*t/n,p[1]+(q[1]-p[1])*t/n))for t in range(n+1))
 if oksegment(a,z):points=[a,z]
 else:
  aa=tuple(round(v/grid)for v in a);zz=tuple(round(v/grid)for v in z)
  def xy(k):return(k[0]*grid,k[1]*grid)
  def valid(k):
   if k not in cache:cache[k]=allowed(xy(k))
   return cache[k]
  assert oksegment(a,xy(aa))and oksegment(xy(zz),z),(label,'endpoint grid exit blocked')
  heap=[(math.dist(aa,zz),0,aa)];cost={aa:0};prev={};found=False
  while heap:
   _,cc,k=heapq.heappop(heap)
   if cc>cost[k]+1e-9:continue
   if k==zz:found=True;break
   for dx,dy in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
    nxt=(k[0]+dx,k[1]+dy)
    if not valid(nxt):continue
    if dx and dy and(not valid((k[0]+dx,k[1]))or not valid((k[0],k[1]+dy))):continue
    nc=cc+math.hypot(dx,dy)
    if nc<cost.get(nxt,1e20):cost[nxt]=nc;prev[nxt]=k;heapq.heappush(heap,(nc+math.dist(nxt,zz),nc,nxt))
  if not found:return dict(label=label,start=start,end=end,routed=False,reason='No '+side+'-layer grid witness at unchanged native numerical limits; no rule weakened',explored_vertices=len(cost))
  chain=[zz]
  while chain[-1]!=aa:chain.append(prev[chain[-1]])
  raw=[a]+[xy(k)for k in reversed(chain)]+[z];points=[raw[0]];i=0
  while i<len(raw)-1:
   j=len(raw)-1
   while j>i+1 and not oksegment(raw[i],raw[j]):j-=1
   if math.dist(points[-1],raw[j])>1e-8:points.append(raw[j])
   i=j
 for p,q in zip(points,points[1:]):
  assert oksegment(p,q);t=pcbnew.PCB_TRACK(board);t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(p[0]+100),pcbnew.FromMM(p[1]+100)));t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(q[0]+100),pcbnew.FromMM(q[1]+100)));t.SetLayer(pcbnew.F_Cu if side=='F'else pcbnew.B_Cu);t.SetWidth(pcbnew.FromMM(width));t.SetNet(pads[start].GetNet());board.Add(t);added.append(dict(a=p,b=q,width=width,net=net,side=side))
 length=sum(math.dist(p,q)for p,q in zip(points,points[1:]));return dict(label=label,start=start,end=end,routed=True,width_mm=width,layer=side+'.Cu',points_relative_mm=points,length_mm=length,endpoint_mm=math.dist(a,z),topology='Dedicated endpoint branch, not full operating-loop/return qualification')
for params in [('short_shunt_bulk_return','R9.2','C1.2',1.0),('local_CS_RLC','R6.2','U1.4',.4),('dedicated_SENSE_branch','R9.1','R6.1',.4)]:rows.append(route(*params))
if not rows[-1]['routed']:
 va=(-17.2,21.6);vz=(.8,24.6)
 attempt=route('dedicated_SENSE_B_study','R9.1','R6.1',.4,'B',va,vz);rows.append(attempt)
 if attempt['routed']:
  rows.append(route('SENSE_F_entry','R9.1','R9.1',.4,end_xy=va));rows.append(route('SENSE_F_exit','R6.1','R6.1',.4,end_xy=vz));assert all(r['routed']for r in rows[-2:])
  for xy in(va,vz):
   v=pcbnew.PCB_VIA(board);v.SetViaType(pcbnew.VIATYPE_THROUGH);v.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(xy[0]+100),pcbnew.FromMM(xy[1]+100)));v.SetWidth(pcbnew.FromMM(1.0));v.SetDrill(pcbnew.FromMM(.3));v.SetNet(pads['R9.1'].GetNet());board.Add(v)
for f in board.GetFootprints():
 replacements=[]
 for oldmodel in f.Models():
  m=pcbnew.FP_3DMODEL();m.m_Filename=oldmodel.m_Filename.replace('${KIPRJMOD}/models/','${KIPRJMOD}/../../design/models/')
  for attr in('m_Scale','m_Rotation','m_Offset','m_Opacity','m_Show'):setattr(m,attr,getattr(oldmodel,attr))
  replacements.append(m)
 f.Models().clear()
 for m in replacements:f.Add3DModel(m)
for obj in board.GetDrawings():
 if isinstance(obj,pcbnew.PCB_TEXT)and obj.GetText().startswith('OWNER-SELECTED33'):obj.SetText('CONTROL05 SENSE STUDY - PARTIAL TRACKS - NOT ACCEPTED ROUTING')
assert pcbnew.SaveBoard(str(S/(B+'.kicad_pcb')),board)
for ext in('.kicad_pro','.kicad_dru','.kicad_sch'):shutil.copyfile(E/('Velluneo_specification_reset'+ext),S/(B+ext))
(S/'fp-lib-table').write_text((E/'fp-lib-table').read_text().replace('${KIPRJMOD}/','${KIPRJMOD}/../../design/'),encoding='utf-8',newline='\n')
(S/'sym-lib-table').write_text((E/'sym-lib-table').read_text().replace('${KIPRJMOD}/','${KIPRJMOD}/../../design/'),encoding='utf-8',newline='\n')
out=dict(scope='Isolated exploratory current/sense branches; NOT product routing acceptance or complete Kelvin/driver-return/loop proof.',algorithm='Bounded0.2mm A* with conservative padboxes, explicit3/10mm/edge limits and nativeDRCrequired. MainproductPCBunmodified.',basis_board_sha256=hashlib.sha256((E/'Velluneo_specification_reset.kicad_pcb').read_bytes()).hexdigest(),routes=rows,tracks_and_vias=len(list(board.GetTracks())),vias=sum(isinstance(t,pcbnew.PCB_VIA)for t in board.GetTracks()),stage_approved=False,main_product_tracks=0,via_assembly_qualification='Via proximity to opposite bodies and tenting/assembly process require review; no qualified via-in-pad process inferred.')
(S/'study-result.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(out,indent=2))
