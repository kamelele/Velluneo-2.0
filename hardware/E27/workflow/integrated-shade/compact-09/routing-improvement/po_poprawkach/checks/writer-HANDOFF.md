# Private candidate handoff — SC09-ROUTE01-V2

Writer: /root/routing_candidate_writer. CAD lease relinquished after this snapshot; no active source or main changed by this writer.

Frozen native PCB: `.work/routing-vertical/SC09_compact.kicad_pcb` (relative to Velluneo-2.0).
SHA256: `01ef76ebf14ef111709c2412d31b12fdf4a38cbaea2837654bb9d0d7f0cf5691`.

- Native KiCad10.0.6 DRC: 0 violations (all severities), 0 unconnected, 0 schematic parity issues. `routed-DRC.json`.
- Independent full 55 pair engineering screen: PASS, exact unchanged package floors/margins translated with U1/D1/BR1. `routed-spacing.json` and `package-assessment.CAT01.json`.
- Strict screen without package assessments: FAIL retained, `routed-strict-spacing.json`. This is not IEC/product qualification or manufacture release.
- Actual configure plan `03ce5b2db41403e381a1bc7fee13259ad97dcbe0f59f24f429b763ee38fce8a6`, transaction `9c750544b4dd6b2fb19cb91fdb9c56c53b1cdaac674ba7bb27d26d55e15febec`.
- Both protected seed adapter and generic router actually consumed constraints digest `ee7b1f6cf115827b3cfa2b83505c3bf986e99090ecadc0f78ef72862076245ee`. No digest manually substituted.
- Exact protected route purpose/UUID map: `seed-authoring.json` (48 objects), all UUIDs present in final saved copper, proven by `handoff-proof.json`. Kelvin-purpose routes and FORCE-purpose routes remain individually identifiable. No generic FB route was needed/added.
- 285 native segments and13 throughvias. Generic lowfrequency routes contain short grid stair steps; further visibility-aware simplification is possible, but no blind shortcut has been performed.
- No SOURCE poured zones. C5 both legs directly routed on B.Cu without vias. Source spine moved onto source pin centerline. R5 Kelvin branch remains separate from force routing except physical R5 FB pad (root independent audit required).
- PCB rectangle50x32mm, same19refs46physicalpins11nets and same catalogue parts. C4/L1 rotated whole footprints, J2 whole rotated; R8/R9 moved out of rectifier/filter cluster to B(20,22)/(20,25). Main top cage solved by C6 whole rotation90deg, center(6.25,28.5), bottom leads. Max can body[-.25,2.5,12.75,24.5]mm, vent[-.25,-2.5,12.75,2.5]mm. Conservative bothface body keepout[0,2,13.25,25] and vent[0,0,13.25,2.5] preserved with no exceptions. Maximum material overhang .25mm left means50.25mm material extent, not complete50mm module; fixture requires2.5mm free vent air beyond PCB top. No enclosure approval implied.
- J2 standalone LED/+/- labels relocated to actual port area, >=1mm lettering/.15mm stroke, native DRC clean.
- Approval fields remain null. Missing CAT01/spatial approvals, laboratory tests, thermal measurements and four-role independent reviews remain external release blockers; no waiver/order/safety guarantee invented.

Implementation files: `setup.py` initial only (do not rerun; resets trial), `place.py`, `seed.py`, `generic_stock.py`, `grid_stock.py`, `finalize_basis.py`, `polish.py`; final actual pad net map and fixture limits are in `handoff-proof.json`. Generated consumers are under candidate `.electronics-rules`. No dependency or active customer files edited.
