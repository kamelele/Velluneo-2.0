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
