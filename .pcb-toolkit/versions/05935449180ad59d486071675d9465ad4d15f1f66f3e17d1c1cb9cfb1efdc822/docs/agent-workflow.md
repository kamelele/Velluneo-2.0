# Coordinated agent workflow for PCB projects

One coordinator owns the plan and integration. Implementers receive bounded tasks;
four review roles inspect evidence independently. An authorized person approves each
product stage. These instructions are framework-independent; they do not install or
implement an agent runtime, CAD adapter or access-control system.

## Read order and project setup

1. Product specification and recorded human decisions, then the project AGENTS.md.
2. hardware.json and the configured requirements document, including subsystem
   interfaces, requirement IDs, evidence and owned unknowns.
3. The exact pinned ruleset/KiCad versions, selected product/fabrication/assembly
   profiles and rules/catalog.json. Resolve this repository outside project sources.
4. Previous stage packet/approval, current source state and requirements/check reports.
5. The assigned task contract and role instructions in docs/roles/.

Create a short project workflow index listing coordinator, authorized human reviewers,
task/PR links, role assignments, current stage, dependencies and file ownership.
Assign reviewer people per project/task; do not hardcode a team member as final authority.
Only the user or their authorized delegate grants approval authority. An agent cannot
add itself to that list. Use English for repository artifacts.

New projects start with pcb_rules.py init. Existing projects follow
[safe adoption](configuration-adoption.md). Obtain missing requirements instead of
inventing product limits. The [requirements checker](product-requirements.md) runs
before CAD exists. Select and confirm the exact manufacturing/assembly process at
specification; its confirmation is separate from design approval.

## Responsibilities and authority

| Actor | Responsibility | May decide |
|---|---|---|
| Coordinator | Plan, task graph, source scope, review assignment, corrections, integration and stage packet | Accept a deliverable as ready for review; stop/escalate work |
| Implementer | Execute the task in its allowed files, provide changes and evidence | Implementation details within the agreed contract |
| Four review roles | Independent findings against the same input revision | Request corrections, identify blockers or recommend human review |
| Authorized human reviewer | Resolve product choices/deviations and approve stages | Approve/reject the specific evidence/revision and authorize later actions |

Review roles are Reality Checker, Overengineering Reviewer, Completeness Reviewer
and Change Reviewer. Each returns its own report. They need not run simultaneously.
Use a distinct review actor/context from the implementer; record role and actor IDs.
The same underlying model is not proof of independence. Require a separate inspection
of sources/criteria, rather than copying the author's conclusions or another review.
If independent review cannot be provided, report the gap and assign a human review;
do not impersonate unavailable reviewers or silently mark their work complete.

Agent recommendations, counts of agreeing agents and passing CAD do not grant human
approval. Keep native ERC/DRC, requirements, calculations and measurements authoritative
within their scope. A reviewer cannot waive a tool failure by opinion.

## Task loop

1. **Plan:** link the parent outcome and requirement IDs; choose a bounded stage/task.
   Record dependencies, acceptance criteria and unresolved inputs.
2. **Delegate:** issue the [task contract](../templates/project/workflow/task-contract.md),
   identify immutable inputs, allowed paths, outputs, checks and escalation conditions.
   Assign write ownership before editing.
3. **Execute:** implementer works on an isolated branch/worktree, records changes,
   calculations and uncertainty, runs relevant checks and returns a handoff.
4. **Review:** freeze the candidate and send the same source state to all four roles.
   Reviewers are read-only; each reports coverage, evidence, findings and a recommendation.
5. **Correct:** coordinator deduplicates related findings without discarding their IDs
   or reviewers, assigns fixes and requests targeted re-review. A conflicting review
   gets a resolution record and an owner; unresolved conflict is not accepted by voting.
6. **Integrate:** coordinator verifies allowed scope, incorporates approved corrections,
   refreshes libraries/zones where applicable and runs whole-project checks on the
   integrated result. Reviews of a branch are not automatically reviews of integration.
