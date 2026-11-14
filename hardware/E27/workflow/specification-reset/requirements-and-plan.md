# Velluneo E27 — product reset and specification review

Packet: VEL-SPEC-RESET-01, revision 2, 2026-11-14.
Status: interview-derived draft; not an approved specification-stage packet.
Repository baseline: 377fc0a08e74043e255b732f7c2beb63134a3576.
Scope: requirements and planning only. No CAD, libraries, manufacturing exports or historical approvals are changed.

## 1. Purpose and decision basis

Velluneo is a repairable domestic E27 LED lamp. A user replaces an exhausted LED panel instead of discarding the intact base, power supply and housing. Separately sold panels also allow changing white-light colour without replacing the base.

Basis: the owner's Polish-language interview in the current conversation on 2026-11-14. The owner confirmed offline tool-free replacement, one base for three colours, about 800 lm, a laboratory prototype by September 2027, and freedom to redesign all existing electronics. This record paraphrases those decisions; it is not a new human approval of this packet. No permanent conversation URL is available; preserve the actual review decision when the owner reviews a frozen packet.

Owner: Kamil Stępak. Coordinator/document writer: the current assistant context. Technical design reviewers and laboratory supervisors have not yet been named. Repository documentation is English; discussion with the owner is Polish.

The old 8S/D5 architecture is historical input. Eight LEDs, two contacts, 70 × 34 mm, active load identification, timed probes, a microcontroller and the old current/voltage settings are not constraints for the redesign. No new electrical architecture is selected in this packet.

## 2. Requirements confirmed in the interview

All requirement rows are revision 1; packet revision 2 aligns unknown gates without changing owner decisions. Product decisions belong to the owner; engineering acceptance plans belong to the coordinator and assigned technical reviewer. All physical verification is pending. 'Schematic', 'placement' and 'release' identify the gate by which implementation intent or evidence is needed, not permission to proceed now.

| ID | Requirement | Acceptance approach and due gate |
|---|---|---|
| R-PURPOSE | Retain the base when the LED panel fails; replace the complete panel. | Demonstrate panel replacement and restored operation on the integrated prototype; release/integration. |
| R-SUPPLY | E27, nominal Polish 230 V AC / 50 Hz supply; 120 V operation unnecessary. | Establish actual line-voltage design/test envelope before schematic; verify startup, running and faults at its corners before release. |
| R-LIGHT | About 800 lm emitted by the complete lamp with its diffuser fitted. | Agree numerical tolerance and stabilized measurement conditions at specification; measure before final demonstration. |
| R-CCT | Panels in nominal 2700 K, 4000 K and 6500 K; similar brightness. | Agree CCT tolerances and maximum brightness difference at specification; measure all three variants. |
| R-COMPAT | One base accepts all three panels without settings, switches or user configuration. | Freeze a compatible electrical/mechanical interface before schematic/placement; demonstrate each variant on the same base. |
| R-REPLACE | Tool-free intuitive replacement; prevent incorrect installation. | Freeze mechanical keying/retention and contact sequence before placement; assess wrong orientation, partial insertion and repeat replacement. |
| R-OFFLINE | Replacement only after unscrewing from the socket and waiting for cooling/discharge. | Determine safe-access conditions and delay by analysis and measurement; instructions alone are not evidence of safety. Limits before schematic, geometry before placement, measured confirmation before release. |
| R-ENV | Dry domestic interiors; open or ventilated fixtures. Closed fixtures, damp locations and outdoor use are outside prototype scope. | Define rated ambient, ventilation assumptions and operating orientations before schematic/placement; test thermal worst cases before release. |
| R-DIFFUSER | Removable milky diffuser hides individual LEDs and provides broad illumination including the sides. | Agree distribution and appearance criteria at specification; check fit before placement and optical performance on the complete lamp. |
| R-FAULT | An open/failed panel, missing panel and shorted panel must not damage the base. | Define representative faults and duration before schematic; validate protection and temperatures before release. After offline panel replacement, power cycling restores normal operation without reset or fuse replacement. |
| R-EMPTY | The energized base can remain without a panel without damage or overheating. | Define duration and accessible-part limits before schematic; verify no-load behavior and recovery with the approved test fixture. This does not authorize live replacement. |
| R-THERMAL | Protect against overheating using a justified simple implementation. | Select limiting or shutdown/recovery after comparison. Agree thresholds, hysteresis and protection-fault behavior (including sensor faults if a sensor is selected) before schematic; test before release. |
| R-USE | Design for 8–12 hours/day, including long continuous sessions. | Establish continuous-duty thermal test conditions before schematic; a timetable is not a required forced shutdown. |
| R-BASE-LIFE | Five-year base life is an acceptable design target; ten years is aspirational. | Assess parts at measured electrical/thermal stress. At 8–12 h/day: 14,600–21,900 h in five years; 29,200–43,800 h in ten. Calendar aging also matters. Agree failure/end-of-life definition before schematic. Do not claim years of demonstrated service from short tests. |
| R-PANEL-LIFE | Panel life should be comparable to ordinary retail LED lamps. | This is not yet a measurable acceptance limit. Agree hours, lumen maintenance and failure criteria at specification, then establish a feasible validation approach. |
| R-FEATURES | Basic full-output on/off lighting; no Wi-Fi, app or added smart functions. | Confirm feature scope at specification; check normal behavior before release. Wall-dimmer compatibility is excluded from the primary design. |
| R-SIZE | Compare a conventional-bulb-sized concept with a moderately larger concept that improves cooling and replacement. | Present actual envelopes and tradeoffs for owner selection before placement; no existing board size is binding. |
| R-COST | Prefer rational cost and future manufacturability; no fixed prototype budget. | Compare BOM, sourcing, assembly and tooling costs during architecture and release reviews. No invented cost ceiling. |
| R-BUILD | Prefer JLCPCB fabrication and populated PCB delivery; laboratory assembly is a fallback. | Confirm actual service, component availability and any transformer/THT/manual work before process acceptance and release. Housing and lamp assembly are separate. |
| R-DEMO | Deliver one complete, laboratory-tested prototype for presentations by September 2027; iterations allowed. | Agree final review date and test scope; retain matched hardware revisions and actual reports. Commercial certification and sales release are not automatically included. |

