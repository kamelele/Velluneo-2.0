**Corrected magnetic selection:** root selected MYRRA74089. Manufacturer drawing visually verified: body21×21mm, height22mm; pin3 removed;9physicalpins,7NC when primary4–5 used. The preliminary74023 axis interpretation was wrong: it is21×17mmplan and31mmhigh, not17mmhigh. The previous19.5/20mm overall envelope is not met by this part. The original1.324582µs is not established erroneous; see reconciliation below.
# Final engineering calculations for the proposed TME PCB

Actor /root/tme_architecture; bounded research implementation, 2026-11-23. Companion `final-calculations.json` contains reproducible arithmetic inputs, formulas represented by numeric values, scenarios and explicit unknowns. No CAD was edited and no powered test occurred.

This supersedes the preliminary report's tentative suggestion that the old1.324582µs was an error. That number is hardcoded in `work/compact09/catalog-only/catalogue_documents.py`; its complete original derivation was not recovered. At52V andL=.8748mH it corresponds toImin=.463022A/Rsense,max=.589604Ω, which is plausible. **No old calculation error is established.**

## Source and limits of the current model

Primary source: Power Integrations LYTSwitch-1 RevB07/16, pp4,7–9:
https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf?language=en

The manufacturer estimates Rsense=|VFB|/(k×Iout), k=3.6 forLYT16xx, and explicitly says trimming may be necessary. VFB magnitude273–285mV is specified at25°C. No separate guaranteed tolerance for the3.6 coefficient or VFB temperature curve is published in this sheet. Its±3% constant-current headline is for single-line applications, not a new independent guarantee over all line/LED/temperature corners. Therefore dividing every peak-current corner by3.6 gives a useful **screen**, not a guarantee of actual LED current. References to peak below are normal-operation model estimates, not the fault limiter.

Controller minimum-on-time max1.25µs; inputOVP threshold.9–1.1mA andoutputOVP2.3–2.48V are25°C limits. The normal1.25µs timing row is under default-40..125°C conditions. Auto-restart current limit1.06–1.24A is characterized at25°C anddi/dt446mA/µs; it is not a guaranteed bound at an arbitrary MYRRA fault waveform. Foldback138–152°C andtypicalshutdown160°C are protective functions, not suitable normal operating targets.

## New components and explicitly assumed reserves

R5=.68Ω1%,200ppm/K,Viking;R6=3.65Ω1%,400ppm/K,Royal. R7=4×97.6kΩ inseries,total390.4kΩ1% each; provisionalTCR±200ppm/K (must be at least this good in selected exactMPN). R4=12.4kΩ1%,100ppm/K. Both68kbleeders1%,100ppm/K. All resistor bodies are limited to100°C for this screen; ΔTmax75Kfrom25°C. Use independent±1% long-term engineering reserves. These reserves are assumptions, not manufacturer life guarantees at unspecified test conditions.

Extended scenario additionally multiplies25°C FB andOVP threshold limits by.98/1.02 as an **assumed** thermal reserve. It does not turn unspecified IC temperature behaviour into a guarantee. JSON also gives resistor-only scenarios at0/25/40/75/100°C without that reserve.

For each resistor Rlo/hi=Rnom×(1±.01)×(1±TCR×75K)×(1±.01). Parallel combination is computed independently. MagneticLmin=1.3mH×.9tolerance×.9bias×.9temperature=.9477mH; the latter two factors are unverified assumptions.

## Current, timing and magnetic screen

NominalRsense=.57321016Ω; Ipk=.486732A, **not a worst-case maximum**. Nominaltotal output135.203mA, less1.765mA bleeders at60V gives133.439mA externalLED,8.0063W. Actual current/800lm need measurement.

ExtendedRparallel=.552036..594863Ω; normalIpk=.449751..526596A. Dividing by3.6 gives124.931..146.277mA total, with the model limitations above. Full-triangle RMS upper.304031A. Conservative full-triangle sense-resistor powersR5=.04291W,R6=.00812W; actual on-time occupancy reduces healthy averages. This is not a startup/fault pulse rating check.

Minimum on-time is evaluated at **minimum current, minimumLED voltage52V, maximumline253VAC**:
`ton=Lmin×Ipk,min/(253×sqrt(2)−52)` =**1.393833µs**,11.507% above1.25µs. It requiresL≥.849905mH atthatcondition. This passes the stated assumed screen; measured hot/DC-biased differentialL andactual current must satisfy it. Do not substitute nominal current in this minimum calculation.

