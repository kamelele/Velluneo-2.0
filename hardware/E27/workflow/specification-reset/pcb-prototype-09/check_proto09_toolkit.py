from pathlib import Path
import subprocess,sys,json,os,shutil
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-prototype-09';K=W/'kicad-10.0.6/bin';env=dict(os.environ,KICAD_CLI=str(K/'kicad-cli.exe'),KICAD_PYTHON=str(K/'python.exe'),PYTHONUTF8='1');rows=[]
for name,args in [('doctor',['doctor']),('requirements-release',['run','requirements',str(P.relative_to(R)),'--stage','release']),('release-check',['run','check',str(P.relative_to(R)),'--mode','release','--stage','release'])]:
 cmd=[sys.executable,str(R/'pcb-toolkit.py'),*args];r=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
 for ext,t in [('stdout.log',r.stdout),('stderr.log',r.stderr)]:(D/'checks'/(name+'.'+ext)).write_text(t,encoding='utf-8')
 if name!='doctor':shutil.copyfile(P/'.work'/('requirements.json'if name=='requirements-release'else'check.json'),D/'checks'/(name+'.json'))
 rows.append(dict(name=name,command=cmd,exit_code=r.returncode));print(name,r.returncode,flush=True)
(D/'checks/toolkit-execution.json').write_text(json.dumps(dict(commands=rows,scope='Existing managed project contract at specification-reset, not a successful adoption of selected subproject. Selected09 native/portable checks are separate. Any unresolved contract/source/profile/spatial mapping blocks formal release; no configuration applied.',configuration_applied=False,formal_release_pass=False),indent=2)+'\n')
