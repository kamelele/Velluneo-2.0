# Buffered TPS92310 protection and bootstrap proposal

VEL-PROTECTION-01 r1, 2026-11-16. Specification investigation against packet r11 (Git blob 6493b29bd33fbde1f3c61c5e995b11447cb83e9b). Architecture A is unchanged. The controller remains a conditional reference path, not selected hardware or a ready schematic. This document and `fault-contract.md` provide one coherent diagnostic parameter set and identify the remaining acceptance blockers.

## Decision and stop condition

Retain the physically isolated, primary-side-sensed TPS92310 COT reference path with its lower current-limit configuration for the next bounded design proposal. Do not freeze the circuit yet: auxiliary VCC needs a justified limiting/guard strategy and bootstrap must be checked with actual current draw and control timing. The simple unguarded auxiliary path has under 1 V margin in important screens; the calculation must not be presented as a completed protective design.

The input-buffer direction remains 10 uF/450 V. A much smaller secondary capacitor becomes a reasonable analysis candidate once 100 Hz energy storage moves to the primary, but actual current ripple, component RMS/ESR and light metrics still need verification. No implication that any capacitor value guarantees steady light.

## Native-source clarification

TI SLVA511 pages 8–10 and its complete Figure 13 were re-inspected as readable native-PDF renders. The 0.64 V configuration is used with a physically isolated transformer even though the controller mode table labels that setting non-isolated. Its ZCD filtering/clamp network must be designed. The reference does not establish a separate active SCP detector as mandatory; its optional line compensation and rapid gate-discharge network must not be conflated with one.

The earlier `control-and-alternative.md` wording is narrowed in revision 2. This corrects an implication about extra circuitry, not an electrical result. Reference power/transformer/filter values are not copied as a qualified Velluneo circuit. Native TI source hashes are in `sources.json`.

## Diagnostic set, not a released BOM or pin graph

| Function | Analysis candidate | Meaning / remaining evidence |
|---|---|---|
| Input storage | 10 uF/450 V | Previous buffer direction retained; real ESR/ripple/heat/inrush/harmonics remain open. |
| Transformer | Lp 4.0 mH +/-10%, 200:50:48 primary:secondary:auxiliary | New auxiliary count is a calculation input, not a manufactured winding schedule. Isolation, fit and hot magnetics unverified. |
| Current setting | 2.21 ohm +/-1% comparison | About 253.4 mA ideal total secondary current; LED current is lower by bleeder/other loads. No total-regulation accuracy guarantee. |
| ZCD/OVP divider | 100 kohm / 16.2 kohm +/-1% | Raw auxiliary plateau is sensed; filtering, negative clamp/injection and actual waveform remain unqualified. |
| Output storage | 22 uF, +/-20%; investigate 50 V class | Smaller than earlier output-energy-buffer examples. RMS/ESR/ripple and source/footprint not selected. |
| Output bleed | 10 kohm comparison | Does not by itself establish safe service delay or a fault-proof discharge path. |
| VCC storage | 22 uF +/-20% comparison | Bootstrap reserve increases, but startup charging is slower; neither outcome is owner-approved performance. |
| Startup resistance | 474 kohm total, e.g. two 237 kohm values | Replaces 680 kohm in this diagnostic set. Voltage/pulse/thermal/part selection is still open. |
| VCC guard | Evaluate a precision low-Iq shunt such as ATL431B Q-temperature family | Functional mitigation proposal only. No orderable part, cathode-current limit or compensation is selected. |
| Whole-lamp thermal protection | Investigate a self-resetting normally-closed thermal protector at a justified hot location | Candidate simple independent shutdown function; exact temperature, AC rating, placement, life and assembly remain open. IC thermal shutdown alone is insufficient evidence for the lamp. |

The 18–27 V, 250 mA-class values remain provisional. The earlier 240–270 mA factory-development exploration is not a user operating range, and changing the final current requires fresh optical and protection checks. No Wi-Fi, firmware, secondary panel-control board or user calibration is added.

## Normal current and lower current-limit comparison

With a 240–357.796 V bus investigation screen, 96 ideal CrM sampled combinations give primary peaks up to 0.215 A, sense voltage up to 0.471 V, frequency 63.4–125.8 kHz and flux swing up to 0.149 T. The 240 V floor deliberately reserves some space below the refreshed ideal bus result; it is not a proven real drop allowance.

Separately, TI's simplified application-note formula with analyst efficiency sensitivities 0.75/0.8/0.9 gives sense voltage up to 0.535 V, about 55 mV below the listed lower 0.59 V comparator value. This does not model actual losses/control, noise, propagation or full-temperature tolerance. Do not combine the two screens into a certified normal-current margin.

For the listed 0.59–0.68 V comparator range and the comparison resistor, nominal trip current spans 0.264–0.311 A. Adding 210 ns typical propagation at its stated test condition plus 0/100 ns assumed extra turn-off gives sampled peaks up to 0.342 A, linear flux proxy up to 0.238 T and pulse energy up to 0.248 mJ. The delay is not a guaranteed maximum at the lower threshold. Blanking/minimum pulse, real gate behavior, sensing and saturation invalidate any claim of a hard current bound from this algebra.

