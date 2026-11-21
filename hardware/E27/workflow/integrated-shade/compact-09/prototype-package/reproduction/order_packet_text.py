from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'work/Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';W=R/'hardware/E27/workflow/integrated-shade/compact-09';P=W/'prototype-package';Q=ROOT/'work/compact09/order-closure'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
t=load(S/'T1-custom-contract.json');t['designed_mechanical_requirements']['PCB_pad_selection']='FinishedPTH1.20mm;1.80mmlands(squarepin1,roundpins4/8). Samepins1/4/8andcoordinates. Requirephysical3pingo-no-gogauge;donotforceanonmatchingcoil.';save(S/'T1-custom-contract.json',t)
(P/'README.md').write_text('''# SC09 — accepted-size bare laboratory PCB package

**Current scope: unpopulated laboratory PCB for manual prototype assembly and later measurements.** The owner explicitly accepts50×32mm. This closes the earlier25mm width deviation. It does not prove fit in a particular bulb cavity or qualified operation. The actual scoped fabrication disposition is in `bare-board-readiness.json`; full product Toolkit release remains a separate failing report.

## Download and ordering parameters

Use **SC09_do_zamowienia_PCB.zip** (or equivalent SC09_Gerbers_drills.zip): exactly7Gerber layers and2Excellon drill files. CRC/file hashes and coordinates are checked against native CAD. FR-4,2copperlayers,1oz,1.6mm, **lead-free HASL**, green mask, white legends, one board per closed50×32mm outline. No PCBA/stencil/panel or order payment is implied. Review the actual supplier preview before checkout; no supplier CAM acceptance has been obtained here.

27PTH/0NPTH, minimum drill0.30mm; T1 now has three1.20mm holes. Empty NPTH program is intentional. Milling path centreline is50×32mm;0.05mm outline stroke does not increase the intended routed size. Optional native .gbrjob has Finish=None and stroke-size metadata, so it is deliberately excluded from the upload ZIP. The explicit HASL order parameter controls the finish. The loose fabrication directory also retains drill maps/report and native auxiliary job for traceability.

`SC09_KiCad.zip` is the complete portable editable project with local symbols, footprints,17WRL model packages, experimental per-part STEP sources and registered fabrication artifacts. STEP interchange remains unqualified; no empty assembled STEP is delivered. `SC09_assembly.wrl` is the actual embedded visual model. Both native front/back renders are under `views/`.

## Supply specification

Read **SC09_specification.pdf/json**. Input230VAC50Hz, calculations207–253V. Proposed output52–68V LED load, nominal60V. Regulated total current estimate135.2mA includes dual68k discharge resistors; at60V externalLED estimate is133.4mA /8.01W. No accuracy/ripple guarantee is established. This is a constant-current supply, not a regulated60V voltage source.

All-inclusive base loss allocation0.9–1.7W gives input8.91–9.71W and82.5–89.9% efficiency to externalLED at the nominal60V operating point. These are planning scenarios, not measured extrema. At230V and ASSUMED truePF0.90, input is43.0–46.9mARMS. PF/current must be measured. Reference-board91.51% efficiency is not assigned to SC09.

Ambient design scope0–40°C. Explicitly unvalidated temperature scenarios at40°C: U1 junction58–110°C, T1 body59–108°C. The latter can exceed the90°C target: test hot behavior before treating the assembly as rated. C6 can≤75°C is a target,85°C a proposed lab stop; neither is a predicted measured result. Full assumptions and other targets are in the specification.

## Current physical design and checks

PCB50×32×1.6mm; approximate declared assembly envelope50×32×19.5mm. Eight legend strokes were corrected0.12→0.15mm with text height1.0mm. ThreeT1holes were enlarged0.85→1.20mm without changing pin centres, outer lands, nets or circuit. Coil-terminal position is explicitly RADIAL≤0.15mm; nominal fit arithmetic includes conservativePCBposition/hole tolerance. This closes a design fit-envelope problem, not actual supplier sample qualification.

19references,47physicalpads,11intendednets,1explicitNC. Fresh native ERC/DRC/parity, approvedA1graph, two-pass refill and independent all55pair screens are retained. The strict spacing screen fails intrinsic package-land distances; the separate bounded laboratory screen retains finite SO8/bridge/SMA concessions. No soldermask/SELV or normative insulation qualification is claimed. No check exclusion or global floor is relaxed.

Existing older reviews/final-review-inputs belong to commit082ffdb. Current order-stage reviews and exact inputs are separate; see current workflow index and `order-review-inputs.json`. Documents, calculations, scenarios and measurements are distinct.

## Assembly and physical testing remain controlled later steps

Solder bottomSMD first, inspect bridges/polarity, then install THT parts according to exact native schematic/BOM and custom contracts. T1 needs supplier/sample gauge and inductance/DCbias/thermal qualification. R7/RF1/C6 leadforming, insulation support, vent clearance and solder protrusion need actual part inspection. A1:1print gauge is provided in SC09_fit_gauge_1to1.pdf; print100% and verify its50mm ruler. A paper gauge is not a qualified supplied coil.

J1.1=L,J1.2=N; J2.1=LED_PLUS,J2.2=DC_RETURN, both bare-wire interfaces on B.Cu. Pins/coordinates are in SC09_pin_connections.csv, and sides/angles in SC09_positions_manual_reference.csv (native KiCad angles, Xfromleft/Ydownfromtop; not vendor-qualified PnP). No DNP population positions. External LED board, wire strain relief and guarded fixture are outside this PCB.

All internal/output nodes remain MAINS REFERENCED, notSELV. No dimming or hotplug. Isolate power and verify discharge before replacing/reconnecting the LED module. Integrated protection, MOV and bleeders do not provide a touch barrier or demonstrate safe single-fault behavior. BRINGUP.md identifies later qualified-test prerequisites; no powered results or actual order are claimed.
''',encoding='utf-8')
(P/'OPEN_ITEMS.md').write_text('''# Current stage dispositions

## Closed design/fabrication preparation issues

- SIZE: actual owner accepts50×32mmPCB. Earlier25mmwidth deviation is closed; actual bulb cavity fit is still not claimed.
- LEGEND: eight texts changed to0.15mmstroke/1mmheight to match the checked fabrication basis.
- T1HOLE: all three native/canonical/declared holes1.20mm, same1.8mmlands and pin centres. Radialcoilposition tolerance≤0.15mm explicitly stated; residual declared fit screen≈0.029mm. Actual sample gauging still required before assembly acceptance.
- UPLOAD:9file supplierZIP excludes optional mismatching .gbrjob metadata. Lead-freeHASL, material/layers/thickness/copper/outline are explicit.
- REGISTRATION: existing six manufacturing artifact classes are registered with exact source snapshot and hashes. Raw hardware.json is excluded from source_files to avoid a self-hash cycle; its complete design configuration is still automatically bound by the pinned Toolkit. No approvals are invented.

See final scoped bare-board-readiness.json for actual independent closure evidence. Supplier CAM preview/quote/order are not performed by this repository work.

## Later assembly, powered investigation and product obligations retained

1. Coil supplier/sample:180turnAWG32EE10, geometry/gauge, inductance, hotDCbias, DCR, insulation and core loss. NRND IC availability and complete parts basket remain procurement risks.
2. Actual formed R7/RF1/C6 and soldered lead fit, support, vent volume and wire strain relief. The drawing contract is not an inspected assembly.
3. LED current/ripple/line/temperature regulation and actual optical output; nominal133.4mALED is a calculation.
4. DynamicOVP/C6peak, discharge, shorted IC/sense/diode/bleeder faults, coil saturation and MOV/RF1 surge/fusing coordination. No physicalPASS.
5. Component temperatures/losses and life. T1 thermal sensitivity can exceed90°C target at40°Cambient; change design if measurements fail.
6. Guarded test fixture/operator/probe limits, qualified insulation/EMC/safety basis and finished lamp contact/enclosure/cavity obligations. Instructions do not replace access barriers.
7. Full Toolkit product release retains unresolved spatial/provider/exactstage/evidence gates. A separate bare-board fabrication audit does not relabel that report as PASS.

No purchase, supplier message or powered test was performed. These remaining obligations prevent assembled-product or powered-use acceptance; they are not falsely declared measured before a barePCB prototype exists.
''',encoding='utf-8')
bring=(P/'BRINGUP.md').read_text();bring=bring.replace('approximately135mA nominal operation','approximately135mA total /133mA externalLED nominal operation');bring+='\nCurrent specification clarifies inclusivebase-loss accounting and thermal sensitivity. At40°Cambient the unvalidatedT1 scenario spans59–108°C and may exceed90°Ctarget; do not assume thermal acceptance before measurement. The nominal externalLED current is133.4mAat60V afterbleeders, not an exact135.2mALED guarantee.\n';(P/'BRINGUP.md').write_text(bring,encoding='utf-8')
(P/'fabrication/README.md').write_text('Use ../SC09_do_zamowienia_PCB.zip:9files,7Gerber+2drill. ExplicitorderFR4/2layers/1oz/1.6mm/leadfreeHASL/greenmask/whitelegend;nominalroutecentreline50x32mm. NativeoptionaljobFinishNoneand50.05x32.05strokeextentsareauxiliary,excludedfromupload.27PTH/0NPTH;T1threeholes1.20mm. Read current scope/readiness and physical-test obligations.\n')
shutil.copy2(P/'SC09_do_zamowienia_PCB.zip',P/'SC09_Gerbers_drills.zip')
(S/'README.md').write_text('# SC09 accepted-size laboratory driver PCB\n\nPCB50×32mm explicitly accepted by owner; approximate declared assemblyheight19.5mm, not measured. Current total135.2mAestimate includesbleeders: externalLED≈133.4mA/8.01Wat60V. Input230VAC50Hz,screen207–253V. All nodes mainsreferenced.\n\nSee [current packet](../../../workflow/integrated-shade/compact-09/prototype-package/README.md), specificationPDF/JSON,9filebarePCBupload and scopedbare-board-readiness report. Nativelegend0.15mm and threeT1holes1.20mmclose fabricationdesignissues; noelectricalgraphchange. Actualcoil/forming/thermal/fault/EMCqualification remains required before assembly/energized/productacceptance. FullToolkit productreleaseFAIL is retained independently. No order or powered test was performed.\n',encoding='utf-8')
for src,dst in [('ERC.json','SC09_ERC.json'),('DRC.json','SC09_DRC.json')]:shutil.copy2(Q/src,P/'checks'/dst)
shutil.copy2(S/'.work/connectivity.json',P/'checks/toolkit-connectivity.json');shutil.copy2(S/'.work/connectivity-netlist.xml',P/'checks/toolkit-connectivity-netlist.xml')
for name in ['SC09_przod_3D.png','SC09_tyl_3D.png']:shutil.copy2(ROOT/'outputs/Velluneo_SC09_PCB'/name,P/'views'/name)
for name in ['order_native_fix.py','order_T1_fit.py','order_schematic_notes.py','order_documents.py','order_spec_pdf.py','order_packet_text.py']:shutil.copy2(ROOT/'work/compact09'/name,P/'reproduction'/name)
print('Currentpackettexts andsource referencesupdated;previousfullreviewsretainedashistorical')
