#!/usr/bin/env python3
"""Source-conditioned life and required thermal-path budgets, not temperature prediction."""
from pathlib import Path
import json,math,hashlib,itertools,argparse
D=Path(__file__).resolve().parent;P=D.parent.parent
a=argparse.ArgumentParser();a.add_argument('--source-dir',required=True,type=Path);args=a.parse_args()
native=json.loads((D/'sources.json').read_text())['fresh_bytes']
for s in native:
 assert hashlib.sha256((args.source_dir/s['file']).read_bytes()).hexdigest()==s['sha256'],s['file']
C=json.loads((D/'design-contract.json').read_text())
assert abs(sum(C['component_heat_allocations_W'].values())-C['driver_loss_budget_W'])<1e-12
source=P/'electrical-refinement/capacitor/results.json';cap=json.loads(source.read_text())
assert all(r['remaining_load_W']==11 for r in cap['rows'])
ib=max(r['Ib_rms'] for r in cap['rows']);rin_loss=ib*ib*47*1.021
RATED=10000.;TMAX=105.;target=C['bulk_life_target_operating_hours']
def rubycon_lower(ta,rise):
 assert 0<=rise<=20
 # Eq17, lead-wire105C: drop nonnegative reference-ripple heating credit.
 return RATED*2**((TMAX-ta)/10-rise/(10-.25*rise))
def panasonic_screen(ta,rise):
 # Source equation at conservative referenceT1=105C; no rated-ripple heat credit.
 return RATED*2**((105-ta-rise)/10)
life=[]
for ta,rise in itertools.product([60,70,75,80,85,90],[0,2,5,10,15,20]):
 life.append({'ambient_at_capacitor_C':ta,'actual_core_rise_K':rise,'rubycon_eq17_lower_screen_h':rubycon_lower(ta,rise),'meets21900h_screen_only':rubycon_lower(ta,rise)>=target,'panasonic_equation_screen_h':panasonic_screen(ta,rise)})
inverse=[]
for rise in [0,2,5,10,15,20]:
 inverse.append({'core_rise_K':rise,'rubycon_local_air_max_for21900h_C':105-10*(math.log2(target/RATED)+rise/(10-.25*rise)),'panasonic_local_air_max_screen_C':105-rise-10*math.log2(target/RATED)})
def two_node(pd,pl,rd,rl,rx):
 gd,gl=1/rd,1/rl;gx=0 if math.isinf(rx) else 1/rx;det=(gd+gx)*(gl+gx)-gx*gx
 dd=(pd*(gl+gx)+pl*gx)/det;dl=(pl*(gd+gx)+pd*gx)/det
 kd=gd*dd+gx*(dd-dl);kl=gl*dl+gx*(dl-dd)
 assert abs(kd-pd)<1e-10 and abs(kl-pl)<1e-10
 assert max(dd,dl)<=max(pd*rd,pl*rl)+1e-10
 return {'driver_C':40+dd,'light_compartment_C':40+dl,'network_residual_W':max(abs(kd-pd),abs(kl-pl))}
network=[]
for pd,pl,rx in itertools.product([0,2,4],[0,4,8],[1,5,30,100,float('inf')]):
 network.append({'driver_W':pd,'light_W':pl,'cross_coupling_K_per_W':None if math.isinf(rx) else rx,**two_node(pd,pl,7,3.5,rx)})
assert max(max(x['driver_C'],x['light_compartment_C']) for x in network)<=68+1e-10
hotspot=[]
for ref,allocation in [('Q1','Q1_channel_and_switching'),('TVS1','TVS1_and_clamp_diode'),('T1','T1_all_winding_core_termination'),('D3','D3_output_rectifier'),('R1','R1_input_limiter'),('U1','U1_bias_gate_system')]:
 p=C['component_heat_allocations_W'][allocation];hotspot.append({'component':ref,'loss_allocation_W':p,'hotspot_target_C':C['hotspot_targets_C'][ref],'required_hotspot_to70Cnode_max_K_per_W':(C['hotspot_targets_C'][ref]-70)/p})
sigma=5.670374419e-8;area=[]
for dia,h,em,ts in itertools.product([.060,.070],[4,8,12],[.2,.9],[60,70,80]):
 ta=40.;conv=h*(ts-ta);rad=em*sigma*((ts+273.15)**4-(ta+273.15)**4);a=12/(conv+rad)
 area.append({'diameter_m_reference_only':dia,'convection_assumed_W_per_m2K':h,'emissivity_assumed':em,'surface_C':ts,'required_effective_exposed_area_m2_for12W':a,'full_sphere_reference_area_m2':math.pi*dia*dia,'area_ratio_to_full_sphere':a/(math.pi*dia*dia)})
sup=json.loads((P/'finalization/support-results.json').read_text());cond=sup['correlated_normal_linecomp_witness']['bounds']
irms=cond['primary_RMS_A'][1];fs=cond['f_Hz'][1]
switch=[]
for rds in [16,32,48,64]:
 pc=irms**2*rds;reserve=.9-pc
 switch.append({'Rds_ohm_sensitivity_not_hot_guarantee':rds,'conditional_conduction_W':pc,'remaining_of_Q1_0p9W_allocation_W':reserve,'allowed_additional_average_cycle_energy_J':reserve/fs if reserve>=0 else None})
checks={'network_case_count':len(network),'network_energy_balance_max_W':max(x['network_residual_W'] for x in network),'maximum_node_C_for_proposed_budgets':max(max(x['driver_C'],x['light_compartment_C']) for x in network),'life_monotonic_checks':all(rubycon_lower(70,x)>=rubycon_lower(70,x+1) for x in range(20)),'allocations_sum_W':sum(C['component_heat_allocations_W'].values())}
assert checks['life_monotonic_checks']
result={'kind':'calculated design requirements and manufacturer-equation screens; no actual assembly temperatures or lifetime qualification','source_input_sha256':{'design-contract.json':hashlib.sha256((D/'design-contract.json').read_bytes()).hexdigest(),'prior_capacitor_results':hashlib.sha256(source.read_bytes()).hexdigest(),'support-results':hashlib.sha256((P/'finalization/support-results.json').read_bytes()).hexdigest()},'inherited11W_bridge_witness':{'max_bridge_rms_A':ib,'R1_47ohm_plus2p1pct_loss_W':rin_loss,'scope':'unchanged finite-R energy scheduled model only; no larger-power/fault/ripple or temperature guarantee'},'rubycon_eq17_conservative_at_target_h':rubycon_lower(70,10),'life_sweep':life,'required_life_temperature':inverse,'coupled_network':network,'hotspot_requirements':hotspot,'surface_area_sensitivities':area,'Q1_sensitivity':switch,'checks':checks,'limits':['No actual thermal resistance, enclosure, convection coefficient or emissivity is established by this inverse design.','Rubycon reference-ripple core rise was unknown, so nonnegative credit is dropped; all actual rises are inputs, not inferred from can temperature.','Do not transfer Rubycon formula to Panasonic; separate source equation is screened at T1=105C without heating credit. Neither is a demonstrated lifetime.','Q1RthJA38K/W is conditioned on source1inch2FR4/2oz and does not qualify this PCB. Coss_eq9.5pF is time-equivalent, not an energy-equivalent capacitance.','Fault power, NTCopen/passive safety, sensor gradients/lag and all actual materials/layout remain to be established.']}
(D/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'checks':checks,'R1loss_W':rin_loss,'rubycon70C10K_screen_h':result['rubycon_eq17_conservative_at_target_h'],'hotspot_requirements':hotspot},indent=2))
