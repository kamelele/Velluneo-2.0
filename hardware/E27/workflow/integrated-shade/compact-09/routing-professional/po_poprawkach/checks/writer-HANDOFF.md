# SC09-ROUTE02 private candidate handoff

Actual implementer: `/root/routing02_writer`. The coordinator has ended the implementer's CAD lease; `/root` is now the sole CAD/configuration/library writer. This handoff document is the implementer's only subsequent write. No active customer source, main, order or powered test was changed by this implementer.

Last implementer-verified candidate: `.work/routing02/SC09_compact.kicad_pcb`, relative to Velluneo-2.0.

SHA256: `1dd12e13bf94125f6eff2c59fd72c46a02c56de0f31db9287050db983ddf5bee`.

## Completed design changes

- Same50x32mm/two-layer/1.6mm board,19references/46physicalpins/11nets. Functional BOM, schematic, intended physical graph and CAT01 source basis remain byte-identical to ROUTE01. No purchased parts were added.
- J1 AC input is at the right edge, both pad centres x48.4mm. J2 LED output is at the left edge, both centres x1.6mm. Both use y24.5/30mm; closest AC-to-LED pad-centre separation46.8mm. Canonical and embedded port footprints now have straight5.5mm pitch,2x2.5mm rounded-rectangle bare wire lands. No connector body or new MPN is implied. Pin/net/polarity identities, schematic linkage, values and truthful inherited MPN/Datasheet fields were preserved. The assembly metadata fields are hidden on B.Fab.
- C6 anchor(6.75,26), native angle90deg. Maximum can[.25,0,13.25,22]mm is entirely within the PCB footprint. The full5mm vent reserve is external above the PCB and must be supplied by the fixture. Both-face body projection[0,0,13.75,22.5]mm is protected without net exceptions. The now wholly external vent region was deliberately removed from native board areas, not waived inside the board.
- R5/R6/U1/C5/R4 moved0.5mm east together. RF1 centre is(43,28.4). Other principal functional placement is retained.
- All128 track segments are nominal axis/45deg. Ten throughvias; total332.80879048mm of tracks. No arbitrary-angle line-of-sight shortcuts were used. Final geometry audit reports0 outside-pad non45 tracks,0 acute two-track tips,0 duplicates and0 collinear merge candidates. Generic grid stairs were replaced by guarded axis/45 paths and manual few-bend routes; exact collinear unions removed14 further fragments.
- The long front BUS_FILTERED path is a six-leg axis/45 route with simple bends. T1-to-R7 LED routing is one main45run plus horizontal/pad approach. B.Cu AC_N has one symmetric0.5mm offset with0.5mm45chamfers: an exact horizontal y24.5mm trial failed RF1.2 spacing at1.700mm against2mm. The clean offset is necessary; no floor was weakened and RF1 was not crowded upward merely for appearance.
- Broad SOURCE pours remain absent. C5 BP/SOURCE bypass legs are direct on B.Cu. A real same-net Kelvin-via/T1.2 overlap was caught and corrected: the R5 takeoff via is now(16.5,5.2). The final saved-copper audit finds no force/sense join outside physical R5.2.
- Front board lettering was changed from SC09 CAT to SC09 R02; functional circuit remains CAT01.

## Last actual checks

`final-DRC.json`: native KiCad10.0.6, all severities,0 violations,0 unconnected,0 schematic parity issues.

`final-spacing.json`: full55-pair bounded screen PASS; unchanged finite package floors/margins, with U1 exception boxes translated0.5mm east with the unchanged pads.

`final-angle-audit.json`: geometry acceptance PASS, actor explicitly `/root/routing02_writer`.

`final-metrics.json`: physical graph/values unchanged, no SOURCE pours, KelvinPASS with14 per-face native copper objects and all declared critical UUIDs present. The shared metrics utility contains its author/root actor string; **its actual private invoker was this implementer**. This is not an independent root review. Coordinator must rerun the final evidence independently.

The exact protected critical UUID/purpose map is `seed-authoring.json`; the Kelvin subset was updated after correction. No subsequent collinear merge removes any protected object. Actual manual and exact-collinear operations are recorded in `manual-polish-proof.json` and `collinear-proof.json`.

## Configuration and actual adapter inputs

Reviewed/applied configure plan:
`5fbd61b85c47a65a299c21b8b060b35e4a2e71edbc9ec20070a370a8ad2f50be`.

Transaction:
`1995ddeb011b976faf2e7d195dd992a21c0b986225d0a24241d347a06d44a061`.

The diff changes the C6 body projection and removes only the wholly external vent area. Native/global floors, package concessions and severities remain unchanged. Last configure preview `fc06fee1d2929101bc9e57e74db72e742df85752d513312f28cbbde3edb67aae` was generated; the coordinator should verify its saved diff rather than assume a no-op.

Actual routing consumer digest read by seed and generic adapters, also read/recorded by manual polish:
`998c72be2210e7a57131e627e2c0e62128d31ab9e2c0ef09bd397a2aee28e749`.

Generated placement/routing consumers are in the private project's `.electronics-rules` directory. Spatial basis sources are the explicit planned C6/port geometry and canonical footprint-geometry record. Approval remains null; no human acceptance was invented.

## Execution and remaining limits

Actual implementation sequence: `setup.py`, `fix_fields.py`, configure preview/apply, `seed.py`, `generic_stock.py`, guarded45-only `polish.py`, `manual_finish.py`, `fix_kelvin.py`, `merge_collinear.py`. Do not rerun setup on the frozen candidate without intending to reset it. Intermediate failures and final reports are retained for traceability.

Mechanical source changes include both canonical port footprints, embedded port instances, `footprint-geometry.json`, `routing-improvement-basis.json`, selected `spatial-constraints.json`, generated rules/consumer state and PCB. Functional schematic/BOM/graph/library/model assets outside those two bare-port footprints are unchanged. Current placement changes and external5mm vent requirement are this handoff's authority; copied historical ROUTE01 workflow/source prose needs coordinator supersession.

Strict default geometry, exact human graph/spatial/stage decisions, provider/process confirmation and physical electrical/thermal/fault/surge/EMC/insulation tests remain separate open gates. No strict PASS, certified fit, product approval, safe powered operation, stock reservation or order is claimed. Export refresh, source adoption, independent role reviews, archives and GitHub publication remain coordinator work.
