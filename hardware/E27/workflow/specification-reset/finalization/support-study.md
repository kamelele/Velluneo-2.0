# Bounded support-component handoff

SUPPORT-CANDIDATE-01,2026-11-17. Implementer/root/support_design. Read-only shared project sources; only tmp/support-design written. This is a concrete pre-schematic candidate for coordinator integration/review, not independent closure, a physical test or a product-stage decision. Baseline functional intent input-stage/circuit-intent.md and source identities are pinned in support-results.json. No architecture A or owner requirement change.

## Final proposal and circuit nodes

| Position | Concrete initial reference | Connection |
|---|---|---|
| RG |4.7ohm0805 VishayCRCW08054R70FKEA | UCC DRV →RG→Q1gate. NativeST switching-test RG4.7 is a source condition, not proof of suitable circuit timing; no copied switching time is adopted. |
| RGS |47k0603 VishayCRCW060347K0FKEA | Q1gate toQ1source/SENSE at the transistor, not to a remote output or isolated ground. |
| RCS |2.37ohm1206 VishayCRCW12062R37FKEA | Q1source/SENSE toPGND. CS via existing1.40k takes a Kelvin sense from RCS high pad; UCC GND uses quiet RCS low-pad reference. High-current/gate paths must not share the analogue sense trace. |
| RAUX |4.7ohm2512 VishayCRCW25124R70FKEG | DAUX cathode→RAUX→VDD/2x470nF. DAUX anode at raw flyback-positive auxiliary winding; winding returnPGND. VS divider continues sensing RAWauxiliary winding before diode/resistor. |
| Output bleed |2x20k2512 VishayCRCW251220K0FKEG in parallel | Each OUT+–OUT− across the base output capacitor. A single open leaves one20k path; a short is an output-short fault requiring the existing protection validation. |

Native Vishay document20035 supplies ordering construction: F±1%,K±100ppm/K and packages/values above. Importantly, K100ppm is available from1ohm through the applicable range; the separate N200ppm low-value option does not force2.37ohm to be200ppm. Exact identifiers are valid manufacturer-ordering-derived candidates and commercial identities were corroborated; no manufacturer lifecycle promise, live stock or JLC assembly qualification follows. Existing native2026 datasheet rates0805P70=.25W,0603=.125W,1206=.25W,2512=1W; calculations deliberately allow only.125W for gate0805 and.1W for pull0603 to avoid relying on the newer uprating.

Final RGS47k supersedes earlier scratch220k suggestion: do not raise resistance just to fit an inherited bias budget while ignoring passive off pull. The47k choice increases defined main ancillary allowance from.30 to.55mA, raising main base-draw hypothesis2.95→3.20mA;3.50mA stress retained. No10k/220k is silently fitted as an alternative. Actual Miller immunity remains unproved for every choice.

## Calculated support margins and limits

RG/RGS: at assumed16V drive and47k−2.1%, pull current347.73uA. Adding nativeNTC125uA and a10uA gate-leakage illustration gives482.73uA, leaving67.27uA of the new.55mA ancillary allocation. IGSS native condition is VDS0/VGS±20V; it does NOT guarantee actual high-drain-bias off current or Miller injection. IGSS×RGSmax=.480V is only a static comparison, not turn-on immunity. The existing internal150–230k startup pull reinforces the external pull but no switching waveform is inferred.

If the16nC actual-drive/16V/106kHz hypotheses hold, the entire gate-path per-cycle energy allocated to RG is27.14mW. At125C, conservative.125W P70 gate rating derates to44.12mW; this comparison checks average energy only. Instantaneous pulse/sink current and Miller/drain feedback are not qualified by that number. Source driver20mA minimum applies atVDRV8/VDD9; low-side12ohm maximum at10mA is not a guaranteed high-current sink law. Neither Ciss160pFtyp nor fullQg/IDR can establish turn-off delay. Keep100–150ns total delay/RLC calibration conditional.

