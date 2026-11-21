# Velluneo E27 — product reset and specification review

Packet: VEL-SPEC-RESET-01, revision 12, 2026-11-17.
Status: owner accepted product scope/criteria on2026-11-17; integrated specification preflight and fresh review pending. New physical-pin graph has separate unapproved intent.
Repository baseline: 377fc0a08e74043e255b732f7c2beb63134a3576.
Scope: accepted requirements and planning, plus separately drafted pre-CAD connectivity. No CAD, libraries, manufacturing exports or historical approvals are changed.

## 1. Purpose and decision basis

Velluneo is a repairable domestic E27 LED lamp. A user replaces an exhausted LED panel instead of discarding the intact base, power supply and housing. Separately sold panels also allow changing white-light colour without replacing the base.

Basis: the owner's Polish-language interview in the current conversation on 2026-11-14. The owner confirmed offline tool-free replacement, one base for three colours, about 800 lm, a laboratory prototype by September 2027, and freedom to redesign all existing electronics. This record paraphrases those decisions; it is not a new human approval of this packet. No permanent conversation URL is available; preserve the actual review decision when the owner reviews a frozen packet.

Owner: Kamil Stępak. Coordinator/document writer: the current assistant context. Design work and technical checks are assigned to the coordinator and independent agent review contexts; a separate external electronics reviewer is not required to start or continue design. The owner approves stage packets. Laboratory supervisors/support will be established before affected physical tests. Repository documentation is English; discussion with the owner is Polish.

The old 8S/D5 architecture is historical input. Eight LEDs, two contacts, 70 × 34 mm, active load identification, timed probes, a microcontroller and the old current/voltage settings are not constraints for the redesign. Owner selected architecture A on 2026-11-14: isolated constant-current driver in the base and a simple replaceable LED panel. This supersedes the previously open partition choice; exact circuit and all electrical values remain unselected. See architecture-comparison.md revision 2.

## 2. Requirements confirmed in the interview

Requirement rows are revision 1 except R-LIGHT/R-CCT/R-PANEL-LIFE/R-REPLACE/R-DEMO (revision 2) and R-ENV (revision 3). Packet revision 6 records the minimum replacement-cycle count and final handover deadline. Product decisions belong to the owner; engineering acceptance plans belong to the coordinator and assigned technical reviewer. All physical verification is pending. 'Schematic', 'placement' and 'release' identify the gate by which implementation intent or evidence is needed, not permission to proceed now.

