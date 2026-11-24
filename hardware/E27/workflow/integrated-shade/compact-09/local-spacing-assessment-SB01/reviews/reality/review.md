# Review report — SB01-FAB-LOCAL-01 / Reality Checker

- Actual actor: `/root/sb01_r1_final_reality`, independent from both geometry and
  electrical-stress contributors and from the native CAD implementer.
- Frozen assessment core SHA256:
  `1aade033562e650783312af8f588efa42d96a60f6210eb5c00e54e75023ee195`.
- Retained R1 core SHA256:
  `97f362117453cb296a588d0d835dfad7a4bea9931d2c35bd32300ecc238c462f`.
- Retained PCB SHA256:
  `532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.
- Exact unchanged fabrication ZIP SHA256:
  `b722078ed3668e1df757de855754dd7aefc925b9fc8617b28dd7493ece55490e`.
- Scope: review of the unsigned, exact-source fabrication-only disposition for
  an **unassembled, unpowered bare laboratory PCB test article**. No new board,
  controller, component, track, rule or manufacturing file is adopted.
- Recommendation: **ready_for_human_review** for that narrowly bounded proposal.
  This does not grant manufacturing/order approval, close the strict screen or
  demonstrate that the board can safely operate at mains voltage.

## Independent checks and retained scope

I verified all 21 assessment-core hashes before and after review, all eight live
source guards against the current canonical project, and all eight corresponding
R1 source files. The complete 262-file original R1 core is also still unchanged.
Its prior graph/actual-MPN/ERC/DRC/geometry/fabrication review scope can therefore be
retained explicitly; no new electrical function is inferred from this assessment.
The primary evidence hash list, including the selected datasheets, reference
report and older filter-screen inputs, matches the actual local files.

I visually inspected all three included primary land drawings, then independently
checked literal native pad sizes and pitches. BR1 matches MB10S's 1.00 x 2.15 mm
lands at 2.50/5.35 mm centers. U1 matches PI's 1.45 x 0.60 mm SO8 reference lands,
1.27 mm pitch and 5.45 mm opposing-row centers. D1 matches the US1A–US1M family's
2.50 x 1.70 mm lands at 4.00 mm centers. These dimensions explain the nominal
1.50/1.94/0.67 mm gaps without requiring a footprint-copying error.

I ran my own fresh strict and finite-geometry checks with the qualified checker.
The strict result remains FAIL with exactly 23 observations. The finite diagnostic
passes all 55 net-pair checks. I separately inspected each of the 23 actual object
pairs: each maps uniquely to one eligible B.Cu package region, neither member is a
via or zone, and clipped outside/cross-region comparisons leave no residual at
the original targets. The proposal keeps the 1 mm edge target; the CAD minimum is
about 1.05 mm. It does not exempt a complete long track or a whole high-voltage net.
Its local 0.60/1.80/1.40 mm values remain diagnostic parameters, not accepted
electrical minima. The small numerical remainders are not fabrication precision.

This establishes the proposed scope of a manufacturing disposition and the
classification of the 18 escape entries. It does not establish a safe assembled
creepage/clearance, permissible pollution/CTI/altitude, or guaranteed finished gap.
The raw strict FAIL23 must remain accessible alongside the scoped diagnostic PASS.

## Electrical reality check

The stress interpretation is consistent with the retained high-side buck graph.
BR1.1/3 spans the rectified input rail; BR1.2/4 spans the AC input. U1 M and FB are
local low-voltage signals only with respect to moving SOURCE. During the OFF/
freewheel interval their differential to DRAIN is near the high filtered rail.
D1's cathode follows the high side in the MOSFET ON interval and experiences high
reverse stress. These are not low-voltage PCB gaps simply because one terminal
is a feedback pin.

I recalculated the ideal 253 VAC sine crest as 357.796 V and inspected the actual
47-ohm filter-screen data: the conditional maxima are 706.299 V at C1 and
588.698 V at C4. The packet accurately calls these older calculated scenarios,
not measured waveforms or upper bounds. The idealized initial-charge, bridge,
L1-DCR, nonlinear-inductance, MOV/source and load assumptions prevent treating
them as exhaustive startup/surge/fault qualification. A generic 400 V screen is
not an established maximum under those cases.

Neither the IC's 725 V device rating, the rectifiers' 1000 V ratings, nor a suggested
manufacturer solder pattern assigns those ratings to the external PCB gaps. The
packet makes no such transfer and supplies no invented normative minimum. No
electrical evidence here closes the existing powered-insulation question. Actual
stress/finished soldered geometry and applicable insulation conditions still need
qualified assessment and guarded validation before energization.

## Findings, owners and observable closure

No new blocking technical defect was found in the **unsigned fabrication-only
proposal**. The following gates are retained openly:

1. **LOCAL-REALITY-OWNER — pending human disposition; fabrication/order gate.**
   `owner_approval` is null, strict spacing remains FAIL23, and full Toolkit release
   remains FAIL. The current assessment request is not a signature. Owner: the
   actual project owner/authorized human reviewer. Closure: a real decision bound
   to proposal SB01-FAB-LOCAL-01, its exact source/ZIP hashes and its unassembled,
   unpowered test-article scope. It must not be described as a powered safety waiver
   or a passing full Toolkit release. Supplier action remains separately instructed.
2. **LOCAL-REALITY-POWER — existing major; energized prototype/product gate.**
   The maximum operating/startup/fault stress and finished-board insulation
   adequacy are unknown. Owner: qualified electrical reviewer and test investigator.
   Closure: applicable, justified insulation/stress basis and actual identified
   assembly, safe setup, limits and evidence at relevant operating/fault corners.
   This assessment closes classification/containment, not that electrical gate.
3. **LOCAL-REALITY-ASSEMBLY — existing open physical qualification.** Etched feature
   edges, solder fillets, leads, component placement/forming, contamination and
   environment can change real paths. No guaranteed tolerance stack has been
   provided. Owner: assembler and qualified reviewer. Closure: incoming/assembled
   inspection and applicable measured/qualified finished-path evidence. Solder
   mask is not assigned protective credit.

It is reasonable to present the exact bare-board manufacturing proposal to its
owner: the footprints conform to selected suggested lands, the closeness is
bounded and exposed, and the unchanged article has current fabrication audit
evidence. That reasoning supports making an unpowered test article for inspection;
it does not answer whether an assembled article will operate safely at 230 V.

## Invalidation and limitations

No source, CAD, rule, core file, Gerber or ZIP was modified by this reviewer. The
prior R1 Reality report's graph/layout/thermal-uncertainty scope remains retained
by exact file identity. This report adds the finite classification and stress
interpretation only. All prior physical-performance and full-process gates remain.

Any change to guarded sources, the five exact regions/object sets, the proposed
meaning of local values, or the ZIP invalidates the affected recommendation.
Fresh independent evidence is in `verification-summary.json`, `strict-rerun.json`,
`finite-rerun.json` and `verify.py` in this external review directory. An agent's
recommendation, including this one, is not human acceptance or supplier authority.
