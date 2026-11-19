from pathlib import Path
import math,json
R=2*220*.95*(1-.0004*130); Cmin=430e-9*.9; Cmax=430e-9*1.1; Vpk=253*math.sqrt(2)
def bound(A):
 tau=60e-6/math.log(2); k=R*Cmin;front=3e-6;x0=A*(1-math.exp(-front/k))
 def x(t):return x0*math.exp(-t/k)+A*tau/(tau-k)*(math.exp(-t/tau)-math.exp(-t/k))
 lo=0.;hi=.005
 for _ in range(90):
  mid=(lo+hi)/2
  if A*math.exp(-mid/tau)>x(mid):lo=mid
  else:hi=mid
 t=(lo+hi)/2;extra=(2*Vpk*A*(front+tau)+A*A*(front+tau/2))/(4*R)
 E=Vpk*Vpk/(4*R)*.0006+extra+.5*Cmax*Vpk*Vpk+.5*.0033*1.4**2
 return {'excess_V':A,'bus_max_V':Vpk+x(t),'time_after_front_s':t,'whole_pulse_extra_E_J':extra,'Cout_bound_V':math.sqrt(132**2+2*E/120e-6)}
d={'kind':'AnalyticalscalarRCopenTVSandTheveninenergybound','source_envelope':'1100V3usplateauthen60ushalfvaluetail,superimposedon357.796Vnormalpeak; singlepositivepulse only','Rmin_ohm':R,'Cmin_F':Cmin,'Cmax_F':Cmax,'inrush_max_A':Vpk/R,'RF_inrush_total_E_J':.5*Cmax*Vpk**2,'cases':[bound(1100),bound(2200)],'conditional_inputs':['Noinductiveinputfilter; noinputenergybackfeed dueD4','EffectiveCin387..473nFandRFpair>=396.264ohm','OVPinitialCout<=132V, Cmin120uF, complete response<=.6ms','ResidualLout<=3.3mHandimposedI<=1.4A;absratingisnotalimiter','Actualgenerator/probe/layout/thermalverificationstillrequired; notIECqualification'],'VDS_proposed_acceptance_max_V':680,'source_negative_budget_V':5,'layout_overshoot_budget_V':11}
(Path(__file__).parent/'rc-energy-bounds.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps(d['cases']))
