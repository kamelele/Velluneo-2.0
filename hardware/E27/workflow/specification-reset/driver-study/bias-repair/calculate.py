#!/usr/bin/env python3
"""UCC28711 bounded replacement calculation using native SLUSB86C source values.
Run beside ../primary-buffer/calculate.py: python calculate.py > results.json
Not an IC, switching/fault, or physical simulation. Requires numpy through the bus model.
"""
from pathlib import Path
import hashlib,importlib.util,itertools,json,math
A={'Np':152,'Ns':38,'Na':28,'Ae_m2':31e-6,'AL_nom_H':100e-9,'Lp_factors':[.9,1.1],
 'bus_V':[240,280,253*math.sqrt(2)],'Vo_normal_V':[18,21,24,27],
 'Rcs_ohm':2.37,'resistor_factors':[.99,1.01],
 'VCCR_table_V':[.318,.330,.343],'VCSTmax_table_V':[.738,.780,.810],
 'eta_transformer_assumed':[.85,.9,.95],
 'main_diode_V_assumed':[.5,1.2],'sample_diode_V_assumed':[.3,.8],
 'aux_diode_V_assumed':[.5,1.0],'aux_loss_V_assumed':[0,.5],
 'aux_positive_ringing_allowance_V_assumed':3,
 'VDD_normal_ripple_allowance_V_assumed':.5,
 'VDD_min_recommended_V':9,'VDD_max_recommended_V':35,
 'VDD_on_table_V':[19,21,23],'VDD_off_max_table_V':8.5,
 'VDD_effective_cap_range_F':[.75e-6,1e-6],
 'VDD_cap_range_is_unqualified_component_contract':True,
 'Cout_nom_F':10e-6,'Cout_max_F':12e-6,'Cout_effective_min_assumed_F':4e-6,
 'bleeder_output_ohm':10000,'VDD_run_budget_A_assumed':.006,
 'run_current_table_max_without_gate_A':.00265,
 'VDD_start_sink_table_max_A':30e-6,'HV_charge_current_sensitivity_A':[100e-6,250e-6,300e-6,500e-6],
 'HV_current_at_other_VDD_is_not_guaranteed_by_endpoint_spec':True,
 'VDD_boot_reserve_V_assumed':1.0,
 'VS_Rtop_ohm':93100,'VS_Rbottom_ohm':20500,
 'VS_ref25_table_V':[4.01,4.05,4.09],'VS_temp_slope_proxy_V_per_C':-.0008,
 'Tj_sensitivity_C':[-40,25,125],'VS_bias_table_A':[-.25e-6,.25e-6],
 'cable_comp_at_full_load_table_V':[-.055,.025],
 'VS_OVP25_table_V':[4.55,4.71],
 'RLC_total_delay_assumed_s':[100e-9,150e-9], 'KLC_table':[24,25,28.6],
 'NTC_R25_nom_ohm_assumed':100000,'NTC_B_nom_K_assumed':4250,
 'NTC_relative_tolerance_assumed':.01,'NTC_threshold_table_V':[.9,1.0],
 'NTC_current_table_A':[90e-6,125e-6],
 'fault_CS_threshold_table_V':[1.4,1.6]}
n=A['Np']/A['Ns'];nas=A['Na']/A['Ns'];npa=A['Np']/A['Na'];lp0=A['AL_nom_H']*A['Np']**2
rows=[]
for v,vo,lf,rf,vc,vcr,eta,vd in itertools.product(A['bus_V'],A['Vo_normal_V'],A['Lp_factors'],A['resistor_factors'],A['VCSTmax_table_V'],A['VCCR_table_V'],A['eta_transformer_assumed'],A['main_diode_V_assumed']):
 lp=lp0*lf;rs=A['Rcs_ohm']*rf;ip=vc/rs;dd=vcr/vc
 # Effective DD carries independent table corners consistently; nominal is near0.425.
 io=vcr*n*eta/(2*rs);vr=n*(vo+vd);tdem=lp*ip/vr;f=dd/tdem;ton=lp*ip/v
 idle=1/f-ton-tdem
 assert math.isclose(.5*n*ip*dd*eta,io,rel_tol=1e-12)
 assert math.isclose(.5*lp*ip*ip*f*eta,io*(vo+vd),rel_tol=1e-12)
 rows.append(dict(f_Hz=f,primary_peak_A=ip,secondary_peak_A=n*ip,ton_s=ton,tdemag_s=tdem,idle_s=idle,
  effective_demag_duty=dd,CC_total_A=io,LED_after_10k_A=io-vo/A['bleeder_output_ohm'],
  normal_flux_T=lp*ip/(A['Np']*A['Ae_m2']),primary_rms_A=ip*math.sqrt(ton*f/3),secondary_rms_A=n*ip*math.sqrt(dd/3)))
bounds={k:{'min':min(x[k] for x in rows),'max':max(x[k] for x in rows)} for k in rows[0]}
# Aux voltage and bootstrap requirements including a recommended 9V floor rather than only UVLOoff.
vdd=[]
for vo,vd,vda,loss in itertools.product(A['Vo_normal_V'],A['main_diode_V_assumed'],A['aux_diode_V_assumed'],A['aux_loss_V_assumed']):
 vdd.append(nas*(vo+vd)-vda-loss-A['VDD_normal_ripple_allowance_V_assumed'])
