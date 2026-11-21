exec((__import__('pathlib').Path(__file__).parent/'build_c17.py').read_text().split("base='a283")[0])
import warnings, math, xml.etree.ElementTree as ET
from gerbonara import GerberFile,ExcellonFile,LayerStack
from gerbonara.utils import MM
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
base='a283213194bb16990d7614874d12336524f66fcf'
binding=json.loads((D/'source-binding.json').read_text());audit=json.loads((S/'checks/native-audit.json').read_text())
holes=list(csv.DictReader((D/'support/component-holes.csv').open()));vias=list(csv.DictReader((D/'support/filled-vias.csv').open()))
F=D/'gerbers'; notes=[]
with warnings.catch_warnings(record=True)as ws:
 warnings.simplefilter('always');drill=ExcellonFile.open(F/'Velluneo_C17.XLN',plated=True)
 notes=[str(x.message)for x in ws]
expected=[(float(x['X_mm']),float(x['Y_mm']),float(x['Finished_target_mm']))for x in holes]+[(float(x['X_mm']),float(x['Y_mm']),float(x['Diameter_mm']))for x in vias]
remaining=list(drill.objects);assert len(remaining)==42
for x,y,d in expected:
 match=[i for i,a in enumerate(remaining)if abs(a.aperture.diameter-d)<1e-6 and max(abs(a.x-x),abs(a.y-y))<=.000501];assert match,(x,y,d);remaining.pop(match[0])
assert not remaining
sk=GerberFile.open(F/'Velluneo_C17.sk');assert len(sk.objects)==24
for v in vias:assert any(max(abs(o.x-float(v['X_mm'])),abs(o.y-float(v['Y_mm'])))<1e-6 and abs(o.aperture.diameter-.3)<1e-6 for o in sk.objects)
outline=GerberFile.open(F/'Velluneo_C17.GKO');assert len(outline.objects)==4
vertices={(round(v,6),round(w,6))for o in outline.objects for v,w in [(o.x1,o.y1),(o.x2,o.y2)]};assert vertices=={(0.,0.),(45.,0.),(45.,60.),(0.,60.)}
assert sum(abs(o.aperture.diameter-.3)<1e-6 for o in drill.objects)==24
layers=[]
for ext in ['GTL','G2L','G3L','GBL','GTS','GBS','GTO','GBO','GTP','GBP','GKO']:
 g=GerberFile.open(F/('Velluneo_C17.'+ext));assert g.objects
 svg=str(g.to_svg(force_bounds=((-1,-1),(46,61)),fg='#173f70'))
 (D/'preview'/f'CAM-{ext}.svg').write_text(svg,encoding='utf-8')
 doc=fitz.open(stream=svg.encode(),filetype='svg');doc[0].get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(str(D/'preview'/f'CAM-{ext}.png'))
 layers.append(dict(layer=ext,objects=len(g.objects)))
# Compare fresh schematic graph with independent pre-capture intent, physical pin sets.
parts=json.loads((E/'proposed-parts.json').read_text());exp={};nc=set()
for a in parts:
 for pin,net in a['pins'].items():
  if net is None:nc.add((a['ref'],pin))
  else:exp.setdefault(net,set()).add((a['ref'],pin))
root=ET.parse(D/'support/netlist.xml').getroot();actual=[]
for n in root.findall('./nets/net'):
 members={(x.attrib['ref'],x.attrib['pin'])for x in n.findall('node')if x.attrib['ref']in{a['ref']for a in parts}}
 if members and not members<=nc:actual.append(frozenset(members))
