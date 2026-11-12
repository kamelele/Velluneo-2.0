# E27 workflow index

## Toolkit and tools

- Workflow reference [pcb-agent-toolkit 0.7.1 at commit 86614c3](https://github.com/wiktor426/pcb-agent-toolkit/tree/86614c3b9b43713031e0ea481edbe26b71cd1b8f). Use the toolkit checkout outside the Velluneo source tree. Start with the existing-project guide and the project instructions in that revision.
- The toolkit's tree verification passed against the files archived from the exact Git commit. Manifest SHA-256 is `05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822`. It is a candidate. Installed launcher and archive lock are pending.
- The historical E27 checks used KiCad 10.0.8. The local CLI reports 10.0.8 and its bundled Python reports 3.11.5. The toolkit validates KiCad 10.0.6 with its matching pcbnew Python. Verify a compatible environment and run doctor before using toolkit CAD checks. Record any proposed CAD-version migration as a separate task.

## Baseline and ownership

- Existing CAD baseline [239eeee](https://github.com/kamelele/Velluneo-2.0/commit/239eeee4522100944dae18d29fecb506b6db07f1). The existing [prototype handoff](../Pakiet_prototypu_JLCPCB.md) uses [power Rev K](../outputs/Zasilacz_RevK_Moc/README.md) and [control Rev H](../outputs/Zasilacz_RevH_Sterowanie/README.md). [Rev L valley-fill](../outputs/Studium_RevL_ValleyFill/README.md) is a development study. Historical reports are baseline evidence.
- On 2026-11-11 the project owner selected one series string of eight LEDs. The Rev K and Rev H pair and its JLCPCB files are the historical 2×8 prototype reference. The existing valley-fill study remains historical evidence for that design family.
- The active stage is specification. Codex held the documentation write assignment. CAD and library write ownership for 8S will be assigned with the next bounded task. The project owner decides stage acceptance or delegation.

## Active task

- [E27-8S-SPEC task contract](8s/task-contract.md) and [current specification packet](8s/stage-packet.md). The candidate uses one isolated current-regulated output and targets one power PCB.
- [Requirements check](8s/requirements-check.json) reports the fabrication and assembly process review as open. [Proposed JLCPCB process](8s/profile-proposal.md) records the available service choices and the information still needed.
- The cold electrical envelope and connector mapping must be agreed before schematic work. Bench measurements, board-specific process evidence and qualification are separate downstream work. [Specification and test plan](8s/specification.md)
- [Output protection and cold-start study](8s/output-protection-study.md) records the calculated eFuse window and the contact-side discharge and insertion tests for OPEN-CC.
