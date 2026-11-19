# IS-SPEC-01 — final local review packet, IS-1.1

Status: incomplete specification draft for owner discussion. Specification acceptance is BLOCKED. No schematic, placement, routing or release stage has started.

Base commit: 377fc0a08e74043e255b732f7c2beb63134a3576. Local branch: concept/integrated-shade-nonisolated-buck. Remote branch/commit/PR: none.
Final pre-CAD manifest: f847fe676df47340d9db14cc0fbb9152f0499d8d52aeb1f1c6b44885876a9170 (review-inputs-final.json, nine files).
Final requirements intent digest: 433890302af29f01e4a59a65cc84f1bdc9487df48b70ec6962de2aabd83bfa80.
Toolkit 0.7.1-preview.3, ruleset 0.7.1, manifest 05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822, archive 15a2789b06afb014f9dc166ce6da01a903c3b422b5c1b37b2a96581b218784b4. KiCad CLI/pcbnew 10.0.6; doctor passed. No historical CAD conversion.

## Candidate and results

Integrated diffuser/LED module; electronics mainly in base; ~800lm; no dimming; free LED voltage/count. Compare protected non-isolated constant-current buck candidates, without committing to an unsupported IC. BP2863XJ needs full data and sourcing; HV9961-based fallback needs external protection design. Ideal current/voltage arithmetic is verified. Actual operating point, reservoir/EMI strategy, LED selection, cost, dimensions, performance and compliance remain unproven.

40x25mm is only a potential placement experiment. No final board-size claim or manufacturing data exists. Fully detailed references and limits are in the variant README and sources.json.

## Actual checks

- Toolkit source verification and normalized archive reproduction: passed, exact prior lock identity.
- Pinned launcher doctor: exit0, passed; toolkit-doctor.json.
- requirements --stage specification: exit1, passed:false; requirements-check-final.json. REQ-SCOPE and narrowly defined REQ-POWER evidence verified; remaining current errors are OPEN-PROCESS and missing REQ-PROCESS review.
- Historical tracked baseline diff against base: empty. New variant/lifecycle only. Local toolkit/runtime excluded from publication scope.
- Fresh final source-byte hash verification: passed. No ERC/DRC/netlist/spatial checks applicable to this no-CAD draft. No measurements or simulation performed.

## Four actual reviews

- Reality /root/driver_research: final nine hashes verified and calculations recomputed; blocked for specification acceptance. Research/technical-review actor overlap disclosed.
- Overengineering /root/review_simplicity: IS-1.1 seven hashes verified; ready_for_human_review for draft only. OE-01..03 retained. Evidence-only registration does not change its technical scope.
- Completeness /root/review_completeness: IS-1.1 seven hashes verified; four omissions independently verified closed at requirement-definition level; blocked for spec acceptance. Actual unknown inputs remain open. Evidence-only registration checked by final reality/change reviews.
- Change /root/review_change: final nine hashes verified; ready_for_human_review for incomplete draft only; fresh report note closed, publication allowlist remains mandatory.

Reports are coordinator transcriptions of actual returned agent reports, with actor identities and scoped findings preserved. They are not claimed as human approvals or physical certifications. Full state in findings.json and integration-record.json.

## Decisions and remaining inputs

Only a real owner decision against a specific process proposal can close OPEN-PROCESS. Proposed planning route: JLCPCB FR-4 2 layers, 1oz, nominal1.6mm, lead-free HASL; evaluate Standard PCBA with a later evidence-based Economic alternative if suitable. Specific order stackup/material, panel/rails and assembly scope still need verification. No process approval has been inferred from permission to investigate.

Before schematic acceptance: confirmed market/range, first optical/CCT/CRI target, environment/thermal/lifetime limits, selected full-data/procurable parts, actual LED envelope, standards/classification/fault limits and structured electrical interface. Independently reviewed physical pin intent and actual human acceptance precede schematic generation. Geometry/accessibility/interface constraints precede placement. Final qualification requires actual measurements.

## Proposed next actions

Present this exact local packet for permission to save its explicitly incomplete documentation on the separate remote branch, with main untouched. This permission is separate from specification acceptance. Continue resolving specification choices and calculations; no automatic advancement into capture/placement/manufacturing. Use publication-plan.json exact allowlist and recheck base/source freshness immediately before any approved remote write.

## Human decision

No owner approval of this packet, process or stage has yet been recorded. Do not fill this section without the actual decision and its exact scope.

Attachment hashes are in packet-attachments.json, outside the nine-file technical input manifest; the attachment manifest excludes itself to avoid a self-hash cycle.
