from pathlib import Path
import shutil,json,subprocess,sys
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'pcb-cleanup-10';K=W/'kicad-10.0.6/bin'
s=(P/'pcb-driver-08/build_negative_controls.py').read_text().replace('design/checks/negative-controls-inputs.json','checks/negative-controls-inputs.json');(D/'build_negative_controls.py').write_text(s)
subprocess.run([str(K/'python.exe'),str(D/'build_negative_controls.py')],check=True,capture_output=True)
results=[]
for name,folder in [('negative-surface','negative'),('negative-inner','negative-four')]:
 output=D/'checks'/(name+'.json');cmd=[str(K/'kicad-cli.exe'),'pcb','drc','--format','json','--severity-all','--exit-code-violations','--output',str(output),str(D/'.work'/folder/'Velluneo_driver.kicad_pcb')];r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);j=json.loads(output.read_text());assert any(v['type']in('clearance','shorting_items')for v in j['violations']);results.append(dict(name=name,exit_code=r.returncode,violations=len(j['violations'])))
output=D/'checks/negative-topology.json';r=subprocess.run([str(K/'python.exe'),str(D/'analyze_native_routes.py'),'--board',str(D/'.work/negative-topology/Velluneo_driver.kicad_pcb'),'--output',str(output)],capture_output=True,text=True,timeout=120);assert r.returncode==0,r.stderr;assert not json.loads(output.read_text())['junction_cut_diagnostics'][0]['separate']
(D/'checks/controls-summary.json').write_text(json.dumps(dict(negative_native=results,negative_same_net_shortcut_detected=True,positive_current_topology_all_separate=all(c['separate']for c in json.loads((D/'checks/native-analysis.json').read_text())['junction_cut_diagnostics']),scope='Deliberate invalid copies, not product CAD; actual native clearance/short controls and C1 topology diagnostic.'),indent=2)+'\n');print('Actual negative controls detected',results)
