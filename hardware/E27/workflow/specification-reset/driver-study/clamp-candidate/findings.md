# Controller-aware primary clamp proposal

VEL-CLAMP-01 r1, 2026-11-16. Specification investigation following component proposal r2 at draft commit e951517b2becf6ecb2002f2d5ad5c17aa3cb2d3f. Coordinator/sole writer `/root`. R-SUPPLY/R-FAULT/R-EMPTY/R-THERMAL/R-COMPAT/R-BUILD/R-OFFLINE. **No circuit freeze, schematic approval, fault-survival or working-lamp assertion.** Architecture A and simple common panels remain unchanged.

## Proposed implementation

Prefer a **direct avalanche clamp**, comprising **Diodes Incorporated US1M-13-F** and **Vishay SMBJ160A-E3/52**, as the next integrated candidate. Both are surface-mount references. Do not fit the separately studied RCD capacitor/resistors in parallel by default.

Proposed primary-only node intent: US1M anode to MOSFET DRAIN, its cathode to CLAMP; unidirectional TVS cathode to CLAMP, TVS anode to rectified input BUS+. The MOSFET source/primary return and isolated panel return remain separate domains. This is a proposed node/polarity description for review, not a complete approved physical-pin connectivity contract or a generated schematic.

The direct branch has no separate clamp storage capacitor to precharge and no continuous parallel clamp-bleed resistor. It still dissipates leakage energy, including some diverted magnetizing energy, and its TVS heating and parasitic ringing must be checked. A capacitor-free analytical branch is not literally free of component/layout capacitance.

## Why the initial RCD comparison is not preferred

A bus-return 99.8 kohm / 47 nF RCD branch was calculated first using exact reference parts in parts.csv. Its finite-capacitance pulse map conserves leakage plus reflected-source energy; it includes resistor decay between pulses and omits resistor current during charge. A representative RK4 pulse including that resistor was compared at 2 ns/1 ns steps; this is a numerical sanity check, not a whole-converter bound.

| Comparison result | Actual scope |
|---|---|
| 27,648 normal RCD parameter samples | Primary CC/DCM witness, four assumed leakage fractions, resistor/capacitor/diode corners. |
| At leakage ≤2%: drain screen maximum 607.1 V, each resistor average upper proxy ≤0.200 W | Includes assumed +50 V commutation allowance and high-line bus; no measured spike or input surge. |
| At leakage up to5%: drain screen maximum679.4 V, each resistor average upper proxy≤0.370 W | Same constructed normal law; not a fault envelope. |
| 96 low-current/light-load combinations | 64 have no valid assumed periodic secondary-transfer solution;32 give leakage-reset times over600ns. Independent current/frequency points are not a verified UCC operating trajectory. |

TI's native controller guidance calls for leakage reset shorter than600ns at minimum primary current and2.2us at maximum current, followed by sufficiently settled VS ringing. Passing full-load drain-voltage arithmetic alone misses that requirement. The RCD sweep identifies a light-load/sample risk; it does **not** prove that every possible RCD design or actual no-load trajectory fails. This is a bounded clamp correction, not a new converter-topology survey.

RCD fault-train stress tests also show why a normal-only clamp cannot establish immunity: with2% leakage,42V assumed output,0.756A assumed fault peak and106kHz assumed uninterrupted train, the screen crosses700V on pulse24 and800V on pulse110 for the lower capacitor corner. These are counterexamples under imposed hypotheses, not measured fault timing, actual IC behavior or a safe pulse allowance. Predictions after device limits are exceeded have no survival meaning.

## Direct-clamp calculations and conditions

SMBJ160A's native table gives160V stand-off,178–197V breakdown at1mA/25°C,259V clamp at2.3A/25°C and maximum VBR temperature coefficient0.108%/°C. US1M has1000V repetitive reverse rating and75ns recovery under the source test conditions. Neither table supplies the complete actual high-frequency I–V–temperature/forward-recovery waveform.

The constant-avalanche-voltage sensitivity uses175.1–287.0V endpoints. The lower endpoint extrapolates VBR from25°C to10°C; the upper scales259V by the VBR temperature coefficient to125°C. **Scaling Vclamp with the VBR coefficient is only a diagnostic proxy, not a guaranteed hot clamp bound.** The1mA breakdown test also does not bound the full low-current tail. Actual dynamic behavior remains required.

| Result under proposed ≤1% leakage target | Interpretation |
|---|---|
| 17,280 deduplicated static endpoint samples | Subset of34,560 samples across0.5/1/2/5% leakage; no vendor controller model or statistical confidence implied. |
| TVS average power proxy ≤0.229W | Normal25°C-style current/frequency witness with independent voltage stress endpoints. At2% leakage this approximately doubles; insulation must not be compromised to meet the target. |
| Single-pulse TVS energy proxy ≤4.20uJ; peak power proxy ≤99.1W | Does not turn the600W10/1000us non-repetitive/duty-limited table into a repetitive tens-of-kHz qualification. |
| Required effective thermal resistance ≤174.6°C/W in worst normal sensitivity | Conditional local85°C, junction target125°C. Datasheet100°C/W is typical on its specified pad arrangement, not a guarantee for the bulb PCB;5W rating assumes an infinite heatsink and is not adopted. |
| High-line drain endpoint screen ≤696.5V | Includes +50V assumed local commutation allowance. Just3.5V below the700V engineering screen and103.5V below the800V absolute rating; **not** a proven waveform margin or mains-surge pass. |
| Minimum-current leakage-reset proxy ≤94.3ns | Includes the old static25°C OVP endpoint as a conservative extra voltage sensitivity. Faster than600ns in this ideal avalanche model; actual auxiliary/VS ringing and diode recovery remain. |

The earlier component packet allowed2% as a comparison. The preferred direct-clamp candidate now targets **Lleak/Lp≤1%** to reduce continuous TVS heating. This is a proposed transformer engineering acceptance condition, not a manufacturer guarantee, owner-approved product limit or permission to alter insulation. Measure/report the exact finished-transformer inductance/leakage configuration and frequency; reject or recalculate if the target is not achieved. No manufactured transformer, final winding or JLCPCB route is confirmed.

## Coupled startup, fault and safety limits

A direct branch avoids the additional47nF RCD-storage startup-energy burden, but junction capacitance, leakage-energy loss, gate draw and feedback timing still affect acquisition. The parent's4.3mA/0.300ms startup figures remain conditional hypotheses; they are not refreshed full-circuit startup evidence or closure of **RC-BIAS-001**. The RCD comparison could not inherit those figures unchanged if selected.

Fault-train calculations for the direct clamp report power and reset-time/period compatibility. Some imposed high-output/high-current combinations have no complete reset within a switching period and are flagged, not passed. A fixed0.4W average dissipation example yields required burst duty factors, not actual thermal protection or controller retry timing. Datasheet fault shutdown intent is not a bounded detection/turn-off delay.

**RC-COMP-002 remains major/open**: establish actual leakage/diode/TVS waveforms, VS reset/ringing, OVP and current-fault latency, pulse trains, mains surge path, device/clamp SOA and temperature, including clamp faults. A drain clamp does not protect the rectifier, bulk capacitor or HV startup pin against every input surge. Service-access energy/discharge/cooling, whole-lamp thermal recovery, optics and sourcing remain open in their existing records.

Native manufacturer references and hashes are in sources.json; relevant source tables were rendered/read. No actual SPICE/vendor model, CAD, ERC/DRC, installed-toolkit check, supplier communication, purchase or physical test occurred. All results are analytical/constructed numerical sensitivities. This proposal advances the component-level protection design; it does not accept the full circuit or any manufacturing release.
