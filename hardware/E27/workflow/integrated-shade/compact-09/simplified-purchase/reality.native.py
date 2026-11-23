"""Read-only independent native checks for magnetic/sense layout and pin intent."""
from pathlib import Path
import sys,json,hashlib,collections,math
import pcbnew as k
p=Path(sys.argv[1]);before=hashlib.sha256(p.read_bytes()).hexdigest();b=k.LoadBoard(str(p));fs={f.GetReference():f for f in b.GetFootprints()}
mm=lambda n:k.ToMM(n)
pad=lambda r,n:next(x for x in fs[r].Pads()if x.GetNumber()==n)
t1=fs['T1'];cx,cy=mm(t1.GetPosition().x),mm(t1.GetPosition().y)
rect=(cx-6.25,cy-6.25,cx+6.25,cy+6.25)
def intersects(a,z,margin=0.):
 x0,y0,x1,y1=rect;x0-=margin;y0-=margin;x1+=margin;y1+=margin
 dx=z[0]-a[0];dy=z[1]-a[1];lo=0.;hi=1.
 for pp,qq in [(-dx,a[0]-x0),(dx,x1-a[0]),(-dy,a[1]-y0),(dy,y1-a[1])]:
  if abs(pp)<1e-15:
   if qq<0:return False
  elif pp<0:lo=max(lo,qq/pp)
  else:hi=min(hi,qq/pp)
 return lo<=hi
pos=lambda a:(mm(a.x),mm(a.y))
raw=[];g=collections.defaultdict(list);edgeinfo={}
def link(a,z,detail):
 g[a].append(z);g[z].append(a);edgeinfo[(a,z)]=edgeinfo[(z,a)]=detail
def node(layer,pt):return(layer,pt.x,pt.y)
for t in b.GetTracks():
 if t.GetNetname()in['/BP','/M']:
  if intersects(pos(t.GetStart()),pos(t.GetEnd()),mm(t.GetWidth())/2):raw.append({'net':t.GetNetname(),'uuid':t.m_Uuid.AsString(),'description':'BP/M copper overlaps projected maximum T1 body'})
 if t.GetNetname()!='/FB_INDUCTOR':continue
 detail={'uuid':t.m_Uuid.AsString(),'kind':'via'if isinstance(t,k.PCB_VIA)else'track','net':t.GetNetname()}
 if isinstance(t,k.PCB_VIA):link(node(k.F_Cu,t.GetPosition()),node(k.B_Cu,t.GetPosition()),detail)
 else:link(node(t.GetLayer(),t.GetStart()),node(t.GetLayer(),t.GetEnd()),detail)
points=list(g)
for f in b.GetFootprints():
 for pa in f.Pads():
  if pa.GetNetname()!='/FB_INDUCTOR':continue
  hub=('pad',f.GetReference(),pa.GetNumber())
  for n in points:
   if pa.IsOnLayer(n[0]) and pa.HitTest(k.VECTOR2I(n[1],n[2])):link(hub,n,{'kind':'pad','ref':f.GetReference(),'number':pa.GetNumber()})
start=('pad','U1','3');goal=('pad','R5','2');q=collections.deque([start]);prev={start:None}
while q:
 n=q.popleft()
 if n==goal:break
 for z in g[n]:
  if z not in prev:prev[z]=n;q.append(z)
path=[]
if goal in prev:
 n=goal
 while n is not None:path.append(n);n=prev[n]
 path.reverse()
hits=[];details=[]
for a,z in zip(path,path[1:]):
 d=edgeinfo[(a,z)];details.append(d)
 if d['kind']=='track' and isinstance(a[0],int) and isinstance(z[0],int):
  if intersects((mm(a[1]),mm(a[2])),(mm(z[1]),mm(z[2]))):hits.append(d)
expected={'T1.1':'/LED_PLUS','T1.2':'/FB_INDUCTOR','C1.1':'/BUS_RECT','C1.2':'/DC_RETURN','RV1.1':'/AC_FUSED','RV1.2':'/AC_N','RF1.1':'/AC_L','RF1.2':'/AC_FUSED','R6.1':'/SW_SOURCE','R6.2':'/FB_INDUCTOR','D1.1':'/FB_INDUCTOR','D1.2':'/DC_RETURN'}
actual={n:pad(*n.split('.')).GetNetname()for n in expected}
out={'reviewer':'/root/simple_reality_review','board':str(p),'board_sha256':before,'read_only_sha256_unchanged':before==hashlib.sha256(p.read_bytes()).hexdigest(),'pin_intent_expected_from_retained_functional_contract':expected,'actual_native_pin_nets':actual,'pin_intent_matches':expected==actual,'T1_projected_max_body_rectangle_mm':rect,'BP_M_under_body_hits':raw,'U1_FB_to_R5_kelvin_path_found':bool(path),'U1_FB_to_R5_path_edges':details,'U1_FB_sense_branch_under_body_hits':hits,'scope_note':'Native shortest connected path from U1.3 sense pin to R5.2 force junction is inspected independently; force-carrying same-net routes ending at T1.2 are not misclassified as low-current sensitive traces. This is geometry/topology evidence, not EMC, impedance or measured feedback performance.'}
(Path(__file__).parent/'reality.native.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({q:out[q]for q in ['board_sha256','read_only_sha256_unchanged','pin_intent_matches','BP_M_under_body_hits','U1_FB_to_R5_kelvin_path_found','U1_FB_sense_branch_under_body_hits']}))
