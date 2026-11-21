# Isolated flyback feasibility calculation

VEL-FLYBACK-01 r2, 2026-11-14. Author: /root. Stage: specification investigation, not schematic approval. Product requirements r11 on branch `spec/owner-interview-reset-2026-11-14` remain authoritative. Architecture A is owner-selected; all parts and numbers below are engineering candidates. Files belong under `hardware/E27/workflow/specification-reset/driver-study/`.

## Decision supported by this study

Continue evaluating TPS92310 with an approximately 4 mH, 4:1 primary/secondary flyback. Larger 4.7/5.6 mH alternatives do not automatically improve the design: with the same turns they raise flux and move the lower frequency corners downward. This calculation supports further investigation only; it does not establish controller regulation, fit, protection, lifetime or manufacturability. Do not generate a schematic or buy this transformer from these numbers.

The calculation exposed a meaningful protection constraint: a hypothetical 30 V maximum output cannot simply be promised by setting the controller's auxiliary-winding OVP. Its tolerance and transient allowance must be budgeted. The safe-access voltage/energy limit itself remains undecided; 30, 33 and 36 V here are sensitivity examples, not safety classifications.

## Reproducible model and assumptions

Run `python calculate.py > results.json` using Python standard library. Three inductance choices, each 144 enumerated combinations (432 total), cover 200/260/357.796 V DC bulk, 18/21/24/27 V load, 228/250/286.227 mA total secondary current, inductance +/-10%, and 0.5/1.5 us idle delay. Upper total current includes the earlier hypothetical 10 kohm bleeder at 27 V and -1% resistance. Applying that largest bleeder current at every output voltage is a deliberately conservative rectangular screen. The input DC window is an investigation assumption, not an accepted mains range or simulated rectifier waveform.

This is an ideal triangular-current single-cycle critical-conduction model. With n=Np/Ns, reflected voltage Vr=n*(Vo+0.8), ton=Lp*Ipk/Vbulk, toff=Lp*Ipk/Vr and T=ton+toff+delay, the equation Isecondary_average=n*Ipk*toff/(2*T) is solved for Ipk. It is not a fixed-frequency energy estimate. The script checks energy and secondary-current identities at every corner. It does not implement TPS92310 control law, line-cycle behavior, parasitics, startup, burst, missing load or short circuit. The 0.8 V diode approximation and delay are assumptions.

| Nominal primary inductance | Calculated switching frequency | Calculated peak flux swing, 200 primary turns | Primary peak current maximum |
|---|---:|---:|---:|
| 4.0 mH | 53.4–136.9 kHz | 0.174 T | 0.249 A |
| 4.7 mH | 46.5–118.7 kHz | 0.202 T | 0.246 A |
| 5.6 mH | 39.8–101.5 kHz | 0.237 T | 0.242 A |

These are extrema among sampled combinations, not mathematical bounds over every continuous operating condition or manufacturing corner. TI discusses typical design frequencies of 60–150 kHz; the 4 mH screen extends below that guidance and requires controller/timing verification. Do not label it a frequency pass. The modeled minimum on-time for 4 mH is 1.47 us; fault/startup pulses are outside this model.

For 4 mH, primary RMS reaches 81.3 mA, secondary RMS 436.2 mA, and secondary peak 997.1 mA. Ideal transferred magnetic power reaches 7.96 W including the assumed diode drop and secondary load. This is not input power or a transformer rating. The previously proposed capacity reserve is not qualified by this calculation.

## Transformer candidate, not construction instructions

TDK EFD20/10/7 has published effective/minimum area 31 mm2. A published N87 gapped AL100 +/-10% core option exists (`B66417U0100K187`); the mating core, bobbin and insulation system still need selection. With 200 primary / 50 secondary turns its nominal inductance is 4.0 mH. An exploratory 50-turn auxiliary winding supplies the primary controller; it is not electrically connected to the accessible LED secondary. Counts describe a model, not a released winding schedule.

The simplified reluctance calculation gives an effective gap near 0.39 mm, whereas the manufacturer lists an approximate mechanical gap of 0.49 mm for that option. Use the manufacturer's characterized AL rather than machining a gap from the simplified formula. Winding fill, conductor diameters, copper loss, leakage inductance, ferrite loss at actual waveform/temperature, hot saturation margin, creepage/clearance, dielectric barriers and winding termination are unverified. Catalogue core dimensions do not prove an isolated finished transformer fits an E27 base.

At maximum assumed inductance, hypothetical hard primary limits of 0.25/0.30/0.35 A give about 0.177/0.213/0.248 T. These sensitivity values do not set a safe current limit. Controller threshold tolerance, propagation delay and hot magnetic properties must be included before choosing a sense resistor or claiming short-circuit survival. No transformer supplier has confirmed feasibility or insulation.

## Power devices and incomplete heat budget

