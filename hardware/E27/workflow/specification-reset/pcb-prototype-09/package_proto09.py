from pathlib import Path
import json,hashlib,zipfile,shutil,subprocess,sys,io
from PIL import Image,ImageDraw,ImageFont
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-prototype-09';F=D/'fabrication';base='56094af47ed5e110168cf27a6763f7251576de9f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
mode=sys.argv[1]
if mode=='docs':
 job=F/'Velluneo_driver-job.gbrjob';j=json.loads(job.read_text());original=json.loads(job.read_text());j['GeneralSpecs']['ProjectId']['Revision']='PROTO09';j['GeneralSpecs']['Size']={'X':45,'Y':60}
 for rules in j['DesignRules']:
  for key in('PadToPad','PadToTrack','TrackToTrack'):rules[key]=.25
 put(job,j);put(D/'checks/job-metadata-normalization.json',dict(original=original,normalized=j,reason='Native exporter uses stroke-inclusive outline bounds45.05x60.05 and generic0.2mm netclass summary. Use45x60 centerline contour and actual project0.25mm minimum; stronger3/10mm custom rules remain in CAD. Metadata only; no Gerber artwork/drill modification.'))
 (F/'FABRICATION-NOTES.txt').write_text('''VELLUNEO PROTO09 — BARE BOARD PROTOTYPE / FABRICATION REVIEW

ONE rectangular PCB45.000x60.000mm, dimensions at route centerline; use supplied Edge_Cuts contour. Four copper layers in order F_Cu / In1_Cu / In2_Cu / B_Cu. Request JLCPCB JLC04161H-7628, nominal1.6mm, FR4 Tg155, outer35um / inner15.2um, ENIG, green LPI mask, white legends. Listed construction totals1.5862mm; nominal-minus-listed0.0138mm is not an invented dielectric. Confirm exact construction with buyer before production; no controlled impedance target. No panel, Vcut, castellations, blind/buried vias or edge plating.

IMPORTANT: EPOXY-FILLED AND COPPER-CAPPED through-vias, both ends.17designated holes:0.300mm drill,0.600mm copperpad; use designated-filled-vias.csv. Finish exposed caps as other exposed pads. DO NOT fill or cap the25component insertion holes. OnlyT1drilltool0.300mm corresponds to vias in this exact revision; the coordinate map is controlling. All component holes remain open and solderable. Ordinary tenting or soldermask plugging is not a substitute for filled/capped via-in-land sites. Confirm provider's ambiguous general0.15–0.55mm via-diameter label for this0.6pad/0.3hole combination before production.

Common plot/drill origin: nativeboard(77.5,130)mm; outputXright,Yup. Gerber coordinates6decimalmm, Excellon3decimalmm (maximum0.0005mm rounding per axis). PTH42holes =17vias+25componentholes; NPTH0. Separate empty NPTH file intentionally contains no hits. No slots. Outline stroke0.05mm is not extra material allowance. Use centerline45x60. IPC-D-356 netlist supplied for bare-board electrical continuity/short test, not energized functional test.

Mask openings follow supplied artwork; no extra openings in primary/secondary barrier. Do not add copper/thieving/tooling, marks or order numbers in isolation region. Remove order number if service permits; otherwise buyer must approve its exact noncritical location in production films. No undocumented copper repair/substitution. Inspect manufacturer production files, including via filling/capping selection, and require buyer confirmation before fabrication.

The order scope is bare boards for unpowered inspection and component-fit checks. This package is not supplier acceptance, a released assembled mains supply, safety certification, authorization to power or a placed order. See ORDER-CHECKLIST.txt and README. BOM/assembly files are outside the fabrication upload archive; custom transformer/formed terminals are not qualified for turnkey PCBA. No stencil/paste layers are included in bare-board order.
''',encoding='utf-8')
 (D/'ORDER-CHECKLIST.txt').write_text('''PROPOSED SINGLE ORDER SETTINGS — REVIEW BEFORE PAYMENT

Bare rigid FR4 boards only; selected4layer45x60mm design; suggested first lot5boards (quantity is a preparation default, not a user purchase/payment approval). Nominal1.6mm; exactJLC04161H-7628 construction; outer1oz / inner0.5oz; Tg155request; ENIG; greenmask / whitelegend; singlePCB, no panel. Epoxy-Filled&Capped for the17designated0.3mmthrough-vias, componentholes open. No impedancecontrol target; namedstackup still must match. Include bare-board e-test against IPC-D-356, no functional/powered testing. No PCBA or stencil order.

Before submitting production/payment:
1. Upload Velluneo_PROTO09_Fabrication_REVIEW.zip to vendor's review; preserve exact archive hash from manifest. Agent has not uploaded/sent it or contacted supplier.
2. Confirm quoted stackup/copper/laminate, filled/capped0.6pad/0.3hole service and exposedcapfinish; do not silently substitute tenting. Resolve minimum-ring/hole/width/mask/legend findings on actual files. Vendor acceptance and quote are not yet present.
3. Inspect actual production films: fourcopperlayers in correctorder, masks/legends and45x60routecenterline; no copper or identification marks crossing isolationband;42PTH and0NPTH;17filledvias ONLY. Confirm productionfiles option before fabrication. No vendor response has been invented.
4. Qualified technical reviewer must resolve open prototype-manufacturing/assembly findings and the toolkit's failed release/requirement/configuration gates for the intended scope. Previous CAD acceptance and this request do not erase those failures. Operating/insulation/thermal requirements remain required before energized work, independent of bare-board mechanical inspection.
5. Human buyer reviews finalquantity/price/shipping/taxes and explicitly places/pays order. No cost, leadtime or stock quote is claimed here.

AT RECEIPT, BEFORE ASSEMBLY: inspect outline/thickness/holes/caps/mask and compare drilling/map; verify unpowered continuity and isolation to independent netlist with suitable equipment. Dry-fit actual BR1/Q1/F1/R1/T1/C1/wires; do not force unqualified formed terminals. Reject cracked mask/laminate, damagedcaps, obstructedinsertionholes, drilling/registration errors or copper crossing isolationband. Record actual measurements and photographs against serial/revision.

ASSEMBLY/ENERGIZATION HOLD: customEFD25transformer construction/finishedinsulation, formedlead/filletgeometry and assemblyprocess need qualified approval. Check component values/polarity/orientation, soldering and lowvoltage shorts before any power. Startup/fault/current/gate/CS/VS/thermal and finishedcreepage/dielectric tests must follow an independently reviewed bring-up plan at suitable isolated facilities by competent personnel. This document supplies acceptance gates, not a validated mains test procedure or permission to energize.
''',encoding='utf-8')
 (D/'assembly-reference/README.txt').write_text('''REFERENCE ONLY — NOT A TURNKEY PCBA ORDER

BOM33references and nativepositions are supplied for engineering/fit review. SameMPNs/values/pins as DRIVER08. R14uses a named identical-land silk-only footprint variant. No automatic substitution or supplierpartnumbers assigned. CustomEFD25transformer is a manufacturing requirement, not an orderable approvedMPN. FormedBR1/Q1/R1 and provisionalF1 need actualparts/leadforming/finishedsolderjoint validation. SMT parts appear on bothsides; THT/manual assembly and heatcycle/support need qualified processreview. Native rotations/side are not calibrated to a specific assemblyhouse's library. No PCBA/stencil/panel job is released. See solderpaste geometry in CAD only if a later reviewedassemblyprocess needs a stencil.
''',encoding='utf-8')
 (D/'README.md').write_text('''# PROTOTYPE09 — selected board procurement preparation

This prepares the owner's one selected four-layer45×60mm driver for bare-board prototype fabrication review. Native copper, pads, placement, values, MPNs and81-pin electrical intent are unchanged from DRIVER08. Larger1mm/0.15mm legends and0.15mm legend clearance correct actual manufacturer capability mismatches. Three references moved; R14has a named same-land footprint with overlapping legend body lines removed. The matching schematic/BOM/library identifiers are updated. Electrical3/10/0.25mm rules are unchanged; only silk limits/checks are strengthened. Fresh final ERC/DRC/parity are0/0/0; inherited five ignored categories remain disclosed in the previous packet.

**Files are prepared; the order and formal release remain on hold.** This is a concrete fabrication-review package, not a claim that operating mains electronics are qualified. The request authorizes preparation/save, not payment, supplier contact, unperformed tests or human technical approval. Read ORDER-CHECKLIST.txt before using the archive. Actual vendor DFM/quote/process confirmation and open toolkit release/requirements/configuration findings are not replaced by exported Gerbers.

Use **Velluneo_PROTO09_Fabrication_REVIEW.zip** for a future bare-board supplier review: fourcopperGerbers, masks/legends, oneoutline,42PTH/emptyNPTH, IPC-D-356netlist, detailedstackup and17filled/cappedviamap. Centerlineoutline45×60 and commonorigin are independently reconciled against nativegeometry using Gerbonara1.5.0. Excellon coordinates have0.001mm resolution, within0.0005mm peraxis of native. Allninegraphic layers parse; actualCAM images are supplied. This is not independent full-net extraction or supplier acceptance. Parser warnings about KiCadG90 placement are disclosed; NPTH haszero hits and is explicitly classified. Suggested firstlot5boards is a preparation default, not a purchase authorization or price quote.

**Velluneo_PROTO09_Engineering.zip** contains the one editable project andlocaldependencies, source/assemblyreference/PDF/order documents. No turnkeyPCBA order is implied.33-referenceBOM retains customT1 and provisional/formedpart statuses. The delivered driver is rectangular; wholelamp targetØ60×120 and finishedfit/thermal/insulation remain unqualified. Native3D bodies are envelopeallocations.

Source baseline56094af47ed5e110168cf27a6763f7251576de9f; KiCad10.0.6; toolkit86614c3b9b43713031e0ea481edbe26b71cd1b8f. See task-contract, authorization, sourcebinding, native-preservation/CAM checks, exact fresh toolkitreports and four-role reviews. Historical findings C05-CTRL/SENSE/ISOL/FIT/CONFIG and C08-SIMP-01/02/03 remain at their original affected product/physical/release scopes. Human technical reviewer and process/sourcing owners must close observable acceptance criteria; no review vote creates approval. No safety standard text, vendor response, physicalmeasurements, poweredwaveforms or release pass is fabricated.

Actual CAM layers in pcb-preview.png show the fabrication outputs; native3D is source-bound. Artifacts/ZIPmemberhashes/CRC bind exact bytes. Earlier packets are immutable; this packet changes only silk/graphic footprint naming and adds production preparation/evidence. No layout alternative or new circuit is introduced.
''',encoding='utf-8')
 for name in('prepare_proto09.py','prepare_proto09_design.py','fix_proto09_silk.py','finalize_proto09_silk.py','check_proto09_native.py','check_proto09_cam.py','package_proto09.py'):
  s=(W/name).read_text().replace('W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());',"W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());");(D/name).write_text(s,encoding='utf-8')
 put(D/'silkscreen-changes.json',dict(text_height_mm=1,text_stroke_mm=.15,silk_graphic_stroke_min_mm=.15,silk_clearance_mm=.15,reference_positions_mm={'C4':[97,72.5],'R13':[107,128.4],'C1':[89,117.75]},R14_variant='CRCW_2512_R14_SilkClear',R14_only_body_legend_lines_removed=True,all_copper_and_pad_geometry_unchanged=True))
 put(D/'readiness.json',dict(fabrication_files_prepared=True,native_checks_pass=True,independent_CAM_parse_and_drill_outline_reconciliation_pass=True,order_placed=False,supplier_contact=False,vendor_DFM_confirmation=False,formal_release_pass=False,prototype_procurement_status='prepared_for_review_not_released_for_order',assembly_released=False,energization_authorized=False,blockers=['Vendor exact stackup/material/POFV geometry confirmation and production-film approval','Toolkit formal requirements/release/configuration gates remain failed','Qualified prototype manufacturing/formed-terminal/transformer construction assessment; operating/insulation/thermal qualification before energized tests']))
