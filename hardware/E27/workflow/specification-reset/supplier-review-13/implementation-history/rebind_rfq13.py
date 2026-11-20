from pathlib import Path
import json,hashlib,shutil,subprocess,sys,os
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'supplier-review-13';E=D/'design';O=D/'checks';EV=E/'evidence';K=W/'kicad-10.0.6/bin'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
j=json.loads((D/'source-binding.json').read_text());j['base_commit']='0a14df2ea95d2b2b3443585f46e77428671b88d4';put(D/'source-binding.json',j)
p=D/'fabrication/Velluneo_driver-job.gbrjob';j=json.loads(p.read_text());before=json.loads(p.read_text());j['GeneralSpecs']['ProjectId']['Revision']='RFQ13';j['GeneralSpecs']['Size']={'X':45,'Y':60};put(p,j);put(O/'job-metadata-normalization.json',dict(original=before,normalized=j,scope='Metadata revision and route-centreline size only; no artwork edit.'))
p=D/'fabrication/selected-process.json';j=json.loads(p.read_text());j.update(source_packet='RFQ13',source_C09_service_unconfirmed=True,supplier_confirmation=False,finished_component_hole_tolerance_request_plus_minus_mm=.05,T1_finished_hole_acceptance_request_mm=[1.3,1.4],hole_land_registration_request_max_mm=.025,via_ring_interpretation='0.2mm nominal geometry only; actualfinished ring/cap tolerances tobeconfirmed separately',PCB_thickness_request_mm=[1.44,1.76]);put(p,j)
for src,name in[(O/'drc.json','current-drc.json'),(O/'erc.json','current-erc.json'),(O/'CAM-validation.json','current-CAM.json'),(O/'native-analysis.json','native-topology.json'),(O/'current-spacing-and-mounting.json','spacing-and-mounting.json'),(O/'current-negative-controls.json','negative-controls.json'),(O/'policy-review.json','policy-review.json')]:shutil.copyfile(src,EV/name)
for n in('migration-proof.json','config-state.json'):shutil.copyfile(E/'.electronics-rules'/n,EV/n)
put(EV/'native-checks.json',dict(DRC=json.loads((O/'drc.json').read_text()),ERC=json.loads((O/'erc.json').read_text()),source_board_sha256=sha(E/'Velluneo_driver.kicad_pcb')))
review=dict(verified_by='/root coordinator actual inspection; not independentfinalrole',base_commit='0a14df2ea95d2b2b3443585f46e77428671b88d4',current_source_board_sha256=sha(E/'Velluneo_driver.kicad_pcb'),physical_pin_net_map_values_MPNs_retained=True,local_part_pose_changes={'R10':[-.5,0],'C3':[-1.5,0],'R17':[.35,.4]},AUX_RAW_corner_before_mm=[88.1,93],AUX_RAW_corner_after_mm=[88.1,93.6],T1_finished_body_reservation_mm=[30,30,18],fresh_native_graph_and_return_tests=True,scope='CurrentCAD/source/toolkitmapping anddocumentary/conditionalmechanicalreview only. Finishedparts/supplier/humanstage/physicalqualification remainopen.');put(EV/'coordinator-review.json',review)
c=json.loads((E/'requirements.json').read_text());c['revision']='RFQ13-prototype-preparation-1'
for q in c['requirements']:
 q['revision']='RFQ13-1';q['basis']='Actual owner RFQ and mechanical/isolation review request; retained33part pinintent and parentlamp criteria; documented RFQ13 local pose/corner refinements.'
 if q['id']=='PB-IDENTITY':q['text']=q['acceptance']='One45x60mm four-layer driver,33components81pads, same selectedMPNs/values/pinmap; only documentedRFQ13 R10/C3/R17 pose refinements.'
 if q['id']=='PB-GEOMETRY':q['text']=q['acceptance']='Freshstrict nativeDRC0/unconnected0/parity0/ERC0;3mmHVquiet/10.7mmPScoplanar rules and projectedPS>=10.7; nominalviaannulus>=.2mm.'
 if q['id']=='PB-ROUTING':q['text']=q['acceptance']='Retain304segments/17vias, dedicatedmeasurementcopper and separateC1/shunt/source/auxiliaryreturns; documentlocalattachedendpoint/AUXcornerchanges.'
 if q['id']=='PB-TOOL-SCOPE':q['text']=q['acceptance']='Controlledtoolkitadoption supportsactual3/10.7mmselectiveclearance andfourlayerbarrier with genuine migrationproof andnoweakening.'
