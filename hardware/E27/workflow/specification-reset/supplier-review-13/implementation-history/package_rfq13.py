from pathlib import Path
import json, hashlib, zipfile, shutil, subprocess, os, sys
W=Path(__file__).resolve().parent; R=W/'Velluneo-readiness'; P=R/'hardware/E27/workflow/specification-reset'; D=P/'supplier-review-13'; E=D/'design'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j): p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def text(p,s): p.write_text(s,encoding='utf-8')
def files(folder): return [p for p in sorted(folder.rglob('*')) if p.is_file() and p.suffix!='.kicad_prl' and not any(v in p.relative_to(folder).parts for v in ('.work','__pycache__'))]
def archive(name,entries):
 out=D/name
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,n in entries: z.write(p,n)
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(set(z.namelist()))
  for p,n in entries: assert hashlib.sha256(z.read(n)).hexdigest()==sha(p)
 return dict(path=name,sha256=sha(out),bytes=out.stat().st_size,members=[dict(path=n,sha256=sha(p)) for p,n in entries])

text(D/'README.md','''# RFQ13 — selected isolated driver, manufacturer enquiry

Current board: 45 × 60 mm, four layers, 33 components, 81 pads, 304 tracks and 17 vias.
This packet supersedes TOOLKIT11 for the documented mechanical and spacing refinements.
It is the transformer-based driver discussed in this chat. Earlier packets are historical.

The documentary dimensional and assembly/insulation engineering review is complete for
technical enquiry, subject to the actual independent review disposition in review-status.json.
It does not physically confirm a custom transformer or formed parts before they exist.

## Files to use

- Velluneo_RFQ13_Enquiry_Pack.zip: complete enquiry handoff, drafts and response checklist.
- Velluneo_RFQ13_BarePCB_DFM.zip: the bare-board CAM package for the PCB manufacturer's DFM portal.
- Velluneo_RFQ13_Transformer_Assembly.zip: drawings, exact interfaces, BOM and questions for the winding/assembly shop.
- Velluneo_RFQ13_Engineering.zip: editable KiCad project with local libraries/models and current evidence.
- drawings/Velluneo_RFQ13_Dimensioned_Review.pdf: seven-page controlled dimensional/interface review.

The master enquiry ZIP and transformer ZIP are not automatic JLCPCB assembly uploads.
PCB fabrication and custom transformer/formed-part assembly require separate technical responses.
The drafts in supplier/ are UNSENT. Five bare boards is the proposed quotation quantity,
not an order. No supplier contact, purchase, payment, energized test or production release occurred.

## Changes and verification

T1 now reserves the complete requested 30 × 30 × 18 mm assembly, with a 30.5 mm courtyard,
rather than only the raw bobbin. R10 moves 0.5 mm left, C3 1.5 mm left, R17 0.35 mm right
and 0.4 mm down; one AUX_RAW corner moves 0.6 mm down. Attached copper follows these moves.
Values, MPNs, all pin/net assignments, pad/hole geometry, dedicated SENSE/CS copper and
separate current-return branches are retained. The R1 native model now represents its
raised cylindrical dimensional allocation; appearance models do not qualify a formed part.

The pinned toolkit is unchanged: manifest b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97.
Actual preview/apply strengthens primary/secondary rules from 10.0 to 10.7 mm without
weakening other pairs. Fresh native ERC, DRC, unconnected and parity counts are zero.
The conservative all-layer projected P/S copper gap is at least 10.725 mm. The proposed
0.35 mm finishing allowance on each side leaves 10.025 mm; actual production tolerances
still need agreement. These are engineering screens, not claimed IEC tabulated minima.
Nine CAM layers and 42 plated holes are independently matched to native CAD. The via map
identifies 17 filled/capped vias, leaving 25 component insertion holes open.

## What the manufacturer must confirm

The exact finished T1 drawing/STEP, full pin tolerances, clip/core/terminal sections and
insulation materials/process remain supplier deliverables. The Q1 forming proposal requires
an incoming usable lead length of at least 13.0 mm, a controlled jig and first-article fit;
the semiconductor datasheet alone does not guarantee this length. R1 and BR1 also require
supported forming and a returned drawing. C1 requires strain-free pitch alignment and at
least 2 mm free vent space. No blanket 2 mm transformer spacer is permitted.

Read mechanics/ASSEMBLY-AND-ISOLATION-REVIEW.md and the 12 supplier response IDs. Actual
PCB process/films, finished construction, full insulation assessment and physical electrical,
fault and thermal qualification remain open. Genuine current human stage/release approval
is not replaced by an agent review. Parent lamp requirements remain preserved.

Production ordering and energization remain on hold; technical DFM/quotation can proceed
when the independent enquiry review is accepted. Changes require exact-file re-review.
''')
text(D/'mechanics/ASSEMBLY-AND-ISOLATION-REVIEW.md','''# RFQ13 assembly and insulation engineering review

The documentary and current-CAD review is complete for technical enquiry. Physical part
dimensions and finished insulation are not qualified by this review. The dimensioned PDF,
component-interfaces.json, assembly-calculations.json and official sources S1–S12 define
the exact facts, conditional calculations and supplier acceptance requests.

## Corrections completed in the current CAD

The former-only T1 reservation is replaced by a requested finished body of 30 × 30 × 18 mm
and a 30.5 mm courtyard. R10 moves 0.5 mm left; C3 1.5 mm left; R17 0.35 mm right and
0.4 mm down. The AUX_RAW corner moves 0.6 mm down. All 81 pin assignments, values/MPNs,
SENSE/CS copper and separate return branches are retained. Native ERC/DRC/parity pass.

Primary/secondary projected and common-layer copper separation is at least 10.725 mm.
With the retained proposed 0.35 mm finished-growth allowance on each domain, the remaining
budget is 10.025 mm. This closes the earlier arithmetic shortfall under that explicit
assumption. It does not establish a manufacturer's tolerances or an IEC minimum.

The 3 mm HV/quiet rule is a common-copper-layer screen. STARTUP_MID on B.Cu and VDD on
In2.Cu overlap in projection within the primary domain. This requires confirmation of
minimum pressed dielectric and functional dielectric/coupling assessment. It is not a
P/S crossing or an invented all-layer 3 mm clearance. The separate all-layer P/S audit
includes physically present NC pins. All board zones are exclusion areas, not omitted pours.

C1's maximum 10.5 mm case circle contains no unrelated B.Cu copper. Reserve at least
2 mm free space beyond its vent. The requested maximum mounted body height is 22.5 mm
and the service envelope is 24.5 mm from the bottom PCB face. Sleeve/PET is not credited
as reinforced insulation. F1 and C4 are SMD; F1 has no insertion leads or holes.

## Dimensions and forming: documentary closure and supplier hold

TDK's raw former drawing establishes 12.9 mm maximum height and 3.5 ± 0.2 mm pins, not
the complete wound, clipped and sleeved transformer envelope. The 30 × 30 × 18 mm finished
envelope is a procurement limit requiring a returned drawing/STEP and first-article check.
PCB thickness is 1.44–1.76 mm. Flush mounting leaves 1.54–2.26 mm pin tails; adding a
blanket 2 mm spacer can leave −0.46 to +0.26 mm and is excluded.

Q1 proposal Q13-FORM-A requires incoming usable leads ≥13.0 mm, a specified datum,
root straight 3.70–3.80 mm, inside bend radius 0.70–0.75 mm and offset 5.08 ± 0.05 mm.
The worst calculated developed length is 12.745752 mm, leaving 0.254248 mm only if
the incoming screen is met. This is not a datasheet guarantee. The supplier must return
selection yield, jig/formed drawing and a first-article fit. No pin reassignment is allowed.
R1 requires supported forming, body-bottom height 5.0–5.5 mm and maximum body top 13 mm.
BR1 requires supported forming to the native 5.5 mm square pattern and 3–4 mm standoff.
C1 must fit without lead or seal strain; exact lead diameter/position limits remain open.

## Transformer insulation and mounting disposition

T1.3 remains primary; T1.7/8/9 remain secondary. These physical terminals are unwound,
without hidden junctions. Core and yokes are treated as primary. Intact secondary TIW
must continue into controlled terminal zones; bare secondary wire cannot cross primary,
core or yoke regions. The proposed winding build is a reference for supplier review,
not an accepted electrical insulation system. Unspecified resin, enamel, soldermask,
PET sleeves and an unqualified 0.5 mm wall receive no reinforced-insulation credit.

The builder must return exact core/yoke and secondary exit/strip sections, insulation
materials and qualified process, full pin pattern, finished dimensions and a proposed
test basis for review. No unavailable standards table or test voltage/duration is invented.
The PCB manufacturer must confirm laminate/pressed dielectric, hole position/registration,
finished annular rings and filled/capped-via process, and return production films.

These supplier responses are explicit open acceptance inputs in supplier-response-checklist.csv.
No substitution, terminal change, relaxed spacing or production start is authorized by
the enquiry. Housing retention, complete-lamp fit/thermal performance and powered
startup/fault/insulation qualification remain outside the bare-board request. Parent
requirements are retained. Agent reviews do not replace real stage/release approval.
''')
text(D/'supplier/READ_FIRST.txt','''VELLUNEO RFQ13 — TECHNICAL ENQUIRY ONLY, NOT A PRODUCTION ORDER

Please use the exact SHA-256 identified files in RFQ13-manifest.json.
Bare PCB shop: use Velluneo_RFQ13_BarePCB_DFM.zip and PCB-ENQUIRY-UNSENT.txt.
Transformer/assembly shop: use Velluneo_RFQ13_Transformer_Assembly.zip and
TRANSFORMER-ASSEMBLY-ENQUIRY-UNSENT.txt. The dimensioned PDF controls requested interfaces.
Please complete supplier-response-checklist.csv, return dimensioned redlines/DFM
and identify any requirement you cannot guarantee. No work may begin from this enquiry.
Finished part drawings, first-article fit and construction/process acceptance remain open.
''')

