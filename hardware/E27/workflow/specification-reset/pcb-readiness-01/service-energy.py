#!/usr/bin/env python3
"""Coupled passive-energy discharge envelope; not a measured user waiting time."""
from pathlib import Path
import json,math
D=Path(__file__).resolve().parent
Cbulk=18e-6; Cdd=.94e-6*1.05*1.003; Cout_max=20.592e-6;Cout_min=8e-6
Rbulk=499000*1.021;Rdd=1e6*1.021;Rout=10000*1.021
# Deliberately loose capacitor-rating ceilings, not normal operating voltages.
E0=.5*Cbulk*450**2+.5*Cdd*50**2+.5*Cout_max*63**2+.001
Egoal=min(.5*Cout_min*5**2,.5e-3)
tau_mag_condition=.003/.001 # trace(L)<=3mH and each winding R>=1mohm
rows=[]
for name,rb in [('two_bulk_branches',Rbulk),('one_bulk_branch_open',2*Rbulk),('one_bulk_bleeder_short',Rbulk*2/3)]:
 tau=max(rb*Cbulk,Rdd*Cdd,Rout*Cout_max,tau_mag_condition)
 t=tau/2*math.log(E0/Egoal)
 rows.append({'case':name,'bulk_equivalent_R_max_ohm':rb,'slowest_energy_tau_s':tau,'initial_energy_upper_J':E0,'energy_target_J':Egoal,'time_to5V_energy_envelope_s':t,'energy_upper_at100s_J':E0*math.exp(-200/tau),'Vout_upper_at100s_V':math.sqrt(2*E0/Cout_min)*math.exp(-100/tau)})
assert all(x['Vout_upper_at100s_V']<5 and x['energy_upper_at100s_J']<.5e-3 for x in rows)
cool=[]
for ti,tau in [(68,x) for x in [30,60,120,300]]+[(80,x) for x in [30,60,120,300]]:
 cool.append({'initial_surface_C_hypothesis':ti,'ambient_C':40,'thermal_time_constant_s_hypothesis':tau,'time_to45C_s':tau*math.log((ti-40)/(45-40))})
result={'kind':'mathematical conditional energy envelope and illustrative cooling sensitivity, not physical measurements or approved user instructions','proof':'If every stored-energy mode has E_dot<=-2E/tau_max and conversion is passive with no external source after unplugging, arbitrary redistribution still gives E_total(t)<=E0exp(-2t/tau_max). Vout<=sqrt(2E_total/Cout_min). Dedicated resistors establish capacitor-mode terms; a PSD magnetic L matrix obeys L/R<=trace(L)/min(R).','conditions':['R13 and both output bleeders remain intact in these three scenarios; this is not every single component fault.','All initial capacitor voltages are no greater than the stated loose rating ceilings450/50/63V, with total other initial stored energy<=1mJ. This does not rate the whole circuit for those voltages.','Cout total<=20.592uF and permanent base output capacitance>=8uF; any added panel/input storage must be included independently.','Trace of actual winding self-inductance matrix<=3mH and every winding DCresistance>=1mohm; omitted reactive modes must not have a slower energy-decay constant than the selectedtau. These are acceptance conditions, not a fresh physical measurement.','No battery/external backfeed, primary reinsertion, active negative resistance or energy source is present after unscrewing.','A missing R13, outputbleeder failure, winding fault or unbounded external panel capacitance requires another assessment; the proof cannot waive them.'],'storage':{'Cbulk_max_F':Cbulk,'Cdd_max_F':Cdd,'Cout_total_max_F':Cout_max,'Cout_permanent_min_F':Cout_min,'magnetic_tau_upper_condition_s':tau_mag_condition},'cases':rows,'electrical_design_screen_s_not_user_instruction':100,'cooling_sensitivities':cool,'user_wait_not_selected':'An actual user wait is at least max(verified complete-assembly electrical discharge, verified cooling to45C) under accepted conditions, with measurement uncertainty and margins.100s is only this conditional electrical screen; cooler/hotter real structures can require longer.'}
(D/'service-energy.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'cases':rows,'cooling_examples':cool[:4]},indent=2))
