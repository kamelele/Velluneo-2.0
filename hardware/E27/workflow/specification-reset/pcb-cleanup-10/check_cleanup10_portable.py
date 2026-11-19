from pathlib import Path
import zipfile,json,subprocess,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-cleanup-10';K=W/'kicad-10.0.6/bin';m=json.loads((D/'artifact-manifest.json').read_text());eng=next(a for a in m['archives']if 'Engineering'in a['path']);root=D/'.work/extracted';root.mkdir(exist_ok=True)
with zipfile.ZipFile(D/eng['path'])as z:z.extractall(root)
rows=[]
for kind in('drc','erc'):
 out=D/'checks'/('portable-'+kind+'.json');cmd=[str(K/'kicad-cli.exe'),*(['pcb','drc','--schematic-parity']if kind=='drc'else['sch','erc']),'--format','json','--severity-all','--exit-code-violations','--output',str(out),str(root/('Velluneo_driver.'+('kicad_pcb'if kind=='drc'else'kicad_sch')))];r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);j=json.loads(out.read_text());assert r.returncode==0,(kind,r.stdout,r.stderr)
 if kind=='drc':assert not j['violations']and not j['unconnected_items']and not j['schematic_parity']
 else:assert not any(s['violations']for s in j['sheets'])
 rows.append(dict(kind=kind,exit_code=0,source_board_sha256=hashlib.sha256((root/'Velluneo_driver.kicad_pcb').read_bytes()).hexdigest()));print('Portable',kind,0,flush=True)
(D/'checks/portable-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
