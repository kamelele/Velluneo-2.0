# SC06-B driver capture proposal

Board-only230V/50Hz,207–253Vscreen; no enclosure outline. This freezes an engineering BOM and independent physical-pin intent for the requested KiCad schematic. It does not claim production qualification. Main is unchanged. Original17requirements remain controlling; earlier enclosure-fit concerns are deferred by the owner.

## Selected circuit

LYT0006D-TL high-side buck, two RFC1010B-155KE1.5mH inductors in series,33.2ohm sense and22uF samplehold.150uF160V EEUED2C151 stays in the base.470ohm5W R7 permanently limits energy delivered to the LED connector. Defaultloadproposal:30seriesCreeJB2835BG2700KCRI80,D8flux/ACvoltagebins,about55mA. Bins need reel confirmation; the MPN alone does not establish them. This gives about781lm at the declared85CtypicalLEDfactor and87%diffuser transmission; approximately800lm remains a design target, not measured flux. Healthyloadacceptanceproposal72–84.5V,LEDaverage50–60.5mA;fault-current screenuses60Vhealthy/58VoneLEDshort as engineering guard inputs requiring validation.

## Protection redesign

The oldSCR-to-groundBPpath is removed. It could impose approximately−VF onBPrelativeSOURCE against the−0.3V absolute minimum. COUT discharge must not use that path. A PhotoMOS AQY221R2VY now shunts BP to SOURCE through100ohm R6; this keeps the controlled voltage nonnegative. The resistor limitsCBP100nF discharge to about62mA;steady7.5mA BPcharge current gives about0.8V, below the4.35V worstderived undervoltage boundary at the listed25Cconditions. Actualhotchargecurrent,relayRon/timing andstartup remain qualification tests.

TLV6700 uses its400mV reference with2x160k/1k precisiondivider. ATL431 is only a regulated12Vauxiliaryrail, with≥1mA bias required at the controlpoint. A330khysteresisresistor and47kOFFpulldown create an explicit window; do not assume the TLV's internalhysteresis has a specifiedminimum. Outputovervoltage stops switching, the reservoir decays through the bleeders/auxiliarynetwork, and switching can restart after the lower threshold. There is noAC-reset latch in this revision. Automaticretry is bounded by the externalwindow and150uF reservoir; it must be verified on real hardware.

Twoindependent56k1W bleeders are parallel acrossCOUT. Calculated passive135-to5V time is under18s normally and under35s with oneopen resistor, usingC+20% and declaredresistancebudgets. The proposed acceptance target is≤40s afterremovingpower, not a claim of touchsafe contacts. No activecapacitorcrowbar is selected: this avoids continuously dumping the entiredriverpower into a5Wresistor during anopen-load controlfault. A failed-open PhotoMOS defeats the sole activeOVPaction; single-faultcontainment remains a declared safetyacceptance issue, not a falsely closed condition.

InputRF is220ohm fusible FWFU2W220RJ, exactDiodes MB10S-13 bridge,10mH RFC1010B-106KE πfilter, ProTek5KP400A BUSclamp. C1 is100nF2kV R76UR31004030J andC2 is330nF1kV R76QR3330SE30J. These largerpostbridgefilmcapacitors replace450V parts that were below the intendedsurgeclamp. MOV is omitted in this circuit; do not claim that anunqualified275VACMOVprotectsa700Vswitch. TVShotclamp,filterringing,RFpulse/fusing,D1andU1overshootrequirequalification. C4D02120E1200VSiC replaces600VfreewheelD1;1andCASEarecathode,2anode.

## Engineering limits and remaining checks

Normalpeak123V andfault135V are acceptance requirements. Static detector calculations and a conservative normalripple/headroombudget support investigating them, but neither is a measured guarantee. R7 dissipates1.42W at55mA, increasing withripple/current. New150uF+20% energy at135V is1.64025J. Reevaluate allprior68uF results. The currentsetting is a numericaldesignseed, not a manufacturer-qualified currentwindow; physicalcorrelation/trim and fullthermal/flicker/EMC/insulationfaultqualification remain required.

Prototype thermalproposal: localPhotoMOSambient≤85C, capacitorcan≤95C, inputfilm≤100C, U1SOURCE≤100C;−20C startup within the electrolytic rating. These are proposedboardtestboundaries, not accepted enclosure conditions or achieved temperatures. Electrical output is mainsreferenced, neverSELV.

## Native KiCad capture status

Kamil approved the exact SC06-B pin intent on 2026-11-19 and approved the manual prototype process; see owner-capture-approval.json and owner-process-line-decision.json. Open SC06_driver.kicad_pro with KiCad 10.0.6. The native schematic and local symbol/footprint libraries are included. No board has been generated or routed.

Fresh exported connectivity, ERC, footprint pad inventory, requirements and work-mode check reports are saved in the SC06 workflow capture-checks directory. These have different scopes: a passing ERC or netlist comparison is not a passing product/safety review. All original 17 requirements remain controlling; two actual owner choices are now recorded, while engineering/standards and evidence gates remain open.

The applied toolkit configuration supplies the approved fabrication baseline and ERC policy only. Its generic 0.2 mm fabrication clearance is NOT a mains insulation requirement. Product insulation domains/creepage remain undefined and must be established before PCB acceptance. No safety spacing can be inferred from this baseline.

Local land patterns are engineering proposals. Their physical pad inventory is checked with matching pcbnew, and manufacturer-specific pad remapping is documented in footprint-provenance.json. Geometry, lead forming, polarized orientation, thermal spacing and assembly qualification remain subject to review. Generic KiCad 3D references are not certified manufacturer models.

Economic/Standard PCBA sourcing and quotation remain later procurement work. No purchase, production, mains test, schematic-stage acceptance or PCB-stage approval is implied by this capture package.
