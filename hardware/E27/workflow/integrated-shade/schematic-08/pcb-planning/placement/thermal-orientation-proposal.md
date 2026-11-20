# Final saved-board geometry and fixture orientation

This read-only implementer assessment supersedes the initial transformed-core preparation. It covers actual saved PCB SHA256 c503ff1b7660022d665ed4fabbc536c8f05d72899694a1d2da2c8a84ec6357d5. No CAD, library, rule, track, via or zone was written by this helper. Final positions include U5(97.8,54.3,270),C3(110,35.9,0),C5origin(123.35,74.6,180),can center(119.6,74.6),and both films rotated180degrees. All47refs/112numberedpins were freshly read and matched to approved frozen native binding, includingU2.1NC.

## Thermal geometry

Against all nine designated RF/aux/R7 heater drawing bodies, minimum sensitive-part Fab-box separations are U4/R12=16.275mm,U5/R12=24.875mm,C4/R24=19.500mm,C10/R24=10.750mm. Against C5maxD16.5mm circle at actualcenter, relay drawing-body gaps are U4=24.737mm,U5=18.991mm. These are drawing-body geometry, not local ambient, junction/body temperatures, assembled solder/lead clearances or tolerance-qualified thermal separation.

Prefer a vertical open fixture with CAD left edge physically uppermost: rising direction negativeCADX,gravitypositiveCADX. U3(78,72) andR7(84.5,90.5) have18.5mm cross-plume offset inCADy and6.5mm along projected rise. This removes directR7-under-U3 alignment. C5 atpositiveCADX fromR7 is upstream of its rising plume. RF/auxheat lies at yapproximately6..29, separated across the projected plume direction fromC5/control at yapproximately64..88.

No CFD, plume envelope, convection coefficient or temperature prediction is claimed. RF/auxheat can still warm nearby film/rectifier/input regions. Preserve accepted25mm clear air beyond component envelopes bothfaces,35mm front fixture reservation,and U3backsideDC_RETURN-only region[68,62,88,82]. Measure actual local air/package temperatures with accepted stop conditions. No bottom heater underC5 or relays.

## Commutation and quiet paths

final-native-loop-spans.json compares actual final native pin positions against frozen09bplacement using a consistent OFF-path convention: R2.1->L2.1,L2.2->L3.1,L3.2->C5.1,C5.2->D1.2,D1.CASE->R2.2. External straight pin-span sum131.589->80.506mm;closed pin-center polygon including geometric component pin spans160.714->109.631mm. These lower-bound metrics are not routed lengths, actual current-path perimeter, inductance, loop-area proof or EMC thresholds.

C3 direct BP/SOURCE pin spans each2.673mm. Dedicated FB-to-R2sense span11.424mm. Relay SOURCE-to-nearestU1SOURCE spans14.451/20.234mm, longer than initial arrangement. Retain paired actuator/return and quietKelvin routing review; do not claim all actuator legs meet5mm. Preserve D1CASE=SENSE_FB and separate power current from measurement branches.

## Planned output/return corridor

core-correction-corridor-check.json checks proposed,unrouted0.60mm F.Cu centerlines against112actual numbered pad boxes: zero such violations. The initial D1.2 escape uses only exact D1.2-to-CASE andD1.2-to-1 exceptions within courtyard+1mm,then restoresgeneric4mm. Added vias receive no concession. Minimum nominal excess over pad-box targets: DC_RETURN0.310mm,COUT_PLUS0.450mm. These are drawn margins,not fabrication-tolerance or physical-insulation qualification.

Forward/return centerlines run parallel atx124.5/x117.5 overy60.5..74.6,nominal6.4mm copper gap at0.6mmwidth. No tracks were created. Root must inspect eventual routing,intersections,layers,thermalcopper,exactnative shapes,all voltage-pair targets and actual surface paths. Film pin pitch27.5mm and approved block separation still impose long inputreturn; pair inputBUS/DC_RETURN wherepractical andretainwaveform/EMCverification. No arbitrary loop-shortness compliance threshold was introduced.

## Height-view limitations

The isometric figure uses actual saved native positions andFab boxes or courtyardfallback,with per-part height bounds. RF1/RF2=10.5mm,R7=12.5mm include proposed5mmstand-off. U4/U5=2mm andunlistedparts=3mm are engineering reserves. C5=27mm,C1/C2=28.1mm,C4/C10=2.7mm,L2/L3=11.5mm and other specified datasheet bounds are distinguished inJSON. XY drawing boxes are not tolerance-qualified maximum bodies. These are height envelopes,not exactMPNmodels or nativeKiCad3Dviewer coverage. Underside has no components;3mmTHTlead protrusion is a reservation. Wires,strainrelief,probes andclamps are unresolved/omitted. Tall blocks occlude some low envelopes;consultnative topview.
