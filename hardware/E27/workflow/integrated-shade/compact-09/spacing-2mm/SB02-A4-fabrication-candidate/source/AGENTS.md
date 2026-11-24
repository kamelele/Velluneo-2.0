# PCB design by agents

When installed in a project repository, use its pcb-toolkit.py launcher: doctor first,
then run COMMAND PROJECT for backend examples below. Use the locked local dependency;
do not select another checkout or fetch latest. Dependency updates require preview/
explicit apply, fresh checks and affected human review; configuration migration is
separate. Read docs/installation.md in the pinned dependency. Private-source development
without an installed lock remains a separate maintainer context.

## Read requirements first

Read the product specification, hardware.json, requirements.json (or its configured
product.requirements_file path), selected fabrication and assembly
profiles, rule catalog and previous-stage reports. Use the pinned KiCad and ruleset
versions. A tool upgrade requires a separate migration task.
Include an approved electronics-rules revision as a dependency outside board sources.

## Coordinator, implementers and reviewers

Resolve docs/agent-workflow.md and docs/roles/ inside that pinned ruleset dependency;
these paths refer to the ruleset, not automatically to this project. The coordinator
reads coordinator.md, delegates bounded task contracts to implementer.md contexts,
and assigns Reality Checker, Overengineering, Completeness and Change Reviewer roles.
Each reviewer independently inspects the same frozen input and remains read-only.
Record actual actors; do not fabricate independent reviews when a role is unavailable.

Use the task/finding/review/stage/integration/bring-up templates under
templates/project/workflow in the ruleset. Adopt the project issue/PR templates under
templates/project/.github deliberately; init does not install the complete package.
Maintain a task/dependency/ownership index. One active writer per logical shared CAD
file or library, even across branches. Refresh changed dependencies before integration.

Return handoffs with exact input/result revisions, allowed-path diff, requirement IDs,
views/calculations and actual check results. Coordinator receipt is not human approval.
Unresolved blocker/major findings or conflicting reviews stop acceptance. Assign fixes
and independent closure verification; do not resolve by majority vote or changing rules.
Recheck integrated sources and identify which prior reviews/decisions are stale.

Before CAD exists, use intent_digest and explicit input hashes; do not invent a complete
source snapshot. Keep snapshot-referencing lifecycle packets outside their own source
inputs to avoid hash cycles. Genuine design/evidence inputs remain tracked.

## Stages and human reviews

Before each review run requirements --stage STAGE (specification/schematic/placement/
routing/release) and include its traceability matrix and owned open questions.
Keep requirement/interface IDs, owners, revisions and explicit acceptance criteria.
Do not infer expected intent from the CAD under review. Record genuine evidence with
artifact/input hashes; design, calculation, simulation and measurement are different
levels. Unknowns block their declared stage and all later ones. A matching hash never
proves that a measurement occurred or substitutes for human stage approval.

Electrical/firmware interface contracts must be ready by schematic; mechanical
contracts by placement. Follow docs/product-requirements.md in the ruleset repository.

1. Specification: functions, voltage/current domains, faults, interfaces, mechanics,
   environment, applicable standards, test plan and fabrication/assembly options.
2. Schematic and libraries: schematic PDF, BOM/MPNs, pinout and footprint checks against
   exact datasheets, ERC and calculations for supplies and protection.
3. Placement: both sides and 3D views, dimensions/heights, assembly/programming/test
   access, power loops, decoupling, antennas and isolation barriers.
4. Routing: layer views, return paths, stackup, thermal behavior, impedance/lengths,
   fresh ERC/DRC after zone refill and schematic/PCB parity.
5. Release: Gerbers, drills, BOM, positions/rotations, assembly drawing, DNP, panel and
   stencil information, check report and bring-up plan.

After EVERY stage present the complete evidence and open questions. Wait for explicit
approval from the user or the team reviewer authorized by the user before proceeding.
Authorization to perform design work is not approval of its schematic or release.
Never approve your own work or fabricate evidence of human acceptance.
Record approver, a link to the actual decision and source snapshot.
Request renewed review when the final snapshot changes previously reviewed materials.
All four role reports must cover the final packet or have explicit, justified retained
scope. Agents recommend ready_for_human_review; only the user or their authorized team
reviewer approves the stage. A merged PR does not automatically authorize the next
stage, manufacturing, orders or physical testing. Verify source hashes after merge.

