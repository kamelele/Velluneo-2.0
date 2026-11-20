from pathlib import Path
import csv,shutil,json
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/supplier-review-13';E=D/'design'
def write(n,s):(D/n).write_text(s,encoding='utf-8')
write('supplier/PCB-ENQUIRY-UNSENT.txt','''Subject: DFM and quotation only - Velluneo RFQ13, 45 x 60 mm, 4 layers

Dear Technical Sales / DFM team,

Please review Velluneo_RFQ13_BarePCB_DFM.zip, identified by its SHA-256 in
RFQ13-manifest.json, and quote five bare prototype boards. This is an enquiry;
please do not start manufacturing.

Requested construction: JLC04161H-7628, nominal 1.6 mm FR-4, Tg155 request,
35 um outer / 15.2 um inner copper, ENIG, green mask and white legends. Please
identify the actual laminate, CTI/RTI and guaranteed minimum pressed dielectrics.

The 17 designated through-vias require nonconductive epoxy filling and copper
capping, with ENIG on exposed caps: 0.700 mm lands / 0.300 mm Excellon entries.
Leave all 25 component insertion holes open. Please explain pre-drill versus
finished-hole definitions, finished annular-ring limits and cap planarity.

Component Excellon entries specify requested finished plated-hole targets.
For T1, the target is 1.350 mm and desired acceptance is 1.300-1.400 mm.
Please confirm component-hole tolerances, true position and hole/land registration;
if these limits are unavailable, return your guaranteed limits as a redline.

Please check all nine Gerber layers, 42 PTH / 0 NPTH holes, the common origin,
45 x 60 mm route centreline, via map and IPC-D-356 netlist. Add no copper, tooling
or identification marks in the protected isolation band. Return DFM findings,
process/material guarantees, production films for review, price and lead time.
No PCBA, stencil, substitutions or production/payment authorization is included.

Please answer PCB-01 through PCB-05 in supplier-response-checklist.csv. The
dimensioned review drawing provides interface details and outstanding questions.

Regards,
Velluneo project - technical enquiry draft, not yet sent
''')
write('supplier/TRANSFORMER-ASSEMBLY-ENQUIRY-UNSENT.txt','''Subject: Transformer construction and lead-forming feasibility - Velluneo RFQ13

Dear Transformer / Assembly Engineering team,

Please review the RFQ13 interface drawing and attached construction references.
We request a construction/first-article quotation and a toleranced finished
drawing/STEP, including all clips, tape, sleeves and termination features.

T1 requested complete envelope: maximum 30 x 30 x 18 mm above the mounting plane,
flush mounting, ten pins at 5.00 mm pitch and 22.50 mm row spacing. Windings:
P = 120 turns, pin 1 (dot) to 5; A = 22 turns, pin 2 (dot) to 4; S = 30 turns,
pin 6 (dot) to 10. Pins 3, 7, 8 and 9 remain unwound, without hidden junctions.
Lp = 2.304 mH +/-10% and effective P/S leakage <=20 uH are RFQ targets; please
state test methods, frequency, amplitude, temperature and fixture compensation.

Please return full pin-position/coplanarity limits and sections showing core,
steel yokes, primary exits, intact TIW secondary exits and controlled stripped/
soldered zones. Confirm actual insulation materials, their functions, EIS
applicability and qualified preparation/soldering/test procedures. Propose the
applicable test basis; wire-only temperature tests do not qualify the bobbin.
Return any infeasible interface as an explicit redline.

For STF2N80K5, evaluate proposed Q13-FORM-A only if incoming usable lead length
of at least 13.0 mm can be screened from the stated datum. ST does not guarantee
this minimum. The proposed worst developed length is 12.7458 mm, including the
requested PCB thickness range. Please return the forming drawing, jig capability,
selection yield, installed height <=23 mm and first-article insertion results.
Avoid unsupported root stress, forced insertion and rebending.

BR1 requires a controlled 5.5 mm pattern and polarity. R1 requires P25.4 forming
and 5.0-5.5 mm clearance below its body; do not substitute a formed MPN silently.
C1 requires strain-free P5 insertion and at least 2 mm free vent space beyond
its body. F1 and C4 are SMD parts and require no insertion-lead forming.

Please quote construction, first article and inspection separately, using
T1-01 through ASM-03 in supplier-response-checklist.csv. This is not authorization
to assemble, manufacture, energize or charge for an order.

Regards,
Velluneo project - technical enquiry draft, not yet sent
''')
write('fabrication/FABRICATION-NOTES.txt','''VELLUNEO RFQ13 - DFM / QUOTATION ONLY
No production, payment or energized-test authorization.

BOARD: one rectangular 45.000 x 60.000 mm rigid PCB; dimensions refer to the
Edge.Cuts route centreline. Four copper layers in order F.Cu / In1.Cu / In2.Cu /
B.Cu. Request JLC04161H-7628, nominal 1.6 mm FR-4 Tg155, 35 um outer / 15.2 um
inner copper, ENIG, green mask and white legends. Confirm actual material, CTI/RTI
and minimum pressed dielectric thicknesses. Requested thickness range: 1.44-1.76 mm.
No controlled-impedance target, panel, V-cut, edge plating or blind/buried vias.

VIAS: epoxy-fill and copper-cap BOTH ENDS of the 17 specified through-vias only.
Artwork land 0.700 mm; Excellon entry 0.300 mm. Finish exposed caps with ENIG.
Use designated-filled-vias.csv. Ordinary tenting or mask plugging is not a substitute.
Please state your pre-drill/finished-hole definition and guarantees for registration,
finished ring, copper/cap thickness and planarity. The 0.200 mm annulus is nominal
design geometry, not a guaranteed finished minimum.

INSERTION HOLES: keep all 25 component holes open; total 42 PTH, 0 NPTH, no slots
or mounting holes. Requested FINISHED plated-hole targets: T1 ten x 1.350 mm
(desired acceptance 1.300-1.400), Q1 three x 1.500, BR1 four x 1.200, R1 two x
1.100, C1 two x 1.000, and J1/J2 four x 1.600 mm. Confirm pre-drill compensation.
Proposed component-hole tolerance +/-0.050 mm and hole/land registration <=0.025 mm
require explicit agreement. Return guaranteed alternatives for review if unavailable.
F1 and C4 are SMD; do not treat them as insertion components.

FILES: common origin is native (77.5,130) mm; output X right, Y up. Gerber precision
is six decimal mm; Excellon is three decimal mm (rounding <=0.0005 mm per axis).
Nine Gerber layers, separate PTH/empty NPTH, drill maps and IPC-D-356 are supplied.
Bare-board continuity/short e-test is requested; it is not a powered functional test.

ISOLATION: do not add copper, tooling, thieving or identification marks inside
native Y=82.900..92.135 mm across the board width, on any layer. Actual projected
P/S copper gap is >=10.725 mm. The proposed 0.35 mm per-domain finishing budget
is an engineering condition requiring process confirmation, not certification.
Do not add slots, repair artwork or change dimensions without reviewed redlines.

Please return exact production films, DFM exceptions, process/material details,
price and lead time for five bare boards. No PCBA or stencil order is included.
Finished transformer/assembly/isolation acceptance remains separate.
''')
# Keep static BOM aligned with the actual current footprint identifier; electrical MPNs stay unchanged.
p=E/'BOM.csv'
with p.open(newline='',encoding='utf-8')as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
 if row['Reference']=='T1':row['Footprint']='Velluneo_ECO04:TDK_EFD25_FINISHED30x30_RESERVATION';row['Footprint_status']='RFQ13 finished-body reservation; exact builder drawing/first article pending'
