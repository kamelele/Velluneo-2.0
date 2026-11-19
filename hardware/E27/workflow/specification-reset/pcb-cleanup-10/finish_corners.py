"""Clearance-aware octilinear simplification of degree-two native copper chains."""
from pathlib import Path
import json,math,heapq,collections,hashlib
D=Path(__file__).resolve().parent;j=json.loads((D/'geometry-input.json').read_text());ts=j['tracks'];pads=j['pads'];EPS=1e-6
hv={'Net-(F1-Pad1)','Net-(BR1-AC-Pad2)','Net-(F1-Pad2)','Net-(BR1-AC-Pad4)','BULK_POS','DRAIN','Net-(D1-K)','STARTUP_MID'};quiet={'VDD','VS','NTC','CS','DRV','GATE','SENSE','PRIMARY_GND','AUX_RAW','Net-(D2-K)'};sec={'OUTPUT_POS','OUTPUT_NEG','SECONDARY_RAW','unconnected-(T1-Pad7)','unconnected-(T1-Pad8)','unconnected-(T1-Pad9)'}
def key(p):return tuple(round(x,6)for x in p)
def distpoint(p,a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];den=dx*dx+dy*dy;u=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(den or 1)));return math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy)
def cross(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def segdist(a,b,c,d):
 if cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0:return 0
 return min(distpoint(a,c,d),distpoint(b,c,d),distpoint(c,a,b),distpoint(d,a,b))
def lim(a,b):return 10 if(a in sec)!=(b in sec)else 3 if(a in hv and b in quiet)or(b in hv and a in quiet)else .25
def bbox(a,b,r=0):return(min(a[0],b[0])-r,min(a[1],b[1])-r,max(a[0],b[0])+r,max(a[1],b[1])+r)
def overlap(a,b):return a[0]<=b[2]and b[0]<=a[2]and a[1]<=b[3]and b[1]<=a[3]
def rectdist(a,b,q):
 if q[0]<=a[0]<=q[2]and q[1]<=a[1]<=q[3]or q[0]<=b[0]<=q[2]and q[1]<=b[1]<=q[3]:return 0
 corners=[(q[0],q[1]),(q[2],q[1]),(q[2],q[3]),(q[0],q[3])];return min(segdist(a,b,corners[i],corners[(i+1)%4])for i in range(4))
def pointpad(p,pad,r):
 q=pad['box'];return q[0]-r<=p[0]<=q[2]+r and q[1]-r<=p[1]<=q[3]+r
allnodes=collections.defaultdict(list)
for i,t in enumerate(ts):
 for p in({key(t['a']),key(t['b'])}):
  for l in t['layers']:allnodes[(t['net'],l,p)].append(i)
groups=collections.defaultdict(list)
for i,t in enumerate(ts):
 if not t['via']and t['net']not in{'SENSE','CS'}:groups[(t['net'],t['layers'][0],t['width'])].append(i)
chains=[]
for group,indices in groups.items():
 net,l,w=group;adj=collections.defaultdict(list)
 for i in indices:
  for p in(key(ts[i]['a']),key(ts[i]['b'])):adj[p].append(i)
 def anchor(p):
  return len(adj[p])!=2 or len(allnodes[(net,l,p)])!=2 or any(pad['net']==net and l in pad['layers']and pointpad(p,pad,w/2)for pad in pads)or any(t['via']and t['net']==net and math.dist(p,t['a'])<t['width']/2+w/2 for t in ts)
 used=set()
 for p in list(adj):
  if not anchor(p):continue
  for first in adj[p]:
   if first in used:continue
   es=[];pts=[p];cur=p;ix=first
   while ix not in used:
    used.add(ix);es.append(ix);t=ts[ix];end=key(t['b'])if key(t['a'])==cur else key(t['a']);pts.append(end)
    if anchor(end):break
    ix=next(i for i in adj[end]if i!=ix);cur=end
   if len(es)>1:chains.append(dict(group=group,indices=es,points=pts))
current=list(ts);changes=[];protected=[t for t in ts if t['net']in{'SENSE','CS'}]
def legalpath(points,chain):
 net,l,w=chain['group'];r=w/2;remove=set(chain['indices']);ends=[chain['points'][0],chain['points'][-1]]
 # Same-net contacts may only occur in existing endpoint/pad neighborhoods.
 anchors=[]
 for p in ends:
  radius=max([w+.005,*[math.hypot(q['size_mm'][0],q['size_mm'][1])/2+.005 for q in pads if q['net']==net and l in q['layers']and pointpad(p,q,w/2)]])
  anchors.append((p,radius))
 for a,b in zip(points,points[1:]):
  bb=bbox(a,b);bounds=j['outline_bbox_mm'];edge=.5+r
  if min(a[0],b[0])<bounds[0]+edge-1e-6 or max(a[0],b[0])>bounds[2]-edge+1e-6 or min(a[1],b[1])<bounds[1]+edge-1e-6 or max(a[1],b[1])>bounds[3]-edge+1e-6:return False
  for area in j['rectangular_rule_areas']:
   if l in area['layers']and rectdist(a,b,area['box'])<r+.005:return False
  for pad in pads:
   if pad['net']==net:continue
   if l not in pad['layers']and(net in sec)==(pad['net']in sec):continue
   gap=lim(net,pad['net'])+r+.003
   if not overlap(bbox(a,b,gap),pad['box']):continue
   d=distpoint(pad['xy'],a,b)-pad['size_mm'][0]/2 if pad.get('circle')else rectdist(a,b,pad['box'])
   if d<gap:return False
  for ix,t in enumerate(current):
   if t is None or ix in remove:continue
   same=t['net']==net
   if same and net=='DRAIN':continue
   if l not in t['layers']and(net in sec)==(t['net']in sec):continue
   gap=(0 if same else lim(net,t['net']))+r+t['width']/2+.003
   if not overlap(bbox(a,b,gap),bbox(t['a'],t['b'])):continue
   if segdist(a,b,t['a'],t['b'])>=gap:continue
   if same:
    # Exempt only contacts wholly inside the two existing pad/junction discs.
    count=max(1,math.ceil(math.dist(a,b)/.05))
    touches=[(a[0]+(b[0]-a[0])*k/count,a[1]+(b[1]-a[1])*k/count)for k in range(count+1)]
    if all(any(math.dist(p,c)<=rr for c,rr in anchors)for p in touches if distpoint(p,t['a'],t['b'])<gap):continue
   return False
  if net in hv:
   for t in protected:
    if l not in t['layers']and segdist(a,b,t['a'],t['b'])<3+r+t['width']/2+.003:return False
 return True
def candidates(a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];sx=1 if dx>=0 else-1;sy=1 if dy>=0 else-1
 if abs(dx)<EPS or abs(dy)<EPS or abs(abs(dx)-abs(dy))<EPS:return [[a,b]]
 if abs(dx)>abs(dy):mids=[(b[0]-sx*abs(dy),a[1]),(a[0]+sx*abs(dy),b[1])]
 else:mids=[(a[0],b[1]-sy*abs(dx)),(b[0],a[1]+sy*abs(dx))]
 return [[a,b]]+[[a,m,b]for m in mids]
for ci,ch in enumerate(sorted(chains,key=lambda c:len(c['indices']),reverse=True)):
 pts=ch['points'];N=len(pts);dp=[math.inf]*N;prev={};dp[0]=0
 for end in range(1,N):
  # Original edge always retained as fallback; all shortcuts are screened.
  choices=[(end-1,[pts[end-1],pts[end]],False)]
  for start in range(end-1):
   for path in candidates(pts[start],pts[end]):choices.append((start,path,True))
  for start,path,check in choices:
   cost=sum(math.dist(a,b)for a,b in zip(path,path[1:]))+.12*(len(path)-1)
   if dp[start]+cost>=dp[end]-1e-7:continue
   if check and not legalpath(path,ch):continue
   dp[end]=dp[start]+cost;prev[end]=(start,path)
 end=N-1;pieces=[]
 while end: start,path=prev[end];pieces.append(path);end=start
 out=[]
 for path in reversed(pieces):out.extend(path if not out else path[1:])
 compact=[]
 for p in out:
  if len(compact)>1 and abs(cross(compact[-2],compact[-1],p))<1e-7 and (p[0]-compact[-1][0])*(compact[-1][0]-compact[-2][0])+(p[1]-compact[-1][1])*(compact[-1][1]-compact[-2][1])>=0:compact.pop()
  compact.append(p)

 if ch['group'][0]in {'DRAIN','PRIMARY_GND','NTC'} and len(ch['indices'])>=8:
  original_length=sum(math.dist(a,b)for a,b in zip(pts,pts[1:]));best_score=sum(math.dist(a,b)for a,b in zip(compact,compact[1:]))+.3*(len(compact)-1)
  for mid in pts[1:-1]:
   for shift in (.2,.4,.8,1.2):
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
     q=(mid[0]+dx*shift,mid[1]+dy*shift)
     for pa in candidates(pts[0],q):
      for pb in candidates(q,pts[-1]):
       trial=pa+pb[1:];length=sum(math.dist(a,b)for a,b in zip(trial,trial[1:]));score=length+.3*(len(trial)-1)
       if score>=best_score or length>original_length+min(.8,.04*original_length):continue
       if legalpath(trial,ch):compact=trial;best_score=score
 oldlen=sum(math.dist(a,b)for a,b in zip(pts,pts[1:]));newlen=sum(math.dist(a,b)for a,b in zip(compact,compact[1:]))
 if len(compact)-1<len(ch['indices'])and newlen<=oldlen+min(.8,.04*oldlen)+.002:
  for ix in ch['indices']:current[ix]=None
  net,l,w=ch['group'];elements=[dict(net=net,layers=[l],width=w,a=list(a),b=list(b),via=False)for a,b in zip(compact,compact[1:])];current.extend(elements)
  changes.append(dict(net=net,layer=l,width=w,removed_indices=ch['indices'],old_segments=len(ch['indices']),new_segments=len(elements),old_length_mm=oldlen,new_length_mm=newlen,new_elements=elements))
  print(ci,net,len(ch['indices']),'->',len(elements),flush=True)
plan=dict(source_board_sha256=j['source_sha256'],changes=changes,protected_nets=['SENSE','CS'],same_net_contact_guard=True,minimum_clearances_preserved=True,old_segments=sum(not t['via']for t in ts),new_segments=sum(t is not None and not t['via']for t in current),old_length_mm=sum(math.dist(t['a'],t['b'])for t in ts if not t['via']),new_length_mm=sum(math.dist(t['a'],t['b'])for t in current if t is not None and not t['via']),scope='Clearance-aware degree-two chain shortcut plan, original endpoints/widths/layers/vias retained. Native DRC/topology/sensing checks remain required; no operating validation inferred.')
(D/'smoothing-plan.json').write_text(json.dumps(plan,indent=2)+'\n');print('PLAN',plan['old_segments'],'->',plan['new_segments'],flush=True)
