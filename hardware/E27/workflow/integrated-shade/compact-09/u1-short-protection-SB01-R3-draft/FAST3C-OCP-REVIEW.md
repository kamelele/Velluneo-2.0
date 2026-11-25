# FAST3C — final bounded SOIC protection variant

Frozen independent map `intended-map-fast3c-ocp.json`, SHA256`924dfe2ee331eb7d4ae4953e1c9340528d4faf287dede8c7066c328e488fd5bc`. Calculations `fast3c-calculations.json`, SHA256`d6e41016d6f0cc8240bb150b305fba27dfa96d310f1056f0ae984b62b1f7f67f`. No canonicalCAD changed by this author. Root integrates the same45positions/107pins and existingoutline; no extraattenuator/clamp/transistor is added.

## Selected final delta

U2 becomes **TLV1812DR**, realactiveSOIC8, body4.90×3.91mm,pitch1.27mm. All eight numberednetassignments remain identical:1OVP_DRIVE,2OVP_REF,3OVP_SENSE,4DC_RETURN,5OCP_FILTER,6OCP_REF,7OCP_DRIVE,8OVP_AUX5. The SOIC selection removes the earlier VSSOPpad/escape-spacing problem without a localrule waiver.

R14/R15 become **VishayTNPW1206150KBEEN**,1206,150kohm0.1%25ppm/K. The electricaldivider is unchanged; largerpackage supports the selected1mmclearance class. RequestedRT1206BRD07150KLhascorrectspecifications but DigiKeywasoutofstock, so the stockedidenticalvalue/tolerance/TCR Vishaypart is selected. Use conservative0.25Wdesignrating; catalogueheadline0.52Wrequiresmanufacturerthermalconditions.

R17 becomes **RC0805FR-071K1L**,1.1kohm. R27 becomes **RC0805FR-07100KL**,100kohm. C10 becomes **C0805C101J5GACTU**,100pF50VC0G5%. Keep R19220ohm,R181kohm,C847nF,R21/R224.7kohm,R25/R2661.9k/10k,mandatoryAC012ohmwirewoundshuntR24,and the existingC7/C9. C7effective≥70nFat5.09Vover0–110°C remains an explicit engineeringqualification. C10plusinputandlayoutcapacitance must be≤130pF; nameplate100pF alone does not prove that total.

## Primary sources and actual parts

TIprimary RevEJuly2025: https://www.ti.com/lit/ds/symlink/tlv1812.pdf , captured `TLV1812-primary.pdf`, SHA256`fe6a20ce3d711eefc8c800ed94182645f9e07c4ece03c4cb6e3e5ed3ddc49319`.

Vishayprimary Rev10April2026: https://www.vishay.com/docs/28758/tnpw_e3.pdf , captured `TNPW-primary.pdf`, SHA256`6f0508c568cb355aaf2accdd33fe3a780d3ea5ef207c4c9a71839a8acadc33a5`.

Publicindexedcatalogues verified: TLV1812DR https://www.digikey.com/en/products/detail/texas-instruments/TLV1812DR/17748400 reports4402stock,MOQ1,USD1.37;TNPW1206150KBEEN https://www.digikey.com/en/products/detail/vishay-dale/TNPW1206150KBEEN/1611307 reports182stock,MOQ1,USD0.71;C0805C101J5GACTU https://www.digikey.com/en/products/detail/kemet/C0805C101J5GACTU/411397 reports665961stock,MOQ1,USD0.19. R171.1kexactcode is verified byDigiKeymodel727455 and an indexedDigiKeysubstitutetable reporting33619stock/USD0.10; R27100k https://www.digikey.com/en/products/detail/yageo/RC0805FR-07100KL/730491 reports1116328stock,MOQ1,USD0.11. These are snapshots, not stockreservations. ExactC10manufacturerpage: https://search.kemet.com/component-documentation/download/specsheet/C0805C101J5GACTU .

