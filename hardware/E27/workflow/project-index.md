# E27 workflow index

## Current critical footprint library — 17 November 2026

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
