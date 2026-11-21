# LED19 - seven-LED panel checked against C16

## Current result and owner decision

On21November2026 the owner stated: "jak będzie wiecej lumenów to nie problem".
The former850lm ceiling is therefore not a rejection criterion. The750lm minimum,
first4000K configuration and other colour/family, electrical, thermal, service,
insulation and lifetime requirements remain. This is not a manufacturing approval.
See owner-decision.md and the revision13 addendum in requirements-and-plan.md.

Retain seven series Cree JB2835BWT-G-H40GA0000-N0000001 (4000K,80CRIclass) as the
first panel verification candidate, with unchanged C16 R9=1.80ohm / nominal319mA.
Typical-model result:20.652V,6.588W and958.8lm at assumed optical transmission0.87
and the calculated85C junction-flux reference. The three conditional currentpoints
303.624/319/336.057mA yield917.6/958.8/1004.2lm. Higher flux is accepted; these are
calculations, not measured output or full production bounds.

## Electrical compatibility

For seven LEDs, the typical-voltage model over those currents and junction10..115C
gives20.345..21.255V, inside the allocated19..22V load window. This is not a guarantee
of cold/hot/reel extrema. Source current includes assumed transformer delivery0.90;
actual delivery, ripple and transient peaks are uncharacterized. R6/current-loop,
startup/clamp and all other C16 qualification holds remain applicable.

Six LEDs give17.439..18.218V and can fail the existing healthyVDD9.45V bias screen.
Eight give23.252..24.291V, beyond the current22V allocation. The old8LED2700K panel
cannot silently inherit the seven-LED4000K result. The eventual three-colour family
is not closed by this assessment.

## Thermal conditions

Cree specifies480mA maximum DC and125C absolute junction temperature, with explicit
thermal derating. These are not lifetime targets. Its40K/W junction-to-ambient
example permits about326mA at85C AMBIENT; that is distinct from85C JUNCTION used in
the flux model. Neither the actual lamp's thermal resistance nor temperature is known.

Budget all electrical LED input as heat, with no optical credit: the rectangular
typical-model high point is7.143W for seven LEDs, excluding driver
heat/coupling. At an ASSUMED95C solder point, the same modeled power gives junction
about102.75C with maker7.6K/W TYPICAL Rjs, or
110.31C with a hypothetical15K/W allowance. This does not establish either a95C
solder point or a guaranteed junction/life limit. A metal-core/otherwise qualified
substrate, TIM/heat path and measured solder-point/junction estimate are still due.
Transformer surrounding ambient<=50C and driver component temperatures are separate.

## Retained diagnostics, not new selections

The U40/90CRIclass comparison gives824.6lm nominal and789.2..863.6lm at the same
assumptions. It is not selected: changing CRI/parts is unnecessary merely to keep
the former upper limit. Its DigiKey one-piece route is documented; JLC sourcing is
unconfirmed. No purchasing or assembly acceptance is implied.

R9-only2.21/2.26ohm diagnostics reduce H40 flux but require128.4/131.0kHz in the
existing conservative frequency screen, above the120kHz minimum maximum-frequency
capability. Therefore a resistor-only change is not an accepted fix. Optical
attenuation diagnostics are historical; extra dimming is not required by the owner.

## Evidence and limits

The fresh manufacturerPDF matches pinned CLJ-DS40Rev10B bytes. ExactMPN/limits and
native curves were visually checked; numerical replay matches earlier flux/voltage
and C16frequency calculations. results.json and180-row screen-cases.csv preserve
failures and source assumptions. The chart labels the old band as historical.

The order code does not guarantee an upper flux bin. Hot flux references are
calculated by Cree; scaling with the25C current curve assumes separability. Actual
diffuser transmission, bin, stabilizedjunction temperature, CRI/CCT at319mA, flicker,
lifespan and thermal fit require characterization. Photometric acceptance uses the
owner's230Vac/25+/-1Cambient/base-up/complete-diffuser/stabilization method, not an
assumption that ambient equals junction temperature.

No full manufacturerPDF is redistributed. Replay uses the external retained PDF
through check_led19.py from workspacework/. Production CAD/BOMs/rules/C17exports
are unchanged. This is a compatibility calculation and retained verification
direction, not a finishedLEDpanelPCB, measured qualification or production release.
