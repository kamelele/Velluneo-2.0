# ELEC-REFINE-02 — same-waveform bulk-capacitor RMS evidence

2026-11-17, implementer only; base supplied by coordinator: ECO-01capture commit `36ad2f243d36d592228304b26c27188da0d46c4d`. Read device AGENTS and pinned implementer role. All writes only `tmp/refine-cap/`; no shared source, CAD, component value, graph, approval or whole-major status changed. Native publications are referenced by source identity, not redistributed.

**Result: the old approximately0.2006A triangle screen does not establish that15uF is inadequate. A source-pinned same-waveform conditional switched model gives0.127135A maximum bulk RMS, below the0.152A all-band comparison. Keep the existing15uF candidate for continued engineering; this study supplies no reason by itself to change to22uF. Actual capacitor ripple/lifetime acceptance remains open because clamp-return and parasitic/bridge dynamics are not bounded.**

## Correct mathematics, without invented independence

Let `b(t)` be nonnegative bridge charge current, `d(t)` all nonnegative bulk draw, and `r(t)` nonnegative clamp return into the bulk node. Pointwise KCL is `ic=b+r−d`; no assumption that these are uncorrelated or in separate frequency bands is permitted.

For no return, the exact identity is:

`Ic_rms² = Ib_rms² + Id_rms² − 2 mean(b*d) ≤ Ib_rms² + Id_rms²`.

The omitted cross term is nonnegative. This root-sum-square upper bound is therefore valid **because of current signs**, not stochastic independence. A sum of unrelated LF/HF current maxima from different operating models is not automatically a bound on this same circuit.

Including return:

`Ic_rms² ≤ (Ib_rms + Ir_rms)² + Id_rms²`.

This follows by dropping the two negative draw crosses and applying Cauchy only to the positive bridge/return cross. It still requires the Ib/Id bounds to hold on the actual waveform **after return changes the bulk voltage and bridge conduction**. Do not merely append a return budget to an unchanged baseline and call it a physical pass. For an otherwise unclassified signed current `u`, use the safe triangle `||ic+u||≤||ic||+||u||` on a defined unchanged baseline; no orthogonality is presumed.

For complete linear triangular pulses0→Ipk→instantoff, `mean(ip²)=(2/3)Ipk*mean(ip)`. If all input power of that draw is bounded byP and Vbulk≥Vmin, `mean(ip)≤P/Vmin`. Explicit bulk bleeder draw adds at mostVmax/Rbleed to RMS by triangle. The complete-pulse relation is exact for full pulses/long-time moments; a finite nonsynchronous observation needs its end-pulse correction. The directly integrated switched results below do not rely on neglecting that correction.

Using the **old averaged-source** 11W branch envelope, not claiming it is a new physical-switched bound: IbRMS≤.0992271A, Vmin255.7347V,Vmax352.3295V,Ipk.358522A,Rbleed499000×.979Ω yields conditional primaryRMS≤.101394A, draw≤.102116A, and **Ic≤.142385A** instead ofIb+Id≈.201343A. `bounds.py` reproduces the dependency. This is a mathematical improvement to a conditional envelope, not a silent substitution of averaged bridge current for actual HF bridge current.

That conditional envelope allows **13.362mA RMS positive return** before reaching.152A, only if all other bounds still hold. A further **unverified illustration**, not a leakage specification: if positive returned power≤1%×11W, returnpeak≤.358522A, Vbulk≥255.7347V, then shape-independent `Ir_rms²≤Ir_peak*Ir_mean≤Ir_peak*Preturn/Vmin` givesIr≤12.418mA and Ic≤.151302A. This narrow margin demonstrates why assumed1% leakage cannot close the capacitor finding. Actual leakage, return peak/power, bridge HF and auxiliary/startup demand require their own evidence.

## Actual switched finite-R model

`model.cpp`, compiled with `g++ -O3 -std=c++17`, solves the bulk voltage ODE with RK4:

`Ib=max(0,(sqrt(2)*Vac*abs(sin(2πfline*t))−Vbridge−Vbulk)/Rseries)`

`C*dVbulk/dt=Ib−Ipulse−Vbulk/(499000×.979)`.

At each switching-cycle start, `ton=Lp*Ipk/Vstart`; the imposed primary pulse rises linearly0→.358522A then switches off. Frequency is **computed from the same energy target**, `fs=2*11W/(Lp*Ipk²)`, not selected independently from unrelated maxima. Thusfs67.533–82.540kHz forLp±10%. This is an explicit energy-scheduled load diagnostic, **not a native UCC28711 control/startup/fault model**. The ODE includes fixed rectifier drop and finite series resistance; no ESR, input inductance, device capacitance or clamp return.

Pulseon/off events, measurement boundaries and uniform sample boundaries are split exactly before each RK4 integration segment. This avoids crude pulse-edge timestep aliasing. Solve20rectified-line periods, observe the final4; a pulse-energy observation is not asserted to be switching-synchronous or exactly periodic. The energy schedule target is11W **remaining bulk/primary draw**, plus explicit bleed and input losses, matching the old1152-case semantics. It is not wall input11W. The finite observation primary mean reaches11.001878W; do not relabel that numerical record as exactly11.000W or infer an actual controller limit. If the intended11W constraint is wall input, this is a somewhat heavier-load diagnostic, not an exact wall11W witness.

