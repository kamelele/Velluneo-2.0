"""Two-layer, scoped-clearance routing experiment; native DRC is authoritative."""
from pathlib import Path
import json,math,heapq,itertools,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
D=Path(__file__).resolve().parent;j=json.loads((D/globals().get('INPUT_FILE','route-input.json')).read_text());pads={p['key']:p for p in j['pads']};fixed=j['tracks'];new=[];results=[];step=globals().get('GRID_STEP',.2);board_bounds=j['outline_bbox_mm'];bounds=globals().get('GRID_BOUNDS',board_bounds);nx=round((bounds[2]-bounds[0])/step)+1;ny=round((bounds[3]-bounds[1])/step)+1
X=np.arange(nx)[:,None]*step+bounds[0];Y=np.arange(ny)[None,:]*step+bounds[1];XX=np.broadcast_to(X,(nx,ny));YY=np.broadcast_to(Y,(nx,ny));NN=nx*ny
aliases={'Net-(F1-Pad1)':'AC_CAP_A','Net-(BR1-AC-Pad2)':'AC_CAP_B','Net-(F1-Pad2)':'AC_FUSED','Net-(BR1-AC-Pad4)':'AC_LIMITED','Net-(D1-K)':'CLAMP','Net-(D2-K)':'AUX_RECT','Net-(R2-Pad2)':'BLEED_MID'}
for p in pads.values():p['net']=aliases.get(p['net'],p['net'])
for t in fixed:t['net']=aliases.get(t['net'],t['net'])
hv={'AC_CAP_A','AC_CAP_B','AC_FUSED','AC_LIMITED','BULK_POS','DRAIN','CLAMP','STARTUP_MID'};quiet={'PRIMARY_GND','SENSE','CS','DRV','GATE','VDD','AUX_RAW','AUX_RECT','VS','NTC'};sec={'SECONDARY_RAW','OUTPUT_POS','OUTPUT_NEG'}
NEGOTIATED=False
HISTORY=np.zeros((2,nx,ny),dtype=float)
def domainpad(k):return'S'if k.split('.')[0]in{'D3','C4','J2','R11','R12'}or(k.startswith('T1.')and k.split('.')[1]in{'6','7','8','9','10'})else'P'
def limit(a,b,da,db):return 10. if da!=db else 3. if(a in hv and b in quiet)or(b in hv and a in quiet)else .25
def pointseg(a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];den=dx*dx+dy*dy
 t=np.clip(((XX-a[0])*dx+(YY-a[1])*dy)/(den or 1),0,1);return np.hypot(XX-(a[0]+t*dx),YY-(a[1]+t*dy))
def mask(net,width,label,ends,via=False,include_new=True):
 da='S'if net in sec else'P';r=.3 if via else width/2;bad=np.zeros((2,nx,ny),dtype=bool)
 edge=(XX<board_bounds[0]+.5+r+.005)|(XX>board_bounds[2]-.5-r-.005)|(YY<board_bounds[1]+.5+r+.005)|(YY>board_bounds[3]-.5-r-.005);bad[:]=edge
 for area in j['rectangular_rule_areas']:
  q=area['box'];z=(XX>q[0]-r)&(XX<q[2]+r)&(YY>q[1]-r)&(YY<q[3]+r)
  for l in area['layers']:bad[l]|=z
 star='T1.4'if label in{'aux_tap','aux_feed'}else'Q1.3'if label=='source_pulldown'else'C1.2'if label in{'charging_ground','aux_ground','aux_branch','quiet_ground'}else'R9.1'if label=='power_shunt'else None
 exempt=(np.hypot(XX-pads[star]['xy'][0],YY-pads[star]['xy'][1])<.8+r)if star else np.zeros((nx,ny),dtype=bool)
 if label=='power_shunt':exempt|=np.hypot(XX-pads['Q1.3']['xy'][0],YY-pads['Q1.3']['xy'][1])<.8+r
 for k,p in pads.items():
  same=p['net']==net;blocksame=False
  if star and same and k not in ends:blocksame=True
  if label=='quiet_ground'and k not in{'R9.2','BR1.3','T1.2','C3.2','R3.2','R15.2'}:blocksame=False
  if label in{'aux_branch','aux_ground'}and k in{'T1.2','C3.2','R3.2','R15.2','C1.2'}:blocksame=False
  if same and not blocksame and not(via and p['tht']):continue
  gap=(.1 if same and via else .25 if same else limit(net,p['net'],da,domainpad(k)))+r+.015
  b=p['box'];dd=np.hypot(np.maximum(np.maximum(b[0]-XX,XX-b[2]),0),np.maximum(np.maximum(b[1]-YY,YY-b[3]),0));z=dd<gap
  if p.get('circle'):z=np.hypot(XX-p['xy'][0],YY-p['xy'][1])<gap+p['size_mm'][0]/2
  if same and star:z&=~exempt
  layers=(0,1)if via or da!=domainpad(k)else p['layers']
  for l in layers:bad[l]|=z
 for t in fixed+(new if include_new else []):
  if t.get('projection_only')and net not in hv:continue
  same=t['net']==net
  if same and not star and not(via and t['via']):continue
  if same and star:
   if label in{'aux_branch','aux_ground'}and t.get('label')in{'aux_ground','aux_branch'}:continue
   if label=='quiet_ground':
    power=t.get('label')in{'charging_ground','aux_ground','aux_branch','shunt_return'}or(t.get('label')is None and t['net']=='PRIMARY_GND'and abs(t['width']-1)<1e-6)
    if not power:continue
   # Separate pulse-current branch from every existing quiet conductor until its pad junction.
   if label=='power_shunt'and t.get('origin')=='new':continue
  db='S'if t['net']in sec else'P';gap=(.25 if same else limit(net,t['net'],da,db))+r+t['width']/2+.015;z=pointseg(t['a'],t['b'])<gap
  if same and star:z&=~exempt
  layers=(0,1)if via or da!=db else t['layers']
  for l in layers:bad[l]|=z
 return bad
