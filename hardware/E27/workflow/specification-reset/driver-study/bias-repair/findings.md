# Bounded controller/bias repair proposal

VEL-BIAS-REPAIR-01 r1, 2026-11-16. Owner/writer `/root`. Specification investigation only, based on product reset r11 and protection r1. **Not a circuit freeze or stage approval.** Addresses R-SUPPLY/R-COMPAT/R-FAULT/R-EMPTY/R-THERMAL/R-OFFLINE/R-LIGHT/R-BUILD; architecture A is preserved.

## Why this change

The TPS92310 diagnostic path has open major RC-PROT-001: only 0.56 V low-end and 0.85 V high-end VCC headroom in the prior illustrative corners, with unqualified precision-clamp loading and bootstrap timing. Instead of adding an LDO/guard and another bias path, investigate one bounded replacement, **TI UCC28711DR**, with integrated HV startup, 9–35 V recommended VDD, primary-side CC/CV regulation and an NTC input. No new topology survey, panel controller or user configuration is proposed. The old TPS candidate remains blocked; replacement does not close its finding.

Native TI SLUSB86C, SHA-256 in sources.json, is the numerical authority. A cached web rendering returned different table values during retrieval; those were rejected in favor of the downloaded native PDF and inspected page renders. Values used include UVLO 19/21/23 V on, 7.7/8.1/8.5 V off; recommended VDD capacitor 0.047–1 uF; IRUN maximum 2.65 mA without gate drive. This is not a selected manufacturing BOM.

## Diagnostic set and calculated evidence

| Item | Proposed comparison / result | Boundary |
|---|---|---|
| Magnetics | Np/Ns/Na = 152/38/28; AL=100 nH ±10%; Lp=2.3104 mH nominal; Ae=31 mm² | EFD20 reference geometry, not a manufacturable/insulation-qualified winding specification. |
| Current programming | 2.37 ohm ±1%; nominal total 250.6 mA at assumed transformer efficiency 0.90 | Independent VCCR/resistance/efficiency sensitivities give LED 223–276 mA after 10 kohm output bleed. Not guaranteed brightness accuracy. |
| Normal averaged witness | 2592 cases: 33.1–81.8 kHz; positive idle interval; primary peak 0.308–0.345 A; flux 0.136–0.186 T | Constructed DCM/CC energy witness, not actual IC timing. Effective demagnetization duty VCCR/VCST preserves the stated current/energy identities across independent table corners; this is not a guaranteed internal control law. 81.8 kHz is below the 92 kHz minimum table fmax, but valley/sample/settling constraints remain. |
| Auxiliary bias | 11.63–19.78 V assumed normal troughs after subtracting the 0.5 V ripple allowance | Low-end trough margin to recommended 9 V is 2.63 V. This is not a full trough-to-crest bound; an upper crest including ringing remains unqualified. No measured regulation/current loading or temperature component bounds. |
| Open-load control | Static CV sensitivity 27.84–32.27 V; OVP sensitivity 32.83–36.42 V at 25°C | CV uses nominal -0.8 mV/°C slope, not a guaranteed temperature bound; cable-compensation corners included. No-load normally regulates CV, not continual OVP/retry. |
| High bias illustration | At 40 V output, selected diode corner and assumed +3 V auxiliary ringing: 32.86 V | 40 V and 3 V are assumptions, not bounded overshoot. Cannot establish a VDD/fault rating. |
| Output storage | 10 uF nominal, 12 uF max and at least 4 uF effective | Unqualified component contract; actual DC-bias/temperature/age, pulse RMS/ESR and voltage rating need an exact part. No actual light-ripple result. |
| VDD storage | Total effective 0.75–1.0 uF including bypass/storage | Must meet the manufacturer's 1 uF recommended maximum. No nominal capacitor automatically meets this interval. |
| Bootstrap | 6 mA assumed total draw; output takeover proxy 15.11 V; charge proxy 0.808 ms; available/required charge ratio 1.39 | Leaves only 0.317 ms at this draw for the initial acquisition cycles. First three minimum-current cycles are not time-bounded by the datasheet; **startup remains unqualified**. Source capacitor formula gives 0.510 uF minimum under these assumptions. |
| Startup charging | Constant endpoint-current examples 49–329 ms | IHV is specified at VDD=0/HV=100 V, not a guaranteed full-charge curve. Not a turn-on delay guarantee. |
| Input storage refresh | 54 10 uF bus cases, old external startup feed removed in memory; bus floor 250.67 V, LF capacitor RMS max 96.7 mA | Original primary-buffer source hash verified, unchanged. Retains input bleed; no switching/ripple/lifetime/harmonics proof. |

## Fault and integration work that remains

The UCC28711's usual 0.78 V current-control threshold is separate from the 1.4–1.6 V backup fault threshold. At the latter, the linear magnetic proxy reaches **0.368 T before propagation delay**; core saturation, actual current limiting, reset and fault heating are not qualified. Do not treat normal flux as short-circuit proof. Retain RC-PROT-002/003 and the existing fault-contract intent; reinterpret open-panel response as CV regulation with OVP as backup, rather than mandatory immediate shutdown for every panel open. No safe interface voltage/energy or waiting time follows from these values.

The 100 kohm/B4250 NTC comparison gives approximately 78–94°C trip sensitivity with assumed 1% R/B tolerances and datasheet IC current/threshold corners. Neither exact NTC nor trip temperature/location is selected. An open NTC does not guarantee fail-safe thermal shutdown. Whole-lamp thermal mapping and recovery remain required.

VS sampling requires the actual leakage/ringing/reset waveform; line compensation is only a 1.24–2.22 kohm starting sensitivity for assumed 100–150 ns total delay. Exact MOSFET gate charge, diode behavior, transformer coupling/leakage, clamps, VS filter, protection timing and component ratings must be resolved together. The 6 mA bias budget is an analyst assumption, not a sourced MOSFET guarantee. Three-colour compatibility, current calibration, flux and optical modulation remain unverified.

TI's downloaded TINA model package contains an encrypted library. It was inspected but not executed. No SPICE, native CAD, ERC/DRC, physical test, supplier message, JLCPCB stock/assembly confirmation or order occurred. Toolkit install/doctor and the full specification gate remain pending. No outside reviewer is imposed as a prerequisite to calculations.

## Recommendation and next bounded work

Carry UCC28711 as the **proposed repair candidate**, with the TPS path explicitly blocked and preserved as history. Before any circuit freeze, qualify effective capacitors and actual gate/bias load, establish startup acquisition bounds, and discriminate normal CC/CV from short/fault behavior including magnetics. If those conditions cannot be met, return the candidate for correction; do not close RC-PROT-001 by changing controller names. This publication is preliminary evidence, not a replacement for the outstanding full specification packet and genuine owner review.
