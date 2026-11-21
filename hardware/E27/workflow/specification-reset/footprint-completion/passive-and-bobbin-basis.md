# FOOTPRINT-02 source audit A

Bounded implementer; root is sole product CAD writer. Read device-repo AGENTS and installed implementer instructions. Shared CAD/intent unchanged. All coordinates below are candidate front-side footprint conventions with body long axis x, centre origin, pad1left/pad2right. These nonpolar passive devices do not have manufacturer electrical polarity numbering; left/right1/2 is a project choice.

## CRCW native reflow patterns

Source clamp-study/source/vishay-crcw.pdf, document20035 revision14Apr2026, PDFp11 visually inspected. Native table has separateWAVE andREFLOW columns. The following usesREFLOW, not the larger wave patterns. Native drawing definesG innerpadgap,Y padlength along component long axis,X padwidth across component,Z outerspan. Derived centres±(G+Y)/2. All dimensionsmm.

| CRCW size | G | Y | X | Z | Pad size x×y | Pad1 centre | Pad2 centre |
|---|---:|---:|---:|---:|---|---|---|
| 0603 | .75 | .75 | 1.00 | 2.25 | .75×1.00 | (−.750,0) | (+.750,0) |
| 0805 | 1.00 | .95 | 1.45 | 2.90 | .95×1.45 | (−.975,0) | (+.975,0) |
| 1206 | 1.50 | 1.05 | 1.80 | 3.60 | 1.05×1.80 | (−1.275,0) | (+1.275,0) |
| 2512 | 4.75 | 1.45 | 3.50 | 7.65 | 1.45×3.50 | (−3.100,0) | (+3.100,0) |

This is source copper geometry with arithmetic coordinate conversion. Shape/corner radius,mask,paste andcourtyard allowances remain explicit project/assembly choices. Native notes state adequacy for most general applications, not blanket process qualification.

Native body bounds from samep11:

| Size | Length range | Width range | Height range |
|---|---|---|---|
| 0603 | 1.50–1.65 | .75–.95 | .40–.50 |
| 0805 | 1.90–2.20 | 1.10–1.40 | .40–.60 |
| 1206 | 3.00–3.30 | 1.45–1.75 | .50–.60 |
| 2512 | 6.10–6.50 | 3.00–3.30 | .50–.70 |

## Vishay NTCS0603E3104FXT

Source input-stage/source/ntcs0603e3t.pdf, document29056 revision29Sep2026,PDFp2 visually inspected. Native recommended rectangle pads are.80mm alongx by1.00mm alongy, overall outerspan2.40mm. Derivedcentre distance1.60mm, gap.80mm. Coordinatespad1(−.800,0),pad2(+.800,0),both.80×1.00. Nonpolar; these padnumbers are project convention.

Body1.6±.15 long,.8±.15 wide,.8±.15 thick; terminalL2/L3 minimum.2, exposedcentreL4 minimum.4. This is a distinct native pattern; do not silently reuse CRCW0603 pads just because imperial case names match. Mask,paste,courtyard,rotation and anythermal-attachment assumptions remain project choices.

## KEMET C2220C474J5GACTU: source gap and bounded candidate

Source component-study/source/C2220C474J5GACTU.pdf, generated16Nov2026,PDFp1 visually rendered/text inspected. It supplies body/termination dimensions only:L5.7±.4,W5.0±.4,T1.70±.15,Smin3.5,B.60±.35. Thereforebodymax6.10×5.40×1.85mm. No recommended copper land sizes/centres were found in this saved part-specific PDF; its later pages are simulation information, not a land specification.

Bounded attempts to obtain official commercial-family guidance failedHTTP503 for BOTH:

- https://content.kemet.com/datasheets/KEM_C1003_C0G_SMD.pdf
- https://content.kemet.com/datasheets/KEM_C1003_C0G.pdf

Do not label a generic2220 footprint or an automotive/KC-LINK family table as part-specific manufacturer approval. Manufacturer search results for other families are not used to close this source gap.

