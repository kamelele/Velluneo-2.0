# E27 workflow index

## Current startup, protection, thermal and insulation development — 17 November 2026

[PCB-READINESS-01](specification-reset/pcb-readiness-01/README.md) adds executed coupled startup/clamp/NTC/thermal/life/discharge calculations and a source-conditioned transformer material/build candidate. Current31-position CAD/graph/values stay unchanged. New20uH leakage,4W/8W heat-removal and material/process conditions are proposed design inputs, not actual assembly performance or accepted norms. [Exact PCB-entry contract](specification-reset/pcb-readiness-01/pcb-entry-contract.json) retains startup/controller/fault/SOA, complete transformer/insulation and actual enclosure/thermal closures. The owner has no full standards; a discovered expired member rendering is not used to bypass access or establish normative limits. No schematic/placement approval, PCB or physical test is claimed.

## Current library source confirmation — 17 November 2026

[LIB-SOURCE-03](specification-reset/library-source-03/README.md) uses primary KEMET commercial C0G Table3 densityB lands for C2/C3 and confirms F1 copper directly against the downloaded official SCHURTER PDF/drawings. [Current KiCad draft ZIP](specification-reset/library-source-03/Velluneo_driver_LIB03_KiCad.zip) and [schematic PDF](specification-reset/library-source-03/Velluneo_driver_LIB03.pdf) supersede earlier native packages for the new assignment bytes. The owner-approved ECO-01 physical graph,31positions/79terminals/22nets/4NC, values, electrical types and rules are unchanged.19available modules include one retained historical KEMET pattern;18definitions are active.

Actual pinned KiCad10.0.6/matching pcbnew doctor, all-module geometry, graph, MPN/BOM contract, enabled ERC and output/member checks pass at their stated scopes. Requirements U05-U09 and managed work-check configuration remain incomplete. Source confirmation does not qualify soldering, body tolerances, fuse coordination or any inherited electrical/model/thermal/insulation/process finding. No PCB, routing, DRC or physical measurement is created. The separately supplied toolkit-reference checkout was verified as exact86614c3; the unchanged installed manifest/lock remains authoritative. Prior capture packages and reports below are historical for their own source revisions.

## Current electrical refinement evidence — 17 November 2026

[ELEC-REFINE-02 r2](specification-reset/electrical-refinement/README.md) adds64actual finite-R switched-load endpoint cases with200ns/100ns convergence/KCL/RMS/FFT,48finite-auxiliaryloss/charge scenarios,100optical/metrologicalbudgetcases and clamp/winding commutationfrontiers. WorstmodeledbulkRMS127.135mA vssevere152mAcomparison supports retaining15uFcandidates; updatedactive-R13/noVFoutminimum startupwitnessVDD11.2246V supports retainedRAUX4.7underdeclaredhypotheses. Factory-onlyopticalcalibration is analyzed at the accepted230V50Hz/25±1°Ccomplete-lamp condition; no measuredflux orchangedR92.37value.

[Fouractualreviews/integration](specification-reset/electrical-refinement/integration-record.md) support boundedanalysisdelivery only. All66previousnativecaptureinputs are unchanged, so the currentECO-01KiCadZIP/PDF below remainscurrent. No CAD/approvedgraph/partvalue/requirements/profile change ornewECOapprovalquestion. Actualcontroller/parasitic/clamp/fault/thermal/interface/lifetime/process evidence and U05–U09/fullconfiguration remainopen; no finishedsupply/PCB/DRC/physicalmeasurement claim. The smallrawprefix is identifiedaspreview; fullgeneratedwaveformhash/spectrum/replay arepreserved withoutversioning34MBofintermediatedata.

## Current owner-approved ECO-01 native capture — 17 November 2026

