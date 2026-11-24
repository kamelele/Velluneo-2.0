# Final Change Review — SC09-SB02-A4

Actor: `/root/sb02_final_change_review`, independent read-only Change Reviewer.
Recommendation: **ready_for_human_review** for the bare, unpowered laboratory PCB candidate. This is not human acceptance, a full Toolkit release PASS, a supplier order or permission for powered testing.

## Exact reviewed revision

- Frozen core manifest SHA256: `286f47ac8239a97d379de4ce4aa3b9d92fe32f6df983ef1b0374216403fe8048`.
- Native PCB SHA256: `c75423f934b637d8b381745e72bed8440eceddb5020b956ee01f4b4426647564`.
- Toolkit source snapshot: `68b76376ff75d3e65fda4f599cb34afc154e4beb188fdfbbc3e87fa9dda95485`.
- All 234 manifest entries were independently hashed, with no missing or changed file.
- Original saved SC09 board comparison base: `a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`.

## Change assessment and fresh verification

This is an architecture change from the original 19-position LYT1603D board, not a routing-only ECO or interchangeable replacement. The candidate has 36 positions, 83 electrical pins and 84 physical copper contacts. It uses LNK3206P, DF10S, a 2.2 mH standard purchasable buck inductor, a 68 uF output reservoir, new optically coupled TL431 current/OVP feedback, an input reservoir and explicit discharge paths. Reference meanings also change: old R7 was a 390k bleeder, while new R7 is the 18.7 ohm current sense resistor. Parts must therefore be assembled using the candidate BOM and drawings, never the old SC09 reference/value list.

The outline changes from 51.2 x 33 mm to 51.2 x 39.5 mm. J1 is at (149.15,118.1) mm and J2 at (102.05,130.449999) mm, on opposite edges as requested. The candidate has no copper zones; the original had one. Source-derived envelope views disclose 22.4 mm height planning and assembly/lead/registration exclusions. No enclosure interchangeability is established.

I independently ran native KiCad 10.0.6 DRC on the frozen candidate with schematic parity, all track errors, all severities, refill and exit-on-violation options. Result: **0 violations, 0 unconnected items, 0 schematic parity issues**. I independently exported a fresh schematic XML and ran the independent intended-connectivity and 190-pair saved-copper checker: **PASS**, including 36 references, 83 pins, both D1 cathode contacts and 32,905 different-net face comparisons. The exact commands' fresh outputs are retained in this review directory.

I inspected actual native values/footprints and the schematic/copper views, and compared the old/new semantic inventory in `semantic-diff.json`. The 2 mm target applies to enumerated high-differential pairs; declared local normal-operation control groups retain 0.3 mm. The placement/routing consumer digests and the spatial check agree on `85a015f724963e0ac256c83f14526828728413bf0ad3eff81a52d3d4d1dd5ff4`. The independent body and dedicated quiet-return reports are bound to the final PCB; no switch-current shortcut through the declared quiet pickup is reported.

The candidate BOM CSV has 36 rows and exactly C9/C10/R18/R19 marked DNP. Manual position data has 32 populated/wire-port rows. All six release artifact types have matching actual hashes and the current source snapshot. The flat manufacturing ZIP contains seven Gerber layers and two Excellon files, without stale job/maps/reports. The source/export audit reports PASS; raw evidence retains the checked mask-flash support and exact-decimal drill comparison controls without enlarging tolerances. These do not prove manufacturing quality or physical operation.

## Findings, limitations and invalidation

No new blocker or major source/export regression was found within the bare unpowered PCB review scope.

1. **Retained process blocker — full release is not accepted.** Current human connectivity/spatial/stage acceptance and the downstream generic inhouse/provider qualification remain absent. The actual full Toolkit report remains FAIL, approvals are empty and waivers are empty. This recommendation must not be presented as full process release or permission to order. The controller change invalidates earlier SC09 map, schematic, placement, routing and release approvals for this candidate.
2. **Minor native-check scope note.** The final DRC lists `track_not_centered_on_via` and `tuning_profile_track_geometries` as ignored project checks. Their explicit entries are absent in the older SC09 project. Therefore “all native rules enabled” would be inaccurate. This is not an observed missing connection: the final independent routing-quality report separately identifies ten adjacent-bevel contacts and the source-bound disposition records a centred final segment for each. Retain that explicit limitation and evidence; do not treat ordinary DRC alone as a via-centering proof.
3. **Verification gap corrected, not concealed.** Root's first export exposed stale/missing actual MPN fields and native Value differences which the earlier Value-as-MPN check and DRC without parity missed. The rejected source/report and expected-fail regression remain evidence. Final metadata/geometry identity reports preserve copper, poses, body drawings and bindings; the final actual-field/Value/DNP comparison and fresh native parity pass. Earlier clean reports must not be reused as equivalent to these final checks.
4. **Models/rendering and revision presentation.** Native bare-board renders do not show attached bodies; the populated views are explicitly labelled deterministic engineering envelopes. They do not qualify vendor model accuracy, assembly registration or installed fit. The schematic title retains its graph-family draft revision while the full packet identifies A4 and hashes its exact bytes; neither should be called a released production revision.
5. **Retained powered boundaries.** Nonisolated output, shared feedback, D2-open behavior, main-switch short, near-short bias collapse, inrush endurance, hot feedback authority, dynamic OVP, stability, temperatures and efficiency remain unqualified as disclosed. Bare-board checks and the conditional RC calculations do not establish safe handling or powered-test readiness. These require separately defined responsible-person/setup/limits and measurements.

Any source, component, rule, body contract, outline or manufacturing-artifact change invalidates the affected checks and this exact-manifest recommendation. My writes are confined to this review directory; no CAD, source configuration, frozen core, supplier state or Git branch was modified.