The owner reports access to university laboratories for flux, colour, CRI, safety and interference measurements, with experienced support, and holds SEP qualifications. Instruments, calibrated methods, responsible people and availability remain unverified planning inputs. This packet records no physical tests.

## 3. Proposals awaiting owner review

| ID | Proposal | Meaning |
|---|---|---|
| P-OPTICS | 750–850 lm per variant; brightest/dimmest ratio no greater than 1.10 under the same stabilized conditions. | Gives 'about 800 lm' and 'similar brightness' separate measurable limits. Both must hold; final conditions and sample plan remain open. |
| P-CRI | CRI Ra ≥80 for all variants. | Proposed ordinary domestic colour-rendering target, not a measured result. |
| P-SUPPLY | Evaluate 207–253 V AC / 50 Hz as the initial normal-operation screening range. | Requires competent review of the applicable supply/product requirements; not a complete surge or fault envelope. |
| P-ISOLATION | Compare an isolated driver first because the LED panel is user-accessible. | A starting architecture preference only. Determine actual protection class, insulation system, barriers, contact voltage/energy and safe-access limits before schematic. Do not equate low voltage or an isolation label with proven safety. |
| P-SIMPLICITY | Remove the requirement for live-insertion recognition and retry probes. | Consider omitting their implementation only after showing the simpler driver meets open/short/no-load and residual-energy requirements. |

One hundred mechanical replacement cycles is an owner-accepted stretch goal, not a prototype pass/fail requirement. Minimum cycle life remains open. A replacement diffuser is a future product direction; the present requirement is repeat removal and refitting. Optional dimmable-driver work must have a separate scope and must not block the basic prototype.

## 4. Subsystems, interfaces and four profile layers

Subsystems: BASE (driver/protection), PANEL (LEDs and justified inexpensive auxiliary parts), BODY (E27 base, housing, heat path, retention and diffuser). Optional firmware is not selected. The coordinator owns interface preparation; independent technical review is unassigned.

Before schematic, define BASE–PANEL voltage/current windows, polarity, source/sink behavior, startup, no-load, short and recovery, connector/contact count and residual energy on both sides. There is no agreed pin map yet. Before placement, define BODY–BASE–PANEL outline, heights, tolerances, insulation boundaries, keying, retention, thermal contact and service access. Final enclosure manufacture may come later; its interface constraints cannot wait until after PCB manufacture.

