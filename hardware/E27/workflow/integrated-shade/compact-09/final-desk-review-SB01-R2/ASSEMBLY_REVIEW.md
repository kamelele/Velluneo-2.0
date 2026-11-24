# SB01 R2 assembly and fit desk review

Actor: /root/r2_assembly_fit,24Nov2026. Scope: existing51.2x33mm barePCB, manual laboratory assembly, no enclosure and no CAD changes. This is a source-bound dimensional review, not a measurement, electrical release or powered-test authorization.

## Result before ordering

All17 electronic positions and2 bare-wire ports were checked against the actual native PCB pose, pads, holes and net-labelled polarity. No physical incompatibility requiring a different part, outline or copper modification was identified. Custom lead forming for L1/RF1/R7 and horizontalC6 is an ordinary manual prototype operation with documented envelopes, not a claim of factory-qualified lead shape. Actual samples must be formed against the actual board and inspected before soldering; do not force raw pitch tolerances into holes.

Required documentation corrections are material: the present assembly needs **20.5mm nominal-board planning height**, not19.5mm or an achieved20mm limit; T1 is Würth size1210, not1280; exactC6 is unsuffixedEEUFS2A151, nominal12.5x20mm and maximum13x22mm; U1 body3.9x4.9 dimensions are BASIC, not guaranteed maxima. R6 bodylength maximum is3.25mm under the Royalohm family drawing, not3.20mm. These corrections do not require a new board. Proposed field additions for all17parts and bothports are in proposed-geometry-row-addenda.json.

## Height and mechanical envelope

The local top/bottom datums are PCB surfaces. L1 PR02-FS body Dmax3.9,Lbodymax10,Lterminalmax12 with2mm lower forming stand-off and2mm top allowance gives the project16mm top budget. This preserves the parent-approved2mm stand-off and90C engineering temperature target; it is not shortened merely to satisfy a packaging goal. The underside tallest rated package is BR1 at2.9mm(A1max.2+A2max2.7). Thus16+1.6+2.9=20.5mm. JLC1.6mm board+10% is1.76mm, giving20.66mm before forming/solder variation. An unconditional as-built maximum cannot be claimed before sample gauging. Original20mm target is exceeded by0.5mm in nominal planning.21mm can be used only as preliminary handling reserve. External wires and support are excluded.

Trim through-hole leads and solder projections to **<=1.5mm below PCB**; this keeps them within BR1's2.9mm lower package envelope. Inspect after soldering for sharp protrusions, bridges and tilt. Do not shorten the upper2mm forming stand-off. Lead protrusions, wire loops and solder buildup require actual inspection; their uncontrolled length is not bounded by a component data sheet.

Independent transformation of all17 body/forming envelopes gives zero same-face rectangular overlaps. Important nominal mechanical gaps: C6can-to-T1=1.0mm; R7body-to-C1=1.1mm; C1-to-C4=2.7mm; L1body-to-boardright=.6481mm; C1rightedge=.75mm; RF1bottomedge=1.0mm. These are mechanical placement checks, not electrical safety clearances or positional-tolerance certification. L1's body-to-retained virtual court margin is only.1981mm: centre the upright body over pad1 and inspect tilt and return lead. Body/lead concentricity is not fully specified; no claim that arbitrary forming always fits this court is made. Existing physical space permits controlled forming without a new outline.

## Through-hole fit

Using JLC's minimum finishedhole nominal-.08mm and exact maximum round leads gives positive diametral clearance at every THTpart: C1 .17mm; C4 .37mm; C6 .47mm; L1 .29mm; R7 .19mm; RF1 .32mm; RV1 .27mm. The native holes are C1/C4/RF1=1.1,C6/L1=1.2,R7=.9,RV1=1.0mm. Manufacturer raw pitches vary(C1/C4+/-.4,C6+/-.5,RV1+/-1.0); hole-position tolerance is+/-.075mm, so positive wire clearance alone does not establish raw lead insertion without adjustment. Hold/support leads away from seals/coatings and gently adjust them to the actual board. C1's.17mm diametral clearance is the narrowest and merits particular insertion/solder sample inspection, but no incompatible diameter was found.

## Exact C6 assembly

