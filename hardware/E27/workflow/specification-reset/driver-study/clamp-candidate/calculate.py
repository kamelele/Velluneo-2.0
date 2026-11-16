#!/usr/bin/env python3
"""Passive bus-return RCD clamp sensitivities, not an IC or complete switched converter.
python calculate.py > results.json; requires scipy and frozen component-candidate results.
"""
from pathlib import Path
import hashlib,json,itertools,math
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
r=P.parent/'component-candidate/results.json'
assert hashlib.sha256(r.read_bytes()).hexdigest()=='d87c14c11e44aced0eabebf0346bd7d4d648f0d8fbc59fa76ebcfd18f4d60186'
b=json.loads(r.read_text())
a={'R_nom_ohm':99800,'R_factors':[.98,1.02],'C_nom_F':47e-9,'C_effective_factors_assumed':[.95*.997,1.05*1.003],
 'leakage_fraction_sensitivity':[.005,.01,.02,.05],'leakage_design_target_max':.02,
 'bus_V':[240,280,253*math.sqrt(2)],'Vo_V':[18,21,24,27],'Vd_output_V':[.5,1.2],
 'Lp_nom_H':160e-9*120**2,'Lp_factors':[.9,1.1],'Rcs_ohm':2.37,'Rcs_factors':[.99,1.01],
 'VCST_V':[.738,.780,.810],'VCCR_V':[.318,.330,.343],
 'clamp_diode_drop_V_assumed':[.7,1.7], 'extra_commutation_V_assumed':50,
 'screening_drain_target_V':700,'MOSFET_absolute_V':800,
 'R_local_ambient_C_assumed':105,'R_power_70C_W_each':1,'R_zero_power_temperature_C':155,
 'capacitor_rated_DC_V':630,'capacitor_body_temperature_C_assumed':105}

def pulse(v0,ip,L,C,R,vr,vd,T):
 # Positive u0 is required: secondary current transfers with a fixed reflected voltage.
 u=v0+vd-vr
 if u<0: return None
 z=math.sqrt(L/C);theta=math.atan2(ip*z,max(u,0));tc=math.sqrt(L*C)*theta
 if tc>=T:return None
 vp=vr-vd+math.sqrt(u*u+z*z*ip*ip)
 end=vp*math.exp(-(T-tc)/(R*C))
 q=C*(vp-v0);e=.5*C*(vp*vp-v0*v0)
 assert math.isclose(e,.5*L*ip*ip+(vr-vd)*q,rel_tol=2e-9,abs_tol=1e-12)
 return end,vp,tc,e

def steady(ip,L,C,R,vr,vd,f):
 T=1/f;low=max(vr-vd,0)+1e-8
 def g(v):return pulse(v,ip,L,C,R,vr,vd,T)[0]-v
 if g(low)<0:return None
 v0=brentq(g,low,5000,xtol=1e-9);end,vp,tc,e=pulse(v0,ip,L,C,R,vr,vd,T)
 assert abs(end-v0)<1e-6
 return dict(cap_trough_V=v0,cap_peak_V=vp,clamp_time_s=tc,
  resistor_off_interval_W=e*f,resistor_peak_W=vp*vp/R,cap_voltage_pp_V=vp-v0)
rows=[]
for v,vo,lf,rf,vc,vcr,vdo,leak,rr,cf,vd in itertools.product(a['bus_V'],a['Vo_V'],a['Lp_factors'],a['Rcs_factors'],a['VCST_V'],a['VCCR_V'],a['Vd_output_V'],a['leakage_fraction_sensitivity'],a['R_factors'],a['C_effective_factors_assumed'],a['clamp_diode_drop_V_assumed']):
 Lp=a['Lp_nom_H']*lf;ip=vc/(2.37*rf);dd=vcr/vc;vr=4*(vo+vdo);f=dd*vr/(Lp*ip)
 L=leak*Lp;R=99800*rr;C=47e-9*cf;s=steady(ip,L,C,R,vr,vd,f)
 assert s is not None
 # The charging interval omits R current. Add its maximum possible power for a conservative energy proxy.
 p_extra=s['resistor_peak_W']*s['clamp_time_s']*f
 s.update(bus_V=v,Vo_V=vo,Vd_output_V=vdo,Vd_clamp_V=vd,leakage_fraction=leak,frequency_Hz=f,Ip_A=ip,Lleak_H=L,C_F=C,R_ohm=R,
  drain_screen_V=v+s['cap_peak_V']+vd+50,
  resistor_each_average_upper_proxy_W=(s['resistor_off_interval_W']+p_extra)*.51,
  resistor_each_peak_upper_W=s['resistor_peak_W']*.51,
  capacitor_peak_dVdt_V_per_us=ip/C/1e6)
 rows.append(s)
