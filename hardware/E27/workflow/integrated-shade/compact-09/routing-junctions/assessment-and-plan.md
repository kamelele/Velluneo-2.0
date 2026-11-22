# ROUTE03: trace junction and via attachment correction

The owner supplied four enlarged views of remaining defects in ROUTE02. The previous axis/45degree audit passed, but it did not detect tiny grid-anchor steps between parallel diagonals or every offset via/trunk attachment. Those are actual native copper geometries, not raster display artifacts. The new task adds explicit junction checks and magnified native before/after views.

The exact baseline is commitc04198ded93a3d8e1f3ca725176ef723da32d461, nativePCB1dd12e13bf94125f6eff2c59fd72c46a02c56de0f31db9287050db983ddf5bee. All138 source files were copied with hashes before modification. Main remains outside scope.

## Actual baseline findings

- B.Cu DC_RETURN approaches around C1.2 retain two0.1mm steps between diagonal runs. Rebuild the whole incoming branches rather than retaining grid endpoints.
- B.Cu BUS_FILTERED approach near(26.5,22) retains a0.1mm step before its via. Replace the unnecessary intermediate vertices.
- AC_FUSED/AC_N and a coil-force branch contain analogous0.2/0.3mm parallel-run steps and small anchor mismatches. The independent baseline detector identifies six such short steps in total.
- Two via faces lack a trace centreline through the via centre: BUS_RECT near(33.2,2.3) onB.Cu and DC_RETURN near(16.7,20.3) onF.Cu.
- The DC_RETURN via near(21.2,16.0) is attached by a0.2mm lateral stub to the interior of the horizontal trunk at y16.2. This is the protruding-circle case shown by the owner. Align the via with a deliberate trunk junction and adjust its other-face approach.
- One SOURCE width transition0.4/0.6mm is a current-branch geometry, not automatically a defect. Width changes require electrical and visual review rather than blind uniformization. A centred two-leg Kelvin receiver endpoint elbow likewise differs from a side stub into a passing trunk; do not flatten it at the expense of the intended force/sense separation.

## Correction and verification

The private implementer owns `.work/routing03`; root owns later source adoption and publication. Preserve footprint/pad/model/component placements and the existing spatial contract. Use the actual unchanged placement/routing consumer inputs in the surgical adapter and record their digests. Rebuild bounded chains between real pad/via/junction centres with consistent deliberate axis/45 routing, preserving critical functional topology.

Verify all ten vias, all short parallel-run steps, native DRC/parity/connectivity, independent55pair spacing and actual Kelvin intersections. Generate magnified native closeups at the four reported regions as well as whole-board views. Four separate read-only roles inspect the same frozen final packet. Record engineering readiness separately from the still-open genuine human, physical, process and full-product release gates. No order or powered test is authorized.