The FS-A table on page5 was visually checked, rather than relying on interleaved text extraction. EEUFS2A151 is100V150uF,D12.5x20 nominal,1400mArms at100kHz/+105C,.043ohm at100kHz/+20C,10000h. EEUFS2A151L is a different10x25mm case and is not interchangeable under this contract. Page1 givesD+/-.5,L+/-2 whenL>=20,lead.6+/-.05,P5+/-.5. Frequency coefficients for47-330uF are.60@60Hz,.70@120Hz,.85@1kHz,.95@10kHz,1@100kHz; no100Hz coefficient is explicitly published.

Horizontal case has sealplane localX4, ventX26, axis+X, diameter13 maximum, .5mm underside support, top13.5. In the native90degree pose its global body projection isX100.25..113.25,Y100..122. T1 nearestface startsX114.25, giving1mm nominalgap. Keep five millimetres of free3D vent direction fromY100towardY95, including outside thePCBedge99.4. This is feasible on the selected open bench; no closed enclosure claim follows. Keep wiring and supports away from vent; keep copper and components out of existing undercan reservations on both faces. Sleeve is not a certified safety barrier. Any cradle/insulating support must not strain the seal or obstruct the vent. No adhesive chemistry or enclosure material is selected/qualified here.

## SMD and polarity

BR1 andD1 native lands match the exact Diodes manufacturer patterns; U1 retainedD08A lands preserve the manufacturer's1.27mm pitch. T1 lands5.4x2.9mm at9.9mm pitch match the Würth drawing. SamsungC5 and PanasonicR4 land sizes are explicit engineer-selected patterns, not quoted exact vendor patterns. YageoR5/R8/R9 retain documented1206 lands. RoyalohmR6 retains manual prototype1206 lands; its exactfamily drawing was visually verified from a manufacturer-authored catalogue mirror. Its native pads span±.75..±1.80mm and width1.8; bodyhalfmax1.625 and minimum endtermination.25 remain overlapped under nominal centred placement. All of these still need normal solder/centering inspection.

BR1 pad1positiveBUS_RECT,pad3negativeDC_RETURN, pads2/4AC. D1 cathodeband pin1FB_INDUCTOR. C6positivepin1LED_PLUS. U1pin1BP,2M,3FB_INDUCTOR,4BUS_FILTERED,5-8SW_SOURCE. Mounting side and actualnativeglobalpadcoordinates are recorded perpart in assembly-contract.json: bottom views must not reverse polarity. The PR02-FS part occupies physicallegacyL1 and must not be mistaken for the old choke; the actual purchased T1 is stock Würth7687709152, not a custom transformer.

J1/J2 are bare solder wire lands, not purchased connectors. J1 pad1AC_L(148.4,130),pad2AC_N(148.4,124.5); J2pad1LED_PLUS(101.6,124.5),pad2DC_RETURN(101.6,130). Both nativepitch5.5. Legacy origin descriptions in activegeometry are stale. Use separately insulated wires with external strain relief on insulated support, avoid loose strands, and route away from resistors and C6vent. Wire-loop enclosure dimensions are outside this board-level height contract.

## Handoff and limits

Run inspect_native.py using pinned KiCad10.0.6 Python, then check_fit.py and build_handoff.py using HostPy. The native inventory is read-only and never saves the board; check_fit.py guards its boardSHA before calculations. canonical-input-hashes.json freezes reviewed PCB/schematic/BOM/geometry/spatial/thermalinputs. If parent changes metadata the evidence hashes must be refreshed; dimensional changes require rerunning this screen. sources.json binds primary-author dimensions to URLs and hashes available local sourcePDFs; distributor mirrors are explicitly identified as hosting manufacturer-authored documents. Rendered engineering shapes are not proof of delivered-part fit. No fabrication approval or electrical clearances are created by this assembly review.

Ordinary post-arrival unpowered work: verify exactMPNs/cases; trial-form axialparts andC6; check height/casegap/vent; solder in accessible order(bottomSMD first, then shortfrontparts, tallformedTHT last); trim<=1.5mm; inspect joints/polarity/cleanliness and continuity against netmap. Powered startup/thermal/fault evidence remains with the electrical test plan. Nothing here upgrades unmeasured performance to a physical result.
