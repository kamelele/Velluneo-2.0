# SC07-C: targeted single PhotoMOS open-fault mitigation

SC06 native sources remain unchanged. This packet specifies the new46-position/110-pin intent before new native capture. The earlierSC07-A comparator/SCR alternative was investigated but is not selected; it is retained as a labelled study. No new KiCad schematic, PCB, order or mains test has been produced.

## Selected response

Retain detection structure with U2/Q2, but replace U3 by TL431BQPK in SOT89; its physical map is1REF2ANODE3CATHODE, not ATL431DBZ. and add a secondAQY221R2VY actuator. R21 andR26 independently feed the LEDs. R6/U4 andR27/U5 each connect BP to SOURCE through their own100ohm. An open input LED or open output in one package leaves the other complete actuator path. This is targeted actuator redundancy, NOT two independent OVP systems. Shared detection/supply/traces and arbitrary insulation/package faults remain outside that claim.

BothLEDresistors are1.78k0.5WHP0805 to cover the hot LED-short power screen. Q2baseR19 is11k; subtract the emitter-basepullup current when calculating base drive. Auxiliary feed is six845ohm1.5WHP2512,5070ohm total. R22=243k widens hysteresis to compensate for faster discharge. R2=28.7ohm0.75WHP1206 is only a recalculated current seed. U3 SOT89 thermal/reference-current budgets are in regulator-thermal-and-rail.json; minimum1mAoperatingcurrent is not10mAprecisiontest. All partgrades matter; normal lowpower substitutes can fail the stated hot power budgets.

## Actual evidence and limits

electrical-checks.json records every number, corner and condition. StaticOVP, auxiliary bias, each input-short resistor, transistor drive budget, passive bleed, retry and headroom have explicit calculations. The old330khysteresis/10kfeed/80mAguard must not be reused. Additional auxiliary input at120V is about1.26W; this is a real efficiency/thermal cost, not free redundancy.

passive-inrush.cir was actually run with ngspice46; the log and hash of the bundled engine are included. Linear inrush current exceeds the inductor's10%drop reference, which establishes need for nonlinear verification, not actual damage. The current sensitivity model is our own limited sample/hold arithmetic, NOT a manufacturer model or PIXls and NOT a full-temperature current guarantee.

The original17 requirements remain, including physical release evidence. The structured driver/LED interface is now specified. No unknown is closed by simply inventing a test or renaming a typical curve as a maximum. Localcomponent temperature ceilings are design conditions, not measured temperatures.

## Stage boundary

New exact pin-intent approval is required before nativeSC07capture; previousSC06approval is not rebound to this different graph. Schematic acceptance and PCB placement additionally require closure or an explicitly reviewed bounded prototype scope for the remaining current-stage issues. No complete electrical/safety acceptance is claimed.
