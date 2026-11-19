from pathlib import Path
import subprocess,sys,json,shutil,os,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';D=R/'hardware/E27/workflow/specification-reset/pcb-cleanup-10';E=D/'design';K=W/'kicad-10.0.6/bin';env=dict(os.environ,KICAD_CLI=str(K/'kicad-cli.exe'),KICAD_PYTHON=str(K/'python.exe'));rows=[]
for name,args in [('connectivity',['run','connectivity',E.relative_to(R).as_posix()]),('requirements-routing',['run','requirements',E.relative_to(R).as_posix(),'--stage','routing']),('requirements-release',['run','requirements',E.relative_to(R).as_posix(),'--stage','release']),('current-work',['run','check',E.relative_to(R).as_posix(),'--mode','work','--stage','routing']),('current-release',['run','check',E.relative_to(R).as_posix(),'--mode','release'])]:
 cmd=[sys.executable,str(R/'pcb-toolkit.py'),*args];r=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
 for ext,t in [('stdout.log',r.stdout),('stderr.log',r.stderr)]:(D/'checks'/(name+'.'+ext)).write_text(t,encoding='utf-8')
 src=E/'.work'/('check.json'if name.startswith('current-')else'requirements.json'if name.startswith('requirements-')else'connectivity.json')
 if src.exists():shutil.copyfile(src,D/'checks'/(name+'.json'))
 rows.append(dict(name=name,command=cmd,exit_code=r.returncode));print(name,r.returncode,flush=True)
(D/'checks/toolkit-commands.json').write_text(json.dumps(rows,indent=2)+'\n')