If root needs a clearly labelled engineering candidate for inspection, record the coordinator-selected two rectangle pads1.80×5.80mm at(−2.55,0)/(+2.55,0). This gives innergap3.30mm and outerspan6.90mm, with.40mm beyond maximum half-length3.05 and.20mm beyond maximum half-width2.70 on each side. Those are geometric comparisons at zero placement error, not solderfillet/process qualification. The innergap3.30mm is smaller than source minimum exposed-centreS3.50mm, so at least.10mm of each inner land lies below the unmetallized centre even at minimumS; larger actualS increases that under-body land extent. This is not a short-circuit proof or automatic rejection, but requires an explicit soldermask/paste/attachment process decision; native B/S alone does not validate it. This candidate is deliberately PROJECT-ENGINEERED, not source-provided copper geometry. Full component/courtyard extent must use the larger of pads/body plus an explicitly selected allowance. Do not mark C2220 footprint source-qualified until the land guidance gap is resolved or the project-owned calculated pattern receives its required review.

## TDK EFD25 view ambiguity revisited independently

Source component-study/source/efd25.pdf,10/22,PDFp3; native page was re-rendered and inspected. Coilformer plan has upper1,2,3,4,5 and lower10,9,8,7,6. Mountingholes plan has upper10,9,8,7,6 and lower1,2,3,4,5. Neither plan explicitly saysTOP orBOTTOM. Pin1marking is shown on the frontview, but alone does not prove which plan is a component-side PCB view. The two plans are related by a vertical mirror/turnover; selecting a top-side orientation from that fact without an explicit viewing convention would be invented confirmation.

Numbered opposite pairs1↔10,2↔9,3↔8,4↔7,5↔6 are unambiguous; pitch5mm,rowdistance22.5mm, source mountinghole diameter1.3+0.1mm. Copper annulus,finishedhole/drill compensation andcourtyard are not specified there.

For recordkeeping, the MOUNTINGHOLES AS-DRAWN coordinates can be written withcolumnsx=−10,−5,0,+5,+10:uppery=−11.25 has10,9,8,7,6; lowery=+11.25 has1,2,3,4,5. That is an exact coordinate representation of the source diagram, NOT confirmation that it is the desired front-copper view. Mirrory signs reproduces the coilformer plan. Root should keep this owned view gap explicit before accepting a PCB footprint; request manufacturer clarification or inspect an actual marked bobbin. No physical bobbin was available here.

## Evidence

- sources.json:full native inputSHA256,paths,page numbers.
- geometry.json:source-backed reflow/NTC copper dimensions and derived coordinates; KEMET clearly projectcandidate; TDK as-drawn only.
- crcw-land.png,ntcs-land.png,c2220-body.png,efd25-native.png:actual page renderings.
- Actual tools:pdftotext-layout,PyMuPDF page search/render,visualinspection,arithmetic coordinate conversion; bounded primary-source download attempts failed as recorded.
- No CAD generation,physical board placement,manufacturing fit test,source approval or independent review performed.

## Bounded TDK primary STEP follow-up

Official exact-part page https://product.tdk.com/en/search/ferrite/ferrite/ferrite-acc/info?part_no=B66422W1010D001 links “3D Outline(STEP)” to https://product.tdk.com/system/files/dam/doc/product/ferrite/ferrite/ferrite-acc/3doutline_step/c61036-a0162-b202_efd25_sw.step . Actual download savedtdk-efd25.step, SHA256f6acdbbccb291fd39ac8028c163d7bdb47fa6849c8c7d94dce01076f05dfb2f0. STEPFILE_NAME/PRODUCT identifyC61036-A0162-B202-EFD25_SW,dated2021-03-12; product is a generic outline-model identifier, not a textual pin map. Text inventory found no explicitPIN/MARK/terminal-number names. This is not a claim that the model contains no geometric pin1mark; the3D geometry was not rendered/accepted here. Therefore this source retrieval does not itself resolve which native2Dplan is component-side PCBview.

Two explicit unaccepted proposals, for later comparison against a genuinely established top-side convention:

| Proposal | Upper y=−11.25,x=−10,−5,0,+5,+10 | Lower y=+11.25,same x order | Basis |
|---|---|---|---|
| A | 10,9,8,7,6 | 1,2,3,4,5 | native mountingholes as drawn |
| B | 1,2,3,4,5 | 10,9,8,7,6 | native coilformer plan as drawn |

Neither is marked confirmedTOPVIEW. LeavingT1unassigned until orientation is actually resolved is truthful; candidate library artwork must not masquerade as resolved pin placement. No manufacturer contact or physical sample inspection occurred.
