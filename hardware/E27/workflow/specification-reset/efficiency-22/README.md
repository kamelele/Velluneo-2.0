# EFFICIENCY22 — constrained component optimization

Owner authorized diode/resistor selection, revisedCAD/calculations and compendium.
Base63c7a3fed59d7807bd1b71cf9058175b04a22f4b. **Engineering prototype candidate;
not a manufacturing or measured no-regression approval.** Existing C16physical/
process/human gates remain. No order or powered test occurred.

## Applied four-position ECO

| Ref | C16 | E22 | Reason |
|---|---|---|---|
|D3|STTH2R02A/SMA|STPS2200U/SMB|Lower sourceforwardloss envelope;200V/2A/175C retained,10mssurge100Avs75A;newhotleak/Cj require test|
|R16,R17|CRCW2512402KFKEG402k|CRCW2512422KFKEG422k|Retain500V/1W/1%/100ppm family; modestfeedloss reduction|
|R13|CRCW060380K6FKEA80.6k|TNPW060384K5BEEA84.5k|0.1%/25ppm precision improves worst startup/feed bounds despite largerRstart|

Exactpartpurchase routes in selected-bom.json and component reports. STfactory
shop/DigiKey snapshots supportMOQ1, not live/reservedstock. NewpartsJLCstock/
consignment/process unconfirmed. No speculative factory-winding work required.

R1=47ohm, four499k bulkbleeders, two20k outputbleeders, current/fault/sense/
voltage/NTC/gate/aux resistors and F1/Q1/T1/C1/C4 are unchanged. No protection
removed or clearance/severity relaxed. Reject2xstartup scaling:4/64cases cannot
reachUVLO23V with hotD2leak. Reject obsolete/100Vdiodes and200Vworking-voltage
precision2512 replacements that cannot preserve500V single-short stress margin.

## Result and important limitation

Central accounting changes8.586to8.538Winput,
2.046to1.999Wdriverheat and
76.17to76.58%LEDefficiency.
Only~0.41percentagepoints. Hot-leak selected
cases can add~34mWheat; **netgain is not established for all cases**. D3selection
is for comparative prototype validation, not proof of a universally betterpart.
See power/README.md for IR/Cj/source-temperature reference assumptions.

Mixed-tolerance startup64DCcases and72rectifiedwitnesses pass atdeclaredcorners;
worstpre-UVLODCtime.251660to.247664s, minimumnetcharge9.528to11.754uA,
normalfeed-onlyVDDceiling33.8667to33.3912V. Nominal witness is slower(.19388to
.20746s), both within1starget. No-feedholdup bound improves slightly. Passive
VDDdecay/retry timing is not identical; fullIC/outputflux startup/recovery unqualified.

NewD3 can lower auxiliaryVDD. Use VfD3>=0 rather than retaining an unsupported
.5Vminimum: at19Voutput,D2<=1V,ideal lossless winding-ratio screen9.5556V versus9.45Vhealthyallocation.
This is NOT a physical lower bound: R10=4.7ohm, windingdrop and VDD ripple are omitted.
Only105.6mV is available for all omitted losses at19V;22.46mA throughR10 alone
consumes it. Averageauxcurrent cannot bound that pulse drop. ActualVDD/takeover
and the requested no-regression condition remain OPEN (open-conditions.json).
For selected7LEDmodelminimum20.183V, the ideal ratio result is10.213V, leaving
763mV for omittedlosses; neither value qualifies physicaloperation. No-loadCVconservative
upper28.41V(old27.61+.8diodeoffset) andreverseexposure117.86Vbefore ringing
remain belowC4=63V/D3=200V; actualovershoot remains a physicalhold.

## Native layout and checks

Same45x60mm4layer1.6mm board,33positions/80pads/333track-viaobjects. D3SMB
makerlands1.62x2.18mm,pitch4.22/gap2.60; TNPW0603IPCpads.90x1.00/pitch1.60.
D3shifts+.3mmY to avoid the existingoutputtrack; itslabel shifts+.5mmY. No track
or via geometry changes. Newcourtyards/pads/mask/paste requirefreshGerbers.
Sourceprovenance: STPS2200p6visuallychecked; Vishay28950IPC0603recommendation.
NativeERC/DRC/parity/unconnected0 after real clearance/silk/metadata corrections.
Pinneddoctor10.0.6passes; configurepreviewhaszero-byte rulediff, noapplyneeded.
Toolkitconnectivity geometry comparison/remaininghuman/processhold details are
recorded in checks/. No new stage approvals or successful release are claimed.

Freshmanufacturing/ files replace C17 data FORTHISvariant; avoid mixing oldGerbers,
CPL or BOM with E22. Updatedcompendium-23 includes E22source/renders/layers/
schematic/BOM/power/startup/mfgdata/holds. Earlierpackages remain historical.

## Required comparative tests before qualification

Measure trueinput/output watts and synchronized waveforms at207/230/253Vac,
49..51Hz,cold/hot. Compare D3netconduction/leak/Cj loss atsamejunction/leadtemp,
startup>=90%flux<=1s,VDDmin>=9.45V,no-loadCV/overshoot, first/repeatedfaults,
R13open/short/startupRsinglefault, clampenergy/transformerpeak1.1Apkconstraint,
EMI and isolation. Thermalsoak uses the existing>=3hthen<1K/hour1hbaseline and
10/25/40C orientations. Insulatedprobes/qualifiedoperator/testlimits required.
No actualTINA/controllerfault/retry/thermal/safety/life pass is represented.