RCS: applying±2.1% as an outward initial-plus-temperature screen for1%/100ppm over25→125C refreshes256 constructed CC/DCM endpoints. CC223.41–280.88mA, primary peak304.99–349.10mA, primaryRMS52.57–89.92mA, flux.09246–.12935T, frequency32.836–82.897kHz. RCS average loss≤18.76mW versus1206P70.25W derated88.24mW at125C under source mounting. This is not a pulse/fault/aging guarantee or a real IC trajectory. Resistor aging beyond the source test duration is not bounded.

RLC: with1.40k,80.6k,2.37ohm each±2.1%,Lp±10%,KLC24–28.6, the native compensation equation gives equivalent91.49–151.15ns. If actual total delay were100–150ns, residual peak-current error would be−7.22…+10.10mA. KLC itself is tested at−300uA VS current, not every line condition. These are conditional deltas, not a fresh combined current/flux/fault bound. Update normal and fault/clamp assessments before claiming freeze; don't inherit all old±1% outcomes.

RAUX: normal reflected primary-peak proxy1.904A and assumed averageVDD draw5.196mA yield Rloss≤47.48mW only IF those peak/average bounds apply. The1W2512 derates to352.94mW at125C under its source mounting. Current-sharing, leakage/ringing and actual aux charging spikes remain unknown; the reflected value isn't a measured diode-current bound.

The explicit extra.30V resistor reserve requires actual aux conduction fraction≥.08311 of the cycle for average5.196mA andRmax. This is a useful test/simulation constraint, not an invented conduction window. It raises output takeover target to16.2727V from the previous15.8636V. Don't assume diode conduction spans all secondary demagnetization or that a low-mA forward drop is guaranteed.

Bleeders: 2512parts avoid a tight1206 hot-power margin. Each20k−2.1% dissipates73.21mW at37.861V,81.72mW at40V,202.71mW at63V. Each remains below352.94mW source-derived125C rating at these static examples; this does not establish output overshoot/short/fuse protection. At maximum20.592uF sensitivity,40→5V decay is.4372s with both parts or.8744s after one-open; at63V,.5327/1.0654s. These times begin only AFTER all energy transfer to output stops. The15uF primary reservoir can continue switching/replenishing output after unscrewing; removed-panel storage, primary discharge and cooling need separate treatment.5V is merely a calculation endpoint, not an approved accessible-energy limit or user wait time.

## Refreshed conditional startup

The unchanged source-pinned staticLED/ESR integration method was rerun with RCS/bleed temperature allowance, the new.30V aux-resistor reserve, main base3.20mA and stress3.50mA.128cases remain.

| Result | Value and interpretation |
|---|---|
| Output takeover target |16.2727V, assumes1Vauxdiode/.5Vwinding/.5Vripple/.3VRAUX and10VVDDtrough |
| Worst permissible first-three all-RUN time, main12nC/3.20mA |.68924ms under the constructed charge model |
| Worst across16nC/3.50mA stress |.42935ms |
| If firstthree=.300ms plus separate.100ms settling | Worst takeoverVDD10.5085V |

This narrows the previously published.498ms stress acquisition allowance and demonstrates why filling auxiliary/gate positions must refresh the charge budget. No source supplies a first-three timing/RUN-WAIT residency/current envelope across declining9–23V;RC-BIAS-001 stays major/open. No native controller transient, real gate waveforms or measurements occurred.

## CAD and acceptance implications

The six newly populated support positions now have concrete initial values and nonpolar resistor footprints. They can be represented in a DRAFT review schematic once the project's actual specification/tooling/intent prerequisites permit CAD. Missing physical waveforms should remain explicit research/bring-up acceptance items; drawing the circuit cannot close them. This task itself grants no stage advance or CAD acceptance. Root remains the shared CAD writer and must respect repository gates, not silently label a draft qualified.

For STN1NK80Z, native first-page graphic confirms G1,D2,S3,D4(tab). A physical footprint/symbol contract must represent the tab's drain equivalence correctly; the model's D/G/S port order is different. Do not mark the tabNC or map an arbitrary genericSOIC footprint. UCC pin numbering comes from the current7pin native datasheet, not olderEVMHV8 labels. Resistor pad numbers are library convention, nonpolar; verify body/courtyard/power-pad layout against the native dimensions and actual KiCad library before placement.

