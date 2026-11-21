#!/usr/bin/env python3
"""Bounded support-component arithmetic; not controller/thermal/physical validation."""
from pathlib import Path
import hashlib,json,itertools,math
from scipy.integrate import quad
from scipy.optimize import brentq
import argparse
pa=argparse.ArgumentParser();pa.add_argument('--driver-study',required=True);pa.add_argument('--crcw-pdf',required=True);pa.add_argument('--ucc-pdf',required=True);args=pa.parse_args()
root=Path(args.driver_study).resolve()
inputs={
 'startup-candidate/results.json':'267db0de602050e9f014e332e578d9cda85d450a7c67bdc918f15cbf8788a8ed',
 'clamp-candidate/results.json':'29827b4ef38f66a4f11dde07d7410c1170753ebc86767e94fa52af6624690bcc',
 'component-candidate/results.json':'d87c14c11e44aced0eabebf0346bd7d4d648f0d8fbc59fa76ebcfd18f4d60186',
 'native/CRCW.pdf':'773514dbb68319dd7a3b8d381a81798f8bb0a82cf65ecf440ec201dad810e7c5',
 'native/UCC2871x.pdf':'762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248'}
paths={n:root/n for n in inputs};paths['native/CRCW.pdf']=Path(args.crcw_pdf);paths['native/UCC2871x.pdf']=Path(args.ucc_pdf)
for n,h in inputs.items():assert hashlib.sha256(paths[n].read_bytes()).hexdigest()==h,n
#1%initial +100ppm/K over25->125C rounded outward to2.1%; not an ageing bound.
factors=[.979,1.021];Rcs=2.37
rows=[]
for bus,vo,lf,rf,vcs,vcc,eta,vd in itertools.product([240,253*math.sqrt(2)],[18,27],[.9,1.1],factors,[.738,.810],[.318,.343],[.85,.95],[.5,1.2]):
 lp=.002304*lf;rs=Rcs*rf;ip=vcs/rs;dd=vcc/vcs;td=lp*ip/(4*(vo+vd));f=dd/td;ton=lp*ip/bus;irms=ip*math.sqrt(ton*f/3)
 rows.append(dict(primary_peak_A=ip,primary_rms_A=irms,Rcs_loss_W=irms*irms*rs,CC_A=vcc*4*eta/(2*rs),normal_flux_T=lp*ip/(120*57e-6),f_Hz=f,demag_duty=dd,idle_s=1/f-ton-td))
normal={k:[min(x[k] for x in rows),max(x[k] for x in rows)] for k in rows[0]}
rg=4.7;rgs=47000;raux=4.7;vg=16;freq=106000;qg=16e-9;anc=.00055;ntc=.000125;igs=.000010
rgsmin=rgs*.979;rgsmax=rgs*1.021
bias_static=vg/rgsmin+ntc+igs
full_draw=.0035+qg*freq
auxpeak=normal['primary_peak_A'][1]*120/22
rauxmax=raux*1.021
ravgdraw=full_draw
reserve=.30;conduct_duty_min=rauxmax*ravgdraw/reserve
#Native25V table conditions and16nC hypotheses, not drive/model guarantees.
gate={'RG_ohm':rg,'RGS_ohm':rgs,'gate_supply_V_hypothesis':vg,'RGS_current_max_A_proxy':vg/rgsmin,'NTC_current_A_source_max':ntc,'IGSS_abs_A_source_max':igs,'IGSS_test_conditions':'VDS0/VGS+-20V; does not guarantee off-state gate current with high drain bias or Miller injection','allocated_ancillary_total_A':bias_static,'remaining_of0p55mA_A':anc-bias_static,'gate_leakage_times_RGSmax_V':igs*rgsmax,'gate_path_entire_cycle_energy_to_RG_W_proxy':vg*qg*freq,'RG_external_only_peak_sink_A_proxy':vg/(rg*.979),'not_actual_gate_transient_or_sink_rating':True}
aux={'RAUX_ohm':raux,'base_plus_gate_budget_A':full_draw,'reflected_primary_normal_peak_A_proxy':auxpeak,'R_loss_bound_if_peak_and_average_bounds_valid_W':rauxmax*full_draw*auxpeak,'additional_voltage_reserve_V_assumed':reserve,'minimum_aux_conduction_fraction_required_by_average_current':conduct_duty_min,'not_guaranteed_actual_conduction_window_or_bias_waveform':True}
bleed=[]
for v in [27,37.861,40,63]:
 bleed.append(dict(voltage_V_example=v,each_20k_bleeder_P_W_atRmin=v*v/(20000*.979),total_both_P_W_atRmin=2*v*v/(20000*.979)))
