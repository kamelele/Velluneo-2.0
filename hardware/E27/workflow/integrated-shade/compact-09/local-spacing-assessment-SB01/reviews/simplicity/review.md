# SB01 local-spacing proposal — final Simplicity review

Actor: `/root/sb01_r1_final_simplicity`, independent read-only Overengineering
Reviewer. This actor did not author the geometry/stress assessment, proposal or
source. Output is outside the frozen core; no CAD, configuration, rule, core or
supplier state was changed.

Core manifest SHA256:
`1aade033562e650783312af8f588efa42d96a60f6210eb5c00e54e75023ee195`.
Exact PCB SHA256:
`532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.
Exact unchanged candidate ZIP SHA256:
`b722078ed3668e1df757de855754dd7aefc925b9fc8617b28dd7493ece55490e`.

## Recommendation

**ready_for_human_review** for unsigned proposal `SB01-FAB-LOCAL-01`, strictly
limited to fabrication/purchase of this exact **unpowered, unassembled bare PCB
laboratory test article** and its unpowered receipt inspection. No new simplicity
blocker or major scope ambiguity was found. This is not an accepted deviation,
manufacturer order, powered-use approval, normative clearance finding or full
Toolkit release recommendation.

## Independent checks

I verified all 21 frozen core file hashes, the manifest identity, all eight source
guard hashes against the actual current project, the candidate ZIP identity and
the retained R1 core-manifest hash. There were no mismatches. My prior independent
R1 simplicity review remains retained for the unchanged 19-position circuit,
two-layer 51.2 x 33 mm PCB, actual MPN correction and source/artifact bindings.
The new stress/geometry reports and unsigned decision proposal were inspected
independently for this review, not assumed covered by that earlier review.

The proposal, source guard, exact pair/region report and annotated native geometry
view agree on the same five fixed land pairs. The geometry contribution retains
the strict FAIL23, anchors the eighteen escape observations to five finite B.Cu
regions and reports the original outside/cross-region targets and 1 mm edge target.
No whole-net, via, zone or other-layer concession is proposed. I inspected the
assessment script's finite-region specification and the separate strict/scoped
result identities. The local numerical values are explicitly diagnostic parameters;
the proposal installs no lower electrical design floor or native rule.

## Simplicity and scope assessment

The proposal is an appropriate way to present one concrete owner decision while
keeping the existing board. A different controller, altered manufacturer lands,
larger board or broad reroute would change the object under assessment and impose
new schematic, sourcing, layout and verification work. Such a redesign is neither
required nor justified merely to manufacture an inert bare test article under the
proposed scope. No additional electrical component or software abstraction is
introduced, and no existing protection or verification is removed.

The manufacturer-land conformity finding is correctly narrower than dielectric
adequacy. In particular, the M/FB nodes are not misclassified as harmless low-voltage
control gaps relative to DRAIN. The ideal 357.8 V crest and conditional 706.3/588.7 V
filter calculations are not represented as actual measurements or all-operation
limits. Component voltage ratings and recommended lands are not used as external
PCB insulation certificates. This avoids a false simplification of the qualification
problem while still allowing a bounded fabrication-only proposal to be reviewed.

The existing ZIP is reused with an exact hash and source guard. Generating another
Gerber set solely to make the spacing result appear new would add maintenance
burden without a geometry change. A single, explicitly scoped owner acceptance is
more concrete than repeating general approval questions about unchanged sources.

## Conditions that must remain visible

- The proposed owner decision does not turn strict FAIL23 or full Toolkit FAIL
  into PASS. The source and artifact hashes, exact five pad pairs and eighteen
  escape objects must remain bound to any actual acceptance.
- Manufacturing acceptance is limited to an unassembled, unpowered test article.
  It does not establish the actual soldered paths, startup/surge/fault stress,
  CTI/pollution/altitude applicability, assembled insulation or powered performance.
- `owner_approval` is null and the proposal is unsigned. The current assessment
  request is not itself recorded as approval. Supplier action by the agent still
  needs the separately stated instruction; no action follows merely from time.
- The owner-facing answer should state that the geometry investigation is closed
  for this decision, while powered electrical qualification remains open. It must
  not say the five small gaps became 2 mm, that 23 routing defects were repaired,
  or that the complete zasilacz is qualified for use under 230 V.

There is no further component deletion, controller substitution, layout expansion
or rule relaxation recommended by this reviewer. The bounded proposal is suitable
for the one explicit human decision described above; all other release and powered
qualification gates remain separate.
