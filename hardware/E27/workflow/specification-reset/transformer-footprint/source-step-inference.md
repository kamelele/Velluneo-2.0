# T1VIEW-STEP diagnostic handoff

Actual official STEP geometry plus native pin1mark provides a reproducible geometric basis for **ProposalA**: component-side top view has upper10,9,8,7,6 and lower1,2,3,4,5 when x increases right. This is a diagnostic inference submitted for independent review, not a manufacturer-writtenTOPVIEW label, physical-sample verification, accepted footprint, or modification of the frozen27-assignment packet.

## Immutable sources / actual runtime

- Official STEP: `../fp02-a/tdk-efd25.step`, SHA256f6acdbbccb291fd39ac8028c163d7bdb47fa6849c8c7d94dce01076f05dfb2f0. Exact-partTDKproduct page linked this model at https://product.tdk.com/system/files/dam/doc/product/ferrite/ferrite/ferrite-acc/3doutline_step/c61036-a0162-b202_efd25_sw.step . FILE_NAME/PRODUCT:C61036-A0162-B202-EFD25_SW,2021-03-12.
- Native PDF: `../../component-study/source/efd25.pdf`, SHA256f4b6084fa9171a0157c3744663e146da6b3a738171dab4dfd3e137c125f6f06e,p3,10/22. Explicit frontview arrow “Pin1marking” identifies the upper-left diagonal/chamfer feature when pins point down.
- Actually imported usingCadQuery2.7.0/OCP7.8.1.1, not an inferred availability claim. `cq.importers.importStep` returns1solid,430faces. Boundsmm:X±12.5,Z±13,Y−6.15..+10.25, consistent25×26plan and16.4totalheight. No sourcefile edits.

## Distinguishable mark and physical pin side

The nativePDF's marked frontview is reproduced by the STEP front-facing geometry with pins down and unique diagonal/chamfer at upper left. Compare `front-native-orientation.png` against `native-pin1-front-crop.png`; both are actual source-geometry renders.

CadQueryface335 of this actual import is the unique matching planar corner feature:centre(−8.000,−5.150,−8.650)mm,normal(−0.7071068,−0.7071068,0),area0.266274mm². Its box is approximatelyX−8.9414..−7.0586,Y−6.0914..−4.2086,Z−8.7000..−8.6000. `faces.json` preserves all430face records; index335 is a diagnostic import index, not a manufacturer terminal number. No corresponding mirrored feature exists among the inspected opposite-corner faces.

Ten square pin-tip endfaces are actually present atY=+10.25, eacharea0.36mm² (.6square), withcentresX=−10,−5,0,+5,+10 andZ=±11.25. Thus pins extend towardpositiveY, and component-side/top inspection is fromnegativeY. The native-marked front is thenegativeZ flange; its leftmost pin is(X,Z)=(−10,−11.25), so that terminal ispin1. This ties a real asymmetric manufacturer-identified feature to the actual pin array rather than selecting a mirror from an unlabelled plan alone.

## Explicit top-side screen convention and candidate coordinates

Take screenright=+STEPX, screenUP=+STEPZ, looking from−STEPY toward+STEPY. Therefore KiCad-like screenDOWN coordinate is **y_fp=−STEPZ**, andx_fp=STEPX. This handedness matters. The first preliminary message incorrectly usedscreendown=+Z and suggestedB; it was explicitly corrected before handoff/integration. No product CAD or frozen packet was changed.

| Terminal | STEP pin-tip centreX,Y,Z mm | Proposed front-footprintx,y mm |
|---|---|---|
| 1 | −10,+10.25,−11.25 | −10,+11.25 |
| 2 | −5,+10.25,−11.25 | −5,+11.25 |
| 3 | 0,+10.25,−11.25 | 0,+11.25 |
| 4 | +5,+10.25,−11.25 | +5,+11.25 |
| 5 | +10,+10.25,−11.25 | +10,+11.25 |
| 6 | +10,+10.25,+11.25 | +10,−11.25 |
| 7 | +5,+10.25,+11.25 | +5,−11.25 |
| 8 | 0,+10.25,+11.25 | 0,−11.25 |
| 9 | −5,+10.25,+11.25 | −5,−11.25 |
| 10 | −10,+10.25,+11.25 | −10,−11.25 |

`component-top-Xright-minusZdown.png` is the explicit component-top geometry view with those screenaxes. Pins are occluded by the bobbin from this side, so their coordinates above come from the actual BRep endfaces, not guessed visible squares. The native mountingholes plan matches this arrangement (ProposalA). The native coilformerplan, which shows pin-tip squares, matches the opposite/pin-side inspection (ProposalB). These TOP/BOTTOM identifications are geometric inference; the originalPDF does not print those headings.

## Scope and reproducibility

`render.py` imports the actual STEP, exports exact hidden-line±Y/front−Z/isometricSVG/PNG and inventories faces. `explicit-views.py` rotates the shape90° aroundX to obtain a controlled orthographic projection, rotates the rendered image180° to put+Xright/−Zdown, and produces the native-front comparison. Image rotation only sets the screenorientation; the geometric coordinates and transform are separately recorded in `findings.json`. `faces.json` and `findings.json` preserve actual pin-tip and mark records. All final rendered views were visually inspected.

The result proposes an evidence-based resolution of the earlier view ambiguity for review. It does not prove actual shipment markings, bobbin dimensional tolerances, installed finished-transformer orientation, core assembly height, drilled/copperpad dimensions, winding pin contract compliance, isolation, solderability or manufacturing fit. Do not alter an approved graph or silently integrate this into the frozen packet; coordinator should submit the exact candidate/evidence through the required affected review.

Onlytmp/fp02-step-audit/ was written. No sharedCAD/source/intent changes, PCB placement, physical measurements or approval performed.