assert {frozenset(v)for v in exp.values()}==set(actual)
put(D/'checks/CAM-validation.json',dict(passed=True,parser='Gerbonara1.5.0',layers=layers,manufacturing_Gerbers=11,auxiliary_SK=1,selected_filled_vias=24,component_holes_open=18,PTH_total=42,NPTH=0,outline_mm=[45,60],outline_four_closed_segments=True,all_drills_match_native_audit=True,drill_coordinate_tolerance_mm=.000501,SK_matches_all_and_only_0p3mm_vias=True,independent_pre_capture_pin_graph_matches_fresh_netlist=True,source_board_sha256=binding['source_board_sha256'],parser_warnings=notes,limits='Independent CAM layer/outline/hole/SK and schematic-graph checks; not full CAM electrical extraction, live portal acceptance, process qualification or measurement.'))
# Verify current T1 artwork against maker dimensions; no claim about unknown seller lot.
center=next(x['xy_mm']for x in audit['parts']if x['ref']=='T1')
pinxy={'1':[-10,7.62],'2':[-5,7.62],'3':[0,7.62],'5':[10,7.62],'6':[10,-7.62],'7':[5,-7.62],'8':[0,-7.62],'9':[-5,-7.62],'10':[-10,-7.62]}
for pin,xy in pinxy.items():
 pad=next(a for a in audit['pads']if a['id']=='T1.'+pin);assert all(abs(pad['xy_mm'][i]-center[i]-xy[i])<1e-6 for i in [0,1]);assert pad['hole_mm']==1.4 and pad['size_mm']==[1.95,2.3]
