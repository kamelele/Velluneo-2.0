# Safe configuration adoption and recovery

Use Python 3.11+ and the project's pinned KiCad 10.0.6. Work on a local copy of an
existing project. Close KiCad and other editors before apply or rollback; the tool
locks its own operations, not unrelated editors. Keep the ruleset outside board sources.

## Prepare and preview

For new projects use init. For an existing project, create hardware.json from the
template and fill its basename, selected profiles and source_files. Do not run init
against an existing board. Requirements may remain incomplete for work mode, but
release remains blocked until complete and approved.

    python scripts/pcb_rules.py configure PROJECT

The command prints a PLAN_ID and writes .work/configure/plans/PLAN_ID.json and .diff.
No project source is changed. The JSON lists managed fields and conflicts. The diff
shows complete proposed file changes, including possible JSON formatting differences.
Review both. Preserve local settings and resolve each policy conflict deliberately;
incorporate justified stricter limits into hardware.json and preview again. Never
clear exclusions or change pin types solely to pass adoption.

Only rule minima, selected severities, the ERC pin matrix, generated netclass
clearance/track width and the complete assignment-pattern list are managed. Existing
classes retain other attributes; additional classes must satisfy the default floors.
Assignments with incompatible existing lists or multiple wildcard patterns are
refused rather than merged by guessing. Unsupported structures and duplicate names
also block adoption. Unrelated JSON is preserved semantically; if no JSON value
changes, the original project-file bytes are retained.

Supported custom-rule files: absent, zero bytes, exact generated rules (including
legacy Windows line endings), or an unchanged file previously owned by the tool.
Unfamiliar rules and existing nonempty exclusion lists are preserved and block
automatic adoption. Migration of arbitrary scoped rules is outside this version.

## Apply and check

    python scripts/pcb_rules.py configure PROJECT --apply PLAN_ID
    python scripts/pcb_rules.py check PROJECT --mode work

Apply requires the saved plan to match a freshly recomputed proposal, including source
bytes, missing files, hardware.json, ownership state, templates, profiles and tool code.
Any change requires another preview. No force/overwrite option exists. Applying a plan
is not a human stage approval and cannot waive findings.

Changed files get verified backups before replacement. The command prints a
TRANSACTION_ID. Each replacement is atomic; the multi-file operation uses a recovery
journal rather than claiming whole-operation filesystem atomicity. Keep .work locally
for rollback and exclude it from publication. No-op apply writes no source bytes.
Reusing an old pre-apply plan is stale: preview again, then apply the no-op plan.

Commit .electronics-rules/config-state.json with project sources. It records previous
managed values and is included in source snapshots automatically. It is provenance,
not authorization. The checker independently validates actual policy even if state
is edited. Configuration changes invalidate previous approval snapshots.

## Rollback and interrupted updates

    python scripts/pcb_rules.py configure PROJECT --rollback TRANSACTION_ID

Rollback verifies backups and current post-update hashes before restoring original
bytes. Files introduced by the transaction are removed. Intervening user edits cause
refusal; save those edits separately and resolve them before retrying. Do not delete
backups or fabricate a journal to bypass refusal.

An interrupted update blocks further apply operations. The error names the pending
transaction; use rollback to recover. Recovery accepts original or proposed hashes,
accounting for a partially completed write. Tool locks are released by the operating
system after a process exits. An interrupted rollback can be retried. If backups are
lost or files were independently modified, restore from a known Git revision or
verified external backup; automatic recovery cannot reconstruct missing originals.

After rollback rerun work checks and assess the affected reviews. Baseline work checks
can report actual ERC/DRC alongside configuration conflicts where sources are complete.
A baseline with errors is never a passing adoption or release result.
