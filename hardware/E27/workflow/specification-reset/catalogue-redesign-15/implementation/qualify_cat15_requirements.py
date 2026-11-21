from pathlib import Path
import json,subprocess,shutil
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'catalogue-redesign-15'
summary=[]
for stage in('specification','schematic'):
 cmd=[str(W/'kicad-10.0.6/bin/python.exe'),str(R/'pcb-toolkit.py'),'run','requirements','hardware/E27/workflow/specification-reset','--stage',stage]
 r=subprocess.run(cmd,capture_output=True,timeout=60);j=json.loads(r.stdout.decode('utf-8-sig'));assert r.returncode==1 and j['errors']
 (D/f'checks/requirements-{stage}.json').write_text(json.dumps(dict(command=cmd,exit_code=r.returncode,report=j,stderr=r.stderr.decode('utf-8',errors='replace')),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 summary.append(dict(stage=stage,exit_code=r.returncode,error_count=len(j['errors']),error_ids=[x['id']for x in j['errors']]))
impact=dict(new_mandatory_requirements=['R-SOURCING','R-STOCK-T1'],owner_instruction_file='owner-sourcing-instruction.md',no_fabricated_pass_evidence=True,old_evidence_unchanged_but_stale_for_new_intent=True,checks=summary,meaning='Failure is retained. New sourcing requirements are now consumed by the toolkit. Prior specification scope evidence is bound to an old intent; U05-U09 and new transformer application still require actual engineering review/implementation. No new specification/schematic pass is claimed.')
(D/'checks/requirements-impact.json').write_text(json.dumps(impact,indent=2)+'\n')
for name in('correct_cat15_requirements.py','qualify_cat15_requirements.py'):
 shutil.copyfile(W/name,D/'implementation'/name)
# These two files are execution records; reproduction uses the original workspace layout.
(D/'implementation/README.md').write_text('''# Reproduction

build_cat15.py and check_cat15_native.py support execution from this directory.
The first reproduces dated observations and analytical screens, not live inventory.
The second uses pinned KiCad10.0.6 Python and reads actual native CAD.
correct_cat15_requirements.py and qualify_cat15_requirements.py are original execution
records, using the work-directory layout. Do not rerun them from this directory.
The requirements checks failed and historic scope evidence was not renewed.
Re-running any builder on a reviewed packet requires rebinding/reviewing new hashes.
''',encoding='utf-8')
print(json.dumps(impact))