linecomp=[]
for bus,lf,rf,topf,rlcf,k,delay in itertools.product([240,253*math.sqrt(2)],[.9,1.1],factors,factors,factors,[24,28.6],[100e-9,150e-9]):
 lp=.002304*lf;rs=2.37*rf;rt=80600*topf;rlc=1400*rlcf;npa=120/22
 tc=rlc*lp/(k*rt*rs*npa);delta=bus*(delay/lp-rlc/(k*rt*rs*npa))
 linecomp.append(dict(equivalent_compensation_delay_s=tc,residual_peak_current_error_A=delta))
linecomp_bounds={k:[min(x[k] for x in linecomp),max(x[k] for x in linecomp)] for k in linecomp[0]}
# Correlated correction witness: all line-comp corners applied to the SAME normal sample.
correlated=[]
for bus,vo,lf,rf,vcs,vcc,eta,vd,topf,rlcf,k,delay in itertools.product([240,253*math.sqrt(2)],[18,27],[.9,1.1],factors,[.738,.810],[.318,.343],[.85,.95],[.5,1.2],factors,factors,[24,28.6],[100e-9,150e-9]):
 lp=.002304*lf;rs=2.37*rf;rt=80600*topf;rlc=1400*rlcf;npa=120/22
 delta=bus*(delay/lp-rlc/(k*rt*rs*npa));ip=vcs/rs+delta
 assert ip>0
 dd=vcc/vcs;td=lp*ip/(4*(vo+vd));f=dd/td;ton=lp*ip/bus;idle=1/f-ton-td
 assert idle>0
 irms=ip*math.sqrt(ton*f/3)
 correlated.append(dict(bus_V=bus,Vo_V=vo,Lp_H=lp,Rcs_ohm=rs,RS1_ohm=rt,RLC_ohm=rlc,KLC=k,delay_s_assumed=delay,VCST_V=vcs,VCCR_V=vcc,transformer_efficiency_assumed=eta,Vd_V_assumed=vd,residual_peak_A=delta,corrected_peak_A=ip,normal_flux_T=lp*ip/(120*57e-6),primary_RMS_A=irms,Rcs_loss_W=irms*irms*rs,MOS_conduction16ohm25C_W_proxy=irms*irms*16,corrected_CC_A_proxy=.5*4*ip*dd*eta,f_Hz=f,idle_s=idle,secondary_peak_A_proxy=4*ip,secondary_RMS_A_proxy=4*ip*math.sqrt(dd/3),all_current_aux_peak_A_proxy=ip*120/22))
corrkeys=['corrected_peak_A','normal_flux_T','primary_RMS_A','Rcs_loss_W','MOS_conduction16ohm25C_W_proxy','corrected_CC_A_proxy','f_Hz','idle_s','secondary_peak_A_proxy','secondary_RMS_A_proxy','all_current_aux_peak_A_proxy']
corrsummary={'cases':len(correlated),'fixed_dmag_ratio_VCCR_div_VCST_is_a_constructed_hypothesis_not_actual_IC_law':True,'bounds':{k:[min(x[k] for x in correlated),max(x[k] for x in correlated)] for k in corrkeys},'max_peak_case':max(correlated,key=lambda x:x['corrected_peak_A']),'max_flux_case':max(correlated,key=lambda x:x['normal_flux_T']),'max_Rcs_heat_case':max(correlated,key=lambda x:x['Rcs_loss_W'])}
aux['correlated_reflected_peak_A_proxy']=corrsummary['bounds']['all_current_aux_peak_A_proxy'][1]
aux['correlated_peak_and_mean_heat_proxy_W']=rauxmax*full_draw*aux['correlated_reflected_peak_A_proxy']
# Reuse the prior constant-avalanche direct-clamp sensitivities for correlated NORMAL currents only.
# These plateaus are explicitly not a guaranteed hot I-V curve.
clamp_input=json.loads((root/'clamp-candidate/results.json').read_text())
clamp_rows=[]
for x,vz,vdclamp in itertools.product(correlated,[clamp_input['preferred_direct_clamp']['plateau_proxy_V'][0],178,197,259,clamp_input['preferred_direct_clamp']['plateau_proxy_V'][1]],[.7,1.7]):
 vr=4*(x['Vo_V']+x['Vd_V_assumed']);delta=vz+vdclamp-vr
 le=.01*x['Lp_H'];ip=x['corrected_peak_A'];f=x['f_Hz']
 energy=.5*le*ip*ip*vz/delta
 clamp_rows.append(dict(clamp_initial_current_A_proxy=ip,TVS_power_W_proxy=energy*f,TVS_pulse_energy_J_proxy=energy,TVS_peak_power_W_proxy=vz*ip,reset_s_proxy=le*ip/delta,drain_endpoint_V_proxy=x['bus_V']+vz+vdclamp+50))
