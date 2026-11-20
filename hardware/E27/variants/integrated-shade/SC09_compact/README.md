# SC09-A compact bulb-driver proposal

This is a new compact RDR-464-derived architecture, not a scaled SC08-B board. The owner rejected140x100mm and selected4000K,CRIatleast80. Current work is pre-capture:19positions/47physicalpins/11nets/one explicitNC. No new schematic or PCB exists and no new stage approval is recorded.

Primary candidate: LYT1603D-TL nonisolated buck,135mAnominal,20series3VLEDs. Current-generation/input/overvoltage,loss and component bounds are in calculated-proposal.json and reference/. Exactcurrent/voltage/light/thermal/surge behavior remains unmeasured. LYT1603D is active but NRND; T1 retains the manufacturer's custom single-winding EE10 recipe. These are procurement/maintenance risks, not ignored facts.

C6 changes from obsolete150uF63V to current150uF100V, with actual12.5mmnominaldiameter/22mmmaximumcase length. Two68kbleeders support a stated one-open discharge calculation. C1/C4/C5 are updated parts; R7 is a voltage-rated390kVR25 rather than an unreviewed ordinary resistor. R4 retains12.4k for OVPheadroom; currentR6=3.65ohm. No energizedhotplug or independentdualchannelprotection is claimed. All conductors remain mainsreferenced.

The body-only study finds45x25mm packing with horizontalcapacitor and separate5mmventreserve; it omits actualpads,formedleadcollisions,electricalspacing,routing andhousingfit. The maximum proposed stop budget is50x25x20mm. Any inability to meet it requires redesign/review,not silently enlarging the board. Actualcavity/height/leadforming/insulation contracts must be accepted before placement.

All17original finished-product requirements remain controlling; their unchanged source is retained in the SC08 project. Prototype scope does not qualify a finishedlamp. No ERC/DRC/PCBfit/800lm/compliance/order claim follows from research. Earlier routing remains historical;mainisoutsidewritescope.
