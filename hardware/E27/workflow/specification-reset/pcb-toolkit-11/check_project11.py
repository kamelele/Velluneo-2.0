from pathlib import Path
import json,subprocess,os,sys,shutil,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';D=R/'hardware/E27/workflow/specification-reset/pcb-toolkit-11';E=D/'design';K=W/'kicad-10.0.6/bin'
h=json.loads((E/'hardware.json').read_text());h['source_files']=[x for x in h['source_files']if not x.endswith('.kicad_prl')];(E/'hardware.json').write_text(json.dumps(h,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
env=dict(os.environ,KICAD_CLI=str(K/'kicad-cli.exe'),KICAD_PYTHON=str(K/'python.exe'));rows=[]
for name,args in [('configuration-preview',['configure']),('spatial',['spatial']),('connectivity',['connectivity']),('requirements-routing',['requirements','--stage','routing']),('requirements-release',['requirements','--stage','release']),('current-work',['check','--mode','work','--stage','routing']),('current-release',['check','--mode','release'])]:
 cmd=[sys.executable,str(R/'pcb-toolkit.py'),'run',args[0],E.relative_to(R).as_posix(),*args[1:]];r=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
 for ext,t in [('stdout.log',r.stdout),('stderr.log',r.stderr)]:(D/'checks'/(name+'.'+ext)).write_text(t,encoding='utf-8')
 src=E/'.work'/('check.json'if name.startswith('current-')else'requirements.json'if name.startswith('requirements-')else name+'.json')
 if src.exists():shutil.copyfile(src,D/'checks'/(name+'.json'))
 rows.append(dict(name=name,command=cmd,exit_code=r.returncode));print(name,r.returncode,flush=True)
(D/'checks/toolkit-commands.json').write_text(json.dumps(rows,indent=2)+'\n')
for f in ('current-work','current-release'):
 p=D/'checks'/(f+'.json')
 if p.exists():print(f,'ERRORS',json.loads(p.read_text()).get('errors'))