assert not any(a['id']=='T1.4'for a in audit['pads'])
put(D/'support/transformer-dimensions.json',dict(manufacturer='MYRRA',MPN='74032',current_drawing_body_max_mm=[26.5,22.5,26.5],width_axis='26.5mm along pin rows (X in native footprint)',row_spacing_mm=15.24,row_spacing_tolerance_mm=.3,pin_pitch_mm=5,pitch_chain='8x5.0 +/-0.3 as shown on maker drawing; do not silently reinterpret as eight pads on one row',pin_square_mm=.64,lead_length_below_seating_mm=4,lead_length_tolerance_mm=.5,manufacturer_recommended_PCB_drill_mm=1.4,physically_present_pins=9,absent_pin=4,component_side_local_xy_mm=pinxy,body_artwork_mm=[26.5,22.5],reservation_height_mm=26.5,pin_map_and_holes_match_saved_C16=True,documentary_dimension_confirmation=True,physical_lot_confirmation=False,old_stock='Legacy21mm-high version has different body/pin construction. ENIKA lists27x27x21mm; lot is not confirmed. No automatic old-stock substitution. Require current drawing, photo and first-fit inspection.',fit_tolerance='Nominal footprint matches maker recommendation. Row-spacing tolerance/pin straightness and first insertion remain supplier/first-article checks; no guaranteed assembly yield inferred.',sources=[dict(path='MYRRA74032.pdf',url='https://www.atd-shop.com/www/prilohy/74032-datasheet.pdf',sha256=sha(D/'support/MYRRA74032.pdf')),dict(path='MYRRA74032-PCN.pdf',url='https://cdn.soselectronic.com/productdata/21/43/1aa1b4fc/74030.pdf',sha256=sha(D/'support/MYRRA74032-PCN.pdf'))]))
sources=[('Gerbers','https://jlcpcb.com/help/article/gerber-files-preparation','One outline, named inner layers, auxiliary SK purpose in PCB Remark; human drill map supplied.'),('Vias','https://jlcpcb.com/help/article/pcb-via-covering','Nonconductive epoxy fill plus copper caps both ends; select all0.300mm vias; keep component PTH open.'),('KiCad export','https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-8','Fresh11layers+Excellon and map; common retained plot origin instead of tutorial Absolute example.'),('PCB limits','https://jlcpcb.com/capabilities/pcb-capabilities','Public PTH+0.13/-0.08mm, holeposition+/-0.075mm; tighter+/-0.05mm service limited to multilayer ENIG round0.55..2mm holes. Written acceptance required.'),('CPL','https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly','Metric XY, Top/Bottom and CCW angles; native footprint origins/angles require body-centroid/feeder validation.'),('BOM','https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation','BOM/CPL same28SMTreference set; exact MPNs; no guessed LCSC matching.'),('Assembly','https://jlcpcb.com/capabilities/pcb-assembly-capabilities','StandardPCBA minimum70x70mm; request handling panel/rails/fiducials preserving finished45x60mm.'),('External parts','https://jlcpcb.com/help/article/how-to-use-my-own-parts-for-pcb-assembly-order','GlobalSourcing/Consignment and MyParts require actual receipt/selection and supplier agreement.')]
put(D/'jlcpcb-sources.json',dict(checked='2026-11-21 Europe/Warsaw',sources=[dict(topic=a,url=b,application=c)for a,b,c in sources],limitations='Official public pages; no account/upload/quote/supplier acceptance/stock reservation.'))
settings=[('Material','FR-4 Tg155 request; actual laminate/CTI/RTI/minimum dielectrics to confirm'),('Layers','4: GTL/G2L/G3L/GBL = F.Cu/In1.Cu/In2.Cu/B.Cu'),('Finished size','45x60mm; no slots or mounting holes'),('Quantity','5 finished boards, quote basis only'),('Delivery','Single boards for barePCB quote; separate panel proposal for PCBA'),('Thickness','1.6mm nominal, +/-10% request'),('Copper','Outer1oz35um; inner0.5oz15.2um nominal source foil, actual finished values to confirm'),('Stackup','JLC04161H-7628 requested; no unreviewed substitute'),('Finish','ENIG; green mask, white legend both sides'),('Via covering','Epoxy-Filled & Capped; all24marked0.300mm vias both ends'),('T1 holes','Nine finished1.400mm round PTH, required1.350..1.450mm; tighter-hole service to confirm'),('Other holes','Nine insertion PTH per holelist remain OPEN; Q1 target1.700mm, C1 target1.000mm, J1/J2target1.600mm; confirm tolerance/rings'),('Registration','Requested<=0.025mm copper-to-hole displacement for conditional ring budget; not claimed public standard capability'),('Electrical test','Full bare-board continuity/shorts test requested'),('Added marks','Remove/no added copper marks, thieving or tooling in protected band'),('Production file confirmation','Request explicit later review; no automatic confirmation'),('PCBA','Separate Standard two-sided manual feasibility quote; exact MPNs, sourcing, panel and orientations must be confirmed'),('Stencil','Do not order standalone; assembler proposes stencil/paste process after assembly approval')]
put(D/'quote-settings.json',dict(status='Prepared fields, not configured cart',form='https://cart.jlcpcb.com/quote',settings=[dict(field=k,value=v)for k,v in settings]))
remark='''C17/C16 PROTOTYPE QUOTE + DFM ONLY. 45x60mm,4L,1.6mm,ENIG,JLC04161H-7628 requested. Velluneo_C17.sk is AUXILIARY VIA-FILL SELECTION, NOT copper/outline: epoxy-fill and copper-cap BOTH ends of all24 marked0.300mm vias ONLY. Leave18component PTH OPEN. T1 nine FINISHED holes1.400mm REQUIRED1.350..1.450mm; standard+0.13/-0.08 NOT accepted. Quote tighter-hole service on T1; soldered insertion, not press-fit terminals. Requested copper/hole registration<=0.025mm and finished rings>=0.20mm require written response; see holelist/tolerance notes. Keep all four copper layers clear of additions across outputX0..45,Y37.865..47.100mm: no thieving/tooling/copper marks. Confirm laminate/CTI/RTI/minimum pressed dielectrics, fill/cap and actual finished copper. No artwork substitution or automatic productionfile confirmation. Separate Standard two-sidedPCBA quote; preserve45x60finished board and propose handling panel. Not production authorization.'''
txt(D/'PCB-REMARK-PASTE.txt',remark+'\n')
txt(D/'START_HERE_PL.txt','''C17 - aktualny pakiet prototypu oparty na C16

1. Do wyceny samej plytki sluzy Velluneo_C17_Gerber_Upload.zip.
2. Ustawienia: quote-settings.json. Wklej CALY PCB-REMARK-PASTE.txt do uwag.
3. Pelny pakiet przekaz do recznego przegladu technicznego JLCPCB: otwory T1,
   rejestracja miedzi, wypelnianie24przelotek, material i izolacja wymagaja odpowiedzi.
4. Osobno popros o wycene montazu28SMD i opcjonalnie3THT. Przewody poza baza wyceny.
   BOM/CPL sa w assembly/. Nie zatwierdzaj automatycznych zamiennikow ani orientacji.
5. Transformator to gotowy MYRRA74032, obecna wersja26.5x22.5x26.5mm max.
   Starsza oferta27x27x21mm nie jest potwierdzona zamiana; sprawdz rzeczywista partie.
6. Po pisemnej akceptacji procesu, montazu i aktualnych plikow mozna podjac decyzje
   o wykonaniu prototypu do badan. Ten pakiet nie potwierdza dzialania ani bezpieczenstwa.

Nie wyslano zapytania, nie dokonano platnosci ani zamowienia. Stare JLC14/RFQ13 nie sa
plikami tej wersji. Aktualny zrodlowy projekt KiCad pozostaje w catalogue-pcb-16/design.
''')
txt(D/'README.md','''# C17 - current C16 prototype fabrication and assembly handoff

This package binds fresh manufacturing exports to the unchanged C16 board at
commit a283213194bb16990d7614874d12336524f66fcf. The finished driver is45x60mm,
four layers,33positions/80pads,28SMTparts,3THTparts and2wire-pad pairs.

Use Velluneo_C17_Gerber_Upload.zip for bare-PCB quotation. The complete
Velluneo_C17_Prototype_Manufacturing_Package.zip contains separate assembly BOM/CPL,
drawings, transformer evidence, process instructions, checks and portable native CAD.
Read START_HERE_PL.txt, quote-settings.json and PCB-REMARK-PASTE.txt. Use the unsent
technical enquiry for separate barePCB and assembly-feasibility review.

Fresh native ERC/DRC/parity/unconnected are zero. Independent CAM verifies11Gerbers,
oneSK selecting24filled/capped vias,42PTH including18open insertionholes, one45x60outline
and common coordinates. Exact document-based T1dimensions and pin mapping are checked.
The current MYRRA sheet specifies26.5x22.5x26.5mm maximum, not the old21mm-high stock.

This is a prepared manufacturing-data candidate for prototype DFM/quotation, NOT a
manufacturing release or a ready automatic full-PCBA order. TighterT1holes, registration,
minimumrings, actual material/dielectrics and PCBA process/panel must be accepted in
writing. Native footprint origins/angles are not verified feeder/centroid data.
LCSC fields stay blank in upload BOM until exact matching/availability is confirmed;
observed sourcing codes/routes are provided separately in FULL BOM and sourcingregister.
Harness is excluded from base quote; lengths/sleeving/strain relief remain undefined.

All C16 fault/startup/magnetics/clamp/thermal/insulation/first-fit and lamp integration
holds remain. Missing revised human approvals and physical evidence are reported by
the pinned toolkit; no tests or approvals are invented. No supplier message, account
upload, payment or order occurred. Both-face previews are saved copper diagrams,
not assembled3D renders. Historical RFQ13/JLC14 manufacturing ZIPs are superseded.
''')
txt(D/'support/FABRICATION-REQUIREMENTS.txt','''C17 fabrication / DFM acceptance request

Gerber order GTL/G2L/G3L/GBL = F.Cu/In1.Cu/In2.Cu/B.Cu. OneGKO outline,
two masks, two legends, two pastes. ExcellonXLN is FINISHED plated-hole targets,
not uncompensated drill tools. One human drillmap and one auxiliarySK selection.
All coordinates use nativeX-77.5,130-nativeY mm; board0..45x0..60. Do not mirror
bottom manufacturing files. Human bottom assembly drawing alone is mirrored.

24diameter0.300mm throughvias: NONconductive epoxy-fill and copper-cap BOTH ends;
not tenting/ordinary mask plugging. All18componentholes must remain open.
No plated/nonplated slots, blindvias or NPTH. All listed component holes are round.

T1nine finishedholes1.400+/-0.050mm REQUIRED. Public standard+0.13/-0.08 would
allow1.320..1.530mm, not acceptable to this request. Ask whether the advertised
tighter-hole service can apply to these soldered insertionholes. They are not
press-fit terminals. Maker recommends1.4mm; pitch/row tolerance and actual firstfit
remain to be checked with a current-part sample before accepting assembly yield.

T1landX1.950mm; declared minland1.925, maxhole1.450 and relative registration0.025
give minimumring(1.925-1.450)/2-0.025=0.2125mm. Q1land2.350/hole1.700; declared
minland2.325,maxhole1.830,registration0.025 gives0.2225mm. These are CONDITIONAL
budgets, not manufacturer guarantees. Public holeposition+/-0.075mm does not
establish0.025mm copper/hole registration. Return guaranteed finishedrings>=0.20mm
on all component/via pads, registration, land/cap tolerances and any proposed changes.

Protect all-layer no-copper band outputX0..45,Y37.865..47.100mm. No thieving,
tooling/identification copper or modifications in band. FinishedP/Scopper and
finished insulation remain subject to process/product review, not a Gerber certificate.
Nominal CAD projected P/Scopper11.146726mm is not a guaranteed finished distance.

Request exactJLC04161H-7628, FR4Tg155,1.6mm+/-10%, ENIG,green/white, outer35um/
inner15.2um nominal source construction. Confirm laminate identity, CTI/RTI, pressed
dielectric minimums and finishedcopper. Do not substitute stackup/material silently.
Request full bare-board continuity/shorts test. Ask for prequoteDFM and later explicit
productionfile review; a paid-order film service is not a claimed free prequote check.
''')
txt(D/'assembly/READ_BEFORE_ASSEMBLY.txt','''C17 assembly candidate - manual feasibility and quotation

Quote five finished45x60boards: optionA28SMT on both faces; optionB addsT1/Q1/C1.
J1/J2arewirepadpairs, not connectors; exclude harness from base quote. Full33list
also identifies exact wire rawmaterial, but no cutlength/sleeve/strainrelief is released.
No DNP electronicpositions. Do not substitute MPN, package, rating or suffix.

BOM_28_SMT.csv and CPL_28_SMT.csv are matching JLC-style CSVs. All LCSC upload fields
are blank pending exact vendor match. BOM_33_FULL.csv includes observed sourcing hints
and purchase links, not reserved stock. Ask GlobalSourcing/Consignment feasibility;
do not assume externally purchased parts are accepted or already in MyParts.

CPL uses native footprint origins, positiveCCW normalized0..360degrees, mm and
Top/Bottom. Both faces share top-viewXY; bottomX is NOT negated. Body centroid and
supplier feeder-zero offsets must be checked for every package in placement preview.
assembly-top/bottom.svg show native fab/padnumber orientation; bottom drawing is
physically mirrored. All33nativepositions supplied separately for engineering reference.
Request corrected machineCPL and marked polarities for independent approval.

StandardPCBA minimum70x70mm exceeds the finished45x60board. Ask JLC to propose
panel/rails/fiducials/tooling and tab locations outside finishedoutline; retain all
existing copperclearances and no-copper band. No panel artwork is released here.
Quote stencil/paste/reflow process after mixedpackage checks; original paste apertures
are exported, not a processqualified stencil. Large factorySMD R1/BR1 and hybridC4
need package/reflow/handling confirmation. C1/T1/Q1 areTHT, not pickandplaceSMT.

T1=currentMYRRA74032,9pins,pin4absent. Reject wrongpinmap, oldbody substitute or
forced insertion. Q1straightleads: lowestwide shoulder>=3mm abovePCB, bodybottom
approx6.5mm, reservedheight29.7mm; agree controlled fixture/support and inspect before
soldering/trim. No userleadforming or customtransformer winding. C1frontmounted,
correctpolarity and>=2mm ventclearance. Follow operations.csv and dimensionedPDF.

Before energizing verify every polarizedcomponent, connector/wire net, solderjoint,
clearance, insulation, partlot and actualmechanical fit. Follow bring-up plan; no
electrical/thermal/insulation test was performed by generating these files.
''')
questions=[('F01','Can you fabricate the exact four-layer stack/material, finish and thickness requested? Return CTI/RTI and minimum finished dielectrics.'),('F02','Accept T1 nine FINISHED1.400+/-0.050mm holes for soldered insertion? State actual service/cost.'),('F03','Guarantee>=0.20mm finishedrings and stated land/hole/cap/registration limits? Requested registration<=0.025mm is nonstandard.'),('F04','Confirm all24SK-selected0.300mm vias epoxy-filled/copper-capped BOTH ends,18componentholes open.'),('F05','Preserve all-layer protected band and provide exact-file DFM/productionfile review route.'),('A01','Quote28SMT two-sided, then separately additional3THT. Harness excluded. Confirm exact MPNs and external sourcing/consignment.'),('A02','Provide handlingpanel/rails/fiducials for45x60finished board, centroid/feeder-angle corrections and marked placementpreview.'),('A03','Accept actual currentT1sample/firstfit and Q1shoulder>=3mm fixture/support withoutleadforming? Return assembly limits.'),('R01','List every proposed change, fee, exception, MOQ and acceptancecondition before order; no automatic substitutes.')]
csvout(D/'JLCPCB-TECHNICAL-RESPONSES.csv',['ID','Question','Supplier_response','Evidence','Status'],[dict(ID=i,Question=q,Supplier_response='',Evidence='',Status='OPEN - no supplier contact')for i,q in questions])
txt(D/'JLCPCB-ENQUIRY-UNSENT.txt','''Subject: C17 isolated driver prototype - bare PCB and separate assembly feasibility quote

Hello,
Please review the attached C17 prototype package based on the C16 design. Please
quote5finished45x60mm four-layer PCBs and separately assess assembly of28SMTparts
on both sides, with optional3THTparts. Harness wiring is excluded from the base quote.

The ZIP includes current Gerbers/drills,24viafill selection,18opencomponentholes,
fullMPNBOM,SMTBOM/CPL,assembly drawings and currentMYRRA74032manufacturer evidence.
Please answer all IDs in JLCPCB-TECHNICAL-RESPONSES.csv. In particular T1hole
tolerance, minimumrings/registration, filled/cappedvias, material/dielectric limits,
panelhandling, externalparts and machineorientation need written confirmation.

Please return all DFM redlines, process/sourcing constraints, costs/MOQs and required
changes before any order. No unreviewed artwork, part or stack substitutions.
This is a technical quotation request only, not authorization to fabricate, assemble,
charge a service fee or begin production. Electrical qualification is pending.

Thank you.

UNSENT DRAFT - no supplier was contacted by preparing this package.
''')
txt(D/'task-contract.md','''# C17 bounded manufacturing-data task

Owner explicitly requests a complete production package and transformer dimension
confirmation; earlier instruction authorizes GitHub publication. BaseC16commit
a283213194bb16990d7614874d12336524f66fcf. Root is sole writer of manufacturing-c17
and project-index entry. NativeCAD/libraries/rules/requirements/approvals remain
byte-identical. No toolkit upgrade, supplier message, upload, payment or order.

Acceptance: fresh ERC/DRC/parity/unconnected0; independent pre-capture graph check;
11manufacturingGerbers,1SK,1Excellon,1drillmap,45x60outline,42PTH/24filled/18open;
common coordinates;33fullBOM/28SMTBOM-CPL/3THT/2wire pairs; assembly/dimensioned
drawings, paste/panel/DNP/process instructions, bring-upplan, source/artifactSHA256
and CRC checks. Verify currentT1body/pin/holes against visually inspected makerPDF
and PCN; actual sellerlot/firstfit remain explicitly unmeasured. Preserve physical,
process and genuineapprovalholds. Four actual independent read-only roles inspect
the same frozen final body before publication; no role impersonation.
''')
# Compact fabrication/assembly/dimension report with native layer drawings.
for side in ['top','bottom']:
 doc=fitz.open(D/'drawings'/f'assembly-{side}.svg');doc[0].get_pixmap(matrix=fitz.Matrix(5,5),alpha=False).save(str(D/'.work'/f'assembly-{side}.png'))