elif mode=='preview':
 image=Image.new('RGB',(1800,1650),'#101827');dr=ImageDraw.Draw(image);font=lambda n:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
 dr.text((45,30),'VELLUNEO / PROTOTYP PCB',font=font(38),fill='white');dr.text((45,88),'45 × 60 mm • 4 warstwy • poprawiony nadruk • pliki do przeglądu produkcyjnego',font=font(25),fill='#adc0d5')
 for i,side in enumerate(('top','bottom')):
  im=Image.open(D/('native-'+side+'.png')).convert('RGB');im.thumbnail((820,640));image.paste(im,(45+880*i,145));dr.text((45+880*i,795),'Góra'if i==0 else'Spód',font=font(24),fill='white')
 for i,key in enumerate(('top-copper','inner_1-copper','inner_2-copper','bottom-copper')):
  im=Image.open(D/('CAM-'+key+'.png')).convert('RGB');im.thumbnail((410,590));image.paste(im,(45+440*i,890));dr.text((45+440*i,845),('Gerber F.Cu','Gerber In1.Cu','Gerber In2.Cu','Gerber B.Cu')[i],font=font(23),fill='white')
 dr.text((45,1500),'Gerbery i wiercenia sprawdzone • 42 otwory • 17 przelotek do wypełnienia i pokrycia miedzią',font=font(24),fill='#72e0b0');dr.text((45,1550),'Zamówienie: po akceptacji wykonania i plików przez producenta. Badania działania i izolacji pozostają otwarte.',font=font(20),fill='#adc0d5');dr.text((45,1590),'Podgląd rzeczywistych plików. Bryły 3D pokazują gabaryty elementów.',font=font(20),fill='#adc0d5')
 image.save(D/'pcb-preview.png');target=W.parent/'outputs/Velluneo_prototype09.png';shutil.copyfile(D/'pcb-preview.png',target)
 ins=[D/'design/Velluneo_driver.kicad_pcb',D/'native-top.png',D/'native-bottom.png',*[D/('CAM-'+k+'.png')for k in('top-copper','inner_1-copper','inner_2-copper','bottom-copper')]];put(D/'preview-manifest.json',dict(inputs=[dict(path=p.relative_to(D).as_posix(),sha256=sha(p))for p in ins],output=dict(path='pcb-preview.png',sha256=sha(D/'pcb-preview.png'))));print(target)
