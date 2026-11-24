"""Explicit ideal-diode, linear-inductor engineering sensitivity screen.
Not a manufacturer model or a qualified nonlinear/hardware/surge upper bound.
"""
from pathlib import Path
import json,itertools,math,hashlib
import numpy as np
H=Path(__file__).resolve().parent
def run(cases,dt=5e-8,duration=.001,source='step'):
 n=len(cases);a=np.array([c.get('a0',0.)for c in cases]);i=np.array([c.get('i0',0.)for c in cases]);b=np.array([c.get('b0',0.)for c in cases]);s=np.array([a,i,b]);R=np.array([c['R']for c in cases]);C1=np.array([c['C1']for c in cases]);C4=np.array([c['C4']for c in cases]);L=np.array([c['L']for c in cases]);dcr=np.array([c['DCR']for c in cases]);phase=np.array([c.get('phase_deg',90.)for c in cases])*math.pi/180;vp=np.array([c.get('VAC',253.)*math.sqrt(2)for c in cases]);maxa=a.copy();maxb=b.copy();maxi=abs(i);mina=a.copy();minb=b.copy();maxld=abs(a-b);energy=np.zeros(n);maxsource=np.zeros(n);maxdv=np.zeros(n)
 def f(t,s):
  v=vp if source=='step' else vp*np.abs(np.sin(2*math.pi*50*t+phase))
  current=np.maximum(0.,(v-s[0])/R)
  return np.array([(current-s[1])/C1,(s[0]-s[2]-dcr*s[1])/L,s[1]/C4]),current
 for k in range(round(duration/dt)):
  t=k*dt;k1,cur=f(t,s);k2,_=f(t+dt/2,s+dt*k1/2);k3,_=f(t+dt/2,s+dt*k2/2);k4,_=f(t+dt,s+dt*k3);s+=dt*(k1+2*k2+2*k3+k4)/6
  maxa=np.maximum(maxa,s[0]);maxb=np.maximum(maxb,s[2]);maxi=np.maximum(maxi,abs(s[1]));mina=np.minimum(mina,s[0]);minb=np.minimum(minb,s[2]);maxld=np.maximum(maxld,abs(s[0]-s[2]));energy+=cur**2*R*dt;maxsource=np.maximum(maxsource,cur);maxdv=np.maximum(maxdv,abs(k1[0])/1e6)
 return [dict(c,dt_s=dt,duration_s=duration,source=source,C1_peak_V=float(maxa[j]),C4_peak_V=float(maxb[j]),L1_peak_A=float(maxi[j]),L1_diff_peak_V=float(maxld[j]),C1_min_V=float(mina[j]),C4_min_V=float(minb[j]),RF1_energy_J=float(energy[j]),RF1_peak_A=float(maxsource[j]),C1_dvdt_V_per_us=float(maxdv[j]))for j,c in enumerate(cases)]
def summarize(rows):
 return {k:max(r[k]for r in rows)for k in ['C1_peak_V','C4_peak_V','L1_peak_A','L1_diff_peak_V','RF1_energy_J','RF1_peak_A','C1_dvdt_V_per_us']}
if __name__=='__main__':
 groups=[]
 for rn,ln,c4n in itertools.product([47,82,100],[3.3e-3,330e-6,220e-6],[150e-9,330e-9,470e-9]):
  cases=[dict(R=rn*rs,L=ln*ls,C1=47e-9*c1s,C4=c4n*c4s,DCR=dcr)for rs,ls,c1s,c4s,dcr in itertools.product([.95,1.05],[.9,1.1],[.95,1.05],[.9,1.1],[0.,7.08 if ln==3.3e-3 else .7])]
  rows=run(cases,dt=1e-7);groups.append({'nominal':{'R_ohm':rn,'L_H':ln,'C4_F':c4n},'maxima':summarize(rows),'corners':rows})
 (H/'value-grid.json').write_text(json.dumps({'model':'Ideal blocking bridge; unloaded linear C1-L1-C4 Pi; no MOV, source parasitics, saturation, converter or magnetic pulse rating. DCR0 is sensitivity not physical assertion.','groups':groups},indent=2)+'\n')
 print(json.dumps([{'nominal':g['nominal'],'maxima':g['maxima']}for g in groups],indent=2))
