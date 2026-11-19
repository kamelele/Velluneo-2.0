"""Source-bound first-order screens for the selected33-part basis; no IC simulation."""
from pathlib import Path
import json,math,itertools,hashlib
D=Path(__file__).resolve().parent;parts={p['ref']:p for p in json.loads((D/'design/proposed-parts.json').read_text())}
assert parts['U1']['mpn']=='UCC28701DBVR'and parts['Q1']['mpn']=='STF2N80K5'
LP=.002304;R4,R5,R6,R9=80600.,17400.,1400.,2.32;NPA=120/22;VB=253*math.sqrt(2);AE=57e-6
td_eq=R6*LP/(25*R4*R9*NPA)
comp=[]
for ns in(50,69,101,td_eq*1e9,150,200):
 td=ns*1e-9;ideal=25*R4*R9*td*NPA/LP;err=VB/LP*td-(VB/NPA/R4/25)*R6/R9
 comp.append(dict(assumed_total_delay_ns=ns,RLC_ideal_ohm=ideal,first_order_peak_current_residual_A=err))
corners=[]
for lp,rcs,rupper,rlc,klc,td,vcst in itertools.product((LP*.9,LP*1.1),(R9*.979,R9*1.021),(R4*.979,R4*1.021),(R6*.979,R6*1.021),(23.,28.),(50e-9,200e-9),(.715,.775)):
 error=VB/lp*td-(VB/NPA/rupper/klc)*rlc/rcs;ip=vcst/rcs+error
 corners.append(dict(Lp_H=lp,RCS_ohm=rcs,Rupper_ohm=rupper,RLC_ohm=rlc,KLC=klc,assumed_delay_s=td,VCS_threshold_V=vcst,peak_A=ip,first_order_flux_T=lp*ip/(120*AE)))
ocp=1.6/(R9*.979);ocpE=.5*LP*1.1*ocp**2;ntc=1/(1/298.15+math.log((.95/105e-6)/100000)/4100)-273.15
cv=4.05*(1+R4/R5)*30/22-.8
aux=[dict(assumed_output_V=v,ideal_aux_VDD_V=(v+.8)*22/30-.8,below_nominal_CV_boundary=v<cv)for v in(20,26,32)]
fault_sink=(VB-8.45)/(804000*.979)-8.45/(80600*1.021)
startup=[]
for vac,rf,bf,cf,leak,drop in itertools.product((207,253),(.979,1.021),(.979,1.021),(.95,1.05),(3e-6,20e-6),(0,5)):
 rs0=804000*rf;rb0=80600*bf;cc0=.94e-6*cf;bulk=vac*math.sqrt(2)-drop;parallel=1/(1/rs0+1/rb0);vinf=parallel*(bulk/rs0-1.5e-6-leak);assert vinf>23
 startup.append(dict(Vac=vac,assumed_bulk_drop_V=drop,Rstartup_ohm=rs0,Rbleed_ohm=rb0,Ctotal_F=cc0,assumed_D2_leak_A=leak,equilibrium_V=vinf,conditional_time_to23_s=-parallel*cc0*math.log(1-23/vinf)))
# This declared conservative load combines incompatible datasheet maxima as a budget,
# not a realizable guaranteed IC waveform or a measured hold-up interval.
run_load=2.65e-3+5e-9*140000;rb=80600*.979;rs=804000*1.021;cc=.94e-6*.95
lo=8.45;hi=19.;load=run_load+hi/rb-(207*math.sqrt(2)-hi)/rs;hold=cc*(hi-lo)/load
result=dict(status='Owner-selected33 basis; first-order engineering screens, not qualified operating proof',basis_parts_sha256=hashlib.sha256((D/'design/proposed-parts.json').read_bytes()).hexdigest(),R6_function='RLC line-compensation resistor. No explicit external CS capacitor in the graph.',R6_retained_ohm=R6,R6_equivalent_delay_ns=td_eq*1e9,RLC_source_equation='RLC=KLC*Rupper*RCS*TD*(NP/NA)/LP',delay_sensitivity=comp,conditional_current_corner_count=len(corners),conditional_peak_current_range_A=[min(x['peak_A']for x in corners),max(x['peak_A']for x in corners)],conditional_max_first_order_flux_T=max(x['first_order_flux_T']for x in corners),static_OCP_peak_A=ocp,static_OCP_flux_T=LP*1.1*ocp/(120*AE),single_pulse_OCP_stored_energy_J=ocpE,nominal_CV_boundary_V=cv,ideal_auxiliary_cases=aux,NTC_nominal_trip_C=ntc,NTC_guaranteed_trip_window_available=False,NTC_open_guaranteed_shutdown=False,fault_sink_needed_at8p45_A=fault_sink,minimum_guaranteed_fault_sink_available=False,R13_max_dissipation_at35_W=35**2/(80600*.979),conditional_gate_charge_time_at20mA_s=5e-9/.020,conditional_Miller_time_at20mA_s=3.7e-9/.020,declared_worst_budget_hold_up_19_to8p45_s=hold,hold_up_load_budget_A=load,powered_test_performed=False,IC_native_simulation_performed=False,assumptions=['TotalTD50-200ns is an engineering sensitivity interval, not guaranteed ST or TI timing.','ST Qg5nC/Qgd3.7nC/Rg18ohm are typical at source test conditions, not maximum bounds.','LP±10%,R4/R6/R9±2.1%,KLC23/28,VCS.715/.775 are independently swept; no correlated IC behavioral model.','Normal32V CC operation is not established:32V exceeds the conditional nominalCV30.305V. Prior32V energy cases are envelope diagnostics, not proof of CC capability.','Flux assumes zero residual flux and A_min57mm2; no saturation/remanence/reset-fault qualification.','OCP screen is one pulse; energy*140kHz is not a realizable fault-power claim.','NTC beta/current/threshold nominal calculation does not establish a guaranteed protection window or open-sensor fail-safe.','Startup-feed ceiling excludes auxiliary/surge/commutation injection; no minimum fault draw is guaranteed.','Hold-up uses a declared conservative additive current budget, no complete start-up or UVLO/handoff model.'])
result.update(startup_case_count=len(startup),startup_cases=startup,conditional_worst_time_to23_s=max(r['conditional_time_to23_s']for r in startup),conditional_min_startup_equilibrium_V=min(r['equilibrium_V']for r in startup),normal_line_startup_feed_only_zero_draw_ceiling_V=VB*(80600*1.021)/(804000*.979+80600*1.021),startup_datum_caveat='1.5uA specified at18V; DC charging law/leakage assumptions are not a guaranteed IC transient model.',source_CS_threshold_and_frequency_limits_are_average_levels=True,individual_cycle_peak_current_or_frequency_bound_proven=False)
result['assumptions'].append('TI SLUSB41A p5/p6 footnote(1): EMI modulation means the quoted CS thresholds and switching-frequency limits are average levels. The conditional range is not an individual-cycle peak-current bound, and140kHz is not a proven individual-cycle frequency ceiling.')
(D/'controller-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items()if k not in('assumptions','delay_sensitivity','startup_cases')},indent=2))
