# SB01 fixed-package spacing: electrical stress basis

Date: 2026-11-24. Actual contributor: `/root/sb01_spacing_stress_basis`.
Scope: read-only assessment of BR1, U1 and D1 in the existing SB01; no CAD, netlist, rules, MPN or controller change. Recommendation to the coordinator, not human acceptance or certification.

## Result and boundary

All five reported pad gaps correspond to selected manufacturers' suggested solder-land geometry. This supports retaining those footprints to manufacture an **unpowered bare laboratory test article**, subject to the independent geometry/fabrication audit and an explicitly scoped deviation from the project's voluntary 2 mm screen. It does **not** establish their dielectric adequacy under actual operating, startup, surge or fault stress. Keep the strict spacing result as FAIL with the exact five pad pairs and 18 local escapes visible; do not relabel it PASS.

The project has not supplied an applicable normative clause establishing that every pair requires 2 mm, or an applicable normative derivation proving these smaller gaps sufficient. Neither a semiconductor's 725/1000 V rating nor its suggested pad pattern transfers to a PCB insulation rating. There is no new technical basis here to close powered safety qualification. Bare-board procurement readiness must be distinguished from readiness for energized use.

Reviewed PCB SHA256: `532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`. Source paths and local evidence hashes are recorded in `evidence-hashes.json` beside this report.

## Circuit interpretation

BR1 is MB10S-13: pin 1 BUS_RECT (+), pin 3 DC_RETURN (-), pins 2/4 AC_FUSED/AC_N. RF1 is 47 ohm, with the MOV across the AC input after RF1. L1 feeds BUS_FILTERED and C4 is returned to DC_RETURN. U1 LYT1603D has pin 4 DRAIN on BUS_FILTERED; pins 5–8 SOURCE on SW_SOURCE. Pin 3 FB_INDUCTOR is connected to SOURCE through parallel sense resistors R5/R6; pin 2 M is referenced to SOURCE via R4 and to LED_PLUS via R7. D1 US1M-13-F is the freewheel diode, cathode (pin 1) at FB_INDUCTOR and anode (pin 2) at DC_RETURN. This is a non-isolated high-side buck: output DC_RETURN is not a protective-earth or safe-touch reference.

For the intended 207–253 V RMS sine supply, the ideal line crests are 292.74–357.80 V (230 V nominal: 325.27 V). These are sinusoidal source calculations, **not all-operation rail maxima**. Rectifier drops normally reduce rail voltage, while filter energy exchange, startup and ringing can raise it.

## Individual pair decisions

1. **BR1.1 / BR1.3 — BUS_RECT / DC_RETURN, 1.500002 mm.** This sees rectified input rail voltage. The low-frequency line-only estimate reaches approximately 357.8 V before bridge drops. It is not bounded by that value during filter charging. The existing simplified SB01 cold-plug screen predicts C1/BUS_RECT peak 706.30 V. The bridge's 1000 V rating is not the external gap's rating. Diodes MB10S datasheet p.4 gives pad center distance C = 2.50 mm and pad width X = 1.00 mm, implying the 1.50 mm gap. Decision: manufacturer-pattern conformity is supportable; powered transient/insulation acceptance remains unknown.

2. **BR1.2 / BR1.4 — AC_FUSED / AC_N, 1.500002 mm.** This is the instantaneous differential line voltage, up to 357.8 V magnitude at 253 V RMS before disturbances. The sine's 715.6 V peak-to-peak is not its simultaneous differential magnitude. Mains impulses, upstream source impedance and MOV tolerance/current alter the maximum. The selected MOV's 710 V at 10 A specification is a test point, not a universal clamp ceiling. The same MB10S p.4 land calculation supports 1.50 mm. Decision: manufacturer-pattern conformity is supportable; surge/fault qualification remains unknown.

3. **U1.2 / U1.4 — M / BUS_FILTERED, 1.940002 mm.** The M-pin voltages in the PI datasheet are relative to moving SOURCE, not DC_RETURN. In the freewheel/OFF interval, SOURCE is near the freewheel node and M is near SOURCE plus its sensing voltage (normal OFF description: 1–2.4 V). DRAIN remains on the high filtered bus: DRAIN–M therefore sees approximately the full filtered rail, not merely a 2.4 V signal. ON-state input-sensing current changes this relationship. PI p.11 gives 1.27 mm pin pitch and 0.60 mm land width: two pitches minus land width = 1.94 mm. Decision: manufacturer-pattern conformity is supportable; precise startup/surge/fault upper bound and insulation acceptance remain unknown.

