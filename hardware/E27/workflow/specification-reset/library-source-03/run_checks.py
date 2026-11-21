#!/usr/bin/env python3
"""Run pinned native checks, retaining actual command results and stage failures."""
from pathlib import Path
import argparse,json,os,subprocess,sys,shutil
D=Path(__file__).resolve().parent;P=D.parent;R=P.parents[3]
a=argparse.ArgumentParser();a.add_argument('--kicad-bin',type=Path,required=True);args=a.parse_args()
cli=args.kicad_bin/'kicad-cli.exe';cad=args.kicad_bin/'python.exe';py=sys.executable
env=os.environ.copy();env.update(KICAD_CLI=str(cli),KICAD_PYTHON=str(cad),KICAD_CONFIG_HOME=str(R/'.work/kicad-config'),KICAD_DOCUMENTS_HOME=str(R/'.work/kicad-documents'),PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
records=json.loads((D/'command-results.json').read_text()) if (D/'command-results.json').exists() else []
project=P.relative_to(R).as_posix()
def run(name,command,must_pass=True,json_name=None):
 r=subprocess.run([str(x) for x in command],cwd=R,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
 records.append({'name':name,'command':[str(x) for x in command],'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 (D/'command-results.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8',newline='\n')
 if json_name:
  try:(D/json_name).write_text(json.dumps(json.loads(r.stdout),indent=2)+'\n',encoding='utf-8',newline='\n')
  except json.JSONDecodeError:pass
 print(name, r.returncode,flush=True)
 if must_pass and r.returncode:raise SystemExit(f'{name} failed; actual output retained')
 return r
run('doctor',[py,'pcb-toolkit.py','doctor'],json_name='doctor.json')
run('integrate-library',[py,D/'integrate.py'])
run('capture',[py,P/'schematic-capture/generate_driver.py','--output-dir',D])
run('native-library',[cad,P/'footprint-completion/verify_native_library.py',D/'native-library-check.json'])
run('connectivity',[py,'pcb-toolkit.py','run','connectivity',project],json_name='connectivity.json')
run('capture-contract',[py,P/'eco01-capture/verify_capture.py','--bom',D/'BOM.csv','--output',D/'capture-contract-check.json'])
sch=P/'Velluneo_specification_reset.kicad_sch'
run('erc',[cli,'sch','erc','--format','json','--severity-all','--exit-code-violations','--output',D/'erc.json',sch])
run('pdf',[cli,'sch','export','pdf','--output',D/'Velluneo_driver_LIB03.pdf',sch])
assert (D/'Velluneo_driver_LIB03.pdf').stat().st_size>0
run('svg',[cli,'sch','export','svg','--output',D/'svg',sch])
(D/'footprint-svg').mkdir(exist_ok=True)
run('footprint-svg',[cli,'fp','export','svg','--footprint','KEMET_2220_C0G_DensityB_Native','--output',D/'footprint-svg',P/'libraries/Velluneo_Driver.pretty'])
assert (D/'footprint-svg/KEMET_2220_C0G_DensityB_Native.svg').stat().st_size>0
run('requirements',[py,'pcb-toolkit.py','run','requirements',project,'--stage','schematic'],False,'requirements-schematic.json')
run('work-check',[py,'pcb-toolkit.py','run','check',project,'--mode','work','--stage','schematic'],False,'check-work.json')
shutil.copyfile(P/'.work/check.json',D/'check-work.json')
print('Native checks finished; failures remain explicit, no stage acceptance')
