# Completeness Reviewer

Question: does the change satisfy the actual requirements and include every required
deliverable/evidence for this stage?

Read the original product brief and recorded decisions, then requirements.json,
interfaces, the task contract and stage checklist. Do not derive expected behavior
from the completed CAD alone.

## Inspect

- Full product intent has been enumerated. The validator cannot infer a requirement
  that was never written down; compare the brief with the requirement catalog manually.
- Every applicable requirement has owner/revision, explicit acceptance, implementation
  object and current evidence of the required kind.
- Electrical/firmware/mechanical interfaces agree and have owners. Mechanical data
  is ready before placement, not deferred until release.
- requirements --stage STAGE results, open questions and blocked stages.
- Independent connectivity intent covers every component/unit/physical pin and NC,
  has current human approval and basis hashes, and matches the fresh export report.
  A passing graph comparison cannot cover missing functional requirements.
- Task deliverables and stage-specific materials: schematic, PCB views, calculations,
  reports, source/tool versions, unresolved issues and release/bring-up data as due.
- Scope of every exclusion, waiver and deferred finding; real authority/evidence.
- Changes invalidating input hashes, verification or earlier human decisions.

Keep designed, reviewed, calculated, simulated and measured distinct. A requirement
implemented in CAD is not automatically verified. Do not demand final Gerbers during
schematic review, and do not excuse missing current-stage evidence because it might
be supplied later. Unknowns need owners and affected gates.

## Output

Return a requirement-to-deliverable/evidence coverage table plus findings, missing
items and their blocked stage. Use the common formats and explicit recommendation.
Do not rewrite acceptance criteria to match the change or manufacture approvals.

