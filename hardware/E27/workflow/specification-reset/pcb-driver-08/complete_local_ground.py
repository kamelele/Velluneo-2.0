"""Complete the local C2/U1 return against the already planned selected copper."""
from pathlib import Path
import json,math
D=Path(__file__).resolve().parent;prior=json.loads((D/'selected-route-plan.json').read_text())
exec(compile((D/'routing_geometry.py').read_text(),str(D/'routing_geometry.py'),'exec'));new.extend(prior['new_elements'])
es,reason=plan('C2.2','U1.5',.4,'local_ground');assert es is not None,reason
prior['new_elements'].extend(es);prior['attempts'].append(dict(a='C2.2',b='U1.5',label='local_ground',width_mm=.4,success=True,reason=None,planar_length_mm=sum(math.dist(e['a'],e['b'])for e in es),vias=sum(e['via']for e in es)))
groups=[set(g)for g in prior['remaining_groups']];a=next(g for g in groups if 'C2.2'in g);b=next(g for g in groups if 'U1.5'in g)
if a is not b:a.update(b);groups.remove(b)
prior['remaining_groups']=[sorted(g)for g in groups];(D/'selected-route-plan.json').write_text(json.dumps(prior,indent=2)+'\n');print('Localground',prior['attempts'][-1],'groups',len(groups),flush=True)