with p.open('w',newline='',encoding='utf-8')as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
shutil.copyfile(p,D/'assembly-reference/BOM.csv')
questions=[('PCB-01','PCB fabricator','Exact stack, laminate, CTI/RTI and minimum pressed dielectrics','Return actual guaranteed material/construction'),('PCB-02','PCB fabricator','17 filled/capped vias and 25 open component holes','Confirm coordinate map and selective treatment'),('PCB-03','PCB fabricator','Finished hole size, true position and registration','T1 target1.35; desired1.30-1.40; state compensation'),('PCB-04','PCB fabricator','Finished ring, cap, mask and legend tolerances / films','Return exact-file DFM redlines and production films'),('PCB-05','PCB fabricator','Quote five bare boards, e-test, cost and lead time','Quotation only; no production or payment'),('T1-01','Transformer builder','Finished 30x30x18 outline/STEP and full pin pattern','Toleranced drawing plus first-article fit'),('T1-02','Transformer builder','Core/yoke/secondary-exit insulation construction','Sections, material functions, procedures and test basis'),('T1-03','Transformer builder','Turns, polarity, Lp, leakage and DCR methods','State actual guarantees and measurement conditions'),('ASM-01','Forming provider','Q13-FORM-A incoming screen, jig, height and fit','Drawing, usable-lead yield and first-article records'),('ASM-02','Forming provider','BR1/R1 forming, polarity, standoffs, tails and fillets','No silent MPN substitution or forced insertion'),('ASM-03','Assembly provider','C1 vent/fit and F1/C4 SMD process','Vent >=2mm; polarity, reflow and height review'),('REL-01','Qualified reviewer / buyer','Accept exact redlines, films, first article and test basis','Separate actual authorization before production/use')]
with(D/'supplier/supplier-response-checklist.csv').open('w',newline='',encoding='utf-8')as f:w=csv.writer(f);w.writerow(['Question_ID','Owner','Required_response','Acceptance_evidence','Supplier_response','Evidence_reference','Review_status']);w.writerows([list(x)+['','','PENDING']for x in questions])
print('Polished supplier-facing drafts/notes; BOM T1 footprint now matches currentCAD.')
