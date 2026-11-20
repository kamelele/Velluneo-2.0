# Start here — recipient path

## Starting from an idea?

You do not need to start with the commands below. Open your device repository in
your agent, use the [copyable kickoff prompt](../README.md#start-with-an-idea-and-an-agent),
and follow [Your first project](first-project.md). The agent asks a few questions,
explains choices and prepares a specification for review before designing a circuit.
Requirements discussion can begin before CAD tooling is installed. The remaining
sections are the technical setup/reference for the agent or experienced user.

Use this guide with the exact extracted toolkit you received. Current packages are
technical previews using the candidate archive protocol. Apache-2.0 applies to our
material; license scope is in LICENSE, NOTICE and THIRD_PARTY_NOTICES.md.
Keep project requirements, approvals and evidence in your own repository; no central
registration or submission of your project is required. No private
repository, Drive account or service authentication is needed to run the toolkit.
Use Python 3.11+ and validated KiCad 10.0.6 with its matching pcbnew Python; see
[installation](installation.md) for tested Windows/Ubuntu scope and tool paths.

## 1. Verify, install and check the environment

Obtain the archive and its expected SHA256 through your trusted review/release channel.
Extract into a temporary toolkit directory. From that directory, use:

```sh
python scripts/package_toolkit.py verify-tree .
python scripts/toolkit_install.py install ../my_project_repo --archive ../TOOLKIT.zip --sha256 EXPECTED_SHA256 --allow-candidate
```

Replace TOOLKIT.zip and EXPECTED_SHA256 with the received file and trusted digest;
create/select my_project_repo first. It must be separate from the extracted toolkit.
Tree verification checks integrity; the trusted archive digest identifies the expected
package. Neither authenticates a reviewer. Candidate consent is not publication consent.

From my_project_repo:

```sh
python pcb-toolkit.py status
python pcb-toolkit.py doctor
python pcb-toolkit.py run init boards/my_board --vendor jlcpcb --assembly inhouse
```

The selected vendor/assembly are proposals to review, not confirmed capabilities.
Do not proceed past a failed doctor. KICAD_CLI and KICAD_PYTHON may select nonstandard
paths; doctor verifies actual tool versions. Keep the lock, launcher and immutable
dependency in your project version control as described in installation.md.

## 2. Complete the four profile layers before design

| Layer | Decide and record | Review material |
|---|---|---|
| Common | Exact toolkit/KiCad pin, libraries, pin types and review process | Lock, hardware.json, library sources |
| Product | Use case, voltage/current/environment, interfaces, mechanical and special requirements | Specification, requirements.json, evidence/unknowns |
| PCB fabrication | Supplier, actual service, stackup, copper, finish and confirmed limits | hardware.json fabrication fields and order-specific evidence |
| Assembly | Supplier or actual in-house process, parts/paste/stencil/inspection limits | Assembly profile, confirmation evidence and unresolved questions |

JLCPCB and Eurocircuits are candidate profile choices independent of assembly mode.
In-house assembly needs the local PCBA provider's confirmation. Do not invent values to
remove unknowns. If an unknown affects a stage, identify its owner and block that stage.
Do not reuse the tutorial's synthetic evidence in a real project.
Capture local assembly limits using the [provider capabilities template](local-pcba-provider.md).
Bind it and its evidence to source snapshots and requirements; rule cards are not
automatically compiled into DRC.

## 3. Work stage by stage

init creates drafts and AGENTS.md; it does not create CAD, a full installed workflow
or approvals. Read [project instructions](../templates/project/AGENTS.md),
[requirements](product-requirements.md), [connectivity](intended-connectivity.md) and
[spatial contracts](spatial-constraints.md). Adopt workflow/issue/PR templates from
templates/project deliberately after checking conflicts with existing files.

| Stage | Prepare for the assigned human reviewer |
|---|---|
| Specification | Scope, four profile proposals, requirements/interfaces, open questions, independent pin intent and outline constraints |
| Schematic/libraries | Schematic view, pin/footprint verification, calculations, ERC and intended-connectivity report |
| Placement | PCB views, connector/enclosure fit and component orientation, spatial report, unresolved layout questions |
| Routing | PCB copper views, return paths/critical nets review, fresh DRC and parity/connectivity checks |
| Release | Consistent source/report/output revisions, Gerber/drill/BOM/assembly data, approvals, confirmed processes and bring-up plan |

The coordinator delegates bounded work with one writer per shared CAD/library file.
Four independent reviewers examine the same frozen input: Reality Checker,
Overengineering Reviewer, Completeness Reviewer and Change Reviewer. Record actual
actors and unavailable roles. Submit a packet after each stage and wait for the
assigned human's decision before the next stage. Coordinator receipt is not approval.
See [workflow](agent-workflow.md) and [review evidence](reviews.md).

Run from the project repository; replace STAGE and PLAN_ID with actual values:

```sh
python pcb-toolkit.py run requirements boards/my_board --stage specification
python pcb-toolkit.py run configure boards/my_board
python pcb-toolkit.py run configure boards/my_board --apply PLAN_ID
python pcb-toolkit.py run connectivity boards/my_board
python pcb-toolkit.py run spatial boards/my_board
python pcb-toolkit.py run check boards/my_board --mode work --stage STAGE
python pcb-toolkit.py run snapshot boards/my_board
python pcb-toolkit.py run check boards/my_board --mode release
```

Preview first, inspect the plan/diff, close KiCad, then apply the current plan.
STAGE is specification, schematic, placement or routing. Requirements can be checked
before CAD exists; full CAD commands need actual sources. Exit 0 is success, 1 means
findings/incomplete work and 2 means tool/configuration failure. Read each new .work
report; an old green report is not evidence for changed inputs. Work success alone
does not approve a stage or manufacturing release. Recheck after source/library/rule/
zone changes and refresh affected reviews.

## 4. Learn with the original example

Use the separate [connector-adapter example](../examples/connector-adapter/README.md).
It includes editable schematic/PCB/libraries, independent specification, requirements,
views, calculations, BOM, a bring-up plan and four authored review perspectives.
Its replay demonstrates clean ERC with wrong pins, detection, correction and a blocked
release. All approval-like labels are synthetic; no agents or humans are impersonated.
Do not copy its generic geometry or profile assumptions as qualified production inputs.

## Existing projects, deviations and help

For an existing board, use the [existing-project path](existing-projects.md).
For findings, record the rule/object, expected/actual behavior, source revision and
evidence. Fix the design; any justified exception needs a local scope, reason and
genuine approval tied to its rule/object. Never change pin types, globally loosen
limits or suppress unknown rules to obtain green reports.

Report problems using [contribution guidance](contributing.md). Include the pinned
manifest/version, platform/tools, minimal non-confidential reproduction and fresh
reports. Keep credentials and customer files out of issues. Unconfirmed product/process
requirements belong to the project's owner, not an invented toolkit default.
