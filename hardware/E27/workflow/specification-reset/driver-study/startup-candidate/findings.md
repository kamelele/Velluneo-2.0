# Integrated startup charge and auxiliary-sampling proposal

VEL-STARTUP-01 r1, 2026-11-16. Specification investigation, baseline draft3f1fa94710b3a92dd957841619716d76c176f0e9. Writer/coordinator `/root`. R-SUPPLY/R-COMPAT/R-FAULT/R-EMPTY/R-LIGHT/R-THERMAL/R-BUILD. **Conditional calculations and proposed component values; no circuit freeze, approved schematic or verified working lamp.** Architecture A and common simple panels remain intact.

## Concrete proposed update

| Function | New investigation reference | Purpose / boundary |
|---|---|---|
| VS upper resistor | 80.6kohm, Vishay CRCW080580K6FKEA,0805 | Lower divider impedance with negative VS-current headroom at high line. |
| VS lower resistor | 17.4kohm, Vishay CRCW080517K4FKEA,0805 | Preserve a suitable CV ceiling while evaluating resistor-temperature effects consistently. |
| CS line compensation | 1.40kohm, Vishay CRCW06031K40FKEA,0603 | Starting value within the recalculated1.09–1.94kohm range for assumed100–150ns total turn-off delay; not a calibrated delay guarantee. |
| VDD capacitors | Retain2×470nF C0G candidate | Do not increase capacitance beyond the native1uF recommended upper value based merely on the older reference design described below. |

No VS filter capacitor is proposed. The native controller guidance warns against one that interferes with waveform sensing. Exact footprints, pin graph, live sourcing and whole-board assembly remain later gates. The resistor MPNs are proposed from the native family/ordering basis; catalog-search matches are not a JLCPCB availability confirmation.

## Startup calculation: distinguish the phases

The earlier constant-current VDD examples were deliberately simple. This study separates:

1. First three minimum-current pulses: assumed duration, base IC/ancillary draw, and3×assumed gate charge. Conservatively credit no output charging during this interval.
2. A separate assumed0.100ms settling interval at the106kHz gate-charge envelope, without crediting output charge.
3. Constant-current output charging: integrate the pinned static Cree LED law, output bleed and optional ESR. Gate switching-frequency demand follows a conservative envelope of the constructed CC/DCM witness rather than106kHz throughout the ramp.

The auxiliary takeover target now explicitly includes a10V trough target,1V auxiliary-diode drop,0.5V assumed winding loss and0.5V assumed ripple. It requires approximately15.86V output. The previous15.18V proxy used a different reserve allocation; it is not copied as the new complete trough criterion.

128 parameter combinations cover4.032–20.592uF output capacitance,0/0.24ohm assumed ESR,7/8 LEDs,0/−0.3V per-LED assumed forward-voltage shifts,12/16nC assumed actual-drive gate charge and2.95/3.5mA assumed base draw. The temperature-shift and combined capacitor stress factors are sensitivities, not manufacturer guarantees. Gate-frequency dynamics and immediate post-settling CC behavior are constructed hypotheses, not the UCC's implemented startup state machine.

| Calculated charge-budget result | Scope |
|---|---|
| Maximum permissible first-three-pulse interval under the main12nC/2.95mA budget: worst case0.952ms | Also includes the separate0.100ms settling interval. Not a datasheet timing bound. |
| Across the larger16nC/3.5mA stress budget: worst case0.498ms | Identifies sensitivity to actual gate and IC current, not an approved component envelope. |
| If the first three pulses finish within0.300ms: lowest takeover VDD is10.78V | Above the internal10V calculation target under all stated sensitivities. Not measured or full-circuit evidence. |
| At1ms first-three-pulse interval, the main-budget worst case falls below10V | The missing acquisition-time evidence still matters; no unconditional startup pass. |

The2.65mA IRUN source limit is specified under the datasheet's25V supply test condition. The2.95mA base budget includes a0.3mA allowance, and3.5mA is an additional sensitivity; neither establishes actual draw across the9–23V startup trajectory. The12nC gate-charge allowance remains unverified at actual drive; the16nC case does not convert a typical model into a guaranteed limit.