| ID | Requirement | Acceptance approach and due gate |
|---|---|---|
| R-PURPOSE | Retain the base when the LED panel fails; replace the complete panel. | Demonstrate panel replacement and restored operation on the integrated prototype; release/integration. |
| R-SUPPLY | E27, nominal Polish 230 V AC / 50 Hz supply; 120 V operation unnecessary. | Establish actual line-voltage design/test envelope before schematic; verify startup, running and faults at its corners before release. |
| R-LIGHT | 750–850 lm emitted by each complete lamp variant with its diffuser fitted (owner accepted). | Stabilized conditions/sample plan remain to be agreed at specification; measure before final demonstration. |
| R-CCT | Panels in nominal 2700 K, 4000 K and 6500 K; brightest/dimmest flux ratio ≤1.10 and CRI Ra ≥80 (owner accepted). | Agree CCT tolerances and stabilized conditions at specification; measure all three variants. |
| R-COMPAT | One base accepts all three panels without settings, switches or user configuration. | Freeze a compatible electrical/mechanical interface before schematic/placement; demonstrate each variant on the same base. |
| R-REPLACE | Tool-free intuitive replacement; prevent incorrect installation. Minimum 50 complete panel replacement and diffuser reclosing cycles without damage to mountings or loss of reliable electrical contact. | Freeze mechanical keying/retention and contact sequence before placement; assess wrong orientation, partial insertion and at least 50 full replacement/reclosing cycles. Keep 100 cycles as a stretch goal only. |
| R-OFFLINE | Replacement only after unscrewing from the socket and waiting for cooling/discharge. After diffuser removal only the panel and mounting are accessible; the driver remains behind a separate base cover. | Determine safe-access conditions and delay by analysis and measurement; instructions alone are not evidence of safety. Limits before schematic, geometry before placement, measured confirmation before release. |
| R-ENV | Dry domestic interiors, ambient 10–40°C; all operating orientations, including base up, base down and horizontal; open or ventilated fixtures. Owner confirmed this narrower first-prototype range after the retail comparison. Closed fixtures, damp locations and outdoor use are outside prototype scope. | Ambient range and all orientations accepted; define ventilation assumptions at specification; identify and test thermal worst-case orientation before release. |
| R-DIFFUSER | Removable milky diffuser hides individual LEDs and provides broad side illumination assessed against an ordinary milky E27 lamp around 800 lm. Emission towards the cap is not required. | Agree distribution and appearance criteria at specification; check fit before placement and optical performance on the complete lamp. |
| R-FAULT | An open/failed panel, missing panel and shorted panel must not damage the base. | Define representative faults and duration before schematic; validate protection and temperatures before release. After offline panel replacement, power cycling restores normal operation without reset or fuse replacement. |
| R-EMPTY | The energized base can remain without a panel without damage or overheating. | Define duration and accessible-part limits before schematic; verify no-load behavior and recovery with the approved test fixture. This does not authorize live replacement. |
| R-THERMAL | Protect against overheating using a justified simple implementation. | Select limiting or shutdown/recovery after comparison. Agree thresholds, hysteresis and protection-fault behavior (including sensor faults if a sensor is selected) before schematic; test before release. |
| R-USE | Design for 8–12 hours/day, including long continuous sessions. | Establish continuous-duty thermal test conditions before schematic; a timetable is not a required forced shutdown. |
| R-BASE-LIFE | Five-year base life is an acceptable design target; ten years is aspirational. | Assess parts at measured electrical/thermal stress. At 8–12 h/day: 14,600–21,900 h in five years; 29,200–43,800 h in ten. Calendar aging also matters. Agree failure/end-of-life definition before schematic. Do not claim years of demonstrated service from short tests. |
| R-PANEL-LIFE | Panel design target: 15,000 operating hours while retaining at least 70% of initial luminous flux (L70 target), accepted by owner. | Evaluate exact LED lifetime data at measured operating conditions and document the assessment and uncertainty. A short prototype test does not demonstrate 15,000 h. Define sample/population criteria, catastrophic-failure treatment and maintenance measurement conditions at specification. |
| R-FEATURES | Basic full-output on/off lighting; no Wi-Fi, app or added smart functions. | Confirm feature scope at specification; check normal behavior before release. Wall-dimmer compatibility is excluded from the primary design. |
| R-SIZE | Compare a conventional-bulb-sized concept with a moderately larger concept that improves cooling and replacement. | Present actual envelopes and tradeoffs for owner selection before placement; no existing board size is binding. |
| R-COST | Prefer rational cost and future manufacturability; no fixed prototype budget. | Compare BOM, sourcing, assembly and tooling costs during architecture and release reviews. No invented cost ceiling. |
| R-BUILD | Prefer JLCPCB fabrication and populated PCB delivery; one LED colour assembled by JLCPCB is sufficient for the first prototype. All three colours need not be stocked/assembled there now. Laboratory assembly remains a fallback; future three-colour common-base compatibility remains required. | Confirm actual service, exact parts/bins for at least one initial colour and any transformer/THT/manual work before process acceptance and release. Future colour variants may use another sourcing/assembly route. Housing and lamp assembly are separate. |
| R-DEMO | Deliver one complete, integrated, laboratory-tested and documented prototype with at least one colour no later than 30 September 2027. Completing all three colours by then is a stretch goal, not a deadline acceptance condition; iterations are allowed. | Final deadline accepted: 30 September 2027. Agree detailed test scope and intermediate bookings; retain matched hardware revisions and actual reports. Commercial certification and sales release are not automatically included. |