The owner accepted exactECO-01 graph5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8. [Current SCH-ECO01-02 packet](specification-reset/eco01-capture/README.md), [nativePDF](specification-reset/eco01-capture/Velluneo_driver_ECO01.pdf) and [editableKiCadZIP](specification-reset/eco01-capture/Velluneo_driver_ECO01_KiCad.zip) implement the four499k2512 dualbulkbleed/twoexistingpackagechanges, added1MVDDbleed and exactnumericreferencealiases.31positions/79physicalterminals/22nets/4NC now match the acceptedintent;18unchangedlocalfootprintdefinitions cover allpositions. Activeparts basis is electrical-integration/proposed-parts.json; old schematic-intent/parts.json is deliberately preserved as historicalhashboundbasis.

ActualnativeKiCad10.0.6 doctor/geometry/graph/ERC/MPN-BOM-footprintchecks and PDF/SVGexports pass at documentedscopes. The previousannotationwarning is absent and SCH-ANN-001 narrowly independentlyclosed. [Fouractualreviews/integrationrecord](specification-reset/eco01-capture/integration-record.md) support thiscapturetransfer only. SchematicrequirementsU05–U09 and fullmanagedconfiguration stillfail. Prior startup/clamp/model/input/flux/capripple/magnetics/service/thermal/safety/process majors stayopen; no finishedsupply/PCB/routing/DRC/order or physicalmeasurement. AcceptedECOpermission is already recorded; no repeatdecision needed for its application. Earlier28component reports/packages and predecisionnullapprovalproposal below are historical for their ownrevisions.

## Current electrical integration and passive ECO review — 17 November 2026

The [ELEC-CLOSE-01 r2 packet](specification-reset/electrical-integration/README.md) adds source-backed startup analysis(128ramp/768residual-current cases), an authentic-core/bobbin winding-window diagnostic, hot copper-loss calculations and1152averaged input cases with timestep refinement. It identifies a bulk-bleeder one-open/one-short weakness and prepares a specific [31-position passive/numeric-reference ECO](specification-reset/electrical-integration/ECO-01.md), [proposed graph](specification-reset/electrical-integration/proposed-connectivity.json) digest5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8. The changed graph is unapproved and unapplied; the existing approved28-position native schematic/local library remains byte-identical.

[Four actual independent reviews and integration record](specification-reset/electrical-integration/integration-record.md) recommend exactECOintent human review only. Current native doctor/oldgraph/ERC checks pass in their limited scopes; schematic requirementsU05–U09 and fullmanagedconfiguration still fail. Newcapacitortotalripple and current/flux budget gaps are explicit, along with all earlier electrical/model/thermal/safety majors. Proposed40V openfault ceiling is illustrative/unapproved; no complete service wait is established. No finished supply/PCB/DRC/order or physical measurement is claimed.

## Current all-position library candidates — 17 November 2026

All28 physical component positions now have candidate footprints using18 unique definitions. The [current packet](specification-reset/transformer-footprint/README.md) resolves the earlier T1 view ambiguity through independently checked authentic STEP/PDF marking correlation. [Current editable ZIP](specification-reset/transformer-footprint/Velluneo_driver_all_footprints.zip) includes the complete local library. Current52-file source hashes and four targeted final reviews retain prior17 unchanged module scopes.

Native KiCad10.0.6 checks pass for all18 module geometries/28 assignments/73 footprint terminals, unchanged full28-component graph and zero reported enabled ERC findings. Completing assignment does not qualify every part/process: F1 source-visual gap, KEMET/project copper, THT/wire construction and finished transformer insulation/envelope remain explicit. Schematic requirements U05–U09, full managed-configuration failure and all existing electrical/model/thermal/safety majors stay open. No productPCB, copper, DRC or manufacturing release exists.

## Earlier three-part footprint library — 17 November 2026

