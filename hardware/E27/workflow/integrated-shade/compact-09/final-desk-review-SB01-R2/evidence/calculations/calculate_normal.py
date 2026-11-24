"""Reproducible normal-design arithmetic and a calibrated periodic CrM surrogate.
No manufacturer controller macromodel, measured waveform or compliance claim.
"""
from pathlib import Path
import math,itertools,json,hashlib
import numpy as np
H=Path(__file__).resolve().parent;ROOT=H.parents[2];P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
guard={n:sha(P/n)for n in ['SC09_compact.kicad_pcb','SC09_compact.kicad_sch','bom-build.json','hardware.json','startup-correction.SB01-R2.json']}
R5=.68;R6=3.65;rp=lambda a,b:a*b/(a+b)
Rnom=rp(R5,R6)
# Initial tolerances are sourced; TCR excursion/life/IC-temperature reserves are
# explicit engineering sensitivities, not guaranteed lifetime limits.
Rlo=rp(R5*.99*.98*.99,R6*.99*.96*.99)
Rhi=rp(R5*1.01*1.02*1.01,R6*1.01*1.04*1.01)
ipnom=.279/Rnom;ipmin=.273*.98/Rhi;ipmax=.285*1.02/Rlo
theta=(np.arange(2048)+.5)*math.pi/2048;s=np.sin(theta);shape=s**1.5
def transfer(w,rf,r,c1,c4):
 return (1+1j*w*rf*c1)/(1+1j*w*(rf*c1+(rf+r)*c4)-w*w*rf*r*c1*c4)
def periodic(vac,vo,ip,ind,rf,r,c1,c4,aux,n=128):
 # sin^1.5 gives k=3.594 rather than PI nominal3.6 before dead-zone loss.
 # This is a current-envelope scenario, not reverse-engineered IC firmware.
 pk=ip*shape;vpk=vac*math.sqrt(2);u=np.maximum(0,vpk*s-2.2)
 auxp=aux*shape/shape.mean();power=vo*pk/2+auxp
 disc=u*u-4*(rf+r)*power;b=np.where(disc>0,(u+np.sqrt(np.maximum(0,disc)))/2,0)
 active=(b>vo+1.7);pk=np.where(active,pk,0);b=np.where(active,b,u)
 duty=np.divide(vo,b,out=np.zeros_like(b),where=active);j0=pk*duty/2+np.divide(auxp,b,out=np.zeros_like(b),where=active)
 freq=np.divide(vo*(b-vo),ind*pk*b,out=np.zeros_like(b),where=active&(pk>0))
 freq=np.where(active,np.maximum(1,freq),1)
 hf_r=0.;hf_rf=0.;unfiltered=np.zeros_like(b)
 for k in range(1,n+1):
  w=2*math.pi*k;z=np.exp(-1j*w*duty)
  ck=np.divide(pk*((z-1)/(w*w)+1j*duty*z/w),duty,out=np.zeros_like(z),where=duty>0)
  var=2*np.abs(ck)**2;unfiltered+=var
  omega=2*math.pi*k*freq;h=transfer(omega,rf,r,c1,c4)
  hoff=c1/(c1+c4+1j*omega*r*c1*c4)
  # Use larger frozen-state gain (forward/open rectifier) for this scenario.
  g=np.maximum(np.abs(h),np.abs(hoff));grf=np.abs(h/(1+1j*omega*rf*c1))
  hf_r+=float(np.mean(var*g*g));hf_rf+=float(np.mean(var*grf*grf))
 var_total=pk*pk*(duty/3-duty*duty/4);tail=np.maximum(0,var_total-unfiltered).mean()
 lf=math.sqrt(float(np.mean(j0*j0)))
 # Separate LF charging-current triangle bound; avoids pretending that a
 # quasi-static model reproduces reverse blocking at the zero crossing.
 cap_r=c4*vpk*(2*math.pi*50)/math.sqrt(2);cap_rf=(c1+c4)*vpk*(2*math.pi*50)/math.sqrt(2)
 ir=math.sqrt((lf+cap_r)**2+hf_r+tail);irf=math.sqrt((lf+cap_rf)**2+hf_rf+tail)
 il2=float(np.mean(pk*pk/3));io=float(pk.mean()/2);i_rf_avg=float(j0.mean());mos2=float(np.mean(pk*pk*duty/3));diode_avg=float(np.mean(pk*(1-duty)/2))
 c6lf=float(np.mean((pk/2-io)**2));c6hf=float(np.mean(pk*pk/12))
 q=np.cumsum((pk/2-io))*(.01/len(pk));dvpp=(q.max()-q.min())/120e-6
 r7=float(np.mean(duty*(b-vo)**2+(1-duty)*(vo+1.7-2.0)**2))/390000
 lowtime=np.divide(ind*pk,b-vo,out=np.zeros_like(b),where=active)
 return {'VAC':vac,'Vout_V':vo,'Ipeak_envelope_A':ip,'L_H':ind,'RF_ohm':rf,'R10_ohm':r,'C1_F':c1,'C4_F':c4,'aux_loss_assumption_W':aux,'harmonics':n,'external_LED_current_A':io-vo/34000,'regulated_current_A':io,'R10_LF_scenario_rms_A':lf,'R10_LF_cap_triangle_bound_A':cap_r,'R10_HF_scenario_rms_A':math.sqrt(hf_r),'harmonic_tail_unfiltered_variance_A2':float(tail),'R10_RMS_planning_envelope_A':ir,'RF1_RMS_planning_envelope_A':irf,'R10_loss_W':ir*ir*r,'RF1_loss_W':irf*irf*rf,'T1_RMS_scenario_A':math.sqrt(il2),'T1_RMS_peak_all_time_upper_A':ip/math.sqrt(3),'MOS_RMS_scenario_A':math.sqrt(mos2),'MOS_conduction_100C_7R8_W':mos2*7.8,'D1_average_A':diode_avg,'D1_forward_1V7_screen_W':diode_avg*1.7,'C6_RMS_scenario_A':math.sqrt(c6lf+c6hf),'C6_100Hz_envelope_ripple_Vpp_at120u':float(dvpp),'T1_Cu_100C_screen_W':il2*2.2*(1+.00393*80),'R5_loss_W':il2*Rnom*Rnom/R5,'R6_loss_W':il2*Rnom*Rnom/R6,'R7_loss_scenario_W':r7,'R8_each_loss_W':vo*vo/68000,'bridge_forward_2V2_screen_W':i_rf_avg*2.2,'IC_BP_regulator_785uA_screen_W':float(np.mean(np.maximum(0,b-vo)*.000785*(1-duty))),'natural_CrM_frequency_max_Hz':float(freq.max()),'natural_CrM_frequency_min_active_Hz':float(freq[active].min()),'TON_min_active_us':float(lowtime[active].min()*1e6),'TON_max_active_us':float(lowtime[active].max()*1e6),'duty_max':float(duty.max()),'passes_voltage_discriminant_in_active_region':bool(np.all(disc[active]>0))}
