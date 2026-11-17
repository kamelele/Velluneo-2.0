# Independent native physical-terminal basis, group B

PIN-BASIS-B,2026-11-17. Implementer/root/support_design, bounded read-only project inspection. Only tmp/pin-basis-b written. This is input for independent intended connectivity before CAD, not a review, stage approval, footprint sign-off or generated schematic. Source hashes in sources-local.json; native page views were rendered separately in this folder. No expected graph was derived from existing/generated CAD.

## Terminal sets and proposed local numbering

| Exact part | Manufacturer physical terminal set | Independently supported function | Proposed project-library numbering and geography |
|---|---|---|---|
| STN1NK80Z | Numbered1,2,3,4 |1=G,2=D,3=S,4=drain tab | Preserve1G/2D/3S/4D. In a top-view frame with tab opposite the three front leads, front leads are1G–2D–3S; tab4 isD. Do not substitute modelD/G/S terminal order. |
| STTH2R02A | Two terminals K/A; no numeric pin assignment in the inspected source | Cathode K at banded end; anode A opposite; exact A suffix=SMA | Locally define1=K,2=A. For chosen0degree local top-view frame, pad1/band left, pad2 right. This is project numbering, not a manufacturer assertion. |
| STTH1R02A | Two terminals K/A; no numeric pin assignment in the inspected source | Cathode K at banded end; anode A opposite; exact A suffix=SMA | Same local1K/2A, band left in project0degree frame. |
| US1M-13-F | Two terminals cathode/anode; no native numeric numbering | SMA; source explicitly allows cathode band OR cathode notch | Same local1K/2A, marked cathode left in chosen0degree frame. Do not inferK from marking-text rotation alone. |
| SMBJ160A-E3/52 | Two terminals cathode/anode; no native numeric numbering | UnidirectionalSMB(DO-214AA); band identifiesK | Same local1K/2A. A is NOT the same part asCA; no bidirectional substitution. |
| Rubycon450BXW15MEFR10X20 | Two radial leads with+/−polarity; native drawing does not number them | Positive andnegative indicated in dimension figure;10mmcase gives nominalF5.0mmlead pitch | Locally define1=+,2=−. A convenient localTHT frame is1at(0,0),2at(5,0)mm, with bodycenterbetween. Coordinates are a project convention. |
| PanasonicEEHZA1J100P | Two SMDV-chip electrical terminals+/−; native source does not number them | Black can sector is explicitly negative marking. Exact standardDcase; NOT a radial-leaded part | Locally define1=+,2=−. For chosen project0degree frame putpositive left andnegative right; the negative can sector must therefore be on the right. Native illustration may be rotated to this frame; it is not a fixed world-coordinate constraint. |
| KEMETC2220C474J5GACTU | Two interchangeable tin-finished end electrodes; no source pin numbers or polarity | NonpolarC0G MLCC, no marking | Locally define1/2 to distinguish expected net sets. At local0degree frame1left/2right along L. Either physical orientation is electrically equivalent; do not assign+/−to this ceramic. |

All numeric assignments for two-terminal diodes/capacitors above are deliberately LOCAL identifiers. They must be used consistently in the independent graph, symbol and footprint, and checked afresh at generated-CAD review. Body band/negative marking belongs to assembly orientation, not just silkscreen aesthetics.

## Native source locations, package geometry and direct visual observations