The owner reports access to university laboratories for flux, colour, CRI, safety and interference measurements, with experienced support, and holds SEP qualifications. Instruments, calibrated methods, responsible people and availability remain unverified planning inputs. This packet records no physical tests.

## 3. Numerical decision register and remaining proposals

| ID | Proposal | Meaning |
|---|---|---|
| P-OPTICS | 750–850 lm per variant; brightest/dimmest ratio no greater than 1.10 under the same stabilized conditions. | OWNER ACCEPTED on 2026-11-14 in this conversation. Both limits must hold; conditions/sample plan remain open. This accepts desired performance, not measured compliance. |
| P-CRI | CRI Ra ≥80 for all variants. | OWNER ACCEPTED on 2026-11-14 in this conversation. Not a measured result. |
| P-AMBIENT | Ambient 10–40°C for the first prototype. | OWNER ACCEPTED on 2026-11-14 after clarification that this is a narrower prototype scope, not retail-range equivalence. Wider-temperature operation is outside current scope. |
| P-SUPPLY | Evaluate 207–253 V AC / 50 Hz as the initial normal-operation screening range. | Requires competent review of the applicable supply/product requirements; not a complete surge or fault envelope. |
| P-ISOLATION | Compare an isolated driver first because the LED panel is user-accessible. | A starting architecture preference only. Determine actual protection class, insulation system, barriers, contact voltage/energy and safe-access limits before schematic. Do not equate low voltage or an isolation label with proven safety. |
| P-SIMPLICITY | Remove the requirement for live-insertion recognition and retry probes. | Consider omitting their implementation only after showing the simpler driver meets open/short/no-load and residual-energy requirements. |

