#!/usr/bin/env python3
"""Integrated charge/sampling feasibility with explicit acquisition hypotheses.
Not an IC or switched-converter simulation. Requires canonical sibling results.
"""
from pathlib import Path
import hashlib,json,itertools,math
from scipy.integrate import quad
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
for folder,digest in [('component-candidate','d87c14c11e44aced0eabebf0346bd7d4d648f0d8fbc59fa76ebcfd18f4d60186'),('clamp-candidate','29827b4ef38f66a4f11dde07d7410c1170753ebc86767e94fa52af6624690bcc')]:
 f=P.parent/folder/'results.json';assert hashlib.sha256(f.read_bytes()).hexdigest()==digest
 if folder=='component-candidate':component=json.loads(f.read_text())
 else:clamp=json.loads(f.read_text())
A={'Np':120,'Ns':30,'Na':22,'Lp_H':2.304e-3,'Lp_factors':[.9,1.1],
 'Rcs_ohm':2.37,'Rcs_factors':[.99,1.01],'VCCR_V':[.318,.343],'VCSTmax_V':[.738,.810],
 'Cdd_min_F':.890321e-6,'Cdd_max_F':.989961e-6,'VDD_on_min_V':19,'VDD_target_trough_V':10,
 'Vout_main_diode_min_V':.5,'Vout_main_diode_max_V':1.2,'aux_diode_max_V':1.,
 'aux_winding_loss_assumed_V':.5,'aux_ripple_allowance_assumed_V':.5,
 'Cout_F':[4.032e-6,12e-6,17.16e-6,20.592e-6],'Cout_ESR_assumed_ohm':[0,.24],
 'nLED':[7,8],'LED_voltage_shift_per_diode_assumed_V':[0,-.3],
 'Qg_actual_drive_budget_assumed_C':[12e-9,16e-9],
 'base_VDD_draw_assumed_A':[.00295,.0035],
 'base_budget_includes_0p3mA_allowance':True,'IRUN_source_2p65mA_test_VDD_V':25,
 'first3_time_s_assumed':[.3e-3,.6e-3,1e-3,1.5e-3],
 'post3_settling_s_assumed':.1e-3,'settling_f_Hz_assumed':106000,
 'LED25_model':{'Is_A':9.8487e-31,'N':1.5601,'Rs_ohm':.86341,'T_K':298.15},
 'RS1_proposed_ohm':80600,'RS2_proposed_ohm':17400,'divider_envelope_factors':[.979,1.021],
 'RLC_proposed_ohm':1400,'RLC_total_delay_s_assumed':[100e-9,150e-9],
 'pin_capacitance_sensitivity_F':[2e-12,5e-12,10e-12,15e-12],
 'VS_initial_error_assumed_V':1.,'VS_final_error_target_V':.1,
 'combined_reset_engineering_budget_s':600e-9,'other_recovery_allocation_s_assumed':100e-9,
 'charge_current_fraction_assumed':[.5,.75,1.],
 'Qoss_typ_only_at_640V_C':9.5e-12*640}
n=4;nas=22/30;npa=120/22
v_take=(10+1+.5+.5)/nas-.5
icc=.318*4*.85/(2*2.37*1.01)
assert abs(icc-.22584283744830178)<1e-12
fcoef=max(vcr*n*2.37*rf/(2.304e-3*lf*vc*vc) for vcr,rf,lf,vc in itertools.product(A['VCCR_V'],A['Rcs_factors'],A['Lp_factors'],A['VCSTmax_V']))
N=1.5601;vt=8.617333262145e-5*298.15;isat=9.8487e-31;rs=.86341

def led(v,nled,shift):
 def residual(i):return nled*(N*vt*math.log1p(i/isat)+rs*i+shift)-v
 if residual(1e-16)>0:return 0.
 return brentq(residual,1e-16,.48,xtol=1e-15)

rows=[]
for cap,esr,nled,shift,qgate,base in itertools.product(A['Cout_F'],A['Cout_ESR_assumed_ohm'],A['nLED'],A['LED_voltage_shift_per_diode_assumed_V'],A['Qg_actual_drive_budget_assumed_C'],A['base_VDD_draw_assumed_A']):
 def net_at_vo(v):return icc-led(v,nled,shift)-v/10000
 net_take=net_at_vo(v_take);assert net_take>0
 vc_target=v_take-esr*net_take
 def values(vc):
  if esr==0:v=vc
  else:v=brentq(lambda vv:vv-vc-esr*net_at_vo(vv),vc,vc+esr*icc,xtol=1e-12)
  current=net_at_vo(v)
  assert current>0
  f=fcoef*(v+1.2)
  assert f<106000
  return current,f
 t=quad(lambda v:cap/values(v)[0],0,vc_target,epsabs=1e-12)[0]
 q_ramp=quad(lambda v:(base+qgate*values(v)[1])*cap/values(v)[0],0,vc_target,epsabs=1e-13)[0]
 q_settle=.0001*(base+qgate*106000);q_first3=3*qgate;avail=.890321e-6*9
 max_first3=(avail-q_ramp-q_settle-q_first3)/base
 scenarios={str(t3):19-(base*t3+q_first3+q_settle+q_ramp)/.890321e-6 for t3 in A['first3_time_s_assumed']}
 rows.append(dict(Cout_F=cap,ESR_assumed_ohm=esr,nLED=nled,LED_shift_assumed_V=shift,Qg_assumed_C=qgate,
  base_draw_assumed_A=base,charge_time_s=t,Vout_takeover_trough_target_V=v_take,
  LED_current_at_takeover_A=led(v_take,nled,shift),ramp_gate_frequency_max_envelope_Hz=fcoef*(v_take+1.2),
  VDD_charge_ramp_C=q_ramp,post3_settling_charge_C=q_settle,first3_gate_charge_C=q_first3,
  max_first3_time_s_proxy=max_first3,VDD_at_takeover_scenarios_V=scenarios,
  old_constant_6mA_remaining_time_s_proxy=(avail/.006)-t))
