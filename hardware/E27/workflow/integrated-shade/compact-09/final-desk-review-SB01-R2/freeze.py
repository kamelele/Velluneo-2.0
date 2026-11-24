from pathlib import Path
import json,hashlib,shutil,zipfile
H=Path(__file__).resolve().parent; ROOT=H.parents[1]; C=H/'candidate'; O=ROOT/'outputs/SC09_SB01_R2_finalny_przeglad';O.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
# Source metadata only; exact MPNs, copper, libraries and numerical rules unchanged.
hw=read(C/'hardware.json')
for n in ['PURCHASE.SB01-R2.csv','COST.SB01-R2.json','PURCHASE_REVIEW.SB01-R2.md']:
 if n not in hw['source_files']:hw['source_files'].append(n)
save(C/'hardware.json',hw)
d=read(C/'prototype-gates.SB01.json')
d['new_qualification_items']=[x.replace('fullLCstartup','R2RCstartup').replace('Conditional58â€“107C model is NOT temperaturepass.','Old temperature forecast is historical, not a pass.') for x in d['new_qualification_items']]
d['pre_order_desk_review']='Normal calculations and actual-part fit complete for a first guarded laboratory prototype; no compulsory hardware modification identified. Not a full release or test authorization.'
d['current_authority']=['NORMAL_REVIEW.SB01-R2.md','ASSEMBLY_REVIEW.SB01-R2.md','PURCHASE.SB01-R2.csv']
save(C/'prototype-gates.SB01.json',d)
rd=C/'README.md';txt=rd.read_text(encoding='utf-8');txt=txt.replace('Current startup correction candidate:', 'Current desk-reviewed laboratory candidate:',1).replace('Current engineering candidate: [SC09-SB01 simplified procurement]','Historical R1 engineering candidate: [SC09-SB01 simplified procurement]',1);rd.write_text(txt,encoding='utf-8')
for p in C.rglob('*'):
 if p.is_file() and p.suffix not in ['.kicad_prl','.lck'] and '.work' not in p.relative_to(C).parts:
  json.loads(p.read_text(encoding='utf-8')) if p.suffix=='.json' else None
base=read(H/'baseline.json')['files'];now={p.relative_to(C).as_posix():sha(p) for p in C.rglob('*') if p.is_file() and p.suffix not in ['.kicad_prl','.lck'] and '.work' not in p.relative_to(C).parts}
changed={n:{'before':base.get(n),'after':v} for n,v in now.items() if base.get(n)!=v}
immutable=['SC09_compact.kicad_pcb','SC09_compact.kicad_sch','SC09_compact.kicad_pro','SC09_compact.kicad_dru','release-refinement-R2/SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip']
assert all(base[n]==now[n] for n in immutable)
retained={'base_commit':'872adddb3da9b3dbfa57e5c81ef7ba51da2a841c','board_schematic_rules_unchanged':True,'BOM_electrical_identity_unchanged':True,'BOM_descriptor_only_change':'T1 manufacturer size label1280 corrected to1210; same exact MPN/value/pins/footprint. Native CAD untouched.','unchanged_hashes':{n:now[n] for n in immutable},'no_new_board':True,'contributor_old_metadata_hashes':'Retained contributor inputs point to baseline hardware/geometry/BOM. Documentation/source-basis, T1size descriptor and generated consumer digests updated; actual PCB/schematic and selected MPNs/values/pins unchanged. Assembly/calculation evidence retained by exact CAD/MPN identity.','retained_views':'outputs/SC09_SB01_R2_podglady — exact board and model bytes unchanged; no new render required.','strict_spacing':'23 localized manufacturer-land/escape findings retained from baseline packet. No global2mm pass or electrical safety waiver claimed.','supplier_zip':'7Gerbers+PTHdrill; no NPTH holes;8flatmembers. Existing exact ZIP preserved, fresh native export and fabrication audit pass.'}
with zipfile.ZipFile(C/immutable[-1])as z:
 retained['supplier_zip_members']=z.namelist();assert len(z.namelist())==8 and all('/' not in n for n in z.namelist())
save(O/'retained-scope.json',retained)
save(O/'source-snapshot.json',{'base_commit':retained['base_commit'],'files':now,'changed_files':changed,'deleted_files':[n for n in base if n not in now]})
assert not [n for n in base if n not in now]
for src,dst in [('candidate/PURCHASE.SB01-R2.csv','Lista_zakupow_SB01_R2.csv'),('candidate/COST.SB01-R2.json','Koszt_SB01_R2.json'),('candidate/NORMAL_REVIEW.SB01-R2.md','NORMAL_REVIEW.md'),('candidate/ASSEMBLY_REVIEW.SB01-R2.md','ASSEMBLY_REVIEW.md'),('candidate/PURCHASE_REVIEW.SB01-R2.md','PURCHASE_REVIEW.md'),('candidate/release-refinement-R2/SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip','SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip')]:shutil.copy2(H/src,O/dst)
for d in ['calculations','assembly','purchasing']:
 q=O/'evidence'/d;q.mkdir(parents=True,exist_ok=True)
 for p in (H/d).iterdir():
  if p.suffix in ['.py','.json','.md','.csv']:shutil.copy2(p,q/p.name)
shutil.copytree(H/'native-final',O/'checks/native',dirs_exist_ok=True)
for n in ['doctor.stdout.txt','doctor.stderr.txt','toolkit-work.json','toolkit-release.json','toolkit-requirements.json','task-contract.json','baseline.json','integrate.py','freeze.py']:
 if(H/n).exists():shutil.copy2(H/n,O/n)
save(O/'REVIEW_INPUT.json',{'scope':'Final normal/assembly/purchasing pre-order desk review for first SB01R2 manual laboratory prototype. Not full product release, not physical testing.','candidate_absolute':str(C),'source_snapshot_sha256':sha(O/'source-snapshot.json'),'retained_scope_sha256':sha(O/'retained-scope.json'),'actual_purchasing':'16exactMPNs/17electronics,8TME+8DigiKey; DKindexed not live;~180PLN budget not quote. NoPCB/LED/consumables.','review_rule':'Read-only four distinct actors; report material issues, do not fabricate acceptance. Final core manifest excludes review outputs and later integration notes.'})
manifest={p.relative_to(O).as_posix():sha(p) for p in O.rglob('*') if p.is_file() and p.name not in ['core-manifest.json'] and 'reviews' not in p.relative_to(O).parts and p.suffix!='.zip'}
save(O/'core-manifest.json',manifest)
print(json.dumps({'output':str(O),'changed_files':len(changed),'core_files':len(manifest),'manifest_sha256':sha(O/'core-manifest.json')}))
