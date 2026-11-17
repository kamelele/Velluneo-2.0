"""Three commanded sampling pulses with residual flux: idealhybrid diagnostic only."""
from pathlib import Path
import math,itertools,json
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
r=[]
for bus,lf,rf,vcs,leb,delay,vd,cap,freq in itertools.product([240,253*math.sqrt(2)],[.9,1.1],[.979,1.021],[.175,.215],[180e-9,280e-9],[100e-9,150e-9],[.5,1.2],[4.032e-6,12e-6,20.592e-6],[92000,106000]):
 lp=.002304*lf;ls=lp/16;rs=2.37*rf;target=vcs/rs;period=1/freq;bleed=10000*.979
 # Affineoffstate [Is,Vout,1]; dIs/dt=-(Vout+Vd)/Ls,dV/dt=(Is-V/R)/C.
 A=np.array([[0,-1/ls,-vd/ls],[1/cap,-1/(bleed*cap),0],[0,0,0]],float)
 ip0=0.;vo=0.;events=[]
 for k in range(3):
  trise=max(0.,(target-ip0)*lp/bus);ton=max(trise,leb)+delay
  assert ton<period
  ipend=ip0+bus*ton/lp
  vo*=math.exp(-ton/(bleed*cap));initial=np.array([4*ipend,vo,1.])
  def off(t):return expm(A*t)@initial
  available=period-ton;last=off(available);reset=False
  if last[0]<=0:
   tz=brentq(lambda t:off(t)[0],0,available,xtol=1e-14);last=off(tz);vo=max(0,float(last[1]))*math.exp(-(available-tz)/(bleed*cap));ipnext=0.;reset=True
  else:vo=float(last[1]);ipnext=float(last[0])/4
  events.append({'pulse':k+1,'initial_primary_residual':ip0,'ton':ton,'ideal_threshold_rise_time':trise,'LEB_limited':trise<leb,'peak_primary':ipend,'remaining_primary_equivalent':ipnext,'Vo_at_nextclock':vo,'fully_demagnetized':reset,'peak_flux_proxy_T':lp*ipend/(120*57e-6)})
  ip0=ipnext
 r.append({'bus':bus,'Lp':lp,'Rcs':rs,'VCSTmin':vcs,'LEB':leb,'totaldelay_assumed':delay,'diode_drop_assumed':vd,'Cout':cap,'command_frequency':freq,'pulses':events})
summary={'scope':'Idealhybrid3commandedpulses, notTIstate-machine/SPICE/validatedtransistor model','cases':len(r),'all_on_times_less_1over106k':max(e['ton'] for x in r for e in x['pulses'])<1/106000,'max_on_time':max(e['ton'] for x in r for e in x['pulses']),'max_first3_peak_primary':max(e['peak_primary'] for x in r for e in x['pulses']),'max_first3_flux_proxy':max(e['peak_flux_proxy_T'] for x in r for e in x['pulses']),'Vo_after_3periods_range':[min(x['pulses'][-1]['Vo_at_nextclock'] for x in r),max(x['pulses'][-1]['Vo_at_nextclock'] for x in r)],'after3_remaining_primary_equivalent_range':[min(x['pulses'][-1]['remaining_primary_equivalent'] for x in r),max(x['pulses'][-1]['remaining_primary_equivalent'] for x in r)],'cases_withoutreset_between_firsttwo':sum(not x['pulses'][0]['fully_demagnetized'] for x in r),'LEB_limited_pulses':sum(e['LEB_limited'] for x in r for e in x['pulses']),'max_peak_case':max(r,key=lambda x:max(e['peak_primary'] for e in x['pulses'])),'omissions':['actualgatecharge/driveMiller/Coss/spikes/recovery','actualstartupVS/CSfilterandfaultstate transitions','RLCsubtraction (omittedforupperthresholdpeak illustration,notminimumenergyguarantee)','actualoffphasewindingcoupling/leakage/auxdraw','temperaturedependentVf/currentlimits','magneticnonlinearity/initialremanence'],'conclusion':'Residualcurrent+LEBpermitscommandedmaxfrequencyinthisconstructedhybridwitness,withhigherthanVCSTmin/Rcs peaks; first3arenotassumedfullyDCM. Notproofactualstartupmatchesit.'}
(P/'hybrid3-results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
