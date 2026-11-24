# Change Review — SB01-FAB-LOCAL-01

Actor: `/root/sb01_r1_final_change`, independent from the current geometry/stress
contributors and coordinator. Recommendation: **ready_for_human_review**, only
for the exact unsigned proposal to manufacture an unpowered, unassembled bare
laboratory test article. This review does not accept a deviation, release a
powered design or authorize a supplier action.

## Frozen inputs and preservation

Assessment core SHA-256:
`1aade033562e650783312af8f588efa42d96a60f6210eb5c00e54e75023ee195`.
Retained R1 core SHA-256:
`97f362117453cb296a588d0d835dfad7a4bea9931d2c35bd32300ecc238c462f`.
Unchanged PCB SHA-256:
`532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.

I independently verified all 21 assessment-core file hashes before and after this
review and all 262 retained R1-core hashes. All eight declared current source
guards match both the actual canonical project and retained R1 source: PCB,
schematic, .pro, .dru, hardware.json, both consumer input files and the exact
Gerber/drill ZIP. No current source, CAD, numeric rule, configuration, circuit,
library or production artifact changed. No approval or waiver was inserted into
the project by the proposal. This review wrote only its own external report area.

## Independent geometry and scope checks

I reran the qualified checker against the guarded current board twice. The fresh
strict report reproduces FAIL23 with no exceptions. The second run with the
explicit proposal reproduces its scoped geometric diagnostic PASS, without
conflating that result with strict or electrical acceptance. All 23 strict
observations are on B.Cu: five pad-pad pairs and eighteen local pad/track or
track/track approaches. Proposed pairs are exactly U1.3/4, U1.2/4, BR1.1/3,
BR1.2/4 and D1.1/2. Only specified pads/tracks and their B.Cu escape portions are
eligible; no via, zone, other layer or blanket net exemption is proposed.

I independently checked literal current land dimensions and controlling pitches:
BR1 pads 1.00 x 2.15 mm at 2.50 mm adjacent pitch; U1 pads 0.60 x 1.45 mm with
1.27/2.54 mm controlling pitches; D1 pads 1.70 x 2.50 mm at 4.00 mm pitch. These
produce the stated nominal 1.50, 0.67, 1.94 and 1.50 mm gaps. The accompanying
primary-land pages and native figure are consistent with this scope. The tiny
numerical remainders are not manufacturing tolerance or usable safety margin.

The clipping/eligibility implementation and source-bound findings were inspected.
Regions are anchored to current native pad polygons, not obsolete BR1 coordinates.
The original targets are retained for outside and cross-region pieces; the fresh
full 55-pair diagnostic has no residual outside-region failure. The 1.0 mm edge
target is retained. Its 0.60/1.80/1.40 mm local values are clearly labelled analysis
parameters, not newly installed rules, qualified electrical minima or guaranteed
finished-board/soldered gaps.

## Artifact, approval and electrical interpretation

The eight-file flat Gerber/drill ZIP is byte-identical to retained R1 and to the
guarded project artifact, SHA-256:
`b722078ed3668e1df757de855754dd7aefc925b9fc8617b28dd7493ece55490e`.
No new Gerbers merely relabel the unchanged geometry. The source-bound fabrication
recheck supports physical fabrication, not energized dielectric adequacy.

`fabrication-only-proposal.json` remains explicitly proposed/not approved;
`owner_approval` is null. Strict spacing, full Toolkit release, powered-spacing
acceptance, operating-stress bound and normative-insulation acceptance are all
false. The scope after an actual owner's acceptance is limited to fabricating and
receiving an unassembled, unpowered test article. Agent supplier action still
requires separate instruction. No elapsed time, review recommendation or earlier
request is fabricated as a signature.

The stress report properly treats M/FB as low voltage only relative to their
moving SOURCE node; the identified gaps can experience high rail-related stress.
It does not use the ideal 357.8 V line crest as an all-operation ceiling. Conditional
706.3/588.7 V filter-screen values are explicitly calculations with unbounded
omissions, not measurements or validated maxima. Semiconductor ratings and
recommended footprints are not substituted for PCB insulation qualification.
Those limitations are carried into the owner-facing assessment and proposal.

## Findings and recommendation

No new blocker or major scope/regression finding was found in this bounded,
unsigned manufacturing-only proposal. The geometry/classification investigation
may be treated as completed for presenting this specific owner decision.

The existing strict FAIL23, absent normative/finished-path acceptance, full Toolkit
process/product gates and powered/thermal/fault qualification remain open. They
must not be presented as closed after the geometry investigation or by this review.
An actual owner's acceptance would apply only to the specified unpowered bare
test article; it must not become a general electrical-clearance waiver or a
claim that the zasilacz is safe to operate. Any source/region/artifact change
invalidates the corresponding bindings and requires affected verification.

Evidence: `verification.json`, `fresh-strict.json`, `fresh-finite.json`,
`commands.json` and `verify.py`, all outside the frozen assessment's own inputs.
