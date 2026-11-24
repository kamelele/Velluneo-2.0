"""Read-only independent inspection of restored SB01; no native save or approval."""
from pathlib import Path
import json,hashlib,math,sys,heapq
import pcbnew as k
H=Path(__file__).resolve().parent;P=H.parent/'baseline';pcb=P/'SC09_compact.kicad_pcb'
ROOT=H.parents[2];sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(pcb);b=c.q.load_native(pcb);b.BuildConnectivity();xy=lambda p:[k.ToMM(p.x),k.ToMM(p.y)]
fs={f.GetReference():f for f in b.GetFootprints()};pads={(r,p.GetNumber()):p for r,f in fs.items()for p in f.Pads()}
tracks={t.m_Uuid.AsString():t for t in b.GetTracks()}
obj={}
for (r,n),p in pads.items():obj[r+'.'+n]={'kind':'pad','position_mm':xy(p.GetPosition()),'size_mm':xy(p.GetSize()),'angle_deg':p.GetOrientationDegrees(),'net':p.GetNetname(),'layers':[k.LayerName(ly)for ly in [k.F_Cu,k.B_Cu]if p.IsOnLayer(ly)]}
for uid,t in tracks.items():
 via=isinstance(t,k.PCB_VIA);obj[uid]={'kind':'via'if via else'track','start_mm':xy(t.GetStart()),'end_mm':xy(t.GetEnd()),'width_mm':k.ToMM(t.GetWidth(k.F_Cu)if via else t.GetWidth()),'net':t.GetNetname(),'layer':t.GetLayerName()}
old=json.loads((ROOT/'work/sc09-order-audit/strict-spacing-fresh.json').read_text());rows=[]
for i,f in enumerate(old['findings'],1):
 a,z=obj[f['a']],obj[f['b']];intrinsic=f['kinds']==['pad','pad']
 rows.append({'number':i,**f,'classification':'intrinsic_exact_package_land_pair'if intrinsic else'local_escape_observation_adjacent_to_intrinsic_package_constraint','objects':[a,z],'routing_disposition':'Cannot reach existing2mm generic target by rigid placement/routing while keeping these exact manufacturer lands.'if intrinsic else'May improve exit geometry or number of duplicate observations; starting copper still shares the intrinsic terminal neighbourhood. Do not claim complete2mm closure from a reduced count.'})
part=[]
for r,f in sorted(fs.items()):
 field=f.GetField('MPN');part.append({'ref':r,'value':f.GetValue(),'actual_MPN_property':field.GetText()if field else None,'origin_mm':xy(f.GetPosition()),'angle_deg':f.GetOrientationDegrees(),'side':'B'if f.IsFlipped()else'F','attributes':f.GetAttributes(),'models':[m.m_Filename for m in f.Models()]})
graph={};meta={}
def node(layer,p):return(layer,int(p.x),int(p.y))
def add(a,z,w,d):graph.setdefault(a,[]).append((z,w));graph.setdefault(z,[]).append((a,w));meta[(a,z)]=meta[(z,a)]=d
for uid,t in tracks.items():
 if isinstance(t,k.PCB_VIA):add(node(k.F_Cu,t.GetPosition()),node(k.B_Cu,t.GetPosition()),0,uid)
 else:add(node(t.GetLayer(),t.GetStart()),node(t.GetLayer(),t.GetEnd()),math.dist(xy(t.GetStart()),xy(t.GetEnd())),uid)
points=list(graph)
for (r,n),p in pads.items():
 hub=('pad',r,n)
 for a in points:
  if p.IsOnLayer(a[0])and p.HitTest(k.VECTOR2I(a[1],a[2])):
   # Only links having the same physical pad net may join the hub.
   same=any(tracks[u].GetNetCode()==p.GetNetCode()for (x,z),u in meta.items()if x==a)
   if same:add(hub,a,0,r+'.'+n)
def path(left,right):
 start=('pad',*left.split('.'));goal=('pad',*right.split('.'));dist={start:0};prev={};queue=[(0,str(start),start)]
 while queue:
  d,_,a=heapq.heappop(queue)
  if d!=dist[a]:continue
  if a==goal:break
  for z,w in graph.get(a,[]):
   if d+w<dist.get(z,float('inf')):dist[z]=d+w;prev[z]=a;heapq.heappush(queue,(d+w,str(z),z))
 if goal not in dist:return {'from':left,'to':right,'found':False}
 ns=[goal]
 while ns[-1]!=start:ns.append(prev[ns[-1]])
 ns.reverse();edges=[meta[(a,z)]for a,z in zip(ns,ns[1:])];return {'from':left,'to':right,'found':True,'centreline_length_proxy_mm':dist[goal],'object_ids':edges}
paths=[path(a,z)for a,z in [('C5.1','U1.1'),('C5.2','U1.5'),('C5.2','U1.6'),('C5.2','U1.7'),('C5.2','U1.8'),('U1.3','R5.2'),('C4.1','U1.4'),('C4.2','D1.2'),('R5.2','D1.1'),('U1.5','R5.1'),('R5.2','T1.2')]]
contract=c.Contract(P,ROOT/'work/routing-improvement/spacing-matrix.CAT01.json',None);cc=c.Checker(b,contract);cc.collect()
result={'actor':'/root/sb01_refine_diagnostic','board_sha256':before,'source_unchanged':before==sha(pcb),'native_unconnected':b.GetConnectivity().GetUnconnectedCount(False),'parts':part,'findings_23':rows,'classification_counts':{'intrinsic_pad_pairs':sum(r['kinds']==['pad','pad']for r in rows),'local_escape_observations':sum(r['kinds']!=['pad','pad']for r in rows)},'paths':paths,'scope':'Independent native part/geometry/path inspection only. Endpoint path lengths omit pad-internal lengths and have zero via transition proxy; not loop inductance, thermal, EMC, normative insulation or powered qualification.'}
(H/'baseline-diagnostic.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({n:result[n]for n in ['board_sha256','source_unchanged','native_unconnected','classification_counts','paths']}))