| Profile | Current state | Required next evidence |
|---|---|---|
| Common | Toolkit reference 0.7.1-preview.3, ruleset 0.7.1; installed project launcher/lock absent. Historical CAD used KiCad 10.0.8; toolkit baseline is 10.0.6. | Trusted installable archive/digest, deliberate version decision, installed lock and passing doctor before CAD. |
| Product | Repairable E27 lamp, offline replacement, dry interiors and open/ventilated fixtures. | Resolve specification unknowns and obtain a genuine decision on the complete packet. |
| Fabrication | JLCPCB preferred. No layer count, laminate, copper, finish or board thickness selected for the redesign. | Compare actual services and document proposed process for owner review; obtain order-specific evidence at relevant gates. |
| Assembly | Supplier assembly preferred; university assembly fallback. | Confirm service scope, BOM/MPNs, sourcing, manual/THT/transformer exceptions, inspection and test access. |

## 5. Open-question register

| ID | Question / closure evidence | Owner | First blocked gate |
|---|---|---|---|
| U01 | Accept or revise P-OPTICS, P-CRI and P-SUPPLY; record owner decision and technical basis where applicable. | Owner + technical reviewer | Specification |
| U02 | Define panel service-life hours, lumen maintenance, failure criterion and minimum replacement cycles. | Owner + coordinator | Specification |
| U03 | Name competent electrical reviewer and responsible laboratory person; establish a feasible proposed fabrication/assembly route, explicitly listing unconfirmed supplier constraints. Detailed order evidence remains due at U11/U13. | Owner + coordinator | Specification |
| U04 | Select exact laboratory-demo scope versus external qualification; identify applicable product/safety/EMC/flicker requirements without assuming old limits. | Technical reviewer + owner | Specification |
| U05 | Select driver architecture and LED candidates using power, tolerance, thermal and cost calculations; no fixed LED count or current. | Coordinator + independent reviewer | Schematic |
| U06 | Implement the product-level safety/operating criteria from U16: determine numerical circuit limits, discharge/cooling implementation, short duration/recovery, hot/cold startup and disturbance response. | Electrical reviewer + laboratory lead | Schematic |
| U07 | Develop thermal/life calculations and detailed optical measurement procedures using the specification decisions from U14/U15; define base lifetime/end-of-life basis. | Coordinator + laboratory lead | Schematic |
| U08 | Select overtemperature behavior, thresholds and sensor-fault response; define absence/reversal/partial-contact abuse cases even though live replacement is forbidden. | Electrical/mechanical reviewers | Schematic |
| U09 | Freeze panel/base pin map and independently reviewed intended connectivity with exact datasheet/pin/footprint basis. | Coordinator + independent reviewer + owner decision | Schematic |
| U10 | Freeze preliminary enclosure envelope, heat path/contact, insulation materials, dimensions, heights, keying and retention. | Mechanical owner (to assign) + coordinator | Placement |
| U11 | Confirm actual stackup, copper, materials and service limits as needed for insulation/layout/assembly. | Coordinator + supplier | Placement |
| U12 | Confirm available calibrated instruments, personnel, samples, test limits and stop conditions. Release evidence must cover actual operating/fault conditions. | Laboratory lead + owner | Release / each affected physical test |
| U13 | Establish BOM availability, exact costs, release outputs, matched revisions and test/programming/assembly instructions. | Coordinator + supplier + owner | Release |
| U14 | Agree nominal CCT tolerances, stabilized optical acceptance conditions and sample plan; approve a distribution/appearance criterion and assessment method, including side illumination and hidden LED points. | Owner + coordinator + laboratory lead | Specification |
| U15 | Establish rated ambient range, operating orientations and explicit open/ventilated-fixture assumptions for thermal feasibility. | Owner + coordinator + technical reviewer | Specification |
| U16 | Define product-level safe-access behavior, normal/fault operating boundaries, applicable fault cases and recovery expectations; competent reviewer establishes the acceptance basis for residual energy, accessible surfaces and cooling. Numerical circuit implementation follows at U06. | Electrical reviewer + owner + laboratory lead | Specification |
| U17 | Agree an exact final handover date within September 2027 and an initial laboratory/iteration booking plan. | Owner + laboratory lead | Specification / schedule baseline |

Unknowns remain open; none are resolved by a convenient default. Assign named people before their gate. More unknowns may emerge from architecture work.

## 6. Verification plan

No acceptance test is authorized until its safe setup, responsible person, numerical limits and stop conditions are recorded.

