"""Finer full-outline VDD completion in unadopted four-layer comparison."""
from pathlib import Path
import json,math
D=Path(__file__).resolve().parent;prior=json.loads((D/'four-layer-plan.json').read_text());GRID_STEP=.1
exec(compile((D/'probe_four_layer.py').read_text().split('retained_fine=')[0],str(D/'probe_four_layer.py'),'exec'))
new.extend(prior['new_elements'])
for a,b,label in [('R10.2','C2.1','main_VDD'),('R17.2','R10.2','startup_VDD'),('T1.2','C1.2','aux_ground')]:
 if any(r.get('label')==label and r['success']for r in prior['attempts']):continue
 es,reason=plan(a,b,.3,label)
 if es is not None:
  new.extend(es);prior['new_elements'].extend(es);prior['attempts']=[r for r in prior['attempts']if r.get('label')!=label];prior['attempts'].append(dict(a=a,b=b,label=label,width_mm=.3,grid_mm=.1,success=True,reason=None,length_mm=sum(math.dist(e['a'],e['b'])for e in es)))
 print('4L DISTRIBUTION',label,reason,None if es is None else len(es),flush=True)
(D/'four-layer-plan.json').write_text(json.dumps(prior,indent=2)+'\n')
