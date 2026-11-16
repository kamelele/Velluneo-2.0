#!/usr/bin/env python3
"""Component-bound sensitivities and constructed switching-period LED/storage witness.
Not an IC model. python calculate.py > results.json; depends on frozen prior results.
"""
from pathlib import Path
import hashlib,json,itertools,math
P=Path(__file__).resolve().parent
r=P.parent/'bias-repair/results.json'
assert hashlib.sha256(r.read_bytes()).hexdigest()=='3b55eeb33d3a98eb0da91edca0c4ce45005f7866b07b0cb15e7e936a1fea6313'
b=json.loads(r.read_text());a=b['assumptions'];n=4;lp=160e-9*120**2
np_turns=120;nas=22/30;ae_min=57e-6
takeover=(9+1+1+.5)/nas-.5
icharge=b['normal_bounds']['CC_total_A']['min']-takeover/10000
cddmin=2*470e-9*.95*(1-30e-6*100)
cddmax=2*470e-9*1.05*(1+30e-6*100)
# Manufacturer independent endurance and solder limits are deliberately multiplied as a sensitivity,
# not a manufacturer guarantee for their combination or in-operation temperature behavior.
cout_initial=[8e-6,12e-6];cout_stressed=[8e-6*.7*.9*.8,12e-6*1.3*1.1*1.2]
boots=[]
for cout,draw,delay in itertools.product([12e-6,17.16e-6,cout_stressed[1]],[4.3e-3,6e-3],[0,100e-6,300e-6,1e-3,5e-3]):
 t=cout*takeover/icharge
 avail=cddmin*9
 boots.append(dict(Cout_F=cout,draw_A=draw,initial_acquisition_s_assumed=delay,charge_time_s=t,
  VDD_at_takeover_V_proxy=19-draw*(t+delay)/cddmin,charge_margin_to_10V_C=avail-draw*(t+delay)))
# Constant-current diagnostic with independently swept datasheet corners as in the parent.
rows=[]
for v,vo,lf,rf,vc,vcr,eta,vd in itertools.product(a['bus_V'],a['Vo_normal_V'],a['Lp_factors'],a['resistor_factors'],a['VCSTmax_table_V'],a['VCCR_table_V'],a['eta_transformer_assumed'],a['main_diode_V_assumed']):
 L=lp*lf;ip=vc/(2.37*rf);dd=vcr/vc;f=dd/(L*ip/(4*(vo+vd)));io=vcr*4*eta/(2*2.37*rf)
 sec=4*ip*math.sqrt(dd/3);pri=ip*math.sqrt(L*ip/v*f/3)
 # Applying lowest normal-frequency correction conservatively to the total normal switching RMS upper bound.
 factor=.65 if f<20000 else .7 if f<30000 else .75 if f<40000 else .8 if f<50000 else .85 if f<100000 else 1.
 rows.append(dict(f_Hz=f,cap_RMS_upper_A=sec,cap_ripple_utilization_50V_part=sec/(.75*factor),cap_ripple_utilization_63V_part=sec/(1.0*factor),
  normal_flux_T=L*ip/(np_turns*ae_min),MOS_conduction_25C_W=pri**2*16,MOS_hot_conduction_2p5x_proxy_W=pri**2*16*2.5))
# Refresh static auxiliary and CV/OVP endpoints for the changed auxiliary turns ratio.
vdd=[nas*(vo+vd)-vda-loss-.5 for vo,vd,vda,loss in itertools.product(a['Vo_normal_V'],a['main_diode_V_assumed'],a['aux_diode_V_assumed'],a['aux_loss_V_assumed'])]
cv=[];ov=[]
for tf,bf,vd,loss,bias in itertools.product(a['resistor_factors'],a['resistor_factors'],a['sample_diode_V_assumed'],a['aux_loss_V_assumed'],a['VS_bias_table_A']):
 top=93100*tf;bot=20500*bf;k=bot/(top+bot);rt=top*bot/(top+bot)
 for ref,temp,comp in itertools.product(a['VS_ref25_table_V'],a['Tj_sensitivity_C'],a['cable_comp_at_full_load_table_V']):
  cv.append(((ref-.0008*(temp-25)+comp+bias*rt)/k+loss)/nas-vd)
 for threshold in a['VS_OVP25_table_V']:ov.append(((threshold+bias*rt)/k+loss)/nas-vd)
# Native Cree static 25C law, already used/pinned by coupled study; switching source is constructed.
isat=9.8487e-31;N=1.5601;rs=.86341;vt=8.617333262145e-5*298.15

def ledcurrent(vc,ise,esr,nled,guess):
 i=max(guess,1e-12)
 for _ in range(9):
  vled=nled*(N*vt*math.log1p(i/isat)+rs*i)
  fun=vled*(1+esr/10000)+esr*i-vc-esr*ise
  der=nled*(N*vt/(i+isat)+rs)*(1+esr/10000)+esr
  j=i-fun/der
  i=max(j,i*.1,1e-12)
 return i

