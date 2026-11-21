"""Bounded root router: full pair clearances; no package exceptions in new paths."""
from pathlib import Path
import json,math,heapq,time,hashlib,shutil,sys,os
import numpy as np
import pcbnew as k
R=Path(__file__).resolve().parents[2]/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';D=Path(__file__).resolve().parent/'routing';src=Path(os.environ.get('SC09_ROUTE_BOARD',str(S/'SC09_compact.kicad_pcb')));b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(src));origin=(100,100)
STEP=.1;NX=501;NY=321;LAYERS=[k.F_Cu,k.B_Cu];VD=.75;DRILL=.3;EPS=.01
pads={(f.GetReference(),p.GetNumber()):p for f in b.GetFootprints() for p in f.Pads()};coords=lambda p:(k.ToMM(p.x)-100,k.ToMM(p.y)-100);P=lambda r,n:coords(pads[r,str(n)].GetPosition());v=lambda x,y:k.VECTOR2I(k.FromMM(x+100),k.FromMM(y+100))
matrix=json.loads(Path(os.environ.get('SC09_ROUTE_MATRIX',str(R.parent/'compact09/spacing-thermal/spacing-contract.proposed.json'))).read_text());pair={tuple(sorted((p['net_a'],p['net_b']))):max(.3,p['surface_creepage_target_mm']) for p in matrix['pair_matrix']}
def sep(a,c):return 0 if a==c else pair.get(tuple(sorted((a.lstrip('/'),c.lstrip('/')))),.3)
def win(x0,y0,x1,y1,r):
 lo=max(0,math.floor((x0-r)/STEP));hi=min(NX,math.ceil((x1+r)/STEP)+1);bot=max(0,math.floor((y0-r)/STEP));top=min(NY,math.ceil((y1+r)/STEP)+1);return slice(lo,hi),slice(bot,top),np.ogrid[lo:hi,bot:top]
def stamp_rect(f,box,r):
 x0,y0,x1,y1=box;xs,ys,(xx,yy)=win(*box,r);xx=xx*STEP;yy=yy*STEP;dx=np.maximum(np.maximum(x0-xx,xx-x1),0);dy=np.maximum(np.maximum(y0-yy,yy-y1),0);f[xs,ys]|=dx*dx+dy*dy<=r*r
def stamp_seg(f,a,c,r):
 x0,y0=a;x1,y1=c;xs,ys,(xx,yy)=win(min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1),r);xx=xx*STEP-x0;yy=yy*STEP-y0;dx=x1-x0;dy=y1-y0;t=np.clip((xx*dx+yy*dy)/(dx*dx+dy*dy),0,1) if dx or dy else 0;f[xs,ys]|=(xx-t*dx)**2+(yy-t*dy)**2<=r*r
def fields(net,width):
 blocked=np.zeros((2,NX,NY),bool);vb=np.zeros((NX,NY),bool);x,y=np.ogrid[:NX,:NY];x=x*STEP;y=y*STEP
 def border(rad):
  gap=.5+rad+EPS;return (x<gap)|(x>50-gap)|(y<gap)|(y>32-gap)|(x+y<.8+gap*math.sqrt(2))|(x-y>49.2-gap*math.sqrt(2))|(-x+y>31.2-gap*math.sqrt(2))|(x+y>81.2-gap*math.sqrt(2))
 blocked|=border(width/2);vb|=border(VD/2)
 # Source-controlled native can/vent rule area; front copper and all vias excluded.
 stamp_rect(blocked[0],(6.5,.25,33.5,13.25),width/2+EPS);stamp_rect(vb,(6.5,.25,33.5,13.25),VD/2+EPS)
 for p in pads.values():
  if p.GetNetname()==net:continue
  gap=sep(net,p.GetNetname())+EPS;pt=coords(p.GetPosition());bb=p.GetBoundingBox();a=coords(bb.GetOrigin());c=coords(bb.GetEnd());box=(*a,*c)
  for i,layer in enumerate(LAYERS):
   if not p.IsOnLayer(layer):continue
   if p.GetShape()==k.PAD_SHAPE_CIRCLE:stamp_seg(blocked[i],pt,pt,k.ToMM(p.GetSize().x)/2+gap+width/2)
   else:stamp_rect(blocked[i],box,gap+width/2)
  if p.GetShape()==k.PAD_SHAPE_CIRCLE:stamp_seg(vb,pt,pt,k.ToMM(p.GetSize().x)/2+gap+VD/2)
  else:stamp_rect(vb,box,gap+VD/2)
 for t in b.GetTracks():
  if t.GetNetname()==net:continue
  gap=sep(net,t.GetNetname())+EPS
  if isinstance(t,k.PCB_VIA):
   pt=coords(t.GetPosition());r=k.ToMM(t.GetWidth(k.F_Cu))/2
   for i in range(2):stamp_seg(blocked[i],pt,pt,r+gap+width/2)
   stamp_seg(vb,pt,pt,r+gap+VD/2)
  else:
   i=LAYERS.index(t.GetLayer());a=coords(t.GetStart());c=coords(t.GetEnd());r=k.ToMM(t.GetWidth())/2;stamp_seg(blocked[i],a,c,r+gap+width/2);stamp_seg(vb,a,c,r+gap+VD/2)
 return blocked,vb