rows=[]
for vac,vo,aux in itertools.product([207,230,253],[52,60,68],[.3,1.2]):
 rows.append(periodic(vac,vo,ipnom,.0015,47,100,47e-9,150e-9,aux))
# Deliberately combine low-L/high-current with tolerance corners, not a claim
# that temperature, bias, maximum RMS and highest voltage are simultaneous.
for vac,vo,rf,r,c1,c4 in itertools.product([207,253],[52,68],[47*.95*.98,47*1.05*1.02],[87.75,112.75],[44.65e-9,49.35e-9],[135e-9,165e-9]):
 rows.append(periodic(vac,vo,ipmax,.000972,rf,r,c1,c4,1.2))
keys=['R10_RMS_planning_envelope_A','RF1_RMS_planning_envelope_A','R10_loss_W','RF1_loss_W','T1_RMS_scenario_A','MOS_conduction_100C_7R8_W','D1_forward_1V7_screen_W','C6_RMS_scenario_A','C6_100Hz_envelope_ripple_Vpp_at120u','T1_Cu_100C_screen_W','R5_loss_W','R6_loss_W','R7_loss_scenario_W','natural_CrM_frequency_max_Hz']
maxima={k:max(x[k]for x in rows)for k in keys}
normal25={'Rpar_ohm':Rnom,'Ipeak_A':ipnom,'total_output_A':ipnom/3.6,'LED_output_A_at60V':ipnom/3.6-60/34000,'sense_25C_initial_only_Ipeak_A':[.273/(Rnom*1.01),.285/(Rnom*.99)],'extended_Rpar_ohm':[Rlo,Rhi],'extended_Ipeak_A':[ipmin,ipmax],'extended_total_output_A':[ipmin/3.6,ipmax/3.6],'extended_LED_A_52to68V':[ipmin/3.6-68/(68000*.99/2),ipmax/3.6-52/(68000*1.01/2)],'note':'3.6 is PI design equation, not a guaranteed full-temperature current. Temperature/life/ICextra2percent reserves are declared engineering sensitivities.'}
vpk=253*math.sqrt(2);minl=.0015*.8*.9*.9;ton_min=minl*ipmin/(vpk-52);lreq=1.25e-6*(vpk-52)/ipmin
stresses={'mains_crest_207_230_253_V':[x*math.sqrt(2)for x in [207,230,253]],'T1_voltage_normal_running_max_V':vpk-52,'T1_voltage_initial_output_zero_conditional_max_V':vpk,'T1_voltage_rating_V':400,'T1_Lmin_screen_H':minl,'T1_Lrequired_for_minON_H':lreq,'T1_minON_screen_us':ton_min*1e6,'T1_minON_max_limit_us':1.25,'T1_minON_margin_percent':(ton_min/1.25e-6-1)*100,'T1_Ipeak_fraction_of20CtypIsat0A8':ipmax/.8,'T1_full_triangle_RMS_upper_A':ipmax/math.sqrt(3),'T1_IR_rating_A':.52,'D1_reverse_normal_no_ringing_screen_V':vpk+1.7,'D1_VRRM_V':1000,'U1_VDS_normal_no_ringing_screen_V':vpk+1.7,'U1_VDS_absmax_V':725,'C1_voltage_normal_screen_V':vpk,'C1_rating_V':1000,'C4_voltage_normal_screen_V':vpk,'C4_rating_V':630,'C4_AC_component_of_unipolar_rectified_sine_Vrms':253*math.sqrt(1-8/math.pi**2),'C4_AC_rating_Vrms':200,'C4_dVdt_required_from_peakI_over_Cmin_V_us':ipmax/135e-9/1e6,'C4_dVdt_isolated_pulse_rating_V_us':250,'C6_DC_rating_V':100,'C6_HF_ripple_rating_A':1.4,'C6_conservative_60Hz_frequency_factor':.60,'C6_conservative_ripple_current_screen_A':1.4*.60,'R7_peak_normal_voltage_screen_V':vpk-52,'R7_working_voltage_V':1600,'R4_max_power_at2V48_andRmin_W':2.48**2/(12400*.99),'bleeder_each_W_at90V_Rmin':90**2/(68000*.99),'R10_continuous_allowable_W_if_localambient90C_linear70to200':2*(200-90)/(200-70)}
dead=2*math.asin((68+36)/(207*math.sqrt(2)))/(2*math.pi*50)
bp={'C5_nominal_F':4.7e-6,'C5_rating_V':25,'BP_supply_max_V':5.35,'BP_shunt_max_V':5.55,'BP_reset_max_V':4.65,'BP_headroom_min_V':5.075-4.65,'assumed_effective_C5_sensitivity_F':1.5e-6,'deadzone_threshold_Voutplus36_V':104,'deadzone_time_at207V_Vout68_s':dead,'typical_standby_A':180e-6,'C5_drop_with1u5_typstandby_V':180e-6*dead/1.5e-6,'required_Ceff_for_typstandby_hold_F':180e-6*dead/(5.075-4.65),'C5_typ_charge_time2mA_net180uA_to5V075_with4u7_s':4.7e-6*5.075/(.002-.00018),'limits':'No minimum startup charge current/maximum standby current or guaranteed Ceff-vsDCbias is published in the inspected tables; no hard startup-time bound. Chosen4.7uF X7R25V follows PI nominal recommendation. VerifyBPminimum/softstart at prototype; no automaticC5replacement required by this normal screen.'}
ovpmax=2.48*(1+390000*1.01/(12400*.99));ovpmin=2.3*(1+390000*.99/(12400*1.01));ovp_ext=89.486765
open_p=90*ipmax/2;single_e=.5*.0018*ipmax**2
ovp={'static_25C_1percent_range_V':[ovpmin,ovpmax],'static_nom_V':2.4*(1+390000/12400),'retained_extended_resistor_screen_high_V':ovp_ext,'one_normal_peak_pulse_energy_upper_J':single_e,'one_pulse_voltage_rise_from_extended_high_at120u_V':math.sqrt(ovp_ext**2+2*single_e/120e-6)-ovp_ext,'normal_openload_power_envelope_W_at90V':open_p,'energy_budget_delay_to100V_from_extended_high_at120u_s':.5*120e-6*(100**2-ovp_ext**2)/open_p,'limits':'Normal-current envelope only, not faultauto-restart1.24A. No maximum controller OVPdelay specified, so this quantifies required response budget rather than proving dynamicOVP/singlefault safety.'}
ovp['output_trip_initial25C_min_with_D1_1V7_V']=ovpmin-1.7
ovp['R7_R4_TCR_sensitivity']={'R7_abs_ppm_K':200,'R4_abs_ppm_K':100,'IC_min_threshold_held25C_V':2.3,'initial_resistors_percent':1,'extra_age_drift_percent':0,'D1_forward_offset_screen_V':1.7,'rows':[{'resistor_delta_abs_K':dt,'output_trip_min_V':2.3*(1+390000*.99*(1-200e-6*dt)/(12400*1.01*(1+100e-6*dt)))-1.7}for dt in [0,50,75,100]],'normal_upper_output_peak_screen_V':68+maxima['C6_100Hz_envelope_ripple_Vpp_at120u']/2,'verdict':'Initial25C clears68Vplusmodelripple. Hot/upper68V regulation remains conditional: resistor100K sensitivity overlapsripple, IC hot OVP threshold unspecified, diode1.7V is25C1A screen not guaranteed alltemp bound. No narrowing loadwindow or relaxing90Vstop; measure actual OVP and68V load atcorners. Legacy69.371V no-diode screen is not a guaranteedhot threshold.'}
controlling=max(rows,key=lambda x:x['R10_loss_W']);fine=periodic(controlling['VAC'],controlling['Vout_V'],controlling['Ipeak_envelope_A'],controlling['L_H'],controlling['RF_ohm'],controlling['R10_ohm'],controlling['C1_F'],controlling['C4_F'],controlling['aux_loss_assumption_W'],256)
result={'actor':'/root/r2_normal_calcs','date':'2026-11-24','base_commit':'872adddb3da9b3dbfa57e5c81ef7ba51da2a841c','source_guards':guard,'normal_current':normal25,'normal_stress_screens':stresses,'BP_startup_sensitivity':bp,'OVP_response_budget':ovp,'periodic_model':{'kind':'Calibrated quasi-static line/CrM Fourier current surrogate, NOT a manufacturerICmacromodel or observed periodic waveform','assumptions':['Rectifiedsine after2.2Vbridge drop; idealbuck triangular switching current; sin^1.5 peak envelope approximatesPIk3.6. Actual LYTSwitch control will differ.','Vo52/60/68V; Ipeakfromselectedsense network; auxiliaryloss.3or1.2W assumed atfilteredbus to budgetnormalconverterloss and boostinputcurrent.','HFfiltertransfer with forward and open bridgefrozenstates; useperharmoniclargerR10gain. This is not a globalnonlinearrectifierbound.','LFcapacitivecharging via explicit normtriangle addition; no fake zero-crossing waveform. Fouriertailconservativelyunfiltered because RCgain<=1.','L.972mHlow sensitivity combines20percenttolerance andtwo10percenthot/biasfactors. No guaranteedhotLcurve; measurementlater.','No forcedminfrequency,burst,softstart,OC/OVP,parasiticringing,dielectric,thermalorEMCphysicalmacromodel. NaturalCrMnearvalleytiming outsidecontrollerlimits is diagnostic,notclaimICviolatesitsownlimits.'],'case_count':len(rows),'maxima':maxima,'nominal_230V60V_aux1p2':next(x for x in rows if x['VAC']==230 and x['Vout_V']==60 and x['aux_loss_assumption_W']==1.2 and x['R10_ohm']==100),'harmonic_convergence_controlling_128vs256':{'coarse_R10_W':controlling['R10_loss_W'],'fine_R10_W':fine['R10_loss_W'],'delta_W':fine['R10_loss_W']-controlling['R10_loss_W']},'rows':rows},'canonical_sources_unchanged':all(sha(P/n)==v for n,v in guard.items()),'physical_measurements_performed':False,'human_approval':False}
losskeys=['R10_loss_W','RF1_loss_W','MOS_conduction_100C_7R8_W','D1_forward_1V7_screen_W','T1_Cu_100C_screen_W','R5_loss_W','R6_loss_W','R7_loss_scenario_W','bridge_forward_2V2_screen_W','IC_BP_regulator_785uA_screen_W']
partloss=lambda row:sum(row[k] for k in losskeys)+2*row['R8_each_loss_W']
nom=result['periodic_model']['nominal_230V60V_aux1p2'];nomloss=partloss(nom);ledpower=60*nom['external_LED_current_A']
result['loss_and_thermal_budget']={'nominal_component_loss_screen_W':nomloss,'all_scenario_component_loss_screen_W':[min(map(partloss,rows)),max(map(partloss,rows))],'additional_core_switch_dielectric_loss_planning_W':[.15,.6],'nominal_total_driver_loss_planning_W':[nomloss+.15,nomloss+.6],'nominal_external_LED_power_model_W':ledpower,'nominal_efficiency_planning_fraction':[ledpower/(ledpower+nomloss+.6),ledpower/(ledpower+nomloss+.15)],'T1_copper_only_temperature_rise_scaled_from_IR40K_K':40*(maxima['T1_RMS_scenario_A']/.52)**2,'limits':'Core/switching/dielectric additions are explicit planning assumptions, not guaranteed/calibrated losses. Auxiliary loss in RC model boosts input current; do not add it again to the component loss budget. No resistor/junction temperature forecast without actual thermal boundary conditions. T1 copper-only scaling omits core loss, adjacent heat and enclosed ambient.'}
(H/'normal-calculations.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'normal_current':normal25,'stress':stresses,'periodic_maxima':maxima,'BP':bp,'OVP':ovp,'convergence':result['periodic_model']['harmonic_convergence_controlling_128vs256']},indent=2))
