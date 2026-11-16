#!/usr/bin/env python3
"""Ideal 50Hz bridge/bulk-input screen with finite series resistance.
Run: python calculate.py --verify-halved-step > results.json
Not a switching-controller/startup/fault/EMC simulation. Requires numpy.
"""
import argparse, itertools, json, math
import numpy as np

A={'vac_rms_V':[207,230,253],'line_Hz':50,
 'cap_nom_F':[4.7e-6,6.8e-6,10e-6,15e-6],'cap_factors':[.8,1.2],
 'remaining_constant_bus_load_W':[6,8,10],
 'lumped_input_series_R_ohm':[10,22,47],
 'bridge_total_fixed_drop_V':1.6,
 'dedicated_primary_bleeder_R_ohm':1e6,
 'startup_feed_R_ohm':680000,'startup_VCC_assumed_V':18.3,
 'time_step_s':2e-6,'settling_half_cycles':20,
 'bulk_voltage_comparison_floor_V':200,
 'discharge_resistor_tolerance':.01,
 'discharge_example_thresholds_V':[60,30],
 'thresholds_are_not_safe_access_limits':True}
cases=[dict(vac_rms_V=v,cap_nom_F=c,cap_factor=ct,remaining_bus_load_W=p,series_R_ohm=r)
 for v,c,ct,p,r in itertools.product(A['vac_rms_V'],A['cap_nom_F'],A['cap_factors'],A['remaining_constant_bus_load_W'],A['lumped_input_series_R_ohm'])]
vac=np.array([c['vac_rms_V'] for c in cases]);vp=vac*math.sqrt(2)
cap=np.array([c['cap_nom_F']*c['cap_factor'] for c in cases])
p=np.array([c['remaining_bus_load_W'] for c in cases]);rs=np.array([c['series_R_ohm'] for c in cases])
period=1/(2*A['line_Hz'])

