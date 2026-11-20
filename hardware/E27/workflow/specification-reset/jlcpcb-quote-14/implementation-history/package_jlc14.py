from pathlib import Path
import json,hashlib,zipfile,shutil,csv
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';S=P/'supplier-review-13';D=P/'jlcpcb-quote-14'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def files(folder):return[p for p in sorted(folder.rglob('*'))if p.is_file()and p.suffix!='.kicad_prl'and not any(t in p.relative_to(folder).parts for t in('.work','__pycache__'))]
def archive(name,entries):
 out=D/name
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
  for p,n in entries:z.write(p,n)
 with zipfile.ZipFile(out)as z:
  assert z.testzip()is None and len(z.namelist())==len(set(z.namelist()))
  for p,n in entries:assert hashlib.sha256(z.read(n)).hexdigest()==sha(p)
 return dict(path=name,sha256=sha(out),bytes=out.stat().st_size,members=[dict(path=n,sha256=sha(p))for p,n in entries])
cam=json.loads((D/'checks/CAM-validation.json').read_text());assert cam['passed']and cam['SK_flashes']==17
drc=json.loads((D/'checks/drc.json').read_text());assert not drc['violations']and not drc['unconnected_items']and not drc['schematic_parity']
erc=json.loads((D/'checks/erc.json').read_text());assert not any(x['violations']for x in erc['sheets'])
upload=archive('Velluneo_JLC14_Gerber_Upload.zip',[(p,p.name)for p in files(D/'gerbers')]);assert len(upload['members'])==14 and upload['bytes']<100*1024*1024
# Only CAM belongs in the automatic upload; the complete handoff has separate support data.
put(D/'JLC14-manifest.json',dict(revision='JLC14',base_commit='b33e57c78eb3c1d644e3d00e96ccc5e47dc8bcaa',source_board_sha256='05e08b6cafcf2a980c1dd7d66d020364d72356808b41bf197c5b594edb8bb236',purpose='PCB quotation and separate manual assembly feasibility; no order or supplier contact',upload_archive=upload,support_files=[dict(path=p.relative_to(D).as_posix(),sha256=sha(p))for folder in('support','assembly-feasibility')for p in files(D/folder)],instructions=[dict(path=p.name,sha256=sha(p))for p in files(D)if p.parent==D and p.suffix in('.txt','.json','.md')and p.name not in('JLC14-manifest.json','artifact-manifest.json','frozen-files.json','review-status.json','review-record.json','finding-ledger.json','integration-record.md','stage-packet.md')]))
entries=[(D/upload['path'],upload['path']),(D/'JLC14-manifest.json','JLC14-manifest.json')]
for folder in('support','assembly-feasibility'):entries +=[(p,p.relative_to(D).as_posix())for p in files(D/folder)]
for n in('README.md','START_HERE_PL.txt','PCB-REMARK-PASTE.txt','PCB-REMARK-SHORT.txt','JLCPCB-ENQUIRY-UNSENT.txt','JLCPCB-TECHNICAL-RESPONSES.csv','quote-settings.json','jlcpcb-sources.json'):entries.append((D/n,n))
handoff=archive('Velluneo_JLC14_Quote_Handoff.zip',entries)
put(D/'artifact-manifest.json',dict(archives=[upload,handoff],all_CRC_memberlists_and_SHA256_verified=True,upload_contains_no_nested_ZIP_PDF_nativeCAD_BOM=True,upload_max100MB_verified=True,contains_11_manufacturing_Gerber_1SK_1Excellon_1map=True,portal_import_performed=False,supplier_contact=False))
# Verify the actual nested handoff's manufacturing payload and referenced assembly data.
with zipfile.ZipFile(D/handoff['path'])as z:
 with zipfile.ZipFile(__import__('io').BytesIO(z.read(upload['path'])))as g:
  assert g.testzip()is None and len(g.namelist())==14
 b=list(csv.DictReader(z.read('assembly-feasibility/BOM_26_SMT_QUOTE_REFERENCE.csv').decode('utf-8').splitlines()));c=list(csv.DictReader(z.read('assembly-feasibility/CPL_26_SMT_QUOTE_REFERENCE.csv').decode('utf-8').splitlines()));assert len(b)==len(c)==26 and {q['Designator']for q in b}=={q['Designator']for q in c}
 with zipfile.ZipFile(__import__('io').BytesIO(z.read('assembly-feasibility/Velluneo_RFQ13_Transformer_Assembly.zip')))as t:assert t.testzip()is None