One hundred mechanical replacement cycles is an owner-accepted stretch goal, not a prototype pass/fail requirement. Minimum 50 full panel-replacement and diffuser-reclosing cycles is required; mountings and reliable electrical contact must remain intact. A replacement diffuser is a future product direction; the present requirement is repeat removal and refitting. Optional dimmable-driver work must have a separate scope and must not block the basic prototype.

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
| U01 | P-OPTICS and P-CRI accepted by owner on 2026-11-14; P-SUPPLY and its technical basis remain open. Optical measurement conditions are still tracked at U14. | Owner + technical reviewer | Specification |
| U02 | Panel target 15,000 h / ≥70% initial flux accepted on 2026-11-14. Define sample/population acceptance, catastrophic-failure treatment, maintenance measurement conditions remain open. Minimum replacement life is now accepted as 50 complete panel-replacement/diffuser-reclosing cycles. | Owner + coordinator | Specification |
| U03 | External pre-fabrication electronics reviewer is not an owner prerequisite. Assign technical calculations/checks to the coordinator and four independent agent contexts; owner retains stage approval. Establish a feasible proposed fabrication/assembly route with unconfirmed constraints explicit. Name physical-test personnel before affected tests; detailed order evidence remains due at U11/U13. | Coordinator + owner | Specification |
| U04 | Select exact laboratory-demo scope versus external qualification; identify applicable product/safety/EMC/flicker requirements without assuming old limits. | Technical reviewer + owner | Specification |
| U05 | Architecture A selected by owner: isolated CC driver in base, simple LED panel. Select/verify its LED and driver implementation using power, tolerance, thermal and cost calculations; no fixed LED count or current. | Coordinator + independent reviewer | Schematic |
| U06 | Implement the product-level safety/operating criteria from U16: determine numerical circuit limits, discharge/cooling implementation, short duration/recovery, hot/cold startup and disturbance response. | Electrical reviewer + laboratory lead | Schematic |
| U07 | Develop thermal/life calculations and detailed optical measurement procedures using the specification decisions from U14/U15; define base lifetime/end-of-life basis. | Coordinator + laboratory lead | Schematic |
| U08 | Select overtemperature behavior, thresholds and protection-fault response (including sensor faults only if a sensor is selected); define absence/reversal/partial-contact abuse cases even though live replacement is forbidden. | Electrical/mechanical reviewers | Schematic |
| U09 | Freeze panel/base pin map and independently reviewed intended connectivity with exact datasheet/pin/footprint basis. | Coordinator + independent reviewer + owner decision | Schematic |
| U10 | Freeze preliminary enclosure envelope, heat path/contact, insulation materials, dimensions, heights, keying and retention. | Mechanical owner (to assign) + coordinator | Placement |
| U11 | Confirm actual stackup, copper, materials and service limits as needed for insulation/layout/assembly. | Coordinator + supplier | Placement |
| U12 | Confirm available calibrated instruments, personnel, samples, test limits and stop conditions. Release evidence must cover actual operating/fault conditions. | Laboratory lead + owner | Release / each affected physical test |
| U13 | Establish BOM availability, exact costs, release outputs, matched revisions and test/programming/assembly instructions. | Coordinator + supplier + owner | Release |
| U14 | Owner accepted an ordinary milky approximately 800 lm E27 lamp as distribution reference, without cap-direction emission. Select exact reference/comparison conditions; finalize CCT tolerances, stabilized optical conditions and sample plan. | Owner + coordinator + laboratory lead | Specification |
| U15 | Ambient 10–40°C and all orientations are accepted. Define open/ventilated-fixture assumptions and the thermal worst-case analysis/test plan at specification. Actual worst-case measurements belong to R-ENV/U12 before the affected tests and release, not before design. | Owner + coordinator + technical reviewer | Specification |
| U16 | Owner accepted separate base shielding: only panel/mounting accessible after diffuser removal. Define remaining normal/fault, recovery, residual-energy and cooling criteria through coordinator and independent technical reviews; implementation follows U06. | Electrical reviewer + owner + laboratory lead | Specification |
| U17 | Final handover deadline 30 September 2027 accepted; the proposed staged planning baseline is recorded. Confirm actual laboratory/iteration bookings before affected work/tests, without blocking ordinary design on bookings. | Owner + laboratory lead | Release / before affected tests |

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

These are planning windows, not promised supplier/laboratory bookings. The owner-confirmed final handover deadline is 30 September 2027. Earlier internal dates remain proposed planning milestones, not confirmed bookings.

| Window | Work and exit |
|---|---|
| Nov–Dec 2026 | Finish requirements, architecture comparison, preliminary mechanical/thermal envelopes and process proposals; specification gate. |
| Jan–Feb 2027 | Driver and LED calculations, interfaces, independently reviewed pin intent, schematic/libraries and verification; schematic gate. |
| Mar 2027 | Envelope choice, thermal/assembly access, placement, then routing with fresh checks and separate human gates. |
| Apr–May 2027 | Release review, separately authorized prototype order and first supervised laboratory bring-up. Panel samples may be needed earlier for driver compliance/thermal decisions. |
| Jun–Jul 2027 | Integrate enclosure/diffuser, measure all variants, correct defects and make a further iteration if needed. |
| Aug 2027 | Final measurements, documentation and demonstration procedure; preserve schedule contingency. |
| Sep 2027 | Final corrections, documentation and presentation preparation; by 30 September deliver one complete, integrated, reviewed and tested prototype with its evidence and stated limitations. This is the final completion deadline, not the start of integration. |

Every stage has a frozen packet, independent reviews, fresh applicable checks and explicit human decision. Ordering, physical testing and public demonstration each require their appropriate authorization and conditions; starting this project does not grant them.

## 8. Task, evidence and review status

Task VEL-SPEC-RESET-01: prepare this interview-derived first review packet. One writer: current assistant. Writable scope: new specification-review documentation only. Acceptance for this task: trace owner decisions, separate proposals/unknowns, map next gates and tests, preserve old CAD and explicitly disclose verification gaps. This task is not acceptance of the specification stage.

