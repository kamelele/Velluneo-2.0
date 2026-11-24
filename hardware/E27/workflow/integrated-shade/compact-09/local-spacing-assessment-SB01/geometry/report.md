# Current SB01 local spacing geometry assessment

Actor: `/root/sb01_spacing_geometry`, read-only technical contributor, not a final
reviewer of this contribution and not an authorized human waiver approver.

Current saved PCB SHA256:
`532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.
The source was not saved or modified. No native/custom rule, numerical project
limit, manufacturer land, routing, via, zone, MPN or placement was changed.

## What is now established

A fresh independent strict check reproduces exactly 23 observations after 13,417
different-net face-object comparisons: five intrinsic land pairs and eighteen
pad/track or track/track escape observations. All are on B.Cu at the three named
packages. The strict generic 2 mm matrix remains FAIL, without exceptions applied.

The primary manufacturer recommended lands were independently checked literally
against the current native pads and visually inspected source drawings:

- BR1 MB10S-13: Diodes DS39045 Rev.3-2, page 4, MBS recommended lands 1.00 x
  2.15 mm, adjacent pitch 2.50 mm and row pitch 5.35 mm. Both named adjacent
  pad gaps are 1.50 mm by drawing arithmetic.
- U1 LYT1603D: PI LYTSwitch-1 Rev.B 07/16, page 11 D08A reference lands 1.45 x
  0.60 mm, pitch 1.27 mm. Pin3/4 gap is 0.67 mm and pin2/4 gap is 1.94 mm.
- D1 US1M-13-F: Diodes DS16008 Rev.11-2, page 4, US1A–US1M SMA recommended
  lands 2.50 x 1.70 mm at 4.00 mm pitch. The pad gap is 1.50 mm.

All literal land checks pass. The five strict failures therefore do not identify
a copied manufacturer footprint dimension error that could be repaired without
changing the selected land pattern. Rigid relocation cannot enlarge these gaps.

## Fresh, finite geometric containment

`current-finite-region-proposal.json` freshly anchors five exact regions to the
current pad polygons. This does not reuse the obsolete BR1 coordinates. It retains
the 1.0 mm copper-edge target rather than the older proposal's 0.5 mm target.

Paired-pad bounding-box margins are 1.0 mm for U1.3/4 and 0.3 mm for each other
pair. Only the specified B.Cu native pads and uniquely pad-rooted local track
portions are eligible. Vias, zones, other nets, other layers and unrelated tracks
are not eligible. An entire long track is not exempt merely because one part
passes through a region.

The qualified checker clips actual copper into inside/outside pieces. Only two
inside pieces sharing the exact pair region use the diagnostic local value;
outside and cross-region piece comparisons retain the original matrix target.
All 23 offending close portions map to exactly one region, without ambiguous
pad ownership. All eighteen escape observations are accounted for by those
finite regions. The complete 55-pair screen then passes the *geometric proposal*,
with no outside/cross-region residual. The original strict report is preserved.

The inherited proposal values 0.60/1.80/1.40 mm are used solely as analysis
parameters. They are not derived electrical minima, an IEC deviation acceptance
or a qualified manufacturing process. Their nominal CAD headroom is only about
0.07 mm at U1.3/4, 0.14 mm at U1.2/4 and 0.10 mm at the other pairs. These numbers
must not be advertised as warranted soldered-clearance margins.

Exact current region bounds and all 23 original object UUIDs, pad roots, measured
gaps and clipped-piece decisions are in `current-geometry-assessment.json`.

## Manufacturing and assembled-path uncertainty

The reported 0.670002 mm is effectively 0.67 mm nominal saved-copper geometry.
The extra millionths reflect polygon/search precision, not factory tolerance.
No accepted pad-edge fabrication-growth bound or soldered joint/lead clearance
bound has been supplied. Do not apply a generic track-width tolerance as if it
were a guaranteed minimum space between these pad edges.

Common global registration of one copper layer does not change the relative gap
between its two pads. Local feature-edge variation can change it. Component lead
size, solder fillets/bridges, placement and forming affect assembled air/surface
paths even where the bare copper remains unchanged. Their worst-case combined
bound is unknown. Solder mask receives no safety/creepage credit in this analysis.

## Bounded conclusion for the coordinator

The geometry question is resolved: the five controlling nominal gaps match the
manufacturer recommended land geometry; all eighteen close escape observations
are limited to five explicit current-source package regions; field-copper targets
remain satisfied outside/crossing those regions. No layout redesign is justified
merely to reduce duplicate strict-report entries.

Electrical suitability, assembled insulation, transient/high-frequency stress,
CTI/pollution/altitude applicability and any safety or powered acceptance are not
closed by this geometry result. A bare, unpowered prototype fabrication decision
can reference this exact geometric disposition, but it must be recorded separately
by its actual authorized owner. This contributor does not grant that acceptance.

Primary files visually inspected (no source documents modified):

- `work/compact09/capture-active/MB10S.pdf` — DS39045 Rev.3-2, p4.
- `work/compact09/capture-active/US1J.pdf` — US1A–US1M family DS16008 Rev.11-2, p4.
- `work/compact09/rdr-research/lytswitch-1_family_datasheet.pdf` — Rev.B 07/16, p11.

The corresponding rendered pages are retained in this contribution directory.
