"""Bounded octilinear draft router; actual KiCad DRC/connectivity are authoritative.
No waived geometric condition or fabricated external engine execution.
"""
from pathlib import Path
import json,math,heapq,time,itertools
import numpy as np
D=Path(__file__).resolve().parent;j=json.loads((D/'geometry-input.json').read_text());pads={q['key']:q for q in j['pads']}
aliases={'Net-(F1-Pad1)':'AC_CAP_A','Net-(BR1-AC-Pad2)':'AC_CAP_B','Net-(F1-Pad2)':'AC_FUSED','Net-(BR1-AC-Pad4)':'AC_LIMITED','Net-(D1-K)':'CLAMP','Net-(D2-K)':'AUX_RECT','Net-(R2-Pad2)':'BLEED_MID'}
for q in pads.values():q['net']=aliases.get(q['net'],q['net'])
hv={'BULK_POS','DRAIN','STARTUP_MID','AC_CAP_A','AC_CAP_B','AC_FUSED','AC_LIMITED','CLAMP'}
quiet={'PRIMARY_GND','SENSE','CS','DRV','GATE','NTC','VDD','VS','AUX_RAW','AUX_RECT'}
secondary={'SECONDARY_RAW','OUTPUT_POS','OUTPUT_NEG','OUTPUT_BLEED_MID'}
critical={'SENSE','CS'}
tracks=[];results=[];step=.2;via_d=.8;families={}
C1cx=(pads['C1.1']['xy'][0]+pads['C1.2']['xy'][0])/2;C1cy=(pads['C1.1']['xy'][1]+pads['C1.2']['xy'][1])/2
C1bodylayer=0 if j.get('component_sides',{}).get('C1')=='F.Cu'else 3
for name,keys in{'quiet':['U1.5','C2.2','R5.2','RT1.2','R13.2'],'aux':['T1.1','C3.2'],'shunt':['R9.2'],'charge':['BR1.3'],'bleedA':['R3.2'],'bleedB':['R15.2'],'power':['Q1.3','R8.2'],'kelvin':['R6.1']}.items():
 for key in keys:families[key]=name
def domainpad(k):return'S'if k.split('.')[0]in{'C4','D3','R11','R12','J2'}or(k.startswith('T1.')and int(k.split('.')[1])>=6)else'P'
def domainnet(n):return'S'if n in secondary else'P'
def gap(a,b,da,db):return 10.7 if da!=db else 3.0 if(a in hv and b in quiet)or(b in hv and a in quiet)else .25
# Explicit numerical copies of the retained scoped contract; no global relaxation.
def shared_exemption(net,family,other_family,X,Y):
 if family==other_family or other_family is None:return np.ones_like(X,dtype=bool)
 star='C1.2'if net=='PRIMARY_GND'else'R9.1'if net=='SENSE'else None
 if star:
  x,y=pads[star]['xy'];return np.hypot(X-x,Y-y)<(2.0 if net=='PRIMARY_GND'else 1.3)
 return np.zeros_like(X,dtype=bool)
