from pathlib import Path
import json,hashlib,shutil
H=Path(__file__).resolve().parent; C=H/'candidate'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
calc=read(H/'calculations/normal-calculations.json')
for src,dst in [('calculations/normal-calculations.json','normal-calculations.SB01-R2.json'),('calculations/REPORT.md','NORMAL_REVIEW.SB01-R2.md'),('assembly/assembly-contract.json','assembly-contract.SB01-R2.json'),('assembly/REPORT.md','ASSEMBLY_REVIEW.SB01-R2.md'),('assembly/sources.json','assembly-sources.SB01-R2.json')]: shutil.copy2(H/src,C/dst)
spec=read(C/'power-supply-specification.json')
keep=['input_VAC_RMS','frequency_Hz','nonisolated','SELV','ambient_design_C','nominal_output_V','proposed_LED_voltage_window_V','regulated_total_current_mA','bleeder_current_mA_at60V','external_LED_current_mA_at60V','external_LED_power_W_at60V','LED_count_series','LED_MPN','CCT_K','CRI_min','optical_target_lm','optical_measurement_performed','discharge','ports','PCB_origin_absolute_mm','prototype_temperature_stops']
spec={k:spec[k] for k in keep if k in spec}
loss=calc['loss_and_thermal_budget']; stress=calc['normal_stress_screens']
spec.update(revision='SC09-SB01-R2-final-desk-review',PCB_mm=[51.2,33,1.6],envelope_mm=[51.2,33,20.5],assembly_height_planning_mm=20.5,
 assembly_height_with_max_PCB_thickness_mm=20.66,height_limit='Planning only before lead-forming/solder variation; not an achieved20mm ceiling. Wires/support excluded.',
 base_loss_inclusive_of_bleeders_W=loss['nominal_total_driver_loss_planning_W'],estimated_LED_efficiency_percent=[100*v for v in loss['nominal_efficiency_planning_fraction']],
 estimated_input_power_W=[loss['nominal_external_LED_power_model_W']+v for v in loss['nominal_total_driver_loss_planning_W']],
 input_RMS_current='Surrogate planning maxima RF1 71.5mA, L1/R10 68.5mA. PF and actual input current unmeasured; no fixedPF guarantee.',
 current_extended_sensitivity_mA=[1000*v for v in calc['normal_current']['extended_LED_A_52to68V']],
 L1={'MPN':'PR02FS0201000KR500','kind':'100ohm2W pulse resistor, legacy L1 location; R10 in calculations','normal_planning_max_loss_W':0.529},
 RF1={'MPN':'FW20A47R0JA','kind':'47ohm2W fusible protective resistor','normal_planning_max_loss_W':0.257},
 T1={'MPN':'7687709152','package':'WE-PD HV1210','L_H':.0015,'IR_A':.52,'Isat_typ20C_A':.8,'extended_peak_A':calc['normal_current']['extended_Ipeak_A'],'min_ON_us':stress['T1_minON_screen_us'],'normal_RMS_scenario_max_A':.1992,'full_triangle_upper_A':stress['T1_full_triangle_RMS_upper_A']},
 C6={'MPN':'EEUFS2A151','capacitance_uF':150,'rating_V':100,'body_nominal_D_L_mm':[12.5,20],'body_max_D_L_mm':[13,22],'ripple_rating100k105C_A':1.4,'conservative_lowfrequency_rating_A':.84,'scenario_max_ripple_A':.137,'horizontal_vent_free_mm':5},
 OVP={'nominal_V':77.88,'initial25C_with_diode_lower_V':71.51,'extended_static_upper_screen_V':89.49,'prototype_stop_V':90,'hot68V_regulation':'Conditional: TCR/diode/IC threshold can remove upper-load discrimination; measure actual LED voltage/ripple and hot threshold. No silent window change.','dynamic_response':'Not proven;100V capacitor absolute rating is not the90V test limit.'},
 calculation_authority='normal-calculations.SB01-R2.json and NORMAL_REVIEW.SB01-R2.md',assembly_authority='assembly-contract.SB01-R2.json',
 physical_measurements_performed=False,final_PCB_release_accepted=False,status='Desk-reviewed first laboratory prototype candidate; full toolkit release and finished-product qualification remain unapproved.')