A shorted output can demagnetize very slowly: with the assumed diode drop, a diagnostic discharge time reaches about 739 us versus a 94 us low-frequency off-time comparison. Normal CrM reset therefore cannot be assumed during a short. Actual incomplete-reset/CCM burst behavior, UVLO restart, winding/diode heating and absence of fuse operation require controller-specific and physical verification. The manufacturer reference behavior is evidence of a possible strategy, not our fault-survival result.

## Open-panel OVP and auxiliary interaction

Divider/reference/diode/auxiliary-loss/bias sensitivities give a static output trip interval about 28.81–34.33 V. Normal positive ZCD voltage reaches 3.854 V versus the 4.1 V lower OVP threshold. The 246 mV difference is a sampled comparison, not a ringing/noise allowance or 10% guaranteed headroom. Static short-output ZCD values stay below the trigger comparison, but ringing and diode behavior are unmodeled.

As an energy illustration only, four additional hard-limit pulse-energy proxies into Cout-20% would raise the worst static trip value to about 35.94 V. Four is an assumed count including an in-flight allowance, not a verified stop-latency bound. Neither 35.94 V nor the illustrative 40 V working ceiling is an accepted accessible-contact limit. Filter delay, continuing conversion, parasitics and independent component faults are not bounded.

The same auxiliary winding powers VCC. Its normal sensitivity is about 16.26–26.57 V, leaving only 0.56 V over the largest listed turn-off threshold. Under the illustrative open-energy peak, VCC can reach about 35.15 V, only 0.85 V below its 36 V operating ceiling. Thus winding ratio/diode/loss/OVP cannot be chosen independently. The controller's absolute maximum is not a design operating target. The unguarded path is not accepted for freeze.

## VCC guard and bootstrap: real remaining work

A precision shunt guard is a justified mitigation to investigate rather than assuming an arbitrary Zener fixes the problem. A passive nominal Zener may interfere with worst-case startup or leave inadequate operating-voltage margin after tolerance, knee and temperature effects.

For an ATL431B Q-temperature family comparison, a 1.21 Mohm/100 kohm +/-1% divider and conservative combinations of listed reference/drift/cathode-voltage/current sensitivities give a static interval about 30.62–34.22 V. This only suggests room between the 29 V startup comparison and 36 V operating ceiling. It does not prove the interval under actual cathode current or dynamics. The device's minimum-current and reference limits have specific test conditions; capacitor stability above 30 V, leakage, current limiting, transient/average heat and single-fault behavior remain unqualified. In particular, adding a series limiting resistor can consume the already small low-normal VCC headroom. No clamp implementation is released.

The bootstrap scenario uses fixed 1.5 us startup pulses, 50/72/94 us off-time sensitivities, delivery factors 0.5/0.8, assumed 2/3/5 mA VCC draws and 1 W net post-arming charge power. Maximum calculated time to auxiliary takeover is about 22.39 ms; the smallest assumed capacitor hold-up is 25.70 ms, leaving only 3.31 ms. These typical/assumed quantities do not establish real startup. The guard's load/dynamics are not included in that scenario and must be integrated before adoption.

Charging VCC from zero to 29 V through 474 kohm at 240 V with maximum assumed RC and the table startup sink gives about 1.68 s before bus rise, guard loading or real control action. That is not actual switch-on time and is a visible performance trade-off, not an accepted delay. Bootstrap and startup speed must be resolved together before calling this an ordinary-bulb response.

## Updated dependency and residual energy

Because the startup resistor changed, the existing primary-buffer script was verified by SHA-256 and rerun with 474 kohm in an isolated module context; the historical source and results were not edited. The 54 refreshed 10 uF cases give minimum bus about 250.14 V, maximum bus about 355.90 V, input-power range 6.312–10.693 W and low-frequency capacitor RMS up to 97.82 mA. Previous 680 kohm input results remain historical. The previous half-step test belongs to that older input; this overlay was executed at 2 us with energy identities, not falsely reported as a fresh 1 us sweep.

Cout+20% stores about 0.0211 J at the illustrative 40 V. Its passive 40-to-5 V calculation gives about 0.554 s, but the primary buffer can keep conversion or retry behavior alive after mains removal. This is not a user wait time. Direct capacitor discharge into a short is not limited by the primary comparator and depends on ESR/wiring/contact inductance; it needs separate assessment. Thermal cooling can govern service delay as well.

## Evidence and next action

`python calculate.py > results.json` executed. It verifies the exact sibling primary-buffer script dependency, checks ideal-cycle current identities, refreshes bridge/CPL energy checks and performs declared sensitivity arithmetic. No actual control-loop/IC/SPICE, short-circuit dynamics, clamp stability, electrical qualification, CAD/ERC/DRC, installed-toolkit pass or physical test is claimed. Actual independent review scopes and file hashes are in `review.md`.

The next bounded closure is the VCC guard/auxiliary/bootstrap design, followed by the combined specification proposal with optical criteria and open-interface/test/process decisions. Do not open another broad topology survey or treat owner approval of desired behavior as electrical certification. No purchase, supplier communication or physical test was performed.

Sources, native hashes in sources.json:
- TI TPS92310 SNVS792: https://www.ti.com/lit/ds/symlink/tps92310.pdf
- TI SLVA511: https://www.ti.com/lit/an/slva511/slva511.pdf
- TI ATL431 rev E: https://www.ti.com/lit/ds/symlink/atl431.pdf
