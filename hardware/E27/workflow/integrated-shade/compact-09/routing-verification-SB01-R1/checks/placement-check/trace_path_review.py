from pathlib import Path
import json,hashlib,heapq,math
import pcbnew as k
H=Path(__file__).resolve().parent;src=H.parent/'baseline/SC09_compact.kicad_pcb';before=hashlib.sha256(src.read_bytes()).hexdigest();b=k.LoadBoard(str(src));fp={f.GetReference():f for f in b.GetFootprints()};pads={(f.GetReference(),p.GetNumber()):p for f in fp.values()for p in f.Pads()};graph={};segments={}
node=lambda ly,p:(int(ly),p.x,p.y)
def edge(a,z,length,uuid):graph.setdefault(a,[]).append((z,length,uuid));graph.setdefault(z,[]).append((a,length,uuid))
node_nets={}
for t in b.GetTracks():
 uid=t.m_Uuid.AsString()
 if isinstance(t,k.PCB_VIA):
  p=t.GetPosition();edge(node(k.F_Cu,p),node(k.B_Cu,p),0,uid)
  for ly in [k.F_Cu,k.B_Cu]:node_nets[node(ly,p)]=t.GetNetname()
 else:
  a,z=node(t.GetLayer(),t.GetStart()),node(t.GetLayer(),t.GetEnd());edge(a,z,math.hypot(z[1]-a[1],z[2]-a[2])/1e6,uid);segments[uid]={'net':t.GetNetname(),'face':t.GetLayerName(),'width_mm':k.ToMM(t.GetWidth()),'a_mm':[a[1]/1e6,a[2]/1e6],'z_mm':[z[1]/1e6,z[2]/1e6]};node_nets[a]=t.GetNetname();node_nets[z]=t.GetNetname()
for p in pads.values():
 for ly in [k.F_Cu,k.B_Cu]:
  if not p.IsOnLayer(ly):continue
  center=node(ly,p.GetPosition())
  for n in list(graph):
   if n==center or n[0]!=int(ly)or node_nets.get(n)!=p.GetNetname():continue
   if p.HitTest(k.VECTOR2I(n[1],n[2]),0):edge(center,n,math.hypot(center[1]-n[1],center[2]-n[2])/1e6,'pad-contact')
def path(ref1,pin1,ref2,pin2):
 p1,p2=pads[ref1,pin1],pads[ref2,pin2];assert p1.GetNetname()==p2.GetNetname();starts=[node(ly,p1.GetPosition())for ly in [k.F_Cu,k.B_Cu]if p1.IsOnLayer(ly)];targets={node(ly,p2.GetPosition())for ly in [k.F_Cu,k.B_Cu]if p2.IsOnLayer(ly)};heap=[(0,a,[])for a in starts];best={}
 while heap:
  cost,n,ids=heapq.heappop(heap)
  if n in best:continue
  best[n]=cost
  if n in targets:return{'from':ref1+'.'+pin1,'to':ref2+'.'+pin2,'net':p1.GetNetname(),'centerline_path_mm':cost,'UUIDs':ids,'segments':[dict(uuid=uid,**segments[uid])for uid in ids if uid in segments]}
  for z,l,uid in graph.get(n,[]):
   if z not in best:heapq.heappush(heap,(cost+l,z,ids+[uid]))
 return{'from':ref1+'.'+pin1,'to':ref2+'.'+pin2,'error':'No endpoint graph path; endpoint-only graph does not infer mid-segment or pad-overlap joins.'}
paths=[path(*args)for args in [('C5','1','U1','1'),('C5','2','U1','5'),('C5','2','U1','8'),('U1','3','R5','2'),('R5','2','T1','2'),('C4','2','D1','2')]]
def hit(a,z,box):
 lo,hi=0.,1.
 for j in [0,1]:
  d=z[j]-a[j]
  if abs(d)<1e-12:
   if a[j]<box[j]or a[j]>box[j+2]:return False
  else:
   u,v=sorted([(box[j]-a[j])/d,(box[j+2]-a[j])/d]);lo=max(lo,u);hi=min(hi,v)
   if lo>hi:return False
 return True
box=[114.25,115.75,126.75,128.25];hits=[]
for p in paths:
 if p.get('from')not in ['U1.3','C5.1','C5.2']:continue
 for s in p.get('segments',[]):
  w=s['width_mm']/2;wide=[box[0]-w,box[1]-w,box[2]+w,box[3]+w]
  if hit(s['a_mm'],s['z_mm'],wide):hits.append({'path':p['from']+'->'+p['to'],'segment':s})
r={'actor':'/root/sb01_refine_placement_check','board_sha256':before,'source_unchanged':hashlib.sha256(src.read_bytes()).hexdigest()==before,'paths':paths,'critical_BP_SOURCE_sense_paths_under_T1_max_body':hits,'T1_max_body_mm':box,'limits':['Path length is an endpoint graph proxy, not inductance or field/coupling simulation.','The R5.2/T1.2 path is power-force routing on FB_INDUCTOR; do not label every trace on that net a sensitive signal.','Only quiet/current-sense and bypass paths are compared to the Wuerth no-sensitive-traces guidance; body-box intersection is a conservative geometry screen.']};(H/'baseline-paths.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'paths':[{k:p.get(k)for k in ['from','to','centerline_path_mm','error']}for p in paths],'sensitive_body_intersections':len(hits),'source_unchanged':r['source_unchanged']}))
