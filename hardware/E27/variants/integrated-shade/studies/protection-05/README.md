# PR05: base reservoir, passive reconnect limiter and pulse-rated discharge

PR05 selects a simple passive protection candidate: keep the68uF/160V reservoir in the base, add RINS470ohm AC05 between COUT+ and LED+, and replace R6 with the same470ohm pulse-rated part. Upgrade the two22kohm bleeders to2010/0.75W. All original17requirements remain controlling. This is a revised engineering proposal, not accepted schematic/PCB or permission for mains tests.

The two power resistors have different jobs. RINS remains in series during lighting and limits reconnect even before an SCR trip; the bulk reservoir must have NO alternate path bypassing it to the module. R6 remains in the AN60Fig8 latch path COUT+ -> L2 -> SOURCE -> D2 -> BP -> R6 -> SCR -> bridgeDC-. The previous100ohm resistor gave excessive modeled current relative to the selected inductor screen.470ohm reduces the135V capacitor-only upper bound below0.32A, including a declared3% resistance budget, versus L2's0.50A25C saturation screen. Existing current in L2 at trip, hot inductance and latch behavior still require checking. Do not claim470ohm is an approved substitution in the PI reference circuit.

## Voltage and optical operating point

85V is no longer the reservoir operating point. At55mA, RINS drops25.85V and loses1.422W. A healthy64–90V LED string therefore calls for roughly90–116V nominal at the reservoir. The screening envelope permits60.5mA and adds a3% resistance reserve: the maximum normal reservoir voltage is approximately120.75V. The proposed OVP static target is125–133V with an overshoot-inclusive ceiling135V. These are requirements for the new detector, not measured or guaranteed values of the old100V Zener circuit. Keep160V COUT; do not substitute the63V capacitor considered with TPS2660.

About30–32 series Cree JB2835B G/J LEDs near55mA are an optical/current study seed, not a frozen LED count/bin/CCT. Cree's typical4000K80CRI figures cannot prove800lm at a different CCT/CRI after the diffuser. The64V healthy and62V one-short lower bounds are explicit hypothetical acceptance inputs; they must be established from the actual selected string and its temperature/current range. LED current regulation must include the44kohm bleeder current, about2.7mA at120V. The new detector also draws approximately3.0mA through its36kohm feed and0.463mA through its divider:55mALED at120V therefore requires about61.19mA total driver current. Include all three auxiliary paths in the LYT/sense design. The old95mA sense values do NOT apply; AN60/PIXls iteration for the new current and L is outstanding.

## Component loading

At135V and81.6uF the stored energy is0.74358J. With470ohm minus5%, the full-short initial resistor load is40.82W and current0.302A. The added3% resistance budget raises these to about42.08W/0.312A. Healthy64V and one-short62V assumptions yield approximately164/169mA with this budget. These currents must fit the actual hot LED thermal limit; the Cree180mA105C example assumes ambient temperature and40C/W junction-to-ambient, not measured solder temperature.

Vishay's AC05 room-temperature overload condition is50W for5s. The complete passive capacitor-only waveform lies below that power; this is a conservative engineering screening comparison, not a250J rating or hot/repetitive pulse qualification. RINS starts hot after dissipating up to about1.86W at the screening current/resistance corner. Converter energy before shutdown must be added. R6 also needs a full continued-feed/holding/reset check. If the latch fails and135V is sustained across R6, it would dissipate roughly39W continuously and fail its rating.

The two22kohm bleeders each dissipate0.207W nominal at135V;0.209W at unequal1% corners. CRCW2010's derated allowance at125C is0.265W under its mounting conditions. Include TCR and measured local temperature before qualification. A single bleeder short overloads the other at about0.837W: the pair is NOT single-fault-tolerant discharge protection. Passive135-to5V time is about12s, and the contacts remain mains-referenced even after that calculation.

## Simplicity decision

The40V TPS26600PWPR alternative adds low-loss active limiting but its60V input limit is not protected by its own output OVP. It also lacks a guaranteed low-current limit window at the proposed200–250mA settings, and its startup ramp alone does not limit arbitrary reconnect. Solving the input overshoot and qualifying a new LED/current point adds work. Retain it as a comparison, not the active circuit. No added eFuse or bypass switch is selected in PR05. Permanent resistor loss is the material price of simplicity.

## PCB gate

The fit experiment reserves real envelopes for both AC05 resistors, upgraded bleeders and a detector block, retaining the20mm reservoir height. It is NOT a nativePCB, footprint/padmap, routed placement, E27 fit or thermal result. The earlier64x40mm estimate predates these parts and must not be quoted as the new board size.

Before schematic capture: close the exact current/LED voltage envelope, precision detector qualification/full circuit pin intent, full-source operating calculation and process choice; obtain the human decision on the exact specification/connectivity packet. Before placement: accepted schematic, footprint checks, ERC/connectivity and spatial intent. Pending hot pulse/overshoot tests are qualification work, not fabricated proof. PR05 does not advance an acceptance stage. See the owned gate list and four actual review records in the workflow directory.

A concrete ATL431/PNP precision-trigger candidate and independent pin draft are included in ovp-candidate.json. Its calculated interval and low-current limitation remain explicit; it has not closed the OVP gate. Smaller560ohm AC04 was compared and deferred: only1.5mm shorter body, less thermal margin and another4.95V/0.272W at55mA. Retain470ohm AC05 for this frozen packet.

SPARE_VR1 and SPARE_R5 in the fit data are retired old component reservations kept as conservative free space; they are not parts of the new detector. The OVP block is not a final footprint/padmap.
