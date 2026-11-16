#!/usr/bin/env python3
"""Pinned primary-buffer engine, exact input-stage candidate sensitivities.
Not an IC, safety, surge, fault, EMC or physical simulation. Outputs JSON.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json,math
pa=argparse.ArgumentParser();pa.add_argument('--parent',required=True);pa.add_argument('--verify-halved-step',action='store_true');pa.add_argument('--include-cases',action='store_true');a=pa.parse_args()
p=Path(a.parent);assert hashlib.sha256(p.read_bytes()).hexdigest()=='432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea'
spec=importlib.util.spec_from_file_location('input_bus',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.A.update(startup_feed_R_ohm=float('inf'),dedicated_primary_bleeder_R_ohm=998000)
rows=[];convergence={}
for drop in [1.6,2.2]:
 m.A['bridge_total_fixed_drop_V']=drop
 m.cases=[dict(vac_rms_V=v,cap_nom_F=cn,cap_factor=cf,remaining_bus_load_W=w,series_R_ohm=47*rf+source)
   for v,cn,cf,w,rf,source in itertools.product([207,230,253],[10e-6,15e-6],[.8,1.2],[6,8,10],[.95,1.05],[0,10])]
 m.vac=m.np.array([c['vac_rms_V'] for c in m.cases]);m.vp=m.vac*math.sqrt(2)
 m.cap=m.np.array([c['cap_nom_F']*c['cap_factor'] for c in m.cases]);m.p=m.np.array([c['remaining_bus_load_W'] for c in m.cases]);m.rs=m.np.array([c['series_R_ohm'] for c in m.cases])
 rr,_=m.run(2e-6)
 if a.verify_halved_step:
  fine,_=m.run(1e-6)
  for k in ['bulk_min_V','bulk_max_V','line_rms_A','capacitor_LF_rms_A','repetitive_charge_peak_A','calculated_line_input_W']:
   diff=max(abs(x[k]-y[k]) for x,y in zip(rr,fine));convergence[k]=max(convergence.get(k,0),diff)
 for r in rr:
  r['bridge_total_drop_V_assumed']=drop
  # Original engine models total source+candidate resistance. Use all loss as conservative candidate-resistor heat allocation.
  r['candidate_Rin_loss_upper_allocation_W']=r['lumped_series_loss_W']
 rows.extend(rr)
keys=['bulk_min_V','bulk_max_V','calculated_line_input_W','line_rms_A','repetitive_charge_peak_A','capacitor_LF_rms_A','candidate_Rin_loss_upper_allocation_W','fixed_bridge_loss_W','dedicated_bleeder_loss_W','true_power_factor']
b={k:[min(x[k] for x in rows),max(x[k] for x in rows)] for k in keys}
# Independent conservative algebraic primary-HF RMS screen from existing constructed CC/DCM energy law.
hf=[]
for bus,lp,rc,vc,vcr,vo,vd in itertools.product([240,253*math.sqrt(2)],[.002304*.9,.002304*1.1],[2.37*.99,2.37*1.01],[.738,.810],[.318,.343],[18,27],[.5,1.2]):
 ip=vc/rc;ton=lp*ip/bus;tdem=lp*ip/(4*(vo+vd));f=(vcr/vc)/tdem;hf.append(ip*math.sqrt(ton*f/3))
# Conservative mixed-band screen:50Hz coefficient .8;10kHz coefficient2.1 for10-82uF.
# Charge all LF RMS to50Hz and entire constructed primary RMS to10kHz, using triangle inequality.
ripple=[]
for cn,iref in [(10e-6,.130),(15e-6,.190)]:
 group=[x for x in rows if x['cap_nom_F']==cn];lf=max(x['capacitor_LF_rms_A'] for x in group);hr=max(hf)
 ripple.append(dict(bulk_nom_F=cn,LF_A=lf,constructed_primary_RMS_upper_A=hr,LF_reference_A=iref*.8,HF_reference_A=iref*2.1,normalized_triangle_sum=lf/(iref*.8)+hr/(iref*2.1),minimum_bus_V=min(x['bulk_min_V'] for x in group),load_consistency_not_verified=True,interpretation='LF/HF terms come from uncoupled load/control models. HF0.0889A is not a proved bound for10W. Triangle inequality is conservative only for valid same-design spectrum bounds; this is an investigation comparison, not whole-converter rating/life qualification. Prior HF witness bus>=240V.'))
preferred=[x for x in rows if x['cap_nom_F']==15e-6]
vcrest=253*math.sqrt(2);cmax=18e-6;rmin=47*.95
cold={'fixed_source_step_V':vcrest,'Cmax_F':cmax,'Rmin_ohm':rmin,'peak_A_comparison':vcrest/rmin,'tau_s':rmin*cmax,'energy_dissipated_R_J_comparison':.5*cmax*vcrest*vcrest,'I2t_A2s_comparison':cmax*vcrest*vcrest/(2*rmin),'fuse_melting_I2t_typ_A2s_at10In':.15,'I2t_fraction_of_fuse_typ_comparison':cmax*vcrest*vcrest/(2*rmin)/.15,'this_is_not_verified_repetitive_or_fault_coordination':True}
if convergence:
 assert convergence['bulk_min_V']<.02 and convergence['line_rms_A']<.0002 and convergence['capacitor_LF_rms_A']<.0002
r={'study':'VEL-INPUT-01','date':'2026-11-17','cases_count':len(rows),'assumptions':{'Vac_rms_V':[207,230,253],'input_envelope_is_engineering_proposal_not_new_owner_acceptance':True,'line_Hz':50,'remaining_bus_load_W':[6,8,10],'bulk_nom_F':[10e-6,15e-6],'preferred_bulk_nom_F':15e-6,'bulk_initial_cap_factors':[.8,1.2],'bridge_drop_sensitivity_V':[1.6,2.2],'fixed_Rin_ohm':47,'fixed_Rin_tolerance':.05,'source_resistance_sensitivity_ohm':[0,10],'no_old_external_startup_feed':True,'primary_bleeder_ohm':998000,'no_cap_leakage_ESR_age_or_controller_modeled':True},'bounds':b,'half_step_max_abs_differences':convergence,'cold_charge_step_comparison':cold,'bulk_ripple_screen':ripple,'preferred_15uF_bounds':{k:[min(x[k] for x in preferred),max(x[k] for x in preferred)] for k in keys},'bulk_initial_energy_J_at_highline_Cmax':.5*cmax*vcrest*vcrest,'primary_bleeder_each_series_499k_initial_nom_W':vcrest*vcrest/(4*499000),'discharge_to30V_s_comparison_at998k_plus1percent_Cmax':998000*1.01*cmax*math.log(vcrest/30),'no_safe_service_time_or_surge_pass':True,'worst_low_bulk_case':min(rows,key=lambda x:x['bulk_min_V']),'max_Rin_heat_case':max(rows,key=lambda x:x['candidate_Rin_loss_upper_allocation_W']),'new_simulation_type':'Averaged line/bulk numerical integration only; no controller or switched converter','cases':rows}
if not a.include_cases:r.pop('cases')
print(json.dumps(r,indent=2))
