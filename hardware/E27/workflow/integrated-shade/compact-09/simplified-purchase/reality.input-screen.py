"""Independent review calculation, not a nonlinear bound or design implementation."""
from pathlib import Path
import math,json,hashlib
H=Path(__file__).resolve().parent
def trial(dt=2.5e-8):
 V=253*math.sqrt(2);R=9.5;C1=44.65e-9;C4=135e-9;L=3.63e-3;DCR=7.08
 def f(s):
  a,i,b=s
  return ((max(0,(V-a)/R)-i)/C1,(a-b-DCR*i)/L,i/C4)
 s=(0.,0.,0.);m=[0.,0.,0.]
 for _ in range(round(.001/dt)):
  a=f(s);b=f(tuple(x+dt*y/2 for x,y in zip(s,a)));c=f(tuple(x+dt*y/2 for x,y in zip(s,b)));d=f(tuple(x+dt*y for x,y in zip(s,c)))
  s=tuple(x+dt*(aa+2*bb+2*cc+dd)/6 for x,aa,bb,cc,dd in zip(s,a,b,c,d))
  m=[max(m[0],s[0]),max(m[1],abs(s[1])),max(m[2],s[2])]
 return {'dt_s':dt,'C1_peak_V':m[0],'L1_peak_A':m[1],'C4_peak_V':m[2]}
out={'reviewer':'/root/simple_reality_review','review_calculation':'Initial unloaded peak-line step through ideal blocking bridge and RF1-C1-L1-C4 Pi network','parameters':{'VAC':253,'Rin_ohm':9.5,'C1_F':44.65e-9,'C4_F':135e-9,'L1_H':3.63e-3,'L1_DCR_ohm':7.08,'initial_conditions':[0,0,0],'time_s':.001},'results':[trial(),trial(1.25e-8)],'limitations':['Linear L1 is invalid once its quoted small-signal/10%-drop envelope is exceeded. This is an overvoltage flag, NOT a guaranteed upper bound.','No source impedance beyond RF1, no measured parasitics/MOV/nonlinear inductance/converter load.','Higher-voltage C1 alone does not prove retained C4, L1, U1, MOV or surge/fault adequacy.','Calculation is a read-only review finding, not an implemented fix, physical measurement or order/energization authorization.']}
(H/'reality.input-screen.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['results']))
