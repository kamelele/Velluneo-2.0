#!/usr/bin/env python3
"""Averaged LED/capacitor ODE, static manufacturer diode law at25C plus explicit sensitivities.
Not a SPICE or LYTSwitch-5 simulation. Run: python calculate.py > results.json
Requires NumPy and SciPy. --verify-halved-step repeats at half step for convergence evidence.
"""
import argparse, hashlib, itertools, json, math
from pathlib import Path
import numpy as np
from scipy.special import lambertw

PARAM={'Is_A':9.8487e-31,'N':1.5601,'Rs_ohm':.86341,'Tnom_C':25,
       'binning_reference_current_A':.055,'stated_DC_max_current_A':.480}
A={'counts':[7,8],'mean_LED_current_A':[.25,.2835],
   'cap_nom_F':[220e-6,470e-6,1000e-6,2200e-6],'cap_factor':.8,
   'fixed_Tj_sensitivity_C':[25,85],'uniform_offset_per_LED_V':[-.1,0,.1],
   'temperature_coefficient_proxy_V_per_C':-.0009,'input_power_ripple_fraction':1.0,
   'bleed_ohm':10000,'line_Hz':50,'time_step_s':20e-6,
   'settling_cycles_per_feedback_iteration':24,'mean_current_relative_tolerance':2e-6}
K_B=1.380649e-23
Q_E=1.602176634e-19
av=PARAM['N']*K_B*(273.15+PARAM['Tnom_C'])/Q_E

# Exact inverse of Vf=a*log(1+I/Is)+Rs*I at Tnom. EG/XTI are deliberately not evaluated.
def vf(current):
 return av*np.log1p(np.asarray(current)/PARAM['Is_A'])+PARAM['Rs_ohm']*np.asarray(current)
def iv(per_led_V):
 z=PARAM['Rs_ohm']*PARAM['Is_A']/av*np.exp((per_led_V+PARAM['Rs_ohm']*PARAM['Is_A'])/av)
 return np.maximum(0,av/PARAM['Rs_ohm']*lambertw(z).real-PARAM['Is_A'])
for i in [.055,.25,.48]:
 assert math.isclose(float(iv(vf(i))),i,rel_tol=1e-12)

cases=[dict(count=n,target_mean_LED_A=i,cap_nom_F=c,cap_actual_F=c*A['cap_factor'],
            fixed_Tj_sensitivity_C=t,uniform_offset_per_LED_V=d)
       for n,i,c,t,d in itertools.product(A['counts'],A['mean_LED_current_A'],A['cap_nom_F'],A['fixed_Tj_sensitivity_C'],A['uniform_offset_per_LED_V'])]
n=np.array([c['count'] for c in cases]);target=np.array([c['target_mean_LED_A'] for c in cases])
cap=np.array([c['cap_actual_F'] for c in cases])
shift=np.array([c['uniform_offset_per_LED_V']+A['temperature_coefficient_proxy_V_per_C']*(c['fixed_Tj_sensitivity_C']-25) for c in cases])
period=1/(2*A['line_Hz'])

def quantities(energy):
 if np.any(energy<0):raise ValueError('Nonphysical negative energy: reduce step or review model')
 voltage=np.sqrt(2*energy/cap)
 current=iv(voltage/n-shift)
 return voltage,current,current*voltage,voltage**2/A['bleed_ohm']