def masks(net,width,family,ends,bounds,via=False):
 nx=round((bounds[2]-bounds[0])/step)+1;ny=round((bounds[3]-bounds[1])/step)+1
 xx=np.arange(nx)[:,None]*step+bounds[0];yy=np.arange(ny)[None,:]*step+bounds[1];X=np.broadcast_to(xx,(nx,ny));Y=np.broadcast_to(yy,(nx,ny));r=via_d/2 if via else width/2;bad=np.zeros((4,nx,ny),dtype=bool)
 bb=j['outline_bbox_mm'];bad[:]=(X<bb[0]+.5+r+.025)|(X>bb[2]-.5-r-.025)|(Y<bb[1]+.5+r+.025)|(Y>bb[3]-.5-r-.025)
 if net not in {'BULK_POS','PRIMARY_GND'}:
  # Preserve C1 body-side unrelated-copper exclusion, including through vias.
  under=np.hypot(X-C1cx,Y-C1cy)<5.25+r+.025
  if via:bad[:]|=under
  else:bad[C1bodylayer]|=under
 for a in j['rectangular_rule_areas']:
  b=a['box'];z=(X>b[0]-r)&(X<b[2]+r)&(Y>b[1]-r)&(Y<b[3]+r)
  for l in a['layers']:bad[l]|=z
 da=domainnet(net)
 for k,q in pads.items():
  same=q['net']==net;foreign_same=same and net in{'PRIMARY_GND','SENSE'}and k not in ends and k not in{'C1.2','R9.1'}and families.get(k)!=family
  if same and not foreign_same:continue
  db=domainpad(k);need=(.25 if same else gap(net,q['net'],da,db))+r+.025;b=q['box'];dist=np.hypot(np.maximum(np.maximum(b[0]-X,X-b[2]),0),np.maximum(np.maximum(b[1]-Y,Y-b[3]),0))
  if q.get('circle'):dist=np.hypot(X-q['xy'][0],Y-q['xy'][1])-q['size_mm'][0]/2
  z=dist<need
  if foreign_same:z&=~shared_exemption(net,family,families.get(k),X,Y)
  layers=range(4)if via or da!=db or(net in hv and q['net']in critical)or(net in critical and q['net']in hv)else q['layers']
  for l in layers:bad[l]|=z
 for q in tracks:
  same=q['net']==net;foreign_same=same and net in{'PRIMARY_GND','SENSE'}and q.get('family')!=family
  if same and not foreign_same:continue
  a,b=q['a'],q['b'];dx=b[0]-a[0];dy=b[1]-a[1];den=dx*dx+dy*dy;t=np.clip(((X-a[0])*dx+(Y-a[1])*dy)/(den or 1),0,1);dist=np.hypot(X-(a[0]+t*dx),Y-(a[1]+t*dy));db=domainnet(q['net']);need=(.25 if same else gap(net,q['net'],da,db))+r+q['width']/2+.025;z=dist<need
  if foreign_same:z&=~shared_exemption(net,family,q.get('family'),X,Y)
  layers=range(4)if via or da!=db or(net in hv and q['net']in critical)or(net in critical and q['net']in hv)else q['layers']
  for l in layers:bad[l]|=z
 return bad
def add_seed_via(key):
 q=pads[key];tracks.append(dict(net=q['net'],a=q['xy'],b=q['xy'],width=via_d,layers=[0,1,2,3],via=True,family='kelvin',label='Kelvin pad takeoff '+key))
