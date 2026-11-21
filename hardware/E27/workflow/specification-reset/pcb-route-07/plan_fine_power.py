"""Bounded full-outline fine-grid test of remaining power distribution."""
from pathlib import Path
import json,math
D=Path(__file__).resolve().parent
INPUT_FILE='current-input.json';GRID_STEP=.1
exec(compile((D/'plan_routes.py').read_text().split('groups=')[0],str(D/'plan_routes.py'),'exec'))
rows=[]
for a,b in [('T1.5','Q1.2'),('Q1.2','D1.2'),('C1.1','T1.1'),('T1.1','R16.1'),('C1.1','BR1.1')]:
 es,reason=plan(a,b,.3,'fine_power')
 if es is not None:new.extend(es)
 rows.append(dict(a=a,b=b,success=es is not None,reason=reason,length_mm=None if es is None else sum(math.dist(e['a'],e['b'])for e in es)))
 print(rows[-1],flush=True)
(D/'fine-power-plan.json').write_text(json.dumps(dict(input_source_sha256=j['source_sha256'],grid_mm=GRID_STEP,new_elements=new,attempts=rows),indent=2)+'\n')
