# Original connector adapter — complete tutorial source set

This small, original passive board teaches the workflow. It is not a qualified product,
manufacturer reference design or production release. Sources have no customer lineage.
All approval-like records are labelled synthetic; hardware.json has no real stage
approvals, waivers or release artifacts. No actual agents or independent humans are
claimed. The real participant/agent pilot is a separate activity.

Start with [specification](board/specification.md), [review walkthrough](review.md),
[schematic view](views/schematic.svg) and [PCB copper view](views/pcb.svg).
Editable sources are under board/: board.kicad_pro / .kicad_sch / .kicad_pcb / .kicad_dru,
local Tutorial symbol/footprint libraries, hardware/requirements/connectivity/spatial
contracts, BOM and [unexecuted bring-up plan](board/bringup-plan.md).
The physical-pin table was authored independently of exported CAD. Generic connector
geometry deliberately lacks a real manufacturer's part selection and qualification.

## Reproduce actual findings

From the extracted toolkit root, with the exact KiCad 10.0.6 available:

```sh
python examples/connector-adapter/replay.py
```

On Windows the checker locates the standard KiCad install. Nonstandard installs use
KICAD_CLI / KICAD_PYTHON as described in the installation guide. replay.py itself uses
standard Python; geometry checks dispatch to matching pcbnew Python. Linux needs the
validated KiCad package and its matching distribution Python.

The replay copies sources into a new .work/recipient-example/UNIQUE/board directory,
previews/applies configuration only in that disposable copy, introduces the known
wrong-pin defect, runs real ERC/connectivity checks, restores exact corrected
schematic bytes, runs the full routing work check, verifies a blocked release and
exports fresh schematic/PCB SVG views. It asserts original input hashes are unchanged.
Every run keeps its evidence; it does not clean or overwrite a recipient project.

Expected summary: passed=true, erc_clean_defect_detected=true,
corrected_work_passed=true, release_blocked=true. The replay exits 0 only when all
these positive and intentional negative expectations hold. An unexpected result
raises an error/nonzero exit; read the traceback and retained reports.

Read .work/recipient-example/result.json for the source hashes, snapshot, actual tool
version, work directory and limitations. Inside that work directory, .work contains
defect-erc.json, defect-connectivity.json, corrected-work.json, blocked-release.json,
fresh native CAD reports and views/. The last check.json is intentionally the blocked
release report, not the earlier green work result. Committed views illustrate the
corrected source; generate fresh views/reports for any change.

## Use in your own project

Follow [Start here](../../docs/start-here.md), install the pinned dependency into a
separate project repository and create new project contracts/CAD. Do not install a
dependency into this example under the extracted toolkit or copy synthetic evidence
as genuine approval. The toolkit's package runner exercises installation separately.

For exploration, copy board/ to a separate sandbox, use the installed wrapper, preview
configuration adoption and inspect the plan before applying. Copied demonstration
evidence stays synthetic. Template project AGENTS.md and workflow packets explain
real review gates; this automatic replay is a test, not permission to skip them.

The authoring utility build_sources.py requires KiCad's matching pcbnew Python and
overwrites the tutorial board sources; it is not part of normal reproduction. It
must not be pointed at a recipient's design. Edit/review the committed CAD normally.
