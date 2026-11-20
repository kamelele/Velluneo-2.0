from pathlib import Path
import json,hashlib,shutil,runpy
root=Path(__file__).resolve().parents[1];R=root/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';W=R/'hardware/E27/workflow/integrated-shade/compact-09'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(W/'review-inputs.json',W/'review-inputs-v1.json')
req=load(S/'requirements.json')
for id,text,acc,gate in [
 ('C_ENV','Preserve original environment inputs before schematic acceptance.','Owner declares fixture/enclosure orientations, thermal path, capacitor case/lifetime target and LED junction design limit; evidence plan before schematic acceptance, actual measurements before release.','schematic'),
 ('C_OPTICAL_INPUT','Preserve agreed optical and LED cold/hot input basis.','4000K/minCRI80 known; owner agrees flux acceptance band, diffuser loss range, operating-temperature/bin assumptions and full LED electrical envelope before schematic acceptance.','schematic'),
 ('C_SAFETY_BASIS','Confirm insulation/classification and applicable test basis before schematic acceptance.','Qualified review identifies lamp/controlgear architecture, exact applicable standard editions and numeric critical stress/spacing basis. No SELV or instruction-only contact barrier.','schematic'),
 ('C_COST','Price the entire build before purchase.','Complete BOM, PCB, winding, assembly and process price at named quantity/date, including exclusions and Economic/Standard comparison; no ordering permission inferred.','release')]:
 req['requirements'].append({'id':id,'revision':'SC09-A','owner':'Kamil and root designer','text':text,'basis':'Retained original17 obligations and independent COMP-02 finding','acceptance':acc,'gate':gate,'implementation':[{'subsystem':'DRIVER','object':id,'path':'original-requirements-crosswalk.json'}],'method':'review','evidence_ids':[]})
 if gate=='schematic':req['unknowns'].append({'id':'OPEN_'+id,'record_id':id,'field':'acceptance','owner':'Kamil and root designer','question':acc,'blocks_stage':gate,'status':'open','evidence_ids':[]})
# Explicit two-ended planning contract; acceptance remains open at schematic gate.
interface={'id':'IFC-DRIVER-LED','revision':'SC09-A','owner':'Kamil and root designer','status':'Proposed, not approved','source':{'subsystem':'DRIVER','connector':'J2','pins':{'1':'LED_PLUS','2':'DC_RETURN'}},'destination':{'subsystem':'LED_MODULE','connector':'LED-WIRE-PADS proposed','pins':{'1':'LED_ANODE','2':'LED_CATHODE'}},'pin_map':{'J2.1':'LED-WIRE-PADS.1','J2.2':'LED-WIRE-PADS.2'},'source_voltage_V':[52,68],'destination_voltage_V':[52,68],'nominal_current_mA':135,'absolute_fault_target_V':90,'basis':'Both endpoints are proposed matching targets, not measured LED qualification. Current extrema, transient/restart envelope, actual pin labeling and optical/temp/bin constraints require agreement before schematic acceptance.','startup_fault_behavior':'Disconnected replacement only with verified discharge; IC cannot limit a direct C6-to-LED reconnection impulse. No powered hotplug. All pins mains-referenced.','port_type':'Two solder-wire pads at each end; consumer mating/contact barrier not selected.'}
save(S/'two-endpoint-interface.proposed.json',interface)
# Use toolkit-defined interface schema only once numeric endpoint envelopes are accepted.
req['unknowns'].append({'id':'OPEN_IFC_ACCEPTANCE','record_id':'C_INTERFACE','field':'acceptance','owner':'Kamil and root designer','question':'Finalize and accept structured two-endpoint voltage/current/pin/startup/fault contract from two-endpoint-interface.proposed.json before schematic acceptance; no compatible targets relabelled measured endpoints.','blocks_stage':'schematic','status':'open','evidence_ids':[]})
mapping={'REQ-SCOPE':['C_SCOPE'],'REQ-POWER':['C_ARCH','C_EFFICIENCY'],'REQ-LIGHT':['C_LIGHT','C_COMPLIANCE','C_OPTICAL_INPUT'],'REQ-MAINS':['C_SUPPLY'],'REQ-FAULT':['C_PROTECTION'],'REQ-SAFETY':['C_SAFETY_BASIS','C_PACKING','C_COMPLIANCE'],'REQ-PROCESS':['C_PROCESS'],'REQ-PARTS':['C_PARTS'],'REQ-CONNECTIVITY':['C_GRAPH'],'REQ-SIZE':['C_SIZE','C_PACKING'],'REQ-EMC':['C_COMPLIANCE'],'REQ-COST':['C_COST'],'REQ-ENV':['C_ENV','C_THERMAL'],'REQ-SAFETY-TEST':['C_COMPLIANCE'],'REQ-FAULT-TEST':['C_PROTECTION','C_THERMAL'],'REQ-OPTICAL-INPUT':['C_OPTICAL_INPUT'],'REQ-INTERFACE':['C_INTERFACE']}
cross=load(S/'original-requirements-crosswalk.json')
for x in cross['requirements']:
 x['active_ids']=mapping[x['id']];x['active_gates']={y:next(z['gate'] for z in req['requirements'] if z['id']==y) for y in x['active_ids']}
 x['SC09_status']='Retained at original gate(s). Research direction review does not close these prerequisites. Prior CAD/measurement approvals not inherited.'
