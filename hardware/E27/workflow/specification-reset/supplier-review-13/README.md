# RFQ13 — selected isolated driver, manufacturer enquiry

Current board: 45 × 60 mm, four layers, 33 components, 81 pads, 304 tracks and 17 vias.
This packet supersedes TOOLKIT11 for the documented mechanical and spacing refinements.
It is the transformer-based driver discussed in this chat. Earlier packets are historical.

The documentary dimensional and assembly/insulation engineering review is complete for
technical enquiry, subject to the actual independent review disposition in review-status.json.
It does not physically confirm a custom transformer or formed parts before they exist.

## Files to use

- Velluneo_RFQ13_Enquiry_Pack.zip: complete enquiry handoff, drafts and response checklist.
- Velluneo_RFQ13_BarePCB_DFM.zip: the bare-board CAM package for the PCB manufacturer's DFM portal.
- Velluneo_RFQ13_Transformer_Assembly.zip: drawings, exact interfaces, BOM and questions for the winding/assembly shop.
- Velluneo_RFQ13_Engineering.zip: editable KiCad project with local libraries/models and current evidence.
- drawings/Velluneo_RFQ13_Dimensioned_Review.pdf: seven-page controlled dimensional/interface review.

The master enquiry ZIP and transformer ZIP are not automatic JLCPCB assembly uploads.
PCB fabrication and custom transformer/formed-part assembly require separate technical responses.
The drafts in supplier/ are UNSENT. Five bare boards is the proposed quotation quantity,
not an order. No supplier contact, purchase, payment, energized test or production release occurred.

## Changes and verification

T1 now reserves the complete requested 30 × 30 × 18 mm assembly, with a 30.5 mm courtyard,
rather than only the raw bobbin. R10 moves 0.5 mm left, C3 1.5 mm left, R17 0.35 mm right
and 0.4 mm down; one AUX_RAW corner moves 0.6 mm down. Attached copper follows these moves.
Values, MPNs, all pin/net assignments, pad/hole geometry, dedicated SENSE/CS copper and
separate current-return branches are retained. The R1 native model now represents its
raised cylindrical dimensional allocation; appearance models do not qualify a formed part.

The pinned toolkit is unchanged: manifest b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97.
Actual preview/apply strengthens primary/secondary rules from 10.0 to 10.7 mm without
weakening other pairs. Fresh native ERC, DRC, unconnected and parity counts are zero.
The conservative all-layer projected P/S copper gap is at least 10.725 mm. The proposed
0.35 mm finishing allowance on each side leaves 10.025 mm; actual production tolerances
still need agreement. These are engineering screens, not claimed IEC tabulated minima.
Nine CAM layers and 42 plated holes are independently matched to native CAD. The via map
identifies 17 filled/capped vias, leaving 25 component insertion holes open.

## What the manufacturer must confirm

The exact finished T1 drawing/STEP, full pin tolerances, clip/core/terminal sections and
insulation materials/process remain supplier deliverables. The Q1 forming proposal requires
an incoming usable lead length of at least 13.0 mm, a controlled jig and first-article fit;
the semiconductor datasheet alone does not guarantee this length. R1 and BR1 also require
supported forming and a returned drawing. C1 requires strain-free pitch alignment and at
least 2 mm free vent space. No blanket 2 mm transformer spacer is permitted.

Read mechanics/ASSEMBLY-AND-ISOLATION-REVIEW.md and the 12 supplier response IDs. Actual
PCB process/films, finished construction, full insulation assessment and physical electrical,
fault and thermal qualification remain open. Genuine current human stage/release approval
is not replaced by an agent review. Parent lamp requirements remain preserved.

Production ordering and energization remain on hold; technical DFM/quotation can proceed
when the independent enquiry review is accepted. Changes require exact-file re-review.
