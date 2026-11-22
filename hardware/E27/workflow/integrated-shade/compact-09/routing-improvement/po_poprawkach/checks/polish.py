"""Guarded line-of-sight simplification of unprotected generic routing only."""
from pathlib import Path
import json,sys,math,re,hashlib,collections
import pcbnew as k
H=Path(__file__).resolve().parent;ROOT=H.parents[1];S=ROOT/'work/Velluneo-2.0/.work/routing-vertical'
sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
src=S/'SC09_compact.kicad_pcb';before=src.read_bytes();b=c.q.load_native(src)
co=c.Checker(b,c.Contract(S,H/'spacing-matrix.CAT01.json',H/'vertical/package-assessment.CAT01.json'));co.collect()
contract=json.loads((S/'.electronics-rules/routing-input.json').read_text());assert contract['constraints']['minimums_mm']['clearance']==.3
seed=json.loads((H/'vertical/seed-authoring.json').read_text());protected={r['uuid']for r in seed['routes']}
tracks={t.m_Uuid.AsString():t for t in b.GetTracks()if not isinstance(t,k.PCB_VIA)}
obj={o.id:o for o in co.objects if o.kind=='track'}
def xy(p):return(p.x,p.y)
def key(t,p):return(t.GetNetname(),t.GetLayer(),t.GetWidth(),xy(p))
links=collections.defaultdict(list)
for uid,t in tracks.items():
 if uid in protected:continue
 links[key(t,t.GetStart())].append(uid);links[key(t,t.GetEnd())].append(uid)
# Preserve endpoints touched by pads/vias/protected routes, and generic branch
# contacts that do not coincide with both exact centreline endpoints.
blocked=set()
for uid,t in tracks.items():
 if uid in protected:continue
 o=obj[uid]
 for p in [t.GetStart(),t.GetEnd()]:
  for a in co.objects:
   if a.id==uid or a.layer!=o.layer or a.net!=o.net:continue
   if a.kind=='track' and a.id not in protected:
    # Generic routes can contain adjacent .1mm stair steps whose rounded
    # envelopes overlap. Those are not distinct protected receiver branches.
    # Native connectivity is rechecked on the complete proposed result.
    continue
   if a.shape.Contains(p):blocked.add(key(t,p));break
seen=set();chains=[]
for uid,t in tracks.items():
 if uid in protected or uid in seen:continue
 ends=[key(t,t.GetStart()),key(t,t.GetEnd())]
 start=next((p for p in ends if len(links[p])!=2 or p in blocked),ends[0]);ids=[];points=[start[3]];current=uid;node=start
 while current not in seen:
  seen.add(current);ids.append(current);tr=tracks[current];a,d=xy(tr.GetStart()),xy(tr.GetEnd());end=d if node[3]==a else a;points.append(end);node=(node[0],node[1],node[2],end)
  if len(links[node])!=2 or node in blocked:break
  nxt=next(q for q in links[node]if q!=current)
  if nxt in seen:break
  current=nxt
 if len(ids)>1:chains.append((ids,points))
safe=c.q.rectangle([100.5,100.5,149.5,131.5]);areas=[c.q.rectangle(a['rectangle_mm'])for a in contract['constraints']['areas']]
obstacles=list(co.objects);removed=set();added=[];log=[]
def propose(t,a,d):
 n=k.PCB_TRACK(b);n.SetNet(t.GetNet());n.SetLayer(t.GetLayer());n.SetWidth(t.GetWidth());n.SetStart(k.VECTOR2I(*a));n.SetEnd(k.VECTOR2I(*d));return n
def valid(t):
 layer=b.GetLayerName(t.GetLayer());shape=co.native_poly(t,layer);net=t.GetNetname().lstrip('/')
 if not c.q.clipped(shape,safe,False).IsEmpty() or any(not c.q.clipped(shape,a).IsEmpty()for a in areas):return None
 for o in obstacles:
  if o.layer!=layer or o.net==net:continue
  gap=max(.3,co.c.gap(net,o.net))
  if c.q.close(shape,o.shape,gap):return None
 return c.q.Copper(t.m_Uuid.AsString(),'track',net,t.GetNetname(),layer,shape,source=t)
for ids,points in chains:
 t=tracks[ids[0]];i=0;replacement=[];newobjects=[]
 while i<len(points)-1:
  chosen=None
  for j in range(len(points)-1,i+1,-1):
   n=propose(t,points[i],points[j]);o=valid(n)
   if o is not None:chosen=(j,n,o);break
  if chosen:
   j,n,o=chosen;replacement.append(n);newobjects.append(o);i=j
  else:
   # Keep the actual original edge when no full-matrix shortcut qualifies.
   replacement.append(tracks[ids[i]]);i+=1
 if len(replacement)>=len(ids):continue
 # Retain unchanged edge UUIDs; only deleted native blocks are removed from raw.
 keep={n.m_Uuid.AsString()for n in replacement if n.m_Uuid.AsString()in tracks};removed.update(set(ids)-keep)
 for n in replacement:
  if n.m_Uuid.AsString()not in tracks:added.append(n)
 obstacles.extend(newobjects)
 log.append({'net':t.GetNetname(),'old_segments':len(ids),'new_segments':len(replacement),'old_UUIDs':ids,'new_UUIDs':[n.m_Uuid.AsString()for n in replacement]})
raw=before.decode().replace('\r\n','\n');count=0
def delete(m):
 global count
 if any('"'+uid+'"'in m.group()for uid in removed):count+=1;return ''
 return m.group()
raw=re.sub(r'\n\t\(segment\n.*?\n\t\)',delete,raw,flags=re.S);assert count==len(removed)
tmp=H/'polished.kicad_pcb';tmp.write_text(raw);new=c.q.load_native(tmp)
idmap={}
for t in added:
 n=k.PCB_TRACK(new);n.SetNet(new.FindNet(t.GetNetname()));n.SetLayer(t.GetLayer());n.SetWidth(t.GetWidth());n.SetStart(t.GetStart());n.SetEnd(t.GetEnd());new.Add(n);idmap[t.m_Uuid.AsString()]=n.m_Uuid.AsString()
for row in log:row['new_UUIDs']=[idmap.get(uid,uid)for uid in row['new_UUIDs']]
assert k.SaveBoard(str(tmp),new,True)
assert c.q.raw_track_nets(tmp)=={t.m_Uuid.AsString():t.GetNetname()for t in c.q.load_native(tmp).GetTracks()}
(H/'pre-polish.kicad_pcb').write_bytes(before)
(H/'polish-proof.json').write_text(json.dumps({'actual_actor':'/root','source_sha256':hashlib.sha256(before).hexdigest(),'result_sha256':hashlib.sha256(tmp.read_bytes()).hexdigest(),'constraints_digest_supplied':contract['constraints_digest'],'protected_seed_UUIDs_preserved':not bool(protected&removed),'removed':len(removed),'added':len(added),'chains':log,'method':'Generic degree2 chains only; full unchanged matrix plus all old and previously accepted new other-net copper, saved both-face areas and0.5mmedge guard. Native DRC/connectivity and full independent screen still required. No package exception used to qualify new shortcuts.'},indent=2)+'\n')
print(json.dumps({'chains_simplified':len(log),'removed':len(removed),'added':len(added),'protected_preserved':not bool(protected&removed)}))