def xy(ix,iy):return(ix*step+bounds[0],iy*step+bounds[1])
def grid(p):return(round((p[0]-bounds[0])/step),round((p[1]-bounds[1])/step))
def plan(a,b,width,label):
 print('TRY',label,a,b,width,flush=True);deadline=time.monotonic()+3
 net=pads[a]['net'];assert net==pads[b]['net'];bad=mask(net,width,label,{a,b},include_new=not NEGOTIATED);penalty=((mask(net,width,label,{a,b})&~bad)*80.+HISTORY) if NEGOTIATED else np.zeros_like(bad,dtype=float);vmask=None;aa=grid(pads[a]['xy']);bb=grid(pads[b]['xy']);starts=[];targets=set()
 for l in pads[a]['layers']:
  if not bad[l,*aa]:starts.append((l,*aa))
 for l in pads[b]['layers']:
  if not bad[l,*bb]:targets.add((l,*bb))
 if not starts or not targets:return None,'blocked endpoint'
 ids=np.arange(2*NN).reshape(2,nx,ny);rr=[];cc=[];ww=[]
 for dx,dy in((1,0),(0,1),(1,1),(1,-1)):
  xa=slice(0,nx-dx);xb=slice(dx,nx)
  ya=slice(max(0,-dy),min(ny,ny-dy));yb=slice(max(0,dy),min(ny,ny+dy))
  good=~(bad[:,xa,ya]|bad[:,xb,yb])
  if dx and dy:good&=~(bad[:,xa,yb]|bad[:,xb,ya])
  u=ids[:,xa,ya][good];v=ids[:,xb,yb][good];cost=math.hypot(dx,dy)+(penalty[:,xa,ya][good]+penalty[:,xb,yb][good])/2;rr.extend((u,v));cc.extend((v,u));ww.extend((cost,cost))
 vmask=mask(net,width,label,{a,b},via=True,include_new=not NEGOTIATED);good=~(vmask[0]|vmask[1]|bad[0]|bad[1]);reuse={}
 for p in pads.values():
  if p['net']==net and p['tht']:reuse[grid(p['xy'])]=p['xy']
 for t in fixed+(new if not NEGOTIATED else []):
  if t['net']==net and t['via']:reuse[grid(t['a'])]=t['a']
 for (x,y),p in reuse.items():
  if not(0<=x<nx and 0<=y<ny):continue
  if not(bad[0,x,y]or bad[1,x,y]):good[x,y]=True
 u=ids[0][good];v=ids[1][good]
 via_penalty=mask(net,width,label,{a,b},via=True)&~vmask if NEGOTIATED else np.zeros_like(vmask)
 vc=3.+80.*(via_penalty[0][good]|via_penalty[1][good])+HISTORY[0][good]+HISTORY[1][good];rr.extend((u,v));cc.extend((v,u));ww.extend((vc,vc))
 graph=coo_matrix((np.concatenate(ww),(np.concatenate(rr),np.concatenate(cc))),shape=(2*NN,2*NN)).tocsr()
 dist,pred,source=dijkstra(graph,indices=[int(ids[s])for s in starts],min_only=True,return_predecessors=True)
 target=min((int(ids[t])for t in targets),key=lambda q:dist[q])
 if not np.isfinite(dist[target]):return None,'no two-layer grid witness (exhaustive grid graph)'
 nodes=[tuple(map(int,np.unravel_index(target,ids.shape)))]
 while nodes[-1]not in starts:
  target=int(pred[target]);assert target>=0;nodes.append(tuple(map(int,np.unravel_index(target,ids.shape))))
 nodes.reverse();pts=[(nodes[0][0],*pads[a]['xy'])];old=nodes[0]
 for l,x,y in nodes:
  if l!=old[0]and(x,y)in reuse:pts.extend([(old[0],*reuse[x,y]),(l,*reuse[x,y])])
  pts.append((l,*xy(x,y)));old=(l,x,y)
 pts.append((nodes[-1][0],*pads[b]['xy']))
 # Keep orthogonal/45-degree grid geometry, removing collinear vertices only.
 compact=[]
 for p in pts:
  if compact and p==compact[-1]:continue
  if len(compact)>=2 and p[0]==compact[-1][0]==compact[-2][0]:
   z,q=compact[-2],compact[-1]
   if abs((q[1]-z[1])*(p[2]-q[2])-(q[2]-z[2])*(p[1]-q[1]))<1e-8:compact.pop()
  compact.append(p)
 elements=[]
 for p,q in zip(compact,compact[1:]):
  if p[0]!=q[0]:
   if any(math.dist(p[1:],v)<1e-7 for v in reuse.values()):continue
   elements.append(dict(net=net,a=list(p[1:]),b=list(p[1:]),width=.6,layers=[0,1],via=True,origin='new',label=label))
  elif math.dist(p[1:],q[1:])>1e-8:elements.append(dict(net=net,a=list(p[1:]),b=list(q[1:]),width=width,layers=[p[0]],via=False,origin='new',label=label))
 return elements,None
groups=None # Geometry kernel is consumed by the bounded planning helpers.
