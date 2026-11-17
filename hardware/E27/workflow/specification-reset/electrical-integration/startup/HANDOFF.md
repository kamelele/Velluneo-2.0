# ELEC-CLOSE-01 startup implementer handoff

Read projectAGENTS/installed implementer and current specification revision12, finalization/support study, inherited driver/bias/startup sources. This handoff is integrated only under electrical-integration/startup/. No product CAD, approved physical graph, component value or requirement changed. This is new primary-source evidence plus reproduced analytical calculations, not a controller/SPICE/physical startup pass or major-finding closure.

## Real source correction

Earlier statements that no source describes the initial sampling frequency are too broad. TI **SLUAAC5, August2021**, official https://www.ti.com/lit/pdf/SLUAAC5, listsUCC28710/1/2/3 among its covered controllers(p2). Its initial-power-up discussion(p5) says three sampling gate pulses occur at the controller maximum switching frequency; retry discussion(p7) repeats that cadence. P3 explicitly warns that controllers are parametrically different and usesUCC28704 for its control-law example. Thus this is a valid source witness for the intended sampling cadence, not a full corner-certified UCC28711 startup timing envelope. It does not specify UVLO-to-first-edge latency or extensions/fault/residual-current handling in this exact circuit. Do not import the example's750ns blanking value intoUCC28711 as a new guarantee.

TI **SLUA783, October2016**, official https://www.ti.com/lit/pdf/SLUA783,p5 explicitly placesUCC28710/1/2/3 first-cycle on-time fault threshold at1/fSW(max). This adds a concrete source-defined screen absent from the previous charge-only calculation.

Downloaded originals were actually visually inspected. SHA256:SLUAAC5=57cb199bd678c1af8283f12ef1f0cb3b51e7f75a5d8392977fd68b6489af0796; SLUA783=23be2ca81d848bcb7e49baab8a1945ec68ddaf711aa43b9965ac50e962d1d806. NativeUCCPDF remains762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248.

## Reproduced current candidate and improved conditional witness

`calculate.py` independently reproduces128r12 cases and agrees numerically with saved support-results.json:main first-three all-RUN allowance0.689239ms,stress0.429348ms; takeover16.272727V output; worst ramp1.508169ms/5.942571uC. It asserts the existing stress allowance and takeover match. The effective minimumCDD0.890321uF provides**8.012889uC** from minimum19V turnon to chosen10V trough (9.348371uC to maximum8.5V UVLO-off).

Use three periods at the slowest specifiedfSW(max)=92kHz as a **source-cadence witness**, not an invented measured elapsed time:3/92k=32.6087us. Keep the existing separate100us settling hypothesis, constructedCC ramp, no first-three output-energy credit,16nC gate hypothesis and3.5mA all-RUN base hypothesis. Calculated worst takeoverVDD becomes**11.55965V**, compared with10.50849V for the old arbitrary0.300ms first-three interval. This supports feasibility with material reserve; it does not prove actualstartup takes32.6us or fulfils those hypotheses.

The more useful charge-domain acceptance condition avoids assigning RUN/WAIT residency:

    Ibase*Tbase + Qg*Nequivalent + Qextra <= 8.012889 uC

For the existing worst constructed ramp plus source-cadence witness,Tbase=1.6407777ms andNequivalent=55.098707gate events. At16nC this allows a constant base current up to**4.34630mA**; at3.5mA it allowsQg up to**41.2018nC**. Each is a one-variable sensitivity holding the other and constructed timing/ramp fixed, not two simultaneous limits. At3.5mA/16nC, unmodelled acquisition/bias chargeQextra must remain<=**1.388588uC**. A defensible corner envelope for this net charge, rather than an assumed WAIT fraction, is the specific missing witness.

Alternatively, retain first-three elapsedT and cumulativeRUN durationR in milliseconds. After existing ramp/settling/three gate-charge allocations, the stress case has1.502718uC left:

    0.970*T + 2.530*R <= 1.502718 uC

This uses nativeIWAIT120uA/IRUN2.65mA at25V plus the existing0.85mA stress ancillary allowance continuously. It does not assert a duty split or current limits at declining startupVDD.

## IRUN and ancillary interpretation

