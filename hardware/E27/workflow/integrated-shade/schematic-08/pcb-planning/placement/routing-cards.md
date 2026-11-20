# Routing cards for the corrected placement

These are routing plans. The native PCB still has no tracks, vias or conductive zones.

## Power progression

The corrected layout keeps all 47 parts and accepted regions. Film-capacitor BUS pads face the core; D4 is near the film-bank side, and the inductors progress toward C5. The same large D1.CASE cathode contact is used in both OFF-loop comparisons. It already shares SENSE_FB with pin 1; no electrical change is involved.

The sum of minimum external freewheel connection spans is 80.506 mm, versus 131.589 mm in the rejected arrangement. L3-to-C5 is 22.130 mm and C5-return-to-D1 is 23.496 mm. C2 BUS-to-D4 is 12.985 mm. D4-to-U1 grows to 16.546 mm: an explicit tradeoff. These are physical pin-center lower bounds, not routed lengths, parasitic inductance, EMC results or a manufacturer compliance limit.

## Output and return corridors

`planned-output-corridors.svg` overlays dashed guides on the native layer export. They are not PCB copper or manufacturing data. The proposed 0.6 mm COUT path runs at x=124.5 mm toward C5 positive. DC_RETURN exits D1 pad 2 toward x=103.5, travels to y=60.5, then x=117.5 and down beside the output path toward C5 negative. This avoids a front-side crossing of the D1 cathode and the U5 SOURCE pad.

Conservative checks against all 47 footprints find zero corridor/pad-box violations, with nominal target margins of 0.310 mm (return) and 0.450 mm (output). The exact D1 pad-pair concession applies only within its accepted courtyard-plus-1-mm escape; generic spacing resumes outside. No new via or zone concession is granted. These two guides do not qualify all future routes: exact saved-board DRC, voltage-pair, finite-escape and surface-path checks remain required.

## Feedback and bypass

C3 is directly beside U1; each bypass leg has a 2.673 mm minimum span. R2 sense-to-U1 FB spans 11.424 mm. Use a dedicated quiet Kelvin branch from R2/C10 sense, around the north side of U1 SOURCE pins through the space below C3. Keep diode power current out of this sense branch. C3 was moved to y=35.9 mm to increase the entry space. Actual track widths, entry clearances and layer changes must still be checked; a drawn center line is not proof of routing.

## PhotoMOS branches

The SOURCE branches span 14.451/20.234 mm, exceeding the initial advisory 5 mm connection goal. Both 100-ohm resistors are near the C3 BP star. Route each actuator's BP/SOURCE branches together to reduce loop area, away from drain and quiet-control wiring. Backside paired tracks may be needed where front-side input-domain pads obstruct a generic-clearance path. Use normal via clearances; component pad exceptions do not extend to added vias. A narrow backside track is distinct from the prohibited blanket SOURCE plane.

Only the explicitly accepted SOURCE-referenced local pairs may use the 0.30 mm functional target. Other domains retain their full targets. Longer clamp branches are a disclosed planning tradeoff, not a completed 5 mm claim, CMTI qualification or measured shutdown result. Actual hot operation and the 0.6 ms shutdown condition remain to be verified before energized acceptance.

## Input and quiet returns

The accepted film-bank/output separation leaves a long input return. Plan adjoining BUS/return routes with their generic HV spacing. Keep high-current input/output return out of U3, R15/R17 and U2 reference taps. Connect the quiet return as a separate branch at the main return star. Keep the fast SOURCE copper compact on the front; no blanket backside SOURCE plane. Interlayer geometry does not establish qualified physical insulation.

## Thermal reservations

Actual heater-to-sensitive-part courtyard gaps meet the 10 mm planning floor, including C4/C10. Fab-box checks give minima of 16.275 mm (U4), 24.875 mm (U5), 19.500 mm (C4) and 10.750 mm (C10). Keep the left board edge physically uppermost in the vertical fixture. No component temperatures are predicted by these distances.

U3's 20 × 20 mm backside DC_RETURN-only region and nine intended thermal vias remain reservations for routing; an effective thermal resistance of 85 K/W has not been demonstrated. The guarded fixture, probe setup, wire restraint, temperature limits and physical tests remain prerequisites for energizing. There is no enclosure design or MPN substitution in this task.