elif mode=='zip':
 archives=[]
 for name,members in [('Velluneo_PROTO09_Fabrication_REVIEW.zip',{p.relative_to(F).as_posix():p.read_bytes()for p in F.iterdir()if p.is_file()}),('Velluneo_PROTO09_Engineering.zip',{**{p.relative_to(D/'design').as_posix():p.read_bytes()for p in(D/'design').rglob('*')if p.is_file()and not any(x in p.parts for x in('.work','__pycache__'))},**{p.relative_to(D).as_posix():p.read_bytes()for p in(D/'assembly-reference').rglob('*')if p.is_file()},**{n:(D/n).read_bytes()for n in('README.md','ORDER-CHECKLIST.txt','readiness.json')}})]:
  zpath=D/name
  with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED)as z:
   for n,raw in sorted(members.items()):z.writestr(zipfile.ZipInfo(n,date_time=(2026,11,19,0,0,0)),raw,compress_type=zipfile.ZIP_DEFLATED)
  with zipfile.ZipFile(zpath)as z:
   assert z.testzip()is None
   for n,raw in members.items():assert z.read(n)==raw
  archives.append(dict(path=name,sha256=sha(zpath),crc_pass=True,members=[dict(path=n,bytes=len(r),sha256=hashlib.sha256(r).hexdigest())for n,r in sorted(members.items())]))
 put(D/'artifact-manifest.json',dict(archives=archives,files=[dict(path=p.relative_to(D).as_posix(),sha256=sha(p))for p in sorted(F.iterdir())if p.is_file()]));print('Verified',[(a['path'],len(a['members']))for a in archives])