7. **Present:** create the [stage packet](../templates/project/workflow/stage-packet.md),
   including every review, tool results, views/calculations and open questions.
   Wait for explicit approval from an authorized human before starting the next stage.
8. **Merge/close:** after the applicable human acceptance and merge authorization,
   merge the PR, verify resulting source hashes, record the outcome in the issue and
   close only completed acceptance criteria. A rejected/closed PR does not complete
   the task. Merging within a stage does not itself advance the stage.

Suggested task states: planned → assigned → in_progress → awaiting_reviews →
changes_requested (loop) → integrated → awaiting_human_review → accepted → merged → closed.
Use blocked with an owner/reason when inputs, evidence or authority are missing.
These are documented states, not automatically enforced GitHub transitions.

## Task contract and handoff

At minimum record task ID/parent issue, stage, goal/non-goals, requirement/interface IDs,
input revision and hashes, dependencies/base commit, actor, writable paths and leases,
expected deliverables, acceptance checks, deadline/budget if assigned, escalation/stop
conditions and handoff location. Do not invent budgets or deadlines.

Before CAD exists, bind inputs with the requirements intent_digest, file hashes and
repository commit. Do not manufacture a full-source snapshot when required CAD files
do not yet exist. Once available, also record pcb_rules.py snapshot and exact tool/rule
versions. Inputs must be actual saved files; GUI-only edits are not reviewable state.

The handoff includes base/result revisions, changed files, requirement/object links,
commands and actual results, visual/calculation artifacts, known limitations and
remaining questions. Work outside the write scope, changed inputs, conflicting
ownership, unexplained findings or a missing prerequisite cause a return/escalation.
Completion of one task does not imply completion of its parent epic or stage.

## Concurrent CAD editing and integration

The coordinator keeps a write-ownership table: logical file/resource, task, actor,
base revision, lease status and dependent tasks. One active writer per shared CAD file,
including across branches. Separate worktrees prevent filesystem collisions but do
not make competing edits to the same board safe. Shared libraries, net assignments,
generated constraints and outlines also require explicit ownership.

Independent boards can be edited in parallel after their interface contracts agree.
Other agents can concurrently calculate, research and review read-only. Split schematic
sheets only when dependencies and common libraries are controlled. Do not split one
board into overlapping placement/routing writers. Release/reassign ownership explicitly
after a handoff; a suspended actor cannot resume an expired lease without reassignment.

Record whether a branch starts from main or another task. A dependency change requires
refreshing/rebasing the candidate, updating input hashes and rerunning affected checks.
Never resolve CAD conflicts with blind ours/theirs choices or textual edits whose
electrical/geometric meaning has not been checked. Reapply changes in the pinned tool
or return the conflict to its owner. Use the integration record template.

## Four reviews and finding resolution

Use [review reports](../templates/project/workflow/review-report.md) and
[findings](../templates/project/workflow/finding.md). Each finding identifies the exact
rule/requirement and object, problem, consequence, evidence type/location/revision,
severity, affected gate, correction owner and an observable closure condition.

| Severity | Consequence |
|---|---|
| blocker | Stop the affected operation/stage; resolve missing intent, unsafe assumptions or unusable verification before acceptance |
| major | Correct before task/stage acceptance; potentially wrong function, integration, manufacturability or testability |
| minor | Track with owner and due stage; human must explicitly accept any deferral crossing the current gate |
| note | Record useful information; cannot hide an unassessed defect or missing requirement |

These labels do not change CAD severity or waiver policy. Give uncertain findings an
explicit confidence/unknown statement; uncertainty is not a reason to close them.
Finding states: open → assigned → correction_submitted → verified_closed. Alternatives
are duplicate_of (link the surviving ID) or human_approved_deviation (link actual
authorization and the specific rule/object/snapshot). Keep history and original evidence.

