#!/usr/bin/env python3
"""Reproducible electrical design checks and explicit unapproved ECO.
No claim of complete converter simulation, physical verification or safety certification.
"""
from pathlib import Path
import hashlib,json,math,itertools,argparse,bisect
pa=argparse.ArgumentParser();pa.add_argument('--cree-pdf',required=True);pa.add_argument('--crcw-pdf',required=True);a=pa.parse_args()
P=Path(__file__).resolve().parent.parent;D=P/'electrical-integration'
cf=Path(a.cree_pdf);rf=Path(a.crcw_pdf)
assert hashlib.sha256(cf.read_bytes()).hexdigest()=='74d4261952c25e6833212a82b0f72e759f8297478627a368f4acff22378c92c8'
assert hashlib.sha256(rf.read_bytes()).hexdigest()=='773514dbb68319dd7a3b8d381a81798f8bb0a82cf65ecf440ec201dad810e7c5'
parent=P/'finalization/support-results.json';assert hashlib.sha256(parent.read_bytes()).hexdigest()=='7b031346b2cf2c45744198094e863111ea0efcbaa1a992b4bde0ce05224d1314'
x=json.loads(parent.read_text());factors=[.979,1.021];V0=253*math.sqrt(2);Cmax=18e-6;R=499000
# Pure passive capacitor+bleeder network, NOT complete lamp/service delay.
bleed=[]
for voltage in [V0,400.0]:
 for state in ['healthy','one_resistor_open','one_resistor_short']:
  eq=[];maxp=0.;maxv=0.
  for rs in itertools.product(factors,repeat=4):
   vals=[R*r for r in rs]
   if state=='one_resistor_open':vals[0]=math.inf
   if state=='one_resistor_short':vals[0]=0
   branch=[vals[0]+vals[1],vals[2]+vals[3]];req=1/sum(0 if math.isinf(b) else 1/b for b in branch)
   eq.append(req)
   for i in range(4):
    rb=branch[i//2];vv=(voltage if math.isinf(vals[i]) else 0) if math.isinf(rb) else voltage*vals[i]/rb
    pp=0 if math.isinf(vals[i]) or vals[i]==0 else vv*vv/vals[i]
    maxp=max(maxp,pp);maxv=max(maxv,vv)
  bleed.append({'initial_voltage_V':voltage,'state':state,'Req_ohm':[min(eq),max(eq)],'passive_only_time_to5V_s':max(eq)*Cmax*math.log(voltage/5),'max_element_V':maxv,'max_element_W':maxp,'CRCW2512_voltage_screen500V':maxv<500,'CRCW2512_P125_screen_W':(155-125)/(155-70),'power_screen_within_P125':maxp<(155-125)/(155-70)})
existing={'normal_per_resistor_V':V0/2,'one_short_remaining_resistor_V':V0,'source1206_voltage_max_V':200,'one_short_exceeds_working_voltage':V0>200,'one_open_passive_discharge_bound':'absent, one series chain is broken','highline_nominal_bleed_W':V0*V0/(2*R)}
# New1M VDD bleed current/RC is separate from startup source-law proof.
bias={'proposed_R_ohm':1e6,'source0603_voltage_max_V':75,'worst_recommended_VDD35_draw_A':35/(1e6*.979),'worst23V_start_draw_A':23/(1e6*.979),'power_at35V_W':35**2/(1e6*.979),'RCmax_s_assuming_Cdd1uF':1e6*1.021*1e-6,'passive_only23to5V_s':1e6*1.021*1e-6*math.log(23/5),'internalHV_auxiliary_paths_not_modeled':True}
# Native vector curve, not hand-picked graph percentages. Axis anchors are the PDF's exact grid.
import fitz
with fitz.open(cf) as doc:
 page=doc[5];ds=page.get_drawings();curve=ds[14];frame=ds[9]['rect']
 assert abs(curve['color'][1]-.333)<.001 and len(curve['items'])==11
 x0=frame.x0;x480=468.6102600097656;y0=frame.y1;y750=frame.y0
 pts=[]
 for item in curve['items']:
  assert item[0]=='c'
  p0,p1,p2,p3=item[1:]
  for j in range(101):
   t=j/100;u=1-t;xx=u**3*p0.x+3*u*u*t*p1.x+3*u*t*t*p2.x+t**3*p3.x;yy=u**3*p0.y+3*u*u*t*p1.y+3*u*t*t*p2.y+t**3*p3.y
   pts.append(((xx-x0)/(x480-x0)*480,(y0-yy)/(y0-y750)*7.5))
pts.sort();xs=[p[0] for p in pts]
def mult(mA):
 i=bisect.bisect_left(xs,mA);assert 0<i<len(pts);(x1,y1),(x2,y2)=pts[i-1],pts[i];return y1+(mA-x1)*(y2-y1)/(x2-x1)
# Preserve the source-curve as a derived numerical artefact, not manufacturer min/max limits.
(D/'native-typical-flux-curve.json').write_text(json.dumps({'source_sha256':hashlib.sha256(cf.read_bytes()).hexdigest(),'PDFpage':6,'curve_drawing_index':14,'axis_grid':[x0,x480,y0,y750],'units':['mA','relative_flux_at55mA'],'samples':pts,'typical_curve_not_guaranteed':True},indent=2)+'\n')
ib=x['correlated_normal_linecomp_witness']['bounds']['corrected_CC_A_proxy'];mlo,mhi=mult(1000*ib[0]),mult(1000*ib[1]);nom=mult(250)
optics={'source_current_screen_A':ib,'source_current_screen_not_actual_controller_guarantee':True,'relative_typical_flux_at_screen_ends':[mlo,mhi],'relative_typical_flux250mA':nom,'typical_flux_ratio_due_to_current_screen':mhi/mlo,'allowed_whole_lamp_ratio850over750':850/750,'counterexample_to_guarantee_under_stated_screen':mhi/mlo>850/750,'not_proof_all_hardware_fails':True,'three_nominal_screens_lm':{},'manufacturing_bin_and_Tj_current_separability_not_guaranteed':True}
for cct,n,hot in [('2700',8,27.2),('4000',7,30.),('6500',7,29.9)]:optics['three_nominal_screens_lm'][cct]={'count':n,'nominal250mA_lm':n*hot*.87*nom,'current_screen_lm':[n*hot*.87*mlo,n*hot*.87*mhi]}
# Target-interface/power budgets, not achieved hardware limits.
power={'proposed_panel_normal_V':[18,27],'proposed_interface_max_normal_current_A':.300,'panel_max_DC_power_target_W':27*.300,'base_output_bleed_at27V_W':27**2/(10000*.979),'normal_base_bleed_old_at_highline_W':existing['highline_nominal_bleed_W'],'proposed_normal_primary_bleed_nominal_highline_W':V0**2/R,'added_normal_primary_bleed_W':V0**2/(2*R),'LED_board_solder_temperature_goal_C':85,'ambient_max_C':40,'all_LED_power_as_heat_conservative_R_to_ambient_K_W':(85-40)/(27*.300),'proposed_driver_heat_budget_W':2.5,'whole10p6W_heat_path_budget_K_W':(85-40)/(27*.300+2.5),'not_a_measured_thermal_resistance_or_material_limit':True}
result={'status':'calculated screens and unapproved ECO proposal; noCAD/physicaltest/order','input_hashes':{'support-results':hashlib.sha256(parent.read_bytes()).hexdigest(),'CRCW':hashlib.sha256(rf.read_bytes()).hexdigest(),'Cree':hashlib.sha256(cf.read_bytes()).hexdigest()},'existing_bleeder_findings':existing,'ECO_four2512_499k_branch_corner_cases':bleed,'new_VDD_bleed':bias,'optics':optics,'target_power_and_thermal_budgets':power,'service_access_scope':'RC numbers concern the isolated passive subcircuit; upstream energy transfer, single faults elsewhere and cooling still prevent a measured complete-lamp waiting-time claim.'}
(D/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