elif mode=='inventory':
 h=P/'hardware.json';old=json.loads(subprocess.check_output(['git','show',base+':hardware/E27/workflow/specification-reset/hardware.json'],cwd=R));j=json.loads(h.read_text());assert j==old;files=sorted(p for p in D.rglob('*')if p.is_file()and not any(x in p.relative_to(D).parts for x in('checks','.work','__pycache__','reviews'))and p.suffix in('.py','.json','.md','.txt','.csv','.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_dru','.kicad_mod','.kicad_sym','.wrl')and p.name not in('frozen-files.json','review-record.json','integration-record.md','stage-packet.md','inventory-delta.json'));added=[p.relative_to(P).as_posix()for p in files if p.relative_to(P).as_posix()not in j['source_files']];j['source_files']+=added;put(h,j);put(D/'inventory-delta.json',dict(base=base,prior_entries=len(old['source_files']),appended=len(added),entries=added,other_fields_unchanged=True))
 idx=R/'hardware/E27/workflow/project-index.md';s=idx.read_text();heading='''## Current prototype procurement preparation — PROTOTYPE09

[PROTOTYPE09](specification-reset/pcb-prototype-09/README.md) prepares the selected four-layer45×60mm board for bare-board fabrication review. Same copper/pads/electrical basis as DRIVER08; corrected1mm/0.15mm silkscreen and same-land R14legend variant. Fresh native0/0/0/ERC0, independently parsed9CAMlayers/42PTH/0NPTH/45×60outline and explicit17filled-via map. Fabrication-review and separateengineeringZIPs/orderchecklist supplied. Files are prepared, but supplierDFM/process/productionfilm confirmation and formalrelease gates remain open; no order, PCBArelease or energizedqualification is claimed. Older entries below retain historical scope.

''';idx.write_text(s.replace('# E27 workflow index\n\n','# E27 workflow index\n\n'+heading,1),encoding='utf-8',newline='\n');print('Added',len(added),'sources')
