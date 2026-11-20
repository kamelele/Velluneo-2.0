from pathlib import Path
import json,hashlib,sys,copy
root=Path(__file__).resolve().parents[1];R=root/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype';F=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing/final-routing';O=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));save=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
expected='02e3217f2265c5bd8150c335af5123f7e9861c2cf4d463e016d5a124d6f54728';assert sha(F/'review-inputs.json')==expected
m=load(F/'review-inputs.json');bad=[x['path'] for x in m['files'] if sha(R/x['path'])!=x['sha256']];bad.extend(x['path'] for x in m['external_views'] if sha(Path(x['path']))!=x['sha256']);assert not bad,bad
rules=R/'.pcb-toolkit/versions/05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822';sys.path.insert(0,str(rules/'scripts'));import pcb_rules,product_contracts
h=load(S/'hardware.json');actual=load(F/'integrated-toolkit-check.json')
# Independently reproduce the documented snapshot with actual file reads, not a
# bypass of installed-launcher execution. Validate the pinned package separately.
import toolkit_install
lock,folder,package=toolkit_install.current(R)
inputs={str(p.relative_to(S.resolve())).replace('\\','/'):sha(p) for p in pcb_rules.source_files(S,h)}
design={a:b for a,b in h.items() if a not in ['approvals','waivers','release_files']}
inputs['project-design-config']=hashlib.sha256(json.dumps(design,sort_keys=True).encode()).hexdigest()
identity={'kind':'installed','lock_sha256':toolkit_install.hash_lock(R),**lock['current']}
inputs['toolkit:identity']=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
for key in actual['input_hashes']:
 if key.startswith('ruleset:'):inputs[key]=sha(rules/key.split(':',1)[1])
snap=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest()
assert snap==actual['snapshot']==m['integrated_source_snapshot'];assert inputs==actual['input_hashes']
req=product_contracts.evaluate(S,h['product']['requirements_file'],stage='routing');save(O/'fresh-requirements-routing.json',req);assert req['passed']
doc=load(S/h['product']['requirements_file']);old=load(F/'requirements-before-routing-evidence.json');assert len(doc['requirements'])==12
delta=[]
for a,b in zip(old['requirements'],doc['requirements']):
 assert a['id']==b['id'];aa=copy.deepcopy(a);bb=copy.deepcopy(b);aa.pop('evidence_ids');bb.pop('evidence_ids')
 if aa!=bb:
  assert a['id'] in ['LAB_SPATIAL','LAB_SPACING'];aa['implementation']=bb['implementation'];assert aa==bb;delta.append(a['id'])
for e in doc['evidence']:
 assert e['intent_digest']==product_contracts.intent_digest(doc);assert sha(S/e['artifact'])==e['sha256']
 for x in e['inputs']:assert sha(S/x['path'])==x['sha256']
assert len(doc['evidence'])==10
original=load(S/'requirements.json');assert len(original['requirements'])==17;assert sha(S/'requirements.json')=='1f10e2590e53a47f696a52c97886514582ace16ab7e28c953b4599a8bbcfa5af'
interface=load(S/'driver-led-interface.json');embedded=copy.deepcopy([x for x in original['interfaces'] if x['id']=='IFC-DRIVER-LED'][0]);standalone=copy.deepcopy(interface)
interface_evidence_difference={'embedded':embedded.pop('evidence_ids'),'standalone':standalone.pop('evidence_ids')};assert embedded==standalone
sp=load(S/h['product']['spatial_file']);dg=hashlib.sha256(json.dumps({a:b for a,b in sp.items() if a!='approval'},sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest();assert dg==sp['approval']['intent_digest']=='e229ed9dd0a8a593837efcfeaac4fe11b63160d5ceab293653b18370dc764dc8'
for x in sp['basis_sources']:assert sha(S/x['path'])==x['sha256']
ri=load(S/'.electronics-rules/routing-input.json');assert ri==load(S/'.electronics-rules/placement-input.json');assert ri['constraints']['intent_digest']==dg
result={'actor':'/root/final_route_completeness','role':'Completeness Reviewer','manifest_sha256':expected,'hash_checks':{'files':len(m['files']),'external_views':len(m['external_views']),'mismatches':bad},'freshly_recomputed_source_snapshot':snap,'complete_source_and_rules_hash_map_matches':True,'current_requirements_intent_digest':product_contracts.intent_digest(doc),'routing_requirements_pass':True,'current_LAB_evidence_records':10,'release_criteria':[q['id'] for q in doc['requirements'] if q['gate']=='release'],'acceptance_texts_and_thresholds_unchanged':True,'only_implementation_path_updates':delta,'original_product_requirements':17,'original_product_requirements_sha256':sha(S/'requirements.json'),'embedded_and_separate_interface_functional_fields_equal':True,'interface_evidence_ids_difference':interface_evidence_difference,'actual_approved_spatial_intent_digest':dg,'active_spatial_basis_hashes_pass':True,'consumer_digest':ri['constraints_digest']}
save(O/'independent-inspection.json',result);print(json.dumps(result,indent=2))
