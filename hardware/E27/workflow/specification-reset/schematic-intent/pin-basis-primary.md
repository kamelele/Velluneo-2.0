# PIN-BASIS-A: pre-schematic physical pin evidence

Diagnostic implementer, not reviewer. Bounded read-only shared-input inspection; outputs onlytmp/pin-basis-a/. No CAD generated, no source approval or finding closure. No Git repository metadata was available in device-repo; exact native input hashes are in sources.json. Read projectAGENTS/workflow index and installed implementer/workflow guidance at manifest05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822.

## Diodes Incorporated MB10S-13, MBS

Native DS39045Rev3-2March2017,p1, raster visually inspected. Orient exactly as native pin diagram: body polarity marks at upper edge, '-'left and '+'right, semicircular body feature at right. This is the native displayed top orientation, not a generic bridge convention.

| Native terminal | Position in native diagram | Function | Proposed electrical intent |
|---|---|---|---|
| 1 | upper right | + | rectified positive/bulk positive |
| 2 | lower right | ~ | AC input B |
| 3 | upper left | - | rectified return/primary GND |
| 4 | lower left | ~ | AC input A |

All four terminals are used; AC2/4 may be exchanged electrically. Symbol pin numbers and footprint pad numbers must follow this native1+,2AC,3-,4AC mapping. Do not inheritKiCad9 Diode_Bridge:MB2S: its mapping is3+,4-,1/2AC. Host KiCad9 Diode_SMD:Diode_Bridge_Vishay_MBLS is a different vendor package/geometry and is not native MB10S proof. Its displayed pads1upper-left,2upper-right,3lower-right,4lower-left do not match the native orientation without a controlled remap/rotation. Prefer a dedicated native-numbered MBS definition over silent symbol/footprint renumbering. Physical dimensions/landpattern qualification remains later work.

## TI UCC28711DR, 7-terminal D SOIC

Native SLUSB86C,p3 top-view electrical pin table and drawing are authoritative for terminal-function numbering.

| Native functional terminal | Function | Physical position in native p3 top view |
|---|---|---|
| 1 | VDD | left top |
| 2 | VS | left second |
| 3 | NTC | left third |
| 4 | GND | left bottom |
| 5 | CS | right bottom |
| 6 | DRV | right third, opposite pin3 |
| 7 | HV | right top, opposite pin1 |

There is no terminal oppositeVS2: a vacant position separatesDRV6 andHV7. All seven real terminals are used. There is no logicalpin8 or electricalNC pin in this functional table. CAD must label the upper-right pad7, with no pad at the vacant position; do not compact the right row to equal1.27mm spacing.

Important native appendix discrepancy: D0007A generic mechanical/package drawing in the same PDF labels upper-right SOIC geometric position8 and lower-right5, with2.54mm gap to the next present right-side lead. This is not permission to wireHV as8; it is a difference between generic package-position notation and this datasheet's contiguous functional numbering. Capture the electrical1..7 mapping above and explicitly document its placement on the7-lead body. The package geometry must use the native omitted-lead position rather than a generic7-pin contiguous-row footprint. This discrepancy should be independently inspected before footprint acceptance.

## TDK B66422W1010D001 raw EFD25/13/9 coil former

Native TDK10/22,p3 visually inspected:10square pins, one section; supplied part is an unwound coil former, not a finished120:30:22 transformer.

| Native drawing | Left-to-right first displayed row | Left-to-right opposite row |
|---|---|---|
| Coil-former plan at left | 1,2,3,4,5 (upper) | 10,9,8,7,6 (lower) |
| Mounting-hole plan at center | 10,9,8,7,6 (upper) | 1,2,3,4,5 (lower) |

Thus1opposes10,2opposes9,3opposes8,4opposes7,5opposes6.5mm pitch,22.5mm row spacing in mounting-hole plan. Pin1 marking is explicitly shown on the bobbin front drawing. The PDF does not explicitly label these plan viewsTOP/BOTTOM; their row reversal must not be hidden. For a schematic the physical terminal numbers/rows are unambiguous. For later top-side CAD, tie view convention to the pin1 mark and manufacturer drawing; do not guess a mirrored footprint from visual appearance alone.

### Proposed engineered custom winding terminal contract

Choose row1–5 exclusively primary-side and row6–10 exclusively isolated-secondary-side. Dots are a NEW winding requirement: primarydot1,auxiliarydot2,secondarydot6 have equal instantaneous winding polarity. They are not an existingTDK finished-transformer guarantee.

| Winding | Turns | Dot/start terminal and net | Undotted/finish terminal and net |
|---|---|---|---|
| Primary | 120 | 1, BULK_POS | 5, MOSFET_DRAIN |
| Auxiliary | 22 | 2, PRIMARY_GND | 4, AUX_FLYBACK_POS (aux diode anode/VS upper divider) |
| Secondary | 30 | 6, OUTPUT_NEG | 10, SECONDARY_FLYBACK_POS (output diode anode) |

Unused physical pins3,7,8,9: explicitly no winding wire, no PCB electrical connection. Leave them mechanically present unless a separately controlled mechanical/insulation decision removes them. No shield or hidden intermediate taps are assumed. With primarydot1positive during MOSFETon, undotted auxiliary4 and secondary10 become positive during flybackofftime, matching rectifier-anode intent.

Winding order, wire construction, insulation barriers/margins, routing of leadouts, creepage, impregnation, core/gap/AL tolerance, bobbin pin orientation confirmation, and winding/hipot/phase acceptance remain real transformer-build requirements. Assigning opposite pin rows alone does not establish reinforced isolation, fit or manufacturability. This contract is suitable for explicit pre-schematic intent review, not release of an existing finished transformer.

## Actual checks and artifacts

- Native PDFs extracted withpdftotext-layout and rendered withpdftoppm; visually inspected MB10Sp1,TDKp3 and TI functionalp3 plus appendix mechanicalp35.
- Source URLs/fullSHA256/byte counts:sources.json.
- Native render artifacts:mb10s-page1.png,efd25-page3.png,ucc-page3.png. ucc-package-outline.png is the visually inspected native package outline at PDFpage35. ucc-package29.png is the page29 introduction and is not used as physical evidence.
- Shared source files unchanged. Host KiCad9 library inspection is corroboration/conflict detection only, not the physical pin source. No ERC/DRC, fit or finished-hardware measurements performed.