# Refresh auxiliary-sampling divider, static CV/OVP and VS negative current for proposed values.
def divider(r1,r2):
 cv=[];ov=[];negative=[];rths=[]
 for tf,bf,vd,loss,bias in itertools.product(A['divider_envelope_factors'],A['divider_envelope_factors'],[.3,.8],[0,.5],[-.25e-6,.25e-6]):
  top=r1*tf;bottom=r2*bf;k=bottom/(top+bottom);rt=top*bottom/(top+bottom);rths.append(rt)
  for ref,T,comp in itertools.product([4.01,4.09],[-40,25,125],[-.055,.025]):
   cv.append(((ref-.0008*(T-25)+comp+bias*rt)/k+loss)/nas-vd)
  for threshold in [4.55,4.71]:ov.append(((threshold+bias*rt)/k+loss)/nas-vd)
  for bus in [240,253*math.sqrt(2),400]:negative.append((bus,bus/npa/top))
 return cv,ov,negative,rths
cv,ov,negative,rths=divider(A['RS1_proposed_ohm'],A['RS2_proposed_ohm'])
oldcv,oldov,oldnegative,oldrths=divider(93100,20500)
imin=.175/(2.37*1.01);imaxmin=.215/(2.37*.99)
min_vz=clamp['preferred_direct_clamp']['plateau_proxy_V'][0]
treset=(.01*2.304e-3*1.1*imaxmin)/(min_vz+.7-4*(max(ov)+1.2))
assert treset>0
qbudgets=[dict(mean_current_fraction_assumed=g,Q_node_budget_C=g*imin*(600e-9-100e-9-treset),
 remaining_after_typical_Qoss_C=g*imin*(600e-9-100e-9-treset)-A['Qoss_typ_only_at_640V_C']) for g in A['charge_current_fraction_assumed']]
tdemag_min=2.304e-3*.9*imin/(4*(max(cv)+1.2))
# Conservative combined600ns allocation +200ns final settling guard, not the exact vendor tLK interval definition.
settle_available=tdemag_min-600e-9-200e-9
pins=[]
for cp in A['pin_capacitance_sensitivity_F']:
 pins.append(dict(Cpin_F_assumed=cp,settle_to_0p1V_s=max(rths)*cp*math.log(10),available_s=settle_available,
  within_combined_allocation=max(rths)*cp*math.log(10)<=settle_available))
rlcs=[k*80600*2.37*td*npa/2.304e-3 for k,td in itertools.product([24,25,28.6],[100e-9,150e-9])]
keys=['charge_time_s','LED_current_at_takeover_A','VDD_charge_ramp_C','max_first3_time_s_proxy']
nom=[x for x in rows if x['Qg_assumed_C']==12e-9 and x['base_draw_assumed_A']==.00295]
print(json.dumps(dict(study='VEL-STARTUP-01',date='2026-11-16',assumptions=A,cases=len(rows),
 charging_bounds={k:[min(x[k] for x in rows),max(x[k] for x in rows)] for k in keys},
 main_budget_min_first3_time_s=min(x['max_first3_time_s_proxy'] for x in nom),
 all_sensitivity_min_first3_time_s=min(x['max_first3_time_s_proxy'] for x in rows),
 first3_0p3ms_worst_VDD_V=min(x['VDD_at_takeover_scenarios_V']['0.0003'] for x in rows),
 main_budget_first3_1ms_worst_VDD_V=min(x['VDD_at_takeover_scenarios_V']['0.001'] for x in nom),
 worst_startup_case=min(rows,key=lambda x:x['max_first3_time_s_proxy']),
 proposed_divider={'RS1_ohm':80600,'RS2_ohm':17400,'RLC_ohm':1400,'CV_sensitivity_V':[min(cv),max(cv)],
  'OVP25_sensitivity_V':[min(ov),max(ov)],'Rth_ohm':[min(rths),max(rths)],
  'negative_VS_current_high_line_max_A':max(i for v,i in negative if v<400),
  'negative_VS_current_at_400V_max_A':max(i for v,i in negative if v==400),
  'line_run_rms_sensitivity_V':[80600*f*npa*i/math.sqrt(2) for f,i in itertools.product(A['divider_envelope_factors'],[190e-6,275e-6])],
  'RLC_delay_sensitivity_ohm':[min(rlcs),max(rlcs)]},
 clamp_reset_proxy_with_new_OVP_s=treset,minimum_primary_current_A=imin,node_charge_allocations=qbudgets,
 minimum_demag_s=tdemag_min,pin_capacitance_settling_sensitivity=pins,
 max_pin_capacitance_for_combined_allocation_F=settle_available/(max(rths)*math.log(10)),
 scenario_min_VDD_V={str(t):min(x['VDD_at_takeover_scenarios_V'][str(t)] for x in rows) for t in A['first3_time_s_assumed']},
 main_budget_worst_case=min(nom,key=lambda x:x['max_first3_time_s_proxy']),
 old_divider_same_envelope={'RS1_ohm':93100,'RS2_ohm':20500,'CV_sensitivity_V':[min(oldcv),max(oldcv)],'OVP25_sensitivity_V':[min(oldov),max(oldov)],'Rth_max_ohm':max(oldrths),'max_pin_capacitance_same_allocation_F':(2.304e-3*.9*imin/(4*(max(oldcv)+1.2))-800e-9)/(max(oldrths)*math.log(10))},
 no_valid_controller_or_full_circuit_SPICE_or_physical_test=True),indent=2))
