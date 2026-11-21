"""Numerical/source checks for the bounded diagnostics, not a circuit approval."""
from pathlib import Path
import json,hashlib,math,argparse
a=argparse.ArgumentParser();a.add_argument('--source-dir',required=True,type=Path);arg=a.parse_args()
D=Path(__file__).resolve().parent;P=D.parent.parent;S=arg.source_dir.resolve()
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((D/'sources.json').read_text());r=json.loads((D/'results.json').read_text());eco=json.loads((D/'ECO-03-candidate.json').read_text());probe=json.loads((D/'native-probe.json').read_text())
for f in source['fresh_sources']:assert h(S/f['file'])==f['sha256'],f['file']
for p,v in source['repository_inputs_SHA256'].items():assert h(P/p)==v,p
rows=r['reset']['rows'];assert len(rows)==r['reset']['case_count']==210
assert math.isclose(r['reset']['passive_no_injection_35_to7p7_upper_s'],1.530404879812665,rel_tol=1e-12)
for x in rows:
 if x['uniform_fault_draw_A_hypothesis']==0 and x['uniform_injection_A_hypothesis']>=8e-6 and x['off_threshold_V']==7.7:assert x['time_to_off_s'] is None
 if x['time_to_off_s'] is not None:assert x['time_to_off_s']>=0
start=r['matched_old_worst_startup_comparisons'];a0,a1,b0,b1=start
assert a0['config']['extra_bias_A']==a1['config']['extra_bias_A']==0
assert b0['config']['extra_bias_A']==b1['config']['extra_bias_A']==85e-6
assert b0['VDD_min_V']<a0['VDD_min_V'] and b1['VDD_min_V']>10
refinement=abs(b1['VDD_min_V']-b0['VDD_min_V']);assert refinement<2e-6
charge=r['initial_output_capacitor_charge_sensitivity'];assert not charge[0]['reaches19V']
assert charge[1]['reaches19V'] and charge[2]['reaches19V'] and charge[2]['time_s']<charge[1]['time_s']
qerr=max(abs(x.get('charge_residual_C',0)) for x in charge);eerr=max(abs(x.get('VDD_port_energy_residual_J',0)) for x in charge)
assert qerr<1e-16 and eerr<1e-12
bp=r['backup_ECO_candidate'];assert bp['LDO_bleeder_475k_min_load_A']>=10e-6 and 80<bp['device_error_plus_extra_resistor_screen_C'][0]<bp['formula_nominal_trip_C']<bp['device_error_plus_extra_resistor_screen_C'][1]<90
assert len(eco['proposed_additions'])==7 and not eco['active_graph_changed']
u2,u3=eco['proposed_additions'][:2];assert u3['pins']['3']=='NTC' and u2['pins']['2']=='NC_DNC_FIXED_VERSION' and u2['pins']['8']==u2['pins']['5']=='VDD'
assert any('No circuit loaded' in m or "aren't any circuits loaded" in m for m in probe['messages_last20'])
assert not probe['Velluneo_native_simulation_performed']
result={'passed':True,'scope':'source identity, numerical convergence/conservation and proposal pin consistency only; no functional/native/physical or stage proof','sources_verified':len(source['fresh_sources']),'repository_dependencies_verified':len(source['repository_inputs_SHA256']),'reset_cases_verified':len(rows),'matched_extra_bias_startup_refinement_V':refinement,'maximum_charge_residual_C':qerr,'maximum_VDD_port_energy_residual_J':eerr,'new_ECO_additions':len(eco['proposed_additions']),'native_model_compatibility':'failed as recorded; zero API load return did not establish success','physical_measurements':False,'stage_approved':False}
(D/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(result,indent=2))