The [FOOTPRINT-01 packet](specification-reset/footprint-study/README.md) creates and assigns three actual native footprints for U1, BR1 and Q1, with source-backed copper and exact approved numbering. [Current ZIP](specification-reset/footprint-study/Velluneo_driver_3_footprints.zip) includes the local library and assignments. Four independent contexts reviewed the36-file candidate packet. Native15-pad geometry, unchanged28-component physical graph and ERC checks pass at their stated scopes; only3of28 footprints are addressed. Schematic-stage acceptance, remaining physical libraries/interfaces/process and all old electrical majors stay open. No productPCB exists. Earlier capture reports/packages below remain historical for their source revision.

## Earlier native schematic capture — 17 November 2026

The owner accepted the exact independently reviewed physical-pin map and instructed capture. [Actual decision](specification-reset/schematic-capture/owner-intent-approval.md) binds graphintent b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57 to prior commit0b79ac05d025fdcde1de0418874043a2d5f530b2. Graph topology/basis remains unchanged; only its approval is now recorded. This is not approval of the newly generated schematic stage.

The [editable native schematic](specification-reset/Velluneo_specification_reset.kicad_sch), local library, [PDF](specification-reset/schematic-capture/Velluneo_driver.pdf), [KiCad ZIP](specification-reset/schematic-capture/Velluneo_driver_KiCad_draft.zip) and [capture packet](specification-reset/schematic-capture/README.md) now exist. Root is the sole CAD/library writer. Support/model contexts supplied bounded source/annotation investigations; separate Reality/Overengineering/Completeness/Change contexts review the frozen capture.

Actual locked KiCad10.0.6 comparison passes28 physical components/73 terminals/21 nets/4NC against approved intent. Native ERC exits0 with no reported findings under the recorded default checks after three justified non-physical source declarations. U1 types, physical graph and ERC severities/exclusions are unchanged. Native export still reports the approved nonnumeric-reference annotation warning; SCH-ANN-001 remains open.

[Requirements schematic check](specification-reset/schematic-capture/requirements-schematic.json) remains incomplete at U05–U09. [Full work check](specification-reset/schematic-capture/check-work.json) records configuration failure because managed profile/rules/ownership and a realPCB are absent; no DRC or full stage pass is claimed. Physical footprints, transformer insulation/build, LED/interface implementation and existing startup/clamp/model/thermal/safety majors remain open. No dummy PCB, order or physical test is created.

The installed exact preview0.7.1-preview.3/ruleset0.7.1, manifest05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822/archive15a2789b06afb014f9dc166ce6da01a903c3b422b5c1b37b2a96581b218784b4, and supported Ubuntu26.10/KiCad10.0.6/pcbnew runtime remain pinned. Fresh doctor passes. Earlier tool qualification covers examples, not this product. Accepted r12 product scope and passing specification-level preflight remain valid at their limited content/evidence scope.

The older toolkit/task entries below are historical provenance and must not override the above current preparation state or reactivate earlier approvals for this redesign.

## Historical toolkit and tools