## Configuration and rules

Use scripts/pcb_rules.py init for a new project. Complete hardware.json, then run
configure to PREVIEW. Review the diff and conflicts, close KiCad, and explicitly apply
the printed plan ID with configure --apply PLAN_ID. See docs/configuration-adoption.md
in the ruleset repository. Do not manually edit generated custom rules to bypass policy.
Preserve .electronics-rules/config-state.json in version control. Keep .work backups
locally for rollback; do not publish them.

Choose exact service, stackup, copper and assembly process. The agent proposes and
the user approves. A manufacturer does not determine the product's safety class.
Frameless stencil is a candidate process choice, not line qualification.
Do not assign assembly capabilities without the local PCBA provider's confirmation.
Use templates/project/local-pcba-provider-capabilities.json from the pinned toolkit
as a starting record; follow docs/local-pcba-provider.md to bind confirmed limits,
manual review requirements and evidence. This file alone does not generate DRC.

Do not change pin types to passive, add PWR_FLAG without an actual source, relax global
limits or disable checks to obtain a clean report. Do not use No Connect on a pin that
must be connected. A deviation requires a rule ID, exact objects/scope, electrical or
manufacturing rationale and human approval. A shared profile is not the place for an
exception affecting one component. Historical results provide context, not approval.

## Verification and release

Before placement, independently complete spatial-constraints.json, set product.spatial_file
and obtain real approval of its intent digest. Read docs/spatial-constraints.md in the
pinned ruleset. Review configure's spatial-resolved.json, source diff and SVG footprint/
pad/connection/area preview before applying the plan. Do not move shared CAD objects
outside the assigned ownership scope. Existing mismatched geometry needs manual migration.

Supply the exact .electronics-rules/placement-input.json and routing-input.json contract
to placement/routing adapters and record the constraints_digest actually supplied.
These declared inputs do not prove adapter execution or install an autonomous router.
Run spatial after saved PCB changes, then fresh DRC. Never bypass custom area rules;
a router ignoring them is unqualified. Keep sensitive nets, switching nodes, return
paths, loops and Kelvin requirements in block cards linked to product evidence.
Geometry does not prove topology, SI/PI/EMC or physical isolation.

Before generating the schematic, prepare product.connectivity_file from independently
reviewed requirements and datasheets. Enumerate components, units, physical pin numbers,
net pin sets, explicit NC reasons and electrical separation barriers. Record basis
file hashes and obtain a real human decision bound to the intent digest. Never derive
the expected graph from the schematic being tested or invent approval evidence.
See docs/intended-connectivity.md inside the pinned ruleset dependency.

After schematic or library changes, run connectivity and retain its fresh export report.
Compare physical pin membership, not net names. Keep three independent checks: approved
intent versus schematic, ERC, and schematic/PCB parity with DRC. Passing one cannot
replace another. A connectivity mismatch requires correction or an explicitly reviewed
intent change; it cannot be waived by changing ERC types or ignoring a finding.
An electrical separation check does not verify physical insulation or creepage.

Run check --mode work after changing sources, libraries, rules or zones.
Use --stage for the stage being reviewed; the default work stage is specification.
Save complete reports, tool/ruleset versions and source hashes. Tool failure means
verification is absent, never passed. Include local libraries and subsheets in
source_files. CAD checks do not replace calculations, review, EMC or safety testing.

Before release bind manufacturing files to the final source snapshot. Review layers,
outline, drills, BOM/DNP, sides, rotations and assembly process. Record artifact hashes,
product-requirement evidence and genuine stage approvals. check --mode release must
pass. Its result is evidence for acceptance, not a certificate.
Do not send the project to a supplier or order boards without a separate user instruction.
Never publish protected full projects in the rules repository.

Before bring-up/integration, name hardware/enclosure/cabling/firmware revisions,
responsible human, actual test setup, expected results and stop conditions. Missing
limits block that test. Record actual measurements and create linked defect/ECO issues;
rework and firmware changes require renewed affected verification. A bring-up plan
is not a record of measurements, and an operating board is not full product qualification.

Write project documentation and agent deliverables in English; retain original source
identifiers and quotations where required for traceability.
