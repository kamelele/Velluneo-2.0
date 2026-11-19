# SC07-B coupled reservoir screen

Run actual Python script coupled_output.py; outputs coupled-results.json and coupled-trace-nominal-230.csv. This extends the earlier own AN60-inspired sample/hold mathematics, not PIXls or SPICE. Independent source equations and explicit limitations are embedded in the script/results.

Selected assumptions: Rsense28.7ohm, L3mH, output Cmin120uF, LED fixed84.5V+RINS470ohm, auxiliary12.075V rail/5322ohmfeed, two56k bleeders,321kdetector branch, leakage1.45mA (additional0leakcase). Load-current slope and cap charge are coupled each switching cycle. Resistor corners433.105..508.305ohm. Eight illustrative controller/L/RLED corners per line plus nominal =27cases. No actual pi filter, OVP, relay or full-temperature guarantee.

1s simulations split at0.5s: first half startup reported separately, second half is steady reporting interval. Longest charging gap is consecutive cycles with driver charge<1e-15C. A missing20ms burst requires two adjacent10ms bins with effectively zero charge. This is no statement about photometric flicker metrics.

Nominal207/230/253VAC results respectively:
- LED average54.351/54.560/54.211mA.
- Reservoir peak111.023/110.990/110.676V.
- Peak-to-peak reservoir ripple2.174/1.909/1.646V.
- Largest zero-charge gap2.485/2.242/2.015ms.

Across27illustrative cases: peak116.628V; LEDaverage48.518..62.096mA; mean driver current up to86.835mA. Eighteen cases fall outside proposed50..60.5mA LED average window. All cases have charge in every10ms bin; maximum zero-charge interval2.614ms. No20ms missing steady burst observed. This supports the conditional steady-case analysis without proving90mA or123V over real corners. No fictitious0.7A guarantee is used: peak model current is the selected ILIMIT input.

Numerical sensitivity: nominal230VAC1s vs2s gives LEDaverage54.559922vs54.559268mA, peak110.990vs110.966V and ripple1.909vs1.871V. Replacing exact affine output update with Euler gives54.494175mA, peak110.990586V and ripple1.989V. Switching decision discontinuities change burst patterns; precision at millivolts is unjustified. Charge balance residual is recorded. The model does not establish exact periodic limit cycles. Larger physical-model uncertainties dominate.

A fixed conservative10ms current-drain reserve is not a modeled20ms supply gap. This model finds neither missing half-cycles nor a20ms charge interruption at the studied points. Actual input filter/auto-restart/thermal mechanisms can differ and remain excluded explicitly.