The implementer may propose a fix, not mark its own finding independently verified.
The originating reviewer or another assigned independent reviewer checks the closure
condition on the corrected revision. Coordinator records disagreements and resolution
evidence. Escalate unresolved product/physics tradeoffs to the human owner; do not
choose the majority opinion or weaken global rules to obtain agreement.

A review reports ready_for_human_review, changes_requested, blocked or not_applicable.
The latter requires an exact scope/phase reason and coordinator review; it is not a
substitute for unavailable evidence. A role-specific ready result is not approval
of the complete project. Silence or an empty unscoped report is not a completed review.

## Stage packets and human gates

Use [review evidence](reviews.md) for mandatory materials at specification, schematic/
libraries, placement, routing and release. Include the appropriate requirements matrix,
all four review reports, resolved/deferred findings, actual tool results, schematic PDF,
PCB layer/3D views and calculations appropriate to the stage. Include open questions
even when they block only a later gate; never present them as confirmed capability.

Bind the packet to the candidate commit, intent/source snapshot, ruleset/tool versions
and attachment hashes. Keep stage packets, review state and human-approval records
as lifecycle metadata, separate from source snapshot inputs if they reference that
snapshot; otherwise self-referencing hashes become impossible. Genuine design inputs
such as requirements, libraries, calculations and declared technical evidence still
belong in source tracking under the project contract.

Human approval references the specific packet/revision, approver and actual decision
link/text. In hardware.json record genuine approved_by/evidence/snapshot values for
the existing checker once a complete source snapshot exists. Pre-CAD approval can bind
intent/input hashes in the stage packet; the final release must obtain genuine human
confirmation covering final snapshots. Do not silently carry forward or rewrite prior
approvals to a new hash. Packet/attachment checks remain procedural in this release;
the CLI does not authenticate a human or enforce this entire workflow.

Changing sources, requirements, libraries, rules or zones requires an impact record:
which reviews/checks are stale, which need repetition and why. Unaffected reviews may
be referenced only with explicit scope/evidence; the final packet must cover the
integrated revision. Recompute after merge; differing hashes require renewed review.
Passing requirements/DRC does not override stale human acceptance.

## Bring-up and product integration

Release delivers matched Gerbers, drills, BOM/DNP, positions/rotations, assembly data,
reports and the [bring-up plan](../templates/project/workflow/bringup-plan.md).
Keep manufacturing release, ordering authorization, receipt, first power-on and final
product acceptance distinct. Do not order or upload to a supplier without authorization.

Before prototype testing, record hardware/enclosure/firmware revisions, serial/sample
identity, instrumentation, expected values, limits/stop conditions, programming and
test access and the responsible human. Unknown limits block that test rather than
receiving defaults. Capture actual measurements; agents may analyze records but cannot
invent physical operations or results. Integrate cabling/pinout, mechanical fit,
firmware version/configuration, normal operation, startup and fault behavior.

Log defects as linked issues with requirement/object, conditions, reproduction,
evidence, affected revisions and next verification. Rework or ECO invalidates relevant
evidence and returns through review. An operating prototype is not proof that every
EMC/safety/environmental or production requirement is met.

## Adoption and validation scope

Project templates live under templates/project/workflow and templates/project/.github.
Copy deliberately into an existing repository after reviewing conflicts; do not
overwrite its issue forms or AGENTS.md blindly. init currently copies the project
AGENTS.md, not this entire workflow package. Resolve role instructions in the pinned
ruleset dependency; packaging/installation is addressed in #17/#18.

The [synthetic walkthrough](../examples/agent-workflow/README.md) exercises the procedure
and existing requirements checks. It is not an actual multi-agent CAD run or human
approval. The real second-person/end-to-end pilot remains #20. Independent
[intended-versus-actual connectivity](intended-connectivity.md) is now checked against
a fresh schematic export. [Shared spatial constraints](spatial-constraints.md) add
declared adapter inputs, native area/outline verification and scoped DRC; they do not
install a planner/router or replace topology and human reviews. #20 remains the real pilot.
