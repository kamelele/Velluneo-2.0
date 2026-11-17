# Finite-resistance startup and protection refinement

ELEC-REFINE-02, bounded implementer analysis against the coordinator's ECO-01 capture identified as `36ad2f243d36d592228304b26c27188da0d46c4d`. No CAD, approved graph, component value or configuration was changed. These are conditional calculations and source interpretations, not a TI controller simulation, physical measurement, independent approval or finding closure.

**Retain RAUX = 4.7 Ω by default.** The finite winding-resistance candidate does not itself invalidate the charge-domain startup witness. Removing an unsupported minimum output-diode drop reduces its calculated VDD reserve. A narrow auxiliary charging-window sensitivity exposes a useful design frontier; it does not establish that the real controller has that window.

## Source and input basis

The script verifies the complete hashes of five external native PDFs against [sources.json](sources.json): TI SLUSB86C, SLUAAC5 and SLUA783, plus ST STTH1R02 and STTH2R02. It also verifies the exact repository support, startup and winding-result inputs. Native PDFs and rendered pages are not redistributed here.

Hot winding resistances are read from the saved MLT60 mm / 125 °C construction budget: Rp = 7.225860 Ω, Ra = 1.405578 Ω, Rs = 0.705633 Ω. These are proposed-length/DC copper calculations, not measured hot winding impedances. The active 1 MΩ R13 is included once, using the conservative additional draw 35 V / 979 kΩ = 35.7508 µA.

TI's native Eq. 3 and Eq. 14 explicitly include transformer-delivery efficiency:

`IOCC = VCCR × Nps × ηXFMR / (2 × RCS)`.

Multiplication by ηXFMR is therefore not intrinsically an error. TI defines it to cover core/winding loss, leakage and bias power, not arbitrary whole-converter efficiency. The retained 0.85 charging-current assumption is not re-derived here or guaranteed. Do not subtract the same finite losses again when a later model explicitly accounts for them.

## Auxiliary voltage and charge frontier

The off-phase equations distinguish winding current from diode charging current:

- `VAUX_RAW = (Na/Ns) × (Vo + VFout + Is × Rs) − IA × Ra`
- `VDD = VAUX_RAW − VFaux − IAD × RAUX`

Here IA is total auxiliary winding current; IAD is current through DAUX/RAUX. Their difference includes VS-divider current. The rectangular-window sensitivity approximates IA = IAD and neglects that small divider term. For raw auxiliary voltage no greater than 35 V, its Ra drop is below approximately 0.52 mV with the selected divider. This omission does not establish an actual waveform bound. Positive secondary `Is × Rs` is omitted when screening minimum VDD.

The hot auxiliary series path is 6.204278 Ω, including RAUX at +2.1%. Do not add the old separate 0.5 V winding and 0.3 V RAUX allowances again after calculating their actual drops.

ST specifies no minimum forward drop for the output diode. Replacing the inherited **0.5 V minimum assumption with the passive 0 V screen**, while retaining the old combined 0.8 V path allowance and 0.5 V ripple allocation, raises takeover output from 16.2727 V to **16.7727 V**. With active R13, the inherited worst-case charge witness gives **VDD = 11.224575 V**, compared with 11.493763 V at the old target. This retains source-cadence, gate-charge, all-RUN base draw, settling and constructed CC-ramp assumptions; it is not a finite-loss full-converter transient.

At the upper mean-bias hypothesis of 5.231751 mA, the required charge per 106 kHz cycle is 49.3561 nC. Combining the inherited warm-seven-LED / 20.592 µF charge limit with the hot path gives this **equivalent flat charging-window frontier**:

| Assumed auxiliary diode drop | Minimum equivalent window fraction for the 10 V charge target |
|---|---:|
| 1.0 V | 1.9958% |
| 1.2 V sensitivity | 2.2756% |

Mean current divided by window fraction does not bound real peak current or sampling current. Actual acceptance must check delivered charge, `∫IAD dt ≥ Ibase × T + Qg`, and VDD trough/crest over the complete trajectory.

For illustration, a 2% rectangular window with VFaux = 1 V and VFout minimum = 0 gives:

| RAUX candidate | Required takeover output | Calculated takeover VDD |
|---|---:|---:|
| 4.7 Ω, retained | 17.89495 V | 10.01166 V |
| 2.2 Ω sensitivity only | 16.98445 V | 11.08996 V |
| 1.0 Ω sensitivity only | 16.54740 V | 11.35223 V |

