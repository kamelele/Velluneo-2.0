"""Independent result invariants/convergence; does not qualify a controller model."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
a=json.loads((D/'results-80.json').read_text());b=json.loads((D/'results-160.json').read_text())
aa=a['behavioral_model']['cases'];bb=b['behavioral_model']['cases'];assert len(aa)==len(bb)==65
assert sum(c['config']['Raux_ohm']==4.7 for c in bb)==64
for x,y in zip(aa,bb):assert x['config']==y['config']
delta={k:max(abs(x[k]-y[k]) for x,y in zip(aa,bb)) for k in ['Vo_final_V','VDD_final_V','VDD_min_V','VDD_max_V','total_aux_charge_C','duration_s']}
assert delta['VDD_min_V']<.001 and delta['VDD_final_V']<.001
assert max(c['maximum_KCL_error_A'] for c in bb)<1e-9
assert max(c['maximum_off_energy_error_J'] for c in bb)<1e-8
assert all(c['remains_above8p5_UVLO'] and c['reaches10V_reserve'] and not c['events'] for c in bb)
worst=min((c for c in bb if c['config']['Raux_ohm']==4.7),key=lambda c:c['VDD_min_V'])
sensitivity=bb[-1];assert {k:v for k,v in worst['config'].items() if k!='Raux_ohm'}=={k:v for k,v in sensitivity['config'].items() if k!='Raux_ohm'}
r={'passed':True,'scope':'Numerical invariants and step refinement only, not nativeIC/thermal/electrical qualification','case_count':len(bb),'active_4p7_case_count':64,'max_80to160_absolute_delta':delta,'maximum_KCL_error_A':max(c['maximum_KCL_error_A'] for c in bb),'maximum_off_energy_error_J':max(c['maximum_off_energy_error_J'] for c in bb),'worst_active_VDD_min_V':worst['VDD_min_V'],'matched_2p2_VDD_min_V':sensitivity['VDD_min_V'],'matched_improvement_V':sensitivity['VDD_min_V']-worst['VDD_min_V'],'all_cases_above10V_engineering_reserve':True,'inputs_sha256':{n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['calculate.py','results-80.json','results-160.json']}}
(D/'verification.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(r,indent=2))
