from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'work/Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';W=R/'hardware/E27/workflow/integrated-shade/compact-09';P=W/'prototype-package';Q=ROOT/'work/compact09/order-closure';D=S/'release-candidate';D.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot():
 r=subprocess.run([sys.executable,str(R/'pcb-toolkit.py'),'run','snapshot','hardware/E27/variants/integrated-shade/SC09_compact'],capture_output=True,text=True);assert r.returncode==0,r.stdout+r.stderr;s=r.stdout.strip();assert len(s)==64;return s
for name in ['SC09_do_zamowienia_PCB.zip','SC09_BOM.csv','SC09_positions_manual_reference.csv','SC09_assembly_front.pdf','SC09_assembly_back.pdf','BRINGUP.md']:shutil.copy2(P/name,D/name)
with zipfile.ZipFile(D/'SC09_drills.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((P/'fabrication').glob('*.drl')):z.write(p,p.name)
(D/'README.md').write_text('Generated release-candidate outputs deliberately excluded from design source_files to prevent self-hash cycles. Actual six artifact classes are registered in hardware.release_files with exact source snapshot and hashes. This closes file registration only; actual human approval, product physical gates and supplier CAM acceptance are not fabricated.\n')
g=S/'footprint-geometry.json';m=load(S/'Models/MODEL_INFO.json');m['root_current_geometry_sha256']=sha(g);m['root_current_geometry_note']='CurrentCADdrillsT1=1.20mm;17visualmeshesunchanged. Modelgeometry_sourcehistoricalauthoringrecordsarenotredefinedasnewmanufacturersamples.';save(S/'Models/MODEL_INFO.json',m)
hw=load(S/'hardware.json');hw['source_files']=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file() and p.name!='hardware.json' and not any(x in p.relative_to(S).parts for x in ['.work','.electronics-rules','__pycache__','release-candidate']) and p.suffix not in ['.kicad_prl','.bak']);hw['release_files']={};save(S/'hardware.json',hw)
before=snapshot();mapping={'gerbers':['SC09_do_zamowienia_PCB.zip'],'drills':['SC09_drills.zip'],'bom':['SC09_BOM.csv'],'positions':['SC09_positions_manual_reference.csv'],'assembly_drawing':['SC09_assembly_front.pdf','SC09_assembly_back.pdf'],'bringup_plan':['BRINGUP.md']}
hw['release_files']={kind:[{'path':'release-candidate/'+name,'sha256':sha(D/name),'snapshot':before} for name in names] for kind,names in mapping.items()};save(S/'hardware.json',hw)
after=snapshot();assert before==after,'Release registration introduced a self-hash cycle'
save(Q/'artifact-registration.json',{'source_snapshot':before,'snapshot_after_registration':after,'stable':True,'raw_hardware_excluded_from_source_files':True,'complete_design_config_still_hashed_by_pinned_toolkit':True,'release_candidate_outputs_excluded_from_source_inputs':True,'registered_classes':hw['release_files'],'approvals_fabricated':False,'global_rules_changed':False,'full_release_pass_claimed':False});print('Registered6artifactclasses; stable source snapshot',after)