MYRRA74089 primary1.3mH±10%,.85Apeak. Normalpeakupper.5266A is61.95% of statedpeak. Conservative energy usingLmax1.43mH andImax is198.27µJ versus469.63µJ atmanufacturer.85A/nominalL. Primary normalvoltageupper305.80V; open secondaries5/86turnratio ideal17.78V each; auxiliary12/86 ideal42.67V, plusringing/commonmode. Allunusedpinsarehot-domainNC.

A fixed-peakCrM toy calculation f=1/[L×Ipk×(1/(Vin−Vout)+1/Vout)] gives104.27kHz at52V and129.22kHz at68V withLmin/Imin. The manufacturer132kHz flyback example is **not a universal maximum rating**, but this reveals that frequency cannot simply be called82kHz for all corners. Actualline/on-time modulation/forced-frequency behaviour must be measured and assessed forcoreloss.

**DCR, primary RMS rating, hotbias andcoreloss are unpublished in the short MYRRA sheet.** Worst-normal copperloss coefficient is.092435×DCR_hot watts. Proposed laboratory acceptance budget: DCR25≤2.0Ω, DCRhot≤2.6Ω, yieldingCu≤.240W underthisscreen; these are project acceptance thresholds to measure, not catalogue specs or predictions. Reject/review parts exceedingthem. Require normalIpk≤.55A andnoaccelerating/saturationknee, fullwaveformRMS≤.32A, hotdifferentialL≥.9477mH preferably andatleast.849905mH forbaretimingcriterion. BetterLmarginmustnotbeclaimedfromzerobiasmeasurementalone.

**Fault gate remains:** manufacturer.85Apeak isbelowLYTfaultlimiter1.24A. A short/startup/controlfault may have a different waveform. Do not claim guaranteed fault containment or firstpulse saturation immunity from normalcurrentmargin. Before anypoweredfaulttest, definecontainedfixture andindependentcurrentlimiting; characterizefaultswithinmanufacturercoilcurrent, orredesignfaultcurrentprotection/selectothermagnetic. A fuseisnot a cyclebycycle.85Apeaklimiter.

## OutputOVP anddivider power

NominalstaticOVP=`2.4×(1+390400/12400)`=**77.96129V**. This is theexact4×97.6k result, not77.957V. Includingresistorreserves and25°CICthresholds gives70.31971..85.58893V. Extraassumed±2%ICthermalreserve gives**68.91332..87.30071V**. DynamicCOUT≤90V remains a measurement target,not a proven clamp.

At68V meanoutput thelowOVPscreen hasonly.913V headroom:100Hzripple andswitchingovershootcantriggerprematureOVP. Thus52–68V is a proposedloadwindow, **not a guaranteed fully regulated envelope**. Example screening: at207VAC/68V, line-deadzone duration2asin(68/(207sqrt2))/(2π50)≈1.49ms;146mA discharge intoCmin112.8µF canlose~1.93V overthatinterval. This doesnot predictcompletecontrolledripple,but confirms theheadroomneedsrealwaveformqualification. ReduceacceptableLEDVfwindow/retuneOVPonlywithfullnewcorneranddynamicreview.

R7stringconservativeconstant305.80V bound=.24811Wtotal, about.06203Weach before mismatch;400Vconstantstress=.42453Wtotal,.10613Weachequalshare,.10981Wworstindependentmismatch. Rateeachpartagainstitsactualhotderatingandmaxworkingvoltage; do nottransfertheoldHVRthermalresistance. Fourresistorsneedseparateclearanceatintermediatenodes, nooverlappingroutingacrossthestring.

InputOVPstaticmintrip391.20V at52Voutput andresistorlowscreen; maxtrip512.64V at68Vhighscreen. Normalrectifiedlinecrest357.80V isbelowmintrip, conditionally. InputOVPiscontrolresponse,not anexternal600Vdiode/400Vcapacitorclamp. MOVcatalogueclamp(e.g710V at10A) doesnotproveallnodesbelowratings;diodeVreverse,400Vfiltercaps,725VIC,seriesresistorpulseandMOVtemperature/energyneedactualcoordinatedsurgeanalysis/test. No surge pass is created here.

## Three47µF capacitors anddischarge

COUT=141µFnominal,112.8..169.2µF at±20%;energystoredat90V=.68526J;at68V=.39119J. Withone68kbleederfailedopen, survivingRmax69.887051kΩ gives**34.1783s from90Vto5V**;bothhealthy17.0892s. Nootherdischargepathcredited. Worstperresistor90Vpower=.122455W;JSON givesexact. Dischargecalculationdoesnotcoversimultaneousbleederfailuresanddoesnotauthorizehotinsertion. Verifydeenergizedanddischargedbeforehandling.

