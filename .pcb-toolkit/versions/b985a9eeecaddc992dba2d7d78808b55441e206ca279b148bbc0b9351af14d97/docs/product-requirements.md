# Product requirements and subsystem interface contracts

requirements.json is the versioned input to the coordinator and Completeness Reviewer.
It describes intended behavior and agreements before CAD exists. It is not generated
from the schematic under review. New projects receive an intentionally incomplete
template; no product thresholds, capabilities or approvals are invented.

## Start and stage checks

Set product.requirements_file in hardware.json to the project-relative document path.
For an existing 0.2.0 project, copy templates/project/requirements.json and add this
field deliberately. The old product.requirements list is deprecated and cannot satisfy
release verification. Preserve its content as migration input; do not translate a
legacy evidence string into a claimed passed measurement automatically.

    python scripts/pcb_rules.py requirements PROJECT --stage specification
    python scripts/pcb_rules.py requirements PROJECT --stage schematic
    python scripts/pcb_rules.py requirements PROJECT --stage placement

These commands do not require KiCad or board files. They write .work/requirements.json
with errors, a traceability matrix, open questions and blocked stages. Exit codes:
0 passes the requested stage, 1 means missing/conflicting/stale evidence, 2 means an
invalid or unreadable document. Passing the checker does not approve a stage.

check --mode work uses specification by default; use --stage to evaluate a later gate.
check --mode release always checks all requirements through release. Declared contract
files, evidence artifacts and their input files are automatically included in source
snapshots and configuration-plan inputs. Keep these files under version control.
An undeclared legacy contract is reported as unconfigured in work mode and blocks release.

## Document and identity

Top-level keys: schema_version=1, product, revision, subsystems, requirements,
interfaces, unknowns and evidence. Product/revision are nonempty strings. Every record
has a globally unique ID using letters, digits, underscores or hyphens, starting with
a letter. IDs remain stable; increment revisions for intentional changes.

Subsystems contain id, kind (pcb/enclosure/firmware) and owner. Name actual board roles
and interface owners, not agent-generated filenames alone. The manifest must contain
at least one subsystem and one requirement. Humans still review whether all product
requirements and interfaces have been enumerated; the tool cannot infer omitted intent.

## Requirements and the matrix

Each requirement contains:

| Field | Meaning |
|---|---|
| id, revision, owner | Stable identity, revision and accountable person/team |
| text | Explicit product requirement |
| basis | Product decision or exact source of the requirement |
| acceptance | Concrete pass/fail criterion, including values/units and conditions where applicable |
| gate | First blocked stage: specification, schematic, placement, routing or release |
| implementation | Nonempty list of {subsystem, object}, optionally a project-relative path for verification inputs |
| method | design, review, calculation, simulation, measurement, ERC or DRC |
| evidence_ids | References to evidence records; an empty list remains unverified |

The matrix links ID/revision → implementation → required method → current evidence →
observed level and stage status. Designed, reviewed, calculated, simulated, measured,
ERC-checked and DRC-checked are distinct. A document review never satisfies measurement.
Textual criteria are not automatically evaluated: their correctness and adequacy require
the named reviewer. CAD checks, simulations and physical tests remain different proofs.

## Shared interface fields

An interface uses the same revision/owner/basis/acceptance/gate/method/implementation/
evidence fields as a requirement. Also provide kind, requirements (nonempty references
to requirement IDs), two distinct subsystem endpoints, startup_behavior and fault_behavior.
Every link names both sides and the connector/cable or software/mechanical agreement.

Electrical and firmware contracts must be due no later than schematic; mechanical
contracts no later than placement. Earlier gates are allowed. Unresolved details must
have an owner and explicit unknown record; they are not assigned fallback values.

### Electrical

Each endpoint has subsystem, connector and pins. Each pin has a unique string pin
number, signal and role (power/signal/ground/nc). Power and signal pins also have
direction (source/sink, or bidirectional for a signal) and finite voltage_min_v /
voltage_max_v. A power source declares available current_ma; its sink declares load
current_ma. Ground and explicitly unused pins do not require invented voltage budgets.