ExistingRC-BIAS-001/RC-COMP-002/model/sampling/fault/service/thermal/process findings remain open. Remaining prerequisites include controller/gate actual behavior or defensible evidence, integrated clamp/short/open recovery and surge, finished insulatedtransformer specification/pinout, input EMI/filter/process, accessible output/service criteria and physical layout/fit. These support calculations supply none of those absent passes. No outside reviewer or measurement is invented.

## Reproduce and integrate

From this finalization directory:

```sh
python support-calculate.py --driver-study ../driver-study --crcw-pdf /reference/dcrcwe3.pdf --ucc-pdf /reference/ucc2871x.pdf > /path/isolated-support-results.json
```

Source hashes are asserted. Coordinator integration is now complete for this candidate: explicit canonical prior-result paths and separate native-PDF arguments replaced the implementer's scratch-folder dependency lookup, and the adapted script was rerun. The command is a numerical study run, not an installed-toolkit CAD check or physical measurement. The original implementer wrote only isolated scratch files; root owns these final repository files. Final files are support-calculate.py,support-results.json,support-parts.csv,sources.json and this integrated study. No vendor PDF is redistributed. Affected older comparisons remain stale until refreshed; no old result silently covers the modifiedRCS/current scenario.

## Coordinator-requested correlated normal-current update

Applied line-compensation residual to the SAME normal case, rather than summing independent maxima:

`Ip = VCST/RCS + Vbus*(tdelay/Lp - RLC/(KLC*RS1*RCS*Npa))`.

4096correlated samples include RCS/RS1/RLC±2.1%,Lp±10%,KLC24–28.6 and assumed100–150ns delay. Reconstructed frequency uses a fixedDdemag=VCCR/VCST hypothesis, not a verified native control law. Maximum correctedIp=.358522A; maximum flux=.131098T occurs at a DIFFERENT correlated corner, not atIp maximum. RMSprimary≤.091545A,RCS average heat≤.019445W;16ohm/25C conduction proxy≤.134089W. Corrected constructedCC range=.218763–.289194A, secondary initial peak≤1.43409A and secondaryRMS upperproxy≤.538790A. Actual line regulation or magnetics protection is not established.

MaxIp case:Vbus357.796V,Lp2.0736mH,RCS2.32023ohm,RS182.2926k,RLC1370.6ohm,KLC28.6,delay150ns,VCST.810V. Its residual is+.00941845A and flux.108689T. Maxflux uses Lp2.5344mH andIp.353816A; the same highline/lowRCS/highRS1/lowRLC/KLC/delay corners give.131098T. Exact cases are retained in support-results.json.

The all-primary-current-toaux peak proxy becomes1.95557A; conditionalRAUX peak×mean heat proxy48.76mW. These remain a constructed current-sharing bound, not actual diode-current measurements.

For completeness,40960normal-only direct-clamp sensitivities were updated from these correlated currents with the inherited1%leakage,175.1164–286.972V plateau proxies and.7/1.7V blocking-diode drops. MaximumTVS averageproxy=.238555W,pulseenergy4.40832uJ,peakpower102.886W,normal resetproxy142.30ns. The +50V commutation-assumed drain endpoint remains696.468V because the imposed plateau is current-independent. This unchanged endpoint is NOT evidence that the actual clamp voltage is unaffected by current. The inherited VBR-temperature-coefficient scaling is still not a guaranteed hot avalancheI–V curve; no fault/surge/stop-latency orRC-COMP-002 closure follows. Physical hot/repetitive behavior remains unresolved.

The priorinput-stage.0889A HF witness is now stale for this modified constructed current scenario: the newnormal value is.09155A. A regenerated mixed-band comparison may use it as a sensitivity, but it still cannot couple independent10Wbus-load/current spectra into a whole-converter rating bound. No unmodified historical report is silently made current by this handoff.
