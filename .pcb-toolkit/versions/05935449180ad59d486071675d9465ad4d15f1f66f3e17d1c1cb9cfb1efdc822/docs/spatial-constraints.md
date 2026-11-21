# Shared spatial constraints

The spatial contract resolves one set of inputs for placement, routing and KiCad DRC.
It does not install a placement engine or router. The generated consumer files check
the declared inputs supplied to an adapter; they cannot prove that an external tool
actually consumed them. Always inspect the saved PCB and run real DRC afterward.

## Prepare independently

init creates an incomplete spatial-constraints.json draft. Fill it from mechanical,
product and datasheet requirements, then set product.spatial_file in hardware.json.
Never derive an expected outline or protected region solely from the PCB under test.
Missing spatial adoption blocks release; undeclared work remains explicitly unverified.
Once declared, malformed or inconsistent spatial constraints fail work checks too.

The version 1 document contains:

- revision, basis and basis_sources with project-relative paths and SHA256 hashes;
- outline_mm: [xmin, ymin, xmax, ymax], in board coordinates and millimetres;
- areas: unique IDs, rectangle_mm, explicit F.Cu/B.Cu layers, disallow object types,
  basis and exceptions;
- blocks: analog/power review cards linked by requirement_id to requirements.json;
- no_blocks_reason when there are no relevant blocks;
- approval: approved_by, real decision evidence and intent_digest.

An area may disallow track, via, pad and/or zone. Do not add a margin from a generic
example: derive the rectangle and its relationship to conductors from the actual
requirement. Rectangles are closed boundaries for KiCad's intersection test, not a
creepage calculation. Only the tested outer copper layers are supported.

Every exception names one exact PCB net within one area and records reason,
approved_by and actual decision evidence. Wildcards/expressions are rejected. The net
must exist in the PCB; the exception is not a global rule relaxation. Exception
metadata is part of the human-approved intent digest. Approval records are attestations,
not authenticated signatures; an agent must not invent them.

Each block card names id, basis and an existing requirement_id. It explicitly covers
sensitive_nets, switching_nodes, return_paths, loops and kelvin_connections. Every topic
has objects (a list of exact design identifiers) and a rationale. An empty list needs
an explicit rationale explaining why the topic is inapplicable; silence is not a
completed analysis. Put acceptance criteria, unknowns, review/calculation/simulation/
measurement evidence and affected stages in the linked product requirement.

## Preview and apply

```sh
python scripts/pcb_rules.py configure PROJECT
python scripts/pcb_rules.py configure PROJECT --apply PLAN_ID
python scripts/pcb_rules.py spatial PROJECT
python scripts/pcb_rules.py check PROJECT --mode work --stage placement
```

Review the configuration diff and .work/spatial-preview.svg before applying.
The readable .work/spatial-resolved.json includes resolved constraints and intent_digest
for the genuine human decision. An approval change still invalidates source snapshots.
The preview shows proposed outline/protected rectangles and the actual saved footprint
bounding envelopes and pad positions. Dashed green lines connect pads on the same net
as a review aid; they are not routes or proof of physical continuity. Blue envelopes
are footprint bounding boxes, not clearance-qualified courtyards or 3D collision tests.
No components are moved by this implementation. Review both PCB sides/3D separately.

The existing preview/apply transaction covers project settings, custom rules, added
outline/area geometry and placement/routing input files. Preview does not write the
source PCB. Applying requires the exact current plan; stale sources/configuration/
libraries/dependencies refuse application. Backups and rollback include the PCB.

Only a genuinely absent outline is created. Existing geometry must match the declared
rectangle exactly, as four straight Edge.Cuts segments. Arcs, holes, slots and cutouts
need separate implementation/validation and currently fail closed. Existing mismatched,
duplicate or removed managed areas require deliberate manual migration; they are not
silently overwritten. Unrelated board objects are preserved. Unknown custom rules and
existing exclusions still use the safe-adoption refusal rules.

## One resolved contract

The contract combines explicit outline/areas/block cards with resolved fabrication/
product minima and the same netclass settings used in .kicad_pro. It is hashed and
written identically into .electronics-rules/placement-input.json and routing-input.json.
Adapters must take these exact files as their constraint input; task/review records
must identify the digest actually supplied. Consumer-file divergence fails verification.
These files are versioned design inputs; keep them with config-state.json.

Native named KiCad rule areas are generated with fixed IDs and explicit geometry.
Custom .kicad_dru intersectsArea/disallow rules enforce the scoped restrictions,
including exact-net exceptions. The native area flags themselves are neutral to avoid
unconditionally forbidding an approved net. A tool that ignores custom rules is not
qualified to route this contract; actual KiCad DRC remains required.

Explicit named netclasses also generate minimum track-width constraints matching
their declared track_width. Default retains the existing global floor and preferred
router width. This closes the gap between a named class's preferred routing width and
DRC minimum enforcement; calculate the product value before declaring it.

The spatial document, basis, consumer files and checker modules enter snapshots and
configuration fingerprints. Changes invalidate previous checks/approvals. Human spatial
approval is bound to intent_digest; stage/release approvals still bind final snapshots.
Run fresh ERC, intended-connectivity, DRC/parity and requirements checks after changes.

## Limits

Return currents, loop area, Kelvin topology, sensitive-node coupling, SI/PI/EMC,
thermal performance and physical isolation still require the linked calculations and
human reviews. No rectangle or clean DRC establishes those properties. Missing product,
manufacturer/service or assembly confirmation remains a release blocker.

Validation uses original synthetic geometry and synthetic approval records, never
customer CAD or actual product acceptance. Tests must cover valid and violating objects,
layer and exception scope, netclass width, consumer divergence, preview stability and
rollback using the exact pinned KiCad on Windows and the Ubuntu container.

Run the bundled candidate runner for fresh unit/CAD results; historic private
validation reports are not part of this package. Preserve actual findings and limits.
