# Primary energy-buffer proposal and mains-current screen

VEL-PRIMARY-BUFFER-01 r1, 2026-11-16. Preliminary specification investigation against product packet r11 and architecture A. Sole writer/coordinator: /root. Proposed location: `driver-study/primary-buffer/`. No capacitor, series resistor, controller or safe wait time is released for hardware. Read the separate `acceptance-proposal.md` for proposed optical criteria.

## Recommendation

Use 10 uF/450 V as the next primary-buffer analysis candidate, with Panasonic EEUEE2W100 as a concrete size/rating reference. Retain the enclosed, isolated constant-current base and simple panel. This narrows the storage direction; it does not select a complete controller or qualify the part.

A larger capacitor is not automatically better. The 10 uF grid retains approximately 250 V minimum on the modeled DC bus, comfortably above the earlier 200 V comparison floor, while larger values increase stored energy and worsen the modeled total power factor. The 200 V floor itself is an engineering comparison point, not the verified controller dropout limit. Even 4.7 uF stays above that floor in this ideal grid; selecting it solely from voltage would ignore capacitor current, lifetime, real ESR, availability and regulation margins.

The main outstanding decisions are now bounded: actual controller/protection behavior with a buffered bus, capacitor ripple/thermal acceptance and mains-harmonic applicability. Do not restart a broad topology survey from this calculation. No PFC stage is added or ruled out before the actual harmonics/test basis is assessed.

## Reproducible model

`python calculate.py --verify-halved-step > results.json` uses NumPy and evaluates 216 combinations:

- 207/230/253 V RMS at 50 Hz: proposed supply screening, not a newly approved range.
- 4.7/6.8/10/15 uF, capacitance factors 0.8/1.2.
- Remaining constant DC-bus load 6/8/10 W. This is a sensitivity budget, not predicted lamp power or an efficiency result.
- Lumped input resistance 10/22/47 ohm; bridge drop fixed at 1.6 V.
- Separate illustrative 1 Mohm bleeder and 680 kohm startup feed to assumed 18.3 V VCC.

The load budget is defined excluding those two additional feeds. Actual converter/bias energy sharing is not solved. The model integrates capacitor energy with finite bridge charging current and constant-power discharge. It starts near charged operation, settles for 20 rectified half-cycles and measures the last half-cycle. It is not startup/UVLO or a cold-plug simulation. The lumped resistance is a mathematical source-path parameter, not a released fusible resistor or a replacement for capacitor ESR.

The converter is treated as an ideal constant bus-power consumer. Therefore these results do not demonstrate LED current regulation, flicker or a real controller's operation across the changing bus. Input inductance/EMI filter, source waveform distortion, capacitor ESR/leakage, switching current, bridge dynamics, tolerances beyond the sample grid, temperature and surges are excluded.

## Grid results

Extrema below are among sampled cases, not guaranteed continuous bounds:

| Nominal bulk capacitor | Lowest DC bus voltage | Highest modeled low-frequency capacitor RMS current | Total power-factor range | Lowest fundamental displacement factor |
|---|---:|---:|---:|---:|
| 4.7 uF | 210.6 V | 84.3 mA | 0.451–0.602 | 0.897 |
| 6.8 uF | 234.0 V | 90.9 mA | 0.424–0.587 | 0.929 |
| 10 uF | 250.3 V | 97.5 mA | 0.403–0.575 | 0.954 |
| 15 uF | 261.1 V | 103.0 mA | 0.389–0.568 | 0.972 |

Representative 10 uF(-20%), 22 ohm, 10 W remaining-bus-load cases:

| Mains | Bus minimum/maximum | Calculated AC input | Total PF | Fundamental displacement factor |
|---|---:|---:|---:|---:|
| 207 V | 251.9–289.9 V | 10.433 W | 0.532 | 0.961 |
| 230 V | 287.9–322.5 V | 10.450 W | 0.513 | 0.969 |
| 253 V | 323.2–355.0 V | 10.479 W | 0.495 | 0.974 |

The 10 uF grid's total modeled input spans 6.264–10.621 W. Thus the actual measured input may cross the 10 W regulatory band even if a separate internal budget is called 10 W. The model distinguishes total PF from the phase displacement of its fundamental current. The fundamental phase result alone does not qualify harmonic emission: current THD in this grid is approximately 136–224%. No harmonic standard limit or market-compliance pass is applied here.

The script analytically relates PF to fundamental distortion/displacement and numerically integrates mains power and losses. Bridge charging current is pulsed; nominal capacitance alone says nothing about acceptable harmonics. Applicable lighting harmonic limits, exact test edition and laboratory method remain open.

