"""Own AN60-inspired per-cycle sample/hold + coupled reservoir screen. Not PIXls/SPICE."""
import math,json,itertools
from pathlib import Path
OUT=Path(__file__).parent

def simulate(vac=230.,Rs=28.7,L=.003,f=66000.,ilim=.375,vth=1.65,Cfb=22e-6,tmin=.5e-6,Cout=120e-6,Rled=470.,Vled=84.5,leak=.00145,duration=1.,method='exact'):
 T=1/f;tau=Rs*Cfb;cf=i=v=0.; N=round(duration*f);start=N//2;halfN=round(.01*f);hist=[];qd=ql=qa_all=0.;imax=0.;gap=egap=gmax=emax=0.;halves={};startupmax=0.;charge_balance=0.;vstart=None;trace=[]
 for n in range(N):
  vin=max(0.,math.sqrt(2)*vac*abs(math.sin(2*math.pi*50*n*T))-1.6);ton=qa=0.;enabled=cf<vth and vin>v
  if enabled:
   a=(vin-v)/L;ton=min(.69*T,max(tmin,(ilim-i)/a));j=i+a*ton;qa=(i+j)*ton/2;i=j;cf*=math.exp(-ton/tau)
  a=(v+1+max(cf,0.))/L;tf=min(T-ton,i/a);j=max(0.,i-a*tf);qb=(i+j)*tf/2
  cf=(cf-Rs*i-Rs*a*tau)*math.exp(-tf/tau)+Rs*(i-a*tf+a*tau);cf*=math.exp(-(T-ton-tf)/tau)
  q=qa+qb;pk=i;i=j;vold=v
  # All branches are resistive/piecewise affine; use exponential constant-average-driver update.
  # Input q/T is held for one switching period. This is not within-cycle switching simulation.
  g=2/56000+1/321000; const=leak
  if v>12.15:g+=1/5070;const-=12.15/5070
  if v>Vled:g+=1/Rled;const-=Vled/Rled
  if method=='exact':
   eq=(q/T-const)/g;v=max(0.,eq+(v-eq)*math.exp(-g*T/Cout))
  else:v=max(0.,v+(q-T*(max(0.,v-Vled)/Rled+max(0.,v-12.15)/5070+2*v/56000+v/321000+leak))/Cout)
  vm=(v+vold)/2; led=max(0.,vm-Vled)/Rled;load=led+max(0.,vm-12.15)/5070+2*vm/56000+vm/321000+leak
  if n<start:startupmax=max(startupmax,v)
  else:
   if vstart is None:vstart=vold
   hist.append(v);qd+=q;ql+=load*T;qa_all+=led*T;imax=max(imax,pk);charge_balance+=q-load*T
   gap=gap+T if q<1e-15 else 0.;egap=egap+T if not enabled else 0.;gmax=max(gmax,gap);emax=max(emax,egap)
   key=n//halfN;halves[key]=halves.get(key,0.)+q
   if n%round(f/10000)==0:trace.append([n*T,v,led,q/T,cf])
 elapsed=(N-start)*T
 return dict(inputs=dict(vac=vac,Rs=Rs,L=L,f=f,ilim=ilim,vth=vth,Cfb=Cfb,tmin=tmin,Cout=Cout,Rled=Rled,Vled=Vled,leak=leak,duration=duration,method=method),steady=dict(Vmin=min(hist),Vmax=max(hist),ripple=max(hist)-min(hist),LEDavg=qa_all/elapsed,driveravg=qd/elapsed,loadavg=ql/elapsed,model_Ipk=imax,longest_zero_charge_gap_s=gmax,longest_disabled_gap_s=emax,min_10ms_charge_c=min(halves.values()),missing_10ms_charge_bins=sum(q<1e-12 for q in halves.values()),missing20ms_steady_burst=any(halves[k]+halves.get(k+1,1.)<1e-12 for k in halves),charge_balance_residual_c=charge_balance-Cout*(v-vstart),last_voltage=v,start_voltage=vstart),startup=dict(peak_first_half_v=startupmax),trace=trace)

cases=[]
for vac in [207.,230.,253.]:
 cases.append(simulate(vac=vac))
 # Eight illustrative corners per line, controller bundles are sensitivity choices NOT guaranteed envelopes.
 for Rled,high,L in itertools.product([470*.95*.97,470*1.05*1.03],[False,True],[.0024,.0033]):
  cases.append(simulate(vac=vac,Rled=Rled,L=L,Rs=28.7*(.99 if high else 1.01),vth=1.76 if high else 1.54,ilim=.504 if high else .350,f=70000. if high else 62000.,tmin=.675e-6,leak=.00145))
convergence=[simulate(vac=230.,duration=2.),simulate(vac=230.,method='euler')]
# Deliberately isolate capacitor leakage input, not assumed typical current.
leakfree=simulate(vac=230.,leak=0.)
report=dict(kind='Own coupled per-cycle ideal-source analytical simulation, not PIXls/SPICE',equations=['Iled=max(0,(Vout-84.5)/Rled)','Iaux=max(0,(Vout-12.15)/5070)+2*Vout/56000+Vout/321000+Ileak','Cout*dVout/dt=Iinductor-Iled-Iaux','For each piecewise affine load region: Vnext=Veq+(Vold-Veq)*exp(-g*T/Cout), Veq=(Qdriver/T-constant)/g'],scope='SC07-C dualPhotoMOS normal steady load only; OVP not modeled; crossing threshold indicates design conflict, not qualified clamping',limitations=['Ideal rectified source minus1.6V; actual pi filter, bridge switching, DCR,ESR,losses,nonlinear L,reverse-current startup,frequency jitter,50ms/800ms auto-restart and BP/OVP shutdown omitted. Fixed69%maximumduty, not a swept device duty envelope.','Frozen Vout during each switching cycle and analytic CFB ramp integration; output region uses beginning-of-cycle branch state and average driver charge.','All controller corner values remain illustrative25C/sensitivity inputs, not full-temperature/all-slope guaranteed bounds.','LED constant84.5V is worst-Vf load assumption, not actual diode IV or finalbin guarantee. Startup peak separated from steady last half; no safety acceptance.'],cases=[{k:v for k,v in x.items() if k!='trace'} for x in cases],convergence=[{k:v for k,v in x.items() if k!='trace'} for x in convergence],leak_free={k:v for k,v in leakfree.items() if k!='trace'})
report['summary']=dict(cases=len(cases),max_v=max(x['steady']['Vmax'] for x in cases),min_v=min(x['steady']['Vmin'] for x in cases),LEDavg_range=[min(x['steady']['LEDavg'] for x in cases),max(x['steady']['LEDavg'] for x in cases)],max_chargegap_s=max(x['steady']['longest_zero_charge_gap_s'] for x in cases),missing20ms_any=any(x['steady']['missing20ms_steady_burst'] for x in cases),normal123V_exceedances=sum(x['steady']['Vmax']>123 for x in cases),lowest_OVP126V_exceedances=sum(x['steady']['Vmax']>126 for x in cases))
(OUT/'coupled-results.json').write_text(json.dumps(report,indent=2)+'\n')
with (OUT/'coupled-trace-nominal-230.csv').open('w') as f:
 f.write('time_s,Vout_V,Iled_A,Icharge_avg_A,VCFB_V\n');f.writelines(','.join(str(v) for v in row)+'\n' for row in cases[9]['trace'])
print(json.dumps(dict(summary=report['summary'],nominals=[cases[k]['steady'] for k in [0,9,18]],convergence=[x['steady'] for x in convergence]),indent=2))
