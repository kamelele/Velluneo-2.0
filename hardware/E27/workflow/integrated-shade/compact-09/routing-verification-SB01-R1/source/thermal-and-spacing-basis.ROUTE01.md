# Routing correction: electrical and thermal assessment limits

This addendum supersedes thermal interpretations of the pre-correction layout, not the component ratings. The laboratory environment remains 0–40°C. No temperatures, switching waveforms, efficiency, EMC, surge or fault behavior have been measured.

## Floating switching reference

The selected circuit is a nonisolated high-side buck. U1 SOURCE, C5 return and the current-sense reference float with the switching node. SOURCE is not DC_RETURN. A recommendation to enlarge a low-side MOSFET source ground plane cannot be applied to this switching node without considering its capacitive coupling. Broad SOURCE pours are removed in the candidate; only deliberate local connections should remain.

Removing that copper invalidates any prior estimate that relied on its heat spreading. No minimum SOURCE copper area, inherited 80/100 K/W ambient-to-junction figure or previous case-temperature range qualifies this layout. Manufacturer example thermal resistances are specific to their stated PCB geometry, copper weight, ambient and airflow. This two-layer 1 oz board must be measured in its actual guarded fixture. Copper-area reduction is an electrical geometry result, not proof of lower temperature or improved EMC.

## Loss budget and measurement plan

The unchanged paper planning budget is 0.9–1.7 W for the complete base, including the two output bleeders. At 60 V they dissipate approximately 0.106 W together. This allocation is an assumption, not a guaranteed worst case. Record stabilized input power, external LED power and their difference at 207/230/253 V AC and the selected 0–40°C ambient corners. Record actual input power factor and ripple; do not assign the RDR-464 reference board's measured efficiency to this board.

Instrument U1 SOURCE/case, D1 case, C6 can, T1, L1, RF1, R7 and both bleeders without defeating the guarded mains-referenced setup. Preliminary targets remain C6 can ≤75°C (stop at85°C), T1 ≤90°C and U1 SOURCE/D1 case ≤100°C; component derating or other rated limits take precedence. These case targets do not establish junction temperature. Apply a manufacturer-supported junction estimation method and record its uncertainty, or leave junction temperature unqualified. Stop earlier for abnormal regulation/current, rating violations or visible degradation.

T1 remains catalogue Coilcraft MSS1210H-125KED, not a custom winding. Its earlier 50.2–90.3°C range came from assumed core loss and thermal resistance, not this layout or measurements. Do not use that range as layout acceptance. R7 remains HVR25; the older VR25 thermal resistance does not apply. Check actual mounting, local ambient, power/voltage derating and soldered clearances on the prototype.

## Geometry and insulation scope

The independent matrix retains all55 net-pair screens: local floating control pairs use0.25mm, LED_PLUS/DC_RETURN1mm and other pairs2mm. Native manufacturing clearance and track-width floors remain0.3mm; holes0.3mm, annular width0.2mm, copper-edge0.5mm. A factory minimum is not a functional insulation requirement.

Intrinsic U1, BR1 and D1 land spacings do not meet every unmodified2mm pair target. The existing finite package assessments are retained as bounded laboratory engineering concessions, with unchanged floors and escape margins. They are not normative insulation waivers or human approval. The strict screen must remain visible alongside the bounded screen. Neither soldermask nor PCB surface geometry establishes three-dimensional air clearance, formed-lead/solder geometry, access protection or standards compliance.

The horizontal C6 maximum can and vent projection are protected on both copper faces in the correction candidate. The final candidate points the can toward -Y, with leads near the lower edge. Its maximum can extends0.25mm beyond the left PCB edge;2.5mm of the5mm free vent reserve lies above the PCB edge. The fixture must provide that free volume and support the manually formed part. Rectangular50×32mm PCB dimensions do not include that external fixture clearance. Native3D models illustrate geometry; they do not qualify the sample, fixture or final enclosure.

## Acceptance boundary

A clean routed CAD candidate requires fresh ERC, native DRC and schematic parity, zero unrouted connections, exact46-pin/11-net intent equality, the bounded55-pair screen, saved-fill freshness, spatial/consumer consistency and direct inspection of both faces. The Kelvin path requires an additional same-net intersection check because native DRC cannot detect an unwanted same-net force/sense join.

Those design checks may support an engineering review packet. They do not supply missing exact-stage human decisions, provider/process confirmation or physical qualification. Full Toolkit product release remains blocked wherever those inputs are absent. No order, supplier communication or powered test is authorized by this document.

