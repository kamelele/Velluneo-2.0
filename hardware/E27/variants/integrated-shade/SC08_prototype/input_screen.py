"""SC08 own RC input and surge numerical screen; not IEC qualification."""
import math,json,itertools
from pathlib import Path
OUT=Path(__file__).parent
VP=253*math.sqrt(2); RMIN=2*220*.95*(1-.0004*(155-25)); RMAX=2*220*1.05*(1+.0004*(155-25)); CMAX=430e-9*1.1

def normal(vac=230.,Rin=440.,Cin=430e-9,Cout=120e-6,duration=1.):
 f=66000.;T=1/f;Rs=28.7;L=.003;ilim=.375;vth=1.65;tau=Rs*22e-6; i=cf=v=bus=0.;N=round(f*duration);start=N//2;vmax=0.;vmin=1e9;ql=qsum=i2sum=0.;pk=0.;busmax=0.;gap=gmax=0.
 for n in range(N):
  vrect=max(0.,math.sqrt(2)*vac*abs(math.sin(2*math.pi*50*n*T))-1.6);vin=max(0.,bus-1.7);qa=ton=0.
  if cf<vth and vin>v:
   a=(vin-v)/L;ton=min(.69*T,max(.5e-6,(ilim-i)/a));j=i+a*ton;qa=(i+j)*ton/2;i=j;cf*=math.exp(-ton/tau)
  a=(v+1+max(cf,0.))/L;tf=min(T-ton,i/a);j=max(0.,i-a*tf);qb=(i+j)*tf/2;cf=(cf-Rs*i-Rs*a*tau)*math.exp(-tf/tau)+Rs*(i-a*tf+a*tau);cf*=math.exp(-(T-ton-tf)/tau);i=j
  q=qa+qb;led=max(0.,v-84.5)/470.;load=led+max(0.,v-12.15)/5070+2*v/56000+v/321000+.00145;v=max(0.,v+(q-load*T)/Cout)
  if vrect>bus:
   # Analytic RC update for converter input charge averaged over T; exact isource² integral in conduction region.
   z=qa/T; y=(vrect-bus)/Rin-z; k=Rin*Cin; ex=math.exp(-T/k);src2=z*z*T+2*z*y*k*(1-ex)+y*y*k/2*(1-ex*ex); bus=vrect-Rin*z+(bus-vrect+Rin*z)*ex
  else:src2=0.;bus=max(0.,bus-qa/Cin)
  if n>=start:
   vmax=max(vmax,v);vmin=min(vmin,v);ql+=led*T;qsum+=q;i2sum+=src2;busmax=max(busmax,bus);gap=gap+T if q<1e-15 else 0.;gmax=max(gmax,gap)
 dt=(N-start)*T;irms=math.sqrt(i2sum/dt)
 return dict(Vac=vac,Rin=Rin,Cin=Cin,Cout=Cout,duration=duration,Coutmax=vmax,Coutmin=vmin,LEDavg=ql/dt,driveravg=qsum/dt,RFtotalW=irms*irms*Rin,RF_each_equal_nom_W=irms*irms*Rin/2,bridge_RMS=irms,busmax=busmax,max_chargegap=gmax)

# Double-exponential voltage: intended1.2/50-type test proposal, actualvirtualtimings calculated below.
a=14600.;b=2470000.;tpk=math.log(b/a)/(b-a);norm=math.exp(-a*tpk)-math.exp(-b*tpk)
def wave(t):return (math.exp(-a*t)-math.exp(-b*t))/norm

def surge(amplitude=1000.,Tj=125.,dt=50e-9,C=CMAX,R=RMIN,init=VP,zero_tvs=False):
 factor=1+.0011*(Tj-25);VB=462*factor;rd=(602-462)/2.5*factor;v=init;er=et=qs=0.;pmax=ipk=itpk=vmax=0.;n=round(.001/dt)
 def deriv(t,v):
  src=VP+amplitude*wave(t);isrc=max(0.,(src-v)/(R+2.));it=0. if zero_tvs else max(0.,(v-VB)/rd)
  return (isrc-it)/C,isrc,isrc*isrc*R,it*v,it
 for n in range(n):
  t=n*dt;k1=deriv(t,v);k2=deriv(t+dt/2,v+k1[0]*dt/2);k3=deriv(t+dt/2,v+k2[0]*dt/2);k4=deriv(t+dt,v+k3[0]*dt)
  v+=dt*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6; er+=dt*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6;et+=dt*(k1[3]+2*k2[3]+2*k3[3]+k4[3])/6;qs+=dt*(k1[1]**2+2*k2[1]**2+2*k3[1]**2+k4[1]**2)/6;vmax=max(vmax,v);ipk=max(ipk,k1[1]);itpk=max(itpk,k1[4]);pmax=max(pmax,k1[3])
 return dict(amplitude=amplitude,Tj_assumed=Tj,dt=dt,C=C,Rtotal=R,init=init,Vmax=vmax,source_Ipeak=ipk,TVS_Ipeak=itpk,RF_total_energy_J=er,RF_each_equal_energy_J=er/2,source_I2t=qs,TVS_energy_J=et,TVS_Ppeak_W=pmax,status='Piecewise-linearTVSengineeringmodel;alphaVBRmappedtoVc/Rdconditionally,notvalidatedhotclamp;noRFfusing,parasiticsorTVSselfheating')