vo_take=(A['VDD_min_recommended_V']+A['VDD_boot_reserve_V_assumed']+max(A['aux_diode_V_assumed'])+max(A['aux_loss_V_assumed']))/nas-min(A['main_diode_V_assumed'])
io_min=bounds['CC_total_A']['min']-vo_take/A['bleeder_output_ohm']
t_charge=A['Cout_max_F']*vo_take/io_min
q_run=t_charge*A['VDD_run_budget_A_assumed']
q_available=A['VDD_effective_cap_range_F'][0]*(min(A['VDD_on_table_V'])-A['VDD_min_recommended_V']-A['VDD_boot_reserve_V_assumed'])
boot={'aux_takeover_output_V_proxy':vo_take,'available_output_charge_current_A_proxy':io_min,
 'charge_time_s_proxy':t_charge,'charge_needed_by_run_budget_C':q_run,'available_charge_C':q_available,
 'charge_margin_ratio_before_initial_cycles':q_available/q_run,
 'remaining_initial_cycle_time_s_at_6mA_proxy':(q_available-q_run)/A['VDD_run_budget_A_assumed'],
 'three_initial_low_current_cycles_not_time_bounded':True,
 'required_CDD_F_manufacturer_formula_with_6mA':q_run/(min(A['VDD_on_table_V'])-A['VDD_off_max_table_V']-1),
 'endpoint_constant_charge_examples_s':{str(i):A['VDD_effective_cap_range_F'][1]*max(A['VDD_on_table_V'])/(i-A['VDD_start_sink_table_max_A']) for i in A['HV_charge_current_sensitivity_A']}}
cv=[];ov=[];negative=[]
for tf,bf,vd,loss,bias in itertools.product(A['resistor_factors'],A['resistor_factors'],A['sample_diode_V_assumed'],A['aux_loss_V_assumed'],A['VS_bias_table_A']):
 top=A['VS_Rtop_ohm']*tf;bot=A['VS_Rbottom_ohm']*bf;k=bot/(top+bot);rt=top*bot/(top+bot)
 for ref,temp,comp in itertools.product(A['VS_ref25_table_V'],A['Tj_sensitivity_C'],A['cable_comp_at_full_load_table_V']):
  vref=ref+A['VS_temp_slope_proxy_V_per_C']*(temp-25)+comp
  cv.append(((vref+bias*rt)/k+loss)/nas-vd)
 for threshold in A['VS_OVP25_table_V']:
  ov.append(((threshold+bias*rt)/k+loss)/nas-vd)
 for v in A['bus_V']:negative.append(v/npa/top)
ntc=[]
for r25,beta,th,ic in itertools.product([99000,101000],[4250*.99,4250*1.01],A['NTC_threshold_table_V'],A['NTC_current_table_A']):
 trip=th/ic;temp=1/(1/298.15+math.log(trip/r25)/beta)-273.15;ntc.append(temp)
rlc=[k*A['VS_Rtop_ohm']*A['Rcs_ohm']*td*npa/lp0 for k,td in itertools.product(A['KLC_table'],A['RLC_total_delay_assumed_s'])]
# Inductive flux diagnostic at backup OCP only, not proof of a bounded switching fault peak.
backup=max(lp0*lf*th/(A['Rcs_ohm']*rf)/(A['Np']*A['Ae_m2']) for lf,th,rf in itertools.product(A['Lp_factors'],A['fault_CS_threshold_table_V'],A['resistor_factors']))
# Refresh bus model without the old external startup-resistor feed; retain separate primary bleeder.
src=Path(__file__).resolve().parent.parent/'primary-buffer/calculate.py'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea'
spec=importlib.util.spec_from_file_location('bias_ucc_primary',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.A['startup_feed_R_ohm']=float('inf');p,_=m.run(m.A['time_step_s']);p=[x for x in p if x['cap_nom_F']==10e-6]
pb={k:{'min':min(x[k] for x in p),'max':max(x[k] for x in p)} for k in ['bulk_min_V','bulk_max_V','calculated_line_input_W','capacitor_LF_rms_A','true_power_factor','fundamental_displacement_factor']}
print(json.dumps({'study':'VEL-BIAS-REPAIR-01','date':'2026-11-16','assumptions':A,
 'candidate':'UCC28711DR bounded replacement, not a qualified released circuit',
 'native_source_SHA256':'762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248',
 'Lp_nom_H':lp0,'Np_Ns_ratio':n,'Na_Ns_ratio':nas,'normal_cases':len(rows),'normal_bounds':bounds,
 'normal_bias_screen_V':[min(vdd),max(vdd)],'normal_bias_headroom_to_9V_V':min(vdd)-9,
 'aux_bias_at_40V_output_plus3V_ringing_proxy':nas*(40+max(A['main_diode_V_assumed']))-min(A['aux_diode_V_assumed'])+A['aux_positive_ringing_allowance_V_assumed'],
 'bootstrap':boot,'CV_output_sensitivity_V':[min(cv),max(cv)],'OVP25_output_sensitivity_V':[min(ov),max(ov)],
 'VS_negative_current_A':[min(negative),max(negative)],'RLC_starting_sensitivity_ohm':[min(rlc),max(rlc)],
 'NTC_beta_comparison_trip_C':[min(ntc),max(ntc)],'NTC_trip_not_approved':True,
 'backup_OCP_linear_flux_T':backup,'backup_not_validated_fault_waveform':True,
 'input_overlay_cases':len(p),'input_overlay_bounds':pb,'old_external_startup_feed_removed_only_in_memory':True,
 'unresolved':'Initial 3-cycle timing; effective capacitor/diode/gate-charge bounds; actual sample/valley/ripple/fault/thermal/optical behavior; components/sourcing/insulation.',
 'no_SPICE_or_CAD_or_physical_test':True},indent=2))
