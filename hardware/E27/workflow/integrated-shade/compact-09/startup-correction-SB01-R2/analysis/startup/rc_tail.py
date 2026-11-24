from rc_screen import H
import numpy as np, math,itertools,json
cases=[dict(RF=rf,R=r,C1=49.35e-9,C4=165e-9,VAC=253,phase_deg=ph,a0=a,b0=b)for rf,r,ph,a,b in itertools.product([43.757,50.337],[87.75,112.75],[0,45,90,135],[0,357.8],[0,357.8])]
n=len(cases);RF=np.array([c['RF']for c in cases]);R=np.array([c['R']for c in cases]);C1=np.array([c['C1']for c in cases]);C4=np.array([c['C4']for c in cases]);phase=np.array([c['phase_deg']*math.pi/180 for c in cases]);s=np.array([[c['a0']for c in cases],[c['b0']for c in cases]],dtype=float);tailP=np.zeros(n);tailv=np.zeros(n);dt=2e-7
def f(t,s):
 v=253*math.sqrt(2)*np.abs(np.sin(2*math.pi*50*t+phase));ib=np.maximum(0.,(v-s[0])/RF);ir=(s[0]-s[1])/R
 return np.array([(ib-ir)/C1,ir/C4])
for k in range(round(.02/dt)):
 t=k*dt;k1=f(t,s);k2=f(t+dt/2,s+dt*k1/2);k3=f(t+dt/2,s+dt*k2/2);k4=f(t+dt,s+dt*k3);s+=dt*(k1+2*k2+2*k3+k4)/6
 if t>=.001:
  p=(s[0]-s[1])**2/R;tailP=np.maximum(tailP,p);tailv=np.maximum(tailv,abs(s[0]-s[1]))
out={'kind':'UnloadedRCtailcheckonly; excludesactivebuckload/surge/parasitics','initial_window_s':[0,.001],'tail_window_s':[.001,.02],'dt_s':dt,'tail_R10_max_W':float(max(tailP)),'tail_R10_max_V':float(max(tailv)),'cases':[dict(c,tail_R10_W=float(tailP[j]),tail_R10_V=float(tailv[j]))for j,c in enumerate(cases)]}
(H/'rc-tail.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='cases'}))
