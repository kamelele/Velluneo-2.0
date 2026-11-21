from pathlib import Path
import json,hashlib,subprocess,sys,os,shutil
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';D=R/'hardware/E27/workflow/specification-reset/supplier-review-13';E=D/'design';K=W/'kicad-10.0.6/bin'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
h=json.loads((E/'hardware.json').read_text());nets=set()
for q in h['product']['scoped_clearances']:
 nets.update(q['nets_a']);nets.update(q['nets_b'])
 if q['id']=='PRIMARY_SECONDARY':q['min_mm']=10.7
h['configuration_migration']='configuration-migration13.json'
put(E/'configuration-migration13.json',dict(schema_version=1,legacy_rules_sha256=sha(E/'Velluneo_driver.kicad_dru'),legacy_project_sha256=sha(E/'Velluneo_driver.kicad_pro'),net_names=sorted(nets),reviewed_by='/root coordinator, sourcebound stronger-only refinement review',reason='Ownerrequestedfinishedisolation/mountingreview before supplierinquiry. Increase P/Sdesignscreen10to10.7mm toretainoldproposed.35mmperdomain finishedmetalbudget; all otherconstraints/nativefloors/3mmHVquietretained. Actualsourcebound nativeprobe3 passes; nophysicalprocessorstandardapproval inferred.'))
h['source_files']=[p.relative_to(E).as_posix()for p in sorted(E.rglob('*'))if p.is_file()and p.suffix!='.kicad_prl'and p.name!='hardware.json'and not any(x in p.relative_to(E).parts for x in('.work','__pycache__','release'))]
h['release_files']={};put(E/'hardware.json',h)
env=dict(os.environ,KICAD_CLI=str(K/'kicad-cli.exe'),KICAD_PYTHON=str(K/'python.exe'))
cmd=[sys.executable,str(R/'pcb-toolkit.py'),'run','configure',E.relative_to(R).as_posix()];r=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120);(D/'checks/configuration-preview.log').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,(r.stdout,r.stderr)
plan=max((E/'.work/configure/plans').glob('*.json'),key=lambda x:x.stat().st_mtime);j=json.loads(plan.read_text());assert not j['conflicts'];shutil.copyfile(plan,D/'checks/configuration-plan.json');shutil.copyfile(plan.with_suffix('.diff'),D/'checks/configuration.diff')
# Independently inspect generatedpolicy before applyingthe actualtransaction.
import base64
raw=base64.b64decode(j['outputs']['Velluneo_driver.kicad_dru']);assert b'10.700000mm'in raw and b'3.000000mm'in raw
proof=json.loads(base64.b64decode(j['outputs']['.electronics-rules/migration-proof.json']));assert proof['ordered_pair_cases']==841 and all(x[3]>=x[2]for x in proof['effective_pairs'])
r=subprocess.run(cmd+['--apply',j['id']],cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120);(D/'checks/configuration-apply.log').write_text(r.stdout+r.stderr,encoding='utf-8');assert r.returncode==0,(r.stdout,r.stderr)
put(D/'checks/policy-review.json',dict(ordered_cases=841,weakened_pairs=0,strengthened_pairs=sum(x[3]>x[2]for x in proof['effective_pairs']),PS_before_mm=10,PS_after_mm=10.7,HVquiet_mm=3,explicit_native_minimums_and_severities_preserved=True,actual_preview_and_apply=True,scope='Geometricprocessmargin target, not a normativelimit or confirmedfinishedinsulation. Old.35mmperdomainbudgetretained, nottightenedtoclaimpass.'))
print(r.stdout.strip());print('Genuinecontrolledadoption PASS; stricter10.7mm P/Sscreen.')
