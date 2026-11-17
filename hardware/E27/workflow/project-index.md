# E27 workflow index

## Current redesign preparation — 17 November 2026

The owner accepted the product scope/criteria and requested continued work towards the native KiCad power supply. [Product packet r12](specification-reset/requirements-and-plan.md), [actual owner decision](specification-reset/schematic-intent/owner-scope-acceptance.md) and [scope integration packet](specification-reset/scope-stage-packet.md) are current. The old D5 design remains historical.

The exact exported preview0.7.1-preview.3/ruleset0.7.1 is installed using [project launcher](../../../pcb-toolkit.py) and immutable lock, manifest05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822/archive15a2789b06afb014f9dc166ce6da01a903c3b422b5c1b37b2a96581b218784b4. Genuine Ubuntu26.10/KiCad10.0.6/pcbnew executes; [fresh doctor](specification-reset/scope-toolkit-doctor.json) passed. Prior validation covers127 passed unit tests/one Windows skip and101 native example scenarios, not this lamp's CAD or measurements.

The [fresh specification preflight](specification-reset/scope-requirements-preflight.json) now passes with zero specification errors after genuine scope review/acceptance evidence linkage; ten later implementation/process/test unknowns remain. This supersedes the earlier eight-finding finalization preflight as current requirements status without erasing its history. It is a specification-consistency/review-evidence check, not electrical verification.

The independently prepared [physical-pin packet](specification-reset/schematic-intent/README.md) enumerates28 components/73 terminals/21 nets/4 explicit NCs. Four actual independent reviewers recommend owner graph review. Intent digest b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57; its approval remains null. Real acceptance of this new graph is required before generating the schematic. No product schematic/PCB, ERC/DRC, manufacturing files or measurements have been produced by this reset.

Electrical/model/insulation/thermal majors remain open at their affected gates. The owner will perform later laboratory work with experienced support; no hardware/instruments are connected here and no physical test is reported. Exact interfaces and process/material/geometry decisions remain due at their declared stages.

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
