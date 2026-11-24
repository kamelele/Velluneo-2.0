"""Passive RC replacement of L1; no magnetic or silicon macromodel is claimed."""
from pathlib import Path
import numpy as np,math,itertools,json
H=Path(__file__).resolve().parent
def run(cases,dt=2.5e-8,duration=.001,source='sine'):
 n=len(cases);RF=np.array([c['RF']for c in cases]);R=np.array([c['R']for c in cases]);C1=np.array([c['C1']for c in cases]);C4=np.array([c['C4']for c in cases]);vp=np.array([c['VAC']*math.sqrt(2)for c in cases]);phase=np.array([c['phase_deg']*math.pi/180 for c in cases]);s=np.array([[c['a0']for c in cases],[c['b0']for c in cases]],dtype=float);maxv=s.copy();minv=s.copy();maxrf=np.zeros(n);maxr=np.zeros(n);energyRF=np.zeros(n);energyR=np.zeros(n);pulse_over_100W=np.zeros(n);pulse_over_10W=np.zeros(n)
 def f(t,s):
  v=vp if source=='step' else vp*np.abs(np.sin(2*math.pi*50*t+phase));ib=np.maximum(0.,(v-s[0])/RF);ir=(s[0]-s[1])/R
  return np.array([(ib-ir)/C1,ir/C4]),ib,ir
 for k in range(round(duration/dt)):
  t=k*dt;k1,ib,ir=f(t,s);k2,ib2,ir2=f(t+dt/2,s+dt*k1/2);k3,ib3,ir3=f(t+dt/2,s+dt*k2/2);k4,ib4,ir4=f(t+dt,s+dt*k3);s+=dt*(k1+2*k2+2*k3+k4)/6;maxv=np.maximum(maxv,s);minv=np.minimum(minv,s);maxrf=np.maximum(maxrf,abs(ib));maxr=np.maximum(maxr,abs(ir));energyRF+=(ib*ib+2*ib2*ib2+2*ib3*ib3+ib4*ib4)*RF*dt/6;energyR+=(ir*ir+2*ir2*ir2+2*ir3*ir3+ir4*ir4)*R*dt/6;p=ir*ir*R;pulse_over_100W+=np.where(p>100,dt,0);pulse_over_10W+=np.where(p>10,dt,0)
 return [dict(c,dt_s=dt,duration_s=duration,source=source,C1_peak_V=float(maxv[0,j]),C4_peak_V=float(maxv[1,j]),C1_min_V=float(minv[0,j]),C4_min_V=float(minv[1,j]),RF_peak_A=float(maxrf[j]),R10_peak_A=float(maxr[j]),R10_peak_V=float(maxr[j]*R[j]),R10_peak_W=float(maxr[j]**2*R[j]),RF_energy_J=float(energyRF[j]),R10_energy_J=float(energyR[j]),R10_time_above_100W_s=float(pulse_over_100W[j]),R10_time_above_10W_s=float(pulse_over_10W[j]))for j,c in enumerate(cases)]
def summary(rows):
 return {k:max(r[k]for r in rows)for k in ['C1_peak_V','C4_peak_V','RF_peak_A','R10_peak_A','R10_peak_V','R10_peak_W','RF_energy_J','R10_energy_J','R10_time_above_100W_s','R10_time_above_10W_s']}
if __name__=='__main__':
 # RF1:5%+200ppm/K*100K; chosenPR02-FS R10:10%+250ppm/K*100K.
 cases=[dict(RF=47*rs,R=100*r10s,C1=47e-9*c1s,C4=150e-9*c4s,VAC=vac,phase_deg=ph,a0=a,b0=b)for rs,r10s,c1s,c4s,vac,ph,a,b in itertools.product([.95*.98,1.05*1.02],[.90*.975,1.10*1.025],[.95,1.05],[.9,1.1],[207,253],[0,45,90,135],[0,357.8],[0,357.8])]
 rows=run(cases,dt=1e-7)
 coarse=summary(rows);convergence=[]
 for key in ['R10_peak_W','R10_energy_J','RF_energy_J','C4_peak_V']:
  c=max(rows,key=lambda c:c[key]);fine=run([c],dt=2.5e-8)[0];convergence.append({'key':key,'coarse':c[key],'fine':fine[key],'absolute_delta':abs(c[key]-fine[key]),'case':fine})
 cold=[r for r in rows if r['a0']==0 and r['b0']==0]
 out={'assumptions':['Ideal blocking bridge; passiveRF1-C1-R10-C4; R10=100ohm replacesL1. No controller/surge/macromodel.','Independentretainedinputcapcharge0/357.8V,zeroinductorenergybecauseL1removed;207/253VAC50Hzfourphases;notanexhaustivephysicalstateclaim.','RF1range5%initialplus200ppm/K100K;R10PR02-FS10%initialplus250ppm/K100K envelope. C1±5%C4±10%.','Allcurrentandenergypeaksarenumericalscenarioresults;maximumprincipleprovidesa separateidealRCvoltagebound.','Tailinputenergyintegratedonly1ms;periodicrunninglossnot inferredfromstartuptransient.'], 'maxima':coarse,'cold_maxima':summary(cold),'convergence':convergence,'rows':rows,'dc_loss_table':[{'I_RMS_A':i,'R10_max_ohm':112.75,'R10_W':i*i*112.75,'RF1_W':i*i*47*1.05*1.02,'pair_W':i*i*(112.75+47*1.05*1.02)}for i in [.04,.05,.06,.08,.1]],'voltage_invariant_proof':'For0<=source(t)<=Vmax and0<=initialC1,C4<=Vmax, RF1,R10,C1,C4>0 andnoenergysourcefromload: at a=Vmax da/dt=(max(0,(u-Vmax)/RF1)-(Vmax-b)/R10)/C1<=0; at b=Vmax db/dt=(a-Vmax)/(R10*C4)<=0. Lowerfaceshaveinwardderivatives. Thus bothvoltagesremain[0,Vmax]. This removesintentionalLCresonance only; parasiticinductance/EMI/surge/faultovershootarenotmodeled.'}
 (H/'rc-screen.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['rows','assumptions']},indent=2))
