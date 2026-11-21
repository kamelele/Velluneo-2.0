from pathlib import Path
import math,json,hashlib,ast
import scipy.integrate,scipy.optimize
R=Path(r'C:\Users\kamil\Documents\Codex\2026-11-17\zo\work\Velluneo-readiness');P=R/'hardware/E27/workflow/specification-reset';D=P/'design-closure-02';W=R.parent
f=json.loads((D/'frozen-files.json').read_text(encoding='utf-8'));body=f['body_sha256']
assert body=='d02eab969d03e53213033b2cd71d3c3f079b050bcfc2633e2053bbbe1e19c526'
for x in f['files']:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
native=0
for scope,folder,key in [('controller','closure-controller-sources','fresh_sources'),('cooling','closure-cooling-sources','fresh_bytes')]:
 reg=json.loads((D/scope/'sources.json').read_text(encoding='utf-8'))
 for s in reg[key]:
  assert hashlib.sha256((W/folder/s['file']).read_bytes()).hexdigest()==s['sha256'];native+=1
t=json.loads((D/'transformer/construction-contract.json').read_text(encoding='utf-8'));F=x=integral=0.;width=t['winding_band_mm']/1000
for seg in t['selected_order_inner_to_outer']:
 d=seg['radial_mm']/1000;delta=seg['turns']*{'P':1,'S':-4,'A':0,'T':0}[seg['winding']];f0=F
 per=lambda y:2*(.0131+.0069)-8*.002+2*math.pi*(.002+y)
 integral+=scipy.integrate.quad(lambda y:per(y)*(f0+delta*(y-x)/d)**2,x,x+d,epsabs=1e-20)[0]
 F+=delta;x+=d
L=4*math.pi*1e-7*integral/width
expected=json.loads((D/'transformer/results.json').read_text(encoding='utf-8'))['selected_PS_slab_H'];assert abs(L-expected)<1e-18 and F==0
A=math.pi*.09*.045+math.pi*(.09**2-.027**2)/4;Rh=.004/(4*150*.005*.003)+.1
q=scipy.optimize.brentq(lambda q:q-A*(3*(29-(2+Rh)*q)+.85*5.670374419e-8*((342.15-(2+Rh)*q)**4-313.15**4)),0,7)
housing_plate=69-2*q+4*.85
saved=json.loads((D/'cooling/housing-branch.json').read_text(encoding='utf-8'));assert abs(housing_plate-saved['chosen_hypothesis_case']['primary_plate_C'])<1e-10
q68=(69-(68-4*.85))/2;th68=68-4*.85-Rh*q68
evf=q68/(A*5.670374419e-8*((th68+273.15)**4-313.15**4));assert abs(evf-saved['required_emissivity_times_viewfactor_for68C_no_convection_screen'])<1e-10
reset=1.021e6*.94e-6*1.05*1.003*math.log(35/7.7);ctrl=json.loads((D/'controller/results.json').read_text(encoding='utf-8'));assert abs(reset-ctrl['reset']['passive_no_injection_35_to7p7_upper_s'])<1e-12
old=(P/'pcb-readiness-01/startup-protection/calculate.py').read_text(encoding='utf-8').replace('base=.0035;','base=.0035+cfg.get("extra_bias_A",0.);');tree=ast.parse(old)
cross=json.loads((D/'cross-check.json').read_text(encoding='utf-8'));worst=cross['worst160'];temp=worst['new_cut_length_DCR_temperature_C_screen']
ns={'math':math,'NPS':4.,'NAS':22/30,'R13':979000.,'RBLEED':9790.,'wr':{k:r*(1+.00393*(temp-20))for k,r in t['proposed_DCR20_upper_ohm'].items()}}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'pure_trajectory','exec'),ns)
refine=ns['trajectory'](worst['config'].copy(),640)
assert abs(refine['VDD_min_V']-cross['matched320']['VDD_min_V'])<1e-5
out=dict(body_sha256=body,members=len(f['files']),fresh_native_source_instances=native,independent_quad_PS_leakage_uH=L*1e6,independent_housing_plate_C=housing_plate,independent_housing_heat_W=q,independent_no_convection_epsVF_threshold=evf,independent_reset_s=reset,author_pure_function_replay_steps=640,replay_minimum_VDD_V=refine['VDD_min_V'],replay_delta_vs320_V=refine['VDD_min_V']-cross['matched320']['VDD_min_V'],scope='Independent arithmetic and numerical replay; no actual nativecontroller or hardware validation')
print(json.dumps(out,indent=2))