4. **U1.3 / U1.4 — FB_INDUCTOR / BUS_FILTERED, 0.670002 mm.** In the ON interval the differential is approximately MOSFET ON drop plus sense-resistor drop. In the OFF/freewheel interval, FB_INDUCTOR is near minus the diode forward voltage relative to DC_RETURN, while DRAIN is at BUS_FILTERED. Differential stress is approximately VBUS_FILTERED + VF. A conditional line-only illustration is 357.8 + 1.7 = 359.5 V; 1.7 V is US1M's specified 1 A/25°C forward-voltage maximum and is **not** a validated diode limit for every startup current/temperature. Existing simplified C4 startup prediction is 588.70 V before adding local dynamic effects. PI p.11 gives 1.27 − 0.60 = 0.67 mm between adjacent lands. Decision: manufacturer-pattern conformity is supportable; this is the most visibly constrained fixed gap, and powered dielectric acceptance cannot be asserted from geometry or component ratings.

5. **D1.1 / D1.2 — FB_INDUCTOR / DC_RETURN, 1.500002 mm.** During freewheel the diode is forward biased by approximately VF. During MOSFET ON, its cathode follows the high-side switch through the sense path, giving reverse stress approximately the filtered rail minus MOSFET/sense drops. Startup and switching ringing can increase it. US1M's 1000 V reverse rating is a semiconductor limit, not a PCB clearance proof. Diodes US1A–US1M p.4 explicitly gives recommended SMA pad gap G = 1.50 mm. Decision: manufacturer-pattern conformity is supportable; actual reverse waveform and insulation acceptance remain unknown.

The 18 nearby escape findings need their own exact object/zone list and confirmation that they are truly short package approaches, not a blanket exception for each high-voltage net. This stress review does not independently establish their actual geometry.

## Transient and fault limitations

The existing `work/sc09-simple/reviews/reality.damping-screen.json` is a calculated **screen**, not a measured upper bound. Its 47 ohm group assumes an initially discharged C1–L1–C4 filter, ideal blocking bridge, a 253√2 V input step, 50 ns integration steps over 1 ms, and zero L1 DCR as a deliberately low-damping case. Its component-tolerance sweep reports C1 peak 706.299 V, C4 peak 588.698 V and L1 peak 2.126 A. Nonlinear inductance/saturation, actual MOV behavior, converter loading, retained capacitor charge, source parasitics and the complete mains surge envelope are not captured. These values must neither be presented as actual observed stresses nor used as guaranteed ceilings. In particular a generic 400 V operating screen does not close cold-plug stress.

Open sense/divider components, open freewheel diode, shorted MOSFET, MOV failure, LED disconnection, filter saturation and incoming impulses can change node voltages and timing. This review has no validated exhaustive single-fault voltage map or independent fail-safe disconnect proof. PI's own checklist (datasheet p.6) requires measuring peak drain voltage, including startup/fault conditions, and checking it against the device's limit. An internal overvoltage/current function is not an external insulation certificate.

Recommended evidence before energized qualification: measured differential waveforms at both rectified rails and U1 D–SOURCE/D–FB/D–M and D1 reverse voltage across relevant input/load/temperature corners; explicit startup/restart/retained-charge and justified surge/fault cases; justified applicable insulation category, pollution/CTI/altitude and finished-board solder/3D creepage assessment. A responsible human must define safe test setup and stop criteria separately. No physical tests were performed for this report.

## Primary evidence

* Power Integrations, LYTSwitch-1 family datasheet, Rev B, July 2016: pp.2–4 pin references and operation; p.5 layout; p.6 measured validation checklist; pp.7–9 electrical limits; p.11 SO-8 D08A land pattern. Official URL: https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf
* Diodes Incorporated, MB10S DS39045 Rev 3-2, March 2017: p.2 electrical ratings; p.4 MBS recommended land pattern. Official URL: https://www.diodes.com/datasheet/download/MB10S.pdf
* Diodes Incorporated, US1A–US1M DS16008 Rev 11-2, December 2014: pp.1–2 identity, polarity and electrical ratings; p.4 SMA recommended land pattern. Official URL: https://www.diodes.com/datasheet/download/US1M.pdf
* Power Integrations RDR-464, 28 October 2016: pp.7–10 schematic/layout; pp.38,40–43 drain/startup/short/diode/open-load waveform examples. Official URL: https://www.power.com/sites/default/files/documents/rdr464.pdf . The online endpoint returned an access error during this review; the existing local PDF was read and hashed. This is a related reference topology with different selected parts, not a test report for SB01.

Documentary dimensions support compatibility of the selected land patterns. They do not establish applicability or compliance with a particular IEC safety clause. No standard minimum is invented here.
