# Independently approved intended connectivity

Three controls answer different questions:

1. **Intent ↔ schematic:** does the physical-pin graph match an independently specified,
   human-approved document?
2. **ERC:** do the schematic's electrical pin rules pass?
3. **Schematic ↔ PCB / DRC:** does the board match the schematic and geometric rules?

Passing ERC/parity cannot establish intended function when both CAD representations
repeat the same error. This feature implements the first comparison without treating
net names as identity. Keep all three controls in schematic/release review.

## Prepare intent before generating the schematic

Set product.connectivity_file in hardware.json, normally intended-connectivity.json.
init copies an unapproved draft. Legacy projects copy the template and add the
declaration explicitly. Legacy work reports unconfigured intent; release refuses it.
A declared document is checked whenever the full checker runs.

An authorized person reviews a physical pin table from product requirements,
interfaces and exact part information. Record independent basis and source hashes.
Do not export the schematic and call its graph the expected graph. The tool cannot
prove intellectual independence or reviewer authenticity; reviewers must inspect
provenance and the actual decision.

Scope is one KiCad project/default variant. Separate board projects use separate
documents with local refdes. Product-level cable/firmware/mechanical contracts remain
in requirements.json; this checker does not automatically combine boards.

## Document schema_version=1

| Field | Meaning |
|---|---|
| revision | Nonempty revision string, incremented for intentional changes |
| basis | Independently reviewed source/purpose, not a conclusion inferred from CAD |
| basis_sources | Project-relative {path,sha256} list; nonempty for designs with components |
| components | Unique annotated refdes and explicit unit/physical-pin maps |
| nets | Unique internal ID and complete set of {ref,pin} members |
| no_connects | Explicit {ref,pin,reason} for unused physical pins |
| barriers | Optional {id,side_a,side_b,basis} electrical separation agreements |
| empty_design_reason | Required if no components exist, e.g. a reviewed coupon |
| approval | Actual approved_by, evidence and intent_digest, or null while draft |

Example component: {"ref":"U1","units":[{"name":"A","pins":["1","2"]},
{"name":"B","pins":["3","4"]}]}. Unit names follow validated export naming (e.g. A/B);
pins are physical package numbers, not signal names or unit-local renumbering.
Preserve strings such as A1, EP and 01. Shared physical pins may appear in multiple
unit maps but belong to only one expected net or NC. Pinless components require
pinless_reason. Unannotated references and ambiguous/duplicate JSON keys are rejected.

Every physical pin must occur exactly once in nets or no_connects. A singleton net
requires single_pin_rationale; it is not a substitute for explicit NC on an unused pin.
No partial-net scopes, wildcard matching, ignored extra components or automatic
waivers are supported. Correct CAD or deliberately revise/reapprove intent.

Net IDs are diagnostic references, not KiCad labels. Generated names/aliases may
change without a mismatch if physical membership is unchanged. Names still need
human readability/functional review. Barrier sides reference disjoint known net IDs
and must not become electrically connected. This does not establish physical isolation,
clearance, creepage or safety compliance (#8/#11).

Basis files are stable sources outside .work and must match their hashes. The intent
itself or .kicad_sch/.kicad_pcb under test cannot be its own basis. Other derived content
cannot be recognized automatically: independent review remains essential.

## Approval and hashes

intent_digest is SHA256 of canonical UTF-8 JSON excluding the top-level approval:
sort_keys=True, ensure_ascii=False, separators=(',',':'), allow_nan=False.
Component/net/NC/barrier/basis/revision changes invalidate prior approval.
Record the authorized person's actual decision link/text and exact accepted digest.
Agents must not invent approvals or rebind a previous decision to new content.
These are provenance records, not digital signatures.

A basis file change blocks comparison until its hash is deliberately updated and
new intent approved. Intent, approval and basis files enter project snapshots and
configure preview inputs automatically. Final stage approvals still require the
current full project snapshot. The intent digest does not depend on generated CAD,
avoiding self-confirming or cyclic expectations.

## Run comparison

    python scripts/pcb_rules.py connectivity PROJECT
    python scripts/pcb_rules.py check PROJECT --mode work --stage schematic
    python scripts/pcb_rules.py check PROJECT --mode release

The standalone command requires the actual schematic and intent, not a PCB.
It writes .work/connectivity.json. Full checks include the result/commands in
.work/check.json alongside ERC/DRC/parity and requirements. Missing legacy intent
blocks release; stale/invalid/mismatched declared intent cannot be hidden by clean CAD.

The previous .work/connectivity-netlist.xml is removed before fresh export with
sch export netlist --format kicadxml. Nonzero exit, absent/empty/unsupported output,
another source schematic or changed inputs fail verification. Cached success is not
accepted. Exit 0: agreement/current approval; 1: graph/approval findings; 2: invalid
configuration or export failure.

## Supported export and diagnostics

Validated: **KiCad 10.0.6**, XML export E with exact Eeschema version identity.
The explicit exporter identity list is Eeschema 10.0.6 (Windows) and
Eeschema 10.0.6+dfsg-1 (Ubuntu package 10.0.6+dfsg-1). Arbitrary packaging suffixes,
nightlies and later package revisions are rejected. See [Ubuntu validation](linux-validation.md)
for the headless container environment, reproduction and actual evidence.
Unsupported formats, unresolved library pin inventories or unit data fail rather
than silently dropping pins. Default export scope is used; alternate variants and
exceptional/stacked-symbol forms need separate validation before support is claimed.
Include relevant local sheets, libraries and tables in source tracking.

XML unit lists describe library units, not necessarily all placed instances.
The comparison checks library unit/pin maps, symbol-instance timestamp counts and
actual physical connectivity. This detects the tested omitted unit without assuming
that a unit list proves placement. It does not reconstruct every timestamp-to-unit
relationship from raw schematic text; retain ERC missing-unit checks and library review.

NC uses the exported no_connect pin indication, not a name beginning “unconnected”.
Expected NC must be explicit and electrically isolated; joining marked pins still
fails. Truthful pin types remain a separate library/ERC obligation.

Findings identify missing/extra components/pins, unit/pin or instance-count mismatch,
merged/split nets, unassigned pins, missing/unexpected/connected NC and bridged electrical
separation. Actual net names are diagnostic only. Reports include intent digest/revision,
exact intent/export hashes, commands and exporter version.

## Validation and limits

[Original fixtures](../examples/connectivity/README.md) cover valid/renamed graphs,
merge, split, wrong pin, omitted unit, missing NC and connected NC. A merged-net fixture
passes ERC and PCB parity/DRC while the independent comparison fails. Synthetic
approvals and excluded-from-board passive fixture symbols test gates; they are not
human acceptance or a physical product design.

Agreement does not establish MPN/package correctness, functional operation,
voltage/current adequacy, firmware, PCB geometry, EMC, safety or manufacturing capability.
Use requirements, four reviews, DRC/parity and physical tests. Never change the expected
graph merely to make a failing schematic pass.