64 endpoint cases: Vac207/253V; fline49/51Hz; C12/18uF (15uF±20%); seriesR44.65/59.35Ω; bridge drop1.6/2.2V; Lp2.0736/2.5344mH. These endpoints and an imposed fixedpeak are a bounded diagnostic grid, not a proof over the continuous envelope or the actual controller's correlated peak/frequency/power corners. Source+RIN resistance is lumped, just as in the earlier screen. Net11W energy target deliberately covers the remaining converter draw in this model; a separate arbitrary auxiliary load is not added on top to double-count energy. Real direct HV startup draw and its timing remain excluded.

## Numerical results and checks

| Quantity | Result |
|---|---:|
| Maximum actual same-waveform IcRMS | **.1271347701A** |
| Maximum IbRMS across grid | .0992242678A |
| Maximum IdrawRMS across grid | .0989709689A |
| Valid RSS of these separate model maxima | .1401453104A |
| Worst actualIc / .152A comparison | .836413 |
| Nominal unchanged-baseline signed-current RMS budget | .0248652A |
| Positive-return KCL budget if Ib/Id bounds still hold | .0161393A |
| Lowest modeled bus | 255.715836V |

WorstIc case:207Vac,51Hz,C18uF,R44.65Ω,Vbridge2.2V,Lp2.0736mH,fs82.540306kHz; bus265.626–283.449V, primaryRMS.0978409A. Its exact bridge/draw cross moment is.00165019457A², reducingIc² by.00330038915A². Direct calculation accounts for that cross; it is not an independence assumption.

200→100ns maximum differences: IcRMS1.872e−10A,IbRMS1.407e−10A,IdrawRMS7.984e−12A,Vmin1.232e−7V,Vmax6.321e−5V. Squared-KCL identity residual across all64cases≤7.803e−15A². The finite observation capacitor mean-energy drift can reach.002213W; this is preserved rather than asserted to be a perfectly periodic steady state. The code asserts the RMS identity/nonnegative cross and numerical refinement limits. Time-step convergence validates this imposed model's numerics, not real IC behavior.

## Spectrum of the actual modeled capacitor current

Saved worst-case `wave.csv`:392157uniform100ns samples over39.2157ms, with actual modeledIb,Ip,bleed,Ic,V. FFT uses proper one-sided normalization including the odd-length last bin. FFT Parseval RMS and sample RMS agree numerically; slight difference from RK4 integratedRMS (~1.23uA) is sample/quadrature resolution, not physical uncertainty.

| Band | Modeled Ic RMS |
|---|---:|
| <50Hz, including finite-windowDC | .00000717A |
| 50–120Hz | .0551411A |
| 120–500Hz | .0684636A |
| 500Hz–1kHz | .0204766A |
| 1–10kHz | .00704823A |
| 10–100kHz | .0536208A |
| ≥100kHz | .0713510A |

Band energies add by Parseval; band RMS amplitudes must not be linearly added as though independent worst cases. The finite-window spectrum contains leakage from nonsynchronous switching and is not a standards EMC measurement. It supplies actual conditional waveform evidence rather than an invented manufacturer spectrum-combination prescription.

## Native rating decision and limits

Native Rubycon `input-stage/source/bulk-bxw.pdf`, SHA256 `9fb3a22e969e8244e135b7204aa46baa7b8a99d68803a6408fca20c3d8fd5fa6`, p4 exact450V/15uF/10×20row: **.190Arms at120Hz/105°C**, .475A at100kHz. Nativep1 coefficient table10–82uF:50/60Hz.80,120Hz1.00,500Hz1.30,1kHz1.50,10kHz2.10,100kHz≥2.50. Therefore.152A is the familiar deliberately severe all-band50Hz **comparison**, not a substitute for the manufacturer's actual composite-spectrum/temperature/lifetime acceptance. No interpolation or quadratic mixed-frequency acceptance formula is invented from this table.

The conditional actual waveform is below even that severe comparison. **Recommendation: retain450BXW15MEFR10X20 as the prototype candidate; withdraw the claim that the loose.2006A triangle alone mandates replacement. Keep RC-COMP-002 and actual full-ripple/lifetime acceptance open.** No part value, procurement choice, rated operating temperature or release decision is changed here.

Remaining concrete acceptance inputs: clampreturn waveform/power/peak or justified bound; actual UCC-correlated input demand including direct HV current; actualbridge HF/source impedance/ESR/parasitic currents; manufacturer-accepted frequency/temperature calculation and mounting/thermal conditions. Those are owned by the coordinator/later circuit model and physical validation; no reviewer, measurement, manufacturer confirmation or full-major closure is fabricated.

## Reproduce / source record

From the workspace root: `python tmp/refine-cap/calculate.py` builds the local C++ diagnostic and runs200ns/100ns sweeps plus a worst-case waveform capture; then `python tmp/refine-cap/bounds.py`. Outputs are `results.json`, `bounds-results.json`, `wave.csv`. No vendor source originals are copied.

Existing averaged-input result SHA256 `a2ba3a610228251b3f825fcdc7375e99e5e4d74a252ca3ee515775a112bf9816`; original source-engine SHA256 `432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea`. The model's peak/current/Lp inputs are coordinator-supplied conditional witnesses, not a new source-backed whole-controller guarantee. All script/result/input hashes are preserved in `handoff-hashes.json`.


Integration note: This is the preserved original implementation narrative. Current integrated reproduction paths and provenance are in `README.md` and `sources.json`; original temporary paths identify historical evidence only. The integrated `calculate.py` accepts an explicit external SHA256-pinned Rubycon PDF, builds its executable outside the repository, and resolves outputs relative to its own directory. The integrated `bounds.py` resolves the historical averaged data from the verified project root. No native vendor files or compiled executable are redistributed.
