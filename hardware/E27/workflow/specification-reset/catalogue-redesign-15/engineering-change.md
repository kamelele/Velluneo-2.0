# CAT15 — selected factory-stock redesign basis

The owner explicitly excludes custom windings. Select MYRRA **74215**, a complete
factory-wound catalogue transformer; Farnell Poland4461577 shows48 units,MOQ1,
24.86PLN net on20Nov2026. Do not buy obsolete74015 or a bare bobbin/core kit.
The existing RFQ13/JLC14 transformer and production files do not meet this requirement.

Keep the isolated CC architecture and select120:27:14 turns,1.8mH. Use S3 pins7–10;
S1/S2 are real connected taps, externally unused. Follow the independent pin-intent
file. 19x16x19.5mm is the maximum body;19.5mm is HEIGHT. This is0.5mm higher than
the earlier18mm reservation, although substantially smaller in plan. Complete lamp
diameter60x120mm remains a target, not a proven enclosure fit.

Selected adaptation: R4=51.1k, R6=1.96k, R9=2.55ohm; R5=17.4k stays. Nominal
current is~250mA, CV boundary~29.95V and a **20..27V analytical load window** is
proposed. The old18V lower end is not carried forward. None of these screens proves
the required750..850lm at the diffuser; the final LED panel remains to be matched.
TD126.5ns and transformer efficiency90% are assumptions. Do not treat average CS
thresholds/frequency or static1.6V as proven individual-cycle bounds. The1.6V/RCS
fault screen exceeds the transformer's0.50Apk rating; abnormal stress is OPEN.

Select factory SMD R1=AC05AT0K04709JBW00, BR1=SDB107-TP and Q1=STD2N80K5 to remove
customer lead forming. U1=DBVT is a packaging-only choice. TVS1=LittelfuseSMBJ160A
has an actually stocked route. Keep F1: AC-AT is not a specified fusible resistor.
BR1's30A surge is lower than the former50A: rerun inrush/fuse/bridge coordination.
The new T1's unpublished leakage/DCR cannot inherit the custom transformer's20uH
assumption or thermal calculation. R10/TVS are stocked starting selections, not a
qualified new clamp; repeat clamp/reset/diode/thermal calculations and bench tests.

## Exact mechanical holds before applying new placement/routing

The proposed libraries below are source-dimension inputs, not accepted production
footprints. The old custom footprint must never be assigned to74215.

* T1: nine physical pins, missing3; row12.2mm, primarypitch2.7, secondarypitch3.5,
  recommended drill1.1mm, pin0.60+/-0.10, row tolerance+/-0.5,pitch+/-0.25mm.
  All2mm PTH lands give only10.2066mm nominal P/S copper separation and fail10.7mm.
  All1.5mm lands give10.7066mm but insufficient annulus under the earlier illustrative
  process budget. Candidate six1.55mm active PTH plus three NPTH clearance holes for
  unused5/8/9 gives10.7419mm nominal active copper gap. Unused pin metal and winding
  taps still exist. Validate real annulus, insertion, paste/mask, external metal,
  tolerances and component internal insulation separately; NPTH is not a safety waiver.
* Q1: manufacturer's DPAK land pattern has only1.8mm between drain tab and gate/source
  lands. This fails the unchanged project3mm HV/quiet floor. The datasheet's630Vrms
  footprint note supports investigation, not an automatically authorized exception.
  A demonstrably usable modified footprint or an explicit reviewed package-local
  policy decision is required before applying Q1. Never lower the global3mm rule.
* BR1: pad1=plus top-right,2=AC bottom-right,3=minus top-left,4=AC bottom-left,
  in TOP view. Maker assigns polarity, not numeric pad IDs; this is an explicit local
  mapping to check against the new symbol. Pads1.19x1.52, pitch5.21x8.74mm; P/N gap4.02mm.
* R1: maker WSZ pads4x10mm, centres22.7mm, innergap18.7mm; factory lead shape.
  ~10mm maximum height allowance. Keep away from C1, polymer and touchable enclosure.
* C1 remains stock radial; no forced pitch forming. Preserve2mm vent space and full
 10.5x22mm worst-case body allowance.

## Assembly and handoff

The proposal has29 electronic SMT positions, T1/C1 THT and two wire-pad pairs.
JLCPCB's listing is not supplier acceptance of the complete board. Source the exact
outside parts via agreed Global Sourcing/consignment or a separate assembly operation.
Quantity, feeder attrition, lead times, two-sided handling/panelization, native
centroids/rotations and the finished harness remain to be agreed after actual CAD.
No new CPL, Gerber ZIP or 'order-ready' PCBA BOM is emitted from stale coordinates.