| Test family | Planned evidence |
|---|---|
| Optical | Stabilized flux after diffuser, three CCT variants, Ra, agreed uniformity/distribution and visible points, brightness matching; include flicker measurements and criteria after scope assessment. |
| Electrical | Input power/efficiency, line corners, startup, ripple, open load, absent panel, short and recovery after offline replacement, repeated power cycles and applicable disturbances. |
| Thermal/life | Worst declared ambient/orientation/ventilation, LED board and junction estimate, transformer/driver/capacitor/contact temperatures, thermal shutdown and recovery, cooling delay; documented life estimate. |
| Access/insulation | Exposed surfaces during service, residual charge on base and removed panel, insulation/touch-current tests and applicable single faults selected by the competent reviewer. No historic voltage/spacing target is automatically sufficient. |
| Mechanical | Tool-free replacement, incorrect orientation, partial insertion, retention, thermal contact, repeated diffuser opening and agreed cycle test. |
| EMC | Conducted/radiated emissions, immunity and mains-related performance/flicker as determined by the requirements assessment; document setup and whether evidence is pre-compliance or formal. |

A completed DRC, calculation or simulated fault is not physical validation. Record actual samples, calibration, uncertainty, conditions, source/hardware revisions and raw data.

## 7. Proposed staged schedule

These are planning windows, not promised supplier/laboratory bookings. The owner deadline is September 2027; the exact handover date is open.

| Window | Work and exit |
|---|---|
| Nov–Dec 2026 | Finish requirements, architecture comparison, preliminary mechanical/thermal envelopes and process proposals; specification gate. |
| Jan–Feb 2027 | Driver and LED calculations, interfaces, independently reviewed pin intent, schematic/libraries and verification; schematic gate. |
| Mar 2027 | Envelope choice, thermal/assembly access, placement, then routing with fresh checks and separate human gates. |
| Apr–May 2027 | Release review, separately authorized prototype order and first supervised laboratory bring-up. Panel samples may be needed earlier for driver compliance/thermal decisions. |
| Jun–Jul 2027 | Integrate enclosure/diffuser, measure all variants, correct defects and make a further iteration if needed. |
| Aug 2027 | Final measurements, documentation and demonstration procedure; preserve schedule contingency. |
| Sep 2027 | One reviewed integrated prototype with evidence and explicit remaining limitations. |

Every stage has a frozen packet, independent reviews, fresh applicable checks and explicit human decision. Ordering, physical testing and public demonstration each require their appropriate authorization and conditions; starting this project does not grant them.

## 8. Task, evidence and review status

Task VEL-SPEC-RESET-01: prepare this interview-derived first review packet. One writer: current assistant. Writable scope: new specification-review documentation only. Acceptance for this task: trace owner decisions, separate proposals/unknowns, map next gates and tests, preserve old CAD and explicitly disclose verification gaps. This task is not acceptance of the specification stage.

Toolkit source ZIP supplied by the owner: pcb-agent-toolkit-main.zip. The extracted tree passed package_toolkit.py verify-tree, exit 0, manifest SHA-256 05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822, matching the historical workflow index. This verifies source-tree integrity only; it is not a trusted installable archive digest or an installed launcher. Source provenance is the supplied ZIP, not an asserted new Git revision. No toolkit or KiCad migration is applied.

Requirements CLI: not run; no new machine-readable requirements/interface/evidence contract or installed launcher is claimed. Doctor/ERC/DRC/connectivity/spatial: not run for this draft. No new CAD, simulations or measurements. Historical reports and approvals remain bound to their original revisions and cannot authorize this redesign.

Before declaring the specification stage ready: resolve U01–U04 and U14–U17, produce the versioned requirements.json and interface/unknown records, install/verify the selected tooling as applicable, retain a fresh requirements --stage specification matrix, perform the four independent review roles on the final frozen packet, close blocking findings and obtain actual owner approval. For a documentation-only preliminary review, reviewer findings may identify these known gaps; they must not be recorded as passes for the formal gate.

Integration task before merge or treating this draft as the active brief: update hardware/E27/workflow/project-index.md to point to the reset, mark D5 as historical, and preserve all original records. The existing index is intentionally untouched on this documentation draft branch; it still describes the old active task.

Human approval: NOT GIVEN. Next owner action: review desired behavior, proposed numerical targets and open questions. Next engineering action within specification: compare simpler architectures, obtain needed evidence and complete the formal packet. Schematic work remains blocked.