Toolkit source ZIP supplied by the owner: pcb-agent-toolkit-main.zip. The extracted tree passed package_toolkit.py verify-tree, exit 0, manifest SHA-256 05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822, matching the historical workflow index. This verifies source-tree integrity only; it is not a trusted installable archive digest or an installed launcher. Source provenance is the supplied ZIP, not an asserted new Git revision. No toolkit or KiCad migration is applied.

Historical pre-contract status was: no requirements CLI or machine-readable contract. Current status: draft requirements.json and hardware.json exist, and preflight-output.json records an actual standalone-candidate requirements run returning incompleteness (exit 1); see specification-readiness.md. Installed launcher/doctor and CAD/interface checks remain pending. Doctor/ERC/DRC/connectivity/spatial: not run for this draft. No new CAD, simulations or measurements. Historical reports and approvals remain bound to their original revisions and cannot authorize this redesign.

Before declaring the specification stage ready: resolve U01–U04 and U14–U16, produce the versioned requirements.json and interface/unknown records, install/verify the selected tooling as applicable, retain a fresh requirements --stage specification matrix, perform the four independent review roles on the final frozen packet, close blocking findings and obtain actual owner approval. For a documentation-only preliminary review, reviewer findings may identify these known gaps; they must not be recorded as passes for the formal gate.

Integration task before merge or treating this draft as the active brief: update hardware/E27/workflow/project-index.md to point to the reset, mark D5 as historical, and preserve all original records. The existing index is intentionally untouched on this documentation draft branch; it still describes the old active task.

Human approval: NOT GIVEN. Next owner action: review desired behavior, proposed numerical targets and open questions. Next engineering action within specification: compare simpler architectures, obtain needed evidence and complete the formal packet. Schematic work remains blocked.

## 9. Revision 3 decision and review impact

Owner decision in the current conversation, 2026-11-14: accepted proposed brightness and colour rendering; accepted 10–40°C only if comparable to ordinary bulbs. Record P-OPTICS/P-CRI as confirmed performance intent and P-AMBIENT as conditional, pending clarification after manufacturer comparison. No exact message URL is available; the original conversation remains the approval source. This does not approve the full packet or any circuit.

The four review reports in review-status.md cover the exact revision 2 hash only. Revision 3 changes optical requirement text, adds manufacturer comparison and records owner decisions. Affected requirements/contracts/digests and reviews must be refreshed for a future formal gate. No formal requirements check, new independent review, CAD check or physical measurement is claimed for revision 3. All other open questions and the integration-index task remain open.

## 10. Revision 4 owner decision

On 2026-11-14, after the narrower-than-retail temperature comparison and a direct question about retaining 10–40°C for the first prototype, the owner confirmed: "Так, можем устаљити." This records acceptance of ambient 10–40°C for the prototype, not a measured thermal pass or full specification-stage approval. U15 remains partially open for orientation and ventilation conditions. No wider-temperature compatibility is claimed. Revision 2 review reports remain historical; affected formal-gate reviews and requirement evidence must be refreshed when the full specification is frozen. No CAD or physical test changes.

## 11. Revision 5 owner decisions

On 2026-11-14 the owner accepted every operating orientation and the proposed panel lifetime plan, in response to a question explicitly describing 15,000 h with at least 70% initial light output and the limitation of short-term testing. Record base-up, base-down and horizontal as required test orientations, plus any intermediate worst case identified. The panel L70 figure is a design target, not demonstrated lifetime; it does not specify a B-value/population failure fraction or catastrophic-failure allowance, which remain U02 questions. U15 remains partly open for fixture/ventilation conditions. Full packet approval is absent; revision 2 reviews are historical and affected formal-gate reviews must be refreshed. No CAD, orders or physical test results changed.

## 12. Revision 6 owner decisions

