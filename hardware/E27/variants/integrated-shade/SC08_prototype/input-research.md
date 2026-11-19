# SC08 input research: concrete minimum-change prototype proposal

Author: /root/review_completeness. Root owns project integration. Read-only SC07 source; only work/sc08-input-research written. No CAD, approved intent, order or physical test changed/performed. This proposes a bounded prototype investigation, not IEC/EN compliance or complete electrical acceptance.

## Proposed exact parts/topology

1. Remove RFC1010B-106KE input L1 and parallel RC1206FR-074K7L R1. Join RECT_PLUS/BUS_PLUS as one post-bridge input reservoir. This removes the problematic input inductor rather than attempting to certify its deeply saturated1A behavior. It also removes that LC resonance; EMC remains to test.
2. Use TWO TE Connectivity FWFU2W220RJ (6-2176792-5),220ohm2W5% fusible wirewound, in series before the bridge:440ohm total. Existing part plus one addition. Manufacturer primary page gives±400ppm/K; distributor±300ppm is not used. Each body16x5.5mm. Actual pulse/fusing curve and thermal mounting still required.
3. Keep MB10S-13 bridge and the current100nF2kV R76UR31004030J plus330nF1kV R76QR3330SE30J, now parallel at the post-bridge reservoir:430nF total. Declare effective Cin minimum387nF and maximum473nF as conservative overall design bounds to substantiate using capacitance tolerance/temperature/aging or incoming qualification. They are not automatically guaranteed just from nominal labels.
4. Replace ProTek5KP400A with Vishay **1.5KE440A-E3/54**:376Vstand-off;418..462Vbreakdown;602Vmaximumclamp at2.5A25C10/1000; maximum VBR temperature coefficient0.110%/K. Commercial grade, axial1.5KE body about9.5x5.3mm; exact package/lead-forming review still required. Do not interchange manufacturer voltage conventions.
5. Add **STMicroelectronics STTH110A** SMA blocking diode:anodeBUS_PLUS,cathodeU1DRAIN.1000V,1A,75nsmaximumreverse-recoveryat25Cspecifiedtest;175Cmax. Its role is the manufacturer-recommended remedy for reverse DRAIN current in high-L/low-C buck startup/turnoff. Actual cold/hot reverse recovery and transient VDS still require correlation; this does not magically establish a0.7A current bound.

Net component count is unchanged if one RF and one blocking diode replace L1/R1; TVS replaces existing D3. No MOV selected:275VAC MOV clamp alone does not establish700Vswitch protection. Existing two film capacitors remain large; no enclosure claim.

## Executed screens

input_screen.py was actually run. input-results.json contains complete parameters/equations/results. No SPICE/PIXls claim: normal-operation model is the existing own sample/hold/controller calculation coupled to an averaged scalar RC input and actual load. Surge is a scalar RC+piecewise-linearTVS RK4 model with half-step refinement. The analytical no-TVS RC comparison below is stronger than relying on that assumed TVS model.

RFpair minimum=396.264ohm using both−5%and−5.2%TCRreserve at155C. Maximum486.024ohm. This resistance corner is conservative;155Cisnotanallowed continuous operating temperature for2Wpower. Set a prototype localambient/body budget and check derating separately.

**Peak-line connection, initially empty input capacitor, noTVS conduction:**
- VP=253sqrt(2)=357.796V;Cmax473nF.
- Ipeak<=0.902923A;RCtime187.433us.
- TotalRFenergy0.0302763J;equal split0.0151381Jeach. Mixed high/lowindividual energy bound0.0166782J.
- Bridge pulse integral I²t=7.64043e−5A²s. MB10Sspecification3.74A²s is only1..8.3ms, so do NOT claim this subms pulse is formally qualified by that number.30A/8.3ms rating likewise only a comparison, not our waveform/hot test.

**Illustrative normal model with440ohm nominal, Cin430nF,Cout120uF,Rsense28.7ohm,3mH,CFB22uF,25Ccontroller parameters:**

