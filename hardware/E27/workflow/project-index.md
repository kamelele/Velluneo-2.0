# E27 workflow index

## Toolkit and tools

- Workflow reference [pcb-agent-toolkit 0.7.1 at commit 86614c3](https://github.com/wiktor426/pcb-agent-toolkit/tree/86614c3b9b43713031e0ea481edbe26b71cd1b8f). Use the toolkit checkout outside the Velluneo source tree. Start with the existing-project guide and the project instructions in that revision.
- The toolkit's tree verification passed against the files archived from the exact Git commit. Manifest SHA-256 is `05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822`. It is a candidate. Installed launcher and archive lock are pending.
- The historical E27 checks used KiCad 10.0.8. The local CLI reports 10.0.8 and its bundled Python reports 3.11.5. The toolkit validates KiCad 10.0.6 with its matching pcbnew Python. Verify a compatible environment and run doctor before using toolkit CAD checks. Record any proposed CAD-version migration as a separate task.

## Baseline and ownership

- Existing CAD baseline [239eeee](https://github.com/kamelele/Velluneo-2.0/commit/239eeee4522100944dae18d29fecb506b6db07f1). The existing [prototype handoff](../Pakiet_prototypu_JLCPCB.md) uses [power Rev K](../outputs/Zasilacz_RevK_Moc/README.md) and [control Rev H](../outputs/Zasilacz_RevH_Sterowanie/README.md). [Rev L valley-fill](../outputs/Studium_RevL_ValleyFill/README.md) is a development study. Historical reports are baseline evidence.
- On 2026-11-11 the project owner selected one series string of eight LEDs. The Rev K and Rev H pair and its JLCPCB files are the historical 2×8 prototype reference. The existing valley-fill study remains historical evidence for that design family.
- The owner accepted the 8S specification and process proposal for design planning on 2026-11-12. Codex owns the interface preparation task. CAD and library write ownership will be assigned after the interface and independent pin intent review.

## Active task

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
