# Final Change Review — SC09-SB01 R1

Actor: `/root/sb01_r1_final_change`, an independent read-only review context,
separate from the CAD writer, coordinator and baseline diagnostic contributors.
Review recommendation: **ready_for_human_review**, strictly for the existing,
unpowered laboratory PCB verification packet. This is not approval to manufacture,
order, assemble under a qualified process, energize or release a finished lamp.

## Exact reviewed input

- Frozen core manifest SHA-256:
  `97f362117453cb296a588d0d835dfad7a4bea9931d2c35bd32300ecc238c462f`.
- Candidate PCB SHA-256:
  `532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.
- Candidate schematic SHA-256:
  `16cbd188b02399d2eecd0965939a2f07cda1e96a40c45574b9d7d791a0ff22a4`.
- Toolkit snapshot:
  `f834905c883e608cee4dc5f8d8050f7689bdafa138911e3820f9d6d3b3f0c692`.
- Baseline PCB:
  `a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`.

All 262 core file hashes were independently verified before and after inspection.
The original packet and authoritative CAD were not changed. Native verification
used a byte-verified private source copy inside this review's own output directory;
any generated private preferences are not design inputs or publication artifacts.

## Independently verified change scope

Exact normalized text comparison proves that the PCB and schematic each contain
only one U1 MPN-property replacement, `LYT1603D-TL` to `LYT1603D`. Both human-readable
values, every circuit connection, copper object, placement, pad, model binding and
board drawing are otherwise identical. This aligns the inherited purchasing field
with the already selected tube-packaging BOM; it introduces no new controller or
electrical part. The 19 positions, 46 physical pin memberships, 11 nets and
51.2 x 33 mm outline remain unchanged.

Five of the 149 baseline source paths differ: the two native files, `hardware.json`
and the two generated placement/routing consumer-input files. No other baseline
source differs. Hardware changes are confined to `release_files` and its historical
release note. Both generated inputs differ only in their intent and constraints
digests; after removing those two digest fields, their complete numeric limits,
regions, block cards and other content are identical. Native `.pro` and `.dru` are
byte-identical. The new consumer digest matches the current spatial report, whose
remaining error is actual missing human acceptance rather than a consumer mismatch.
Recording a consumer digest is not evidence that an external router ran.

The shorter L1-to-C4 trial is not present in the candidate. Its reported crossing
cannot have been accidentally integrated: the exact native-source text comparison
excludes every copper edit. The final user-facing description must say that routing
was verified and retained, not that these tracks were rerouted or improved.

## Fresh checks and artifact binding

The review independently ran native KiCad 10.0.6 ERC and DRC with all severity,
all-track-error and schematic-parity options. ERC, DRC violations, parity issues
and unconnected items are zero. A fresh reviewer XML export and actual native pad
memberships each match the independently prepared SB01 intended connectivity:
46 pins, 19 references and 11 nets. Actual native MPN properties and fresh schematic
MPN fields match the selected electronic BOM; Value parity and populated flags
also match. The exported purchasing BOM has 19 rows and U1 `LYT1603D`; the manual
position file has 19 rows including wire ports.

Six current release-artifact kinds independently match their actual hashes and
the declared source snapshot. The KiCad ZIP contains exactly the 155 declared
source/release entries, with each byte hash matching the packet. The supplier ZIP
contains exactly eight flat files, seven Gerber layers and one PTH drill file;
all match the current raw exports. The empty NPTH and `.gbrjob` are not supplied as
extra fabrication layers. The separate core fabrication audit passes. Inspection
of the current copper and assembly views found no new semantic reversal or
placement change. AC and LED ports remain on opposite edges, with the bottom
assembly view explicitly mirrored.

The unpowered inspection plan identifies the actual Wuerth 7687709152 coil,
KEMET R76 capacitor, selected MOV, fusible resistor, US1M diode, Royalohm R6 and
HVR25 R7. It explicitly prevents older Coilcraft/TDK/VR25 instructions from being
treated as current. Old source and release records remain historical rather than
silently being relabelled as accepted. Retaining the earlier populated 3D views is
justified for their stated appearance scope by exact geometry/model identity and
the original image hashes. They are not claimed as new populated renders or
qualified physical-fit models.

## Findings and retained limits

No new blocker or major CAD/export regression was found in this bounded change.
The following existing limits must remain visible and are not closed by this review:

- **Strict spacing FAIL23 remains.** Five fixed package land pairs and eighteen
  local escape observations at BR1/U1/D1 are not repaired by the metadata change.
  No exception was applied to the fresh strict report. Native manufacturing DRC
  with a 0.3 mm floor does not demonstrate compliance with the separate 2 mm
  functional screen. Fixed land gaps cannot be enlarged by rigid relocation or
  cosmetic routing. The user's return to this design is not a standards waiver.
- **Full Toolkit release remains FAIL.** Existing product/physical evidence,
  current human stage/intent/spatial decisions and downstream assembly-provider
  confirmation are still missing. Clean native checks and new artifact bindings
  do not authorize acceptance or ordering. Scope must not be expanded to a powered
  or finished-product release.
- **Native default ignored checks remain explicit.** The raw DRC lists
  `track_not_centered_on_via` and `tuning_profile_track_geometries` as ignored.
  These settings were not altered by this change. The independent routing-quality
  and topology evidence is separate; do not claim every native rule type ran.
- **Minor pre-existing assembly-drawing clarity:** R6/R7 reference text is crowded
  in the bottom assembly view. Use the BOM, manual position file and actual land
  mapping together during inspection. This is not a new electrical or copper
  regression, and it does not justify a board redesign in this task.
- Manual lead forming/support, R6 sample fit, capacitor vent space, actual soldered
  clearances, temperatures, hot magnetic behavior and fault/surge response remain
  unqualified. No physical measurement is inferred from the drawings or hashes.

Changed native purchasing fields and current artifact/configuration bindings need
the applicable exact-source human review. Earlier geometry-only observations and
appearance views may retain only the explicit unchanged-geometry scope. Existing
finished-product, powered-test and manufacturing acceptance cannot transfer merely
because the graph is unchanged.

Evidence generated by this review: `verification.json`, `commands.json`,
`fresh-ERC.json`, `fresh-DRC.json`, `fresh-netlist.xml` and `independent_check.py`.
These reports are outside the frozen core's own source inputs. No supplier action,
main-branch write or design acceptance was performed by this reviewer.
