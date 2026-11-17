"""Source-conditioned commercial cooler and designed interface screens; no hardware tests."""
from pathlib import Path
import json,math,argparse,hashlib,itertools
D=Path(__file__).resolve().parent
a=argparse.ArgumentParser();a.add_argument('--source-dir',type=Path,required=True);args=a.parse_args()
sources=json.loads((D/'sources.json').read_text())
for s in sources['fresh_bytes']:
 b=(args.source_dir/s['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==s['sha256'],s['file']
C=json.loads((D/'construction.json').read_text())
def rise(name,p):
 points=C['cooler_rise_points_W_K'][name]
 assert 0<=p<=points[-1][0]
 if p<points[0][0]:return points[0][1]*(p/points[0][0])**.8 # Alpha power-law screen, not vendor low-power guarantee
 for (p0,t0),(p1,t1) in zip(points,points[1:]):
  if p0<=p<=p1:return t0+(p-p0)*(t1-t0)/(p1-p0)
 return points[-1][1]
def state(name,pd,pl,gamma,ri):
 ts=40+gamma*rise(name,pd+pl)
 return {'sink_C':ts,'primary_plate_C':ts+pd*ri,'LED_board_C':ts+pl*.25,'driver_interface_heat_W':pd,'sink_to_air_heat_W':pd+pl,'power_balance_residual_W':0.0}
rows=[]
for name,pd,pl,g,ri in itertools.product(C['cooler_rise_points_W_K'],[2,4,6],[0,4,8],[1,1.1,1.25,1.5],[.5,.85,1.2]):
 s=state(name,pd,pl,g,ri);rows.append(dict(cooler=name,driver_W=pd,light_heat_W=pl,mounting_orientation_environment_multiplier=g,driver_interface_K_per_W=ri,**s,primary_plate_le68_screen=s['primary_plate_C']<=68))
normal=[dict(cooler=n,**state(n,4,8,1.25,.85),gamma_max_for_plate68=(68-40-4*.85)/rise(n,12)) for n in C['cooler_rise_points_W_K']]
interface={
 'two_30x30mm_TIM_interfaces_K_per_W':2*.133*645.16/900,
 'AM997_ceramic_2mm_20WmK_30x30contact_K_per_W':.002/(20*.0009),
 'primary_6063_plate_2mm_through_K_per_W':.002/(150*.0009),
 'adapter_3mm_radial_annulus_screen_K_per_W':math.log(math.sqrt(58*58/math.pi)/math.sqrt(30*30/math.pi))/(2*math.pi*150*.003),
 'adapter_to_fin_end_TIM_450mm2_K_per_W':.133*645.16/450,
 'additional_contact_spreading_reserve_K_per_W':.10}
interface['sum_screen_K_per_W']=sum(interface.values());assert interface['sum_screen_K_per_W']<.85
geometry={'ceramic_square_diagonal_mm':58*math.sqrt(2),'driver_board_allocation_diagonal_mm':math.hypot(72,38),'housing_inner_diameter_mm':84,'ceramic_radial_fit_remaining_mm':(84-58*math.sqrt(2))/2,'board_radial_fit_remaining_mm':(84-math.hypot(72,38))/2,'ceramic_primary_plate_overhang_each_side_mm':(58-30)/2,'TIM_force_30x30_at10psi_N':68947.6*.0009,'fin_end_TIM_force_450mm2_at10psi_N':68947.6*.00045,'no_component_packing_or_normative_separation_proof':True}
assert geometry['ceramic_radial_fit_remaining_mm']>0 and geometry['board_radial_fit_remaining_mm']>0
# Smooth conventional shell sensitivity. This rejects only this smooth-shell concept, not all possible60mm designs.
area=math.pi*.060*.035+math.pi*.060**2/4
smooth=[{'h_assumed_W_per_m2K':h,'emissivity_assumed':em,'area_m2':area,'heat_at68C_40Cambient_W':h*area*28+em*5.670374419e-8*area*((68+273.15)**4-(40+273.15)**4)} for h,em in itertools.product([3,5,8,12],[.5,.85])]
# Fault power is derived as an allowable thermal condition, NOT supplied by the unvalidated controller.
fault=[]
for target in [80,88.6,95,105,110]:
 lo,hi=0.,40.
 for _ in range(70):
  p=(lo+hi)/2
  if state('Micro8680',p,0,1.25,.85)['primary_plate_C']<=target:lo=p
  else:hi=p
 fault.append({'plate_target_C':target,'maximum_continuous_driver_only_heat_W_for_declared_screen':lo})
# Lumped source-off cooldown; nonlinear sink loss obtained by inversion of the declared curve.
def reject_q(delta,gamma):
 if delta<=0:return 0.
 lo,hi=0.,45.
 for _ in range(45):
  p=(lo+hi)/2
  if gamma*rise('Micro8680',p)<delta:lo=p
  else:hi=p
 return (lo+hi)/2
def cool(cp,cs,dt):
 s=state('Micro8680',4,8,1.25,.85);y=[s['primary_plate_C']-40+1.866/cp,s['sink_C']-40];initial=cp*y[0]+cs*y[1];energy=0.;t=0.
 def f(y):
  q=(y[0]-y[1])/.85;out=reject_q(y[1],1.25)
  return [-q/cp,(q-out)/cs,out]
 while max(y)>5 and t<7200:
  k1=f(y);k2=f([y[i]+dt*k1[i]/2 for i in range(2)]);k3=f([y[i]+dt*k2[i]/2 for i in range(2)]);k4=f([y[i]+dt*k3[i] for i in range(2)])
  y=[y[i]+dt*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6 for i in range(2)];energy+=dt*(k1[2]+2*k2[2]+2*k3[2]+k4[2])/6;t+=dt
  assert min(y)>-1e-8
 return {'primary_heat_capacity_J_per_K_assumed':cp,'sink_heat_capacity_J_per_K_assumed':cs,'step_s':dt,'time_to_both_nodes45C_s':round(t,5),'energy_balance_residual_J':initial-energy-cp*y[0]-cs*y[1]}
cooling=[cool(cp,cs,dt) for cp,cs,dt in itertools.product([20,80],[180,360],[.5,.25])]
assert max(abs(x['energy_balance_residual_J']) for x in cooling)<1e-5
summaries=[]
for name,g in itertools.product(C['cooler_rise_points_W_K'],[1,1.1,1.25,1.5]):
 r=[x for x in rows if x['cooler']==name and x['mounting_orientation_environment_multiplier']==g]
 summaries.append({'cooler':name,'multiplier':g,'cases':len(r),'primary_plate_min_C':min(x['primary_plate_C'] for x in r),'primary_plate_max_C':max(x['primary_plate_C'] for x in r),'cases_plate_le68':sum(x['primary_plate_le68_screen'] for x in r)})
out={'scope':'Executed commercial-curve/interfacing/geometry/thermal sensitivities; no measured temperatures, qualified insulation, all-orientation guarantee or user wait.','inputs_sha256':{n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['construction.json','sources.json']},'normal12W_40C_gamma1p25_ri0p85':normal,'interface_screen':interface,'geometric_budgets':geometry,'smooth60mm_shell_sensitivities':smooth,'steady_sweep_count':len(rows),'steady_sweep_definitions':{'driver_W':[2,4,6],'light_heat_W':[0,4,8],'multiplier':[1,1.1,1.25,1.5],'interface_K_per_W':[.5,.85,1.2]},'steady_sweep_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'steady_sweep_summary':summaries,'fault_heat_frontiers':fault,'cooling_sensitivities':cooling,'limits':['gamma1.25 is a stress hypothesis inspired by another manufacturer orientation example; it is not a MechaTronix all-orientation bound. Adapter/end-cover/fixture effects are included only by that unproven multiplier.','Material thermal conductivities and TIM impedance are source-conditioned typical values plus chosen screening deratings; no guaranteed hot minimum, pressure retention or actual total interface resistance is established.','Annular radial spreading is a designed continuous-sheet surrogate; real distributed fin contacts are not a continuous annulus. Extra reserve does not validate this approximation.','C1air/core rise, individual hotspot-to-plate paths and sensor gradients/lag still require a full design/model; primary plate temperature alone does not determine them.','Source-off cooldown extrapolates low-temperature heat rejection and assumes lumped capacities and1.866J residual energy. It does not select a complete-assembly service waiting time.','All mechanical dimensions are proposed design allocations; no approved spatial intent, supplier confirmation or component placement is created.']}
(D/'results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'normal':normal,'interface':interface,'geometry':geometry,'cooling':cooling,'cases':len(rows)},indent=2))
