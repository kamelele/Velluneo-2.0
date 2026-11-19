"""Strict shape-aware completion of the saved imported candidate; no protected-net rerouting."""
from pathlib import Path
import json,math
D=Path(__file__).resolve().parent;INPUT_FILE='tail-input.json'
exec(compile((D/'plan_routes.py').read_text().split('groups=')[0],str(D/'plan_routes.py'),'exec'))
NEGOTIATED=False;groups=[set(g)for g in j['connected_pad_groups']];rows=[]
def group(k):return next(g for g in groups if k in g)
def connect(a,b):
 for width in([.8,.6,.4,.3]if pads[a]['net']in{'DRAIN','BULK_POS','OUTPUT_POS','OUTPUT_NEG','SECONDARY_RAW','CLAMP'}else[.4,.3]):
  es,reason=plan(a,b,width,'tail_distribution')
  if es is not None:
   new.extend(es);ga,gb=group(a),group(b);ga.update(gb);groups.remove(gb);rows.append(dict(a=a,b=b,width_mm=width,elements=es));print('TAIL ADDED',a,b,width,flush=True);return True
 return False
for sweep in range(2):
 for net in sorted({p['net']for p in pads.values()}):
  if net in{'PRIMARY_GND','SENSE','CS'}:continue
  ng=[g for g in groups if pads[next(iter(g))]['net']==net]
  while len(ng)>1:
   pairs=sorted((math.dist(pads[a]['xy'],pads[b]['xy']),a,b)for i,g in enumerate(ng)for h in ng[i+1:]for a in g for b in h)
   if not any(connect(a,b)for _,a,b in pairs[:12]):break
   ng=[g for g in groups if pads[next(iter(g))]['net']==net]
remaining=[sorted(g)for g in groups];deficit=len(remaining)-27
(D/'tail-plan.json').write_text(json.dumps(dict(input_source_sha256=j['source_sha256'],new_elements=new,branches=rows,remaining_groups=remaining,remaining_group_deficit=deficit,scope='Strict two-layer shape-aware grid additions; protectedGND/SENSE/CS untouched. Native checks required.'),indent=2)+'\n');print('TAIL DEFICIT',deficit,flush=True)
