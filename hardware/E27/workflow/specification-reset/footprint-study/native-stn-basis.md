# FOOTPRINT-01: STN1NK80Z native four-pad candidate basis

Implementer source audit only, 2026-11-17. No CAD, shared libraries, graph, rules, placement, review decisions or human approval changed. Writable scope: `tmp/fp-native-b/`.

## Input identity

- Native manufacturer source: `component-study/source/stn1nk80z.pdf`, ST DS14259 Rev 2, July 2026, 14 pages; SHA256 `b2e23ffd24302bb78fd42dddbd25155a0833f785765aba20ef38fdff6aabf03b`.
- PDF p1: physical numbers and electrical diagram G(1), D(2,4), S(3).
- PDF p8 Figure 19, drawing 0046067_15: top-view package orientation, tab 4 above body, three leads below, numbered 1,2,3 left to right.
- PDF p9 Table 8 and Figure 20, drawing 0046067_15: native dimensions and recommended footprint. Both pages rendered and visually inspected; do not extract land dimensions from package body dimensions.
- Approved-intent file byte SHA256: `b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a`. Parent-supplied approved graph digest: `b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57`. Q1 expected: 1 GATE, 2 DRAIN, 3 SENSE, 4 DRAIN.
- `git -C device-repo rev-parse HEAD` cannot return a base commit here: this workspace copy is not a Git repository. File hashes are the reproducible input identifiers.

## Native recommended land facts

Figure 20 supplies four rectangular lands: three equal lead lands 1.2 mm wide by 1.5 mm deep; one tab land 3.3 mm wide by 1.5 mm deep. The lead pitch is 2.3 mm (outer lead center span 4.6 mm). The separation between tab-land centerline and three-lead centerline is **6.4 mm**. This is centerline separation, not clear copper gap or total span.

The illustration is oriented tab above, leads below. Numeric identities come from Figure 19/p1, not from Figure 20 alone. Native source does not define a KiCad origin, axis convention, pad layer settings, mask expansion, paste reduction, courtyard, silkscreen, pad corner radius or production acceptance.

## Proposed exact coordinate realization

This is a **candidate coordinate convention derived from native recommended land dimensions**, not an additional manufacturer coordinate table. Front/top view, X right, Y down (KiCad footprint editing convention); origin halfway between the two land-row centerlines. Tab upper side; lead 1 lower left. No mirroring.

| Pad | Native function | Approved net | X mm | Y mm | Copper size X × Y mm |
|---|---|---|---:|---:|---:|
| 1 | Gate | GATE | -2.3 | +3.2 | 1.2 × 1.5 |
| 2 | Drain lead | DRAIN | 0 | +3.2 | 1.2 × 1.5 |
| 3 | Source | SENSE | +2.3 | +3.2 | 1.2 × 1.5 |
| 4 | Drain tab | DRAIN | 0 | -3.2 | 3.3 × 1.5 |

Simple arithmetic: 6.4 / 2 = 3.2; 4.6 / 2 = 2.3. The resulting pad row outer edges are Y=±3.95 mm and the row-to-row open copper gap is 4.9 mm. These arithmetic extents are geometric descriptions only, not clearance/creepage acceptance. Preserve distinct pad numbers 2 and 4 even though they share the drain net. A candidate local name could be `STN1NK80Z_SOT223_4Pad_ST_DS14259`; naming is coordinator-owned.

Rectangular pads reproduce the drawn land shape. A rounded-rectangle corner radius would be a local process proposal and changes copper area; it is not specified in Figure 20. Likewise mask/paste settings and assembly tolerances require the project's process acceptance. No assumed copper heat-spreader area is included in this native land transcription.

## Native package tolerances, mm

| Dimension | Min | Typ | Max | Meaning in native outline |
|---|---:|---:|---:|---|
| A | — | — | 1.8 | Package height |
| A1 | 0.02 | — | 0.1 | Stand-off |
| B | 0.6 | 0.7 | 0.85 | Narrow lead width |
| B1 | 2.9 | 3.0 | 3.15 | Tab width |
| c | 0.24 | 0.26 | 0.35 | Terminal thickness |
| D | 6.3 | 6.5 | 6.7 | Body width along three leads |
| E | 3.3 | 3.5 | 3.7 | Molded body depth |
| H | 6.7 | 7.0 | 7.3 | Overall terminal span |
| e | — | 2.3 | — | Adjacent lead center pitch |
| e1 | — | 4.6 | — | Outer lead center span |
| V | — | — | 10° | Native outline terminal-angle limit |

Thus a maximum molded-body envelope is 6.7 × 3.7 mm; overall terminal span is 7.3 mm; height maximum is 1.8 mm. These are package facts, not qualified courtyard or a finished E27 fit claim. A centered rectangular maximum body outline, if used, is an implementation envelope approximation rather than exact native tapered-body shape.

## Generic host footprint conflict

Corroborating host library only: `/usr/share/kicad/footprints/Package_TO_SOT_SMD.pretty/SOT-223-3_TabPin2.kicad_mod`, SHA256 `8732e6fb9d63576e4ecfcdb953443fe6f34b5afabc87ef136cdd40fe7cf03434`. It refers to KICAD9 models; it does not qualify the parent's KiCad 10 environment.

| Host pad label | X,Y mm | Size X × Y mm |
|---|---|---|
| 1 | -3.15,-2.3 | 2.0 × 1.5 |
| 2 (lead) | -3.15,0 | 2.0 × 1.5 |
| 2 (tab) | +3.15,0 | 2.0 × 3.8 |
| 3 | -3.15,+2.3 | 2.0 × 1.5 |

The host merges the physical tab into pad number **2**, has no pad **4**, and uses different land dimensions and 6.3 mm row separation. Its orientation is rotated relative to the native tab-upper illustration. The electrical common-drain fact does not authorize dropping an approved physical terminal. It is therefore not a direct substitute for this approved four-terminal graph. A source-based custom four-pad realization avoids both the missing-pad4 mismatch and silently inheriting a different land pattern. Do not mark pin4 NC, omit it from checking, or change the graph to force compatibility.

## Limits and handoff

Concrete candidate basis is supplied for native four-pad construction; actual footprint construction and checks belong to the sole CAD writer. Required subsequent checks include pad-number/net matching, front-view pin1 orientation, native dimensions, process/mask/paste/courtyard acceptance and any applicable thermal/clearance rules. This audit establishes neither device thermal qualification nor PCB stage approval. No physical measurements were performed.
