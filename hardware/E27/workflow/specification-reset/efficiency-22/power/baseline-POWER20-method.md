# POWER20 method and assumptions

## Evidence level

This is a conditional steady-state engineering accounting model, not a switched
simulation, measured efficiency, temperature guarantee, qualification or release.
It uses C16/LED19 and exact current parts; no earlier custom-transformer DCR,
leakage, core geometry or thermal model is transferred to MYRRA74032.

The actual current law is Itotal=VCCR*etaXFMR*4/(2*Rcs). R11||R12=10k draws
Vo/10k; solve ILED=Itotal-Vo/10k jointly with seven LEDs' native typical Vf curve.
The voltage reference Tj85C is an INPUT, not a predicted operating temperature.
10/115C voltage screens do not calculate flux changes or couple optical and thermal
behavior. No new luminous-flux result is claimed. LED19's 319mA LED calculation
was an approximation; this packet distinguishes total secondary and LED current.

etaXFMR=.90 is the existing assumed C16 parameter. TI includes winding/core,
leakage and bias in it. .85/.93 are hypothetical sensitivities, not maker bounds.
Current varies with eta; it is not artificially held319mA during that sweep.
VCCR/Rcs corners preserve C16's allocation. VCS and LP selections are recorded
in calculate.py and do not cover all controller waveforms, jitter or fault states.

## Charge and energy

Use Ip=VCST/Rcs and an EFFECTIVE secondary triangular peak eta*4*Ip. Its duty
is 2Itotal/(eta*4*Ip), its RMS squared is 2/3*effective_peak*Itotal. This is a
charge-consistent loss-branch surrogate: it is NOT an actual winding waveform.
An unscaled triangle would overdeliver current by1/eta and is not reused here.
The surrogate RMS is only a screening input to diode/capacitor losses.

Pd3=.68*Itotal+.06*IsRMS²+selected_reverse_loss, following ST's conduction
formula with an additional assumed reverse-loss sensitivity. Pc4=.12*IC4RMS²
uses the source100kHz20C ESR condition; it is not a hot/aged ESR bound.
G=(Vo*Itotal+Pd3+Pc4)/eta and fs=G/(.5*LP*Ip²). Effective demagnetization
voltage includes the diode/cap losses, enforcing both average charge and energy.
Neither zero algebraic residual nor a plausible fs validates real control timing.

All winding/core/clamp/net-auxiliary power is allocated INSIDE (1-eta)*G.
Net auxiliary current subtracts startup current once. U1 continuous RUN2.1mA
(or2.65mA sensitivity) is specified at25V; actual RUN/WAIT average at~11V is
unknown. GateQg10nC is typical. The auxiliary group includes gate, bias, R10,
R13, D2 and VS network; an additional5mW pulse/network allowance is assumed.
The remaining magnetic allowance is split between T1 and D1/TVS1 using
20/35/50% clamp fractions. These allocations are not predictions from leakage
or core data. Changing the split changes component heating without changing Pin.

Outside that allowance: Q1, R9, bridge, fuse, R1, input capacitors,
startup804k, bulk499k, secondary diode, C4 and output10k. Startup resistor heat
and delivered VDD power are separated; the latter is allocated to the auxiliary
group once. The full input/output/component-heat ledger is checked against
independent line-source power integration.

Primary RMS uses a first-order triangular ramp with line-averaged1/Vbus;
finite on-state resistance, magnetizing-current distortion and resonance are not
solved. Q1 Rds8/12/16ohm are selected cold-to-hot sensitivities; only8ohm at25C,
10V gate is a source maximum. Switching .5/2/5uJ per event includes residual
Coss/turnoff/ringing; it is not a maker bound. Do not add Eoss again. Published
Co(er)6pF relates to0..840V energy, not constant operating Coss; time-related17pF
is different. Neither the resistive fall-time test nor zero-current diode
commutation establishes actual flyback loss.

## Input rectifier and capacitor model

