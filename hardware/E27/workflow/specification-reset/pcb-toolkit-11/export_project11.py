from pathlib import Path
import subprocess,json,hashlib,shutil,os,sys
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-toolkit-11';E=D/'design';K=W/'kicad-10.0.6/bin';B=E/'Velluneo_driver.kicad_pcb'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
before={ext:sha(B.with_suffix(ext))for ext in('.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_dru')};rows=[]
jobs=[('drc',['pcb','drc','--schematic-parity','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/drc.json',B]),('erc',['sch','erc','--format','json','--severity-all','--exit-code-violations','--output',D/'checks/erc.json',B.with_suffix('.kicad_sch')]),('gerbers',['pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts','--use-drill-file-origin','--subtract-soldermask','--precision','6','--output',str(D/'fabrication')+os.sep,B]),('drill',['pcb','export','drill','--drill-origin','plot','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','svg','--generate-report','--report-path',D/'checks/drill-report.txt','--output',str(D/'fabrication')+os.sep,B]),('ipc356',['pcb','export','ipcd356','--output',D/'fabrication/Velluneo_driver.d356',B]),('position',['pcb','export','pos','--format','csv','--units','mm','--use-drill-file-origin','--output',D/'assembly-reference/positions-native.csv',B]),('schematic-pdf',['sch','export','pdf','--output',D/'assembly-reference/Velluneo_driver.pdf',B.with_suffix('.kicad_sch')])]
for name,args in jobs:
 cmd=[str(K/'kicad-cli.exe'),*[str(x)for x in args]];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
 for ext,t in [('stdout.log',r.stdout),('stderr.log',r.stderr)]:(D/'checks'/(name+'.'+ext)).write_text(t,encoding='utf-8')
 rows.append(dict(name=name,command=cmd,exit_code=r.returncode));assert r.returncode==0,(name,r.stderr);print(name,'PASS',flush=True)
assert before=={ext:sha(B.with_suffix(ext))for ext in before}
put(D/'checks/native-export-commands.json',rows);put(D/'source-binding.json',dict(base_commit='53fa8e2e29cae11e857f3d961ca063b20f7d08cf',source_files={B.with_suffix(ext).relative_to(R).as_posix():h for ext,h in before.items()},lock=json.loads((R/'.pcb-toolkit/lock.json').read_text()),KiCad='10.0.6',exports_did_not_change_sources=True))
shutil.copyfile(E/'BOM.csv',D/'assembly-reference/BOM.csv')
for n in ('selected-process.json','designated-filled-vias.csv'):
 shutil.copyfile(P/'pcb-cleanup-10/fabrication'/n,D/'fabrication'/n)
s=(W/'check_proto09_cam.py').read_text().replace("D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-prototype-09'","D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-toolkit-11'")
(W/'check_cam11.py').write_text(s,encoding='utf-8')
