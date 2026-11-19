# IS-SPEC-01 task contract

Stage: specification, draft IS-1. Parent: current user request, 2026-11-19.
Coordinator/writer: /root. Research implementer: /root/driver_research, read-only.
Human reviewer: Kamil, project owner; no stage approval recorded.
Base commit: 377fc0a08e74043e255b732f7c2beb63134a3576.
Toolkit: 0.7.1-preview.3, ruleset 0.7.1, manifest 05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822.
Normalized archive 15a2789b06afb014f9dc166ce6da01a903c3b422b5c1b37b2a96581b218784b4 reproduces the prior verified lock.
KiCad: 10.0.6 CLI and matching pcbnew; historical CAD is not converted.

Goal: derive a reviewable separate driver specification, research alternatives and identify blocking inputs. Requirement IDs REQ-SCOPE through REQ-COST are defined in requirements.json.
Non-goals: schematic capture, final pin graph, enclosure design, placement/routing, manufacturing, orders, mains testing and remote publication.
Write lease: /root exclusively owns hardware/E27/variants/integrated-shade/** and hardware/E27/workflow/integrated-shade/** for this task. Toolkit installer owns .pcb-toolkit/** and pcb-toolkit.py locally. Reviewers are read-only and return reports to the coordinator.
Acceptance: sources and operating-point calculations are explicit; requirement checker produces a fresh report with all open gates; four real read-only reviews inspect a frozen input; exact bytes and unresolved findings remain visible. A failing gate is not relabelled as passed.
Stop: do not start schematic capture without full selected-part data, independent intent and actual relevant human approvals. Do not use surrogate pin/MPN guesses, loosen checks or claim measurements.
No user budget or deadline assigned. Handoff: stage-packet.md and actual check/review artifacts in this directory.
