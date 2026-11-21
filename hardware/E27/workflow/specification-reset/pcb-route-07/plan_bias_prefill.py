"""Preserve validated control paths, localize the rectifier damping resistor and reservoir loop."""
from pathlib import Path
import json,math,hashlib
D=Path(__file__).resolve().parent;retained_path=D/'retained-bias-control.json'
if not retained_path.exists():
 previous=(D/'ground-plan.json').read_bytes();old=json.loads(previous);keep={k:v for k,v in old['active_routes'].items()if old['tasks'][int(k)]['label']!='AUX_RECT_reserved'}
 retained_path.write_text(json.dumps(dict(previous_plan_sha256=hashlib.sha256(previous).hexdigest(),previous_seed_sha256=old['input_source_sha256'],tasks=old['tasks'],active_routes=keep,scope='Exact protected geometry replay; changed R10 layout needs fresh native validation.'),indent=2)+'\n')
retained=json.loads(retained_path.read_text());exec(compile((D/'plan_routes.py').read_text().split('groups=')[0],str(D/'plan_routes.py'),'exec'));NEGOTIATED=False
branches={int(k):v for k,v in retained['active_routes'].items()};rows=list(retained['tasks']);new=[e for es in branches.values()for e in es]
for a,b,label,widths in[('D2.1','R10.1','AUX_RECT_reserved',[.8,.6,.4,.3]),('R10.2','C3.1','bias_reservoir_VDD',[.4,.3])]:
 for width in widths:
  es,reason=plan(a,b,width,label)
  if es is not None:break
 assert es is not None,(a,b,reason)
 i=next((i for i,r in enumerate(rows)if r['label']==label),len(rows));row=dict(a=a,b=b,label=label,width=width,planar_length_mm=sum(math.dist(e['a'],e['b'])for e in es),vias=sum(e['via']for e in es))
 if i<len(rows):rows[i]=row
 else:rows.append(row)
 branches[i]=es;new.extend(es);print(label,width,row['planar_length_mm'],flush=True)
(D/'ground-plan.json').write_text(json.dumps(dict(input_source_sha256=j['source_sha256'],retained_path_input_sha256=hashlib.sha256(retained_path.read_bytes()).hexdigest(),new_elements=new,active_routes=branches,tasks=rows,scope='Protected return/control/local-power candidate; native geometry/current/EMI/process checks still required.'),indent=2)+'\n')
