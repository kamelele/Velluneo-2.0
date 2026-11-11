# E27 workflow index

## Toolkit and tools

- Workflow reference [pcb-agent-toolkit 0.7.1 at commit 86614c3](https://github.com/wiktor426/pcb-agent-toolkit/tree/86614c3b9b43713031e0ea481edbe26b71cd1b8f). Use the toolkit checkout outside the Velluneo source tree. Start with the existing-project guide and the project instructions in that revision.
- The toolkit's tree verification passed against the files archived from the exact Git commit. Manifest SHA-256 is `05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822`. It is a candidate. Installed launcher and archive lock are pending.
- The historical E27 checks used KiCad 10.0.8. The local CLI reports 10.0.8 and its bundled Python reports 3.11.5. The toolkit validates KiCad 10.0.6 with its matching pcbnew Python. Verify a compatible environment and run doctor before using toolkit CAD checks. Record any proposed CAD-version migration as a separate task.

## Baseline and ownership

- Existing CAD baseline [239eeee](https://github.com/kamelele/Velluneo-2.0/commit/239eeee4522100944dae18d29fecb506b6db07f1). The existing [prototype handoff](../Pakiet_prototypu_JLCPCB.md) uses [power Rev K](../outputs/Zasilacz_RevK_Moc/README.md) and [control Rev H](../outputs/Zasilacz_RevH_Sterowanie/README.md). [Rev L valley-fill](../outputs/Studium_RevL_ValleyFill/README.md) is a development study. Historical reports are baseline evidence.
- Current task is workflow adoption for the existing E27 power supply and control. Coordinator and writer for the adoption documents is Codex. The write scope is `AGENTS.md` and this index. CAD and library ownership has not been assigned for the next task.
- The project owner is the authority for stage decisions and any delegation. A toolkit stage packet, a stage decision bound to that packet, and the four review reports are pending. The existing LED specification remains the basis for this adoption. A one-string driver is a design proposal discussed separately.

## Next task

- Reconcile the product requirements and the 26 V interface against the existing specification. Prepare separate board records for the prototype pair and document independently sourced connectivity intent and unresolved inputs. Keep the LED insert and mechanical design outside this task. Record any mechanical constraints needed by the electrical design as inputs to confirm.
- Review fabrication and assembly with the project owner. JLCPCB is the selected supplier. The exact stackup, panel and mounting plan remain to be confirmed. The toolkit JLCPCB profile proposes a 0.20 mm track width and 0.30 mm hole preference. The control prototype has tracks down to 0.18 mm and vias down to 0.20 mm. Map these differences and the existing mains isolation rules before proposing any KiCad configuration change.
- Acceptance evidence includes the current tool and source revisions, requirements and open questions, the profile comparison, a configuration preview once the environment is ready, and a stage packet with actual review coverage. [Toolkit workflow](https://github.com/wiktor426/pcb-agent-toolkit/blob/86614c3b9b43713031e0ea481edbe26b71cd1b8f/docs/agent-workflow.md) · [Existing-project guide](https://github.com/wiktor426/pcb-agent-toolkit/blob/86614c3b9b43713031e0ea481edbe26b71cd1b8f/docs/existing-projects.md)