| Function | Candidate / screen | Limitation |
|---|---|---|
| Controller | TPS92310, primary-side sensed isolated flyback candidate | No selected operating mode, resistor network or validated current accuracy; sourcing not confirmed. |
| Switch | STD3NK80Z-1, 800 V, IPAK through-hole | Comparison candidate, not an SMT/JLC-ready selection. Its 4.5 ohm maximum is specified at 10 V gate and 25 C; actual gate drive and hot resistance need verification. |
| Secondary rectifier | STTH1R02A, SMA, 200 V family | Exact A suffix matters. Package thermal conditions and pulsed current/recovery behavior require review; catalogue average current alone is insufficient. |

The modeled maximum drain plateau is 469 V. Adding an assumed 100 V leakage overshoot produces 569 V; this does not bound actual spikes, mains surge or clamp faults. An 800 V comparison device leaves more nominal voltage room than 650 V, without establishing a qualified rating. Secondary reverse voltage is 116.45 V before ringing, motivating a 200 V comparison diode, not proving adequacy.

For 4 mH, isolated loss proxies are: switch conduction up to 0.030 W using the cold 10 V resistance; diode conduction up to 0.229 W with fixed 0.8 V drop; hard-switch overlap approximately 0.077–0.261 W assuming 50 ns. The latter is only a sensitivity illustration in a valley-switched application. No total efficiency is calculated: hot resistance, gate drive, core/copper, clamp, capacitive switching, reverse recovery, bridge, startup and controller losses remain unbudgeted. Do not add independent worst corners and call that a validated thermal result.

## Startup and overvoltage findings

TI gives full-temperature startup UVLO extremes of 23–29 V and an upper running turn-off threshold of 15.7 V. The exploratory auxiliary ratio gives approximately 18.3–27.3 V after the assumed rectifier drop in normal operation. An auxiliary voltage below startup threshold can maintain operation after startup; the separate startup path must charge VCC sufficiently and sustain the transition. With an illustrative 8 uF minimum capacitance, a 23-to-15.7 V fall stores 1.13 mJ; at an assumed constant 10 mA draw it takes 5.84 ms. That is only a threshold/charge screen, not proof of startup or a selected capacitor/resistor. Startup delay, low-line charging, actual gate-current draw, hot leakage and worst-case VCC overshoot still require calculation.

The ZCD overvoltage threshold spans 4.1–4.5 V with three-cycle debounce. OVP senses the raw auxiliary winding plateau, approximated here by Vo+0.8 V at a 1:1 auxiliary/secondary ratio; VCC additionally loses its own rectifier drop. Using a hypothetical 10% normal headroom and 1 V transient allowance, the divider-ratio intervals for 30 V and 33 V ceilings do not overlap even before divider tolerance. A 36 V example has an ideal interval, but that does not approve 36 V, safe contacts, single-fault behavior or transient overshoot. The same 1:1 auxiliary ratio would produce about 36.3 V at VCC if output reached 36 V under the assumed drops, already above TI's 36 V operating ceiling. Therefore auxiliary supply clamping/ratio and output protection must be designed jointly; the 40 V absolute maximum is not an operating target. This algebra excludes leakage spikes, bias loading and fault dynamics. A tighter independently bounded ceiling could require secondary sensing/protection, a different controller or a revised verified operating envelope. No extra panel electronics are selected yet.

For input bulk storage, an illustrative 10 uF capacitor at -20%, 10 W draw and a full 10 ms discharge from the ideal 207 V AC peak yields 246.37 V. This supports exploring 200 V as a conservative DC sample point but is not a bridge/capacitor simulation. Inrush, capacitor ripple/lifetime, PF, harmonics and flicker remain open. A bulk capacitor choice cannot inherit a controller brochure's PFC claim automatically.

## Next engineering work and stage status

First complete the operating-mode/current-programming and startup calculations, compare a current-production integrated-switch alternative, and resolve the normal/fault accessible-interface voltage and energy limits. Then obtain a feasible transformer/process route and optical/thermal LED envelope. Actual specification approval and toolkit installation/environment checks remain separate prerequisites before CAD. This study does not replace them or introduce an external-reviewer-before-design prerequisite. The base cover is required, but an instruction to unplug does not by itself establish safe accessible contacts, insulation or residual charge.

No schematic, ERC/DRC, SPICE simulation, measured waveform, physical safety test, human engineering review, supplier confirmation or order is claimed. Independent agent review of this frozen study is recorded separately; earlier specification/LED reviews do not approve it.

## Primary sources inspected, 2026-11-14

- TI TPS92310 SNVS792: https://www.ti.com/lit/ds/symlink/tps92310.pdf (electrical table pp. 3–4, operation/design discussion). Different reference-circuit input conditions are not copied into this project.
- TI SLVA511: https://www.ti.com/lit/an/slva511/slva511.pdf (compact lower-power reference; not this design).
- TDK EFD20/10/7, October 2022: https://www.tdk-electronics.tdk.com/inf/80/db/fer/efd_20_10_7.pdf (core data and AL option).
- ST STD3NK80Z-1 DS14364 rev1: https://www.st.com/resource/en/datasheet/std3nk80z-1.pdf (ratings and gate conditions).
- ST STTH1R02 DS4743 rev4: https://www.st.com/resource/en/datasheet/stth1r02.pdf (rectifier family/package ratings).