NativeIRUN2.65mA is specified atVDD25V,IDRV0,NTCopen. IWAIT120uA is another state. Neither3.2mA nor3.5mA is a manufacturer current limit across9–23V. Their added0.55/0.85mA are project allowances. Existing RGS47k at16V/−2.1%,NTC125uA and10uA gate-leakage illustration sum0.48273mA; main leaves0.06727mA extra, stress0.36727mA. Pull-down consumption only occurs whileVGS is high, so charging it continuously is conservative, but reducing it through an invented gate/RUN/WAIT duty would be unjustified. Gate charge is allocated separately; native20mA source-current test atVDRV8/VDD9 does not guarantee a complete real gate waveform or turn-off delay.

## Initial pulses: concrete compatibility check

SLUA783's source on-time screen is9.434us at106kHz. AtLp±10%,RCS±2.1%,240–357.796V and nativeVCST(min)175–215mV, ideal first-cycle magnetic rise is**0.419–0.979us**, before actual gate/sense dynamics. The selected inductance therefore does not itself approach that fault screen in this ideal calculation.

A fully-reset,no-load secondaryLC calculation gives first-pulse demagnetization21.47–63.86us, longer than the nominal9.43–10.87us sampling period. Therefore commanded sample cadence cannot be equated to three independently fully-demagnetizedDCM cycles. This observation is not a claim that TI's sampling sequence cannot work.

`hybrid3.py` explicitly carries residual current through three commanded periods:ideal magnetizing inductance, sourceLEB180–280ns, ASSUMED100–150ns total delay,0.5/1.2V diode assumptions, bleed,capacitor cases and92/106kHz. **768cases actually executed.** Maximumon-time1.12852us,primary peak0.242097A,linearfluxproxy0.079820T. Every case retains current between the first two pulses; many later pulses areLEB-limited. After three periodsVo=0.421–4.306V andremaining primary-equivalent current0.0252–0.2211A. Thus a residual-current/LEB-overshoot sequence is physically compatible within this constructed witness; it does not validate the actualTIstate machine or establish three exactIPP(min) pulses. Realgate/Miller/Coss,recovery,VS/CSspikes,leakage/aux current,remanence and magnetic nonlinearity are omitted. RLCsubtraction is omitted for a higher-threshold peak illustration, not as a minimum delivered-energy guarantee. Actualrecords/conditions are inhybrid3-results.json.

## Optional unapproved RVDD ECO, kept separate

For coordinator's proposed1Mohm VDD bleeder, use the conservative35V/(1Mohm×0.979)=35.7508uA additional draw, even though the studied decline starts<=23V. Repeating the same calculations gives:

| Conditional result | Approved baseline | Optional UNAPPROVED RVDD |
|---|---:|---:|
| WorstVDD with source-cadence witness |11.55965V|11.49376V|
| WorstVDD at old0.300ms first-three assumption |10.50849V|10.43187V|
| Stress first-three all-RUN allowance |0.429348ms|0.408746ms|
| Main first-three all-RUN allowance |0.689239ms|0.663855ms|

RVDD was not folded into the baseline or applied toCAD. Other passive-discharge ECO branches do not draw fromVDD directly and are not added to this bias calculation.

## Practical decision and exact remaining scope

Update the analytical source basis to the newly found intendedfSW(max) sampling cadence and on-time screen; preserve the current2x470nF candidate rather than increaseCDD beyond its native1uF recommendation. The charge frontier shows useful margin, so the existing arbitrary0.3ms assumption is no longer the only feasibility witness. RetainRC-BIAS-001 as unresolved for physical/full-model validation until the actual startup trajectory supplies netcharge<=8.012889uC to sustained auxiliary takeover andVDD>=10V, under the circuit/input/component/temperature envelope. Needed signals are matchedVDD,DRV/gate,CS,rawaux andoutput; actualQg/bias draw/settling andfalsefault behaviour must be resolved in that same trajectory. No scope expansion into a generic topology survey is needed.

A timing-independent passive feed sized for the assumed full5.196mA bias would needR<=41.76kohm at240V/23V and dissipate~2.684W at highline:rejected as the default6–10W lamp solution. ReducingCout can improve reserve (12uFmax permits1.138ms in the same stressmodel), but would require independently meeting output/opticalripple criteria; no capacitor change is selected here.

Run the repository-relative commands in README.md; calculate.py requires external hash-matched source PDFs. Inputs/results/conditions/hashes, all128ramp rows, source PDF hashes/URLs/page references and actual calculation logs are preserved; vendor PDFs and rendered pages are not redistributed in this repository. No actual controller-model execution, altered source parameters, measurement, majorfinding selfclosure or stageapproval claimed.
