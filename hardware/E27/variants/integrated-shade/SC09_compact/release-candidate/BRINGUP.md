# Laboratory bring-up plan — no tests performed

This document is a plan, not authorization or measurement evidence. Before power, a qualified230V investigator must name the actual hardware/LED/fixture/wiring revisions, responsible person, equipment ratings, measurement bandwidth, current limit, protection and stop criteria. Use guarded mains-rated equipment and differential measurement; never attach an ordinary grounded oscilloscope lead to floating mains-referenced nodes. An isolation transformer alone does not make internal parts safe.

Unpowered: compare all19 references/46pads against the independent CAT01 intent (0NC) and pin CSV. Inspect polarity, solder bridges, actual clearances, formed leads, bottom protrusion, vent reserve and wire support. Inspect catalogue T1 MSS1210H-125KED and its two SMD lands. Manufacturer inductance test:100kHz,0.1Vrms,0Adc,1.08–1.32mH at25C; DCR<=1.013ohm at25C. Check sample identity and required hot/DC-bias behavior in a separately defined safe setup. The .8748mH hot/bias paper screen combines assumed factors; it is not a manufacturer guaranteed hot curve. No powered testing with an unverified part. Check bleeders, J1/J2 identification and absence of unexpected shorts. Identify minimum actual soldered clearances at package concessions.

Qualified test setup: fully contained access barrier, remote isolation/emergency stop, appropriately fused/current-limited supply and correctly rated differential probes, current measurement and power analyzer. Record starting discharged C6 voltage. Use the chosen verified LED string or a suitable rated load. Both output leads remain mains referenced. Disconnect and verify discharge before changing any load; do not hot-plug LED.

Initial nominal230V run: capture input RMS current/power/PF, LED average/ripple current, output voltage and peak drain/source waveforms with bandwidth stated. Verify proposed normal52–68V load window and approximately135mA total /133mA externalLED nominal operation; no guaranteed current tolerance has yet been established. Repeat at207/253VAC and ambient0/40C after stable operation, using a qualified corner-test protocol. Record Pin-Pout rather than assigning reference-board efficiency.

Open-load/restart: only with separately reviewed guarded test procedure, capture peak C6 and OVP timing; proposed peak stop90V on100V-rated C6. Initial target is not proof of safe transient control. Record discharge90-to5V with both bleeders and one open, using safe deenergized switching arrangements; computed one-open36.45s is a model only. Do not perform LED reconnection while C6 is charged.

Thermal: measure stabilized C6can, T1, L1, RF1, R7, R8/R9, U1SOURCE and D1case in actual chosen fixture/orientations at ambient0–40C. Planning targets C6<=75C (stop85C), T1<=90C, SOURCE/D1case<=100C; junction estimates use applicable manufacturer models, not generic ambient thermal resistance. Stop earlier if any rated derating/stress limit, abnormal current, unstable regulation, smell, discoloration or arcing is reached. Reassess allocation0.9–1.7W from measured losses; not a qualified upper bound.

Abnormal/surge/EMC tests require their own qualified procedures and protected fixtures. Do not short components or apply surge simply on the authority of this plan. Record actual limits, test source impedance/waveform, protective coordination and sample outcomes. No numeric surge/EMI/single-fault PASS is claimed here. Defects require linked revisions and rechecks.

Current specification clarifies inclusivebase-loss accounting and thermal sensitivity. At40°Cambient the unvalidatedT1 scenario spans50.2–90.3°C and may exceed90°Ctarget; do not assume thermal acceptance before measurement. The nominal externalLED current is133.4mAat60V afterbleeders, not an exact135.2mALED guarantee.


CAT01 supersedes every customT1 sample/winding task with factoryMSS1210H-125KED sample/rating/fit inspection. Use currentcatalogue-part electricalreport; noVR25thermalresistance transfer toHVR25. No poweredtestsperformed or authorizedbythisdocument.


ROUTE01: Use the current corrected layout and both-face C6body/vent contract. Can material extends0.25mmleft, fixture vent requires2.5mmfreeair abovePCB. BroadSOURCEpours are removed; do not transfer earlier source-copper thermal predictions. Inspect the physicalR5Kelvinjoin and actual soldered geometry. All listed measurements remain unperformed.
