#!/usr/bin/env python3
"""TPS92310 protection/boot feasibility arithmetic; NOT a controller or fault simulation.
Run: python calculate.py > results.json
Requires sibling ../primary-buffer/calculate.py for refreshed bus-input sensitivity.
"""
from pathlib import Path
import hashlib,importlib.util,itertools,json,math

A={'Np':200,'Ns':50,'Na':48,'Ae_m2':31e-6,'Lp_H':.004,'Lp_factors':[.9,1.1],
 'normal_bus_screen_V':[240,280,253*math.sqrt(2)],'normal_output_V':[18,21,24,27],
 'Rsense_ohm':2.21,'resistor_factors':[.99,1.01],'Vref_design_V':.14,
 'diode_main_V_assumed':[.5,1.2],'diode_aux_V_assumed':[.5,1.0],
 'aux_plateau_loss_V_assumed':[0,.5],'dead_time_s':[.5e-6,1.5e-6],
 'OCP_low_V_from_table':[.59,.68],'OVP_V_from_table':[4.1,4.5],
 'ZCD_arm_V_from_table':[1.16,1.3],'ZCD_trigger_min_V_from_table':.48,
 'ZCD_input_A_sensitivity':[-1e-6,1e-6],
 'Ru_ohm':100000,'Rl_ohm':16200,
 'prop_delay_typ_s_at_test_conditions':210e-9,'extra_gate_turnoff_s_assumed':[0,100e-9],
 'Cout_nom_F':22e-6,'Cout_factors':[.8,1.2],'bleeder_output_ohm':10000,
 'CVCC_nom_F':22e-6,'CVCC_factors':[.8,1.2],
 'Rstart_nom_ohm':474000,'VCC_start_minmax_V':[23,29],'VCC_off_max_V':15.7,
 'VCC_operating_max_V':36,
 'startup_Ton_s_typ':1.5e-6,'startup_Toff_s_sensitivity':[50e-6,72e-6,94e-6],
 'startup_delivery_efficiency_assumed':[.5,.8],
 'VCC_draw_A_assumed':[.002,.003,.005],
 'post_arm_net_output_charging_W_assumed':1.0,
 'post_threshold_energy_pulses_assumed':4,
 'illustrative_output_working_ceiling_V':40,
 'working_ceiling_is_not_touch_safety_limit':True}
n=A['Np']/A['Ns'];r=A['Na']/A['Ns']

def cycle(vin,vo,lp,rs,td):
 io=A['Vref_design_V']*n/rs
 vr=n*(vo+.8)
 aa=.5*n*lp/vr;bb=-io*lp*(1/vin+1/vr);cc=-io*td
 ip=(-bb+math.sqrt(bb*bb-4*aa*cc))/(2*aa)
 ton=lp*ip/vin;off=lp*ip/vr;period=ton+off+td
 assert math.isclose(n*ip*off/(2*period),io,rel_tol=1e-12)
 return dict(primary_peak_A=ip,normal_sense_V=ip*rs,frequency_Hz=1/period,
             ton_s=ton,normal_flux_T=lp*ip/(A['Np']*A['Ae_m2']))
normal=[cycle(v,vo,A['Lp_H']*l,A['Rsense_ohm']*rf,td) for v,vo,l,rf,td in itertools.product(A['normal_bus_screen_V'],A['normal_output_V'],A['Lp_factors'],A['resistor_factors'],A['dead_time_s'])]
nb={k:{'min':min(x[k] for x in normal),'max':max(x[k] for x in normal)} for k in normal[0]}
# Independent application-note efficiency screen; don't equate this with the ideal cycle model.
eff=[]
for eta,vin,vo,vd in itertools.product([.75,.8,.9],A['normal_bus_screen_V'],A['normal_output_V'],A['diode_main_V_assumed']):
 vs=2*.14/eta*vo/(vo+vd)*(vin+n*(vo+vd))/vin
 eff.append(dict(eta_assumed=eta,vin_V=vin,vo_V=vo,vd_V=vd,normal_sense_V=vs,headroom_to_low_table_min_V=.59-vs))

fault=[]
for th,rf,l,vin,extra in itertools.product(A['OCP_low_V_from_table'],A['resistor_factors'],A['Lp_factors'],A['normal_bus_screen_V'],A['extra_gate_turnoff_s_assumed']):
 lp=A['Lp_H']*l;rs=A['Rsense_ohm']*rf
 ip=th/rs+vin/lp*(A['prop_delay_typ_s_at_test_conditions']+extra)
 fault.append(dict(trip_A=th/rs,peak_with_delay_proxy_A=ip,flux_with_delay_proxy_T=lp*ip/(A['Np']*A['Ae_m2']),energy_per_pulse_J=.5*lp*ip**2))
