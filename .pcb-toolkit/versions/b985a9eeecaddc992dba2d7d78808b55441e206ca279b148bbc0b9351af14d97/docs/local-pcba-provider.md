# Local PCBA provider capabilities and rules

Start from [local-pcba-provider-capabilities.json](../templates/project/local-pcba-provider-capabilities.json).
It is a blank, provider-neutral record, not a qualified process or executable DRC
profile. null means unknown; an empty list means nothing has been declared, not
unlimited support. false, where applicable, means explicitly unsupported. No default
pitch, package, stencil thickness or inspection capability is supplied.

## Adopt the record

1. Copy the template into your board directory as local-pcba-provider-capabilities.json.
   init does not copy this optional template automatically. Use a separate record for
   each materially different provider/site/process; avoid mixing capabilities.
2. Identify the actual provider/site/process and fill scope from their evidence.
   Add source records to sources, for example an ID, revision/date, project-relative
   evidence path and its SHA256. Cite those IDs from each rule. Keep confidential
   provider documents in the project, not in a public toolkit contribution.
3. For each rule, fill value, unit, applies_to, basis, confirmation and verification.
   Minimum/maximum values are numbers; range is a two-number [minimum, maximum] list.
   For categorical requirements, add a rule with relation "allowed-values", an
   explicit value list and unit "none". Copy a rule card and assign a new stable ID
   for additional limits; distinguish limits from preferred design parameters.
4. List exceptions with exact objects, reason, evidence and genuine approval. Review
   scope and unknowns with the project owner. Changing status to confirmed requires
   actual dated provider evidence; project acceptance is a separate human decision.

The supplied rule cards cover lead pitch, component body gap and stencil thickness.
Add package-specific solder-mask/paste requirements, fiducials, tooling/edge rails,
panel dimensions, rotation/height restrictions and inspection requirements as needed.
Do not infer a universal minimum package from one footprint or a linear package name.

## Make the requirements effective in a project

This file is a capture/review template. The current checker does not parse its rule
cards or compile them into .kicad_dru. To bind it to reviews, add it and the provider
evidence files to hardware.json source_files. They then participate in source snapshots.
Changing only this JSON without the steps below does not create automatic enforcement.

Create requirements.json records for the applicable limits, naming the responsible
owner, affected objects/stage and evidence of verification. Copy unresolved questions
into that contract's unknowns with the same stage blocker; the template's own
open_questions list is not an automatic gate. Use the product-requirements guide
for the existing contract/evidence schema. Requirement evidence must be refreshed
when the provider record, sources or design changes.

| Provider requirement | Verification path |
|---|---|
| Lead pitch / supported package | Check selected component datasheet, land pattern and exact provider process; record review evidence |
| Component body gap, nozzle access, height | Placement/mechanical review using actual body/courtyard/enclosure geometry |
| Paste/stencil apertures and thickness | Assembly/paste-layer review with selected paste and stencil process |
| Panel, fiducials, reflow, inspection/rework | Process checklist with provider confirmation and project evidence |
| A genuinely universal supported copper/drill minimum | Deliberately map to existing product.minimums_mm, review configure diff and validate resulting DRC |

Body gap and lead pitch are not copper clearance. Do not translate them into a global
clearance rule. cad_mapping stays null until an exact supported implementation and
positive/negative KiCad examples exist. If an automatic mapping is needed, propose a
focused toolkit change rather than silently editing generated .kicad_dru. Unsupported
requirements stay explicit manual reviews with evidence, not ignored checks.

assembly.mode remains inhouse or supplier; choosing a local provider does not change
the configuration API. Attach confirmation through the existing assembly evidence
fields (assembly.confirmation_evidence and, for inhouse,
assembly.local_pcba_provider_confirmation). A capability sheet does not
replace confirmed order details, real stage approvals, inspections or bring-up results.
