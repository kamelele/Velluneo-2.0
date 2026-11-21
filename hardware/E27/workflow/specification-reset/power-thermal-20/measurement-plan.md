# POWER20 falsification and cooling measurements

This is a plan, not a test record or permission for an unqualified person to energize
mains hardware. Existing C16/C17 safety/assembly/insulation/fault holds remain.
Responsible qualified operator, sample ID, actual PCB/BOM/enclosure/LED assembly,
safe isolated instrumentation, barriers and exact stop limits must be assigned
before powered work. No physical operation occurred for this packet.

1. Confirm bought MYRRA74032 revision, fit, pin mapping, actual insulation and
   approved assembly including Q1 shoulder elevation. Obtain maker loss/DCR/leakage
   and thermal-rise data if possible. Measure these using appropriate methods on
   actual parts; do not transfer historical custom-winding data.
2. At207/230/253Vac50Hz measure true input watts, RMS current, PF and current
   waveform with a calibrated power analyzer. Measure synchronized total output
   and LED current/voltage; include the10k output bleeder separately. Efficiency
   to LEDs=PLED/Pin; driver dissipation=Pin-PLED. Record uncertainty.
3. Measure primary on/off currents and D3 current, fs/valley switching, bus ripple,
   VDD, gate and drain waveforms; confirm source-load charge and power balance.
   Separate Q1 switching/conduction and clamp heat by measured waveforms/calorimetry.
   Check first and repeated faults/startup against existing1.1Apk/voltage/delay
   screens before assuming normal power numbers cover abnormal operation.
4. Measure C1 LF/HF and C4 RMS currents by frequency band and temperature; compare
   corrected maker ripple ratings at actual temperature/frequency. Obtain ESR
   versus temperature/age and internal-rise data; existing RMS surrogate is not
   qualification. Check R1 steady/pulse energy and fuse coordination separately.
5. Thermal soak in final-size enclosure at room10/25/40C, base-up/base-down/
   horizontal and any worse orientation, with driver alone and LED operating at
   each line/load condition. Retain the revision12 thermal baseline: bare lamp
   holder, still air, no surrounding fixture and>=200mm nearby clearance. Measure air
   beside T1 without touching a warm surface, board, T1 winding/core/case, Q1case,
   D3 solder/lead, U1top, BR1, R1, TVS, C1/C4 case and LED solder points. Use safe
   isolated thermocouples, tiny sensors and emissivity-corrected thermography;
   avoid conduction errors from probes. Air, board and junction are separate.
6. Determine equilibrium and record time series using the existing revision12
   baseline: after>=3hours, critical temperatures change<1K/hour for1hour.
   A shorter logging interval does not replace this equilibrium criterion.
   Infer effective cavity and board paths from measured heat flows and paired
   LED-on/off tests. Fit actual thermal impedances, replace all guessed resistances,
   rerun POWER20 and check local gradients/uncertainty rather than merely average.
7. Stop before exceeding any maker absolute/operating limit or existing product
   limit; T1 surrounding air must remain<=50C. Initial reserve aims cavity<=45C,
   capcases<=85C, Q1junction<=110C require operator-adopted limits and uncertainty.
   D3 junction estimate uses measured lead+30*Pd3; Q1 uses measuredcase+4.2*PQ;
   U1top+5.1*PU1 is a characterization estimate, not a guaranteed network resistor.
   No extrapolation from case to capacitor/T1 internal temperature without data.
8. Compare a thermally separated LED carrier and insulated conduction to housing
   against a vented/printed shell. Keep primary metal inaccessible and preserve
   isolation, fire/material, creepage/clearance and contamination requirements.
   New mechanical or electrical changes need affected CAD/review checks.

Deliver calibrated logs, photos/sensor positions, ambient/line/load/orientation,
equilibrium uncertainty and worst observed conditions, then update power/cooling
requirements. Normal thermal operation does not close EMC/safety/fault/life gates.