## Comparator specifications and honest limits

TLV1812hasPORwithoutputLOW,2.4Vminimumsupply,±4mVfulltemperatureoffset and±1.2nAfulltemperatureinputbias. Dualquiescentcurrentmaximum10uA/channel withoutputHIGH. There is no internalhysteresis. The250mVhigh-outputdropmaximum at4mA appears in a tablewhose defaulttest supply is12V. Therefore≤250mVdrop at the actual AUX4.86–5.09V is an explicit prototypequalificationenvelope, not mislabelled as a5Vmanufacturermaximum. The typicalsource-currentgraphs support plausibility but cannot create a guaranteedbound. The same distinction applies to420nstypicalpropagation at12V: use a measured≤2uscomparatorcontribution atAUX5V in the150ustotalbudget.

TLV1812inputs have conventionalrailclamps. They are not supply-independent40Vinputs; the40Vrating is the allowed supplyrange. The absolute-ratingfootnote supports current-limitedrailoverdrive≤10mA for181x. The separate1mAsoft-clampdiscussion primarily concerns182xopen-drain versions;100kR27 is nevertheless a deliberatelyconservativechoice keeping the singlefaultinjectionbelow1mA. Do not claim the1812input accepts30VwhileAUXis5V merely because its family name says40V.

## OCP detection and ordinaryoutputshort

AC01shunt remains1.88708–2.1042ohm over0–110°C includinginitial±5%anddirectionalnegativeTCR. Retaining the conservative10mVtotalinputerrorenvelope plus actual1.2nAbias through100kandthereference network gives staticOCPtrip **317.772–382.781mA**,nominal347.705mA. The1/3attenuator proposal is NOT used;R28doesnotexist in this map.

This keeps the severe-faultdetection thresholdabove the citednormalplanningpeaks304mAideal and268.8mA20Sspecificmodel, but those models do not replace a real cold/hot/startupcurrentripplemeasurement. Measurednormalpeak must remainbelow317.772mAwithmargin. OCPdetects the U1shortcaseevenwhen intactLEDsclampbelowOVPtrip; it is not a currentregulator or LEDsurvivalguarantee.

At90VLED_RETURN_SENSEshortpulse,100kR27 limitsinputcurrent≤90/98k=0.9184mA. Combined biasplusinputinjectionmaximumapproximately10.105mA is belowLM4040's15mArecommendedcurrentrange, resolving FAST3B's17.9mAoverrangecase. Inputclampwaveform must still be verified; the currentlimit is not a guarantee of normalcomparatoroperation while itsinputisclamped. The faultfirstcrosses OCPthreshold before highinputclamping;the commonFAULT/D3latchmust retain theeventwhile thechargedC6shortpulsecontinues.

R27worsttransientpower90²/98k≈82.7mW for a submillisecond capacitorpulse;continuousnormalpowerisnegligible. ExistingordinaryC6short energy review andmandatoryAC01shunt remain applicable: allocated<0.89J versus≥2Jroomtemperaturegraphscreen and1.40Jexplicitengineeringhotreserve. This is not a hotrepetitivepulsegenericguarantee.

## Gate, filter and response

Keep C9transientcharge≤3.6nC,C7effective≥70nF,thusAUXdroop≤51.429mV. Combinedwith50mVremoteQ1cathodeoffset ONLY in thegatecalculation,0.8VORdiodeengineeringenvelope and250mVcomparatorVOHqualification gives **482.375uAminimumgatecurrent**, versus SCRcoldIGTmaximum300uA.

R171.2kwould leave only314.6uA and approximately140usgatecharging, which doesnot leave the150usresponsebudgetroom. Selected1.1kremoves that weakness. Piecewise4mAsource-loadmodel: firstchargegate0→0.3V in5.315us after deducting0.6mAsteadyfeedback/leak,0.3mAgate andworstR18current; from0.3Vupward,theload at guaranteedminimumdrive is3.808mA,below4mA. The subsequentworst-voltageRCphase takes67.540us,total **72.855us**. This is an engineeringload-line/RCmodel, not a manufacturerSCRturnontimeguarantee.

