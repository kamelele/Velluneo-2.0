from pathlib import Path
import subprocess,json,shutil,os
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';D=R/'hardware/E27/workflow/specification-reset/catalogue-pcb-16';E=D/'design';C=D/'checks';P=E.relative_to(R).as_posix();launch=R/'pcb-toolkit.py';rows=[]
os.environ['KICAD_CLI']=str(W/'kicad-10.0.6/bin/kicad-cli.exe');os.environ['KICAD_PYTHON']=str(W/'kicad-10.0.6/bin/python.exe')
jobs=[('doctor',['doctor']),('connectivity',['run','connectivity',P]),('spatial',['run','spatial',P]),('requirements-routing',['run','requirements',P,'--stage','routing']),('work',['run','check',P,'--mode','work','--stage','routing']),('release',['run','check',P,'--mode','release'])]
for name,args in jobs:
 cmd=[str(Path(os.environ['C16_PYTHON'])),str(launch),*args];r=subprocess.run(cmd,cwd=R,capture_output=True,timeout=180);(C/('toolkit-'+name+'.log')).write_bytes(r.stdout+b'\n'+r.stderr);rows.append(dict(name=name,command=cmd,exit_code=r.returncode))
 key={'requirements-routing':'requirements','work':'check','release':'check'}.get(name,name);f=E/'.work'/(key+'.json')
 if f.exists():shutil.copyfile(f,C/('toolkit-'+name+'.json'))
 print(name,r.returncode,flush=True)
(C/'toolkit-commands.json').write_text(json.dumps(rows,indent=2)+'\n')
