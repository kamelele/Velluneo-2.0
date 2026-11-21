from pathlib import Path
import json,hashlib,csv,shutil,zipfile,html
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'work/Velluneo-2.0'; S=R/'hardware/E27/variants/integrated-shade/SC09_compact'; W=R/'hardware/E27/workflow/integrated-shade/compact-09';P=W/'prototype-package';O=ROOT/'outputs/Velluneo_SC09_PCB'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def zip_paths(dest,items,base):
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(items):z.write(p,p.relative_to(base).as_posix())
# An empty-shape native STEP import is never delivered as an assembled model.
step=P/'SC09_assembly.step'
if step.exists():shutil.move(str(step),str(ROOT/'work/compact09/native-step-empty-import.NOT_FOR_DELIVERY.step'))
save(P/'checks/3D-export-status.json',{'native_VRML':'SC09_assembly.wrl; embedded real component meshes, mm, board top-left100,100origin','native_renders':['views/SC09_przod_3D.png','views/SC09_tyl_3D.png'],'STEP':'Not delivered: KiCad10.0.6 imported component labels but discarded faceted source mesh geometry. Empty component shapes were detected in the exported STEP. Source per-part STEP meshes are experimental, not validated interoperable mechanical models. Use native KiCad/WRL for the complete visual model.','no_replacement_with_AI_image':True,'package_models':17,'wire_interfaces_without_models':['J1','J2']})
for name in ['SC09_ERC.json','SC09_DRC.json']:shutil.copy2(O/name,P/'checks'/name)
for name in ['connectivity.json','requirements.json','check.json','connectivity-netlist.xml']:
 shutil.copy2(S/'.work'/name,P/'checks'/('toolkit-release.json' if name=='check.json' else 'toolkit-'+name))
shutil.copy2(ROOT/'work/compact09/checker/test-results.json',P/'checks/checker-controls.json')
shutil.copy2(S/'bom-build.csv',P/'SC09_BOM.csv')
shutil.copy2(S/'bom-build.json',P/'SC09_BOM.json')
for name in ['final_native_audit.py','prepare_handoff.py','assemble_handoff.py']:
 (P/'reproduction').mkdir(exist_ok=True);shutil.copy2(ROOT/'work/compact09'/name,P/'reproduction'/name)
