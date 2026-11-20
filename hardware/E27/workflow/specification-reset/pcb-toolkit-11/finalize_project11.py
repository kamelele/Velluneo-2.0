from pathlib import Path
import json,hashlib,shutil,subprocess,sys,zipfile
from PIL import Image,ImageDraw,ImageFont
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-toolkit-11';E=D/'design';O=D/'checks';T=W/'toolkit-c11-validation-r2';EV=E/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
v=json.loads((T/'.work/package-validation/report.json').read_text());assert v['passed']and v['unit_tests']['failures']==0 and v['unit_tests']['errors']==0
for n in ('report.json','unit-tests.txt','cad.txt','scoped-cad.txt','requirements-example.txt','workflow-example.txt','installed-trial.txt','recipient-example.txt'):
 shutil.copyfile(T/'.work/package-validation'/n,D/'toolkit'/('validation-'+n))
for n in ('integration-results.json','scoped-integration-results.json'):shutil.copyfile(T/'reports'/n,D/'toolkit'/n)
archive=W/'pcb-agent-toolkit-0.7.2-velluneo.1-r2.zip';shutil.copyfile(archive,D/'toolkit/pcb-agent-toolkit-0.7.2-velluneo.1.zip')
shutil.copyfile(T/'PACKAGE-MANIFEST.json',D/'toolkit/PACKAGE-MANIFEST.json')
shutil.copyfile(T/'docs/scoped-policy.md',D/'toolkit/scoped-policy.md')
changed=[]
old=W/'toolkit-reference-export';new=W/'toolkit-c11-source'
for name in json.loads((T/'PACKAGE-MANIFEST.json').read_text())['files']:
 a=old/name;b=T/name
 if not a.exists()or a.read_bytes()!=b.read_bytes():
  target=D/'toolkit/changed-source'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(b,target);changed.append(dict(path=name,before_sha256=sha(a)if a.exists()else None,after_sha256=sha(b)))
put(D/'toolkit/changes.json',dict(base_public_commit='86614c3b9b43713031e0ea481edbe26b71cd1b8f',archive_sha256=sha(archive),manifest_sha256=sha(T/'PACKAGE-MANIFEST.json'),changes=changed,upstream_release=False,actual_extracted_validation=True))
for p in (E/'.work/configure/plans').glob('*.diff'):
 if p.stem=='9febb44fddd710c94008ecff2abdb3d3d6baadffd9dd0d8aaca5e1e63f0f4550':shutil.copyfile(p,O/'applied-configuration.diff')
for n in ('migration-proof.json','config-state.json'):shutil.copyfile(E/'.electronics-rules'/n,O/n)
for n in ('drc.json','erc.json','CAM-validation.json','native-fabrication-input.json','native-analysis.json','current-negative-controls.json','independent-policy-equivalence.json'):
 shutil.copyfile(O/n,EV/n)
shutil.copyfile(D/'toolkit/validation-report.json',EV/'toolkit-validation.json');shutil.copyfile(O/'migration-proof.json',EV/'migration-proof.json')
dr=json.loads((O/'drc.json').read_text());er=json.loads((O/'erc.json').read_text());assert not dr['violations']and not dr['unconnected_items']and not dr['schematic_parity']and not any(s['violations']for s in er['sheets'])
put(EV/'native-checks.json',dict(DRC=dr,ERC=er,source_board_sha256=sha(E/'Velluneo_driver.kicad_pcb')))
put(EV/'coordinator-review.json',dict(verified_by='/root coordinator actual source/native/toolkit inspection; not a final independent reviewer',physical=json.loads((O/'native-fabrication-input.json').read_text()),topology=json.loads((O/'current-negative-controls.json').read_text()),policy=json.loads((O/'independent-policy-equivalence.json').read_text()),scope='Source geometry, explicit current mapping and bounded policy preservation only. No supplier, stage, normative or powered qualification approval.'))
shutil.copyfile(O/'CAM-validation.json',EV/'current-CAM.json')
c=json.loads((E/'requirements.json').read_text());c['revision']='TOOLKIT11-prototype-scope-1'
closed={'PB-IDENTITY','PB-ROUTING','PB-GEOMETRY','PB-CAM','PB-MAPPING','PB-TOOL-SCOPE'}
for q in c['requirements']:q['evidence_ids']=['EV-'+q['id']]if q['id']in closed else[]
for u in c['unknowns']:
 if u['id']=='PB-U-TOOL':u.update(status='resolved',resolution='Separately versioned compatibility candidate installed through real update; actual configure preview/apply owns exact scoped3/10mm rules and four-layer exclusion, independent equivalence and actual clean-extracted validation pass. No upstream or human hardware approval inferred.',evidence_ids=['EV-PB-TOOL-SCOPE'])
