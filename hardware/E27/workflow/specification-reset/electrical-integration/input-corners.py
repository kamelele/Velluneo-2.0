#!/usr/bin/env python3
"""Extend the pinned averaged bridge/bulk model to49/50/51Hz and11W screens.
Separate existing versus proposed bleeder branches; not controller/fault/EMC evidence.
"""
from pathlib import Path
import hashlib,importlib.util,itertools,json,math,time
P=Path(__file__).resolve().parent.parent;D=P/'electrical-integration';f=P/'driver-study/primary-buffer/calculate.py'
assert hashlib.sha256(f.read_bytes()).hexdigest()=='432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea'
s=importlib.util.spec_from_file_location('bus',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.A.update(startup_feed_R_ohm=float('inf'))
rows=[];diff={};start=time.monotonic()
for hz,drop,branch in itertools.product([49,50,51],[1.6,2.2],['existing_series_pair','proposed_two_series_pairs']):
 m.A['line_Hz']=hz;m.period=1/(2*hz);m.A['bridge_total_fixed_drop_V']=drop
 # Low-resistance endpoints maximize this explicit bleeder-loss/load screen.
 m.A['dedicated_primary_bleeder_R_ohm']=(998000 if branch=='existing_series_pair' else 499000)*.979
 m.cases=[dict(vac_rms_V=v,cap_nom_F=15e-6,cap_factor=cf,remaining_bus_load_W=w,series_R_ohm=47*rf+source) for v,cf,w,rf,source in itertools.product([207,230,253],[.8,1.2],[6,8,10,11],[.95,1.05],[0,10])]
 m.vac=m.np.array([c['vac_rms_V'] for c in m.cases]);m.vp=m.vac*math.sqrt(2);m.cap=m.np.array([c['cap_nom_F']*c['cap_factor'] for c in m.cases]);m.p=m.np.array([c['remaining_bus_load_W'] for c in m.cases]);m.rs=m.np.array([c['series_R_ohm'] for c in m.cases])
 r,_=m.run(2e-6);fine,_=m.run(1e-6)
 for k in ['bulk_min_V','line_rms_A','repetitive_charge_peak_A','capacitor_LF_rms_A','lumped_series_loss_W']:
  diff[k]=max(diff.get(k,0),max(abs(a[k]-b[k]) for a,b in zip(r,fine)))
 for a in r:a.update(line_Hz=hz,bridge_fixed_drop_V=drop,bleeder_case=branch,not_switching_controller_or_fault_model=True)
 rows+=r;print(hz,drop,branch,len(r),'elapsed',round(time.monotonic()-start,1),flush=True)
keys=['bulk_min_V','bulk_max_V','line_rms_A','repetitive_charge_peak_A','capacitor_LF_rms_A','lumped_series_loss_W','fixed_bridge_loss_W','dedicated_bleeder_loss_W','calculated_line_input_W']
summary={}
for branch in ['existing_series_pair','proposed_two_series_pairs']:
 g=[r for r in rows if r['bleeder_case']==branch];summary[branch]={'cases':len(g),'bounds':{k:[min(a[k] for a in g),max(a[k] for a in g)] for k in keys},'min_bus_case':min(g,key=lambda a:a['bulk_min_V'])}
result={'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'cases':len(rows),'time_step_refinement_max_abs':diff,'screen_load_note':'6/8/10/11W remaining constant bus load; additional dedicated bleeder explicitly included; no claim load trajectory matches actual IC','summary':summary,'limitations':['Averaged bridge/bulk constant-power model, no real startup/fault/controller','Fixed diode drop, no HF spectrum, input EMI or surge/aging qualification','NewECO branch is a proposal, not fitted hardware','Series-resistor total loss is a conservative allocation to candidateRIN because source resistance also modeled']}
(D/'input-corners-results.json').write_text(json.dumps(result,indent=2)+'\n');print('DONE',len(rows),flush=True)
