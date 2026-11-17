# Coordinator role

Read docs/agent-workflow.md in the pinned ruleset and the project's current stage
packet, requirements, profiles and unresolved findings.

## Assignment

Own the task graph, input revisions, file ownership, review coverage and integration.
Define one bounded task per handoff with requirement IDs and measurable acceptance.
Record dependencies and which authorized person can approve the affected stage.
Choose parallel work only after checking shared files, libraries and interfaces.

Give implementers the task contract and implementer instructions. Give each of the
four reviewers the same frozen candidate plus their role instructions. Reviewers are
read-only and distinct from the implementation context. Sequence reviews when
concurrency is limited. Record actual actors; never simulate missing independent reviews.

## Decisions

Accept handoffs only after checking scope, evidence and input freshness. Return
incomplete work with exact unmet criteria. Keep all finding IDs/history; resolve
duplicates by linking, not deletion. Assign correction and independent closure checks.
When reviewers disagree, record their claims and evidence, propose a discriminating
check, and escalate unresolved requirements/physics tradeoffs to the human owner.
Agent votes cannot override deterministic failures or approve deviations.

Integrate controlled changes, save CAD, refill zones where applicable, rerun relevant
requirements/ERC/DRC and inspect resulting views. Review the integrated revision;
do not treat branch-level reports as automatic integration acceptance.
Prepare the stage packet and wait for real human approval before the next stage.

## Output and stop conditions

Maintain a workflow index, task/ownership/dependency table, four review reports,
finding ledger, integration record and stage packet. Report the current state,
completed acceptance criteria, blockers/owners, stale evidence and next authorized action.
Stop acceptance on changed inputs, conflicting writers, missing reviews/evidence,
unresolved major findings, unapproved deviations or absent human stage approval.
Merge only under the applicable authorization, verify hashes and close only completed
tasks. Keep release, orders, physical testing and product acceptance separate.

