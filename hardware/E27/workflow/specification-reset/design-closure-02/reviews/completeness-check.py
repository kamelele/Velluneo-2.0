from pathlib import Path
import json,hashlib,subprocess
R=Path(r'C:/Users/kamil/Documents/Codex/2026-11-17/zo/work/Velluneo-readiness');P=R/'hardware/E27/workflow/specification-reset';D=P/'design-closure-02';W=R.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
count=0
for s in json.loads((D/'controller/sources.json').read_text(encoding='utf-8'))['fresh_sources']:
 p=W/'closure-controller-sources'/s['file'];assert sha(p)==s['sha256'],p;count+=1
for s in json.loads((D/'cooling/sources.json').read_text(encoding='utf-8'))['fresh_bytes']:
 p=W/'closure-cooling-sources'/s['file'];assert sha(p)==s['sha256'],p;count+=1
t=json.loads((D/'transformer/sources.json').read_text(encoding='utf-8'))
for s in t['retained_material_bytes']:
 p=W/'readiness-sources/isolation'/s['filename'];assert sha(p)==s['sha256'],p;count+=1
deps=0
for s in t['repository_inputs']:assert sha(P/s['path'])==s['sha256'],s['path'];deps+=1
for n,h in json.loads((D/'controller/sources.json').read_text())['repository_inputs_SHA256'].items():assert sha(P/n)==h,n;deps+=1
for n,h in json.loads((D/'cross-check.json').read_text())['input_sha256'].items():assert sha(P/n)==h,n;deps+=1
for folder in ['controller','transformer']:
 m=json.loads((D/folder/'artifact-hashes.json').read_text(encoding='utf-8'))
 files=m.get('files',m)
 print(folder,'manifest_format',list(m)[:4])
 if isinstance(files,dict):
  for n,v in files.items():
   if isinstance(v,dict)and'sha256'in v:assert sha(D/folder/n)==v['sha256'],n
base='ea3b23fced193861c94637524d482b7c0e96d33e'
cfg=json.loads((P/'hardware.json').read_text());old=json.loads(subprocess.check_output(['git','show',base+':hardware/E27/workflow/specification-reset/hardware.json'],cwd=R))
assert {k:v for k,v in cfg.items()if k!='source_files'}=={k:v for k,v in old.items()if k!='source_files'}
assert cfg['source_files'][:len(old['source_files'])]==old['source_files'];assert all((P/f).is_file()for f in cfg['source_files'])
delta=subprocess.check_output(['git','diff','--name-only',base],cwd=R,text=True).splitlines();assert set(delta)=={'hardware/E27/workflow/project-index.md','hardware/E27/workflow/specification-reset/hardware.json'}
c=json.loads((D/'checks/connectivity.json').read_text());assert c['passed']and c['physical_pins']==79 and c['intended_nets']==22 and c['no_connects']==4
assert c['intent_digest']=='5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8'
commands=json.loads((D/'checks/command-results.json').read_text());assert all(c['exit_code']==c['expected_exit_code']for c in commands)
cool=json.loads((D/'cooling/construction.json').read_text())
for n,row in cool['nominal_axial_stack_mm'].items():
 if isinstance(row,dict):assert sum(v for k,v in row.items()if k!='total')==row['total'],n
print(json.dumps({'actual_source_instances_hash_verified':count,'repository_dependency_hash_instances':deps,'source_inventory_additions':len(cfg['source_files'])-len(old['source_files']),'original_tracked_changed_paths':delta,'native_physical_pins':c['physical_pins'],'native_nets':c['intended_nets'],'native_NCs':c['no_connects'],'checks':[(c['name'],c['exit_code'])for c in commands]},indent=2))
