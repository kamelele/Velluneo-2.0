from pathlib import Path
import subprocess,json,hashlib,shutil,sys,os
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-driver-08';E=D/'design';O=E/'checks';K=W/'kicad-10.0.6/bin';B=E/'Velluneo_driver.kicad_pcb';rows=[]
def run(name,args,allowed=(0,)):
 cmd=[str(a)for a in args];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
 for ext,t in [('stdout.log',r.stdout),('stderr.log',r.stderr)]:(O/(name+'.'+ext)).write_text(t,encoding='utf-8')
 rows.append(dict(name=name,command=cmd,exit_code=r.returncode));(O/'final-commands.json').write_text(json.dumps(rows,indent=2)+'\n');print(name,r.returncode,flush=True);assert r.returncode in allowed,(name,r.stdout[-600:],r.stderr[-600:])
run('build-negative-controls',[K/'python.exe',D/'build_negative_controls.py'])
for name,path,negative in [('final-drc',B,False),('negative-surface',D/'.work/negative'/B.name,True),('negative-inner',D/'.work/negative-four'/B.name,True)]:
 run(name,[K/'kicad-cli.exe','pcb','drc','--format','json','--schematic-parity','--severity-all','--exit-code-violations','--output',O/(name+'.json'),path],(0,5))
 j=json.loads((O/(name+'.json')).read_text());assert not j['schematic_parity']
 if negative:assert any(v['type']in('clearance','shorting_items')for v in j['violations'])
 else:assert not j['violations']and not j['unconnected_items']
run('negative-topology',[K/'python.exe',D/'analyze_native_routes.py','--board',D/'.work/negative-topology'/B.name,'--output',O/'negative-topology.json'])
assert not json.loads((O/'negative-topology.json').read_text())['junction_cut_diagnostics'][0]['separate']
run('erc',[K/'kicad-cli.exe','sch','erc','--format','json','--severity-all','--exit-code-violations','--output',O/'erc.json',B.with_suffix('.kicad_sch')])
assert not any(s['violations']for s in json.loads((O/'erc.json').read_text())['sheets'])
run('netlist',[K/'kicad-cli.exe','sch','export','netlist','--format','kicadxml','--output',O/'netlist.xml',B.with_suffix('.kicad_sch')])
run('schematic-pdf',[K/'kicad-cli.exe','sch','export','pdf','--output',D/'Velluneo_driver.pdf',B.with_suffix('.kicad_sch')])
run('positions',[K/'kicad-cli.exe','pcb','export','pos','--format','csv','--units','mm','--use-drill-file-origin','--output',D/'assembly-positions.csv',B])
for name,layer in [('front','F.Cu,F.SilkS,Edge.Cuts'),('inner1','In1.Cu,Edge.Cuts'),('inner2','In2.Cu,Edge.Cuts'),('back','B.Cu,B.SilkS,Edge.Cuts')]:
 run('svg-'+name,[K/'kicad-cli.exe','pcb','export','svg','--layers',layer,'--mode-single','--page-size-mode','2','--exclude-drawing-sheet','--output',D/('copper-'+name+'.svg'),B])
for side in('top','bottom'):
 run('render-'+side,[K/'kicad-cli.exe','pcb','render','--width','1400','--height','1100','--side',side,'--rotate','325,0,30','--perspective','--zoom','.68','--background','opaque','--quality','basic','--output',D/('native-'+side+'.png'),B])
print('Native checks and exports complete',flush=True)
