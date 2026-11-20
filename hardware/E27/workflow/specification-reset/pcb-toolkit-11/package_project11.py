from pathlib import Path
import json,hashlib,zipfile,shutil,subprocess,sys
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-toolkit-11';E=D/'design';K=W/'kicad-10.0.6/bin'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
manifest=[]
for kind,root in [('Fabrication_REVIEW',D/'fabrication'),('Engineering',E)]:
 target=D/('Velluneo_TOOLKIT11_'+kind+'.zip');members=[]
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for p in sorted(root.rglob('*')):
   if not p.is_file()or p.suffix=='.kicad_prl'or any(s in p.relative_to(root).parts for s in('.work','__pycache__')):continue
   n=p.relative_to(root).as_posix();z.write(p,n);members.append(dict(path=n,bytes=p.stat().st_size,sha256=sha(p)))
 with zipfile.ZipFile(target)as z:assert z.testzip()is None and len(z.namelist())==len(members)
 manifest.append(dict(path=target.name,bytes=target.stat().st_size,sha256=sha(target),members=members))
put(D/'artifact-manifest.json',dict(archives=manifest,scope='Fabrication REVIEW is bare-board upload only. Engineering is editable project with local libraries/models/evidence; no formal release or supplier confirmation implied.'))
ex=D/'.work/portable';ex.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(D/'Velluneo_TOOLKIT11_Engineering.zip')as z:z.extractall(ex)
for kind in ('drc','erc'):
 out=D/'checks'/('portable-'+kind+'.json');args=['pcb','drc','--schematic-parity']if kind=='drc'else['sch','erc'];r=subprocess.run([str(K/'kicad-cli.exe'),*args,'--format','json','--severity-all','--exit-code-violations','--output',str(out),str(ex/('Velluneo_driver.'+('kicad_pcb'if kind=='drc'else'kicad_sch')))],capture_output=True,text=True,timeout=120);assert r.returncode==0,(kind,r.stdout,r.stderr)
 print('Extracted engineering',kind,'PASS',flush=True)
put(D/'checks/portable-checks.json',dict(passed=True,archive_sha256=manifest[1]['sha256'],source_board_sha256=sha(ex/'Velluneo_driver.kicad_pcb'),native_drc_erc_parity_zero=True))
put(D/'preview-manifest.json',dict(source_board_sha256=sha(E/'Velluneo_driver.kicad_pcb'),render_source=json.loads((D/'render/render-source.json').read_text()),images=[dict(path=p.relative_to(D).as_posix(),sha256=sha(p))for p in [D/'pcb-preview.png',D/'render/Velluneo_bareboard_top_4K.png',D/'render/Velluneo_bareboard_bottom_4K.png']]))
work=json.loads((D/'checks/current-work.json').read_text());release=json.loads((D/'checks/current-release.json').read_text());req=json.loads((D/'checks/requirements-routing.json').read_text());assert not req['errors'];assert len(work['errors'])==2 and all('approval'in x for x in work['errors'])
put(D/'checks/check-status.json',dict(native_drc_erc_parity_zero=True,configuration_conflicts=0,configuration_applied=True,prototype_criteria_demonstrated=6,work_errors=work['errors'],release_errors=release['errors'],formal_release=False,order_ready=False))
parent=json.loads((P/'pcb-cleanup-10/requirement-dispositions.json').read_text());parent['prototype_scope_closed']=json.loads((D/'procurement-status.json').read_text())['closed'];parent['prototype_scope_open']=['PB-PROCESS'];parent['scope']='Current six bare-board preparation criteria demonstrated. Parent errors preserved unchanged, not closed by toolkit/CAM/render evidence.';put(D/'requirement-dispositions.json',parent)
print('Artifacts complete',[(r['path'],r['bytes'])for r in manifest])
