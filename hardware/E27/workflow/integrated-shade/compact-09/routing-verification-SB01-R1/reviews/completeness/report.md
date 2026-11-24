# SC09-SB01 R1 final completeness review

Actor: `/root/sb01_r1_final_completeness`. Independent read-only review of frozen
core manifest SHA256 `97f362117453cb296a588d0d835dfad7a4bea9931d2c35bd32300ecc238c462f`.
PCB SHA256 `532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.
Toolkit snapshot `f834905c883e608cee4dc5f8d8050f7689bdafa138911e3820f9d6d3b3f0c692`.
No CAD, rule, source metadata, manufacturing file or frozen-core member was edited.

## Recommendation

**ready_for_human_review for the bounded verification candidate only.** No new
technical fabrication-file completeness defect was found. This is not approval
to order, power the board, accept all spacing findings or declare full release.
The complete Toolkit release remains FAIL and the strict spacing comparison
remains FAIL23, as the candidate states. Those are real open gates, not waived
by this recommendation or by the owner authorizing verification work.

## Independent verification and coverage

The structured requirement-to-deliverable coverage table is `coverage.json`.
Detailed actual checks are in `verification.json` and the independently rerun
`fabrication-rerun.json`.

- Verified all 262 frozen-core file hashes before/after inspection, with no
  mismatch. The native KiCad ZIP has 155 entries exactly matching the source
  files intended for delivery. A tool-generated, untracked `.kicad_prl` preference
  file is outside the manifest and intentionally excluded, consistent with the
  original archive policy; it must not become a published design input.
- Verified six hardware release artifact kinds, each actual SHA and the same
  snapshot binding. The current root copies and source release-refinement-R1
  files agree. Historical release-candidate files are explicitly retained as
  historical and must not be ordered.
- Verified the flat candidate manufacturing ZIP contains exactly seven Gerber
  layers and one PTH drill file, all byte-identical to the audited raw exports.
  The raw NPTH file has zero coordinate hits and its omission is explicit. No
  raw `.gbrjob` finish ambiguity is carried into the supplier ZIP.
- Independently reran the provided fabrication comparison on the frozen native
  PCB and raw exports. Copper, pad/via flashes, outline, drills, mask processing
  and the selected geometric fabrication checks pass. Inputs stayed unchanged.
- Parsed the BOM and manual positions: exactly 19 references, 17 populated
  electronic components, two wire ports and zero DNP positions. All actual BOM
  MPNs match the selected canonical SB01 BOM; U1 is LYT1603D and T1 7687709152.
  The positions are correctly described as manual references, not qualified PCBA
  centroid/rotation data. Do not purchase connector bodies for J1/J2.
- Independently compared the 46 intended pin memberships against the fresh XML;
  no mismatch. Inspected the actual-parts check and native ERC/DRC/parity reports.
  Native DRC has zero violations/unconnected/parity findings; its two retained
  ignored keys remain visible and are not represented as all-rule coverage.
- Inspected both-side assembly previews, copper views and the two-page combined
  assembly PDF. The mirrored back view does not change the common top-CAD J1-right,
  J2-left definition. Explicit pin numbers, polarity, coordinates and source graph
  remain the authority for manual assembly.
- Inspected the current unpowered plan. It uses the actual Wuerth T1, KEMET C1,
  HVR25 R7 and other SB01 parts, explicitly excluding old Coilcraft/TDK/VR25
  instructions. It stops before powered testing and retains sample fit, forming,
  vent, wiring, guarded setup and thermal/fault qualification gates.
- Verified both retained populated 3D image hashes and their original review
  manifest. Exact metadata-only source comparison supports retaining geometry/
  model scope; the packet does not falsely call them new populated renders or
  qualified vendor-fit models.

## Findings and limitations

**C-R1-01 — known release blocker, retained.** Full requirements, connectivity/
spatial human decisions and full stage acceptance/provider qualification are
not current. The requirements report has unresolved full-product/interface/
enclosure/safety/thermal/optical items and stale or missing evidence. This packet
does not complete those requirements. Responsible owner: project owner and the
qualified downstream reviewers named before release/physical work.

**C-R1-02 — known spacing blocker, retained.** The strict screen still reports
five intrinsic pad pairs and eighteen adjacent escape observations. A passing
fabrication audit does not close them or prove 230 V safety. Owner/qualified
electrical review remains necessary for any declared acceptance. No global rule,
pad shrink, mask credit or new exception was found in this candidate.

**C-R1-03 — minor assembly presentation.** Some back-side reference text is crowded
around the small resistor cluster, and a few Fab labels sit outside the board
outline. The manual position CSV and numbered pad drawing resolve identity; this
is not a copper/drill defect. An assembly-only annotation cleanup would improve
readability if a later revision is opened, but must get refreshed evidence.

**C-R1-04 — retained physical qualification.** R6 sample/termination fit, RF1/R7/C6
forming/support, C6 vent and lead/solder protrusions, wire strain relief and actual
hot/fault performance are not demonstrated. The 3D images and dimensional screens
cannot replace these checks. No new measurement or operating-temperature closure
is asserted.

This review covers the actual owner request to verify the existing board without
adopting a different circuit. It does not recommend inventing a visible reroute
when the existing routing screens are clean. Four distinct final roles and a
real human decision remain separate from this single report.