- Workflow reference [pcb-agent-toolkit 0.7.1 at commit 86614c3](https://github.com/wiktor426/pcb-agent-toolkit/tree/86614c3b9b43713031e0ea481edbe26b71cd1b8f). Use the toolkit checkout outside the Velluneo source tree. Start with the existing-project guide and the project instructions in that revision.
- The toolkit's tree verification passed against the files archived from the exact Git commit. Manifest SHA-256 is `05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822`. It is a candidate. Installed launcher and archive lock are pending.
- The historical E27 checks used KiCad 10.0.8. The local CLI reports 10.0.8 and its bundled Python reports 3.11.5. The toolkit validates KiCad 10.0.6 with its matching pcbnew Python. Verify a compatible environment and run doctor before using toolkit CAD checks. Record any proposed CAD-version migration as a separate task.

## Baseline and ownership

- Existing CAD baseline [239eeee](https://github.com/kamelele/Velluneo-2.0/commit/239eeee4522100944dae18d29fecb506b6db07f1). The existing [prototype handoff](../Pakiet_prototypu_JLCPCB.md) uses [power Rev K](../outputs/Zasilacz_RevK_Moc/README.md) and [control Rev H](../outputs/Zasilacz_RevH_Sterowanie/README.md). [Rev L valley-fill](../outputs/Studium_RevL_ValleyFill/README.md) is a development study. Historical reports are baseline evidence.
- On 2026-11-11 the project owner selected one series string of eight LEDs. The Rev K and Rev H pair and its JLCPCB files are the historical 2×8 prototype reference. The existing valley-fill study remains historical evidence for that design family.
- The owner accepted the 8S specification and process proposal for design planning on 2026-11-12. Codex owns the interface preparation task. CAD and library write ownership will be assigned after the interface and independent pin intent review.

## Historical 8S task (superseded by owner reset direction)

- [E27-8S-SPEC task contract](8s/task-contract.md) and [current specification packet](8s/stage-packet.md). The candidate uses one isolated current-regulated output and targets one power PCB.
- [Owner decision](8s/process-decision.md) and [passing specification check](8s/requirements-approved-check.json). Board-specific material and assembly evidence remains due at the later gates.
- [Schematic preparation](8s/schematic-prep.md) proposes the connector map and output-voltage window. [Schematic requirements check](8s/schematic-prep-check.json) tracks the outstanding electrical envelope and independent pin intent.
- [Output protection and cold-start study](8s/output-protection-study.md) records the calculated eFuse window and the contact-side discharge and insertion tests for OPEN-CC.

- [8S driver circuit proposal and illustrated connections](8s/driver-circuit-proposal.md) develops the single-board power path and the protection and interlock pin groups for the next connectivity review.
- [8S driver pin intent and protection review](8s/driver-pin-review.md) records the checked active-device pins, JLCPCB resistor candidates, and the remaining voltage and recovery limits.
- [8S short protection and restart candidate](8s/short-protection.md) records the monitor, startup qualification, retained supply and bench acceptance conditions.
- [8S schematic capture input](8s/driver-8s-capture-input.md) records the verified Rev K/Rev H CAD delta and the provisional one-board pin map.
- [Native 8S KiCad draft 8S-D1](../outputs/Zasilacz_8S_Draft/README.md) is the owner-authorized preview with open protection logic marked on the sheet. It is separate from the 16-LED baseline.
- [8S-D2 startup and short control](8s/driver-8s-control.md) captures the complete candidate permit path and records verification and remaining prototype checks.
- [8S-D3 schematic corrections and review](8s/driver-8s-d3-review.md) records the timer input, hold supply, fresh checks and remaining brownout and re-enable cases.
- [8S-D3 brownout check and unrouted 3D placement study](8s/driver-8s-d3-placement-preview.md) records the conditional re-enable path and the draft PCB preview.
- [8S restart decision and hardware-inhibit candidate](8s/driver-8s-restart.md) records the power-good clamp, restart alternatives, state checks and energy screens.
- [70 × 34 mm compact 8S-D3 placement study](8s/driver-8s-compact-placement.md) includes both PCB faces and the current size and verification limits.
- [8S-D4 hardware inhibit and compact placement](8s/driver-8s-d4-inhibit.md) captures the 3.3 V undervoltage clamp and its fit on the 70 × 34 mm draft.
- [Two-contact output and automatic restart](8s/driver-8s-two-contact.md) is the active design decision after D4. The D4 and earlier interlock designs are archived reference studies.
- [D5 secondary circuit and footprint study](8s/driver-8s-two-contact-circuit.md) records the two-contact shutdown and retry path, probe limits and the 70 × 34 mm placement experiment.
- [D5 two-level probe and hardware timing](8s/driver-8s-probe-timing.md) records transient discrimination, pulse and idle interval bounds, and the probe overvoltage cutoff candidate.
- [Przegląd projektu dla mentora](8s/podglad-dla-mentora.md) pokazuje obie strony D5, działanie wersji dwustykowej i wcześniejsze wersje projektu.
