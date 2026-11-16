# LED/output-buffer coupling and revised investigation priority

VEL-LED-BUFFER-01 r1, 2026-11-16. Specification investigation against product packet r11 (Git blob 6493b29bd33fbde1f3c61c5e995b11447cb83e9b) and architecture A. No circuit, current, capacitor, ripple criterion or service delay is selected. Repository location: `hardware/E27/workflow/specification-reset/driver-study/coupled/`.

## Engineering decision supported

Do not advance the simple sinusoidal-power LYTSwitch-5 plus 470 uF output-capacitor path as the leading implementation for the owner's steady-light goal. Retain it as a comparison, and prioritize a primary-side energy-buffered isolated constant-current implementation for the next full comparison. This is an engineering investigation priority, not a specification gate approval, a validated alternative, or a claim that all LYTSwitch-5 circuits are unsuitable. Architecture A, a common enclosed base and simple interchangeable panels, is unchanged.

The coupled model shows that a seemingly modest output-voltage ripple can cause substantial LED current modulation. Increasing only output capacitance helps but has a size/storage/discharge cost. Actual flicker acceptance metrics and measurements remain open. Nothing here establishes compliance or selects TPS92310 automatically: that path still needs its identified protection, startup, regulation and manufacturing work.

## Better source evidence

A manufacturer electrical model for the exact JB2835BWT-G family was found through Cree LED's product page, downloaded as native text and hashed. A native CLJ-DS40 rev10B PDF was also downloaded and hashed. `sources.json` records both URLs, byte counts, access date and SHA-256. Original files are reference downloads, not redistributed in the repository.

The static diode equation at the model's nominal 25 C uses Is=9.8487e-31 A, N=1.5601 and series resistance 0.86341 ohm. This yields approximately 2.930 V and 1.024 ohm incremental resistance per LED at 250 mA. At the 55 mA reference it gives 2.701 V, versus the datasheet's 2.67 V typical value. That 31 mV difference is retained, not silently calibrated away. Model and datasheet are separate typical representations, neither a guaranteed production envelope.

The manufacturer model also contains temperature parameters EG/XTI. This study deliberately evaluates only its static 25 C equation. The 85 C cases use a uniform voltage-shift sensitivity based on the datasheet's typical -0.9 mV/C coefficient, retaining the 25 C curve shape; this is not a full SPICE temperature calculation or self-heating solution. An additional uniform +/-0.10 V per-LED offset is an analyst sensitivity, not a bin guarantee. Identical per-device shifts do not cover individual mismatch, faults or every CCT/bin.

## Coupled equations and actual control assumption

The manufacturer diode law is evaluated and inverted using Lambert W. A fourth-order Runge–Kutta solver integrates capacitor energy:

`d(0.5*C*V^2)/dt = Pavg*(1-cos(2*pi*100*t)) - V*I_LED(V) - V^2/Rbleed`

This is an averaged single-stage sinusoidal-power scenario at 50 Hz mains. Current through the nonlinear LED string and capacitor voltage evolve together; the load is no longer treated as fixed power while voltage changes. Bleeder is the earlier illustrative 10 kohm, not selected hardware. An ideal slow outer calibration adjusts average delivered power until mean LED current reaches the comparison target. It does not simulate a real feedback loop, demonstrate stability, or specify any LYTSwitch-5 resistor. Source-current pulses, switching dynamics, ESR/ESL, transformer/control behavior, optical conversion, startup and faults are excluded.

The script evaluates 96 combinations: 7/8 LEDs; target average LED current 250/283.5 mA; nominal capacitance 220/470/1000/2200 uF at -20%; fixed-temperature sensitivities 25/85 C; uniform voltage shifts -0.10/0/+0.10 V per LED. These are comparisons, not an authorized operating range. Temperature is imposed; ambient/junction rise, lifetime and thermal current derating are not solved. Results at 85 C do not establish permission to operate there at these currents.

## Results: current, not photometric flicker

Representative case: 7 LEDs, target 250 mA mean, 25 C static model, no added voltage shift, capacitance -20%.

| Nominal output capacitor | Minimum/maximum LED current | Electrical modulation `(Imax-Imin)/(Imax+Imin)` | Output-voltage minimum/maximum |
|---|---:|---:|---:|
| 220 uF | 64–440 mA | 74.5% | 19.00–21.81 V |
| 470 uF | 126–376 mA | 49.9% | 19.57–21.39 V |
| 1000 uF | 183–317 mA | 26.8% | 20.02–20.98 V |
| 2200 uF | 219–282 mA | 12.6% | 20.28–20.73 V |

These percentages describe modeled electrical current modulation only. They are not percent light flicker, PstLM, SVM, visibility judgments or safety thresholds. Actual light output versus current/temperature and a real controller waveform must be established before a photometric conclusion. The result is sufficient to reject the earlier inference that a low voltage-ripple number alone supports steady light.