The 4.7 Ω result is a warning hypothesis with almost no reserve, not a validated startup failure or pass. TI SLUA783 p3 describes reducing auxiliary series resistance as a startup remedy. A reduction could improve charging if a narrow window is actually established, but it can increase leakage-energy collection and VDD crest/ringing. No RAUX or RCS ECO is selected or applied. VFaux = 1 V is specified only at the native test conditions; the 1.2 V case is an explicit sensitivity, not a new cold-temperature guarantee.

## Normal, open and short behavior

Finite Rp gives an on-time line-sense example of about 0.525 mA at a 240 V bus and 0.36 A primary current, above the native 275 µA maximum run threshold. This is a static turns-ratio/IR-drop screen, not a sampled-waveform pass. Exact RL on-rise calculations remain below 0.990 µs at minimum-current threshold and 3.851 µs at normal maximum threshold, using 16/32/48 Ω MOSFET sensitivities; those MOSFET values are not guaranteed 125 °C limits.

An open output is normally a CV-regulation case, not automatic continuous OVP/retry. At 30 V the two 20 kΩ bleeders dissipate at least 88.15 mW, exceeding the 8.215 mW ideal minimum-pulse / 755 Hz energy example. This supports an energy-balance operating witness, not actual CV frequency or bias-state stability. The 0.5 V ripple allocation is not a universal open-load VDD ripple bound.

For a hard output short, the finite secondary-resistance illustration gives auxiliary EMF only 1.603 V at the normal CS-threshold current example, or 2.307 V at the 1.6 V backup-threshold example. Both are below VDD at UVLO, so that ideal winding model cannot sustain the bias rail. Expected behavior is loss of auxiliary bias, UVLO and restart, possibly preceded by another detected fault. These threshold-current examples ignore propagation, saturation and commutation and are **not maximum fault currents or stress bounds**.

Native TI fault behavior stops switching, draws IFAULT, discharges VDD to UVLO-off and returns to startup. IFAULT has no specified minimum; do not invent a restart period from its typical or maximum value. Once all bias injection is absent, R13 alone gives calculated upper passive times of 1.5304 s from 35 V to 7.7 V, or 1.1060 s from 23 V to 7.7 V. Those clocks start only when the source-off condition holds. The 2.661 ms run-current short-discharge example and constant-HV-current charge examples in results.json are sensitivities, not guaranteed retry timing. Native IHV endpoint tests do not specify its full charging trajectory.

## OVP and the illustrative 40 V goal

The native OVP threshold limits used here are **25 °C** conditions. With zero output-diode drop, zero secondary sample current and no auxiliary winding IR drop, the static upper threshold is 37.4784 V.

A 1.9556 A auxiliary-current sensitivity produces 41.2266 V in the same algebra. That current was borrowed from a global reflected peak proxy: it is **not an actual auxiliary sample current, not a physically coincident sampling corner and not an OVP bound**. VS samples near secondary-current termination; auxiliary conduction can differ substantially there. The calculation merely shows why a sample-current assumption matters. Approximately 1.3156 A of total auxiliary winding current at that hypothetical sample would consume the static margin to 40 V, under the other stated assumptions.

Neither number bounds dynamic output voltage. Temperature dependence, waveform distortion, ringing and stop latency remain outside this algebra. The existing 40 V value remains an unapproved illustrative goal, not a guaranteed ceiling.

## Reproduce and review

From the repository root, with NumPy/SciPy available:

```bash
python hardware/E27/workflow/specification-reset/electrical-refinement/startup-protection/calculate.py --source-dir /absolute/path/to/native-pdfs
```

The external directory must contain `ucc2871x.pdf`, `sluaac5.pdf`, `slua783.pdf`, `stth1r02.pdf` and `stth2r02.pdf`. Optional `--ucc-pdf` and `--diode-source-dir` accept separately stored originals. Outputs are written beside the script. Changed source or repository hashes cause refusal.

`results.json` preserves all 48 takeover/diode/window sensitivities and the other numerical screens. `calculate.log` is the actual integration rerun. `integration-check.json` records comparison with the original diagnostic; `artifact-hashes.json` binds this packet. No new physical measurements, controller execution, graph/CAD changes, independent review or finding self-closure occurred.