def search(starts,ends,field,vfield):
 if not starts or not ends:return None,0
 ends=set(ends);ex,ey=next(iter(ends))[:2];h=lambda x,y:max(abs(x-ex),abs(y-ey))+.41421356237*min(abs(x-ex),abs(y-ey));cost={s:0 for s in starts};prev={};queue=[(h(*s[:2]),0,s) for s in starts];heapq.heapify(queue);count=0
 while queue:
  _,g,s=heapq.heappop(queue)
  if g!=cost[s]:continue
  count+=1
  if s in ends:
   path=[s]
   while path[-1] in prev:path.append(prev[path[-1]])
   return path[::-1],count
  x,y,side=s
  for dx,dy,dist in [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]:
   xx=x+dx;yy=y+dy
   if not 0<=xx<NX or not 0<=yy<NY or field[side,xx,yy] or (dx and dy and (field[side,xx,y] or field[side,x,yy])):continue
   t=(xx,yy,side);gg=g+dist
   if gg<cost.get(t,math.inf):cost[t]=gg;prev[t]=s;heapq.heappush(queue,(gg+h(xx,yy),gg,t))
  if not vfield[x,y] and not field[1-side,x,y]:
   t=(x,y,1-side);gg=g+35
   if gg<cost.get(t,math.inf):cost[t]=gg;prev[t]=s;heapq.heappush(queue,(gg+h(x,y),gg,t))
 return None,count
def simplify(path):
 if len(path)<3:return path
 result=[path[0]]
 for a,c,d in zip(path,path[1:],path[2:]):
  if tuple(c[i]-a[i] for i in range(3))!=tuple(d[i]-c[i] for i in range(3)):result.append(c)
 return result+[path[-1]]
def ep(r,n):
 p=pads[r,str(n)];return P(r,n),[i for i,l in enumerate(LAYERS) if p.IsOnLayer(l)]
jobs=[('LED_PLUS',ep('R7',2),ep('T1',1)),('DC_RETURN',ep('C4',2),ep('C6',2)),('DC_RETURN',((32.3,14.8),[1]),ep('C4',2)),('DC_RETURN',ep('C1',2),ep('C4',2)),('BUS_RECT',ep('C1',1),((37.3,15.375),[1])),('BUS_RECT',ep('L1',1),((37.3,15.375),[1])),('BUS_FILTERED',ep('C4',1),((46.65,9.1),[0,1])),('FB_INDUCTOR',ep('D1',1),((44.8,4.35),[0,1])),('AC_FUSED',ep('RV1',1),((36.2,9.15),[1])),('AC_N',ep('RV1',2),((31.8,10.025),[1])),('AC_N',ep('J1',2),((31.8,10.025),[1])),('M',ep('R7',1),ep('R4',1)),('M',((48.5,5.065),[0,1]),ep('R4',1))]
if len(sys.argv)>1:jobs=[jobs[int(i)] for i in sys.argv[1].split(',')]
results=[]
for name,(a,sa),(c,sc) in jobs:
 width=.3 if name in ['M','BP'] else .4;net='/'+name;field,vfield=fields(net,width);starts=[(round(a[0]/STEP),round(a[1]/STEP),i) for i in sa];ends=[(round(c[0]/STEP),round(c[1]/STEP),i) for i in sc];starts=[s for s in starts if not field[s[2],s[0],s[1]]];ends=[s for s in ends if not field[s[2],s[0],s[1]]];t0=time.monotonic();path,count=search(starts,ends,field,vfield);row={'net':name,'from':a,'to':c,'starts':starts,'ends':ends,'success':path is not None,'expanded':count,'seconds':time.monotonic()-t0};results.append(row);print(json.dumps(row),flush=True)
 if not path:continue
 path=simplify(path);nt=next(p.GetNet() for p in pads.values() if p.GetNetname()==net)
 def track(aa,cc,i):
  if math.dist(aa,cc)<1e-6:return
  t=k.PCB_TRACK(b);t.SetNet(nt);t.SetLayer(LAYERS[i]);t.SetWidth(k.FromMM(width));t.SetStart(v(*aa));t.SetEnd(v(*cc));b.Add(t)
 xy=lambda state:(state[0]*STEP,state[1]*STEP)
 track(a,xy(path[0]),path[0][2])
 for aa,cc in zip(path,path[1:]):
  if aa[2]==cc[2]:track(xy(aa),xy(cc),aa[2])
  else:
   via=k.PCB_VIA(b);via.SetNet(nt);via.SetPosition(v(*xy(aa)));via.SetViaType(k.VIATYPE_THROUGH);via.SetLayerPair(k.F_Cu,k.B_Cu);via.SetWidth(k.FromMM(VD));via.SetDrill(k.FromMM(DRILL));b.Add(via)
 track(xy(path[-1]),c,path[-1][2])
candidate=D/'grid-candidate.kicad_pcb';assert k.SaveBoard(str(candidate),b,True)
saved=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(candidate));expected={(r,n):p.GetNetname() for (r,n),p in pads.items()};actual={(f.GetReference(),p.GetNumber()):p.GetNetname() for f in saved.GetFootprints() for p in f.Pads()};assert expected==actual,'Native changed pad nets'
shutil.copy2(src,D/'before-grid.kicad_pcb');shutil.copy2(candidate,src);(D/'grid-results.json').write_text(json.dumps(results,indent=2)+'\n');print('GRID',sum(r['success'] for r in results),'/',len(results),flush=True)