put(D/'checks/package-verification.json',dict(passed=True,upload_SHA256=upload['sha256'],handoff_SHA256=handoff['sha256'],upload_members=14,handoff_members=len(handoff['members']),all_member_hashes_and_CRCs_verified=True,nested_upload_and_transformer_archives_verified=True,SMT_BOM_CPL_matching_designators=26,portal_upload_or_import_claim=False,visual_map='Coordinator inspected actual-coordinate map; labels8/10/12 separated, legend and17XYtable legible.'))
put(D/'checks/toolkit-impact.json',dict(toolkit_manifest_sha256='b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97',task='Packaging/export/support-document adaptation only',source_CAD_libraries_rules_requirements_approvals_unchanged=True,actual_native_ERC_DRC_parity_refreshed=True,prior_work_check='supplier-review-13/checks/current-work.json:2genuinehumanholds',prior_release_check='supplier-review-13/checks/current-release.json:14process/qualification/approvalholds',new_toolkit_configuration_migration_required=False,no_toolkit_tests_repeated_reason='No toolkit code/configuration or productdesigninput changes; fresh relevant native/export/CAM/archive checks are supplied.',impact='RFQ13 CAD reviews retained to unchanged source scope. NewauxiliaryCAM/mapping/quoteclaims require their own four-role JLC14 final review.'))
reqs=[('J14-SOURCE','No source CAD/library/rule/requirement or approval changes','source-binding.json'),('J14-CAM','11 manufacturing Gerbers +oneSK +one42PTHExcellon +onehumanmap, commonorigin, exactold9artwork','checks/CAM-validation.json'),('J14-FORM','Exact fieldvalues, full/short PCBRemark, special-hole/registration/stack/fill/support route','quote-settings.json'),('J14-ASM','33MPNs/26SMTreferenceBOM-CPL/7manualoperations, no inventedLCSC/machinecorrections, Standardpanelrequest','checks/assembly-format-check.json'),('J14-DELIVERY','Separate14memberupload andfullhandoff;allCRC/memberhashes;notclaimedliveportalacceptance','checks/package-verification.json'),('J14-WEB','Dated official JLCPCB sources mapped to applied instructions andlimitations','jlcpcb-sources.json')]
put(D/'task-acceptance.json',dict(criteria=[dict(id=i,criterion=c,evidence=e,result='demonstrated in prepared package')for i,c,e in reqs],formal_release=False,order_ready=False,supplier_confirmations_required=True,prior_physical_and_human_holds_retained=True))
H=D/'implementation-history'
for n in('export_jlc14.py','prepare_jlc14.py','polish_jlc14.py','check_jlc14_cam.py','package_jlc14.py'):shutil.copyfile(W/n,H/n)
(H/'README.md').write_text('''# Executed packaging history

Scripts were executed from the original workspace work/ directory using the
bundled1119Python, KiCad10.0.6 and installed Gerbonara1.5.0. Paths resolve there.
Export uses an extracted RFQ13 project clone; no production source is edited.
Run prepare before polish: polish supplies the final clean human-facing text.
The source RFQ13 transformer archive is copied unchanged into assembly-feasibility/.
This archive records the actual implementation, not a portable installation or
permission to submit files, purchase, manufacture or use unverified machine data.
''',encoding='utf-8')
print('JLC14 upload14files and fullhandoff CRC/memberhashes verified',upload['bytes'],handoff['bytes'],flush=True)
