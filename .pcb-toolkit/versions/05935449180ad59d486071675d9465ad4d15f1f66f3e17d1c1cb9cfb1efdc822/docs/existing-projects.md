# Existing projects and controlled updates

Start from a clean, committed backup and record the current CAD/tool/library versions,
custom rules, exclusions and approvals. Inventory conflicts before adopting templates.
Do not copy hardware.json or AGENTS.md over existing project files. Extract the trusted
toolkit separately and follow [installation](installation.md); the installer owns only
its reserved namespace/launcher and refuses unrecognized contents there.

1. Read the existing specification and rule rationale. Create missing contracts
   deliberately from templates; name missing requirements and their owners. Keep
   existing legitimate custom rules until an explicit mapping/review is complete.
2. Keep the existing project basename and list real sources in hardware.json. Select
   the four profile layers; obtain the genuine stage/process approvals needed for
   the intended scope. Tool installation is not approval to convert CAD versions.
3. Run doctor, requirements and configure preview. Review the exact JSON plan and
   .diff against your saved sources. Unknown custom rules block automatic adoption;
   resolve ownership/mapping explicitly without deleting them to bypass the refusal.
4. Close KiCad, apply the current plan, inspect the resulting diff and run actual
   connectivity/spatial/ERC/DRC checks. Reopen CAD and review views. Submit affected
   stage packets; do not carry an old approval forward as if inputs were unchanged.

Configuration preview/apply/recovery and its TRANSACTION_ID rollback are documented
in [configuration adoption](configuration-adoption.md). A stale preview must be
regenerated. Configuration rollback and toolkit-dependency rollback are different.

To update the dependency, use pcb-toolkit.py plan-update NEW.zip --sha256 NEW_SHA256
--allow-candidate; inspect old/new versions, file differences and review impact, then
update --apply PLAN_ID. Run doctor, preview/apply any separate configuration migration,
repeat checks and request affected reviews. Use rollback --to OLD_LOCK_SHA256 to
restore the previous dependency lock; this does not undo a separate CAD/configuration
edit or create approval for it. See installation.md for the full command sequence.

Do not repair modified cached dependencies in place, skip verification or fetch latest
automatically. Report corrupted/unknown ownership state and recover from the trusted
original package/backup through a reviewed procedure. Future incompatible toolkit or
KiCad migrations need separate instructions and validation.