def waveform(nled,C,esr,steps):
 Itotal=.330*4*.9/(2*2.37);vo=nled*(N*vt*math.log1p(.248/isat)+rs*.248)
 ip=.78/2.37;dd=.330/.78;td=lp*ip/(4*(vo+.8));period=td/dd;dt=period/steps
 peak=2*Itotal/dd # Delivered-secondary current proxy, eta folded uniformly into amplitude.
 vc=vo;il=.248;vals=[]
 for cycle in range(40):
  vals=[]
  for k in range(steps):
   t=(k+.5)*dt;ise=peak*(1-t/td) if t<td else 0.
   il=ledcurrent(vc,ise,esr,nled,il);v=nled*(N*vt*math.log1p(il/isat)+rs*il)
   bleed=v/10000;ic=ise-il-bleed;vc+=ic*dt/C
   if cycle==39:vals.append((il,ic,v))
 return dict(nLED=nled,C_F=C,ESR_ohm_assumed=esr,frequency_Hz=1/period,
  ILED_min_A=min(x[0] for x in vals),ILED_max_A=max(x[0] for x in vals),ILED_mean_A=sum(x[0] for x in vals)/steps,
  cap_RMS_A=math.sqrt(sum(x[1]**2 for x in vals)/steps),voltage_pp_V=max(x[2] for x in vals)-min(x[2] for x in vals))
ws=[];err=0
for nl,C,esr in itertools.product([7,8],[cout_stressed[0],8e-6,10e-6,17.16e-6],[.12,.24]):
 lo=waveform(nl,C,esr,600);hi=waveform(nl,C,esr,1200);err=max(err,abs(lo['ILED_max_A']-hi['ILED_max_A']));ws.append(hi)
assert len(rows)==2592 and len(ws)==16
assert all(abs(x['ILED_mean_A']-(.330*4*.9/(2*2.37)-x['nLED']*2.93/10000))<.001 for x in ws), 'Steady-state charge balance failed'
assert err<.0005, 'Step-size sensitivity too large'
print(json.dumps(dict(study='VEL-COMPONENT-01',date='2026-11-16',
 partial_candidate_BOM={'VDD':'2x KEMET C2220C474J5GACTU, 470nF/50V/C0G/5%',
 'Cout_preferred_comparison':'Panasonic EEHZA1J100P,10uF/63V/20%,1000mA@100kHz',
 'Cout_smaller_alternative':'Panasonic EEHZA1H100R,10uF/50V/20%,750mA@100kHz',
 'Qswitch':'ST STN1NK80Z,800V,SOT223,16ohm max@10V/25C'},
 magnetics_proposal={'core_gapped':'TDK B66421U0160K187','core_ungapped':'B66421G0000X187','bobbin':'B66422W1010D001','Np':120,'Ns':30,'Na':22,'AL_H':160e-9,'Lp_H':lp,'Ae_min_m2':ae_min,'assembly_not_qualified':True},
 drain_stress_V_with_100V_assumed_overshoot=max(a['bus_V'])+4*(max(ov)+1.2)+100,
 rejected_600V_device_stress_test='Fails the 100V overshoot/OVP static screen; not selected',
 backup_flux_with_430ns_extra_ramp_proxy_T=(lp*1.1*(1.6/(2.37*.99))+max(a['bus_V'])*430e-9)/(np_turns*ae_min),
 auxiliary_takeover_V_proxy=takeover,normal_VDD_trough_proxy_V=[min(vdd),max(vdd)],CV_sensitivity_V=[min(cv),max(cv)],OVP25_sensitivity_V=[min(ov),max(ov)],
 cdd_tolerance_temperature_range_F=[cddmin,cddmax],cdd_area_body_nom_mm2=2*5.7*5,additional_VDD_capacitance_budget_F=5e-9,
 cout_initial_room_range_F=cout_initial,cout_stressed_sensitivity_F=cout_stressed,
 cout_stress_factors_not_guaranteed=[.7,.9,.8,1.3,1.1,1.2],
 budget={'IRUN_max_A':.00265,'Qg_allowance_C_assumed_at_actual_drive':12e-9,'fmax_table_Hz':106000,
 'other_bias_A_assumed':.0003,'conditional_draw_A':.00265+12e-9*106000+.0003,
 'rounded_conditional_budget_A':.0043,'Qg_table_typical_C_at_10V_only':7.7e-9},
 bootstrap_sensitivity=boots,normal_component_cases=len(rows),normal_component_bounds={k:[min(x[k] for x in rows),max(x[k] for x in rows)] for k in rows[0]},
 switching_witness_cases=ws,half_step_peak_current_difference_A=err,
 switching_source_is_constructed_not_controller_model=True,temperature_C=25,
 no_actual_SPICE_CAD_or_physical_test=True),indent=2))