report=D/'drawings/Velluneo_C17_Fabrication_Assembly.pdf';c=canvas.Canvas(str(report),pagesize=(595.28,841.89))
def title(t,sub):
 c.setFillColor(HexColor('#123747'));c.setFont('Helvetica-Bold',20);c.drawString(40,793,t);c.setFont('Helvetica',10);c.drawString(40,772,sub)
def textblock(lines,y=738,size=10,leading=17):
 c.setFillColor(HexColor('#26343b'));c.setFont('Helvetica',size)
 for line in lines:c.drawString(40,y,line);y-=leading
def foot(n):
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#66727a'));c.drawString(40,28,'C17 / unchanged C16 CAD | PROTOTYPE DFM CANDIDATE | NOT RELEASED');c.drawRightString(555,28,str(n));c.showPage()
title('Velluneo C17','Fabrication and assembly handoff - 21 November 2026')
textblock(['Finished PCB: 45 x 60 mm, four copper layers, nominal 1.6 mm.', 'Source: C16, commit '+base[:16], 'Board SHA256: '+binding['source_board_sha256'][:40]+'...', '33 positions: 28 SMT parts, 3 THT parts, 2 wire-pad pairs.', 'Fresh native ERC / DRC / parity / unconnected: 0 / 0 / 0 / 0.', '42 plated holes: 24 filled/capped vias and 18 OPEN component holes.', 'One 45 x 60 mm outline. No slots, NPTH or mounting holes.', '', 'Layer order: F.Cu / In1.Cu / In2.Cu / B.Cu.', 'Requested stack: JLC04161H-7628; ENIG, green mask, white legend.', 'Outer copper 35 um; inner source foil 15.2 um nominal.', 'Actual laminate, CTI/RTI, pressed dielectrics and finished copper: confirm.', '', 'T1 finished holes: nine at 1.400 +/- 0.050 mm.', 'All 24 vias at 0.300 mm: epoxy-filled and copper-capped BOTH ends.', 'Keep 18 component holes open. SK is selection only, not copper.', 'All-layer no-added-copper band: X 0..45, Y 37.865..47.100 mm.', 'Requested registration <= 0.025 mm and rings >= 0.20 mm: confirm.', '', 'Coordinates: X = nativeX - 77.5; Y = 130 - nativeY, millimetres.', 'Both sides use the same top-view XY. Do not mirror manufacturing data.', 'Bottom human assembly drawing is mirrored for physical inspection.', '', 'Written process/assembly acceptance and genuine design approvals remain due.', 'Startup, faults, clamp, thermal and insulation require prototype tests.', 'No supplier contact, quote receipt, manufacturing, assembly or powered test.'],size=10)
foot(1)
for n,side in [(2,'top'),(3,'bottom')]:
 title('Assembly - '+side.upper(),'Native Fab / pad numbers / legend / outline; bottom is physically mirrored')
 c.drawImage(str(D/'.work'/f'assembly-{side}.png'),120,252,width=330,height=440,preserveAspectRatio=True,anchor='c')
 textblock(['Use exact MPN BOM and native pin numbers to check every polarity.', 'CPL origins/angles need body-centroid and feeder-zero confirmation.', 'T1/Q1/C1 are THT; J1/J2 are wiring operations, not connectors.', 'Do not infer machine-ready placement from a clean native drawing.', 'Finished outline remains 45 x 60 mm; assembler proposes handling panel.'],y=193)
 foot(n)