# Archive packaging uses only current, explicitly separated handoffs.
bare=archive('Velluneo_RFQ13_BarePCB_DFM.zip',[(p,p.relative_to(D/'fabrication').as_posix())for p in files(D/'fabrication')])
asm_entries=[]
for folder in ('mechanics','assembly-reference'):
 asm_entries += [(p,p.relative_to(D).as_posix())for p in files(D/folder)]
asm_entries += [(D/'drawings/Velluneo_RFQ13_Dimensioned_Review.pdf','Velluneo_RFQ13_Dimensioned_Review.pdf')]
asm_entries += [(D/'supplier'/n,n)for n in ('TRANSFORMER-ASSEMBLY-ENQUIRY-UNSENT.txt','supplier-response-checklist.csv','READ_FIRST.txt')]
assembly=archive('Velluneo_RFQ13_Transformer_Assembly.zip',asm_entries)
eng=archive('Velluneo_RFQ13_Engineering.zip',[(p,p.relative_to(E).as_posix())for p in files(E)])
payload=[bare,assembly,eng]
put(D/'RFQ13-manifest.json',dict(revision='RFQ13',source_board_sha256=sha(E/'Velluneo_driver.kicad_pcb'),purpose='Technical enquiry/DFM; no order or physical qualification',payload_archives=payload,documents=[dict(path=p.relative_to(D).as_posix(),sha256=sha(p))for p in [D/'drawings/Velluneo_RFQ13_Dimensioned_Review.pdf',*files(D/'supplier')]]))
master_entries=[(D/x['path'],x['path'])for x in payload]+[(D/'RFQ13-manifest.json','RFQ13-manifest.json'),(D/'drawings/Velluneo_RFQ13_Dimensioned_Review.pdf','Velluneo_RFQ13_Dimensioned_Review.pdf')]+[(p,p.name)for p in files(D/'supplier')]
master=archive('Velluneo_RFQ13_Enquiry_Pack.zip',master_entries)
put(D/'artifact-manifest.json',dict(archives=payload+[master],archive_CRC_and_all_member_hashes_verified=True,source_board_sha256=sha(E/'Velluneo_driver.kicad_pcb')))

# Extract into a new local directory and run actual KiCad against the distributed project.
Q=D/'.work/portable'; Q.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(D/eng['path'])as z:z.extractall(Q)
checks=[]; K=W/'kicad-10.0.6/bin/kicad-cli.exe'
for label,args in [('erc',['sch','erc','--format','json','--output',str(Q/'portable-erc.json'),str(Q/'Velluneo_driver.kicad_sch')]),('drc',['pcb','drc','--schematic-parity','--format','json','--output',str(Q/'portable-drc.json'),str(Q/'Velluneo_driver.kicad_pcb')])]:
 cmd=[str(K),*args];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
 report=json.loads((Q/('portable-'+label+'.json')).read_text())
 assert r.returncode==0,(r.stdout,r.stderr)
 if label=='drc': assert not report.get('violations') and not report.get('unconnected_items') and not report.get('schematic_parity')
 else: assert not any(q.get('violations')for q in report.get('sheets',[]))
 checks.append(dict(check=label,exit_code=r.returncode,report=report))
put(D/'checks/portable-project.json',dict(engineering_zip_sha256=eng['sha256'],checks=checks))
print('Four archives CRC/member hashes and extracted native ERC/DRC/parity PASS',flush=True)