fb={k:{'min':min(x[k] for x in fault),'max':max(x[k] for x in fault)} for k in fault[0]}
# Divider and threshold sensitivities, raw auxiliary plateau before rectifier.
thresholds=[];node=[];arms=[];short_nodes=[]
for ufac,lfac,vd,loss,ib in itertools.product(A['resistor_factors'],A['resistor_factors'],A['diode_main_V_assumed'],A['aux_plateau_loss_V_assumed'],A['ZCD_input_A_sensitivity']):
 ru=A['Ru_ohm']*ufac;rl=A['Rl_ohm']*lfac;k=rl/(ru+rl);rt=ru*rl/(ru+rl)
 for ov in A['OVP_V_from_table']:
  thresholds.append(((ov+ib*rt)/k+loss)/r-vd)
 for av in A['ZCD_arm_V_from_table']:
  arms.append(((av+ib*rt)/k+loss)/r-vd)
 for vo in A['normal_output_V']:
  node.append(k*(r*(vo+vd)-loss)-ib*rt)
 short_nodes.append(k*(r*vd-loss)-ib*rt)
energy=fb['energy_per_pulse_J']['max']*A['post_threshold_energy_pulses_assumed']
cmin=A['Cout_nom_F']*.8
vtrip=max(thresholds)
vpost=math.sqrt(vtrip*vtrip+2*energy/cmin)
# VCC comparison from normal range, plus independent illustrative transient output voltage.
vcc=[]
for vo,vd,va,loss in itertools.product(A['normal_output_V'],A['diode_main_V_assumed'],A['diode_aux_V_assumed'],A['aux_plateau_loss_V_assumed']):vcc.append(r*(vo+vd)-loss-va)
vcc_transient_max=r*(vpost+max(A['diode_main_V_assumed']))-min(A['diode_aux_V_assumed'])

# Simplified bootstrap to ZCD arming, then assumed net output charging power until aux sustains VCC.
boot=[]
vo_arm=max(arms)
vo_takeover=(A['VCC_off_max_V']+max(A['diode_aux_V_assumed'])+max(A['aux_plateau_loss_V_assumed']))/r-min(A['diode_main_V_assumed'])
for vin,l,toff,eta,cf,draw in itertools.product(A['normal_bus_screen_V'],A['Lp_factors'],A['startup_Toff_s_sensitivity'],A['startup_delivery_efficiency_assumed'],A['Cout_factors'],A['VCC_draw_A_assumed']):
 lp=A['Lp_H']*l;co=A['Cout_nom_F']*cf
 pulse=.5*(vin*A['startup_Ton_s_typ'])**2/lp
 pdel=pulse/(A['startup_Ton_s_typ']+toff)*eta
 # Overestimate bleeder power up to arming, ignore helpful startup feed during hold-up.
 pnet=pdel-vo_arm**2/A['bleeder_output_ohm']
 tarm=.5*co*vo_arm**2/pnet
 tpost=.5*co*max(0,vo_takeover**2-vo_arm**2)/A['post_arm_net_output_charging_W_assumed']
 hold=A['CVCC_nom_F']*.8*(A['VCC_start_minmax_V'][0]-A['VCC_off_max_V'])/draw
 boot.append(dict(to_arm_s=tarm,after_arm_to_aux_s=tpost,hold_s=hold,total_to_aux_s=tarm+tpost,margin_s=hold-tarm-tpost))
# DC-fed charging comparison, not total lamp turn-on time.
rmax=A['Rstart_nom_ohm']*1.01;cmax=A['CVCC_nom_F']*1.2;veq=min(A['normal_bus_screen_V'])-14.75e-6*rmax
charge=rmax*cmax*math.log(veq/(veq-29))