With R27max102k andtotalC10+input+layout≤130pF, maximumfiltertimeconstant **13.26us**. At450mAstep, reaching100mVoverdriverequires **45.801us**;at500mA27.212us. At435.772mA it is only theasymptotic100mVboundary, so nofinite50ns/420nsresponse isassigned there.

450mAfilter45.801us+gate72.855us+C9settling2us+measuredcomparatorallowance2us=122.656us. Remaining **27.344us** of the150usTOTALrequirement coversSCRcurrentcompletion andotherinterconnecteffects in thisconditionalmodel. The prototype must actually demonstrate≤150usovertemperature; no datasheet-onlyunconditionalproofisclaimed. TypicalCin8pFcommon/2pFdifferential values do not themselves prove the130pFtotal; measurement/qualifiedlayoutbounds are required.

## Latch, AUX and startup

R19220retained. At correlatedAUXminimum4.85857V,the latchSENSEminimum2.50039Vandreference2.43779Vgive **52.601mVmargin after10mVoffset/errorallowance**. The remoteQ1cathode50mVoffset is not incorrectly applied to thelocalcomparatorreference. Low-overdrivelatchacquisition remains part of the150ussystemmeasurement, rather than transferring a100mVtimingtest to52mV.

At52Voutput thebiasnetworkprovides4.8926mAversusconservative4.4464mAmaximumload,leaving0.4461mA. R21/R22normalbiaslossstays0.3511Wat60Vtotal. KeepC7part/value;C7effective70nFminimumand126.5nFmaximumstartupenvelopes are differentbounds for differentpurposes.

StartupmodelretainsallC4energy10.56mJinstantlyassignedtoC6minimum120uF, giving13.2665Vinitialoutput,followedbyconservative8.2Achargecurrent/68.333Vperms. Withrounded0.45mAstartupload(includingLM4040minimum),AUXcrosses **2.4Vby198.303us**. TIsection7.4.3 describesPORoutputLOW forupto200usafterthe2.4Vcrossing;theswitchingtable200usentryisTYPICAL. Impose a200usprototypequalificationbudgetfromthat2.4Vcrossing,notfromfull5Vregulation. It ends398.303us,whileearliestLED52Vturnon566.832us,leaving **168.528usmargin**. Evenconservativefull5.09Vpoint336.817usplus200usleaves30.014us,buttheintendedPORbasisisthe2.4Vcrossing. ActualPOR/startupwaveformsandnormalno-tripbehaviorrequireverification.

## Integration handoff

Applyonlythefrozencomponent/footprint/valuechanges above. PreserveallnumberednetsandR24externalLEDreturn-onlyKelvinconnection;C6negative/bleeders/converterreturnremainDC_RETURN.R23isC1damper,C9isOVPfilter. NoD5orR28isadded. Rootownsnewintentbinding,fit/routing/nativeERC/DRCandmanufacturingexports. The45position/107pinclaimbelongs to theindependentlycheckedintegratedrootmap;thistopologylistcontains22protectionpositionsplusnamedroot-ownedparts anddoesnotinventextraNCpins.

Prototypeacceptanceconditionsareexplicit:C7effective70nFminimum;totalOCPinputcapacitance130pFmaximum;comparatorVOHdrop250mVmaximumatAUX/4mA;comparatorresponse≤2us;POR≤200usafter2.4V;BAT54Cforward/leakenvelopes;remoteQ1Koffset≤50mV;totalfaultresponse≤150us;normalLEDpeakmargin;AC01hotpulse/coolingreview.Theseconditionskeeptheprojectconcreteandreviewablewithoutclaimingunperformedbenchmeasurements.
