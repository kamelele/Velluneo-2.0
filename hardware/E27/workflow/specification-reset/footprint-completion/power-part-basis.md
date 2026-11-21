# FOOTPRINT-02: bounded native terminal and copper audit

2026-11-17; implementer only. Read device AGENTS and pinned implementer instructions. Root is sole CAD writer. No CAD, approved graph, rules, stage decision or shared file changed. Scope is the explicitly assigned diodes, bulk/output capacitors, input resistor and fuse; not all 25 remaining components.

All coordinate realizations below are **local candidate conventions** derived from native facts: front/top board view; X right, Y down; origin at component center. Rectangle dimensions are X×Y. No backside mirroring. Manufacturer polarity identifies K/A or +/−; **numeric 1K/2A, 1+/2− and nonpolar 1/2 are the project's local numbering**, not manufacturer-assigned numbers for these two-terminal parts.

## Concrete candidate copper table (mm)

| Part / reference | Native copper basis | Local candidate pad centers and size | Evidence class |
|---|---|---|---|
| STTH1R02A / DAUX | p10 Fig20: two 1.4×1.64 lands, gap2.63, outer span5.43 | 1K (-2.015,0), 2A(+2.015,0), both1.40×1.64 | Exact native recommended dimensions, visually verified |
| STTH2R02A / DOUT | p8 Fig14: same numeric dimensions, separately verified | 1K (-2.015,0), 2A(+2.015,0), both1.40×1.64 | Exact native recommended dimensions, visually verified |
| US1M-13-F / DCL | p4 suggested pad layout: X2.50,Y1.70,C4.00,G1.50,X1=6.50 | 1K(-2.00,0),2A(+2.00,0), both2.50×1.70 | Exact native suggested dimensions, visually verified |
| SMBJ160A-E3/52 / TVS1 | p5 mounting layout: padX≥1.52,padY≥2.18, innergap≤2.159, outerspan5.59REF | **Proposed constraint realization:** 1K(-1.935,0),2A(+1.935,0), both1.72×2.20; gap2.15,total5.59 | Native inequalities visually verified; chosen exact values are engineering realization, not fixed native recommended dimensions |
| EEHZA1J100P / COUT | Native hybrid land PDF p1, standard products D/D8: innergap a1.8,padlength b3.2,width c1.6 | Rotate native illustration so positive is left:1+(-2.50,0),2−(+2.50,0),both3.20×1.60 | Exact native recommended standard-product dimensions, visually verified; **not vibration-proof pattern** |
| 450BXW15MEFR10X20 / CBULK | BXW p2: nominalleadpitch F5.0±0.5; wireØ0.6 (no tolerance supplied); no PCB pad/drill prescription found | **Proposed:** 1+(-2.5,0),2−(+2.5,0), plated drill1.0,padØ2.0; positive pad may be rectangular2×2 for identification | Engineering hole/copper proposal; insertion/finished-hole tolerance and native pitch variation require assembly acceptance |
| Vishay AC05 / RIN | AC native p10: wireØ0.8±0.03; native EK variants have P22.5±0.5 or25.4±0.5, height h8±1; native ØB PCB-hole1.0±0.1. Straight axial supply has no preformed PCB pitch | **Proposed manually formed straight-axial assembly:** 1(-12.7,0),2(+12.7,0),pitch25.4; finished plateddrill1.10,padØ2.20 | Explicit engineering forming/land proposal; native EK25.4 is dimensional corroboration, not proof that straight-lead order is factory preformed |
| SCHURTER3403.0268.23 / F1 | Official UMT-H PDF p2 soldering drawing retrieved via web: padwidth3.75,padheight5.6,innergap10 | 1(-6.875,0),2(+6.875,0),both3.75×5.60; outerspan17.50 | Native web drawing transcription; original PDF/JPG local downloads403, no byte hash and no directly viewed local drawing; original-drawing visual verification remains open |

For ST parts center magnitude=(2.63+1.40)/2=2.015. Panasonic=(1.8+3.2)/2=2.5. Fuse=(10+3.75)/2=6.875. These are computations, not measurements. SMA is a package family, **not a common pad recipe**: native ST and Diodes patterns differ markedly. Native ST pad Y1.64 is transcribed exactly even though native lead-width maximum is1.65; do not silently enlarge or treat tolerance qualification as completed.

## Package and marking bounds for footprint body drawings

