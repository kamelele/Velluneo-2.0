# Consolidated specification readiness and design responsibility

VEL-SPEC-READINESS-01 r2, 2026-11-14. Preliminary review package; specification stage remains open. Input product packet revision 9, commit 2ef2b41108f5fe334be4c28f32f8fa52a7eb8188, blob 1963181ebe95987158387b6d1ebd70d7cb05e928, at hardware/E27/workflow/specification-reset/requirements-and-plan.md. Owner decisions are in the original conversation; this document creates no new approval.

## Responsibility and authority

The owner explicitly does not appoint an outside electronics reviewer before fabrication. This is not a prerequisite to begin/continue design. The coordinator prepares the design, calculations, library/pin checks, CAD and actual verification records; distinct read-only agent contexts perform the four toolkit reviews. Owner stage decisions remain required. Review contexts are not represented as licensed human engineers, certification bodies or physical laboratories. Test personnel, safe setup, instrument capability and stop conditions are established before the affected physical test, not demanded as an external appointment at project start.

No guarantee of physical safety/function is inferred from these assignments. Conversely, no missing external reviewer is used as an invented reason to stop ordinary design work. Actual missing technical inputs/checks, not an unnecessary appointment, govern readiness.

## One packet to inspect

- requirements-and-plan.md: current product brief, confirmed values, proposals and owner-decision history.
- requirements.json: first machine-readable traceability draft, 20 product requirements plus one specification-completeness requirement, three subsystems and 17 partly open technical/planning questions.
- hardware.json: isolated draft profile for this reset. JLCPCB/supplier are owner preferences; service, stackup, copper, finish and process confirmation remain null. KiCad 10.0.6 is the toolkit-supported proposal, not a migration of old CAD. There are no CAD source files, pin graphs or spatial contracts yet.
- preflight-output.json: actual source-validator result, not an installed-toolchain or CAD pass.
- led-study/: previous calculations, lifecycle correction, sourcing observations and unsent supplier questionnaire. Their stated scopes and hashes remain important; a review of an older packet does not silently cover changed inputs.

The machine contract is deliberately coarse: subsystem allocations and acceptance text are planning traceability, not exact circuit/interface implementation. Performance checks are due later; no physical evidence is invented. There are no electrical/mechanical endpoint records yet, explicitly pending U09/U10. Do not treat the empty interface list as proof that the lamp has no interfaces. No hardware configuration is applied.

## Actual toolkit preflight

Verified source toolkit manifest: 05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822, package 0.7.1-preview.3 / ruleset 0.7.1. The supplied tree passed verify-tree earlier. Executed from that separate source tree:

`python scripts/pcb_rules.py requirements SPEC_RESET_DIRECTORY --stage specification`

The exact local directory was /workspace/scratch/d4c1ae92033a/spec-contract, an isolated staging mirror of this documentation directory. No existing KiCad sources or project configurations were touched. Source validator identity in the report is standalone-candidate. This is a requirements preflight, not use of an installed project launcher. Trusted installable archive/digest, launcher lock and doctor remain pending before CAD. Do not misreport this run as completing those steps.

Result: exit 1, passed=false, no configuration_error. The contract was parsed and produced 21 matrix rows and 17 open questions; eight current specification findings remain. This is incompleteness, not a tool failure or a passed gate.

| Finding | Actual remaining scope |
|---|---|
| U01 | Supply screening range/basis and optical measurement conditions; accepted brightness and CRI are not being reopened. |
| U02 | Lifetime evidence/sample/failure treatment; 15,000 h L70 and 50 replacement cycles are already accepted. Do not infer a production population guarantee from one prototype. |
| U03 | Feasible fabrication/assembly profile. External human appointment is explicitly not a blocker; test personnel belong before tests. |
| U04 | Product safety/EMC/flicker assessment and exact demonstration/qualification scope. |
| U14 | CCT and optical/distribution/appearance acceptance conditions and sample plan. |
| U15 | Fixture/ventilation test definition and thermal worst-case orientation; 10–40°C/all positions are accepted. |
| U16 | Safe-access, operating/fault behavior and technical acceptance basis before circuit implementation. No nominal voltage is a safety certificate. |
| R-SPEC-PACKET | Review evidence for the complete current contract is absent. This file and past reviews alone do not close it. |

Any future change to requirement text, unknowns or methods changes the intent digest; refresh affected evidence/reviews. U17 bookings now block release/before affected execution rather than specification. U15 requires an early conditions/analysis plan; measured worst-case confirmation remains due later. U12/U17 before-test timing cannot be enforced by this stage-only requirements validator: retain a separate test-readiness/authorization check before every physical test, regardless of stage-check status.

The source-validator report is an observation of this draft, not evidence for its own completeness. No evidence records claim that measurements or supplier acceptance occurred.

## Standards research — scope assessment still required

Official IEC summaries checked 2026-11-14 identify IEC 62031:2026 (LED-module safety; supersedes 2018) at https://webstore.iec.ch/en/publication/92035 and IEC 60598-1:2024 (luminaire safety; supersedes 2020) at https://webstore.iec.ch/en/publication/66620 . The former expressly distinguishes LED modules from LED lamps; the latter includes semi-luminaire requirements. These are scope leads for the user-replaceable construction, not a determination that either alone governs Velluneo. Do not classify by E27 cap alone or inherit a historical clause/spacing limit.

Full applicable text, exact product classification and relevant EN/Polish adoption/harmonization status have not been assessed here. No conformity, CE, numerical safety limit or legal conclusion is claimed. This public-summary lookup cannot resolve U04/U16 or replace calculations and tests. Keep the specific lack of technical source evidence explicit without inventing a requirement for an outside person at project start.

## Next bounded work

Coordinator: prepare concrete proposed optical/environment/test acceptance and the safety/interface assessment; finish the controller/transformer and first-colour process feasibility comparisons; split mixed planning unknowns by the gate that genuinely needs them. Preserve accepted owner decisions while closing only the remaining technical parts.

Then freeze the complete specification candidate, rerun the traceability check with genuine evidence, refresh all four role reviews and present a concise owner decision packet. Do not ask the non-expert owner to certify a mains circuit; their decision concerns the desired behavior and the reviewed stage packet. Schematic work is not authorized by this incomplete draft. No source/manufacturing order, supplier message, physical test or product certification is performed by creating these records.

## Revision 2 synchronization

requirements-and-plan.md r10 updates the historical CLI-status statement and aligns U08/U15/U17 with the corrected contract. Product performance and owner decisions are unchanged. The machine contract remains a draft with no evidence or approvals and an incomplete specification result. The r9 commit remains the interview baseline; r10 corrections are the current planning-state synchronization, not a new owner approval.

## Interview update: guarded base and prototype scope

Packet r11/contract draft3 record the separate base cover, minimum one-colour complete prototype at the unchanged deadline, three colours as a stretch goal, and reference-lamp distribution without cap-direction emission. Preflight is refreshed; old reviews cover their recorded snapshots and require affected updates before formal acceptance. The stage-only checker does not qualify different product-family configurations: finalize scope-specific prototype/family evidence before release and do not treat one panel as proof of three-colour matching. No complete stage approval or physical evidence is claimed.