boardhash=sha(S/'SC09_compact.kicad_pcb');schhash=sha(S/'SC09_compact.kicad_sch')
readme='''# SC09 routed laboratory prototype — manufacturing review packet

**Candidate files are complete for review, not a passed Toolkit release or a qualified lamp.**
Board: **50 x 32 x 1.6 mm**, two copper layers, 1 oz, lead-free HASL, green mask, white legends, manual assembly. Combined component envelope: **approximately 50 x 32 x 19.5 mm**, based on declared maxima, not a measured assembly. The earlier proposed 50 x 25 x 20 mm envelope is **not met**; width is 7 mm greater. No ordinary-bulb cavity fit is demonstrated. No enclosure is designed here.

Input: 230 VAC / 50 Hz, calculations screened at 207–253 VAC. Output: nominal 135.203 mA at 60 V, 8.112 W; proposed LED range 52–68 V, 20 series Lumileds L128-4080CA3500001, 4000 K / CRI >=80. Approximately 800 lm is a lamp target, not measured output. All output terminals and internal copper are mains-referenced; this is not SELV. No dimming or powered LED replacement.

## Files

- `SC09_Gerbers_drills.zip`: bare-board artwork and Excellon drills. Exported with one shared absolute coordinate system; no mirroring or separate offsets.
- `fabrication/`: individual F/B copper, mask, silkscreen, Edge.Cuts, X2 job, plated/nonplated drill files, maps and report. Empty NPTH file is expected (zero NPTH). 27 plated holes, including 10 vias; minimum drill 0.30 mm. No slots or mounting holes. Single board; no panel tooling.
- `SC09_KiCad.zip`: portable native schematic, PCB, project, local symbols/footprints and the 17 actual WRL package models.
- `SC09_schematic.pdf`, `SC09_layers.pdf`: native schematic and copper/silkscreen layers.
- `SC09_assembly_front.pdf`, `SC09_assembly_back.pdf`: native assembly views; back view mirrored for underside assembly. Add pin-position CSV when identifying lands.
- `SC09_BOM.csv/json`: 19 references, 17 electrical parts plus 2 bare-wire interfaces. No populated DNP positions. LED board and external wiring/fixture are not this PCB's BOM.
- `SC09_pin_connections.csv`: actual 47 native pin locations/net membership. Expected intent is independently retained in the KiCad source package, not inferred from this CSV.
- `SC09_positions_manual_reference.csv`: all 19 origins/sides/angles for manual reference. Coordinates are X from left, Y down from top in mm, angles are native KiCad footprint angles. This is NOT a vendor-qualified PCBA pick-and-place file.
- `SC09_assembly.wrl`: complete embedded native 3D visual model, millimetres; generic package appearances. No empty STEP assembly is presented as a full model. See `checks/3D-export-status.json`.
- `views/`: actual native front/back 3D renders; no AI-generated substitute.
- `checks/`: fresh ERC, DRC/parity, independent approved-intent comparison, all-55-pair strict and bounded laboratory spacing screens, two-pass refill equality and native inventory. Complete Toolkit release result is retained even though it fails.
- `validation/`: read-only native saved-copper validator, matrix and bounded package-land assessment. Run with matching KiCad10.0.6 pcbnew. Test controls are retained; no global spacing waiver is introduced.

## Ordering and assembly status

The artwork is an engineering candidate. Do not describe this packet as a passed production release: `checks/toolkit-release.json` is **FAIL**. Remaining product/physical qualification and formal spatial/approval/provider gates are listed there and in `OPEN_ITEMS.md`. Existing owner instructions authorize autonomous design/export/publication, not fabricated individual stage acceptance, purchase or energized tests. No order or supplier message was sent.

For a later authorized bare-board quotation: JLCPCB FR-4, 2 layers, 1.6 mm, 1 oz outer copper, lead-free HASL; one board per outline; do not substitute aluminium PCB, add panel tabs or scale artwork. Confirm layer assignment, 50 x 32 mm outline and PTH/NPTH separation in the supplier preview. No controlled impedance or blind/buried vias. Not an Economic/Standard PCBA upload: prototype assembly is manual. No stencil is required for the hand-solder plan; paste/stencil files are intentionally excluded. A production PCBA change needs a separate process review and quotation.

Assembly: solder bottom SMD parts first, inspect polarity/bridges; install formed R7 and RF1 and other THT parts using their contracts. Verify T1 with a three-pin gauge before installation. Fit C6 horizontally on an appropriate insulating support, keep its 5 mm vent-direction reserve, and avoid damaging its sleeve. Sleeve insulation is not a safety barrier. Trim leads below the board so they cannot contact bottom parts or copper; keep within the declared underside envelope. Check clearances after trimming and soldering. Support insulated wires independently: J1/J2 have bare solder lands, no selected connector or strain relief.

J1 pin1 = L, pin2 = N. J2 pin1 = LED_PLUS, pin2 = DC_RETURN. Exact land locations are in the pin CSV (both interfaces are on B.Cu). C6 pin1 positive; BR1 pin1 positive/pin3 negative; D1 pin1 cathode/pin2 anode; T1 pin1 LED_PLUS, pin8 FB_INDUCTOR, pin4 deliberately unwound/floating. Remove bobbin pins2/3/5/6/7 as contracted. U1 dot/pin1 = BP. Confirm all against native schematic and manufacturer data before soldering.

T1 is the custom 180-turn AWG32, 1 mH EE10 design, NOT an immediately orderable catalogue inductor. Supplier feasibility, winding insulation, DC bias, core loss and finished dimensions require verification. LYT1603D-TL is NRND; no lifecycle/supply guarantee or complete priced basket is claimed. Exact RF1/R7/C6 forming remains an unqualified assembly proposal. A render does not validate supplier fit.

## Electrical and thermal scope

Nominal current is calculated from R5 || R6. Static OVP screening is approximately 69.37–86.51 V with 25 C IC threshold limits; dynamic C6 target <=90 V is unmeasured. C6 is 150 uF / 100 V (screen maximum 180 uF); maximum stored-energy screen 0.729 J at90V. Each 68k bleeder is screened at approximately0.123 W at90V; one open bleeder gives a calculated90-to5V time of36.45s. Verify discharge; do not rely on elapsed time alone.

Planning loss allocation is0.9–1.7 W, **not a guaranteed interval**. Source-connected thermal copper is241.90 mm2 across both layers; D1 DC_RETURN copper is80.99 mm2. Copper area does not establish component temperatures. At0–40 C ambient characterize C6 can (target<=75 C, stop85 C), T1 (target<=90 C), SOURCE pin (target<=100 C), D1 case (target<=100 C), R7 local ambient/body and bleeders. Manufacturer junction/derating limits and the test operator's lower stop limits control. No published reference-board efficiency, surge or EMI result is inherited.

The high-frequency loop is kept around C4/U1/D1/T1 and R5/R6, with a separate sense branch to U1 FB. The long BUS_FILTERED feed is upstream of local C4 and is not the commutation return. SOURCE thermal pours have native pour-only high-voltage guards, not DRC exclusions. The strict all-pair screen fails intrinsic manufacturer package-land gaps; the separate scoped screen passes only explicitly bounded SO8/bridge/SMA land/escape concessions. These are engineering prototype assessments, not normative insulation waivers.

See `BRINGUP.md` before planning any powered investigation. No physical test is recorded as performed.
'''
(P/'README.md').write_text(readme,encoding='utf-8')
(S/'README.md').write_text('# SC09 compact nonisolated LED driver\n\nCurrent native CAD: fully routed laboratory candidate, 50 x 32 mm, approximately19.5 mm total component envelope. Nominal230VAC /135.2mA at60V. All terminals are mains referenced.\n\nThe complete current packet is [prototype-package](../../../workflow/integrated-shade/compact-09/prototype-package/README.md). It includes native CAD, manufacturing candidate exports, front/back3D renders, connectivity and physical spacing evidence, assembly details and open qualification items. The earlier25mm width target is not met. No passed Toolkit release, bulb-cavity fit, physical qualification or order is claimed.\n\nApproved A1 intent is preserved independently; owner autonomy authorizes completion without repeated routine questions. Historical pre-CAD and SC08 packets are not final CAD verification. See owner decisions and current package reports.\n',encoding='utf-8')
(P/'OPEN_ITEMS.md').write_text('''# Open items and disposition

These prevent a claim of a passed complete-product/assembled-unit release. They are not disguised as measured results.

1. SIZE — 50 x32 actual PCB exceeds proposed25mm width. Owner owns cavity/size acceptance; root owns any future redesign. No bulb-fit claim.
2. T1 — custom180T/AWG32 sample, pin gauge, inductance/DC bias/hot loss, insulation and dimensions. Coil supplier/qualified electrical designer; before assembled-unit release.
3. FORMED_PARTS — physical RF1/R7/C6 lead forming, solder protrusion, support and actual vent volume. Assembly operator/qualified mechanical review; before assembly acceptance. Illustrative models are insufficient.
4. CURRENT/OVP — line/LED/hot corners, min-on-time margin, LED ripple/current, start/restart, open load and dynamic C6 voltage. Qualified electrical investigator; physical measurements required.
5. FAULT/SURGE — MOV/RF1 coordination, shorted IC, failed sense/bleeders/diode, coil saturation at1.24A maximum IC fault limit, input transient and high-temperature protection. Qualified laboratory; no claim of safe single-fault operation.
6. THERMAL — actual temperatures, ripple/ESR, hot DCR, loss total and lifetime. Qualified laboratory; native copper area does not close this.
7. INSULATION/EMC — qualified numerical safety basis, component package clearances, actual soldered spacing, external guard fixture, LED/contact accessibility, emission/immunity. Product obligations remain retained. Instructions cannot replace touch protection.
8. FORMAL_WORKFLOW — Toolkit spatial contract/approval not adopted; full product requirements/evidence and release/provider approval gates not passed. Actual autonomy authorization is retained separately; no hash-bound stage decision invented.
9. SUPPLY/COST — NRND IC, custom coil and catalogue inductor availability, complete basket and quote not verified. Procurement owner. Manual prototype process does not imply Economic/Standard PCBA capability.
10. OPTICAL — stabilized800lm, LED junction temperature/bin/diffuser acceptance and complete LED-board endpoint characterization remain unmeasured. LED module is outside this driver PCB.

Files are published for review and prototype planning on the feature branch. There is no automatic purchase or powered test authorization.
''',encoding='utf-8')
(P/'BRINGUP.md').write_text('''# Laboratory bring-up plan — no tests performed

This document is a plan, not authorization or measurement evidence. Before power, a qualified230V investigator must name the actual hardware/LED/fixture/wiring revisions, responsible person, equipment ratings, measurement bandwidth, current limit, protection and stop criteria. Use guarded mains-rated equipment and differential measurement; never attach an ordinary grounded oscilloscope lead to floating mains-referenced nodes. An isolation transformer alone does not make internal parts safe.

Unpowered: compare all19 references/47pads against the independent A1 intent and pin CSV. Inspect polarity, solder bridges, actual clearances, formed leads, bottom protrusion, vent reserve and wire support. Gauge T1; measure its100kHz1Vpp zero-bias inductance0.95–1.05mH/25C, DCR<=2.7ohm25C and required hot bias behavior by a separately defined safe setup. No powered testing with an unverified coil. Check bleeders, J1/J2 identification and absence of unexpected shorts. Identify minimum actual soldered clearances at package concessions.

Qualified test setup: fully contained access barrier, remote isolation/emergency stop, appropriately fused/current-limited supply and correctly rated differential probes, current measurement and power analyzer. Record starting discharged C6 voltage. Use the chosen verified LED string or a suitable rated load. Both output leads remain mains referenced. Disconnect and verify discharge before changing any load; do not hot-plug LED.

Initial nominal230V run: capture input RMS current/power/PF, LED average/ripple current, output voltage and peak drain/source waveforms with bandwidth stated. Verify proposed normal52–68V load window and approximately135mA nominal operation; no guaranteed current tolerance has yet been established. Repeat at207/253VAC and ambient0/40C after stable operation, using a qualified corner-test protocol. Record Pin-Pout rather than assigning reference-board efficiency.

Open-load/restart: only with separately reviewed guarded test procedure, capture peak C6 and OVP timing; proposed peak stop90V on100V-rated C6. Initial target is not proof of safe transient control. Record discharge90-to5V with both bleeders and one open, using safe deenergized switching arrangements; computed one-open36.45s is a model only. Do not perform LED reconnection while C6 is charged.

Thermal: measure stabilized C6can, T1, L1, RF1, R7, R8/R9, U1SOURCE and D1case in actual chosen fixture/orientations at ambient0–40C. Planning targets C6<=75C (stop85C), T1<=90C, SOURCE/D1case<=100C; junction estimates use applicable manufacturer models, not generic ambient thermal resistance. Stop earlier if any rated derating/stress limit, abnormal current, unstable regulation, smell, discoloration or arcing is reached. Reassess allocation0.9–1.7W from measured losses; not a qualified upper bound.

Abnormal/surge/EMC tests require their own qualified procedures and protected fixtures. Do not short components or apply surge simply on the authority of this plan. Record actual limits, test source impedance/waveform, protective coordination and sample outcomes. No numeric surge/EMI/single-fault PASS is claimed here. Defects require linked revisions and rechecks.
''',encoding='utf-8')
(P/'fabrication/README.md').write_text('Bare-board engineering candidate only. Read ../README.md and ../OPEN_ITEMS.md before any upload/order. Two layers FR4,1.6mm,1oz,lead-freeHASL,green mask,white legends. Native absolute shared origin, mm. Outline50x32mm with small corner chamfers. 27PTH/0NPTH; keep both drill files and ignore empty NPTH as expected. No paste/stencil/panel or assembly service included. Do not rotate/scale/mirror individual layers.\n',encoding='utf-8')
zip_paths(P/'SC09_Gerbers_drills.zip',[p for p in (P/'fabrication').iterdir() if p.is_file()],P/'fabrication')
sourcefiles=[p for p in S.rglob('*') if p.is_file() and not any(x in p.relative_to(S).parts for x in ['.work','__pycache__']) and p.suffix not in ['.kicad_prl','.step']]
zip_paths(P/'SC09_KiCad.zip',sourcefiles,S)
save(P/'artifact-source-binding.json',{'board_sha256':boardhash,'schematic_sha256':schhash,'kicad':'10.0.6','status':'Manufacturing candidate and laboratory review packet, full Toolkit release FAIL','CAD_export_method':'Native kicad-cli10.0.6; gerbers/drills share absolute origin. No CAD source changes between checks, renders and fabrication export.','exports':[{'path':p.relative_to(P).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(P.rglob('*')) if p.is_file() and p.name!='artifact-source-binding.json' and 'reproduction' not in p.parts]})
index=R/'hardware/E27/workflow/project-index.md';txt=index.read_text(encoding='utf-8');marker='# E27 workflow index';history=txt[txt.index(marker):];prefix='# Current task — SC09 routed laboratory prototype (2026-11-21)\n\nCurrent [complete review/manufacturing-candidate packet](integrated-shade/compact-09/prototype-package/README.md), [open items](integrated-shade/compact-09/prototype-package/OPEN_ITEMS.md). Board50x32mm, approximate assembled envelope50x32x19.5mm; earlier25mmwidth target not met. Native schematic/PCB, routing,17models and front/back3D now exist. ERC/DRC/parity0; approvedA1connectivity matched. Full Toolkit release NOT passed; no purchase or energized tests performed.\n\nBranch concept/integrated-shade-nonisolated-buck; main outside write scope. Root sole CAD writer; four fresh independent role reports accompany final packet. Historical pre-CAD and SC08 entries below do not represent current acceptance.\n\nPinned toolkit manifest05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822, package0.7.1-preview.3/ruleset0.7.1, KiCad10.0.6. Doctor passed.\n\n';index.write_text(prefix+history,encoding='utf-8')
save(W/'design-state.json',{'revision':'SC09-routed-50x32','state':'complete_candidate_packet_not_released','board_sha256':boardhash,'schematic_sha256':schhash,'native_ERC_DRC_parity':'0 errors/0 unconnected/0 parity issues','formal_release':'FAIL; see prototype-package/checks/toolkit-release.json','size_mm':[50,32,19.5],'proposed_25mm_width_met':False,'branch':'concept/integrated-shade-nonisolated-buck','main_write_authorized':False,'physical_measurements_performed':False,'order_placed':False,'actual_authority':'owner-autonomous-completion.json; no individual stage approvals fabricated'})
print('Assembled packet',P)
