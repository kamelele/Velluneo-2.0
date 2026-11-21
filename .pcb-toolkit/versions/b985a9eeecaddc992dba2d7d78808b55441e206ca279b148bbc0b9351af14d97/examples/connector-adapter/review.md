# Authored coordinator and four-reviewer walkthrough

Mode: worked teaching example with actual CAD checks. Actors: one author writing
all role perspectives; zero independently launched agents, zero real human approvals,
zero prototypes/measurements. A passing script verifies the declared cases, not review
independence. Real projects must use actual actors and stage decisions.

## Coordinator task and ownership

Task ADAPTER-1 implements REQ-SCOPE, REQ-PINS and REQ-GEOMETRY in the original board.
Frozen inputs: specification.md and independent intended-connectivity.json, whose
hashes are in every replay's result.json. One implementer owns board CAD and local
libraries; reviewers are read-only. Profile/intent approval scope is demonstration only.
No task authorizes process confirmation, stage approval, rule relaxation or ordering.

Acceptance: J1.1 -> J2.1 and J1.2 -> J2.2, no cross-connection; correct schematic/PCB
parity, no work ERC/DRC findings; release remains blocked. Handoff contains source
hashes/snapshot, CAD views, calculation, BOM, actual reports and open questions.

## Four review perspectives on the introduced defect

| Role | Independent question / review action in a real task | Tutorial finding/evidence |
|---|---|---|
| Reality Checker | Compare physical connector numbering, actual mating part and expected behavior against the specification, beyond ERC | F-01: J2 physical pins are swapped. Actual connectivity report contains split_net/merged_nets despite zero ERC findings. Generic parts/fit and bench operation remain unverified. |
| Overengineering Reviewer | Check whether a passive adapter needs active circuitry or a reusable module; compare cost, risk and shared-function benefit | No active electronics justified by this scope. Keep two direct tracks. Do not introduce a shared abstraction or reference-library qualification based on one tutorial. |
| Completeness Reviewer | Map every requirement to implementation, evidence and unresolved items | REQ-PINS fails before correction. REQ-SCOPE/GEOMETRY have authored review/calculation and CAD evidence only. Actual parts, process, approvals, measurements and manufacturing package remain release blockers. |
| Change Reviewer | Inspect the exact schematic diff, parity, libraries, net identities and stale evidence | Pin swap changes topology without a pin-type change. Restore endpoints, keep the independent expectation unchanged, then rerun fresh connectivity/ERC/DRC. Do not approve an old snapshot. |

F-01 is a blocking topology error owned by the CAD implementer, scoped to REQ-PINS and
J2 pins 1/2. Reproduce via replay.py; inspect .work/defect-connectivity.json. It is not
an accepted exception. The tutorial never loosens rules or changes pin electrical
types to make ERC green: connector pins are passive in both cases.

## Correction, closure and handoff

The replay restores the committed straight-through schematic bytes, then runs a fresh
full check at routing stage, including requirements, spatial geometry, intended
connectivity, native ERC and DRC with schematic parity. Corrected-work.json must have
passed=true and no ERC/DRC findings. Result.json records its source snapshot and
original inputs; reviewers of a real change would independently verify closure against
that snapshot. The script assertion is not an independent review signature.

The coordinator's final packet contains specification/profile proposals, schematic and
PCB views, calculations/BOM, defect and correction reports, all four perspectives,
bring-up plan and the unresolved items below. State: READY FOR ASSIGNED HUMAN REVIEW,
NOT APPROVED FOR RELEASE. A real flow waits after each specification, schematic,
placement, routing and release packet. The tutorial executes fixture checks across
stages without pretending that those human gates occurred.

## Open questions and release packet gap

- Product owner: real scope, safety/environment applicability and review authority.
- Component owner: actual connector part/datasheet, physical pin numbering, fit,
  retention, footprint tolerances and orientation marking.
- Process owner: actual fabrication service/stackup/copper/finish and assembly,
  stencil/inspection requirements. Candidate preferences are not order confirmation.
- Reviewers: genuine approvals and fresh evidence for the exact source snapshot.
- Release owner: approved consistent Gerber/drill/BOM/assembly artifacts and checks.
  This tutorial intentionally does not provide a manufacturing release package.
- Test owner: approved bench setup/acceptance limits and actual bring-up measurements.

Blocked-release.json must retain process and approval findings; fixing F-01 does not
resolve these questions. For deviations, use a rule/object-specific record with actual
reason/approval; do not waive the tutorial defect. For shared changes or non-confidential
bug reports, follow ../../docs/contributing.md.
