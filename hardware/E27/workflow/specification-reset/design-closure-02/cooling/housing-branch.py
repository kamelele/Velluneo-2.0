"""Designed secondary-domain housing heat-rejection branch; property/geometry-conditioned screen."""
from pathlib import Path
import json,math,itertools,hashlib,ast
D=Path(__file__).resolve().parent;C=json.loads((D/'construction.json').read_text())
tree=ast.parse((D/'calculate.py').read_text());ns={'C':C};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='rise'],type_ignores=[]),'cooler_curve','exec'),ns);rise=ns['rise']
A=math.pi*.09*.045+math.pi*(.09**2-.027**2)/4
Rneck=.004/(4*150*.005*.003);Rh=Rneck+.10
def reject(t,h,em,vf):return A*(h*(t-40)+em*vf*5.670374419e-8*((t+273.15)**4-313.15**4))
def temp_for_power(p,h,em,vf):
 lo,hi=40.,250.
 for _ in range(70):
  t=(lo+hi)/2
  if reject(t,h,em,vf)<p:lo=t
  else:hi=t
 return (lo+hi)/2
def steady(h,em,vf,gamma):
 lo,hi=0.,12.
 for _ in range(65):
  q=(lo+hi)/2;tm=40+gamma*rise('Micro8650',12-q);th=temp_for_power(q,h,em,vf)
  if tm>th+q*Rh:lo=q
  else:hi=q
 q=(lo+hi)/2;tm=40+gamma*rise('Micro8650',12-q);th=temp_for_power(q,h,em,vf)
 assert abs(tm-th-q*Rh)<1e-9 and abs(q-reject(th,h,em,vf))<1e-9
 residual=12-(12-q)-(tm-th)/Rh
 assert abs(residual)<1e-8
 return {'h_housing_W_per_m2K_hypothesis':h,'emissivity_hypothesis':em,'radiation_effective_view_factor_hypothesis':vf,'cooler_multiplier_hypothesis':gamma,'sink_adapter_C':tm,'housing_surface_C':th,'primary_plate_C':tm+4*.85,'LED_board_C':tm+8*.25,'housing_heat_W':q,'commercial_cooler_heat_W':12-q,'heat_balance_residual_W':residual,'primary_plate_le68_screen':tm+4*.85<=68}
rows=[steady(*p) for p in itertools.product([0,3,5],[.5,.85],[.5,1],[1.1,1.25,1.5])]
selected=steady(3,.85,1,1.25)
radiation_only=steady(0,.85,.75,1.25)
lo,hi=0.001,1.
for _ in range(60):
 e=(lo+hi)/2
 if steady(0,e,1,1.25)['primary_plate_C']>68:lo=e
 else:hi=e
effective_emissivity_viewfactor_min=hi
# Derive allowable multiplier under the chosen housing properties; never call them guaranteed physical minima.
lo,hi=1.,3.
for _ in range(60):
 g=(lo+hi)/2
 if steady(3,.85,1,g)['primary_plate_C']<=68:lo=g
 else:hi=g
out={'kind':'Executed alternative geometry/network proposal; not approved housing, actual convection/emissivity or all-orientation/insulation proof','id':'C2b','envelope_mm':[90,173],'relative_to_C0_60x120_mm':{'diameter_increase':30,'height_increase':53},'material':'6063-T6 secondary-domain black-anodized housing; exterior not connected to primary nodes','geometry_mm':{'housing_OD':90,'housing_ID':84,'housing_height':45,'primary_inner_cover_OD_proposal':82,'primary_inner_cover_wall_unqualified':3,'primary_inner_space_diameter':76,'reserved_board_box':[66,32,23],'board_diagonal':math.hypot(66,32),'no_component_placement_or_normative_minimum_claim':True},'heat_path':{'area_m2_outer_side_plus_cap_annulus':A,'neck_count':4,'neck_length_max_mm':4,'neck_width_min_mm':5,'neck_thickness_min_mm':3,'metal_k_screen_WmK':150,'neck_resistance_K_per_W':Rneck,'joint_resistance_screen_K_per_W':.1,'total_adapter_housing_screen_K_per_W':Rh,'geometry_status':'New designed integral neck/adapter/housing interface; actual machining/tolerance/contact structure remains to be confirmed. No conductive neck crosses primary ceramic barrier.'},'chosen_hypothesis_case':selected,'radiation_only_no_convection_hypothesis':radiation_only,'required_emissivity_times_viewfactor_for68C_no_convection_screen':effective_emissivity_viewfactor_min,'cooler_multiplier_max_for68C_under_chosen_housing_properties':lo,'cases':rows,'checks':{'case_count':len(rows),'maximum_abs_heat_balance_W':max(abs(r['heat_balance_residual_W']) for r in rows)},'source_and_input_sha256':{n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['construction.json','calculate.py','sources.json']},'limits':['The added housing branch is actual proposed dimensions/material/neck geometry, but convection/emissivity/view factor are hypotheses. It cannot be called demonstrated cooling or an all-orientation bound.','Radiation orientation is irrelevant only for unchanged view factors and isothermal surroundings. Ventilated fixtures, cap/support shadow and diffuser feedback can alter view factor and ambient temperature.','C2b needs smaller66x32 board allocation to fit its added primary inner cover. Complete31-position packing, contact access and actual barriers remain unresolved before PCB.','Normal4W/8W heat levels, individual component-to-plate paths, C1air/core and sensor gradients/lag remain separate acceptance conditions.','Selected black-anodize emissivity.85 must be confirmed for actual process/temperature; color or nominal finish is insufficient. No coating is treated as electrical insulation.']}
(D/'housing-branch.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'C2b_selected_hypothesis':selected,'gamma_limit':lo,'geometry':out['geometry_mm'],'network':out['heat_path'],'checks':out['checks']},indent=2))