keys=['cap_peak_V','drain_screen_V','resistor_each_average_upper_proxy_W','resistor_each_peak_upper_W','cap_voltage_pp_V','clamp_time_s','capacitor_peak_dVdt_V_per_us']
def bounds(rs):return {k:[min(x[k] for x in rs),max(x[k] for x in rs)] for k in keys}
# Fault train screen starts at an explicitly assumed precharged clamp capacitor, not zero.
bursts=[]
Lpmax=a['Lp_nom_H']*1.1;ip_fault=1.6/(2.37*.99)+max(a['bus_V'])*430e-9/(a['Lp_nom_H']*.9)
for vo,leak,f,cf in itertools.product([0,b['OVP25_sensitivity_V'][1],42],[.02,.05],[10000,33000,106000],[.95*.997,1.05*1.003]):
 C=47e-9*cf;R=99800*1.02;vr=4*(vo+1.2);v0=200.;first_target=None;first_absolute=None;maximum=0.;invalid=False
 for cycle in range(1,1001):
  s=pulse(v0,ip_fault,leak*Lpmax,C,R,vr,1.7,1/f)
  if s is None:invalid=True;break
  v0,vp,tc,e=s;drain=max(a['bus_V'])+vp+1.7+50;maximum=max(maximum,drain)
  if drain>700 and first_target is None:first_target=cycle
  if drain>800 and first_absolute is None:first_absolute=cycle
 bursts.append(dict(Vo_V_assumed=vo,leakage_fraction=leak,frequency_Hz_assumed=f,C_F=C,
  initial_clamp_V_assumed=200,Ip_fault_A_proxy=ip_fault,first_pulse_exceeding_700V_screen=first_target,
  first_pulse_exceeding_800V_in_screen=first_absolute,max_drain_over_1000_pulses_proxy_V=maximum,
  model_invalid_before_1000_pulses=invalid))
normal2=[x for x in rows if x['leakage_fraction']<=.02]
# The passive RCD comparison must also face the controller's minimum-current sampling window.
light=[]
for leak,rf,lf,cf,f,vcmin in itertools.product([.01,.02],a['R_factors'],a['Lp_factors'],a['C_effective_factors_assumed'],[600,3300,33000],[.175,.215]):
 ip=vcmin/(2.37*.99);vr=4*(b['CV_sensitivity_V'][1]+1.2)
 z=steady(ip,leak*a['Lp_nom_H']*lf,47e-9*cf,99800*rf,vr,1.7,f)
 light.append(dict(leakage_fraction=leak,f_Hz_assumed=f,Ip_A=ip,
   periodic_transfer_model_valid=z is not None,clamp_time_s=None if z is None else z['clamp_time_s'],
   below_600ns=None if z is None else z['clamp_time_s']<600e-9))
# Preferred direct diode/avalanche clamp has no separate clamp capacitor to charge at startup.
# Vc(T) scaling is deliberately a stress proxy: the manufacturer coefficient is for VBR, not full Vc(I,T).
tvs={'MPN':'Vishay SMBJ160A-E3/52','VBR25_min_V':178,'VBR25_max_V':197,'Vclamp25_max_V_at_2p3A':259,
 'temperature_coefficient_VBR_max_per_C':.00108,'Tj_sensitivity_C':[10,25,125],
 'plateau_proxy_V':[178*(1-.00108*15),259*(1+.00108*100)],
 'plateau_is_not_a_guaranteed_full_IV_temperature_curve':True,
 'local_ambient_C_assumed':85,'Tj_design_target_C_assumed':125,
 'transformer_leakage_design_target_max':.01}
tvsrows=[]
for x,vz in itertools.product(rows,[tvs['plateau_proxy_V'][0],178,197,259,tvs['plateau_proxy_V'][1]]):
 # Repeated R/C corners have no electrical role in this direct-clamp sensitivity; deduplicated below.
 vr=4*(x['Vo_V']+x['Vd_output_V']);vd=x['Vd_clamp_V'];delta=vz+vd-vr
 tc=x['Lleak_H']*x['Ip_A']/delta;e=.5*x['Lleak_H']*x['Ip_A']**2*vz/delta;power=e*x['frequency_Hz']
 tvsrows.append(dict(leakage_fraction=x['leakage_fraction'],Vz_proxy_V=vz,
  bus_V=x['bus_V'],Vo_V=x['Vo_V'],clamp_time_s=tc,power_W=power,pulse_energy_J=e,
  peak_power_W=vz*x['Ip_A'],diode_average_A=.5*x['Ip_A']*tc*x['frequency_Hz'],
  drain_screen_V=x['bus_V']+vz+vd+50,
  maximum_required_thermal_R_C_per_W=(125-85)/power))