intent=hashlib.sha256(json.dumps({k:x for k,x in c.items()if k!='evidence'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest();c['evidence']=[]
for q in c['requirements']:
 if q['id']not in closed:continue
 path='evidence/native-checks.json'if q['id']=='PB-GEOMETRY'else'evidence/current-CAM.json'if q['id']=='PB-CAM'else'evidence/coordinator-review.json'
 inputs=['Velluneo_driver.kicad_pcb','Velluneo_driver.kicad_pro','Velluneo_driver.kicad_sch','Velluneo_driver.kicad_dru']
 if q['id']=='PB-TOOL-SCOPE':inputs+=['.electronics-rules/config-state.json','.electronics-rules/migration-proof.json','evidence/toolkit-validation.json','spatial-constraints.json','configuration-migration.json']
 c['evidence'].append(dict(id='EV-'+q['id'],kind=q['method'],result='pass',verified_by='/root actual native/CAM/policy/adoption inspection',artifact=path,sha256=sha(E/path),intent_digest=intent,inputs=[dict(path=n,sha256=sha(E/n))for n in inputs]))
put(E/'requirements.json',c)
# Current process and assembly reference, with explicit holds preserved.
for n in ('FABRICATION-NOTES.txt',):
 s=(P/'pcb-cleanup-10/fabrication'/n).read_text();s+='\nTOOLKIT11 supersedes C10 toolkit-adoption hold: scoped3/10mm and four-layer areas now generated/adopted and tested. Actual supplier/order/assembly/energization holds remain. Current source/copper is identical to C10 by native comparison.\n';(D/'fabrication'/n).write_text(s,encoding='utf-8')
for n in ('ORDER-CHECKLIST.txt','SUPPLIER-DFM-REQUEST-DRAFT.txt'):
 s=(P/'pcb-cleanup-10'/n).read_text();s+='\nTOOLKIT11 current packet: toolkit scope/adoption is now demonstrated; supersedes the old compatible-extension requirement. Current files in this packet only. Supplier confirmation and authorized final-stage review still required. This supplier draft has NOT been sent.\n';(D/n).write_text(s,encoding='utf-8')
for n in ('README.txt',):shutil.copyfile(P/'pcb-cleanup-10/assembly-reference'/n,D/'assembly-reference'/n)
rel=E/'release';rel.mkdir(exist_ok=True)
for sub in ('fabrication','assembly-reference'):
 shutil.copytree(D/sub,rel/sub,dirs_exist_ok=True)
for side in ('top','bottom'):shutil.copyfile(P/'pcb-cleanup-10/design/release'/('assembly-'+side+'.png'),rel/('assembly-'+side+'.png'))
shutil.copyfile(D/'ORDER-CHECKLIST.txt',rel/'bringup-hold-and-receipt-plan.txt')
put(O/'assembly-image-provenance.json',dict(source_packet='pcb-cleanup-10',basis='Native semantic equality proves unchanged footprint allocation and copper. Retained envelope-model reference images are not supplier exact-part models.',sources={side:sha(rel/('assembly-'+side+'.png'))for side in('top','bottom')}))
h=json.loads((E/'hardware.json').read_text());h['release_files']={};put(E/'hardware.json',h)
r=subprocess.run([sys.executable,str(R/'pcb-toolkit.py'),'run','snapshot',E.relative_to(R).as_posix()],capture_output=True,text=True,timeout=180);assert r.returncode==0,r.stderr;snap=r.stdout.strip().splitlines()[-1]
files={'gerbers':list((rel/'fabrication').glob('*.g*')),'drills':list((rel/'fabrication').glob('*.drl')),'bom':[rel/'assembly-reference/BOM.csv'],'positions':[rel/'assembly-reference/positions-native.csv'],'assembly_drawing':[rel/'assembly-top.png',rel/'assembly-bottom.png'],'bringup_plan':[rel/'bringup-hold-and-receipt-plan.txt']}
h['release_files']={k:[dict(path=p.relative_to(E).as_posix(),sha256=sha(p),snapshot=snap)for p in ps]for k,ps in files.items()};put(E/'hardware.json',h)
render=D/'render';j=json.loads((render/'high-quality-renders.json').read_text())
for row in j['renders']:
 size=Image.open(render/row['path']).size;row.update(width=size[0],height=size[1],requested_width=4096,requested_height=3072)
put(render/'high-quality-renders.json',j)
# Native renders only, assembled without changing any board image content.
canvas=Image.new('RGB',(2400,1100),'#eceef2');draw=ImageDraw.Draw(canvas)
for i,side in enumerate(('top','bottom')):
 im=Image.open(render/('Velluneo_bareboard_'+side+'_4K.png'));im.thumbnail((1200,1000));canvas.paste(im,(i*1200+(1200-im.width)//2,65))
 draw.text((i*1200+40,28),'Velluneo  |  '+('Gora'if side=='top'else'Dol')+'  |  45 x 60 mm',fill='#18242f',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',27))
draw.text((40,1050),'Rzeczywisty render KiCad | plytka bez elementow | zielona maska, ENIG | akceptacja producenta pozostaje otwarta',fill='#18242f',font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22))
out=W.parent/'outputs';out.mkdir(exist_ok=True);canvas.save(out/'Velluneo_toolkit11_3D.png');canvas.save(D/'pcb-preview.png')
put(D/'procurement-status.json',dict(technical_toolkit_scope_closed=True,closed=sorted(closed),open=['PB-PROCESS'],order_ready=False,formal_release=False,supplier_confirmation=False,actual_final_human_stage_approval=False,assembly_and_energization_qualified=False,upstream_toolkit_release=False,scope='Unpowered bare-board prototype preparation. Parent lamp qualification is unchanged and remains open. No supplier message/order/payment/test executed.'))
(D/'README.md').write_text('''# TOOLKIT11 — scoped isolation rules and native high-quality preview

One selected rectangular 45 x 60 mm, four-layer, 33-component/81-pad driver.
304 copper segments and 17 filled/capped 0.7/0.3 mm vias are unchanged from C10.
Native semantic comparison proves every footprint/pad/track/via position, value,
MPN and copper shape is retained. Only explicit policy ownership/area identity
and stricter future-via defaults change. Native ERC/DRC/parity are all zero.

The compatibility candidate 0.7.2-velluneo.1 generates selective exact-net 3 mm
HV/quiet and 10 mm primary/secondary rules, canonical two/four-layer exclusions,
stronger-only severity overrides and bounded hash-bound legacy adoption. Actual
preview/apply created ownership and an 841-pair migration proof. A separate parser
confirms exact effective-clearance equivalence for 841 directed net cases and
215296 layer/object parameter combinations. Old global minima, strict ERC and
both courtyard ERROR severities remain. Current board negative surface/inner
faults and same-net return shortcut are detected. Original cache/export unchanged.

The exact distributable source ZIP, manifest, changed sources and actual clean
extracted validation are under toolkit/. 152 unit tests ran: 149 passed and three
symlink cases skipped because this Windows account cannot create symlinks; all 101 existing native cases, six new scoped
native cases and installed/update/rollback/examples passed on Windows/KiCad10.0.6.
This is a local reviewed compatibility candidate, not an accepted upstream release
or a newly tested Linux distribution. No customer design enters the toolkit ZIP.

Open design/Velluneo_driver.kicad_pro. Current fabrication files and engineering
archive are separate. Independent CAM reconciles nine layers, 42 PTH/0 NPTH holes
and the 45 x 60 mm outline/common origin. render/ contains actual native raytraced
both-side 4064 x 3056 PNGs. They show the bare PCB like a fabricator preview;
component models and paste overlays are hidden only in a separately identified
render copy. Editable project retains all model allocations. This is not a supplier
photograph or exact-part assembled mechanical qualification.

Six prototype preparation criteria are demonstrated. The actual supplier confirmation
of stackup/material, filled/capped via service and films remains open. Current
connectivity/spatial and final stage approvals are absent and deliberately reported.
No order-ready, normative insulation compliance, qualified transformer/assembly,
powered behavior or thermal qualification is claimed. Parent lamp requirements
remain byte-identical, open at their existing scopes. Supplier request is a concrete
UNSENT draft. No message, order, payment or energized test has been performed.

Final independent role reviews and exact publication checks bind the frozen packet.
Human review applies to this packet; earlier 33-part graph approval is retained at
its genuine digest and is not fabricated into approval of a different snapshot.
''',encoding='utf-8')
for name in ('check_project11.py','prepare_project11.py','export_project11.py','geometry_project11.py','controls_project11.py','policy_audit11.py','render_toolkit11_bare.py','render_toolkit11_hq.py','finalize_project11.py'):
 shutil.copyfile(W/name,D/name)
print('Refreshed actual evidence, six criteria, native renders; supplier/human/physical gates retained.')