On 2026-11-14 the owner rejected the proposed 20-cycle minimum and required at least 50 full panel replacement and diffuser reclosing cycles without mounting damage; the earlier no-contact-degradation acceptance proposal is retained. One hundred cycles remains an optional stretch target. The owner confirmed 30 September 2027 must be final completion of the entire prototype, not an intermediate electronics milestone. Existing scope remains one complete tested prototype, not commercial series-production authorization. Targeting main assembly/tests by end of August remains a proposed internal schedule; it is not a separate owner-approved deadline. U02 remains open for lifetime population/failure and measurement details; U17 remains partly open for bookings and intermediate milestones. No full-stage approval, updated formal review, CAD check or physical result is claimed.

## 13. Revision 7 architecture decision

Owner statement on 2026-11-14: "tak robimy wariant A". Architecture A is the selected direction: isolated mains-to-LED conversion and current regulation in the base; replaceable panel contains LEDs and only justified minor ancillary parts. See architecture-comparison.md revision 2. This accepts functional partition, not a specific part, pin map, LED count/current, protection circuit, electrical safety claim or complete specification-stage packet. Other scope decisions are unchanged. Formal checks and affected reviews remain pending before schematic work.

## 14. Revision 8 first-sample sourcing decision

On 2026-11-14 the owner clarified that one colour variant manufacturable and populated by JLCPCB is sufficient for initial sampling. Do not block the first prototype on simultaneous JLCPCB availability of all three CCT variants. The owner did not remove the final three-colour product compatibility/optical goals, select the first colour, confirm live stock or authorize orders. 4000 K is the coordinator's first sourcing candidate only. Existing stock/process unknowns now apply to the chosen initial variant for the first order, with other variants tracked for later characterization. No formal stage approval or CAD change.

## 15. Revision 9 design responsibility clarification

Owner explicitly stated that no external person is assigned to review before fabrication and asked the assistant to produce a correct design. The assistant accepted responsibility for preparing calculations, schematics, part/library checks, PCB and documented verification within the available tools, with independent agent inspections and genuine owner stage decisions. Do not block design on appointing an outside electronics reviewer. Do not interpret that clarification as completed checks, certification, waiver of unresolved technical requirements, permission to skip stage gates, manufacturing authorization or authorization to energize hardware. Physical operation, thermal behavior, isolation and protection still need actual laboratory evidence, with personnel/setup/limits defined before the affected test. Existing role-based engineering unknowns identify work responsibilities rather than a mandatory external appointment.


## 16. Revision 10 traceability corrections

Current source-validator status replaces the older pre-contract statement. U08 does not mandate a separate temperature sensor. U15 requires declared environmental assumptions and an analysis/test plan at specification, not measured thermal results before design. U17 bookings are due before affected execution/tests and release, not a prerequisite for ordinary design. U12 and U17 use release as their nearest available machine gate; separate test readiness/authorization checks are required before every physical test because a specification/requirements pass alone cannot enforce test readiness. No existing physical-check or release obligation is waived. Formal specification still has substantive unresolved inputs and no owner stage approval.

## 17. Revision 11 owner decisions

The owner accepted a separate base cover: diffuser removal exposes only the LED panel and mounting. Opening the driver cover is not part of panel replacement. Technical insulation/accessibility/discharge details remain open.

The final deadline remains 30 September 2027 for one complete tested prototype with at least one colour. All three completed colour panels by then are desirable, not mandatory if time is insufficient. The three-colour common-base product-family goal remains; never claim unbuilt variants were measured. Before release distinguish tested prototype configuration from future family qualification rather than using one panel to pass all-colour criteria. First sample colour remains a sourcing choice; 4000 K is proposed.

Light distribution is compared against an ordinary milky approximately 800 lm lamp; emission towards the cap is not required. Exact reference/test conditions remain to be selected; no numeric 220–360 degree criterion is adopted. Current priority remains the driver, with mechanical interface assumptions only as needed for isolation, heat and fit. These are actual owner decisions from the current conversation on 2026-11-14, not approval of the complete stage or circuit.

