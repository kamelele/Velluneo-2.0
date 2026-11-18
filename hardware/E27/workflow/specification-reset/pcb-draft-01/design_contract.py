"""Numerical driver limits and draft barrier budget; source limits are not dynamic proof."""
from pathlib import Path
import json,hashlib,math,argparse
D=Path(__file__).resolve().parent;P=D.parent
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=Path,required=True);args=ap.parse_args()
source=args.sources/'slup419.pdf';sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha=='87d0fc2c5989664c2c6bb5f0b8eada5b7cbf39ed7c04ab32627554f9dcd4ca2b'
rmin=2.37*.979;lpmin=2.304e-3*.9;vpk=math.sqrt(2)*253
controller={'source':{'url':'https://www.ti.com/lit/ds/symlink/ucc28711.pdf','sha256':'762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248','pages':[4,5,6,12,23]},
 'VDD_recommended_V':[9,35],'VDD_absolute_max_V':38,'VDD_on_V':[19,23],'VDD_off_V':[7.7,8.5],
 'VS_recommended_negative_current_magnitude_A':.001,'VS_absolute_peak_negative_current_magnitude_A':.0012,'VS_absolute_voltage_V':[-.75,7],'VS_OVP_threshold_25C_V':[4.55,4.71],
 'CS_normal_max_threshold_V':[.738,.810],'CS_backup_threshold_V':[1.4,1.6],'leading_edge_blanking_s':[180e-9,280e-9],'CS_absolute_voltage_V':[-.5,5],
 'NTC_physical_pin':'3','NTC_threshold_V':[.9,1.0],'NTC_pullup_A':[90e-6,125e-6],'maximum_frequency_parameter_Hz':[92000,106000],'recommended_junction_C':[-40,125],
 'static_normal_threshold_current_screen_A':.810/rmin,'static_backup_threshold_current_screen_A':1.6/rmin,'blanking_linear_ramp_screen_A':vpk/lpmin*280e-9,
 'NTC_R_for_below_lowest_threshold_at_max_pullup_ohm':.9/125e-6,'NTC_R_for_above_highest_threshold_at_min_pullup_ohm':1/90e-6,
 'dynamic_peak_current_proven':False,'actual_startup_or_fault_simulation_pass':False,
 'limitations':['Static CS threshold divided by RCS is not a fault peak; include blanking, delay, gate response and saturation.','100uA startup minimum is specified atVDD0/HV100V, not as a complete charging I-V law.','Fault95uA typical/125uA maximum provides no minimum discharge draw or guaranteed retry period.','Typical internal165C shutdown is not external component protection. RT1-open and correlated thermal behavior remain unresolved.']}
barrier={'source':{'url':'https://www.ti.com/lit/ml/slup419/slup419.pdf','sha256':sha,'pages':[10,11],'native_page_10_visually_inspected':True},
 'source_application':'Telecommunications worked example; no transfer of IEC62368/60950 approval to lighting61347/60598.',
 'draft_nominal_pad_and_route_PS_reservation_mm':10,'draft_finished_metal_planning_target_mm':9,'solder_position_outgrowth_allowance_each_domain_mm':.35,
 'saved_pad_bbox_gap_mm':10.225,'budget_after_two_allowances_mm':10.225-.7,'finished_target_residual_mm':10.225-.7-9,
 'proposed_conditions':{'pollution_degree':2,'altitude_max_m':2000,'material_CTI_min':175,'coating_or_mask_insulation_credit':False,'source_worked_example_working_voltage_VDC':400,'actual_working_voltage_RMS_peak_waveform_bound_established':False,'frequency_assessment_ceiling_Hz':106000},
 'lighting_normative_acceptance':False,'slot_selected':False,'solid_insulation_and_T1_core_leadout_qualified':False,
 'remaining':'Establish actual primary-secondary working RMS/repetitive peaks/frequency, applicable lighting source branch, air/surface/solid paths and material/process/withstand contract before routing acceptance. A copper keepout, hipot rating or mask is not a qualified barrier.'}
out={'packet':'PCB-DRAFT-01','purpose':'Source-bound engineering workspace limits, not schematic or placement acceptance','controller':controller,'barrier':barrier,'R1_fusible_candidate_applied':False,'active_31_graph_preserved':True,'readiness':{'native_PCB_authoring_started':True,'schematic_stage_approved':False,'placement_stage_approved':False,'routing_authorized_as_accepted_stage':False,'manufacturing_or_power_test_authorized':False}}
(D/'design-contract.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'controller_static_normal_A':controller['static_normal_threshold_current_screen_A'],'controller_static_backup_A':controller['static_backup_threshold_current_screen_A'],'blanking_linear_ramp_A':controller['blanking_linear_ramp_screen_A'],'finished_PS_budget_mm':barrier['budget_after_two_allowances_mm'],'lighting_qualification':False}))