| Part/source | Inspected native basis |
|---|---|
| STN1NK80Z,DS14259Rev2July2026 | PDFp1 isometric labels1/2/3front and4tab; electricaldiagram expresslylabelsD(2,4),G(1),S(3). The pin4tab is an electrical drain, notNC or a genericthermalpad. |
| STTH2R02A,DS4744Rev3Dec2018 | PDFp1 identifiesK/A and cathode band in theSMAgraphic; p7SMAmechanicaloutline/table;p8recommendedSMAlandfigure; orderingtablep11 bindsSTTH2R02A toSMA. Manufacturer recommended land example: two1.4x1.64mmpads separated by2.63mmgap, overall5.43mmalongline. These are source dimensions, not an automaticKiCadlandqualification. |
| STTH1R02A,DS4743Rev4Dec2018 | PDFp1 explicitlylabelsSMA cathodebandK and oppositeA; A suffix must useSMA rather than other familypackages. Further package/land pages require exactApackagecheck at library stage. |
| US1M-13-F,DS16008Rev11-2Dec2014 | PDFp1 mechanicaldata sayscathodebandorcathodenotch, depicts top/bottomviews and orderingSMA/-13-F. Do not treat bottom-view depiction as top view without mirroring. |
| SMBJ160A-E3/52,Vishay88392Rev09Jan2024 | PDFp1 saysbanddenotescathodeforunidirectionaltypes and showsK/A; SMB(DO-214AA). Native familyelectricaltablehasSMBJ160A row; E3/52commercialorderingroute retained. Sourcep5 packageoutline is SMBDO-214AA, notSMA. |
| RubyconBXW catalog,PDFp2 dimensionfigure/p4exact450Vsize rows | ForD10mm:leadwireφ0.6mm,nominalpitchF5.0mm,diameterD+0.5max,lengthL+αmax withα2.0mm. Exact15uF450V10x20row gives20mmbodylength, hence22mmmax length allowance in that figure and10.5mmmaxdiameter. Drawingindicatespositive/negative leads; rawleadlengths are not a safe substitute for polarity inspection after leadforming/cutting. SleevePET is not an established safety-insulation barrier. |
| PanasonicZA familycatalog2025/individualZA-18Jun2014 | FamilyPDFp1 expresslyidentifiesnegativeblackmarking; technicaldataPDFp19 is exactEEHZA1J100P. StandardDdimensions:diameter6.3±0.5mm,L5.8±0.3mm,baseA/B6.6±0.2mm,H7.8mmmax,terminalwidthW0.65±0.10mm;referenceI2.6/P1.8/K0.35(+.15/−.20)mm. NoTHT5mmpitch exists here. I/P are drawingreference dimensions, not an assumedSMDpadcentrepitch. The standardPpart is not automatically the vibration-proofvariant with additional supportfeatures. |
| KEMET exactgeneratedspecsheet,PDFp1 | Drawinghaswraparoundendterminations alongL;L5.7±0.4,W5.0±0.4,T1.7±0.15mm,B0.6±0.35mm,S3.5mmminimum. Case2220/5651. Do not choose landgeometry solely from nominal2220name; terminationandmaximum-bodygeometry must be checked. |

The Panasonic capacitor's native operating uppertemperature is105C, not125C. The125C resistor-support arithmetic must not be interpreted as capacitor operating approval. Neither metalcapacitorcase is introduced as an additional electrical pin from appearance; case-voltage/insulation assumptions belong to the physical-barrier assessment.

## Expected functional net binding, independent of CAD

Names below are functional aliases from the existingcircuitintent; coordinator may use documented equivalentnetnames while preserving terminal membership.

| Component role | Physical terminal membership |
|---|---|
| Q1STN1NK80Z |G1→GATE,D2andD4→DRAIN,S3→SENSE. NoNCterminal. |
| DOUTSTTH2R02A |A/local2→secondaryflyback-positive windingend;K/local1→OUT+. |
| DAUXSTTH1R02A |A/local2→rawprimary-referenced AUXpositive windingend;K/local1→RAUXinput;RAUXotherend→VDD. Its returndomain isPGND, neverOUT−. |
| DCLAMPUS1M |A/local2→DRAIN;K/local1→CLAMP. |
| TVSSMBJ160A |K/local1→CLAMP;A/local2→BUS+. This is reverse-avalancheclamping, not anode-toPGND. |
| CBULKRubycon |+/local1→BUS+;−/local2→PGND. |
| COUTPanasonic |+/local1→OUT+;−/local2→OUT−. |
| CDD1/CDD2KEMET |Eachcaplocal1→VDD;eachcaplocal2→PGND. Assignment islocalonly; electrodesarephysicallyinterchangeable. |

A standardKiCadMOSfootprint may merge the tab withpad2 instead of presentingnativepin4. If used, that must be an explicit, reviewed physicalpin4→electricalD/pad2 alias in the pin/footprintbasis; it cannot disappear silently. A local symbol/footprint preservingpad4 avoids this ambiguity. No actualKiCadfootprint, stackup, solderland/drilldiameter or placement is approved by this sourceinspection.

## Remaining ambiguities owned by coordinator/library review

- Diode1K/2A andcap1+/2−are proposedLOCALnumbering. Independentintendedconnectivitymust declarethem before comparinggeneratedsymbols/pads.
- Native diodeband and capnegativemarking must match assemblydrawings/positions after rotations andboard-side transforms; these sourceimages alone do not verify a placementfile.
- SMA/SMBfamilyname is insufficient to certifylandpattern. Checkactualpadgeometry, courtyards, soldermask/paste andfootprintorientationagainstexactsource/profile.
- Rubyconleadhole/drill/tolerance andremainingleadforming details need a footprintcheck; onlynominalwire/pitch/bodylimits are establishedhere.
- PanasonicrecommendedPCBland geometry is not fullyselected from thecomponentI/P/Kdimensiontable. A suitablelandpattern andthephysicalleadview must be reviewed separately; donot copya radial footprint.
- Capacitorcase/sleeve safety, primary-secondary clearanceincludingtabandcans, thermalpadareaandmetalheatsinkcoupling remain physicaldesignsubjects. Noindependentreviewclosure, order orphysicalmeasurementoccurred.