def simulate(power,energy,dt,cycles):
 steps=round(period/dt);dt=period/steps
 omega=2*math.pi/period
 def rhs(t,e):
  v,i,pl,pb=quantities(e)
  pin=power*(1-A['input_power_ripple_fraction']*math.cos(omega*t))
  return pin-pl-pb,i,pl,pb
 sum_i=np.zeros(len(cases));sum_pl=np.zeros(len(cases));sum_pb=np.zeros(len(cases))
 min_i=np.full(len(cases),np.inf);max_i=np.zeros(len(cases))
 min_v=np.full(len(cases),np.inf);max_v=np.zeros(len(cases))
 records=[];cycle_start=None
 for step in range(steps*cycles):
  t=(step%steps)*dt
  if step==steps*(cycles-1):cycle_start=energy.copy()
  k1,i1,p1,b1=rhs(t,energy)
  k2,i2,p2,b2=rhs(t+dt/2,energy+dt*k1/2)
  k3,i3,p3,b3=rhs(t+dt/2,energy+dt*k2/2)
  k4,i4,p4,b4=rhs(t+dt,energy+dt*k3)
  energy=energy+dt*(k1+2*k2+2*k3+k4)/6
  if step>=steps*(cycles-1):
   sum_i+=dt*(i1+2*i2+2*i3+i4)/6
   sum_pl+=dt*(p1+2*p2+2*p3+p4)/6
   sum_pb+=dt*(b1+2*b2+2*b3+b4)/6
   v,i,_,_=quantities(energy)
   min_i=np.minimum(min_i,i);max_i=np.maximum(max_i,i)
   min_v=np.minimum(min_v,v);max_v=np.maximum(max_v,v)
   if step%max(1,steps//100)==0:records.append((t+dt,i.copy(),v.copy()))
 mean_i=sum_i/period
 return energy,dict(mean_i=mean_i,min_i=min_i,max_i=max_i,min_v=min_v,max_v=max_v,
    mean_led_power=sum_pl/period,mean_bleed_power=sum_pb/period,
    periodic_energy_delta=energy-cycle_start,
    energy_balance_residual=(energy-cycle_start)-(power*period-sum_pl-sum_pb),records=records)

def run(dt):
 v0=n*(vf(target)+shift)
 energy=.5*cap*v0*v0
 power=v0*target+v0*v0/A['bleed_ohm']
 iterations=[]
 for attempt in range(12):
  energy,m=simulate(power,energy,dt,A['settling_cycles_per_feedback_iteration'])
  err=float(np.max(np.abs(m['mean_i']/target-1)))
  iterations.append(err)
  if err<A['mean_current_relative_tolerance']:break
  power=power*target/m['mean_i']
 else:raise RuntimeError('Average-current ideal-loop calibration did not converge')
 out=[]
 for index,c in enumerate(cases):
  lo=float(m['min_i'][index]);hi=float(m['max_i'][index])
  out.append(dict(c,mean_LED_A=float(m['mean_i'][index]),min_LED_A=lo,max_LED_A=hi,
   current_modulation_percent=100*(hi-lo)/(hi+lo),
   min_output_V=float(m['min_v'][index]),max_output_V=float(m['max_v'][index]),
   mean_LED_power_W=float(m['mean_led_power'][index]),mean_bleed_W=float(m['mean_bleed_power'][index]),
   required_mean_input_to_secondary_W=float(power[index]),
   periodic_energy_delta_J=float(m['periodic_energy_delta'][index]),
   energy_balance_residual_J=float(m['energy_balance_residual'][index]),
   below_binning_reference_current=lo<PARAM['binning_reference_current_A'],
   above_stated_DC_max=hi>PARAM['stated_DC_max_current_A']))
 waves=[]
 for j,c in enumerate(cases):
  if c['count']==7 and c['target_mean_LED_A']==.25 and c['fixed_Tj_sensitivity_C']==25 and c['uniform_offset_per_LED_V']==0:
   waves.append(dict(case_index=j,cap_nom_F=c['cap_nom_F'],t_s=[x[0] for x in m['records']],LED_A=[float(x[1][j]) for x in m['records']],output_V=[float(x[2][j]) for x in m['records']]))
 return out,iterations,waves

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--verify-halved-step',action='store_true');args=parser.parse_args()
 results,iterations,waves=run(A['time_step_s'])
 validation={}
 if args.verify_halved_step:
  refined,_,_=run(A['time_step_s']/2)
  for key in ['min_LED_A','max_LED_A','min_output_V','max_output_V','mean_LED_power_W','current_modulation_percent']:
   validation[key+'_max_absolute_difference']=max(abs(x[key]-y[key]) for x,y in zip(results,refined))
  assert validation['min_LED_A_max_absolute_difference']<1e-4
  assert validation['max_LED_A_max_absolute_difference']<1e-4
  assert validation['current_modulation_percent_max_absolute_difference']<.02
 small_signal=[]
 for count in [7,8]:
  i0=.25
  v0=float(count*vf(i0))
  rd=count*(av/(i0+PARAM['Is_A'])+PARAM['Rs_ohm'])
  p0=v0*i0+v0*v0/A['bleed_ohm']
  for cnom in A['cap_nom_F']:
   c=cnom*A['cap_factor']
   conductance_power=i0+v0/rd+2*v0/A['bleed_ohm']
   gain=p0/(i0*rd*math.sqrt(conductance_power**2+(2*math.pi/period*c*v0)**2))
   small_signal.append(dict(count=count,cap_nom_F=cnom,current_ripple_to_power_ripple_gain=gain,
      input_power_ripple_fraction_for_example_5pct_current=.05/gain,
      example_5pct_is_not_accepted_requirement=True))
 sources=json.loads(Path(__file__).with_name('sources.json').read_text())
 print(json.dumps({'study':'VEL-LED-BUFFER-01','date':'2026-11-16','model_parameters_at25C':PARAM,
  'assumptions':A,'solver':'Fixed-step RK4 capacitor energy ODE, Lambert-W static diode inversion; ideal slow mean-current calibration',
  'equation':'d(0.5*C*V^2)/dt = Pavg*(1-cos(2*pi*100*t)) - V*I_LED(V) - V^2/Rbleed',
  'not_modeled':'Actual IC/feedback dynamics, switching, ESR/ESL, startup/faults, thermal feedback, measured bins/photometry or PstLM/SVM',
  'sources':sources,'small_signal_buffer_budget':small_signal,'cases':results,'feedback_iteration_relative_errors':iterations,
  'validation_halved_step':validation,'representative_waveforms':waves,
  'source_55mA_voltage_check_V':float(vf(.055)),
  'source_250mA_voltage_calculated_V':float(vf(.25)),
  'source_250mA_dynamic_resistance_per_LED_ohm':av/(.25+PARAM['Is_A'])+PARAM['Rs_ohm'],
  'no_SPICE_or_physical_test':True},indent=2))