## Concrete capacitor reference and remaining thermal evidence

Panasonic EEUEE2W100 (without the S/U size suffix) is listed as 10 uF/450 V, +/-20%, 12.5 mm diameter, 20 mm body length and 5 mm lead pitch. The 2025 EE-A catalogue gives 490 mA at 100 kHz for that size and frequency correction factors; the low-frequency rating must not be replaced by the 490 mA headline.

For a deliberately conservative partial screen, the listed 60 Hz factor 0.25 gives 122.5 mA, compared with 97.5 mA maximum low-frequency model current. This treats the lower-frequency factor as a conservative screen for 100 Hz; it does not establish an exact approved 100 Hz rating or any switching-ripple reserve. The 100 Hz and switching components must be assessed together with actual temperature/ESR and the manufacturer's method.

A diagnostic using tan(delta)=0.24 at 120 Hz/20 C gives apparent ESR = tan(delta)/(2*pi*f*C), about 31.8 ohm at nominal 10 uF or 39.8 ohm at 8 uF. Multiplying by the sampled maximum low-frequency RMS squared gives approximately 0.30–0.38 W as a warning-scale dissipation proxy. It is not measured or predicted hot ESR/loss. The ideal model excludes this ESR, so its electrical/thermal predictions are not a qualified capacitor design. Maximum specified leakage is also excluded. Lifetime inside the base, ripple self-heating and ageing/degraded capacitance need real thermal and source-data assessment.

This part is a size/rating reference, not necessarily the smallest/best choice, a JLCPCB-stock confirmation, a selected footprint or a five-year life guarantee. Other packaging suffixes can change size/ripple data. Exact service, sourcing and assembly remain unconfirmed.

## Inrush, discharge and protection implications

The repeated charging peaks in the steady model are not cold inrush. A separate initial algebraic comparison at a discharged capacitor/high-line crest gives 35.6/16.2/7.58 A through 10/22/47 ohm respectively, before unmodeled source inductance, bridge behavior and surge impedance. These are neither measured nor qualified maximum inrush currents. Fuse/bridge/series-element pulse energy and repeated switching must be designed together; do not select a resistor by steady wattage alone. The 10 uF grid's lumped series-path loss is about 0.035–0.384 W, not all necessarily in one physical component.

At 10 uF+20% and the ideal 253 V peak, stored energy is approximately 0.768 J. A hypothetical 1 Mohm+1% dedicated bleeder gives about 21.64 s from that peak to 60 V and 30.04 s to 30 V. These voltages are numerical examples, not accepted touch limits or a user waiting instruction. Actual discharge includes the real converter/startup states and possible faulted/open bleeder; no such helpful paths are credited as a guaranteed independent discharge function. The covered primary storage is separate from the user-accessible secondary and its own discharge/cooling requirements.

The earlier TPS92310 hard-current-threshold and auxiliary VCC/OVP findings remain open. Buffered input does not close those findings or remove overtemperature, empty-panel, shorted-panel and isolation obligations. No sense resistor, MODE wiring, clamp or protection circuit is selected by this note.

## Checks actually performed

NumPy 2.3.5 was used. Fixed-step RK4 uses 2 us and repeats at 1 us for all 216 cases. Maximum difference: minimum bus voltage below 0.00076 V; total PF below 1.21e-6; capacitor RMS current below 0.21 uA. Periodic energy and integrated input/load/loss balance are checked, as is the relation between PF, fundamental displacement and distortion. This validates declared-equation arithmetic, not a real input circuit or harmonic certification.

Native Panasonic catalogue and EUR-Lex reference PDFs were downloaded and hashed in `sources.json`; original files are reference-only and not redistributed. Source provenance, actual independent review scopes and final hashes are in `review.md`. No controller/SPICE model, CAD/ERC/DRC, installed-toolkit environment pass, physical test, supplier message, reservation or order occurred.

Next: finalize the proposed optical acceptance/test basis with the full review packet, calculate actual controller/protection operation across this bus waveform, and establish capacitor/bridge/pulse/thermal/harmonic feasibility. Human specification approval remains separate from engineering investigation and from eventual laboratory validation.

Primary sources accessed 2026-11-16:
- Panasonic exact part: https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUEE2W100
- Panasonic EE-A, 01-Sep-2025: https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1026.pdf (specification/frequency table and exact 450 V rows visually inspected).
- EUR-Lex consolidated benchmark: https://eur-lex.europa.eu/eli/reg/2019/2020/2021-09-01/eng (classification/legal application not decided by this circuit model).