def run(dt):
 steps=round(period/dt);dt=period/steps
 e=.5*cap*(vp-A['bridge_total_fixed_drop_V'])**2
 size=len(cases)
 sum_vin_i=np.zeros(size);sum_i2=np.zeros(size);sum_ir2=np.zeros(size);sum_bridge=np.zeros(size)
 sum_start=np.zeros(size);sum_bleed=np.zeros(size);sum_ic2=np.zeros(size)
 sum_sin_i=np.zeros(size);sum_cos_i=np.zeros(size)
 vmin=np.full(size,np.inf);vmax=np.zeros(size);ipeak=np.zeros(size);records=[]
 def state(t,energy):
  if np.any(energy<=0):raise ValueError('CPL model collapsed; actual UVLO/startup not modeled')
  v=np.sqrt(2*energy/cap)
  vin=vp*math.sin(math.pi*t/period)
  ich=np.maximum(0,(vin-A['bridge_total_fixed_drop_V']-v)/rs)
  ib=v/A['dedicated_primary_bleeder_R_ohm']
  istart=np.maximum(0,(v-A['startup_VCC_assumed_V'])/A['startup_feed_R_ohm'])
  ic=ich-p/v-ib-istart
  return v,vin,ich,ib,istart,ic
 def rhs(t,energy):
  v,vin,ich,ib,istart,ic=state(t,energy)
  return v*ic,(v,vin,ich,ib,istart,ic)
 for step in range(steps*A['settling_half_cycles']):
  t=(step%steps)*dt
  if step==steps*(A['settling_half_cycles']-1):e_start=e.copy()
  k1,s1=rhs(t,e);k2,s2=rhs(t+dt/2,e+dt*k1/2)
  k3,s3=rhs(t+dt/2,e+dt*k2/2);k4,s4=rhs(t+dt,e+dt*k3)
  e+=dt*(k1+2*k2+2*k3+k4)/6
  if step>=steps*(A['settling_half_cycles']-1):
   for weight,phase,s in [(1,t,s1),(2,t+dt/2,s2),(2,t+dt/2,s3),(1,t+dt,s4)]:
    v,vin,ich,ib,istart,ic=s;w=dt*weight/6
    sum_vin_i+=w*vin*ich;sum_i2+=w*ich**2
    sum_ir2+=w*ich**2*rs;sum_bridge+=w*ich*A['bridge_total_fixed_drop_V']
    sum_start+=w*v*istart;sum_bleed+=w*v*ib;sum_ic2+=w*ic**2
    sum_sin_i+=w*ich*math.sin(math.pi*phase/period)
    sum_cos_i+=w*ich*math.cos(math.pi*phase/period)
    vmin=np.minimum(vmin,v);vmax=np.maximum(vmax,v);ipeak=np.maximum(ipeak,ich)
   if step%max(1,steps//100)==0:
    vv,vin,ich,_,_,_=state(t+dt,e)
    records.append((t+dt,vv.copy(),ich.copy()))
 pin=sum_vin_i/period;irms=np.sqrt(sum_i2/period)
 b1=2*sum_sin_i/period;a1=2*sum_cos_i/period
 i1=np.hypot(a1,b1)/math.sqrt(2)
 df=b1/np.hypot(a1,b1);pf=pin/(vac*irms)
 thd=np.sqrt(np.maximum(0,irms**2-i1**2))/i1
 rows=[]
 for j,c in enumerate(cases):
  losses=(sum_ir2[j]+sum_bridge[j]+sum_start[j]+sum_bleed[j])/period
  residual=(e[j]-e_start[j])-(pin[j]-p[j]-losses)*period
  assert abs(residual)<1e-10
  assert abs(pf[j]-df[j]*i1[j]/irms[j])<1e-12
  rows.append(dict(c,bulk_min_V=float(vmin[j]),bulk_max_V=float(vmax[j]),
    calculated_line_input_W=float(pin[j]),line_rms_A=float(irms[j]),
    repetitive_charge_peak_A=float(ipeak[j]),capacitor_LF_rms_A=float(math.sqrt(sum_ic2[j]/period)),
    lumped_series_loss_W=float(sum_ir2[j]/period),fixed_bridge_loss_W=float(sum_bridge[j]/period),
    startup_feed_bus_draw_W=float(sum_start[j]/period),dedicated_bleeder_loss_W=float(sum_bleed[j]/period),
    true_power_factor=float(pf[j]),fundamental_displacement_factor=float(df[j]),
    current_THD_ratio=float(thd[j]),periodic_energy_delta_J=float(e[j]-e_start[j]),energy_balance_residual_J=float(residual),
    sampled_bulk_meets_200V_comparison=bool(vmin[j]>=200)))
 waves=[]
 for j,c in enumerate(cases):
  if c['cap_nom_F']==10e-6 and c['cap_factor']==.8 and c['series_R_ohm']==22 and c['remaining_bus_load_W']==10:
   waves.append(dict(case_index=j,t_s=[x[0] for x in records],bulk_V=[float(x[1][j]) for x in records],line_rectified_A=[float(x[2][j]) for x in records]))
 return rows,waves

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--verify-halved-step',action='store_true');args=ap.parse_args()
 rows,waves=run(A['time_step_s']);check={}
 if args.verify_halved_step:
  refined,_=run(A['time_step_s']/2)
  for key in ['bulk_min_V','bulk_max_V','calculated_line_input_W','line_rms_A','true_power_factor','fundamental_displacement_factor','capacitor_LF_rms_A','repetitive_charge_peak_A']:
   check[key+'_max_abs_difference']=max(abs(x[key]-y[key]) for x,y in zip(rows,refined))
  assert check['bulk_min_V_max_abs_difference']<.02
  assert check['true_power_factor_max_abs_difference']<.0002
  assert check['capacitor_LF_rms_A_max_abs_difference']<.0002
 discharge=[]
 for c in A['cap_nom_F']:
  cmax=c*1.2;v0=253*math.sqrt(2)
  discharge.append(dict(cap_nom_F=c,stored_energy_J_at_Cmax_and_highline_peak=.5*cmax*v0*v0,
    dedicated_bleeder_1Mohm_plus1_time_s={str(v):1e6*1.01*cmax*math.log(v0/v) for v in A['discharge_example_thresholds_V']},
    neither_threshold_nor_time_is_safe_access_acceptance=True))
 cold=[dict(series_R_ohm=r,ideal_highline_crest_current_A=(253*math.sqrt(2)-1.6)/r,
   not_a_measured_or_bounded_inrush=True) for r in A['lumped_input_series_R_ohm']]
 print(json.dumps({'study':'VEL-PRIMARY-BUFFER-01','date':'2026-11-16','assumptions':A,'cases':rows,
  'electrical_cases':len(rows),'verification_halved_step':check,'illustrative_discharge':discharge,
  'cold_plug_in_instantaneous_algebra_only':cold,'representative_waveforms':waves,
  'not_modeled':'Real switching/control/startup/UVLO, capacitor ESR/leakage, bridge dynamics, input inductance/filter/source impedance spectrum, transients, temperature, photometry or standard harmonic limits',
  'no_CAD_or_physical_test':True},indent=2))