connections is an explicit list of {a, b} physical pin mappings covering every pin once.
Mapped roles/signals must agree. Source voltage bounds must fit sink acceptance,
available power current must cover load, and drive directions must be compatible.
Bidirectional signal envelopes need an explicit matching agreement.

These are checks of declared DC envelopes only. They do not establish logic thresholds,
timing, transient response, loading, protection, startup or physical pin assignment in
CAD. Describe those conditions in requirements and provide calculations/tests. The
[connectivity command](intended-connectivity.md) compares separately approved physical
pin membership with the actual exported schematic netlist; it does not prove function.

### Firmware

Each endpoint declares protocol and a nonempty parameters object. Both must match
exactly. Use explicit units in parameter names and define framing, addressing, timing,
levels and versioning where needed. This validator compares declarations, not firmware
binaries or protocol correctness. Startup and fault behavior are reviewed text.

### Mechanical

Provide geometry with unit=mm, outline (at least three finite [x,y] points),
mounting_holes ({x,y,diameter}), connector_positions ({ref,x,y,z,height}),
max_component_height_mm, tolerance_mm, keepouts ({outline,reason}) and thermal_conditions.
Empty lists are explicit assertions of no such features, to be reviewed. Dimensions
must be finite; heights/tolerances are nonnegative and hole diameters positive.

Describe the coordinate origin/orientation in the referenced mechanical drawing and
the acceptance text. Record connector mating/assembly access, wiring and thermal
conditions before placement. The tool checks declared field consistency, not enclosure
fit, polygon clearance, tolerance stacks or thermal feasibility. Spatial CAD enforcement
and layout evidence belong to #11.

## Unknowns

Each unknown has id, record_id, field, owner, question, blocks_stage and status=open.
The report lists the question and blocks that stage and all following ones. An unknown
for placement can remain open during specification; it cannot disappear into a default
dimension. To resolve it, update the target, set status=resolved, record a nonempty
resolution and evidence_ids. Missing/stale/failed resolution evidence still blocks.

## Evidence and freshness

An evidence record contains id, kind (one of the methods), result=pass/fail,
verified_by, artifact (project-relative nonempty file), sha256, intent_digest and
inputs (an explicit list of {path,sha256}). Artifact/input bytes must match the hashes.
Technical methods (calculation/simulation/measurement/ERC/DRC) require nonempty hashed
inputs and implementation.path on each implementation object; the evidence must cover
all of those paths. This binds verification to actual declared design/calculation inputs,
not merely to the unchanged wording of a requirement.
Keep stable evidence copies outside .work; do not use a generated check report as its
own input or introduce cyclic hashes.

intent_digest is SHA256 of canonical UTF-8 JSON for the entire document excluding its
top-level evidence list: sorted keys, ensure_ascii=False, separators=(',',':'),
allow_nan=False. The requirements command reports the current digest even when evidence
is stale. Set IDs/references first, then obtain a genuine verification result, record
its exact inputs/artifact hashes and digest, and rerun the gate check.

Any requirement, interface, revision, acceptance or unknown change invalidates prior
evidence conservatively across the document. Changing only evidence does not create
a digest cycle, but still changes the complete project source snapshot and approvals.
A fail result blocks the referring record even alongside a pass; remove superseded
references only through a reviewed, recorded change.

Hashes establish freshness, not truth or reviewer authority. The checker cannot prove
that a claimed measurement happened or that a verifier was authorized. Preserve actual
review decisions separately; the agent must not fabricate them. Product-specific
standards and barrier values remain in #8 and the existing barrier cards.

## Example and follow-on work

[The original multi-board example](../examples/multi-board/README.md) demonstrates a
valid declared contract, missing requirement, interface conflict, stale evidence and
an unknown blocking placement. It is not a tested circuit or actual human approval.

#15 will use the matrix as the coordinator/reviewer task input; #19 will expand recipient
onboarding. This issue does not implement actual-netlist comparison (#9), spatial
verification (#11), physical qualification or stage orchestration.
