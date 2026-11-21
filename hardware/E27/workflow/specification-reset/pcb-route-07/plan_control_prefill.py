"""Replay exact reviewed return geometry, then jointly reserve controls and two bulk branches."""
from pathlib import Path
import json,math,hashlib
D=Path(__file__).resolve().parent
retained_path=D/'retained-control-returns.json'
if not retained_path.exists():
 previous=(D/'ground-plan.json').read_bytes();old=json.loads(previous);keep={k:v for k,v in old['active_routes'].items()if int(k)not in(2,3)}
 retained_path.write_text(json.dumps(dict(previous_plan_sha256=hashlib.sha256(previous).hexdigest(),previous_seed_sha256=old['input_source_sha256'],tasks=old['tasks'][:10],active_routes=keep,scope='Exact retained copper candidate, not an approval. Current layout and native checks must validate replay.'),indent=2)+'\n')
retained=json.loads(retained_path.read_text())
exec(compile((D/'plan_routes.py').read_text().split('groups=')[0],str(D/'plan_routes.py'),'exec'))
NEGOTIATED=False;branches={int(k):es for k,es in retained['active_routes'].items()};rows=list(retained['tasks']);new=[e for es in branches.values()for e in es]
controlled=[('U1.3','R7.1','DRV_reserved'),('U1.6','R5.1','VS_reserved'),('U1.1','RT1.1','NTC_reserved'),('BR1.3','C1.2','charging_ground'),('T1.2','C1.2','aux_ground'),('D2.1','R10.1','AUX_RECT_reserved'),('T1.4','R4.1','aux_tap'),('T1.4','D2.2','aux_feed'),('R4.2','U1.6','VS_reserved')]
for a,b,label in controlled:
 es,reason=plan(a,b,.3,label);assert es is not None,(a,b,reason)
 i=2 if label=='charging_ground'else 3 if label=='aux_ground'else len(rows)
 row=dict(a=a,b=b,label=label,width=.3,planar_length_mm=sum(math.dist(e['a'],e['b'])for e in es),vias=sum(e['via']for e in es))
 if i<len(rows):rows[i]=row
 else:rows.append(row)
 new.extend(es);branches[i]=es;print('CONTROL',label,row['planar_length_mm'],flush=True)
for a,b,label in[('U1.2','C2.1','local_VDD'),('Q1.1','R8.1','local_GATE'),('Q1.1','R7.2','local_GATE')]:
 es,reason=plan(a,b,.3,label)
 if es is not None:
  i=len(rows);rows.append(dict(a=a,b=b,label=label,width=.3,planar_length_mm=sum(math.dist(e['a'],e['b'])for e in es),vias=sum(e['via']for e in es)));branches[i]=es;new.extend(es);print('LOCAL',label,flush=True)
for a,b,label,widths in[('J1.1','F1.1','AC_input',[.8,.6,.4,.3]),('F1.2','R1.1','AC_fused',[.8,.6,.4,.3]),('TVS1.2','C1.1','clamp_bulk_return',[.8,.6,.4,.3]),('D1.1','TVS1.1','local_clamp',[.8,.6,.4,.3])]:
 for width in widths:
  es,reason=plan(a,b,width,label)
  if es is not None:break
 if es is not None:
  i=len(rows);rows.append(dict(a=a,b=b,label=label,width=width,planar_length_mm=sum(math.dist(e['a'],e['b'])for e in es),vias=sum(e['via']for e in es)));branches[i]=es;new.extend(es);print('POWER RESERVED',label,width,rows[-1]['planar_length_mm'],flush=True)
(D/'ground-plan.json').write_text(json.dumps(dict(input_source_sha256=j['source_sha256'],retained_path_input_sha256=hashlib.sha256(retained_path.read_bytes()).hexdigest(),new_elements=new,active_routes=branches,tasks=rows,scope='Protected control/current-return candidate. Actual native DRC/parity/topology and operating/assembly qualification remain required.'),indent=2)+'\n')