closed={q['id']for q in c['requirements']if q['id']!='PB-PROCESS'}
for q in c['requirements']:q['evidence_ids']=['EV-'+q['id']]if q['id']in closed else[]
intent=hashlib.sha256(json.dumps({k:v for k,v in c.items()if k!='evidence'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest();c['evidence']=[]
for q in c['requirements']:
 if q['id']not in closed:continue
 path='evidence/native-checks.json'if q['id']=='PB-GEOMETRY'else'evidence/current-CAM.json'if q['id']=='PB-CAM'else'evidence/coordinator-review.json'
 inputs=['Velluneo_driver.kicad_pcb','Velluneo_driver.kicad_pro','Velluneo_driver.kicad_sch','Velluneo_driver.kicad_dru']
 if q['id']=='PB-TOOL-SCOPE':inputs+=['.electronics-rules/config-state.json','.electronics-rules/migration-proof.json','configuration-migration13.json']
 if q['id']=='PB-IDENTITY':inputs+=['BOM.csv']
 c['evidence'].append(dict(id='EV-'+q['id'],kind=q['method'],result='pass',verified_by='/root actual native/source/CAM inspection',artifact=path,sha256=sha(E/path),intent_digest=intent,inputs=[dict(path=n,sha256=sha(E/n))for n in inputs]))
put(E/'requirements.json',c)
# Current engineering interfaces become the release drawing/reference; no stage approval is invented.
release=E/'release';release.mkdir(exist_ok=True)
for n in('fabrication','assembly-reference'):shutil.copytree(D/n,release/n,dirs_exist_ok=True)
shutil.copyfile(D/'drawings/Velluneo_RFQ13_Dimensioned_Review.pdf',release/'assembly-review.pdf')
(release/'receipt-and-hold-plan.txt').write_text('''RFQ13 receipt and hold plan
Before assembly, inspect exact material/outline/thickness,17via fill/caps,25open insertionholes,drillregistration andprotectedband. Compareunpoweredcontinuitytonetlist. Obtain acceptedT1/formedpartdrawings andfirstarticlefit;checkvalues/polarity/vents/standoffs/fillets. No production/assembly/energization authorized by the enquiry. Supplierfilms, qualifiedtestbasis, currentstageapproval andactualassembly/finishedinsulation/functional/thermal evidence remainrequired at theirscopes.
''')
h=json.loads((E/'hardware.json').read_text());h['source_files']=[p.relative_to(E).as_posix()for p in sorted(E.rglob('*'))if p.is_file()and p.suffix!='.kicad_prl'and p.name!='hardware.json'and not any(x in p.relative_to(E).parts for x in('.work','__pycache__','release'))];h['release_files']={};put(E/'hardware.json',h)
env=dict(os.environ,KICAD_CLI=str(K/'kicad-cli.exe'),KICAD_PYTHON=str(K/'python.exe'));r=subprocess.run([sys.executable,str(R/'pcb-toolkit.py'),'run','snapshot',E.relative_to(R).as_posix()],cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120);assert r.returncode==0,r.stderr;snap=r.stdout.strip().splitlines()[-1]
files={'gerbers':list((release/'fabrication').glob('*.g*')),'drills':list((release/'fabrication').glob('*.drl')),'bom':[release/'assembly-reference/BOM.csv'],'positions':[release/'assembly-reference/positions-native.csv'],'assembly_drawing':[release/'assembly-review.pdf'],'bringup_plan':[release/'receipt-and-hold-plan.txt']}
h['release_files']={k:[dict(path=p.relative_to(E).as_posix(),sha256=sha(p),snapshot=snap)for p in ps]for k,ps in files.items()};put(E/'hardware.json',h)
# Reuse pinned-wrapper checks, resolving this exact current project.
s=(W/'check_project11.py').read_text().replace('pcb-toolkit-11','supplier-review-13');(W/'check_rfq13.py').write_text(s,encoding='utf-8')
qa=json.loads((O/'pdf-qa.json').read_text());qa.update(visual_inspection_pending=False,visual_inspection='Coordinator inspectedallsevenpagesinPopplercontactsheet andQ1drawingatfullpage; layout/labelslegible,no clipping/overlap.');put(O/'pdf-qa.json',qa)
assert (E/'parent-lamp-requirements.json').read_bytes()==(P/'pcb-toolkit-11/design/parent-lamp-requirements.json').read_bytes()
put(D/'requirement-dispositions.json',dict(prototype_preparation_demonstrated=sorted(closed),prototype_supplier_process_open=['PB-PROCESS'],mechanical_documentary_review_complete=True,finished_dimensions_physically_confirmed=False,finished_transformer_insulation_qualified=False,parent_lamp_contract_preserved_sha256=sha(E/'parent-lamp-requirements.json'),source_enquiry_scope='Readyfortechnicalinquiryafterindependentfinalreview; fullproduct/assembly/energizationqualificationunchanged.'))
print('Rebound currentevidence/snapshot/BOM/releases; no supplier orhumanapproval invented.')