Numerically integrate a sine50Hz full-wave bridge, R1=47ohm plus selected fuse
3/4.48/6ohm, C1=18/15/12uF, fixed bridge pair drop1/1.4/2V, a constant-power
converter, actual-voltage startup and bleeders, and selected leakage. No other
line impedance, EMI filter or harmonic compliance is modeled. Six full line
cycles settle; final two are averaged. Midpoint timestep4us is checked at2us
for nominal. RMS includes charging pulses; I=P/V alone is not RMS. PF=P/(VrmsIrms)
is a model result, separate from conversion efficiency, not a compliance claim.

C1 ESR contributes heat in this model but is not inserted into the charging-path
impedance. Its effect on charging-current shape is omitted. RMS/PF remain
first-order screens; numerical power closure does not validate that waveform.

C1 LF ESR10/22/30ohm and HF ESR1/3/8ohm are sensitivities: no frequency-resolved
exact-part ESR is published. The nominal LF magnitude is motivated by tan-delta
order, not a guaranteed actual100Hz ESR. HF ripple variance uses a spectral-split
triangle approximation with covariance neglected; it cannot qualify capacitor
ripple. Leakage10/50/246.5uA are selected sensitivities; the high value is the
Rubycon rated-voltage five-minute formula evaluated at15uF450V, not a guaranteed
leakage bound at actual bus/temperature. Presets intentionally correlate loss
parameters for tractability; selected extrema are NOT statistical confidence
intervals or exhaustive guaranteed corners. Startup/inrush, faults, standby,
surge, EMI, ageing and abnormal operation require separate tests.

## Thermal network and limits

Compute cavity air=room+Rair*(Pdriver+fLED*PLED), board=cavity+Rb*Pdriver.
All driver heat is assumed to traverse the board node; this is an illustrative
thermal star, not extracted C16 geometry. PLED has no optical heat credit. The
LED fraction0/.25/.5 describes coupling into the driver cavity, not LED efficiency.
Actual conduction directly to housing, radiation to walls, local air gradients,
orientation and vents are unknown. Rair is an effective whole-cavity heat-rejection
parameter, not free-air convection of the PCB. Closed-shell air circulation alone
does not remove heat to the room.

Three ASSUMED paths: targetRair3/Rb8K/W/fLED0; weak closed8/18.52/.25;
poor closed15/30/.5. No existing enclosure is asserted to achieve any of these.
Rb18.52 is merely1/(.0054m²*10W/m²K) for two unobstructed full board faces;
actual board is obstructed, nonisothermal, inside an enclosure. This calculation
does not determine cavity-air resistance or radiator size.

For component temperatures Ti=board+Ri*Pi. Local assumed/reference Ri(K/W):
Q1=20 assumed case-to-board+4.2 source junction-to-case; D3=30 source junction-
to-lead with lead assigned board temperature; U1=44.4 source thetaJB reference,
all auxiliary-group power conservatively assigned to U1; T1=40 unknown hotspot
allowance; C1=80/C4=120 unknown core allowances; R1=25; BR1=30; clamp=50 unknown
allowances. These are conditional sensitivity estimates, NOT actual thermal
resistances. In particular thetaJB test conditions are not this board, and
capacitor/T1 internal temperatures cannot be established from public sources.
Rejecting a hot scenario does not prove a cooler scenario achievable.

The displayed maximum-TOTAL-driver-heat electrical case is not the maximum
temperature case for every component. It is not a per-component envelope.

MYRRA's50C limit is surrounding AIR, not board or winding. At room40C, allowable
cavity rise is10K. Required effective Rair <=10/(Pdriver+fLED*PLED). Use separate
maxima of driver/LED power for a conservative combination of the SELECTED cases;
this still is not a guaranteed worst-case bound. Thermal bridges must preserve
the existing primary/secondary/enclosure insulation. No isolation rule is relaxed.

Absolute maxima are not temperature targets. Maintain maker limits and the existing
project thermal/lifetime requirements; tentative measurement aims C1/C4<=85C,
Q1<=110C and driver cavity<=45C are engineering reserve goals, not newly approved
product requirements. Endurance10000h at105C is not a bulb-life guarantee.