Across the 96 sensitivities, the 470 uF electrical-modulation range is approximately 45.2–50.6%; 1000 uF gives 23.7–27.2%; 2200 uF gives 11.1–12.8%. Twelve 220 uF cases at the upper mean-current comparison exceed the stated 480 mA DC maximum during each cycle (roughly 488–499 mA peaks). No repetitive-pulse allowance or thermal qualification has been established; those cases cannot qualify a proposed panel. No case falls below the 55 mA binning reference. That reference is not asserted to be a manufacturer minimum operating current. The 480 mA DC maximum is thermally conditional and must not be treated as an approved repetitive pulse rating.

The modeled full sweep spans about 17.93–26.10 V, but that includes the unsuitable over-DC-limit cases and is not an actual normal/fault electrical envelope. Do not use it to close the prior coupled-interface/protection finding or select voltage ratings. This study improves the LED/storage coupling only; actual controller, bias/OVP and transients remain uncoupled.

## How much buffering might be needed

A separate linear small-signal calculation near 250 mA gives a power-ripple to relative-current-ripple gain of approximately 0.501 for the 7-LED/470 uF(-20%) case. An illustrative 5% current-amplitude goal would therefore require residual 100 Hz power-ripple amplitude near 10% of average power, rather than the 100% amplitude assumed in the unbuffered sinusoidal-power model. With 1000 uF the gain is approximately 0.268 and that example permits about 18.7% residual power ripple.

Five percent is an example used to quantify buffering, not an owner-approved requirement or a flicker-compliance limit. This local linear calculation does not validate large-signal behavior, a real input capacitor, or the replacement architecture. Buffering on the primary side, a different control strategy or an additional active energy-buffer stage may reduce residual power ripple; none is modeled as a completed circuit here. Prioritize the primary energy-storage option because it can preserve the simple panel and avoid adding a new active panel stage. Input inrush, power factor/harmonics, EMI, isolation, discharge and device heat must be assessed for that option.

## Physical size evidence, not a selected capacitor

As a concrete size reference, Panasonic EEUFR1H102 is a 1000 uF/50 V radial capacitor with a 16 mm diameter and 25 mm body length on the manufacturer's product page. This does not prove it fits the base, is the smallest available part, is needed at 50 V, or is available through JLCPCB. The listed high-frequency impedance/ripple rating cannot be copied as a 100 Hz ESR or lifetime result. No capacitor voltage rating, footprint or BOM item is selected.

The earlier illustrative passive-discharge calculations remain separate; they are not user wait times. A larger output capacitor requires a fresh residual-energy/fault/cooling assessment. Primary-side buffering also stores hazardous energy and does not waive the enclosed base, insulation or discharge requirements.

## Verification performed and limits

`python calculate.py --verify-halved-step > results.json` ran successfully using NumPy 2.3.5 and SciPy 1.17.0. The solver uses a 20 us step, 24 ripple periods per calibration iteration, and repeats the full calculation at 10 us for convergence. It converged in six average-current calibration iterations; maximum relative mean-current error was 3.19e-7. Largest half-step difference was below 3.85 uA in current extrema, 30 uV in voltage extrema and 0.00068 percentage points in electrical modulation. Periodic capacitor energy and integrated energy balance were checked; residual magnitude is about 1.1e-15 J. This establishes numerical consistency of the declared equations, not physical accuracy.

The code checks diode-law/inverse consistency at three currents. Download hashes and parameter matching can be independently checked against the local reference text. No ngspice executable was available; no SPICE run, actual IC model, photometric metric, CAD/ERC/DRC, installed-toolkit check, supplier confirmation, order or physical test is claimed.

Four independent agent review scopes and final hashes are recorded separately in `review.md`. Requirement impacts: R-LIGHT/R-CCT actual optics remain open; R-COMPAT keeps the common base; R-SIZE/R-BASE-LIFE must include storage size/temperature; R-OFFLINE/R-FAULT/R-EMPTY still require separate fault/access analysis. No new requirement is accepted by this report.

## Next bounded work

Compare a primary-buffered isolated CC implementation with the sinusoidal-power path using common input, optical and interface assumptions. Select a proposed quantitative flicker acceptance/test basis, establish real LED current/temperature/flux data and complete controller-specific protection/startup/storage sizing before schematic approval. Toolkit installation and the complete specification gate remain independent requirements. Do not require an outside engineer before calculations or imply that the agent reviews replace eventual laboratory validation.

Sources accessed 2026-11-16:
- Cree electrical model: https://downloads.cree-led.com/files/da/j/J2835/JSeries-SPICE-JB2835BWT-G.txt
- Cree CLJ-DS40 rev10B: https://downloads.cree-led.com/files/ds/j/JSeries-2835-3V-Consolidated.pdf (G-class table/curves; earlier optical assumptions are not requalified).
- Manufacturer model link provenance: https://www.cree-led.com/products/leds/j-series/2835/
- Capacitor size reference: https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1H102