## 2026-11-17 accepted-scope addendum (revision12)

This addendum supersedes earlier descriptions of scope/criteria as awaiting owner decision. Actual owner message and its scope are preserved in schematic-intent/owner-scope-acceptance.md. The owner accepts desired behavior and continued design, not electrical certification or the subsequently prepared physical-pin graph.

Use finalization/decision-packet.md (frozen SHA256 ea6ef879ed417a6ced7360e1434ce873637becf548e33cf261296bcfa9401fba) for the concrete proposed procedures accepted as engineering planning direction: normal207–253Vac/49–51Hz; start≤1s/≥90% stabilizedflux; PstLM≤1.0/SVM≤0.4; CCT2700±150K/4000±200K/6500±300K; first4000K; one measured complete configuration by30September2027 with eventual family requirements retained.

Photometry at230Vac50Hz,25±1C,complete lamp/baseup; at least30min and three5minspaced fluxreadings differing<0.5%,extenduntilstable. CorePro reference and matched polar/appearance comparison follow U14. Thermal baseline is barelampholder,stillair,no surroundingfixture,≥200mm nearbyclearance,10/25/40C/baseup/basedown/horizontal plus anyworseorientation; steadycriticaltemperatures<1K/hourfor1hour after≥3hours. These are planned methods, not measurements.

P0 sample target is one complete prototype.100h/zero catastrophicfailures/≥95%initialflux is an early-workmanshipscreen, not15000hL70orpopulationproof. Base5yearassessment needs component-specific actualtemperature/stress/calendar evidence;10yearsaspirational.

Open/absent/hardshort panel outcomes include no base damage, no fuse/manualreset, offline replacement andpowercycle recovery. Plan24h faultscreen after thermalsteadystate plus repeatedrecovery; individualLEDfaults/contactbounce/wrongorpartialinsertion are separateimplementationcases. AutomaticNTCinhibition/retry is selected direction, threshold/lag/sensorfaultadequacy remains due at schematicacceptance. Servicegoals≤5VDC/≤0.5mJ/≤45C are projectgoals, not universalstandardlimits; actual instructionwait comes from wholeassemblymeasurements.

Proposeddriverfabrication2layerFR4/1.6mm/2oz/greenmask/leadfreeENIG and supplierSMDpopulation, agreedTHT/customtransformerroute, manualfallback; order-specificmaterial/CTI/stackup/assemblyconfirmation is due beforeplacement/processacceptance. No orderauthorized. Completeproductsemi-luminaireclassification and nativeIEC60598/61347/62031/CISPR15/61547/61000-3-2 sourcefamilies are identified in U04; fullclause/numericalinsulation/ENadoption/commercialqualification remain owned implementation gaps. This prototype scope does not assert compliance.

Pre-CAD connectivity is schematic-intent/intended-connectivity.json, independent of oldCAD and not yet approved. Existing circuit/modelmajorfindings remain open at their original acceptance scope.


## 2026-11-21 accepted-scope addendum (revision13 - higher flux permitted)

The owner stated in the current conversation: "jak będzie wiecej lumenów to nie problem".
No permanent message URL is available. Record the original wording rather than
inventing an external approval link. The previous850lm upper target is no longer
a rejection ceiling. Preserve the750lm minimum and all other colour/family matching,
CCT/CRI, electrical, thermal, service, dimensional, insulation and life requirements.
No new exact lumen maximum or higher electrical/thermal rating is invented.

This supersedes only the old upper-flux criterion. Frozen historical packets retain
their exact bytes; their850lm rejection conclusions do not override this owner decision.
See led-compatibility-19 for the current319mA/sevenLED compatibility assessment.
The message does not approve a circuit/panel revision, assembly process, manufacturing,
ordering or physical qualification. Photometric and thermal methods remain as recorded.