title('T1 - MYRRA 74032','Document-confirmed current version; actual stock lot / first fit not measured')
textblock(['Current maximum body: 26.5 x 22.5 x 26.5 mm (X x Y x height).', 'Rows: 15.24 +/- 0.3 mm. Pin pitch: 5.0 mm; maker pitch-chain +/- 0.3.', 'Square pins: 0.64 mm. Tail below seating: 4.0 +/- 0.5 mm.', 'Maker recommended drilling: 1.4 mm. C16 nominal holes: 1.4 mm.', 'Nine pins; pin 4 physically absent. Component-side drawing below.', 'Primary 3-5; auxiliary 2-1; secondary 6-10. Pins 7/8/9 unused.'],size=10)
x0,y0,scale=297,455,10
c.setStrokeColor(HexColor('#18465d'));c.setLineWidth(1);c.rect(x0-132.5,y0-112.5,265,225)
for pin,(x,y)in pinxy.items():
 c.circle(x0+x*scale,y0-y*scale,7,stroke=1,fill=0);c.setFont('Helvetica-Bold',11);c.drawCentredString(x0+x*scale,y0-y*scale+13,pin)
c.setFont('Helvetica',10);c.drawCentredString(x0,579,'26.5 mm maximum');c.drawString(441,455,'22.5 mm');c.drawString(170,318,'PRIMARY ROW / component-side view')
textblock(['Confirmed: C16 body outline, hole count, nominal pitch, row spacing and pin map.', 'Height reserved in C16: 26.5 mm above seating plane.', 'PCN dated 16 July 2015 increases old 21 mm height to 26.5 mm.', 'ENIKA lists old 27 x 27 x 21 mm construction: do not substitute unchecked.', 'Require exact current-part identity, photo / lot drawing and first-fit inspection.', 'Nominal maker footprint match does not guarantee insertion across tolerances.', 'Source PDFs with SHA256 are included in support/.'],y=266,size=10)
foot(4)
title('Assembly and acceptance','Prototype process conditions - return written answers before order')
textblock(['Q1: STFW2N105K5, straight TO-3PF leads. No lead forming.', 'Keep lowest wide shoulder at least 3 mm above PCB.', 'Body bottom approximately 6.5 mm; assembled reservation 29.7 mm.', 'Controlled spacer/fixture, support and first-fit inspection are required.', '', 'C1: front-mounted radial electrolytic. Correct polarity, strain-free insertion.', 'Keep at least 2 mm clear above the vent. Verify enclosure clearance.', '', 'T1: factory-wound MYRRA 74032, current mechanical version.', 'Do not force insertion, swap pins or accept old construction without review.', '', 'J1/J2: two wire-pad pairs; exact raw wire is listed in the full BOM.', 'Harness cut lengths, sleeves and strain relief are not released.', 'Exclude harness from base populated-board quote.', '', 'Panel: Standard PCBA minimum handling size 70 x 70 mm.', 'Ask for rails/fiducials/tab proposal preserving finished 45 x 60 mm outline.', 'No manufacturing panel or process-qualified stencil is released here.', '', 'Native paste apertures are included for assembler process review.', 'No DNP electronics. No automatic MPN / package / stack substitutions.', 'Review all polarities, centroids, feeder angles and package reflow limits.', '', 'Before power: identity, holes, soldering, clearances and insulation inspection.', 'Use the controlled bring-up plan in support/; no powered testing recorded.', 'First/repeated fault current <= 1.1 A peak; allocated extra-rise <= 400 ns.', 'Characterize VDS/clamp, restart, no-load and final-enclosure temperature.', 'Complete finished-product insulation review and tests with qualified personnel.'],size=10)
foot(5);c.save()
pdf=fitz.open(report)
for i,page in enumerate(pdf):page.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(str(D/'.work'/f'report-{i+1}.png'))
put(D/'checks/document-check.json',dict(pages=len(pdf),rendered_all_pages=True,manual_visual_review='Pending coordinator inspection of report1..5PNG and native assemblySVG',transformer_source_PDF_pages_visually_inspected=True))
print('CAM PASS; dimension check PASS; five-page drawing report rendered',flush=True)
