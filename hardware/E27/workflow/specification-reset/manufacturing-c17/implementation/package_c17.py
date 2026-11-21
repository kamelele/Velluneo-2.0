exec((__import__('pathlib').Path(__file__).parent/'build_c17.py').read_text().split("base='a283")[0])
base='a283213194bb16990d7614874d12336524f66fcf'
binding=json.loads((D/'source-binding.json').read_text());assert all(sha(E/p)==h for p,h in binding['source_files'].items())
checks=json.loads((D/'checks/CAM-validation.json').read_text());assert checks['passed']
drc=json.loads((D/'checks/drc.json').read_text());assert not drc['violations']and not drc['unconnected_items']and not drc['schematic_parity']
erc=json.loads((D/'checks/erc.json').read_text());assert not any(x['violations']for x in erc['sheets'])
j=json.loads((D/'checks/document-check.json').read_text());j['manual_visual_review']='Coordinator inspected all five final rendered pages: no clipping/overlap; top/bottom assembly and T1component-side numbering legible.';put(D/'checks/document-check.json',j)
# Bind current manufacturing files in an isolated native-project copy. No approvals changed.
Q=D/'.work/project'; release={
 'gerbers':[p for p in files(D/'gerbers')if p.suffix not in ['.XLN','.svg']],
 'drills':[D/'gerbers/Velluneo_C17.XLN',D/'gerbers/Velluneo_C17-drill_map.svg'],
 'bom':[D/'assembly/BOM_33_FULL.csv',D/'assembly/BOM_28_SMT.csv'],
 'positions':[D/'assembly/CPL_28_SMT.csv',D/'assembly/POSITIONS_33_REFERENCE.csv'],
 'assembly_drawing':[D/'drawings/Velluneo_C17_Fabrication_Assembly.pdf'],
 'bringup_plan':[D/'support/bring-up-and-assembly.md']}
os.environ['KICAD_CLI']=str(K);os.environ['KICAD_PYTHON']=str(W/'kicad-10.0.6/bin/python.exe')
r=subprocess.run([sys.executable,str(R/'pcb-toolkit.py'),'run','snapshot',Q.relative_to(R).as_posix()],cwd=R,capture_output=True,timeout=180);assert r.returncode==0,(r.stdout,r.stderr)
snapshot=r.stdout.decode().strip();assert len(snapshot)==64
h=json.loads((Q/'hardware.json').read_text());h['release_files']={}
for kind,entries in release.items():
 h['release_files'][kind]=[]
 for f in entries:
  rel=Path('release')/f.relative_to(D);out=Q/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,out)
  h['release_files'][kind].append(dict(path=rel.as_posix(),sha256=sha(f),snapshot=snapshot))
put(Q/'hardware.json',h)
r=subprocess.run([sys.executable,str(R/'pcb-toolkit.py'),'run','check',Q.relative_to(R).as_posix(),'--mode','release'],cwd=R,capture_output=True,timeout=240)
(D/'checks/toolkit-mapped-release.stdout.log').write_bytes(r.stdout);(D/'checks/toolkit-mapped-release.stderr.log').write_bytes(r.stderr)
shutil.copyfile(Q/'.work/check.json',D/'checks/toolkit-mapped-release.json')
result=json.loads((D/'checks/toolkit-mapped-release.json').read_text());assert result['snapshot']==snapshot if 'snapshot'in result else True
assert not any('release artifact'in x.lower() for x in result['errors']),result['errors']
put(D/'release-artifacts.json',dict(design_snapshot=snapshot,C16_source_board_sha256=binding['source_board_sha256'],mapping=h['release_files'],scope='Mapping exists in portable clone hardware.json only. C16 originalCAD/configuration untouched. No approvals/waivers added.',toolkit_release_exit_code=r.returncode,toolkit_remaining_errors=result['errors'],all_six_release_artifact_categories_current=True,manufacturing_release=False))
def archive(name,entries):
 p=D/name
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for f,n in entries:z.write(f,n)
 with zipfile.ZipFile(p)as z:
  assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))
  for f,n in entries:assert hashlib.sha256(z.read(n)).hexdigest()==sha(f),n
 return dict(path=name,sha256=sha(p),bytes=p.stat().st_size,members=len(entries))
