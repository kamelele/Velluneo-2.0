# Project contract and acceptance

Use the [agent workflow](agent-workflow.md) for delegation, independent reviews,
write ownership and stage packets. Task receipt, agent recommendations, human stage
approval, PR merge, manufacturing release and physical validation are distinct events.

## hardware.json

schema_version=1. name is the KiCad basename (letters/digits/_/-). kicad_version is
the exact release, initially 10.0.6. Pin an electronics-rules commit as well.
Reports record VERSION and configuration hashes. Keep the dependency outside board sources.

fabrication.vendor is jlcpcb or eurocircuits. service must be in the profile's services.
stackup, copper, finish and confirmation_evidence are required before release.
Confirmation covers the SPECIFIC technology and additional DFM requirements, including
pad-to-pad, hole-to-copper, mask, rings, drill compensation and aspect ratio.
The checker does not read order documentation or establish its authenticity.

assembly.mode is supplier or inhouse. For supplier, confirm the exact PCBA service,
parts availability, packages, sides, panel, fiducials, rotations, stencil and inspection.
For inhouse, obtain process confirmation from the local PCBA provider and record it
in assembly.local_pcba_provider_confirmation. Frameless stencil is a user
decision; choose thickness/apertures for the actual paste and pads.

product.domains lists functions, working/peak voltages and currents.
product.requirements_file points to the versioned requirements/interface document.
It replaces the legacy product.requirements list, which no longer satisfies release
verification. See [the requirements guide](product-requirements.md) for IDs, methods,
acceptance criteria, interfaces, unknowns and revision-bound evidence. Evidence must
refer to the current specification and declared implementation inputs.
minimums_mm optionally tightens global clearance,
track_width, hole_size, annular_width and edge_clearance. Do not put isolation requiring
separate barriers here: one global clearance does not describe the full barrier geometry.

special_requirements lists applications needing further analysis, e.g. medical,
mains isolation, measurement/laboratory, RF, high currents or controlled impedance.
standards_review_evidence is an approved assessment of applicable standards and requirements.
barriers contains side_a, side_b, working_voltage, transient_voltage, pollution_degree,
cti, altitude_m, clearance_mm, creepage_mm, standard_clause, evidence and approved_by.
Also record frequency, protection type and material. Checking that fields are present
does not derive values from a standard or verify the actual creepage path.

netclasses is a list of {name, nets, clearance, track_width}. nets contains KiCad
assignment patterns; verify membership in CAD. Default is reserved. Calculate power
trace widths; the template's 0.254 mm is a working preference, not an ampacity guarantee.
The generator does not automatically migrate xSignals, topology or creepage rules.
Record those requirements and calculations/reviews; add separate tests for automation.

source_files includes local schematics, boards, .kicad_pro, .kicad_dru, libraries and
other design inputs. Local sheets and libraries must be listed. Include library tables,
custom models and documents when they underpin review.
Declared requirement files and their evidence/input files are added automatically to
snapshots and configure plan inputs. Stable evidence must be outside .work. The
requirements command runs before CAD exists; check --mode work can use --stage, while
release always evaluates every requirement through the release gate.
For adopted projects, .electronics-rules/config-state.json is automatically included
in snapshot inputs and must be version controlled. It records ownership, not approval.
See [configuration adoption](configuration-adoption.md) for preview, apply and recovery.

## Approvals and changes

product.spatial_file selects the independent spatial contract. init creates a draft
but leaves this path null until deliberate adoption. Missing adoption blocks release;
declared contracts must pass work checks as well. See [spatial constraints](spatial-constraints.md).
The resolved outline, areas, minima and classes are shared by placement/routing input
files and generated DRC. Native outline/areas and those files use configure preview/
apply/rollback. Consumer input agreement does not prove external tool execution.
Named netclass track_width becomes an explicit DRC minimum when spatial rules are
adopted. Default keeps its global minimum and preferred width distinction.
Cards cover sensitive nets, switching nodes, returns, loops and Kelvin connections,
linked to requirements/evidence. These topics are not proved by rectangle geometry.

product.connectivity_file selects the independent intended-connectivity document.
init installs a deliberately incomplete draft. Adopt it explicitly in older projects;
absence is reported during work and blocks release. Once declared, a failed check
blocks both work and release verification. See [the connectivity guide](intended-connectivity.md).
Intent and its basis files automatically enter snapshots and configure plan inputs.
Changing approval metadata also changes source bytes and invalidates old snapshots.
The standalone connectivity command runs before a board exists. Its current scope is
the default schematic assembly, KiCad 10.0.6 XML E export; variants need separate intent
and validated export handling. It does not validate MPNs or physical isolation.

approvals has specification, schematic, placement, routing and release keys. Each record
contains approved_by, evidence (the actual human decision) and the snapshot command's
result. The agent does not invent approvals. This is not a digital-signature system:
the person recording evidence must be authorized to attest to it.

Any source/configuration change invalidates its snapshot. Release approvals must cover
the final state; changes affecting prior reviews require renewed confirmation.
The tool does not orchestrate stage transitions; the project AGENTS.md requires stopping
at each stage. A configuration no-op preserves source bytes and snapshot.

waivers contains finding_sha256 (SHA256 of JSON with sort_keys=True), snapshot, rule_id,
object_ids, reason, approved_by and approval_evidence. Findings remain in the report.
A waiver does not disable the CAD check or transfer automatically to another revision.
A KiCad exclusion alone is not an approved waiver. Existing exclusion lists are preserved
and currently block automatic adoption pending explicit review.

## Release package

release_files contains lists for gerbers, drills, bom, positions, assembly_drawing and
bringup_plan. Each entry has path (inside the project), sha256 and snapshot. Files must
exist, be nonempty and match the hash. Review actual contents and consistency with CAD:
the checker does not semantically compare Gerbers with the schematic.

The final release approval also contains artifacts_digest: SHA256 of the full
release_files JSON with sorted keys (Python json.dumps(..., sort_keys=True)).
check.json reports it even if approval is missing. Human approval follows inspection
of the specific package. Artifacts stay outside the source snapshot to avoid a hash
cycle; a separate digest binds them to release approval.

check --mode release requires clean checks or approved local waivers, complete inputs
and current approvals. It sends nothing to suppliers and orders no boards. Do not
release a product solely on ERC/DRC results.

## Tool migration

Pin exact versions per project. Migrate a copy separately when adopting another stable
KiCad release. Run the entire suite and check the ERC matrix, DRC precedence, report
formats, zones and exports before expanding supported versions and publishing new rules.
Nightly builds are not the default.
