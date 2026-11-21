# Pinned vendored installation

The initial method is offline archive vendoring into the project repository. Obtain
the exact candidate/release archive and its trusted checksum through the review/release
channel. Runtime commands never fetch latest or contact a repository. The main private
development repository remains canonical; public consumers use reviewed exported versions.

## First installation

Extract/verify the toolkit separately, create or select your project repository, then:

```sh
python TOOLKIT/scripts/toolkit_install.py install PROJECT_REPO --archive TOOLKIT.zip --sha256 EXPECTED_SHA256 --allow-candidate
```

The first published preview retains the tested candidate archive format, so --allow-candidate
is mandatory. It accepts use of that exact candidate, not design-stage/manufacturing
approval or authority to publish the private development repository. Exported material
uses the licenses in LICENSE and THIRD_PARTY_NOTICES.md; retain applicable NOTICE
attribution when redistributing it. Public release-format support
is coordinated separately.
Do not select the extracted toolkit directory itself as PROJECT_REPO.

The installer creates only its owned .pcb-toolkit namespace and pcb-toolkit.py launcher.
The selected immutable dependency is under .pcb-toolkit/versions/MANIFEST_SHA256.
The lock records exact archive/manifest hashes, package/ruleset version, candidate
status and KiCad version. The source-content revision is the manifest digest; it is
not presented as an invented Git commit. Public Git/tag provenance belongs to release
metadata when available. Commit the launcher, lock/history and selected version files.
Generated work/reports/caches are ignored; old dependency versions remain for rollback.
Existing unrelated launchers/namespaces are preserved and block automatic installation.

From PROJECT_REPO:

```sh
python pcb-toolkit.py status
python pcb-toolkit.py doctor
python pcb-toolkit.py run init boards/my_board --vendor jlcpcb --assembly inhouse
python pcb-toolkit.py run requirements boards/my_board --stage specification
python pcb-toolkit.py run configure boards/my_board
python pcb-toolkit.py run check boards/my_board --mode work --stage specification
```

For an existing project, use its actual relative directory instead of init and follow
[safe configuration adoption](configuration-adoption.md). Root-level CAD is supported
with project path dot. Do not put design source_files inside .pcb-toolkit: it is
reserved for tooling, and packaged examples are excluded from board input discovery.
Specify all genuine local sheet/library inputs as before.

The launcher checks pinned manifest/file bytes before importing toolkit code, takes a
project usage lock and selects only that version. Missing/tampered files, an edited
launcher or an unsupported lock fail closed. Use the launcher rather than directly
executing a backend from another checkout. Ordinary private-source development remains
available for projects without an installed lock.

## Environment and reports

Doctor checks Python 3.11+, exact KiCad CLI and matching pcbnew, supported x64 Windows
or headless Ubuntu 26.10, and private per-project .work configuration/documents paths.
KICAD_CLI/KICAD_PYTHON select nonstandard local tool locations; doctor also accepts
--kicad-cli and --cad-python. Paths are reported locally, not stored as portable pins.
Doctor does not install software or qualify untested OS/tool releases. Other platforms
need separate validation. Candidate/source verification works without private access.

Doctor writes .work/toolkit-doctor.json. Dispatch writes .work/toolkit-run.json and
preserves backend reports. Exit 0 is success, 1 is project findings/incompleteness,
2 is configuration/tool failure. Integrity errors may stop at the bootstrap with a
structured error and exit 2; a prior report is not current success. Backend snapshots,
configure plans and reports bind the exact installation/manifest identity and lock.

## Deliberate update and rollback

```sh
python pcb-toolkit.py plan-update NEW.zip --sha256 NEW_SHA256 --allow-candidate
python pcb-toolkit.py update --apply PLAN_ID
python pcb-toolkit.py doctor
python pcb-toolkit.py run configure boards/my_board
```

Inspect the package file/version diff and impact in .work/toolkit-updates before apply.
Only a current, unchanged plan/archive can activate. Reusing a version with different
contents is refused. A no-op preserves lock bytes. Activation changes the dependency
pointer atomically after verified extraction; old immutable files and the previous
lock are retained. Interrupted staging leaves work data and the old active pointer,
or a complete new pointer; never repair a corrupted cache by silently overwriting it.
An initial interrupted install with the exact ownership marker can be retried; unknown
state is preserved for explicit review. There is no automatic cache pruning.

Configuration migration is separate: review configure's diff, close KiCad and apply
its current plan explicitly. Tool updates never edit board sources, rules, approvals
or waivers automatically. Every affected board needs fresh checks/review; identity
changes invalidate snapshots and old configure plans. Pinning hashes does not authenticate
an approver or restore a physical test that never occurred.

```sh
python pcb-toolkit.py rollback --to PREVIOUS_LOCK_SHA256
python pcb-toolkit.py doctor
python pcb-toolkit.py run check boards/my_board --mode work
```

Rollback verifies current/history/previous file integrity before restoring exact lock
bytes. It changes tooling only. Roll back CAD configuration separately using its own
transaction if needed, then recheck and renew affected human reviews. No stage or
manufacturing authorization follows from installing/updating/rolling back tools.

## CI

The manual workflow template under templates/project/.github/workflows validates the
committed pin, builds the pinned Ubuntu tool environment and runs doctor/work checks
without private authentication or runtime network access. Review/copy it deliberately;
init does not install workflows into an existing project. Set the real board path and
stage. Tool-image construction needs Ubuntu package access. Workflow-dispatch testing
is distinct from an actual hosted-run record; the local/container command trial is
recorded separately. Public fork/PR and release credentials remain the public workflow's
responsibility. See [version and support policy](version-policy.md).