# Pure RC inrush exact, including source resistor only: noTVS below418V.
inrush=dict(Vpeak=VP,R_pair_min=RMIN,Cmax=CMAX,Ipeak=VP/RMIN,tau=RMIN*CMAX,I2t=VP**2*CMAX/(2*RMIN),RF_total_energy_J=.5*CMAX*VP**2,RF_each_equal_energy_J=.25*CMAX*VP**2,RF_max_individual_mixed_energy_J=.5*CMAX*VP**2*(RMAX/(RMAX+RMIN)))
res=dict(kind='Executed own numerical screens, no physical tests or CAD approval',proposal=dict(RF='2xTEFWFU2W220RJseries',filter='RemoveL1andR1;parallelC1+C2=430nFexistingfilm',TVS='Vishay1.5KE440A-E3/54',blocking='STTH110A:BUS_PLUSanode,U1DRAINcathode',scope='1kVdifferentialengineeringtestproposal;2kVcomparisonisnotapassclaim'),input_corner=dict(Rmin=RMIN,Rmax=RMAX,temperature_for_resistance_corner=155,Cmax=CMAX),inrush=inrush,normal=[normal(vac=v) for v in [207.,230.,253.]],normal_Rcorners=[normal(vac=207.,Rin=r) for r in [RMIN,RMAX]],normal_duration2=normal(duration=2.),surge=[surge(amplitude=e,Tj=t) for e,t in itertools.product([1000.,2000.],[25.,85.,125.])],surge_refinement=surge(dt=25e-9),surge_from_empty=surge(init=0.),limitations=['NormalRCcharge-averageapproximation:noactualswitchcurrentorHFbridgecurrent,DCR,nonlinearmagnetics,reversecurrent,jitter,auto-restart,OVP,thermalmodelorfulltempcurrentbounds.','TVScapacitancenotincluded. Actualhotclamp/pulsepower/fusing/repeatedsurge/lineEMCstillrequiresqualification.','RemovingL1eliminatesitsnonlinearityandresonance;cannotclaimEMCpasswithoutfiltermeasurement.','BridgeRFpulsewidthsbelow1msarenotcoveredbyMB10SspecifiedI2tinterval1..8.3ms;comparisonisnotqualification.'])
# Entire surge-excess input energy is counted even if part precedes OVP trip: conservative covers precharged Cin.
F1=(1/a-1/b)/norm;F2=(1/(2*a)-2/(a+b)+1/(2*b))/(norm*norm)
res['output_energy_bounds']=[]
for amplitude,delay,Ipk in itertools.product([1000.,2000.],[.0006,.002],[.7,1.4]):
 extra=(2*VP*amplitude*F1+amplitude**2*F2)/(4*RMIN)
 normalP=VP**2/(4*RMIN);ein=.5*CMAX*VP**2;el=.5*.0033*Ipk**2;total=normalP*delay+extra+ein+el
 res['output_energy_bounds'].append(dict(amplitude=amplitude,delay=delay,imposed_Lout_Ipk=Ipk,normal_source_P_bound=normalP,entire_surge_excess_E_bound=extra,Cin_initial_normal_E=ein,Lout_E=el,total_added_E=total,Cout_initial=131.,Coutmin=120e-6,Vout_bound=math.sqrt(131**2+2*total/120e-6),conditional='AllinputpowercrossestwoRF;singleassumedwaveform;Cinputstartnormal<=357.796V;allLoutcurrentboundimposednotguaranteed;includesfullpulseexcessindependentofOVPtripphase;notphysicaltest'))
# Conservative imposedtestenvelope with3usflatpeakthen60ushalfvaluetail; scalarRC comparison, TVS omitted.
def rc_upper(amplitude=1100.,Cin=430e-9*.9,front=3e-6,half=60e-6):
 rc=RMIN*Cin;ta=half/math.log(2);x0=amplitude*(1-math.exp(-front/rc))
 def x(t):return x0*math.exp(-t/rc)+amplitude*ta/(ta-rc)*(math.exp(-t/ta)-math.exp(-t/rc))
 # x'=0 iff sourceexcess=x; locate monotonicrootafterpeak.
 lo=0.;hi=.003
 for _ in range(90):
  mid=(lo+hi)/2
  if amplitude*math.exp(-mid/ta)>x(mid):lo=mid
  else:hi=mid
 tp=(lo+hi)/2;F1=amplitude*(front+ta);F2=amplitude**2*(front+ta/2);extra=(2*VP*F1+F2)/(4*RMIN)
 return dict(amplitude=amplitude,Cin_min=Cin,Rmin=RMIN,front=front,tail_half=half,timeafterfront_peak=tp,busmax_TVS_omitted=VP+x(tp),normalVDS_source_belowreturn_budget_V=5.,conditional_VDS_beforeparasitics=VP+x(tp)+5.,fullpulse_excess_source_E=extra,Cout_with_0p6ms_131V_120uF_L3p3mH1p4A=math.sqrt(131**2+2*(VP**2/(4*RMIN)*.0006+extra+.5*CMAX*VP**2+.5*.0033*1.4**2)/120e-6),scope='Imposeduppertest-envelope;CinminimumandnegativeSOURCE5Vbudgetmustbevalidated,notmanufacturerallconditionguarantees')
res['conservative_RC_test_envelopes']=[rc_upper(a) for a in [1100.,2200.]]
res['surge_waveform']=dict(alpha=a,beta=b,peak_time=tpk,normalization=norm,integral_shape_s=F1,integral_shape_squared_s=F2,description='Single normalized double-exponential1.2/50-typevoltageassumption;notcertifiedgenerator/toleranceenvelope')
res['plateau_bounds']=[dict(surge_V=e,current_bound25C=(VP+e-418)/RMIN,TVS25C_Ipp_limit=2.5,above2p5=(VP+e-418)/RMIN>2.5) for e in [1000,2000]]
res['conditional_hot_clamp']=[dict(Tj=t,Vc=602*(1+.0011*(t-25)),margin_to700=700-602*(1+.0011*(t-25))) for t in [85,100,125,150]]
(OUT/'input-results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
