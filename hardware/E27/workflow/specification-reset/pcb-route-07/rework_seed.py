"""Remove exactly two prior branches that fence the bulk-feed route."""
from pathlib import Path
import pcbnew,json,hashlib
D=Path(__file__).resolve().parent;S=D/'studies/sense';src=S/'Velluneo_sense_exploration.kicad_pcb';out=S/'routing-seed.kicad_pcb'
b=pcbnew.LoadBoard(str(src));j=json.loads((S/'C06-study-result.json').read_text());selectors=[]
def key(a,z):return tuple(sorted(tuple(round(float(v),5)for v in p)for p in(a,z)))
for r in j['routes']:
 if r.get('routed')and r['label']not in('short_shunt_bulk_return','local_CS_RLC','dedicated_SENSE_branch'):
  assert r['routed'];selectors.extend((r['label'],key(a,z))for a,z in zip(r['points_relative_mm'],r['points_relative_mm'][1:]))
removed=[]
for t in list(b.GetTracks()):
 if isinstance(t,pcbnew.PCB_VIA):
  removed.append(dict(label='orphan_transition_after_branch_ripup',net=t.GetNetname(),points_mm=[[pcbnew.ToMM(t.GetPosition().x)-100,pcbnew.ToMM(t.GetPosition().y)-100]]));b.Remove(t);continue
 k=key(*[[pcbnew.ToMM(p.x)-100,pcbnew.ToMM(p.y)-100]for p in(t.GetStart(),t.GetEnd())])
 for label,kk in selectors:
  if k==kk:
   removed.append(dict(label=label,net=t.GetNetname(),points_mm=k));b.Remove(t);break
assert len(removed)>=13,len(removed)
pcbnew.SaveBoard(str(out),b)
(D/'seed-rework.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),reduced_seed_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),removed=removed,scope='Exploratory ripup only. Rebuild native connectivity before planning; prior C06 remains immutable.'),indent=2)+'\n')
print('removed',len(removed))