add_seed_via('R9.1');add_seed_via('R6.1')
def route(a,b,width,label,family=None,preferred=0,force=None):
 t0=time.monotonic();net=pads[a]['net'];assert net==pads[b]['net'],(a,b,net,pads[b]['net']);family=family or label
 bounds=[-22.5,-30,22.5,-17.1]if domainnet(net)=='S'else[-22.5,-8,22.5,30]
 bad=masks(net,width,family,{a,b},bounds);vbad=masks(net,width,family,{a,b},bounds,True);nx,ny=bad.shape[1:]
 def grid(pt):return(round((pt[0]-bounds[0])/step),round((pt[1]-bounds[1])/step))
 def xy(x,y):return[x*step+bounds[0],y*step+bounds[1]]
 reuse={}
 for k,q in pads.items():
  if q['net']==net and q['tht']:reuse[grid(q['xy'])]=q['xy']
 for q in tracks:
  if q['net']==net and q['via']:reuse[grid(q['a'])]=q['a']
 def endpoint_layers(k):
  q=pads[k];return list(range(4))if grid(q['xy'])in reuse else q['layers']
 aa,bb=grid(pads[a]['xy']),grid(pads[b]['xy']);starts=[(l,*aa)for l in endpoint_layers(a)if(force is None or force==l)and not bad[l,*aa]];targets={(l,*bb)for l in endpoint_layers(b)if(force is None or force==l)and not bad[l,*bb]}
 if not starts or not targets:return False,dict(label=label,a=a,b=b,reason='blocked endpoint',starts=starts,targets=list(targets))
 def h(x,y):dx=abs(x-bb[0]);dy=abs(y-bb[1]);return max(dx,dy)+(math.sqrt(2)-1)*min(dx,dy)
 def code(l,x,y):return(l*nx+x)*ny+y
 def state(c):l,rem=divmod(c,nx*ny);x,y=divmod(rem,ny);return l,x,y
 n=4*nx*ny;dist=np.full(n,np.inf);prev=np.full(n,-1,dtype=np.int32);directions=np.full(n,-1,dtype=np.int8);heap=[]
 for l,x,y in starts:c=code(l,x,y);dist[c]=0;heapq.heappush(heap,(h(x,y),0,c))
 dirs=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)];target=None;visits=0
 while heap:
  _,g,c=heapq.heappop(heap)
  if g>dist[c]+1e-9:continue
  l,x,y=state(c);visits+=1
  if(l,x,y)in targets:target=c;break
  for di,(dx,dy)in enumerate(dirs):
   xx,yy=x+dx,y+dy
   if not(0<=xx<nx and 0<=yy<ny)or bad[l,xx,yy]:continue
   if dx and dy and(bad[l,x,yy]or bad[l,xx,y]):continue
   cc=code(l,xx,yy);cost=(math.sqrt(2)if dx and dy else 1)*(1 if l==preferred else 1.10)+(.12 if directions[c]>=0 and directions[c]!=di else 0);gg=g+cost
   if gg<dist[cc]-1e-9:dist[cc]=gg;prev[cc]=c;directions[cc]=di;heapq.heappush(heap,(gg+h(xx,yy),gg,cc))
  if force is None and((x,y)in reuse or not np.any(vbad[:,x,y]|bad[:,x,y])):
   for ll in range(4):
    if ll==l or bad[ll,x,y]:continue
    cc=code(ll,x,y);gg=g+(1 if(x,y)in reuse else 18)
    if gg<dist[cc]-1e-9:dist[cc]=gg;prev[cc]=c;directions[cc]=directions[c];heapq.heappush(heap,(gg+h(x,y),gg,cc))
 if target is None:return False,dict(label=label,a=a,b=b,reason='no path',visits=visits)
 nodes=[];c=target
 while c>=0:nodes.append(state(c));c=int(prev[c])
 nodes.reverse();points=[(nodes[0][0],*pads[a]['xy'])]
 for i,(l,x,y)in enumerate(nodes):
  pt=reuse.get((x,y),xy(x,y))if i and nodes[i-1][0]!=l else xy(x,y)
  if i and nodes[i-1][0]!=l:points.append((nodes[i-1][0],*pt))
  points.append((l,*pt))
 points.append((nodes[-1][0],*pads[b]['xy']))
 compact=[]
 for q in points:
  if compact and q==compact[-1]:continue
  while len(compact)>=2 and q[0]==compact[-1][0]==compact[-2][0]:
   s,t=compact[-2],compact[-1];cross=(t[1]-s[1])*(q[2]-t[2])-(t[2]-s[2])*(q[1]-t[1]);dot=(t[1]-s[1])*(q[1]-t[1])+(t[2]-s[2])*(q[2]-t[2])
   if abs(cross)<1e-8 and dot>=0:compact.pop()
   else:break
  compact.append(q)
 start_count=len(tracks)
 for q,z in zip(compact,compact[1:]):
  if q[0]!=z[0]:
   if grid(q[1:])in reuse:continue
   tracks.append(dict(net=net,a=list(q[1:]),b=list(q[1:]),width=via_d,layers=[0,1,2,3],via=True,family=family,label=label))
  elif math.dist(q[1:],z[1:])>1e-7:tracks.append(dict(net=net,a=list(q[1:]),b=list(z[1:]),width=width,layers=[q[0]],via=False,family=family,label=label))
 return True,dict(label=label,a=a,b=b,net=net,family=family,width=width,objects=len(tracks)-start_count,length_mm=sum(math.dist(q['a'],q['b'])for q in tracks[start_count:]if not q['via']),visits=visits,elapsed_s=time.monotonic()-t0)