save(S/'original-requirements-crosswalk.json',cross)
process=load(S/'owner-process-line-decision.json');process['historical_reference_scope']='Process-only provenance from SC08; any capture approval referenced there is historical and does not authorize SC09.'
process['capture_and_process_evidence']='../SC08_prototype/owner-capture-approval.json (historical SC08 capture only)';save(S/'owner-process-line-decision.json',process)
for e in req['evidence']:e['sha256']=sha(S/e['artifact'])
reqdigest=hashlib.sha256(json.dumps({k:v for k,v in req.items() if k!='evidence'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
for e in req['evidence']:e['intent_digest']=reqdigest
save(S/'requirements.json',req)
calc=load(S/'calculated-proposal.json');calc['minimum_ON_time_primary_screen']='At actual proposed52Vminimum:1.29460us versus1.25us,max-min-ON-screen margin3.568%; same conditional1mH tolerances and assumed10%hotinductance drop.53.6Vhistoricalscreen1.299us not minimumofactivewindow. HotL and ICextrema require measurement.';calc['bleeder_worst_screen_per_resistor_at90V_W']=.12276;save(S/'calculated-proposal.json',calc)
plan=load(S/'standards-and-test-plan.json');plan['before_schematic_acceptance']='C_SAFETY_BASIS/C_ENV/C_OPTICAL_INPUT/interface acceptance remain blocking at schematic, not deferred to release. See original-requirements-crosswalk.';plan['bleeder_thermal_acceptance']='Worst declared resistance screen at90V:eachR8~0.12276W. Check exact RC1206derating vs measuredlocaltemperature undernormal/abnormalOVPduty before poweredprototype.0.25Wheadline not thermalproof.';save(S/'standards-and-test-plan.json',plan)
hw=load(S/'hardware.json');hw['source_files']=sorted(set(hw['source_files']+['two-endpoint-interface.proposed.json']));save(S/'hardware.json',hw)
runpy.run_path(str(Path(__file__).with_name('make_packet.py')),run_name='__main__')
shutil.copy2(Path(__file__).with_name('make_packet.py'),W/'make_packet.py')
shutil.copy2(Path(__file__),W/'correct_review.py')
base=load(W/'review-inputs-v1.json');paths=[x['path'] for x in base['files']]+[(S/'two-endpoint-interface.proposed.json').relative_to(R).as_posix(),(W/'correct_review.py').relative_to(R).as_posix()]
manifest={**base,'revision':'SC09-A-review-2','prior_manifest_sha256':sha(W/'review-inputs-v1.json'),'requirements_intent_digest':reqdigest,'files':[{'path':n,'sha256':sha(R/n)} for n in sorted(set(paths))]}
save(W/'review-inputs.json',manifest)
print('Newmanifest',sha(W/'review-inputs.json'),'requirements_digest',reqdigest)