upload=archive('Velluneo_C17_Gerber_Upload.zip',[(f,f.name)for f in files(D/'gerbers')]);assert upload['members']==14
native=archive('Velluneo_C17_KiCad_Source.zip',[(f,'design/'+f.relative_to(Q).as_posix())for f in files(Q)])
assert native['members']>=len(binding['source_files'])+20,native
with zipfile.ZipFile(D/native['path'])as z:
 for rel,hsh in binding['source_files'].items():
  payload=z.read('design/'+rel)
  if rel=='hardware.json':
   a=json.loads(payload);old=json.loads((E/rel).read_text());a.pop('release_files');old.pop('release_files');assert a==old
  else:assert hashlib.sha256(payload).hexdigest()==hsh,rel
 assert len(z.read('design/Velluneo_driver.kicad_pcb'))>100000
 assert 'design/release/gerbers/Velluneo_C17.GTL'in z.namelist()
txt(D/'support/KICAD-SOURCE-NOTES.txt','''The portable source ZIP uses the exact C16 saved board/schematic/libraries/rules.
Only hardware.json.release_files is added in this export copy, with the current
manufacturing artifact hashes and source snapshot. It contains no added approval or
waiver. Open design/Velluneo_driver.kicad_pro. C16 original files remain unchanged.
The pinned toolkit is retained at repository root; run through pcb-toolkit.py there.
All six release-file categories now pass artifact existence/hash/snapshot validation.
Remaining process, physical and human gates are retained in toolkit-mapped-release.json.
''')
txt(D/'implementation/README.md','''Executed scripts are retained for traceability, not a standalone installation.
They ran from workspace work/ with bundled1119Python, KiCad10.0.6, Gerbonara1.5.0,
PyMuPDF and reportlab. Source C16 is unchanged; transient working/export clones are
not tracked. build_c17 -> finish_c17 -> package_c17. Library access required the local
trusted helper environment. All tool outputs and scope limits are in checks/.
''')
for n in ['build_c17.py','finish_c17.py','package_c17.py']:shutil.copyfile(W/n,D/'implementation'/n)
put(D/'checks/toolkit-impact.json',dict(pin='b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97',doctor_passed=True,C16_all_sources_unchanged=True,portable_clone_change='hardware.json.release_files only; exported files added under release/',all_artifact_categories_verified=True,remaining_holds=result['errors'],toolkit_code_or_rules_changed=False,tests_not_repeated_reason='No toolkit/CAD/rules changes; fresh nativeERC/DRC/parity, graph/CAM, packaging, doctor and mappedrelease checks executed.'))
txt(D/'stage-packet.md','''# C17 review candidate

Purpose: complete current C16 manufacturing-data handoff and documentary transformer
dimension confirmation. NOT final functional qualification or production approval.
Exact base and source hashes: source-binding.json. Outputs: release-artifacts.json.
Fresh native ERC/DRC/parity/unconnected0; graph/CAM/drill/SK/package checks supplied.
All six release artifact categories pass in the mapped portable native project;
toolkit still blocks actual release for the explicit physical/process/human holds.

CurrentMYRRA74032drawing dimensions26.5x22.5x26.5mm match C16reserved body, nominal
pin coordinates and1.4mm holes. MakerPDF and old/new PCN were visually inspected.
Seller actual lot and insertion across tolerance are NOT measured/confirmed.

Open points: written JLCprocess/DFM/material/tighterholes/rings/registration; exact
partsourcing/assembly/machineCPL/panel/fixture; firstfit and poweredqualification;
actual product insulation/thermal/lampintegration and genuine current humanapprovals.
All nine responseIDs remainOPEN. No supplier contact, order, payment or manufacturing.
Four actual independent role contexts review the same frozen body before publication.
''')
put(D/'task-acceptance.json',dict(prepared_manufacturing_data=True,transformer_documentary_dimensions_verified=True,actual_lot_or_firstfit_confirmed=False,native_ERC_DRC_parity_unconnected=[0,0,0,0],independent_CAM_pass=True,full_BOM_positions=33,SMT_BOM_CPL=28,THT=3,wire_pad_pairs=2,filled_vias=24,open_component_PTH=18,all_six_toolkit_release_artifact_categories_verified=True,production_or_PCBA_release=False,portal_import=False,supplier_contact=False,order=False,physical_tests=False))
# Complete handoff includes all supporting data and portable editable source.
items=[(D/upload['path'],upload['path']),(D/native['path'],native['path'])]
for folder in ['assembly','support','drawings','checks']:items +=[(p,p.relative_to(D).as_posix())for p in files(D/folder)if p.name!='package-verification.json']
for n in ['README.md','START_HERE_PL.txt','PCB-REMARK-PASTE.txt','JLCPCB-ENQUIRY-UNSENT.txt','JLCPCB-TECHNICAL-RESPONSES.csv','quote-settings.json','jlcpcb-sources.json','source-binding.json','release-artifacts.json','task-acceptance.json','task-contract.md','stage-packet.md']:items.append((D/n,n))
handoff=archive('Velluneo_C17_Prototype_Manufacturing_Package.zip',items)
put(D/'artifact-manifest.json',dict(base_commit=base,source_board_sha256=binding['source_board_sha256'],archives=[upload,native,handoff],CRC_and_all_archive_member_SHA256_verified=True,manufacturing_upload_only_14_CAM_members=True))
put(D/'checks/package-verification.json',dict(passed=True,upload_members=14,handoff_members=handoff['members'],CRC_and_each_member_hash_verified=True,all_C16_source_hashes_unchanged=all(sha(E/p)==h for p,h in binding['source_files'].items()),portable_native_changes='Only hardware.json.release_files and new release/ files',all_artifact_categories_verified=True,not_a_manufacturing_release=True))
# Add a current entry without rewriting historical C16 evidence.
index=R/'hardware/E27/workflow/project-index.md';s=index.read_text();heading='''## Current prototype manufacturing-data handoff - C17, 21 November 2026

[C17](specification-reset/manufacturing-c17/README.md) packages unchanged C16 CAD
for barePCB DFM/quotation plus separate assemblyfeasibility: fresh11Gerbers/oneSK/
oneExcellon/map,24filledcappedvias,18opencomponentholes,33fullBOM/28SMTBOM-CPL/
3THT/2wirepairs, fivepagefabrication/assemblydrawing, source and artifacthashes,
portableKiCad and exactJLCinstructions. NativeERC/DRC/parity/unconnected0; independent
CAM/pin graph passes. Six toolkit releaseartifact categories now pass in the mapped
portablecopy; actual release gates remainheld. CurrentMYRRA74032makerbody
26.5x22.5x26.5mm,9pins/absent4,15.24mmrows/5mmpitch/1.4mmholes documentchecked
against savedCAD. Old21mmstock/sellerlot/firstfit not confirmed. Process/material/
tighterholes/registration/rings/PCBApanel/sourcing/orientation and physical/human
qualification remainOPEN. No suppliercontact/upload/order/payment or poweredtest.
RFQ13/JLC14ZIPs remain invalid for this variant.

'''
if '## Current prototype manufacturing-data handoff - C17,'not in s:index.write_text(s.replace('# E27 workflow index\n\n','# E27 workflow index\n\n'+heading,1),encoding='utf-8')
print('C17 package verified',upload['bytes'],handoff['bytes'],'mappedrelease errors',len(result['errors']),flush=True)

