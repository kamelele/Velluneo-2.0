"""UNADOPTED process comparison only; no approved stackup or manufacturing change."""
from pathlib import Path
import json,math
D=Path(__file__).resolve().parent
j4=json.loads((D/'current-input.json').read_text())
j4['tracks']=[t for t in j4['tracks'] if t['net'] not in {'VDD','PRIMARY_GND','DRV'}]
for p in j4['pads']:p['layers']=[0,1,2,3] if p['tht'] else [0 if l==0 else 3 for l in p['layers']]
for t in j4['tracks']:t['layers']=[0,1,2,3] if t['via'] else [0 if l==0 else 3 for l in t['layers']]
for a in j4['rectangular_rule_areas']:a['layers']=[0,1,2,3]
for t in json.loads((D/'route-input.json').read_text())['tracks']:
 if t['net']in{'SENSE','CS'}:
  guard=dict(t,layers=[0,1,2,3],projection_only=True,scope='Virtual measurement-corridor obstacle for HV routing only; not physical copper.')
  j4['tracks'].append(guard)
(D/'four-layer-input.json').write_text(json.dumps(j4,indent=2)+'\n')
INPUT_FILE='four-layer-input.json'
source=(D/'plan_routes.py').read_text().split('groups=')[0]
source=source.replace('(2,nx,ny)','(4,nx,ny)').replace('2*NN','4*NN').replace('(0,1)if via or','tuple(range(4))if via or')
start=source.index(' vmask=mask(');end=source.index(' graph=coo_matrix',start)
source=source[:start]+''' vmask=mask(net,width,label,{a,b},via=True);good=~np.any(vmask|bad,axis=0);reuse={}
 for p in pads.values():
  if p['net']==net and p['tht']:reuse[grid(p['xy'])]=p['xy']
 for t in fixed+new:
  if t['net']==net and t['via']:reuse[grid(t['a'])]=t['a']
 for (x,y),p in reuse.items():
  if 0<=x<nx and 0<=y<ny and not np.any(bad[:,x,y]):good[x,y]=True
 for la,lb in itertools.combinations(range(4),2):
  u=ids[la][good];v=ids[lb][good];cost=np.full(len(u),3.)
  rr.extend((u,v));cc.extend((v,u));ww.extend((cost,cost))
'''+source[end:]
source=source.replace('layers=[0,1],via=True','layers=[0,1,2,3],via=True')
exec(compile(source,str(D/'plan_routes.py'),'exec'))
retained_fine=json.loads((D/'fine-plan.json').read_text())['new_elements']
ground_source=json.loads((D/'ground-plan.json').read_text())
local_vdd=[e for k,es in ground_source['active_routes'].items()if ground_source['tasks'][int(k)]['label']=='local_VDD'for e in es]
assert local_vdd
for e in local_vdd:
 e=dict(e);e['layers']=[0,1,2,3]if e['via']else[0 if l==0 else 3 for l in e['layers']];new.append(e)
for e in retained_fine:
 e=dict(e);e['layers']=[0,1,2,3]if e['via']else[0 if l==0 else 3 for l in e['layers']];new.append(e)
rows=[]
for a,b in [('T1.5','Q1.2'),('Q1.2','D1.2'),('C1.1','T1.1'),('T1.1','R16.1'),('C1.1','BR1.1')]:
 for width in [.4,.3]:
  es,reason=plan(a,b,width,'unadopted_four_layer_power')
  if es is not None:break
 if es is not None:new.extend(es)
 rows.append(dict(a=a,b=b,width_mm=width,success=es is not None,reason=reason,length_mm=None if es is None else sum(math.dist(e['a'],e['b'])for e in es)))
 print(rows[-1],flush=True)
for a,b,label in [('R9.2','C1.2','shunt_return'),('C1.2','U1.5','quiet_ground'),('C2.2','U1.5','quiet_ground'),('BR1.3','C1.2','charging_ground'),('T1.2','C1.2','aux_ground'),('R5.2','U1.5','quiet_ground'),('RT1.2','C2.2','quiet_ground'),('R13.2','RT1.2','quiet_ground'),('C3.2','T1.2','aux_branch'),('R15.2','C3.2','aux_branch'),('R3.2','C3.2','aux_branch'),('U1.2','C2.1','local_VDD'),('R10.2','C3.1','bias_VDD'),('R10.2','C2.1','main_VDD'),('R17.2','R10.2','startup_VDD'),('R13.1','C2.1','bleed_VDD'),('U1.3','R7.1','DRV_rebuilt')]:
 if label=='shunt_return':
  aux_es,aux_reason=plan('T1.2','C1.2',.3,'aux_ground')
  if aux_es is not None:new.extend(aux_es)
  rows.append(dict(a='T1.2',b='C1.2',label='aux_ground',width_mm=.3,success=aux_es is not None,reason=aux_reason,length_mm=None if aux_es is None else sum(math.dist(e['a'],e['b'])for e in aux_es)))
  print(rows[-1],flush=True)
  es,reason=plan('U1.3','R7.1',.3,'DRV_rebuilt')
  if es is not None:new.extend(es)
  rows.append(dict(a='U1.3',b='R7.1',label='DRV_rebuilt',width_mm=.3,success=es is not None,reason=reason,length_mm=None if es is None else sum(math.dist(e['a'],e['b'])for e in es)))
  print(rows[-1],flush=True)
 if label=='DRV_rebuilt':continue
 if label=='aux_ground':continue
 if label=='local_VDD':
  rows.append(dict(a=a,b=b,label=label,width_mm=local_vdd[0]['width'],success=True,reason=None,retained_local_bypass=True,length_mm=sum(math.dist(e['a'],e['b'])for e in local_vdd)));continue
 if label=='bleed_VDD':
  rows.append(dict(a=a,b=b,label=label,width_mm=.3,success=True,reason=None,retained_fine_grid=True,length_mm=sum(math.dist(e['a'],e['b'])for e in retained_fine)));continue
 w=1. if label=='shunt_return' else .3
 es,reason=plan(a,b,w,label)
 if es is not None:new.extend(es)
 rows.append(dict(a=a,b=b,label=label,width_mm=w,success=es is not None,reason=reason,length_mm=None if es is None else sum(math.dist(e['a'],e['b'])for e in es)))
 print(rows[-1],flush=True)
(D/'four-layer-plan.json').write_text(json.dumps(dict(input_source_sha256=j['source_sha256'],ripped_nets=['VDD','PRIMARY_GND','DRV'],new_elements=new,attempts=rows,scope='Unadopted 4-layer comparison. VDD/GND/DRV copper rebuilt after power routing. User process approval, exact stackup, native checks and engineering review still required; 2-layer source unchanged.'),indent=2)+'\n')