## Source discrepancy: no automatic larger capacitor

Native SLUSB86C recommended operating conditions list a0.047–1uF VDD bypass range. An older native TI30W reference, TIDUAG6A(2015), explicitly uses10uF and discusses a1s startup example with different startup-current assumptions. The native EVM-160 BOM lists330nF. These are different designs and source conditions; the older10uF example is **not** treated as permission to override the later recommended table, nor as a confirmed distinction between local bypass and total reservoir capacitance. No10uF VDD variant is selected here. A larger-capacitance path would require resolving that source/implementation question and fresh affected review.

## Sampling-node and divider limits

The new divider is evaluated with±2.1% resistor envelopes, covering1% initial tolerance plus100ppm/K over the stated analysis range. IC reference-temperature slope remains nominal. This is an endpoint sensitivity, not a complete temperature guarantee.

| Refreshed result | Interpretation |
|---|---|
| CV27.93–33.54V; static25°C OVP32.94–37.86V | Replaces the old-divider endpoints for this proposal. Nominal output ceiling is about30.6V. Neither interval is a user-access classification or bounded dynamic overshoot. |
| VS negative-current magnitude at high-line envelope≤0.831mA | Below the1mA recommended magnitude in this screen. A400V bus example gives0.929mA; it is not a whole input-surge qualification. |
| Divider source resistance maximum14.61kohm | Old93.1k/20.5k pair gives17.15kohm under the same±2.1% envelope. The current/impedance/CV tradeoff is explicit. |
| Single-pole pin-capacitance allocation≈8.65pF | Old divider gives7.79pF under the same conservative combined timing allocation. Includes actual input/layout/probe loading; no actual pin capacitance or VS ringing was obtained. |

The allocation assumes a1V initial VS error settling to0.1V, a combined600ns precharge/reset engineering budget and a200ns end-of-demagnetization guard. These summed allocations are not the manufacturer's exact definition of leakage-reset time; the physical phases may overlap. They are a proposed conservative design/test screen, not a simulated ringing waveform.

For the direct TVS branch and refreshed OVP endpoint, ideal avalanche reset is about119ns at the examined minimum-current envelope. Allocating another100ns to recovery leaves a total node-charge allowance of roughly14/21/28nC if actual mean charging current is respectively50/75/100% of the minimum primary-current screen. Those current fractions are **assumptions**; Q/I is not a timing bound without a verified current floor/history. The typical ST charge-equivalent9.5pF at640V corresponds to6.08nC for illustration. It is not a worst-case charge at the actual drain swing, temperature or layout. TVS voltage-dependent capacitance, diode/winding/layout charge and inter-cycle charge retention remain within RC-CLAMP-001.

Changing the divider also changes line-run and compensation behavior. Old clamp fault-train25°C endpoints cannot be inherited as new dynamic bounds. Actual line sensing, current control, auxiliary ringing and fault behavior must be rechecked together. Existing healthy-current/flux and source/assembly uncertainties are not closed by these resistor choices.

## Actual model/tool experiment: failed, not evidence

A shared ngspice44.2 library is present even though no command-line ngspice executable was found earlier. The native public STN1NK80Z model was downloaded and pinned. It declares25°C use only. A compatibility adapter removed ELDO selector metadata and replaced its sole POLY cross term with an equivalent behavioral expression while retaining numeric device parameters.

The component transient fixtures **did not converge**: the simulation aborted at picosecond-scale steps before a usable gate-charge trajectory. An independent diagnostic context confirmed failures with SPARSE and KLU. This does not establish a physical transistor defect. `mosfet-model-check.py` records failure with exit1; model-check-status.json and model-check.log preserve the actual result. No model-derived Qg value is used in the startup calculation. The encrypted UCC models still supply no valid controller simulation.

**RC-BIAS-001 and RC-COMP-002 remain major/open.** This packet replaces crude charge bookkeeping with a coupled conditional calculation and supplies concrete divider/compensation references. It does not close acquisition timing, actual gate/bias draw, hot dynamic clamp/repetitive SOA, VS waveform, insulation, service-energy, optical/thermal/EMC, manufacturing or full specification prerequisites. No CAD, supplier communication, order, merge or physical test occurred.