ForcaprippleuseactualESR/currentsharingand100Hzmodulation. Threeidenticalnominalpartsdo notguaranteeexactone-thirdripplecurrent. Fulltriangle.304AisausefulnormalcoilRMSscreen,not aqualifiedcapacitorripplelimit; do notapplytheold150µFpart's1.4Aratingtothreenew47µFparts.

## Planninglossandthermalgates

Theold.9–1.7Wbase-lossestimateisnotautomaticallytransferabletothenewmagnetic/filter/caps. Forplanningonly,use1–2Wtotalbaselossincludingbleeders:at60Vthisgives9.006..10.006Winputand80.01..88.90%LED-to-inputefficiency. At207VACandassumedPF.90,theupperpointis53.71mARMS. NoPF,efficiency,absolutecomponenttemperatureorlifetimepredictionisqualified.

Proposedstop/reviewthresholds:coilbody90°Candlocalair50°C(MYRRAmaxambient);COUTcan85°C,target75°C;U1SOURCE100°CwithconditionalTjtarget120°C;D1case100°C;resistorbodies100°C. Actualdatasheetderatingsmayrequirelowerlimits. No use ofpublishedU1thetaJA80/100K/Wunlessmatching232/645mm²2oztestcopper;our1ozboarddoesnotmatchthoseconditions. Maintainthermalandclearancespacefromcoil/R7/fusibleresistor tocapacitors;domeventandmechanicalcansarenotinsulationbarriers.

## Implementationdecision

MYRRAofferspositiveall-TMEsourcingandnormaloperationpaperheadroom,enoughtoproceedwithanexplicitexperimentalPCBproposal. It doesnotclosephysicalhot/current/OVP/fault/surge/EMCqualification. Preservealltheseownedgates innewTMEvariant,donotmarkmanufacturing/safetyreleasePASS. TheoldSC09ROUTE05approvaldoesnottransferautomaticallytothisnewpartmap.


## Exact magnetic CAD handoff and late input-resistor change

Manufacturer drawing saved `74089-Datasheet.pdf` and `74089-Datasheet.png`, visually inspected. Source https://myrra.com/wp-content/uploads/2017/09/Datasheet-74087-74088-74089-rev-A.pdf . Body21×21×22mm; two rows15.24±.5mm apart, pitch3.81±.3mm, four pitches15.24mm; recommended drill1.2mm. Drawing bottom view: pins1..5 onleft bottomtotop,6..10 onright toptobottom. Pin3REMOVED. Pin8unwoundbutphysical,explicitNC. Primary4–5;NC1,2,6,7,8,9,10. Useall9physicalpads; no fabricatedpad3. Rows must not be mirrored incorrectly when translating bottom-view drawing to top-view footprint. Winding topology: primary4dot/drain to5E,86turns;aux2dot to1,12turns;S1pin6dot to7,5turns;S2pin9dot to10,5turns. Maxambient50°C. Extra22mmheight+board+bottomcomponents must be declared honestly.

Root's late proposed change: separate mains fuse and150Ω3W input resistor, both C1/C4=150nF. Input resistor normal0.54W at60mARMS,0.4327W at53.71mA; this is materially more than10Ωbaseline0.036W. The provisional1–2Wtotalbaselossrange therefore needs actualupdatedbudget rather than being silently called proven. IdealRC nominalscreen withsumC=.3µF givesstoredenergy19.20mJ at253VACcrest andinitial357.8/150=2.385A; it doesNOT establishRLCpeak/damping, fuseI²t, resistorpulseorMOVfaultcoordination. Exactresistor tolerance/hotderating andseparatefuseinterrupt/rating must becheckedbyprotectionowner.


## Final C1 correction after independent review

Final C1 is150nF630V KEMETR71PF315050H6K, sameMPN asC4. The interim47nF400VR66 was rejected: ideal linear Pi-network calculation gave454.29V atC1 itself. With both150nF630V, the same corner screen givesC1peak406.92V, filteredbus407.61V andL1peak1.398A. This removes the known400Vpart-selection concern; it does not qualify the nonlinear transient, fault or surge envelope. L1typical.3A saturation screen is exceeded, so these calculated voltage/current figures are flags, not guaranteed bounds. Input capacitance/PF, current andstartup must be measured. Nominal inputCsum300nF,19.2027mJ at253VACcrest, max21.123mJ with10%capacitance tolerance.
