# Independent pin-table example and actual KiCad fixtures

basis.md is an original fictional table, authored independently of CAD geometry.
intended-connectivity.json records the expected graph and has no human approval.
It cannot pass a production check without a real authorized decision. Never use test
approval helpers on a real project.

The fixture contains two units of U1, connector J1, three pin-pair nets and two NC pins.
N1/N2 must stay electrically separate; this is not an insulation requirement.
Symbols are fictional passive, excluded-from-board fixtures, not real part definitions
or a manufacturing-ready PCB.

Generate/export the original positive fixture in an ignored directory:

    python tests/connectivity_cad.py

It creates .work/connectivity-example with synthetic test approval and runs actual
KiCad comparison. This does not approve any real design. CLI requires KiCad 10.0.6;
the fixture generator uses standard Python.

The full tests/integration.py suite generates independent geometry variants:

| Variant | Expected independent result |
|---|---|
| valid | Matching unit/pin graph and explicit NC |
| renamed | Same graph passes despite a changed KiCad label |
| merged | Merged nets and breached declared separation |
| split | Intended pin pair appears on distinct actual nets |
| wrong-pin | Swapped physical pins cause graph differences |
| omitted-unit | Missing instance count plus missing graph/NC evidence |
| missing-nc | Isolated but unmarked NC fails |
| connected-nc | Intended NC pins joined electrically fail |

Expected topology comes from the independent table, never an exported variant.
Only test setup supplies synthetic approval. The merged case runs full work checks
and demonstrates clean ERC and DRC/parity alongside failing intent comparison.
Release tests cover complete synthetic contracts and missing/stale intent.

