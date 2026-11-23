"""Read-only discrimination of coordinator-proposed input resistors.
Linear screening cannot certify a nonlinear saturated inductor or physical hardware.
"""
from pathlib import Path
import math,itertools,json
H=Path(__file__).resolve().parent
def run(R,C1,C4,L,DCR=0.,dt=5e-8):
 V=253*math.sqrt(2)
 def f(s):
  a,i,b=s
  return ((max(0,(V-a)/R)-i)/C1,(a-b-DCR*i)/L,i/C4)
 s=(0.,0.,0.);m=[0.,0.,0.];energy=0.;ldiff=0.;c1dv=V/R/C1/1e6
 for _ in range(round(.001/dt)):
  a=f(s);b=f(tuple(x+dt*y/2 for x,y in zip(s,a)));c=f(tuple(x+dt*y/2 for x,y in zip(s,b)));d=f(tuple(x+dt*y for x,y in zip(s,c)))
  s=tuple(x+dt*(aa+2*bb+2*cc+dd)/6 for x,aa,bb,cc,dd in zip(s,a,b,c,d))
  m=[max(m[0],s[0]),max(m[1],abs(s[1])),max(m[2],s[2])]
  ldiff=max(ldiff,abs(s[0]-s[2]));c1dv=max(c1dv,abs(f(s)[0])/1e6)
  energy+=max(0,(V-s[0])/R)**2*R*dt
 return {'R_ohm':R,'C1_F':C1,'C4_F':C4,'L1_H':L,'DCR_ohm':DCR,'dt_s':dt,'C1_peak_V':m[0],'L1_peak_A':m[1],'C4_peak_V':m[2],'input_resistor_energy_J':energy,'L1_differential_peak_V':ldiff,'C1_max_dVdt_V_per_us':c1dv}
groups=[]
for rn in [47,100,150]:
 rows=[run(rn*.95,c1,c4,l) for c1,c4,l in itertools.product([44.65e-9,49.35e-9],[135e-9,165e-9],[2.97e-3,3.63e-3])]
 groups.append({'R_nominal_ohm':rn,'maxima':{k:max(r[k]for r in rows)for k in ['C1_peak_V','L1_peak_A','C4_peak_V','input_resistor_energy_J','L1_differential_peak_V','C1_max_dVdt_V_per_us']},'normal60mA_power_W_with5percentR_and2percenthot':.06**2*rn*1.05*1.02,'corners':rows})
out={'actual_reviewer':'/root/simple_reality_review','requested_by_coordinator':'Root-proposed47/100/150ohm same-family input resistor discrimination; no automatic part approval or CAD changes','model':'253sqrt2V initial unloaded step, ideal bridge which blocks reverse current, initially discharged C1-L1-C4 Pi filter, RK4 50ns/1ms. L1DCR=0 is an intentional low-damping screen, not a claim that real winding resistance is zero.','groups':groups,'limitations':['All modelL1peak currents exceed its typical10percentLdrop point. Nonlinear saturation and real pulse winding behavior remain unqualified; maxima are NOT guaranteed hardware upper bounds.','No source impedance beyond nominated resistor, parasitic inductance, nonlinear diode or MOV, converter loading, retained-charge states or full surge waveform.','The current integral in this network is not fuse total-clearing I2t or safe abnormal-fault energy.','NewT1 actual windingvoltage during turn-on may depend on BPcharge/startstate; busvoltage alone is not proof of simultaneous T1stress or its absence.','Normal60mA is a retained planning current, not measured RMS or a worst-case universal bound.']}
(H/'reality.damping-screen.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{k:v for k,v in g.items()if k!='corners'}for g in groups]))
