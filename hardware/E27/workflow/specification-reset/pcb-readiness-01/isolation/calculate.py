#!/usr/bin/env python3
"""Source-pinned insulation construction and geometry budgets; no compliance claim."""
from pathlib import Path
import argparse,hashlib,json,math,re,html
D=Path(__file__).resolve().parent; P=D.parents[1]
a=argparse.ArgumentParser();a.add_argument('--source-dir',type=Path,required=True);args=a.parse_args()
reg=json.loads((D/'sources.json').read_text()); checked=[]
for x in reg['downloaded_sources']:
 p=args.source_dir/x['filename'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==x['sha256'],p
 checked.append({'filename':x['filename'],'sha256':x['sha256'],'bytes':len(b)})
for x in reg['repository_inputs']:
 p=P/x['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'],p
f=(args.source_dir/'ul-fis-b3.html').read_text();t=html.unescape(re.sub('<[^>]+>',' ',f));t=re.sub(r'\s+',' ',t)
for marker in ['FIS-B3','1350F-1','SUMIKON PM-9630','TEX-E']:assert marker in t,marker
assert 'MW=82' in f or re.search(r'MW\s+82',t)
c=json.loads((D/'construction-candidate.json').read_text())
assert c['turns']=={'P':120,'A':22,'S':30};assert c['winding_pins']=={'P':['1','5'],'A':['2','4'],'S':['6','10']}
assert c['tape_wraps']['P_to_A']>=2, 'Selected FIS-B3 1350F-1 interwinding entry requires two layers'
g=json.loads((P/'transformer-footprint/geometry-contract.json').read_text());pads={p['number']:p for p in g['pads']}
primary=['1','2','4','5'];secondary=['6','10'];pair=[]
for p in primary:
 for s in secondary:
  pa,pb=pads[p],pads[s];dx=abs(pa['at'][0]-pb['at'][0]);dy=abs(pa['at'][1]-pb['at'][1]);r=pb['size'][0]/2
  if pa['shape']=='rect':clear=math.hypot(max(0,dx-pa['size'][0]/2),max(0,dy-pa['size'][1]/2))-r
  else:clear=math.hypot(dx,dy)-pa['size'][0]/2-r
  pair.append({'primary':p,'secondary':s,'copper_edge_distance_mm':clear})
gap=min(x['copper_edge_distance_mm'] for x in pair)
position=c['project_combined_solder_outgrowth_and_position_budget_per_domain_mm']
wP,wS=c['wire_OD_budget_mm']['P_A'],c['wire_OD_budget_mm']['S'];T=c['tape_upper_mm']
layers=sum(len(c['layer_turns'][k])*c['wire_OD_budget_mm']['S' if k=='S' else 'P_A'] for k in ['P','A','S'])
wraps=sum(c['tape_wraps'].values());regular=layers+wraps*T;build=regular+c['tape_seam_extra_max_layers_at_one_angle']*T
old=json.loads((P/'electrical-integration/magnetics/winding-results.json').read_text());assert abs(build-old['geometry']['radial_one_seam_mm'])<1e-12
nativewindow=json.loads((P/'electrical-integration/magnetics/window-results.json').read_text());oldwin=nativewindow['candidates'][0]
radial_available=(18.7-.6-13.1)/2
assert abs(oldwin['radial_build_mm']-build)<1e-12
fitremaining=radial_available-build-c['project_extra_radial_build_budget_mm']-c['project_core_bobbin_decenter_budget_mm']
assert fitremaining>0
spans={k:max(v)*c['packing_pitch_mm'][k] for k,v in c['layer_turns'].items()};assert all(v<=c['winding_band_mm'] for v in spans.values())
# A wider winding alternative is arithmetic only: no new STEP intersection/exit verification.
wide_build=build-wP
result={'scope':'Calculated candidate budgets, not finished-transformer/EIS/normative/PCB acceptance','sources_checked':checked,'candidate':c['id'],'winding_graph_preserved':True,'pad_pair_distances':pair,'minimum_P_S_copper_gap_mm':gap,'gap_after_chosen_per_side_budget_mm':gap-2*position,'engineering_P_S_reservation_mm':c['engineering_PCB_primary_secondary_reservation_mm'],'remaining_total_planar_pad_gap_budget_mm':gap-2*position-c['engineering_PCB_primary_secondary_reservation_mm'],'pad_gap_does_not_measure_core_yoke_or_leadout_distance':True,'wire_layers_radial_mm':layers,'tape_total_wraps':wraps,'regular_radial_mm':regular,'one_seam_radial_mm':build,'unchanged_prior_nominal_STEP_envelope':True,'retained_prior_nominal_STEP_intersection_mm3':{'bobbin':oldwin['nominal_bobbin_intersection_mm3'],'core':oldwin['nominal_core_intersection_mm3']},'native_side_dimension_only_available_mm':radial_available,'side_budget_before_new_allocations_mm':radial_available-build,'chosen_extra_build_mm':c['project_extra_radial_build_budget_mm'],'chosen_decenter_mm':c['project_core_bobbin_decenter_budget_mm'],'residual_side_budget_mm':fitremaining,'layer_spans_mm':spans,'minimum_wire_to_band_end_per_side_mm':{k:(c['winding_band_mm']-v)/2 for k,v in spans.items()},'nominal_band_to_straight_barrel_end_per_side_mm':(16.2-c['winding_band_mm'])/2,'FIS_B3_required_P_A_tape_wraps':2,'proposed_P_A_wraps':c['tape_wraps']['P_to_A'],'bobbin_entry_required_wall_mm':.3,'bobbin_wall_all_path_verified':False,'wide_P60_60_arithmetic_only':{'band_mm':14.5,'P_pitch_mm':.240,'P_layer_span_mm':60*.240,'radial_one_seam_mm':wide_build,'side_dimension_only_margin_mm':radial_available-wide_build,'straight_barrel_end_reserve_per_side_mm':(16.2-14.5)/2,'not_selected':'Reduces radial build but sacrifices axial exit reserve; no new STEP/all-path tolerance check, winding-process or leakage evidence'},'thermal_class_ceiling_C':130,'class_ceiling_not_normal_operating_target_or_lifetime':True,'UL_EIS_adoption_above105C_required_in_source':True,'full_product_normative_insulation_limits_established':False,'physical_measurements':False}
(D/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(result,indent=2))