tvsrows=list({tuple(x.items()):x for x in tvsrows}.values());tv1=[x for x in tvsrows if x['leakage_fraction']<=.01]
def tvbounds(z):return {k:[min(x[k] for x in z),max(x[k] for x in z)] for k in ['clamp_time_s','power_W','pulse_energy_J','peak_power_W','diode_average_A','drain_screen_V','maximum_required_thermal_R_C_per_W']}
# Minimum-current / no-load reset proxy independent of a claimed actual switching-frequency law.
min_reset=max(leak*a['Lp_nom_H']*1.1*(vcmin/(2.37*.99))/(tvs['plateau_proxy_V'][0]+.7-4*(vo+1.2))
 for leak,vcmin,vo in itertools.product([.01],[.175,.215],[b['CV_sensitivity_V'][1],b['OVP25_sensitivity_V'][1]]))
tvfault=[]
for vo,leak,f,vz in itertools.product([0,b['OVP25_sensitivity_V'][1],42],[.01,.02],[10000,106000],tvs['plateau_proxy_V']):
 delta=vz+.7-4*(vo+1.2);tc=leak*Lpmax*ip_fault/delta
 power=.5*leak*Lpmax*ip_fault**2*vz/delta*f
 tvfault.append(dict(Vo_assumed_V=vo,leakage_fraction=leak,frequency_Hz_assumed=f,Vz_proxy_V=vz,
  reset_time_s=tc,reset_fits_period=tc<1/f,TVS_power_during_train_W=power,
  hypothetical_max_train_duty_for_0p4W_average=min(1.,.4/power)))
# Fixed-period one-pulse map is compared against explicit RK4 including the neglected R current.
def integrate_one(v0,ip,L,C,R,vr,vd,T,dt):
 v=v0;i=ip;t=0.;vp=v0
 def rhs(v,i):return (i-v/R)/C,-(v+vd-vr)/L
 while i>0 and t<T:
  h=min(dt,T-t);k1=rhs(v,i);k2=rhs(v+h*k1[0]/2,i+h*k1[1]/2);k3=rhs(v+h*k2[0]/2,i+h*k2[1]/2);k4=rhs(v+h*k3[0],i+h*k3[1]);
  vn=v+h*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6;inn=i+h*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6
  if inn<0:
   frac=i/(i-inn);v=v+frac*(vn-v);t+=frac*h;i=0
  else:v=vn;i=inn;t+=h
  vp=max(vp,v)
 return vp,v*math.exp(-(T-t)/(R*C))
# Representative corner comparison, not a blanket proof that the approximation bounds every converter.
x=max(normal2,key=lambda x:x['drain_screen_V']);vr=4*(x['Vo_V']+x['Vd_output_V']);T=1/x['frequency_Hz'];v0=steady(x['Ip_A'],x['Lleak_H'],x['C_F'],x['R_ohm'],vr,x['Vd_clamp_V'],x['frequency_Hz'])['cap_trough_V']
rk1=integrate_one(v0,x['Ip_A'],x['Lleak_H'],x['C_F'],x['R_ohm'],vr,x['Vd_clamp_V'],T,2e-9)
rk2=integrate_one(v0,x['Ip_A'],x['Lleak_H'],x['C_F'],x['R_ohm'],vr,x['Vd_clamp_V'],T,1e-9)
print(json.dumps(dict(study='VEL-CLAMP-01',date='2026-11-16',assumptions=a,cases=len(rows),
 normal_design_target_cases=len(normal2),normal_design_target_bounds=bounds(normal2),all_sensitivity_bounds=bounds(rows),
 worst_design_target_drain_case=max(normal2,key=lambda x:x['drain_screen_V']),
 resistor_each_allowed_W_at_assumed_105C=(155-105)/(155-70),
 capacitor_catalogue_DC_rating_V=630,capacitor_tolerance_temperature_range_F=[47e-9*.95*.997,47e-9*1.05*1.003],
 fault_train_sensitivities=bursts,RCD_light_load_sensitivity=light,
 preferred_direct_clamp=tvs,TVS_normal_cases=len(tvsrows),TVS_leakage_1pct_cases=len(tv1),TVS_1pct_bounds=tvbounds(tv1),TVS_all_sensitivity_bounds=tvbounds(tvsrows),TVS_min_current_reset_proxy_max_s=min_reset,TVS_fault_train_sensitivities=tvfault,
 one_pulse_RK4_check={'analytic_peak_V':x['cap_peak_V'],'RK4_2ns_peak_V':rk1[0],'RK4_1ns_peak_V':rk2[0],
 'step_peak_difference_V':abs(rk1[0]-rk2[0]),'scope':'Representative exact-resistor pulse versus ideal charging map; no whole-converter validation'},
 startup_low_clamp_state_not_modelled=True,
 no_actual_controller_SPICE_CAD_or_physical_test=True),indent=2))