This uses the priorSC07-Cpowercore seed. Root subsequently proposes two22uFX7Rsampleholdcapacitors andPMOSdrive forSC08-A; those changes were not included in this normal-current run. Rerun actualSC08settings before transferring these averages as a SC08prediction. Passive RC/surge and source-energy inequalities do not depend on the samplehold controller model.
- 207/230/253VAC:LEDaverage53.157/54.087/54.446mA;COUTpeak110.440/110.767/110.825V.
- RFpairloss1.818/1.797/1.804W, about0.90Weach;bridgeRMS64.27/63.90/64.03mA.
- At207V with pairRmax486.024ohm:pairloss2.017W,about1.009Weach;LEDaverage53.041mA.
- Nominal230V1s/2s run changesRFpairloss1.79678→1.79646W andLED54.0870→54.0883mA.
- This excludes real switching-current shape, diode recovery, losses, temperature-dependent controller/currentlimits, ripple ESR, auto-restart and OVP. It establishes a credible~1Weach thermal burden, not final power/temperature/flicker limits. Source charging uses per-cycle averaged drain charge; do not call it the exact bridge HF RMS.

**Nominal1kV single differential voltage-pulse study:**Vs=357.796+1000*f(t), f normalized exp(−14600t)−exp(−2470000t);2ohmgenerator series included. Initialbus357.796V. Tj is fixed model input, no TVS self-heating.
- WithRpairmin396.264,Cmax473nF,at125CassumedTVS:BUSmax538.151V,TVSmax0.4075A,219.3Wpeak,0.01591J. PairRFenergy0.05915J,sourceI²t1.49258e−4A²s.25CcaseTVS0.7344A/369.5W/0.03118J.
- Source/bridgepeak2.489A;fromemptyCin3.378A andpairRFenergy0.14207J. Half-step25ns reproduces50nspeakwithin0.1microvolt in this ideal scalar model, which does not imply physical accuracy.
- At2kV:125CmodelBUS617.936V,TVS1.691A/1045W/0.09637J,RFpair0.25380J. This attractive nominal result is NOT a2kVqualification: plateau uppercurrent4.895A exceeds the2.5Aclamp specification, and energy/tolerance/temperature/repetition/overshoot are not closed.

## Independent RC voltage bound: does not require hotTVSclamp

Specify a single positive differential test-voltage excess bounded by1100V for at most3us, then1100*exp(−t/(60us/ln2)). This is an explicit engineering upper-envelope proposal, NOT an assertion that every IECgenerator must meet it; characterize the actual generator waveform, overshoot and source network. It includes margin over nominal1kV/50us but no standard edition/applicability claim.

WithRpair>=396.264ohm,Cin>=387nF,initialBUS<=357.796V and no energy backfeed through the blocking diode, the scalar RC response, EVEN WITH TVS OMITTED/OPEN, is at most**663.946917V**. Load and conductingTVS can only decrease that ideal RC state. Derivation:after the3uspeak, x(t)=x0 exp(−t/RC)+A*tau/(tau−RC)*(exp(−t/tau)−exp(−t/RC)),x0=A(1−exp(−3us/RC));peakwhenx=Aexp(−t/tau),at110.711usafterfront. Bridge blocks after peak, so the capacitor holds rather than discharges; the maximum is unchanged.

Reserve an additional5V for SOURCE belowDCreturn, producing668.947V before layout overshoot. This5V is a proposed measured acceptance budget, not a proved semiconductor envelope. Recommend prototype pass targetVDS<=680Vincluding ringing, giving20Vto700Vabsolute rating; require no measurable reverseDRAIN conduction beyond characterized recovery/leakage. Include probe uncertainty in this target; define actual acceptance with the qualified reviewer.

At2200Vsameenvelope, openTVSBUSbound970.098V: clear FAIL for700Vcontroller. Do not claim2kV fromthe1kVproposal. If2kVbecomesmandatory, redesignclamp/resistor/capacitor/driverbeforeassertingpass. LNK3294G-TL/LNK3296G-TL900V is a real manufacturer-supported alternative withSIMPLISmodel, butCVcontrolisnotdrop-inCC; newfeedbackandintentrequired.

## Whole-pulse output energy bound

For all input current i through RFpair, portpowerafterRF=vs*i−R*i²<=vs²/(4R). Normal sine envelope gives80.7656W. This is a valid waveform-independent input-power ceiling; it is not converter Ipk ceiling.

A normalized double-exponential1kVpulse contributes whole-pulse excessenergy0.0547103J above the normal-power bound. Count the WHOLE excess even if part precedes OVP trip: this covers extraCinprecharge without separately doublecountinghotCin. Add normalCinenergy0.0302763J and residualLoutenergy.003234J forIMPOSED1.4Aand3.3mH. StartingCOUT131V,Cmin120uF,delay0.6ms gives139.4238V. At2ms it becomes146.0258V.2kV/0.6ms gives145.2992V.