# Refresh primary-buffer calculations for Rstart474k (earlier packet used680k).
source=Path(__file__).resolve().parent.parent/'primary-buffer'/'calculate.py'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea'
spec=importlib.util.spec_from_file_location('v_primary_buffer_screen',source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.A['startup_feed_R_ohm']=A['Rstart_nom_ohm']
rows,_=m.run(m.A['time_step_s'])
rows=[x for x in rows if x['cap_nom_F']==10e-6]
assert len(rows)==54
primary={k:{'min':min(x[k] for x in rows),'max':max(x[k] for x in rows)} for k in ['bulk_min_V','bulk_max_V','calculated_line_input_W','capacitor_LF_rms_A','true_power_factor','fundamental_displacement_factor']}
# Static low-Iq shunt-clamp feasibility only; tabulated test conditions are not dynamic validation.
clamp=[]
for rt,rb,ref,drift,ka_shift,iref in itertools.product([.99,1.01],[.99,1.01],[2.487,2.512],[-.034,.034],[-.07225,0],[0,.2e-6]):
 top=1.21e6*rt;bottom=100000*rb
 clamp.append((ref+drift+ka_shift)*(1+top/bottom)+iref*top)
short_demag=max(A['Lp_H']*lf*(.68/(A['Rsense_ohm']*.99)+v/(A['Lp_H']*lf)*310e-9)/(n*vd) for lf,v,vd in itertools.product(A['Lp_factors'],A['normal_bus_screen_V'],A['diode_main_V_assumed']))
print(json.dumps({'study':'VEL-PROTECTION-01','date':'2026-11-16','assumptions':A,
 'ideal_normal_cycle_cases':len(normal),'ideal_normal_cycle_bounds':nb,
 'application_note_efficiency_sensitivity':{'max_normal_sense_V':max(x['normal_sense_V'] for x in eff),'min_headroom_V':min(x['headroom_to_low_table_min_V'] for x in eff),'not_a_guaranteed_loss_or_control_model':True},
 'low_OCP_delay_proxy_bounds':fb,
 'OVP_ZCD_screen':{'trip_output_V':[min(thresholds),max(thresholds)],'normal_ZCD_V':[min(node),max(node)],
 'normal_headroom_to_min_OVP_V':min(A['OVP_V_from_table'])-max(node),
 'short_ZCD_static_range_V':[min(short_nodes),max(short_nodes)],'ringing_and_secondary_shorts_not_simulated':True,
 'assumed_post_threshold_energy_J':energy,'capacitive_post_threshold_peak_V_proxy':vpost,
 'pulse_count_is_not_guaranteed_stop_latency':True},
 'VCC_screen':{'normal_V':[min(vcc),max(vcc)],'min_headroom_to_max_UVLOoff_V':min(vcc)-A['VCC_off_max_V'],
 'proxy_after_OVP_peak_max_V':vcc_transient_max,'margin_to_36V_operating_limit_proxy':36-vcc_transient_max,
 'no_worst_case_ringing_or_clamp_validation':True},
 'bootstrap_sensitivity':{'arm_output_V_max':vo_arm,'aux_takeover_output_V_proxy':vo_takeover,
 'max_to_aux_s':max(x['total_to_aux_s'] for x in boot),'min_hold_s':min(x['hold_s'] for x in boot),'minimum_margin_s':min(x['margin_s'] for x in boot),
 'DC_0to29V_charge_s_maxRC_at240V':charge,'not_an_actual_startup_or_delay_guarantee':True},
 'additional_guard_feasibility':{'family_candidate':'ATL431B Q-temperature grade, not an ordering selection',
 'static_clamp_sensitivity_V':[min(clamp),max(clamp)],
 'divider_top_ohm':1.21e6,'divider_bottom_ohm':100000,
 'reference_KA_current_and_test_conditions_not_reproduced':True,
 'unresolved':'Current limiting versus low-normal VCC headroom; capacitor stability at >30V; turn-on dynamics, leakage, transient/average heating and single faults; no clamp release.'},
 'short_circuit_demagnetization_diagnostic_s':short_demag,
 'low_frequency_offtime_max_table_s_for_comparison':94e-6,
 'short_diagnostic_is_not_actual_CCM_fault_simulation':True,
 'output_capacitor':{'nominal_F':A['Cout_nom_F'],'cap_plus20_energy_at40V_J':.5*A['Cout_nom_F']*1.2*40**2,
 'passive_40to5V_s_Cplus20_Rplus1':A['bleeder_output_ohm']*1.01*A['Cout_nom_F']*1.2*math.log(40/5),
 'not_a_service_wait_time':True},
 'updated_primary_buffer_dependency_SHA256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'updated_primary_buffer_Rstart_ohm':A['Rstart_nom_ohm'],'updated_primary_10uF_cases':len(rows),'updated_primary_10uF_bounds':primary,
 'verification':'Arithmetic, energy/current identities and refreshed ideal bridge/CPL grid; no SPICE/actual controller/fault/physical test.'},indent=2))