clampsummary={'cases':len(clamp_rows),'leakage_fraction_assumed':.01,'inherited_plateau_not_guaranteed_hot_IV':True,'plus50V_commutation_is_assumed':True,'normal_only_not_fault_or_surge':True,'bounds':{k:[min(x[k] for x in clamp_rows),max(x[k] for x in clamp_rows)] for k in clamp_rows[0]}}
output={'parallel_resistors_ohm':[20000,20000],'R_normal_max_ohm':10000*1.021,'R_after_one_open_max_ohm':20000*1.021,'Cout_max_sensitivity_F':20.592e-6,'dissipation_examples':bleed,'discharge_after_all_energy_transfer_stops_s':{str(v):{'both_to5V':10000*1.021*20.592e-6*math.log(v/5),'one_open_to5V':20000*1.021*20.592e-6*math.log(v/5)} for v in [40,63]},'example5V_is_not_safe_access_acceptance':True,'primary_bulk_can_continue_transferring_energy_after_unscrew':True,'one_short_becomes_short_output_fault':True}
#Refreshed existing coupled analytical ramp with sense-temperature allowance + extra0.3V RAUX allocation.
icc=.318*4*.85/(2*2.37*1.021);take=(10+1+.5+.5+reserve)/(22/30)-.5
fcoef=max(vcr*4*2.37*rf/(.002304*lf*vcs*vcs) for vcr,rf,lf,vcs in itertools.product([.318,.343],factors,[.9,1.1],[.738,.810]))
N=1.5601;vt=8.617333262145e-5*298.15;isat=9.8487e-31;rl=.86341

def led(v,n,shift):
 def fun(i):return n*(N*vt*math.log1p(i/isat)+rl*i+shift)-v
 return 0 if fun(1e-16)>0 else brentq(fun,1e-16,.48,xtol=1e-15)
startup=[]
for cap,esr,n,shift,qgate,base in itertools.product([4.032e-6,12e-6,17.16e-6,20.592e-6],[0,.24],[7,8],[0,-.3],[12e-9,16e-9],[.00320,.0035]):
 def cur(v):return icc-led(v,n,shift)-v/(10000*.979)
 target=take-esr*cur(take)
 def vals(vc):
  v=vc if esr==0 else brentq(lambda v:v-vc-esr*cur(v),vc,vc+esr*icc,xtol=1e-12)
  return cur(v),fcoef*(v+1.2)
 time=quad(lambda v:cap/vals(v)[0],0,target,epsabs=1e-12)[0]
 charge=quad(lambda v:(base+qgate*vals(v)[1])*cap/vals(v)[0],0,target,epsabs=1e-13)[0]
 settle=.0001*(base+qgate*106000);gate3=3*qgate
 limit=(.890321e-6*9-charge-settle-gate3)/base
 startup.append(dict(Cout_F=cap,ESR_ohm_assumed=esr,nLED=n,LED_shift_V_assumed=shift,Qg_C_assumed=qgate,base_draw_A_assumed=base,ramp_time_s=time,ramp_charge_C=charge,max_first3_allrun_time_s_proxy=limit,VDD_takeover_if0p3ms_V=19-(base*.0003+charge+settle+gate3)/.890321e-6))
main=[x for x in startup if x['Qg_C_assumed']==12e-9 and x['base_draw_A_assumed']==.00320]
r={'study':'SUPPORT-CANDIDATE-01','date':'2026-11-17','inputs_SHA256':inputs,'resistor_temperature_screen_factor':factors,'not_ageing_or_measured_limits':True,'normal_cases':len(rows),'normal_sense_temperature_bounds':normal,'gate':gate,'line_compensation_conditional_bounds':linecomp_bounds,'correlated_normal_linecomp_witness':corrsummary,'correlated_normal_directclamp_proxy':clampsummary,'aux':aux,'output_bleed':output,'source_resistor_derated_power_at125C_W':{'gate0805_conservative0p125W_at70C':.125*(155-125)/(155-70),'sense1206_0p25W_at70C':.25*(155-125)/(155-70),'2512_1W_at70C':1*(155-125)/(155-70)},'startup_cases':len(startup),'aux_takeover_output_target_V_proxy':take,'main_min_first3_time_s_proxy':min(x['max_first3_allrun_time_s_proxy'] for x in main),'stress_min_first3_time_s_proxy':min(x['max_first3_allrun_time_s_proxy'] for x in startup),'worst_VDD_takeover_if0p3ms_V':min(x['VDD_takeover_if0p3ms_V'] for x in startup),'worst_startup_case':min(startup,key=lambda x:x['max_first3_allrun_time_s_proxy']),'no_controller_model_physical_measurement_or_stage_approval':True}
print(json.dumps(r,indent=2))
