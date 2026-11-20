# Scoped policy compatibility candidate

Version 0.7.2-velluneo.1 is a separately versioned project compatibility candidate,
based on the public 0.7.1-preview.3 source. It is not an accepted upstream release.

Supported scope: exact-net symmetric clearance pairs, rectangular protected areas
on canonical two- or four-layer copper stacks, stronger-only board/ERC severity
overrides, and source-hash-bound adoption of a bounded legacy clearance grammar.
No wildcard conditions, layer-dependent legacy clauses, arbitrary constraints,
six-layer stacks, insulation certification or supplier approval are inferred.

`hardware.product.scoped_clearances` contains objects with `id`, `nets_a`,
`nets_b`, `min_mm`. Groups must be disjoint and name actual saved board nets.
`hardware.product.copper_layers` may be `["F.Cu","B.Cu"]` or
`["F.Cu","In1.Cu","In2.Cu","B.Cu"]`. `hardware.severity_overrides`
contains `board` and/or `erc` dictionaries; only existing rules at equal or
stronger severity are accepted. Profile global limits remain enforced.

`hardware.configuration_migration` names a JSON descriptor containing exactly
`schema_version:1`, `legacy_rules_sha256`, `legacy_project_sha256`, `net_names`,
`reviewed_by` and `reason`. Hashes bind the actual pre-apply files, not an old
unrelated checkpoint. The reviewer records a mechanical policy-preservation
review, not human product approval. Configuration preview independently parses
the actual generated output, checks all ordered existing nets plus empty/unknown
categories, refuses weakening, preserves explicit native minimums/severities and
ERC matrices, and writes the proof through the normal transactional apply.
An ownership record cannot authorize removing a scoped rule. Unsupported or
ambiguous legacy grammar remains a conflict. Never edit the installed cache.

The added four-layer filled/capped-via service is a capability candidate only.
Supplier confirmation of the exact stack, via treatment and files remains required.
The conventional service is unchanged. Human stage/process gates are unchanged.

Validation uses KiCad 10.0.6 and its matching pcbnew runtime. Unit and synthetic
native cases include actual 3 mm/10 mm violations, both inner-layer exclusions,
and stack mismatch rejection. Clean extracted candidate validation records the
actual host and results; this change has not been exercised on Linux. Synthetic
fixture approvals never approve a customer design or manufacturing process.
