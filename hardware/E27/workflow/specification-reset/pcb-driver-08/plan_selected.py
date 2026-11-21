"""Complete the one selected board, protecting short driver/gate paths before power feeds."""
from pathlib import Path
import json,math,time,hashlib
D=Path(__file__).resolve().parent
exec(compile((D/'routing_geometry.py').read_text(),str(D/'routing_geometry.py'),'exec'))
def element_key(e):return(e['net'],tuple(e['layers']),e['via'],tuple(sorted(tuple(round(x,5)for x in p)for p in(e['a'],e['b']))))
labels={element_key(e):e['label']for e in json.loads((D/'protected-local-copper.json').read_text())['elements']}
for t in fixed:
 if t['net']=='PRIMARY_GND':
  t['label']=labels.get(element_key(t));assert t['label'],t
# Actual original dedicated measurement conductors, not all same-net source/pulldown copper.
for t in json.loads((D.parent/'pcb-route-07/route-input.json').read_text())['tracks']:
 if t['net']in{'SENSE','CS'}:fixed.append(dict(t,layers=[0,1,2,3],projection_only=True))
groups=[set(g)for g in j['connected_pad_groups']];rows=[];original_mask=mask
def group(key):return next(g for g in groups if key in g)
def checkpoint():
 (D/'selected-route-plan.json').write_text(json.dumps(dict(source_board_sha256=j['source_sha256'],geometry_helper_sha256=hashlib.sha256((D/'routing_geometry.py').read_bytes()).hexdigest(),attempts=rows,new_elements=new,remaining_groups=[sorted(g)for g in groups],scope='One selected 4-layer board. Native saved connectivity/DRC, source intent and protected copper/topology checks are authoritative; model geometry is not operating qualification.'),indent=2)+'\n')
def connect(a,b,label,widths=(.4,.3),allowed=None):
 global mask
 if group(a)is group(b):return True
 def scoped(*args,**kwargs):
  m=original_mask(*args,**kwargs)
  if allowed is not None:
   for layer in set(range(4))-set(allowed):m[layer]=True
  return m
 mask=scoped
 candidates=[];trials=[];optimize=label in{'primary_feed','primary_drain','clamp_drain','IC_return','AC_fused','bulk_charge'}
 for width in widths:
  es,reason=plan(a,b,width,label)
  length=None if es is None else sum(math.dist(e['a'],e['b'])for e in es);trials.append(dict(width_mm=width,success=es is not None,reason=reason,planar_length_mm=length))
  if es is not None:
   candidates.append((width,es,length))
   if not optimize:break
 mask=original_mask
 if candidates:
  shortest=min(c[2]for c in candidates);width,es,length=max((c for c in candidates if c[2]<=shortest*1.15+1e-8),key=lambda c:c[0]);reason=None
 else:es=None;length=None
 row=dict(a=a,b=b,label=label,width_mm=width,allowed_layers=allowed,success=es is not None,reason=reason,planar_length_mm=length,vias=None if es is None else sum(e['via']for e in es),width_trials=trials);rows.append(row)
 if es is not None:
  new.extend(es);ga,gb=group(a),group(b);ga.update(gb);groups.remove(gb)
 checkpoint();print(json.dumps(row),flush=True);return es is not None
connect('U1.3','R7.1','driver',(.4,.3),[0])
connect('R7.2','Q1.1','gate',(.4,.3),[0])
connect('R8.1','Q1.1','gate_pulldown',(.4,.3),[3])
connect('C1.1','T1.1','primary_feed',(.8,.6,.4),[1,2])
connect('T1.5','Q1.2','primary_drain',(.8,.6,.4))
connect('Q1.2','D1.2','clamp_drain',(.8,.6,.4))
connect('T1.1','R16.1','startup_bulk',(.4,.3))
connect('R14.1','T1.1','bulk_bleed_B',(.4,.3))
connect('R2.1','BR1.1','bulk_bleed_A',(.4,.3))
connect('C1.1','BR1.1','bulk_charge',(.8,.6,.4))
connect('T1.2','C1.2','aux_ground',(.4,.3))
connect('C1.2','U1.5','quiet_ground',(.6,.4,.3))
connect('BR1.3','C1.2','charging_ground',(.6,.4,.3))
connect('R10.2','C2.1','main_VDD',(.4,.3))
connect('J1.1','F1.1','AC_input',(.8,.6,.4,.3))
connect('F1.2','R1.1','AC_fused',(.8,.6,.4,.3))
connect('R1.2','BR1.4','AC_limited',(.8,.6,.4,.3))
connect('J1.2','BR1.2','AC_neutral',(.8,.6,.4,.3))
connect('R16.2','R17.1','startup_mid',(.4,.3))
connect('R17.2','R10.2','startup_VDD',(.4,.3))
connect('R2.2','R3.1','bulk_bleed_mid',(.4,.3))
checkpoint();print('Plannedremaininggroups',len(groups),'target27',flush=True)