save(C/'power-supply-specification.json',spec)
save(C/'catalogue-design-calculations.json',{'revision':spec['revision'],'supersedes':'All prior active SB01 fixed60mA/choke and mixed R1/R2 calculations; old exact bytes retained in baseline commit872addd.', 'calculation_file':'normal-calculations.SB01-R2.json','calculation_sha256':sha(C/'normal-calculations.SB01-R2.json'),'normal_current':calc['normal_current'],'normal_stress_screens':stress,'loss_and_thermal_budget':loss,'BP_startup_sensitivity':calc['BP_startup_sensitivity'],'OVP_response_budget':calc['OVP_response_budget'],'physical_measurements_performed':False})
t=read(C/'thermal-planning.json')
targets={}
for row in t['component_screens']:
 targets[row['ref']]={k:v for k,v in row.items() if any(x in k for x in ['target_C','stop_case_C','max_proposal_C'])}
targets['L1']={'body_target_C':90};targets['C1']={'case_stop_C':80};targets['T1']['body_target_C']=90
save(C/'thermal-planning.json',{'revision':spec['revision'],'kind':'Normal-operation planning, not temperature measurement or enclosed-use qualification','total_driver_loss_planning_W':loss['nominal_total_driver_loss_planning_W'],'loss_boundary':loss['limits'],'normal_component_loss_max_W':{'L1_R10':.529,'RF1':.257,'T1_copper_only':.115,'D1_forward':.200,'U1_MOS_conduction_only':.089,'R5':.019,'R6':.0036,'R7':.029,'R8_each_at60V':.053,'R9_each_at60V':.053},'prototype_temperature_targets_and_stops_C':targets,'individual_stop_precedence':'C1 individual80C overrides grouped85C; C6 design75C and characterization stop85C. Targets are conservative review limits, not predicted temperatures.','measurement_plan':t['measurement_plan'][:2]+['Compare actual input RMS with the71.5mA surrogate envelope; review deviations before continuing. Retain COUT90V,400V normal waveform review threshold, U1/D1 absolute limits and named temperature stops. No powered test authorized by this desk report.','Measure hot OVP discrimination at the highest actual LED voltage; proposed52–68V range remains conditional. No hot-plug.','Closed housing qualification is outside this board-only prototype.'],'sources':[r for r in t['sources'] if r['id']!='VR25']+[{'id':'HVR25','url':'https://www.vishay.com/docs/30260/hvr2537.pdf','basis':'Actual HVR25 family. No VR25 thermal resistance transferred.'}],'physical_measurements_performed':False,'normal_calculation_file':'normal-calculations.SB01-R2.json'})
g=read(C/'footprint-geometry.json'); patches=read(H/'assembly/proposed-geometry-row-addenda.json')
for ref,patch in patches.items():g[ref].update(patch)
g['U1']['nominal_basic_body_bbox_xy_mm']=g['U1'].pop('max_body_bbox_xy_mm')
g['U1']['body_dimension_note']='3.9x4.9BSC is not an absolute maximum; separate4.1x5.1 engineering allowance checked in assembly contract.'
g['J1']['design_basis']=patches['J1']['description'];g['J2']['design_basis']=patches['J2']['description']
save(C/'footprint-geometry.json',g)
save(C/'mechanical-budget.proposed.json',{'revision':spec['revision'],'historical_original_target_mm':[50,32,20],'current_PCB_mm':[51.2,33,1.6],'current_planning_envelope_mm':[51.2,33,20.5],'max_PCB_thickness_planning_height_mm':20.66,'not_guaranteed_maximum':True,'basis':'16mm formed top resistor +1.6nominal PCB +2.9bottom BR1; forming and solder variation excluded. Existing outline retained by explicit same-board instruction. No enclosure development.','assembly_contract':'assembly-contract.SB01-R2.json'})
s=read(C/'source-basis.SB01.json');s['part_changes']['RF1']['notes']='Protective47ohm FW20A retained. R2 downstreamL1 is100ohm PR02-FS. Current RMS/loss authority normal-calculations.SB01-R2.json; prior LC calculations are historical.'
s['current_review']={'revision':spec['revision'],'normal_file':'normal-calculations.SB01-R2.json','assembly_file':'assembly-contract.SB01-R2.json','no_part_or_pin_change_in_final_desk_review':True}; save(C/'source-basis.SB01.json',s)
for name in ['intended-connectivity.SB01.json','spatial-constraints.json']:
 d=read(C/name)
 for b in d['basis_sources']:b['sha256']=sha(C/b['path'])
 save(C/name,d)