jobs=[
 ('R9.1','R6.1',.3,'Dedicated shunt Kelvin','kelvin',2,2),
 ('Q1.3','R9.1',.8,'Source power to shunt','power',0,None),
 ('Q1.3','R8.2',.3,'Source referenced pulldown','power',3,None),
 ('R9.2','C1.2',1.,'Shunt return to bulk capacitor','shunt',0,None),
 ('BR1.3','C1.2',.8,'Bridge charge return to bulk capacitor','charge',3,None),
 ('T1.1','C1.2',.5,'Auxiliary return to bulk capacitor','aux',1,None),
 ('C3.2','T1.1',.45,'Aux reservoir local return','aux',3,None),
 ('U1.5','C1.2',.35,'Quiet control return to bulk capacitor','quiet',2,None),
 ('C2.2','U1.5',.35,'Local controller bypass return','quiet',3,None),
 ('R5.2','U1.5',.3,'VS divider quiet return','quiet',0,None),
 ('RT1.2','U1.5',.3,'NTC quiet return','quiet',0,None),
 ('R13.2','U1.5',.3,'VDD bleed quiet return','quiet',0,None),
 ('R6.2','U1.4',.3,'Current sense input','CS',0,None),
 ('Q1.1','R7.2',.3,'Gate series resistor','gate',0,None),
 ('Q1.1','R8.1',.3,'Gate pulldown','gate',3,None),
 ('U1.3','R7.1',.3,'Controller gate drive','DRV',0,None),
 ('R4.2','R5.1',.3,'VS divider','VS',3,None),
 ('R5.1','U1.6',.3,'VS input','VS',0,None),
 ('RT1.1','U1.1',.3,'NTC input','NTC',0,None),
 ('R10.2','C3.1',.45,'Aux feed to reservoir','VDD',3,None),
 ('C3.1','U1.2',.35,'Controller bias feed','VDD',3,None),
 ('C2.1','U1.2',.4,'Local controller bypass feed','VDD',3,None),
 ('R13.1','U1.2',.3,'VDD bleed feed','VDD',0,None),
 ('R17.2','C3.1',.3,'Startup VDD feed','VDD',3,None),
 ('T1.2','D2.2',.4,'Auxiliary rectifier winding','AUX_RAW',0,None),
 ('T1.2','R4.1',.3,'Winding sense feed','AUX_RAW',3,None),
 ('D2.1','R10.1',.45,'Rectified auxiliary feed','AUX_RECT',0,None),
 ('R3.2','C1.2',.3,'Bleeder A return','bleedA',1,None),
 ('R15.2','C1.2',.3,'Bleeder B return','bleedB',3,None),
 ('T1.10','C4.2',.8,'Secondary reservoir return','OUTPUT_NEG',0,None),
 ('T1.10','J2.2',.8,'LED output return','OUTPUT_NEG',0,None),
 ('R12.2','T1.10',.3,'Output bleed return','OUTPUT_NEG',3,None),
 ('R11.2','T1.10',.3,'Second output bleed return','OUTPUT_NEG',3,None),
 ('T1.6','D3.2',.8,'Secondary rectifier winding','SECONDARY_RAW',3,None),
 ('D3.1','C4.1',.8,'Secondary reservoir feed','OUTPUT_POS',3,None),
 ('D3.1','J2.1',.8,'LED output feed','OUTPUT_POS',0,None),
 ('R11.1','C4.1',.3,'Output bleed feed','OUTPUT_POS',3,None),
 ('R12.1','C4.1',.3,'Second output bleed feed','OUTPUT_POS',3,None),
 ('T1.5','C1.1',.8,'Primary bulk power feed','BULK_POS',1,None),
 ('TVS1.2','T1.5',.65,'Clamp return to primary bulk','BULK_POS',3,None),
 ('BR1.1','C1.1',.8,'Bridge bulk charging feed','BULK_POS',3,None),
 ('R2.1','BR1.1',.3,'Bleeder A bulk feed','BULK_POS',3,None),
 ('R14.1','T1.5',.3,'Bleeder B bulk feed','BULK_POS',3,None),
 ('R16.1','T1.5',.3,'Startup bulk feed','BULK_POS',3,None),
 ('T1.3','Q1.2',.65,'Primary drain power connection','DRAIN',1,None),
 ('D1.2','T1.3',.65,'Short drain clamp pickup','DRAIN',3,None),
 ('D1.1','TVS1.1',.65,'Local diode TVS clamp','CLAMP',3,None),
 ('J1.2','BR1.2',.6,'Mains bridge input','AC_CAP_B',1,None),
 ('J1.1','F1.1',.6,'Mains fused input','AC_CAP_A',1,None),
 ('F1.2','R1.1',.6,'Fused inrush resistor feed','AC_FUSED',3,None),
 ('R1.2','BR1.4',.6,'Limited bridge input','AC_LIMITED',0,None),
 ('R2.2','R3.1',.3,'Bleeder A midpoint','BLEED_MID',2,None),
 ('R14.2','R15.1',.3,'Bleeder B midpoint','BLEED_MID_B',3,None),
 ('R16.2','R17.1',.3,'Startup series midpoint','STARTUP_MID',3,None),
]
priority={'Mains bridge input':0,'Mains fused input':1,'Primary drain power connection':2,'VS input':3}
jobs.sort(key=lambda q:priority.get(q[3],4))
for job in jobs:
 ok,r=route(*job);r['passed']=ok;results.append(r);print(('PASS'if ok else'FAIL'),r,flush=True)
 (D/'route-plan.json').write_text(json.dumps(dict(source_sha256=j['source_sha256'],grid_mm=step,via_diameter_mm=via_d,via_drill_mm=.3,retained_clearance_mm=dict(primary_HV_quiet=3.,primary_secondary_projected=10.7),critical_HV_projection=True,connections=results,elements=tracks,all_planned=all(q['passed']for q in results)),indent=2)+'\n')
 if not ok:break
