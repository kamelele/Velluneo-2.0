# E22 comparative power and temperature screen

Same accounting method as POWER20, changed four-position ECO. Baseline replay
reproduces input8.585985349W andheat2.045713631W exactly.
Current electrical source is ../design/Velluneo_driver.kicad_pcb andselectedBOM.
These are unmeasured conditional estimates, not guaranteed efficiency or temps.

| Central230Vac50Hz | C16 / POWER20 | E22 |
|---|---:|---:|
| InputW | 8.585985 | 8.538387 |
| LEDpowerW | 6.540272 | 6.538948 |
| DriverheatW | 2.045714 | 1.999439 |
| EfficiencytoLED% | 76.1738 | 76.5829 |
| LEDcurrentmA | 316.9364 | 316.8790 |
| D3heatW | 0.241060 | 0.201684 |

Central gain is0.409percentagepoints and
46.27mW less driverheat, not a multi-watt cooling fix.
97paired selected cases include **worse** hot-leak cases: maximum driverheat delta
34.23mW. No all-corners gain is
claimed. Actual choice needs source-matched same-temperature waveform/thermalA-B
testing; do not accept the Schottky solely on its low advertised forwarddrop.

## Changes to the accounting model

Retain source-conditioned etaXFMR=.90 and .85/.93 sensitivities, with magnetic,
clamp and netbias counted INSIDE that allowance, not twice. Rstart=844k and
R13=84.5k; oldmodel804k/80.6k is executed by revision='old'. SourceD3forward
formula changes .68If+.06IfRMS² to .58If+.03IfRMS². These are old150C vsnew125C
hot reference envelopes, not a measured common-temperature curve comparison.
IRassumptions5/100/2500uA cover selected scenarios;2.5mA is the125C200Vmax test,
not a guaranteed bound through175C. Published leakage/Cj curves are typical.

IR reverse duty=(1-Ddemag), so netoutputIf-IR*(1-Ddemag), LEDcurrent additionally
subtracts10kbleeder. This prevents counting reverse charge twice. With an ideal
primary rampDpri=fLPIP/Vbus, average reverse heat is
IR*[Vo*(1-Ddemag)+fLPIP/4]. First-order reverse exposure ignores ringing and
uses Vo during idle. Solve f=(VoIf+Pforward+Pbackground+PC4)/
(eta*.5LPIP²-IRLPIP/4), preserving effective forward charge and aggregate energy.
The same old background reverse/dynamic sensitivity remains; it is not removed
to manufacture a gain. New extra switchingenergy0/.10/.30uJ per event is a
selected incrementalCj sensitivity added to Q1, not a published maximum. It is
not also added toD3. Actual capacitance/recovery/valley behavior remain unmeasured.

C4RMS²=IforwardRMS²+IR²*(1-Ddemag)-Inetoutput². VDDuses sourcehotforward
equivalent for newD3; old.75Vassumption retained only in baseline. Numerical
ledger/charge residuals and timestep checks are numerical checks, not waveform
validation. C1ESRheat is still omitted from rectifier waveform impedance; RMS/PF
are first-order estimates. Same-line-power closure does not validate real currents.

## Temperature scope

Use the SAME illustrative target pathRair3K/W,Rboard8K/W,LEDcoupling0 androom40C
for central comparisons. D3junction-to-leadreference changes30to20K/W. Its lead
is assumed atboardtemperature; no actualthermalpath has been extracted.
Other localT1/capacitor/bridge/resistor thermalresistances remain guesses.

| Central assumed targetpath at40C | C16C | E22C |
|---|---:|---:|
| Q1_junction | 68.339 | 67.987 |
| D3_junction | 69.735 | 66.028 |
| U1_aux_junction_upper_allocation | 64.327 | 63.801 |
| T1_hotspot_UNCALIBRATED | 81.331 | 80.709 |
| C1_internal_UNCALIBRATED | 72.508 | 71.926 |
| C4_internal_UNCALIBRATED | 65.631 | 65.123 |
| R1_hotspot_UNCALIBRATED | 68.217 | 67.655 |
| BR1_junction_UNCALIBRATED | 63.626 | 63.111 |
| TVS_D1_hotspot_UNCALIBRATED | 75.176 | 74.590 |

These are conditional scenarios, not actual predicted internal temperatures.
The selected max-totalheat case is not each component's temperature envelope.
The hottest selectedcase still putsC1around99C under the guessed path, above
tentative85C reservegoal. Cavityair muststay<=50C forMYRRA. E22doesnotclosecooling.
ActualD3Tj/IRslope/thermalrunaway, C1/C4/T1internalrise, faults and life require
the current measurementplan. Keep normalD3operation below125C with uncertainty
until leakage above the source125C condition is characterized;175C absolute is
not a design target or a leakage bound.

Replay `python calculate.py` with the sibling baseline/LED19 inputs available
at the same specification-reset/relative hierarchy. Stdlib only. comparison.json
contains paired97cases and baseline replay. The earlier method is copied as
baseline-POWER20-method.md; this document controls the E22 differences.

## Auxiliary-bias qualification hold

VDD_surrogate_V is an accounting assumption, not a physical lower bound. The
idealratio19*10/18-1=9.5556V leaves only105.6mV above9.45V beforeR10/winding/
ripple losses. Neither this scalar nor averageauxcurrent proves takeover or
physicalno-regression. See ../open-conditions.json; the loss/current comparison
does not close that hold.
