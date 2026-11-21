# Project workflow index

- Product / current stage / pinned ruleset and KiCad: [actual values]
- Coordinator actor: [ID]
- Authorized human reviewers and scope: [actual user/delegate decision references]
- Requirements/interfaces and current intent/source snapshot: [references]
- Stage packet / latest actual human decision: [references or explicitly pending]
- Task/PR dependency graph: [parents, bases and blocked tasks]

## Write ownership

| Logical file/resource | Task/actor | Base revision | Lease state | Dependencies |
|---|---|---|---|---|
| [path] | [task / actor] | [SHA] | [active / released / revoked] | [tasks] |

One active writer per shared CAD file, including separate branches. Reviews are read-only.

## Task/review status

| Task | Stage/state | Implementer | Four review actors/reports | Findings | Next owner/action |
|---|---|---|---|---|---|
| [ID] | [stage / state] | [actor] | [references] | [IDs] | [owner / action] |

Keep open questions, invalidation decisions, integration records, human approvals and
bring-up defects linked here. This index is lifecycle metadata, not its own snapshot
input or a source of invented authority.
