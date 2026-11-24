from pathlib import Path
import json,hashlib,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[1];C=H/'candidate';T=ROOT/'work/Velluneo-2.0/.work/SB01_R2_verify'
p=C/'Models/SC09_L1.wrl';s=p.read_text().replace('6.2992126','6.1417323')
s+='''Transform { translation -0.985 0 5.6299213 rotation 1 0 0 1.5707963 children [ Shape { appearance Appearance { material Material { diffuseColor .7 .7 .7 } } geometry Cylinder { radius .1535433 height 1.023622 } } ] }
Transform { translation 0 0 6.1417323 rotation 0 0 1 1.5707963 children [ Shape { appearance Appearance { material Material { diffuseColor .7 .7 .7 } } geometry Cylinder { radius .1535433 height 1.9700000 } } ] }
''';p.write_text(s)
(H/'toolkit').mkdir(exist_ok=True)
for n in ['check.json','requirements.json']:shutil.copy2(T/'.work'/n,H/'toolkit'/n)
plan='8f8f4d8b448bdc078dad840969a5f1c40f96044ec98ba840d9d42288a6680404'
for ext in ['json','diff']:shutil.copy2(T/'.work/configure/plans'/(plan+'.'+ext),H/'toolkit'/('configure-plan.'+ext))
for n in ['doctor.stdout.txt']:
 old=ROOT/'work/sc09-sb01-spacing-assessment'/n
 if old.exists():shutil.copy2(old,H/'toolkit'/n)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(H/'toolkit/retention-and-execution.json').write_text(json.dumps({'doctor_pin':'Retained same verified pinned runtime/toolkit manifest; current doctor returnedPASSwithknownlocalizedstderrdecode issue','configure_plan_id':plan,'preview_review':'Only intent_digest and constraints_digest changed in two consumer inputs. No numerical rule/region/.pro/.dru change. Applied via pinned configure to repository-local validation mirror and copied controlled outputs to candidate.','config_state_sha256':sha(C/'.electronics-rules/config-state.json'),'full_release_passed':False,'native_checks':'Separate actual native-final2 commands and reports; release checker may stop before commands on product/approval gates.','earlier_invocation_errors':'Unsupported --report; then absolute/unsafe/outside-repository project paths. These are errors, not passing checks. Correct actual run used .work/SB01_R2_verify under repository launcher.','no_approval_fabricated':True},indent=2)+'\n')
print('Final model connection fixed; toolkit reports copied; freeze after last native run.')
