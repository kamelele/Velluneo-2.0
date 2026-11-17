#!/usr/bin/env python3
"""Passive flyback demagnetization with an energy-conserving clamp transition.

No controller, switch capacitance, diode recovery, TVS I-V or physical thermal model.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp
D=Path(__file__).resolve().parent;P=D.parent.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):(D/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',type=Path,required=True);args=ap.parse_args()
source=json.loads((D/'sources.json').read_text())
for e in source['primary_sources']:assert sha(args.source_dir/e['filename'])==e['sha256'],e['filename']
for e in source['repository_inputs']:assert sha(P/e['path'])==e['sha256'],e['path']
c=json.loads((D/'contract.json').read_text())
Lp=c['primary_open_circuit_inductance_H'];n=c['primary_secondary_turns_ratio']
Pallow=(c['proposed_TVS_junction_target_C']-c['proposed_local_air_C'])/c['required_TVS_Rtheta_JA_K_per_W_for_screen']

def analytic(lam,I,Vt,Vd,Vr,Vbus):
 Lm=Lp/(1+lam);Ll=Lp-Lm;Vc=Vt+Vd;E0=.5*Lp*I*I
 split=Vc>Vr*(1+lam)
 if split:
  tc=Ll*I/(Vc-Vr);toff=Lm*I/Vr;Ec=.5*Ll*I*I*Vc/(Vc-Vr)
 else:
  tc=toff=Lp*I/Vc;Ec=E0
 ton=Lp*I/Vbus
 f=min(c['frequency_ceiling_Hz'],c['normal_magnetic_energy_rate_ceiling_W_hypothesis']/E0,(1-c['ideal_DCM_period_reserve_fraction_choice'])/(ton+toff))
 Etvs=Ec*Vt/Vc;Ed=Ec*Vd/Vc;Eout=E0-Ec
 assert min(Etvs,Ed,Eout)>-1e-15 and abs(E0-(Etvs+Ed+Eout))<1e-15
 return {'lambda_Llk_over_Lm':lam,'Lm_H':Lm,'Llk_H':Ll,'Ipk_A':I,'TVS_V_proxy':Vt,'clamp_diode_V_sensitivity':Vd,'reflected_V_screen':Vr,'bus_V_screen':Vbus,'regime':'split_to_secondary' if split else 'all_clamp_secondary_blocked','turnon_s':ton,'clamp_s':tc,'off_s':toff,'frequency_Hz_constructed':f,'magnetic_energy_rate_W':E0*f,'stored_energy_J':E0,'TVS_energy_J':Etvs,'clamp_diode_energy_J':Ed,'secondary_delivered_energy_J':max(0,Eout),'TVS_power_W':Etvs*f,'clamp_diode_power_W':Ed*f,'required_Rtheta_JA_K_per_W':(c['proposed_TVS_junction_target_C']-c['proposed_local_air_C'])/(Etvs*f),'TVS_target_met_if_thermal_contract_holds':Etvs*f<=Pallow}

def lambda_limit(Vt,Vd,Vr,Pin,budget=Pallow):
 Vc=Vt+Vd
 if Vc<=Vr:return {'maximum_lambda':None,'reason':'Even zero leakage can divert all energy; need controller energy/fault constraint or another clamp design.'}
 if budget>=Pin*Vt/Vc:return {'maximum_lambda':None,'reason':'All-clamp average TVS energy already within this hypothetical DC thermal budget.'}
 a=budget*(Vc-Vr)/(Pin*Vt);limit=a/(1-a)
 assert limit<Vc/Vr-1
 return {'maximum_lambda':limit,'maximum_Llk_H_at_fixed_Lp':Lp*limit/(1+limit),'Lm_H_at_limit':Lp/(1+limit),'reason':'Derived DC thermal acceptance frontier in constant-voltage passive model; not measured leakage or guaranteed TVS curve.'}

# Finite-resistance off-phase solver. State is [im, ip, Etvs, Edcl, Eout,
# Edout, EcuS, EcuP]. It independently integrates power, not the analytic formula.
def finite(lam,I,Vt,Vd,Vo,Vf,Rp,Rs,steps):
 Lm=Lp/(1+lam);Ll=Lp-Lm;Vc=Vt+Vd;Vr0=n*(Vo+Vf);E0=.5*Lp*I*I
 times=[];states=[];phases=[];energy=np.zeros(6);im=ip=I;t=0.0
 horizon=50*Lp*I/min(Vc,Vr0)
 h=Lp*I/min(Vc,Vr0)/steps
 def append(sol,phase):
  nonlocal energy,im,ip,t
  for tt,yy in zip(sol.t,sol.y.T):times.append(float(tt));states.append(yy.tolist())
  im,ip=map(float,sol.y[:2,-1]);energy=sol.y[2:,-1].copy();t=float(sol.t[-1]);phases.append(phase)
 def current_end(t,y):return y[1]
 current_end.terminal=True;current_end.direction=-1
 def secondary_end(t,y):return y[0]-y[1]
 secondary_end.terminal=True;secondary_end.direction=-1
 def magnetizing_end(t,y):return y[0]
 magnetizing_end.terminal=True;magnetizing_end.direction=-1
 if Vc+Rp*I>Vr0*(1+lam):
  def rhs(t,y):
   mm,pp=y[:2];Is=n*(mm-pp);Vr=Vr0+n*Rs*Is
   return [-Vr/Lm,-(Vc+Rp*pp-Vr)/Ll,Vt*pp,Vd*pp,Vo*Is,Vf*Is,Rs*Is*Is,Rp*pp*pp]
  sol=solve_ivp(rhs,(0,horizon),[I,I,*energy],events=[current_end,secondary_end],max_step=h,rtol=2e-10,atol=1e-13)
  assert sol.success
  append(sol,'secondary_and_clamp')
  assert min(y[0]-y[1] for y in states)>=-1e-10
  if abs(ip)<1e-9:ip=0.0
  elif abs(im-ip)<1e-9:im=ip=(im+ip)/2
  else:raise AssertionError(('Unexpected first-phase event',im,ip))
 if ip>1e-9:
  def rhs(t,y):
   pp=y[1];di=-(Vc+Rp*pp)/Lp
   return [di,di,Vt*pp,Vd*pp,0,0,0,Rp*pp*pp]
  sol=solve_ivp(rhs,(t,horizon),[ip,ip,*energy],events=current_end,max_step=h,rtol=2e-10,atol=1e-13)
  assert sol.success;append(sol,'all_clamp');im=ip=0.0
 if im>1e-9:
  def rhs(t,y):
   mm=y[0];Is=n*mm;Vr=Vr0+n*Rs*Is
   return [-Vr/Lm,0,0,0,Vo*Is,Vf*Is,Rs*Is*Is,0]
  sol=solve_ivp(rhs,(t,horizon),[im,0,*energy],events=magnetizing_end,max_step=h,rtol=2e-10,atol=1e-13)
  assert sol.success;append(sol,'secondary_only');im=0.0
 residual=E0-float(sum(energy));max_kcl=max((abs((y[0]-y[1])-(n*(y[0]-y[1]))/n) for y in states),default=0.0)
 assert abs(residual)<max(1e-12,E0*1e-7),(residual,E0,phases)
 assert min(energy)>-1e-12
 return {'lambda':lam,'Ipk_A':I,'TVS_V_proxy':Vt,'Vdiode_V_sensitivity':Vd,'output_V':Vo,'output_diode_V_sensitivity':Vf,'Rp_ohm':Rp,'Rs_ohm':Rs,'max_step_s':h,'steps_parameter':steps,'phases':phases,'demag_s':t,'stored_energy_J':E0,'TVS_energy_J':float(energy[0]),'clamp_diode_energy_J':float(energy[1]),'output_energy_J':float(energy[2]),'output_diode_energy_J':float(energy[3]),'secondary_copper_energy_J':float(energy[4]),'primary_copper_energy_J':float(energy[5]),'energy_residual_J':residual,'max_KCL_residual_A':max_kcl,'solver_points':len(times)}

allcases=[]
for lam,Vo,Vf,secDrop,Vt,Vd,I,Vbus in itertools.product(c['leakage_ratio_sensitivities'],c['output_V_screens'],c['output_diode_V_sensitivities'],[0,c['hot_secondary_R_ohm']*c['independent_secondary_peak_A_proxy']],c['TVS_plateau_V_proxies'],c['clamp_diode_V_sensitivities'],c['normal_peak_primary_A_hypotheses'],c['bus_V_screens']):
 r=analytic(lam,I,Vt,Vd,n*(Vo+Vf+secDrop),Vbus);r.update(output_V=Vo,output_diode_V_sensitivity=Vf,independent_secondary_IR_V_screen=secDrop);allcases.append(r)
normal=[x for x in allcases if x['output_V']<=27]
frontiers=[]
for Vo,Vf,secDrop in itertools.product(c['output_V_screens'],c['output_diode_V_sensitivities'],[0,c['hot_secondary_R_ohm']*c['independent_secondary_peak_A_proxy']]):
 Vr=n*(Vo+Vf+secDrop);frontiers.append({'Vo_V':Vo,'VFout_sensitivity_V':Vf,'secondary_IR_screen_V':secDrop,'Vr_V':Vr,'0p55W_Rtheta100_frontier':lambda_limit(175.1164,0,Vr,11),'0p40W_normal_allocation_frontier':lambda_limit(175.1164,0,Vr,11,c['normal_TVS_power_allocation_W_choice'])})
finitecases=[];convergence=[]
for lam,Vo,Vt,Vf in itertools.product([.01,.05],[27,40],[175.1164,286.972],[0,1.7]):
 pair=[finite(lam,c['normal_peak_primary_A_hypotheses'][-1],Vt,0,Vo,Vf,c['hot_primary_R_ohm'],c['hot_secondary_R_ohm'],s) for s in [80,160]]
 finitecases.append(pair[-1]);convergence.append({'case':{k:pair[-1][k] for k in ['lambda','output_V','TVS_V_proxy','output_diode_V_sensitivity']},'delta_TVS_J':abs(pair[1]['TVS_energy_J']-pair[0]['TVS_energy_J']),'delta_demag_s':abs(pair[1]['demag_s']-pair[0]['demag_s'])})
# Degenerate no-resistance reference verifies independent ODE quadrature against
# the analytic split/all-clamp transitions, including an exact regime boundary.
reference=[]
for lam,Vr in itertools.product([.005,.01,.05],[108.0,175.1164/1.01,180.0]):
 a=analytic(lam,.35852176738964414,175.1164,0,Vr,240)
 r=finite(lam,.35852176738964414,175.1164,0,Vr/n,0,0,0,160)
 delta=abs(a['TVS_energy_J']-r['TVS_energy_J']);assert delta<1e-10
 reference.append({'lambda':lam,'Vr_V':Vr,'analytic_regime':a['regime'],'TVS_energy_difference_J':delta,'off_time_difference_s':abs(a['off_s']-r['demag_s'])})
fault=[]
for Ip,label in [(c['normal_peak_primary_A_hypotheses'][-1],'normal current proxy'),(1.6/(2.37*.979),'1.6V/Rsense sensitivity, NOT a guaranteed maximum fault current')]:
 E=.5*Lp*Ip*Ip
 for N in [1,3,9,100]:
  for f in [755,106000]:fault.append({'Ipk_A_sensitivity':Ip,'current_basis':label,'pulses':N,'within_burst_rate_Hz_sensitivity':f,'all_diverted_energy_J_upper_within_passive_model':N*E,'allocated_N_period_window_s_sensitivity':N/f,'energy_rate_W_during_train':E*f,'minimum_repeat_period_s_for0p55W_average':N*E/Pallow,'minimum_repeat_period_s_for0p40W_average':N*E/c['normal_TVS_power_allocation_W_choice'],'not_a_native_fault_latency_or_SOA_acceptance':True})
report={
 'scope':'Executed passive, ideal constant-voltage clamp and diode model; not UCC28711 switching, TVS dynamics, MOS SOA, parasitics or thermal validation.',
 'runtime':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__},
 'input_contract_sha256':sha(D/'contract.json'),
 'normal_thermal_target':{'local_air_C_choice':70,'junction_C_choice':125,'actual_required_Rtheta_K_per_W_not_established':100,'TVS_average_power_allowance_W_at_Rtheta100':Pallow,'normal_allocation_W_choice':c['normal_TVS_power_allocation_W_choice'],'actual_required_Rtheta_K_per_W_at0p40W':(125-70)/c['normal_TVS_power_allocation_W_choice']},
 'analytic_sweep':{'cases':len(allcases),'normal_output_cases':len(normal),'full_cases_canonical_sha256':hashlib.sha256(json.dumps(allcases,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'min_TVS_power_W':min(x['TVS_power_W'] for x in allcases),'max_TVS_power_W':max(x['TVS_power_W'] for x in allcases),'max_normal_output_TVS_case':max(normal,key=lambda x:x['TVS_power_W']),'max_all_output_TVS_case':max(allcases,key=lambda x:x['TVS_power_W']),'cases_above_proposed0p55W_contract':sum(x['TVS_power_W']>Pallow for x in allcases),'all_clamp_cases':sum(x['regime']=='all_clamp_secondary_blocked' for x in allcases),'not_actual_correlated_controller_corners':True},
 'cold_proxy_leakage_frontiers':frontiers,
 'proposed_finished_transformer_acceptance':{'Llk_primary_secondary_H_choice':20e-6,'Lp_open_min_H':Lp*.9,'lambda_at_Lp_min':20e-6/(Lp*.9-20e-6),'normal_TVS_power_W_at_11W_and_cold_highref_proxy':11*(20e-6/(Lp*.9))*175.1164/(175.1164-n*(27+1.7+c['hot_secondary_R_ohm']*c['independent_secondary_peak_A_proxy'])),'not_a_measured_or_supplier_confirmed_part_parameter':True},
 'finite_R_demagnetization_cases':finitecases,
 'convergence_80_to160':{'cases':len(convergence),'max_delta_TVS_energy_J':max(x['delta_TVS_J'] for x in convergence),'max_delta_demag_s':max(x['delta_demag_s'] for x in convergence),'details':convergence},
 'analytic_vs_independent_zero_R_ODE':reference,
 'fault_train_sensitivities':fault,
 'voltage_budget_retained':{'normal_line_crest_V':357.7960312803931,'TVS_hot_plateau_proxy_V':286.972,'clamp_diode_V_sensitivity':1.7,'drain_before_commutation_V_proxy':646.4680312803932,'additional_to700V_engineering_screen_V_proxy':53.531968719606766,'additional_to800V_absolute_rating_V_proxy':153.53196871960677,'not_a_guaranteed_waveform_bound':True},
 'source_hashes_verified':True,'actual_physical_measurement':False,'graph_CAD_values_changed':False}
write('results.json',report)
write('verification.json',{'passed_within_declared_model':True,'analytic_cases':len(allcases),'finite_R_cases_80_and160':len(finitecases)*2,'zero_R_ODE_references':len(reference),'maximum_finite_R_energy_residual_J':max(abs(x['energy_residual_J']) for x in finitecases),'maximum_zero_R_analytic_TVS_difference_J':max(x['TVS_energy_difference_J'] for x in reference),'maximum_current_split_residual_A':max(x['max_KCL_residual_A'] for x in finitecases),'convergence':report['convergence_80_to160'],'limitations':report['scope']})
print(json.dumps({k:report[k] for k in ['normal_thermal_target','analytic_sweep']}));print('Finite-R cases:',len(finitecases),'energy residual max:',max(abs(x['energy_residual_J']) for x in finitecases));print('Passive model checks passed; no physical/controller/fault acceptance')
