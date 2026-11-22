# SC09-ROUTE03 surgical routing handoff

Actual implementer: `/root/route03_writer`. CAD lease is relinquished with this handoff; the coordinator may now adopt and independently verify the candidate. No active customer CAD, main, order or powered test was changed by this implementer.

Base: current customer ROUTE02, commit `c04198ded93a3d8e1f3ca725176ef723da32d461`, PCB SHA256 `1dd12e13bf94125f6eff2c59fd72c46a02c56de0f31db9287050db983ddf5bee`.

Final private PCB: `.work/routing03/SC09_compact.kicad_pcb`, relative to Velluneo-2.0.

SHA256: **`fc2bf0f2e865e23579180fee47f635079a686d576bb84a882f9e91ac462f29fc`**.

## Exact scope

Only PCB copper routing, four via centres and front revision text R02→R03 change. Footprint positions, pads, parts, local libraries/models, schematic, intended physical graph, board dimensions/layers, configuration and selected spatial basis remain byte-identical to the base. Root should adopt only the PCB. The same actual routing consumer was read by `surgical.py`: `998c72be2210e7a57131e627e2c0e62128d31ab9e2c0ef09bd397a2aee28e749`. No configure apply was necessary because no managed setting or spatial intent was altered. Root must verify its own no-op preview after adoption.

The new exact full-copper UUID/purpose/geometry map is `seed-authoring.json`. It distinguishes new, retained and moved-via geometry. All original Kelvin objects and their geometry remain unchanged. It is a current full map, not a claim every retained piece was authored this turn.

## Corrections

- Rebuilt BR1/C1/C4 DC return as whole clean consistent-width runs, removing both .1mm diagonal stair steps around C1. Small cardinal approach pieces are wholly inside actual component lands, so the saved copper union has clean visible45degree arms without grid crumbs. The horizontal upper return is y2.25mm to preserve the full2mm C1BUS spacing at0.4mm route width.
- Rebuilt BR1/MOV phase and neutral paths from real terminal centres, removing .025/.05mm mismatches and .2/.3mm parallel stairs. Neutral is consistently0.3mm, matching its already0.3mm trunk and unchanged POWER minimum; no manufacturing or functional-spacing floor was reduced. Its actual feasible corridor passes the full55pair screen.
- Rebuilt the drain/C4 path and lower BUS_FILTERED via approach, removing its .1mm stair. Rebuilt the R5-to-diode force branch to remove the .3mm stair; the physical R5 Kelvin takeoff is unchanged.
- Removed the .1mm LED-body-corner stair, used a deliberate0.5mm chamfer, and placed the bleeder branch junction exactly on its main45degree centreline. R7LED and C6 terminal entries now use actual pad-centre approaches rather than rounded grid anchors.
- Removed duplicated-in-area M/source-reference routing while preserving their functional branch topology and current-carrying widths. The remaining SOURCE0.4/0.6mm width transition at(14.6,6) is an intentional power-branch junction, not an unexamined cosmetic defect.
- Moved BUS_RECT via `16adb991...`: (33.199999,2.3)→**(33,2.325)**, exactly matching its BR1escape and new F45 approach.
- Moved drain via `8c91fc85...`: (26.9,9.575)→**(27.1,9.6)**, giving a direct F45line to C4 and a short in-pad U1escape.
- Moved DC diagonal via `cb0de63c...`: (16.7,20.3)→**(16.5,20.1)**, exactly on the passing F45centreline, with its Bbranch adjusted45.
- Moved D1 DC via `d355cf10...`: (21.2,16)→**(21.2,16.2)**, exactly on the F horizontal trunk; removed its .2mm side spur. The via remains inside its own B D1 pad.
- Kept the properly centred Kelvin receiver endpoint elbow at(22.2,6.2). Flattening it merely for appearance would reduce separation from the coil force via. It is a normal two-leg endpoint approach, not an off-centre interior side spur.

## Actual checks on final PCB

- `final-DRC.json`: native KiCad10.0.6 all severities, **0 violations,0 unconnected,0 schematic parity errors**.
- `final-spacing.json`: unchanged full55-pair bounded engineering screen **PASS**. No package concession, rule floor or geometry exception changed.
- `final-junction.json`:10vias, **0 off-centre faces,0 short parallel stair steps,0 short via-to-interior-trunk side spurs**. One width-step review candidate is the intentional SOURCE branch described above; it is not a geometry-gate failure.
- `final-angle.json`: **0 non-axis/non45 tracks outside pads,0 acute tips,0 duplicate segments,0 collinear merge candidates**; AC/LED edge placement remains unchanged,46.8mm terminal-centre separation.
- `final-metrics.json`: unchanged physical pin graph and values; **Kelvin PASS**,14 per-face native objects, no additional join outside R5; SOURCE pours remain0. This shared metrics utility retains its author/root actor constant: its actual invoker for this private report was this implementer, not an independent coordinator review.
- Final inventory: **114 segments,10vias,331.96777355mm total track length**. Previous ROUTE02 had128segments/10vias/332.80879048mm.
- Actual native two-layer PDF and PNGs were exported and visually inspected (`layers.pdf`, `layer-0.png`, `layer-1.png`); the reported tiny steps and off-centre rings are removed from the saved copper views.

No physical temperatures, efficiency, EMC, fault, insulation or supplier process qualification were performed. Full Toolkit human/physical/process release gates remain open. This handoff is an engineering candidate receipt, not human stage approval or permission to order/energize it.