| Part | Native dimensions (mm) / body bounding basis | Polarity and frame |
|---|---|---|
| STTH1R02A, STTH2R02A SMA | Molded body alongX E1=3.95–4.60, alongY D=2.25–2.90; overallterminal spanX E=4.80–5.35; heightA1=1.90–2.45, standoffA2=.05–.20; leadwidthb=1.25–1.65,thicknessc=.15–.40,footL=.75–1.50. ST1p9Fig19/Table6; ST2p7Fig13/Table5 | Top view; K-band end assigned localpad1 left. Native pad illustration itself is unnumbered. Candidate maximum bodybox4.60×2.90 centered, not courtyard |
| US1M-13-F SMA | BodyX B4.00–4.60,bodyY A2.29–2.92; overallX E4.80–5.59;heightJ1.96–2.40; terminalwidthC1.27–1.63;leadthicknessD.15–.31;standoffG.05–.20;footH.76–1.52;p4 | Cathode indicated by band or notch per native p1. LocalK1left. Maximum bodybox4.60×2.92; overallleadspan5.59 |
| SMBJ160A-E3/52 SMB | BodyX4.06–4.57,bodyY3.30–3.94; overallX5.21–5.59;height2.13–2.44;terminalwidth1.95–2.20;leadthickness.152–.305;standoff.203max;terminalfoot.76–1.52;p5 | Unidirectional A suffix, cathodeband atleft in native topview; localK1left. Maximum bodybox4.57×3.94 |
| EEHZA1J100P | Exactpart sheet PDFp19/printedZA18: canD6.3±.5;baseA,B6.6±.2;overallleadspanH7.8max;bodyheightL5.8±.3;terminalW.65±.10;K.35(+.15/−.20);I2.6/P1.8 are reference outline dimensions, not landcenterpitch | Negative black cansector; printed bottomview identifiesminus/plus. Native generic recommended standard drawing hasminusabove/plusbelow; localpattern rotatedpositiveleft. CanmaxØ6.8,basemax6.8×6.8,planleadspan7.8; verticalheight6.1max. Do not mistakeH7.8 forheight |
| Rubycon bulk | Nominal10×20; family drawing p2 gives D+.5max=10.5 and L+αmax=22,α2;F5±.5,wire.6; leadlength15min and4min forlong/shortlead identification | Polarized; localpositiveleft/negativeright. Can metal shell/sleeve is not an extra terminal or demonstrated insulation barrier; vent clearance/mountedheight beyondbody remains open |
| AC05 | Nativep10 bodyLmax18,Dmax7.5,wire.8±.03; straightaxialoverallspan B63±1,xmax3. NativepreformedEKheight referscenterlineh8±1, not directlybodytop | Nonpolar. Bodybox18×7.5 for horizontal plan; forming/support,hotbody clearance andmountingheight remain process/thermal design inputs. Existing straightaxial order must not be called factoryEK |
| UMT-H | OfficialwebPDFp2 bodydrawing lists overall15.4 andendview5.35square; these are unlabeled-tolerance drawing values, **not qualified maxima**; familydescription5.3×16 | Nonpolar twoendterminals; local1left/2right. Proposedbodybox15.4×5.35 is nominal drawing representation only; completeheight/tolerance acceptance remains open |

Body rectangles are approximated footprint fabrication outlines. Courtyard, insulation distances, thermal copper, soldermask/paste expansion, allowed assembly tolerances and process rules are not established by these drawings. No traces, component placement or completed-board fit is implied.

## Native source identities

| Source path | Native pages | SHA256 |
|---|---|---|
| input-stage/source/stth1r02.pdf | DS4743Rev4; p9package,p10lands | e4c698e1b8301d7c35e3bfb0a5f2129393b61b14eef7fe30530b9de56aaa43d6 |
| input-stage/source/stth2r02.pdf | DS4744Rev3; p7package,p8lands | f3fa8d616dc9039babf7b8f2916459fc436df5c38da137a743c130da62a0e240 |
| clamp-study/source/diodes-us1m.pdf | DS16008Rev11-2;p1marking,p4outline/pads | d50b2773c0300d97a77f5125419098c8130ecaf967202a44be2b182de8a15c1f |
| clamp-study/source/vishay-smbj.pdf | Doc88392Rev09Jan2024;p5outline/pads | 1b65b57a4311128068c1dec747bbb99f6846ae932d77fcfd39904cb2d7a5cd50 |
| component-study/source/panasonic-za-data.pdf | PDFp19,printedZA18,Jun2014 exactpart | 877d35869a3a68b69c8e70f4898c77fbbc0742337383e3bc0b9641d6522b4de2 |
| tmp/fp02-b/panasonic-lands.pdf | NativeHybrid_landP_e.pdf,p1standardD/D8 | b14e4c77c68997bcc8f30949f64d0c43f0012ebd880ec5c970da4be094cb8bd9 |
| input-stage/source/bulk-bxw.pdf | p2familymechanical | 9fb3a22e969e8244e135b7204aa46baa7b8a99d68803a6408fca20c3d8fd5fa6 |
| input-stage/source/resistor-ac.pdf | Doc28730Rev05Dec2024,p10straight/EKmechanical | ebd3c714bb6b8c267c4cee006f5c72f105ee79c47d43ca680eb7e65929051f51 |

New downloaded primary source: https://industrial.panasonic.com/content/data/CP/PDF/Hybrid/Hybrid_landP_e.pdf . Native exactpart establishes sizecodeD; native land document establishes standardproductDpattern.

SCHURTER primary originals and retrieval are separately preserved in `schurter-web-record.md`; that record's SHA256 identifies our retrieval transcription, **not the inaccessible original PDF bytes**. Native source download gaps and source visual verification are not reported as passes. Body/lands for locally downloaded diode/capacitor pages were rendered with pdftoppm and visually inspected. No physical measurements performed.