Using the moreconservative1100V/3us/60us envelope adds0.0798069J;COUTbound140.9158V at0.6ms.2200Vversion149.5495V. All conditional on timing, voltage-at-trip and current acceptance inputs.1.4Aabsolute drain current rating is NOT a guaranteed inductor current limiter. Redesign/prototypeverify the required current/turnoff bound. Raising original135Vfault requirementto145Vneeds an explicit new engineering decision and recalculatedreconnect/pulse/discharge/loadlimits; these calculations do not authorize that change.

## Practical pre-order/prototype evidence boundary

A board-only, current-limited engineering prototype can be proposed around these exact parts after new map approval and reviewer-defined limits; this is not production/mains-test authorization. Close static arithmetic now, retain real test evidence as real tests.

Required conditions/test plan before claiming operational qualification:
- EstablishCin387..473nF over acceptedtemperature/aging and verifyRFminimum/drift/mounting. Sourceofmissingfullpartpulse/fusingdata remains explicit.
- Define exact1kVdifferentialtest,generatorcalibration/source2ohm,tolerances,phase,polarity,numberofpulses/repetition,and localpreheat.0/90/180/270degree energization, cold−20C and representative hotboard; componenttemperatures within ratings.
- MeasureRFnormalRMS/bodytemp,bridgecurrent,STTH110Atemperature/reversecurrent,U1VDS/SOURCEmin,TVSvoltage/current and COUT. AdoptVDS680Vengineeringtarget,normalCOUT123V and explicitly decidedfaultlimit; captureprobe/bandwidth/uncertainty.
- Verify1.5KEpulsepower/thermalderating for actual current waveform and preheat using manufacturerdata/qualifiedtest; maxVBRcoef alone does not guarantee maxVC hot. Conditional602*(1+.0011*100)=668.22V at125C is a budget, not a completed proof. TVSshort/RFfusing and oneRFshort invalidate simple normal-topology proof and need their own abnormaloperation containment.
- Check localRF~1W each and fanlessboardthermalspacing; no finalenclosure inference. RemovingL1mayhurtEMC; measure before choosing laterEMIfilter. Do not reintroduce unknownsizedcoilsbefore checkingnormal/inrushpulseenergy.
- CorrelateLYTcurrentandBPshutdownlatencywithsingleactuatorfailedopen; do not inferthese from idealcurrentseed. Record actualhot/coldandfaultresults. No testsperformedhere.

## Sources and procurement identity

Primary manufacturer sources inspected2026-11-19:
- Vishay88301Rev09Aug2022 https://www.vishay.com/docs/88301/15ke.pdf (exact440Arow andorderingE3/54; maxVBRtempcoef explicit).
- STDS3067Rev4 https://www.st.com/resource/en/datasheet/stth110.pdf (STTH110ASMAordering,1000V1A75ns25C;18A8.3msSMA).
- TEexactpart https://www.te.com/en/product-6-2176792-5.html (active220R2W±400ppm; nofactorydirectavailabilitypromise).
- DiodesDS39045Rev3-2 https://www.diodes.com/datasheet/download/MB10S.pdf (MB10S-13,1000V,30A8.3ms,3.74A²s1..8.3ms;hotcapacitiveloaddereatingrequired).
- PI https://www.power.com/sites/default/files/documents/lytswitch-0_family_datasheet.pdf andAN60; blockingdiode/startupremedy.
- PI900Valternative https://www.power.com/products/linkswitch/linkswitch-tn2/lnk3296g ; notselecteddropin.

Credibleprototypeprocurementrouteswerefound, notreservedstockorplacedorders:NewarkFWFU2W220RJ46AM5433shows892stock;DigiKey1712-FWFU2W220RJCT-NDalsooffered;Vishay1.5KE440A-E3/54shownasDigiKey1.5KE440A-E3/54GICT-ND;STTH110AatLCSC C99113. Recheckbasket/localdeliveryatorder; inventoryresultsarenotmanufacturerparameterauthority.

Shell downloads failedDNS in this childenvironment, so no downloadedmanufacturerPDFhash is fabricated. PrimarywebPDFtextwas inspected. Numericalcode/results are real local artifacts.
