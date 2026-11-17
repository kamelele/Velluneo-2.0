"""Source-based NTC/auxiliary limits and coupled-branch DCM startup diagnostic.

Standard library only. Behavioral actuator, not the native UCC28711 control law.
No changes to CAD, graph or values. Inputs/hypotheses are separately identified.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,time

D=Path(__file__).resolve().parent;P=D.parent.parent
ap=argparse.ArgumentParser();ap.add_argument('--source-dir',required=True,type=Path);ap.add_argument('--steps',type=int,default=80);args=ap.parse_args()
sources=[('ucc2871x.pdf','https://www.ti.com/lit/ds/symlink/ucc28711.pdf',[4,5,6,10,11,12,16]),('sluaac5.pdf','https://www.ti.com/lit/pdf/SLUAAC5',[2,3,5,7,8]),('slua783.pdf','https://www.ti.com/lit/pdf/SLUA783',[3,5]),('ntcs0603e3t.pdf','https://www.vishay.com/docs/29056/ntcs0603e3t.pdf',[1])]
register=[]
for name,url,pages in sources:
 b=(args.source_dir/name).read_bytes();register.append({'filename':name,'url':url,'pages':pages,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
old=json.loads((P/'electrical-refinement/startup-protection/sources.json').read_text())
expect={a['filename']:a['sha256'] for a in old['primary_sources']}
for s in register:
 if s['filename'] in expect:assert s['sha256']==expect[s['filename']],s
inputs={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['schematic-intent/intended-connectivity.json','electrical-integration/proposed-parts.json','footprint-study/assignments.json','electrical-integration/magnetics/winding-results.json','electrical-refinement/startup-protection/results.json']}
mag=json.loads((P/'electrical-integration/magnetics/winding-results.json').read_text());hot=next(x for x in mag['loss_cases'] if x['MLT_mm']==60 and x['temperature_C']==125);wr={x['winding']:x['R_ohm'] for x in hot['windings']}
NPS=4.;NAS=22/30;R13=979000.;RBLEED=10000*.979

def rt(r25,beta,t):return r25*math.exp(beta*(1/(t+273.15)-1/298.15))
def t_from_r(r25,beta,r):return 1/(1/298.15+math.log(r/r25)/beta)-273.15
ntc=[]
for r25,beta,mpn in [(100000,4100,'NTCS0603E3104FXT'),(68000,3985,'NTCS0603E3683FXT'),(47000,3960,'NTCS0603E3473FXT')]:
 rows=[{'R25':r25*r,'B25_85':beta*b,'INTC_A':i,'Vthreshold_V':v,'Rtrip_ohm':v/i,'beta_model_trip_C':t_from_r(r25*r,beta*b,v/i),'sensor_power_at_trip_W':v*i} for r,b,i,v in itertools.product([.99,1.01],[.99,1.01],[90e-6,125e-6],[.9,1.0])]
 ntc.append({'mpn':mpn,'active':r25==100000,'nominal_trip_C':t_from_r(r25,beta,.95/105e-6),'corner_count':len(rows),'beta_model_trip_C':[min(x['beta_model_trip_C'] for x in rows),max(x['beta_model_trip_C'] for x in rows)],'trip_power_W':[min(x['sensor_power_at_trip_W'] for x in rows),max(x['sensor_power_at_trip_W'] for x in rows)],'corners':rows})
# Sensor first-order ramp lag: Tsource-Tsensor=a*tau*(1-exp(-t/tau)).
lag=[{'ramp_K_per_s':a,'tau_s_screen':4.,'asymptotic_lag_K_if_model_applies':a*4.,'lag_after4s_K':a*4*(1-math.exp(-1))} for a in [.1,.5,1,2,5,10]]

def bisect(fn,a,b,n=65):
 fa=fn(a)
 for _ in range(n):
  m=(a+b)/2;fm=fn(m)
  if fm*fa<=0:b=m
  else:a=m;fa=fm
 return (a+b)/2

def led_current(v,n,shift):
 if n==0:return 0.
 # Retained LED diagnostic equation; typical shape, not a calibrated device model.
 a=1.5601*8.617333262145e-5*298.15;Is=9.8487e-31;rs=.86341
 z=v/n-shift
 if z<=0:return 0.
 i=max(1e-18,min(.5,(z-2.4)/rs))
 for _ in range(10):
  f=a*math.log1p(i/Is)+rs*i-z;der=a/(i+Is)+rs;step=f/der
  new=i-step
  i=new if new>0 else i/2
 return max(0.,i)

def branch(im,vo,vd,rs,rpath,vfs,vfa):
 """Solve secondary-referred ampere-turn KCL and diode complementarity."""
 j=NPS*max(0,im);ss=vo+vfs;aa=(vd+vfa)/NAS
 if ss+j*rs<=aa:return ss+j*rs,j,0.
 if aa+j*rpath/(NAS*NAS)<=ss:return aa+j*rpath/(NAS*NAS),0.,j/NAS
 e=(j+ss/rs+NAS*(vd+vfa)/rpath)/(1/rs+NAS*NAS/rpath)
 return e,max(0,(e-ss)/rs),max(0,(NAS*e-vd-vfa)/rpath)

def trajectory(cfg,steps):
 lp=.002304*cfg['Lp_factor'];rcs=2.37*cfg['Rcs_factor'];cout=cfg['Cout_F'];cdd=cfg['Cdd_F'];rp=wr['P'];rs=wr['S'];ra=wr['A'];rpath=ra+cfg['Raux_ohm']*1.021
 bus=cfg['bus_V'];base=.0035;Qg=16e-9;n=cfg['LEDs'];shift=cfg['LED_shift_V'];vfs=cfg['VFout_V'];vfa=cfg['VFaux_V'];t=0.;vo=0.;vd=19.;trace=[];minkcl=0.;max_balance=0.;qa_total=0.;maxpeak=0.;minvd=vd;maxvd=vd;events=[]
 def load(v):return led_current(v,n,shift)+v/RBLEED
 def passive(dt):
  nonlocal vo,vd
  # RK4 output discharge over subdivision; exact affine VDD draw plus R13.
  parts=max(1,int(math.ceil(dt/10e-6)));h=dt/parts
  for _ in range(parts):
   def f(x):return -load(max(0,x))/cout
   k1=f(vo);k2=f(vo+h*k1/2);k3=f(vo+h*k2/2);k4=f(vo+h*k3);vo=max(0,vo+h*(k1+2*k2+2*k3+k4)/6)
  vd=(vd+base*R13)*math.exp(-dt/(R13*cdd))-base*R13
 if cfg['extra_initial_wait_s']:
  passive(cfg['extra_initial_wait_s']);t+=cfg['extra_initial_wait_s'];minvd=vd
 for k in range(1200):
  if vd<=8.5:events.append('UVLO_trough');break
  ip=(cfg['first3_VCS_V'] if k<3 else .810)/rcs
  r_on=rp+rcs+32 # MOS32ohm is a sensitivity, not a guaranteed hot limit.
  ton=-lp/r_on*math.log1p(-ip*r_on/bus)
  passive(ton);t+=ton;vd-=Qg/cdd;minvd=min(minvd,vd);maxpeak=max(maxpeak,ip)
  # StateVo,VDD,time,Qsecondary,Qaux,heat,loadenergy,biasenergy,auxtime.
  y=[vo,vd,0.,0.,0.,0.,0.,0.,0.];initial=.5*lp*ip*ip+.5*cout*vo*vo+.5*cdd*vd*vd
  def deriv(im,z):
   nonlocal minkcl
   ov=max(0,z[0]);bv=z[1];e,iss,ia=branch(im,ov,bv,rs,rpath,vfs,vfa);q=-lp/(NPS*e);il=load(ov);ib=base+bv/R13
   minkcl=max(minkcl,abs(NPS*max(im,0)-iss-NAS*ia))
   return [(iss-il)/cout*q,(ia-ib)/cdd*q,q,iss*q,ia*q,(iss*iss*rs+ia*ia*rpath+vfs*iss+vfa*ia)*q,ov*il*q,bv*ib*q,q if ia>1e-10 else 0.]
  dm=-ip/steps;im=ip
  for j in range(steps):
   k1=deriv(im,y);k2=deriv(im+dm/2,[u+dm*v/2 for u,v in zip(y,k1)]);k3=deriv(im+dm/2,[u+dm*v/2 for u,v in zip(y,k2)]);k4=deriv(im+dm,[u+dm*v for u,v in zip(y,k3)])
   y=[u+dm*(a+2*b+2*c+d)/6 for u,a,b,c,d in zip(y,k1,k2,k3,k4)];im=max(0,ip+(j+1)*dm);minvd=min(minvd,y[1]);maxvd=max(maxvd,y[1])
  vo,vd=y[:2];offtime=y[2];t+=offtime;qa_total+=y[4];minvd=min(minvd,vd)
  final=.5*cout*vo*vo+.5*cdd*vd*vd;balance=initial-final-y[5]-y[6]-y[7];max_balance=max(max_balance,abs(balance))
  # Deliberately constructed DCM actuator. First3 minimum pulses then source-derived
  # CC demag-fraction target; no assumed fixed maximum-rate first3 pulses.
  dmag=.318/.810
  period=max(ton+offtime+2.55e-6,1/106000,(offtime/dmag if k>=3 else 0))
  idle=period-ton-offtime;passive(idle);t+=idle;minvd=min(minvd,vd)
  if k<3 or k%10==9:trace.append({'pulse':k+1,'time_s':t,'Vo_V':vo,'VDD_V':vd,'period_s':period,'demag_s':offtime,'aux_charge_C':y[4],'aux_conduction_fraction_of_cycle':y[8]/period,'off_energy_error_J':balance})
  if t>=.006:break
  if vd>35:events.append('VDD_35_screen');break
 return {'config':cfg,'integration_steps_per_demag':steps,'pulses':k+1,'duration_s':t,'Vo_final_V':vo,'VDD_final_V':vd,'VDD_min_V':minvd,'VDD_max_V':maxvd,'reaches10V_reserve':minvd>=10,'remains_above8p5_UVLO':minvd>8.5,'maximum_KCL_error_A':minkcl,'maximum_off_energy_error_J':max_balance,'total_aux_charge_C':qa_total,'maximum_commanded_primary_peak_A':maxpeak,'events':events,'trace':trace}

configs=[]
for cap,bus,firstvcs,delay,vfs,vfa in itertools.product([12e-6,20.592e-6],[240,253*math.sqrt(2)],[.175,.215],[0,.0003],[0.,1.7],[1.,1.2]):
 configs.append({'Cout_F':cap,'Cdd_F':.890321e-6,'bus_V':bus,'Raux_ohm':4.7,'first3_VCS_V':firstvcs,'extra_initial_wait_s':delay,'Lp_factor':1.1,'Rcs_factor':1.021,'LEDs':7,'LED_shift_V':-.3,'VFout_V':vfs,'VFaux_V':vfa})
started=time.time();cases=[trajectory(c,args.steps) for c in configs]
compare=min(cases,key=lambda c:c['VDD_min_V'])['config'].copy();compare['Raux_ohm']=2.2;cases.append(trajectory(compare,args.steps))
# Independent arithmetic steady-state auxiliary ceiling, conditional onVo/Ip/VF bounds.
upper=[]
for vo,ip in itertools.product([27,33,40],[.35852176738964415,1.6/(2.37*.979)]):
 ceiling=NAS*(vo+1.7+NPS*ip*wr['S'])
 upper.append({'Vo_ceiling_assumed_V':vo,'Ip_ceiling_assumed_A':ip,'ideal_coupled_aux_ceiling_V':ceiling,'remaining_to35V_V':35-ceiling,'Cddmin_charge_reserve_to35_C':.890321e-6*(35-ceiling),'Cddmin_energy_reserve_to35_J':.5*.890321e-6*(35**2-ceiling**2),'excludes_leakage_commutation_and_sampling_overshoot':True})
result={'scope':'Source/interval calculations and executed ideal coupled-winding behavioralDCM diagnostic; NOT native28711/SPICE/fullconverter/measurement/qualification','base_commit':'b1117ae2caecc037d9fc1253bd9c3a3c4effaaf2','sources':register,'repository_inputs_SHA256':inputs,'ntc':ntc,'NTC_limits':{'Rtrip_min_ohm':.9/125e-6,'Rtrip_max_ohm':1/90e-6,'selfheat_K_if3mWperK_applies_max':1*125e-6/.003,'zero_power_curve_is_not_powered_sensor_error_bound':True,'beta_model_not_full_RT_curve_tolerance_guarantee':True,'source_tau_s':{'value':4,'relation':'less_than','test_mounting_not_declared_assembly':True},'ramp_lag_sensitivities':lag,'open_sensor':'externalNTCshutdownlost; no controller high-resistance fault specified','short_sensor':'NTCpulledlow; PWMshutdown/reset per source; confirm intermittent startup pulse sequence','internal165C':'typical only; above recommended125C andabsolute150C; not component protection design target'},'hot_winding_R_ohm':wr,'aux_ideal_ceiling_screens':upper,'behavioral_model':{'branches':'J=Nps*Im=Is+Nas*Ia; Esec=Vo+VFout+Is*Rs=(VDD+VFaux+IaRpath)/Nas when both conduct; complementarity enforces nonnegative branch currents','on_Rmos_ohm_hypothesis':32,'base_draw_A_hypothesis':.0035,'gate_charge_C_hypothesis':16e-9,'first3':'minpeak, eachallowedfulldemag plus2.55us; no native cadence guarantee','subsequent_actuator':'targetDmag=.318/.810, period>=ton+demag+2.55us and>=1/106k; no eta0.85 secondapplication','omitted':['native controllerVS/CSsampling,blanking,fault/valley state machine','validatedMOSdrive/Qg/Coss anddiodecurrenttemperaturecurves','leakage/parasiticcapacitance/ringing/coreloss/saturation','rampACbus andactualoutputLED/calibratedflux','VDDinternalstatechangingRUN/WAIT draws'],'counts':len(cases),'cases':cases},'no_shared_graph_CAD_or_values_changed':True,'no_self_closure_or_stage_approval':True}
# Compact source-derived results; full representative trajectory is separate.
worst=min(cases,key=lambda c:c['VDD_min_V'])
(D/f'worst-trajectory-{args.steps}.json').write_text(json.dumps(worst,indent=2)+'\n',encoding='utf-8',newline='\n')
for c in cases:
 c.pop('trace')
(D/'sources.json').write_text(json.dumps({'primary_sources':register,'repository_inputs_SHA256':inputs},indent=2)+'\n',encoding='utf-8',newline='\n')
(D/f'results-{args.steps}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'steps':args.steps,'cases':len(cases),'seconds':time.time()-started,'minVDD':min(c['VDD_min_V'] for c in cases),'maxKCLerror':max(c['maximum_KCL_error_A'] for c in cases),'maxOffEnergyError':max(c['maximum_off_energy_error_J'] for c in cases),'NTCactiveRange':ntc[0]['beta_model_trip_C'],'outcomes':[{'Cout':c['config']['Cout_F'],'bus':c['config']['bus_V'],'RAUX':c['config']['Raux_ohm'],'initial_wait':c['config']['extra_initial_wait_s'],'VDDmin':c['VDD_min_V'],'Vo_final':c['Vo_final_V'],'events':c['events']} for c in cases]},indent=2))
