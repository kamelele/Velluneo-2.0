# FOOTPRINT-01 native-source geometry handoff

Bounded implementer/source audit. Shared CAD/approvedgraph unchanged. Root remains sole CAD writer. Outputs are calculated footprint candidates from the native printed land-pattern dimensions, not physical-fit measurements, independent review or approval.

Coordinate convention for both tables: component/top side viewed from above, origin at package/land-pattern centre, x positive right, y positive down (KiCad front-footprint coordinates). Choice of origin/orientation is project engineering; relative distances/pad sizes below follow printed manufacturer examples. Unitsmm.

## UCC28711DR, D0007A

Source:bias-repair/source/ucc2871x.pdf; PDFp36, “EXAMPLE BOARD LAYOUT”, drawing4220728/A01/2018, visually inspected; p35 package outline and p3 functional pin numbering previously inspected. SHA256762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248.

Printed metric land-pattern example:7pads1.55x0.60; opposing pad-column centres5.4; normal lead pitch1.27; total first-to-fourth row distance3.81; missing right-side second row givesHV-toDRV gap2.54. These are example reference land dimensions, not a unique mandatory IPC land design. Printed inch equivalents are rounded (.061,.024,.213,.050,.100); this coordinate candidate deliberately adopts the printed metric values, not an invented exact conversion of both units.

| Functional pad number | Function | x | y | Copper pad size x×y |
|---|---|---:|---:|---|
| 1 | VDD | -2.700 | -1.905 | 1.55×0.60 |
| 2 | VS | -2.700 | -0.635 | 1.55×0.60 |
| 3 | NTC | -2.700 | +0.635 | 1.55×0.60 |
| 4 | GND | -2.700 | +1.905 | 1.55×0.60 |
| 5 | CS | +2.700 | +1.905 | 1.55×0.60 |
| 6 | DRV | +2.700 | +0.635 | 1.55×0.60 |
| 7 | HV | +2.700 | -1.905 | 1.55×0.60 |

No pad at(+2.700,-0.635). Keep the2.54mm gap; do not use a compact three-pad right row. The p36 generic package-position labels call top-right8 and bottom-right5. The actual UCC28711 p3 top-view/function table callsHV7. This candidate intentionally uses functional pad7 at the native top-right physical location, without introducing pad8. The numbering reconciliation must remain visible in the footprint documentation.

P35 package bounds:body width3.81–3.98,body length4.81–5.00,overall lead span5.80–6.19,height1.75max. These are package bounds, not courtyard dimensions. Geometry bounding extents from proposed pads and maximum body arex±3.475,y±2.500 before any courtyard allowance.

The native land drawing shows rounded exposed-metal corners but supplies no corner radius. Rectangular versus rounded-rectangle pad/corner radius is a project/manufacturing choice. P36 shows bothNSMD/SMD mask alternatives; forNSMD it prints0.07max all-around metal-to-mask opening clearance, whileSMD prints0.07min all around beneath mask. Do not copy0.07 as a universally mandatory soldermask expansion. Select compatible mask/paste/courtyard/silkscreen allowances under the actual fabrication/assembly process. No soldermask or courtyard value is approved here.

## Diodes Incorporated MB10S-13, MBS

Source:tmp/pin-basis-a/mb10s.pdf; PDFp4, “Suggested Pad Layout”, DS39045Rev3-2March2017, visually inspected. SHA256a46066843f6b010bffdb85fe3162573330e70bd481df3c5ef9000eeb59e6a77c. Pin-function orientation is nativep1, not a KiCad/Vishay generic bridge convention.

Native printed dimensions:X=1.00 (padwidth),Y=2.15 (padlength),C=2.50 (columncentre distance),X1=3.50 (outerpadspanx),Y1=7.50 (outerpadspany). Derived row-centre distance=Y1−Y=5.35; thereforexcentres±1.25,ycentres±2.675. Native drawing aligns lead/pad long axis vertically in this orientation.

| Native pad number | Function | Native p1 position | x | y | Copper pad size x×y |
|---|---|---|---:|---:|---|
| 1 | DC+ | upper right | +1.250 | -2.675 | 1.00×2.15 |
| 2 | AC | lower right | +1.250 | +2.675 | 1.00×2.15 |
| 3 | DC− | upper left | -1.250 | -2.675 | 1.00×2.15 |
| 4 | AC | lower left | -1.250 | +2.675 | 1.00×2.15 |

At this rotation, '+' and '−' marks are near the upper body edge; the native body semicircular feature is at the right edge. The source suggested pattern is not separately numbered; table maps the same orientation as its package outline and nativep1 pin diagram. A dedicated native1+,2AC,3−,4AC footprint avoids the incompatible genericMB2S symbol numbering.

Nativep4 outline:bodyD=4.50–4.95 horizontal,E1=3.60–4.10 vertical,total leadspanE<=7.00 vertical,leadpitche=2.30–2.70 horizontal,heightA2=2.30–2.70,leadwidthb=.50–.70. Thus the package body overhangs the copper outerspanX1=3.50 in x; do not draw courtyard from pads alone. Combined max body/pad extent isx±2.475,y±3.750 before a project-selected courtyard allowance. This calculation does not account for any process-specific handling clearance.

The native recommended copper pads are drawn rectangular. Mask expansion,paste adjustment,assemblycourtyard,silkscreen and pin1mark shape are not specified by this suggested-pad table and remain explicit project/process decisions. Its text asks to consult current manufacturer package outlines; this audit binds the savedPDF revision/hash and does not claim a fresh package-outline revision beyond it.

## Deliverables and scope

- geometry.json: machine-readable source geometry and coordinate tables, fullnativePDF hashes.
- ucc-land.png and mb-land.png: rendered inspected manufacturer pages.
- mb10s.txt: native text extraction.
- Actual commands:pdftotext-layout; PyMuPDF page-text search/render; visualinspection of the resulting native pages; arithmetic derivation of symmetric centres.
- No physical placement, solderability/assembly assessment, whole-board creepage decision, physical measurement or independent acceptance is performed.
