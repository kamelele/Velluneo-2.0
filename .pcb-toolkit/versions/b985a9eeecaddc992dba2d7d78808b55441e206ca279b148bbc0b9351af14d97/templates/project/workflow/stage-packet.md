# Stage packet — [packet ID and revision]

- Stage / parent issue / candidate PR: [references]
- Candidate commit / intent_digest / source snapshot kind and value: [actual inputs]
- KiCad / ruleset exact versions: [pins]
- Authorized human reviewer: [person assigned by user]
- Requirement/interface matrix: [report and hash]
- Four review reports: [role, actor, revision, report hash and recommendation]
- Findings ledger: [open, independently closed, approved deviations, deferred minor items]
- Stage materials: [schematic PDF, board/layer/3D views, calculations as due]
- Tool checks: [commands, results, report hashes; failures remain visible]
- Open questions: [owner, blocked stage, next evidence]
- Integration / invalidation record: [reference]
- Attachment manifest: [path, SHA256, source revision for each attachment]
- Proposed next action: [specific stage transition or continued correction]

## Human decision — leave empty until an actual decision exists

[Actual approver, decision link/text, timestamp and the exact packet/revision/snapshot
covered. Explicitly accepted deferrals/deviations and remaining limits. Agents must
not invent these values. Approval must be renewed if affected inputs change.]

Keep this packet outside its own source snapshot inputs to avoid hash cycles.
Design inputs and declared technical evidence remain source-tracked.

