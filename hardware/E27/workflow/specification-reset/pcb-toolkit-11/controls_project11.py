from pathlib import Path
import shutil,subprocess,json
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'pcb-toolkit-11';S=P/'pcb-cleanup-10';K=W/'kicad-10.0.6/bin'
for name in ('analyze_native_routes.py','placement-decision.json','historical-DRIVER08-plan.json'):
 shutil.copyfile(S/name,D/name)
s=(S/'build_negative_controls.py').read_text();(D/'build_negative_controls.py').write_text(s)
r=subprocess.run([str(K/'python.exe'),str(D/'analyze_native_routes.py'),'--output',str(D/'checks/native-analysis.json')],capture_output=True,text=True,timeout=120);assert r.returncode==0,r.stderr
subprocess.run([str(K/'python.exe'),str(D/'build_negative_controls.py')],check=True,capture_output=True)
rows=[]
for name,folder in [('surface','negative'),('inner','negative-four')]:
 out=D/'checks'/('negative-'+name+'.json');r=subprocess.run([str(K/'kicad-cli.exe'),'pcb','drc','--format','json','--severity-all','--exit-code-violations','--output',str(out),str(D/'.work'/folder/'Velluneo_driver.kicad_pcb')],capture_output=True,text=True,timeout=120);j=json.loads(out.read_text());assert r.returncode!=0 and any(v['type']in('clearance','shorting_items')for v in j['violations']);rows.append(dict(case=name,exit_code=r.returncode,violations=len(j['violations'])))
out=D/'checks/negative-topology.json';r=subprocess.run([str(K/'python.exe'),str(D/'analyze_native_routes.py'),'--board',str(D/'.work/negative-topology/Velluneo_driver.kicad_pcb'),'--output',str(out)],capture_output=True,text=True,timeout=120);assert r.returncode==0,r.stderr;assert not json.loads(out.read_text())['junction_cut_diagnostics'][0]['separate']
assert all(c['separate']for c in json.loads((D/'checks/native-analysis.json').read_text())['junction_cut_diagnostics'])
(D/'checks/current-negative-controls.json').write_text(json.dumps(dict(passed=True,actual_selected_board_invalid_copies=rows,positive_return_branches_separate=True,same_net_shortcut_detected=True,scope='Actual current generated rules/native board; deliberately invalid copies only; no powered behavior inferred.'),indent=2)+'\n');print('Current positive and negative return/isolation controls PASS',rows)