h=read(C/'hardware.json')
for n in ['normal-calculations.SB01-R2.json','NORMAL_REVIEW.SB01-R2.md','assembly-contract.SB01-R2.json','ASSEMBLY_REVIEW.SB01-R2.md','assembly-sources.SB01-R2.json']:
 if n not in h['source_files']: h['source_files'].append(n)
save(C/'hardware.json',h)
(C/'README.SB01-R2.md').write_text('''# SB01 R2 — first laboratory prototype desk review

The existing51.2x33mm,2layer PCB is retained byte-for-byte. No part, physical pin, net, track, via, mask, legend, outline or drill change is required by the final normal-operation and assembly desk review. Selected fabrication remains FR4,1.6mm,1oz,lead-freeHASL, manual assembly. This engineering head is not a full product release or powered-test authorization.

Physical legacy **L1** is **PR02FS0201000KR500,100ohm,10%,2W**; it is R10 only in calculations. Do not fit the old768772332 choke. RF1 is47ohm FW20A47R0JA. T1 is stock **7687709152,1.5mH,WE-PD HV1210**, not a custom transformer. C6 is **EEUFS2A151**,150uF100V,12.5x20nominal/13x22max; the different151L body is not permitted.

Input207–253VAC50Hz; external LED current approximately133.4mA at60V, about8W, intended20seriesLED. Proposed52–68V load window is conditional at its hot upper end because OVP discrimination is not guaranteed. Normal-loss budget1.24–1.69W and82.5–86.5% efficiency are engineering estimates, not measurements. All output nodes remain mains referenced; noSELV and no hot-plug.

Module height is **20.5mm nominal-board planning**, **20.66mm with maximum PCB thickness**, before forming/solder variation. The previous19.5mm and achieved20mm claims were incorrect.16mm formed top resistor+1.6mm board+2.9mm bottom BR1 govern. Trim lower THT projections<=1.5mm; preserve upper forming stand-off and C6vent5mm. Wires/support excluded.

Use NORMAL_REVIEW.SB01-R2.md, ASSEMBLY_REVIEW.SB01-R2.md and their source-bound JSON contracts. Purchase-only options must match the explicit purchasing list; no unreviewed generic resistor, coil or capacitor substitution. Legacy snapshots and previous workflow packets are history, not current performance.

Native manufacturing checks and bare-PCB disposition are separate from full toolkit release. Strict2mm comparison retains23 localized BR1/U1/D1 land/escape findings; manufacturer land geometry and local prototype assessment do not establish safety insulation qualification. No global clearance relaxation was made. Dynamic startup/OVP, hot pulse behavior, EMI/surge and fault qualification require actual controlled prototype measurements. U1D-Sshort is not guaranteed to protect100V C6 through an ordinary input fuse.
''',encoding='utf-8')
print('Integrated candidate only; CAD, BOM identities unchanged.')
