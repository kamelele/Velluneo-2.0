from pathlib import Path
import json,math,hashlib,shutil
W=Path(__file__).resolve().parent;P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'supplier-review-13';M=D/'mechanics';M.mkdir(exist_ok=True)
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
sources=[('S1','TDK EFD25/13/9 October2022, pp3-4','https://www.tdk-electronics.tdk.com/inf/80/db/fer/efd_25_13_9.pdf'),('S2','ST DS14533 Rev1, pp9-10','https://www.st.com/resource/en/datasheet/stf2n80k5.pdf'),('S3','Vishay88769, p3','https://www.vishay.com/docs/88769/w005g.pdf'),('S4','Vishay28730, AC05 dimensional drawing p10','https://wwwlegacy.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf'),('S5','Rubycon BXW dimensional drawing and450V15uF entry','https://www.rubycon.co.jp/wp-content/uploads/catalog-aluminum/BXW.pdf'),('S6','Rubycon application precautions, vent andmounting','https://www.rubycon.co.jp/wp-content/uploads/catalog/al-cautions.pdf'),('S7','SCHURTER UMT-H, p2 dimensions','https://www.schurter.com/en/datasheet/typ_UMT-H.pdf'),('S8','Panasonic ZA technicaldata, ZA18/p19','https://industrial.panasonic.com/content/data/CP/PDF/ABA0000PE428.pdf'),('S9','ST AN5088, genericpowerpackagehandling1.4.1','https://www.st.com/resource/en/application_note/an5088-rectifiers-thermal-management-handling-and-mounting-recommendations-stmicroelectronics.pdf'),('S10','Furukawa TEX-E referencewiredata','https://www.furukawaelectric.com/tex-e/en/product/texe_series.html'),('S11','JLCPCB viacoveringprocess','https://jlcpcb.com/help/article/pcb-via-covering'),('S12','JLCPCB generalcapabilities','https://jlcpcb.com/capabilities/pcb-capabilities')]
put(M/'sources.json',[dict(id=i,title=t,url=u,reviewed_on='2026-11-20',evidence='Manufacturer document/publicreference, not exact-order supplierconfirmation')for i,t,u in sources])
pcb_min,pcb_max=1.44,1.76;rc=.75+.70/2;development=3.8+math.pi*rc+(5.13-2*rc)+.30+pcb_max+.50
parts=[dict(ref='T1',MPN='Custom EFD25; former B66422W1010D001',source='S1',documented=dict(raw_former_height_max_mm=12.9,pin_length_mm=[3.3,3.7],pin_square_nominal_mm=.6,recommended_finished_PTH_mm=[1.3,1.4],pin_pitch_mm=5,row_spacing_mm=22.5),requested=dict(complete_body_max_mm=[30,30,18],courtyard_mm=[30.5,30.5],mounting='flush; no blanket2mm spacer',finished_PTH_target_mm=1.35),status='Raw formerdimensionsdocument-verified; complete wound/core/yoke/termination bodyrequiresbuilderdrawingandfirstarticle'),dict(ref='Q1',MPN='STF2N80K5',source='S2',documented=dict(body_width_mm=[10,10.4],body_thickness_mm=[4.4,4.6],body_height_mm=[15.9,16.4],overall_length_mm=[28.6,30.6],lead_width_max_mm=1,lead_thickness_max_mm=.7,widened_root_max_mm=3.6,inferred_conservative_free_lead_mm=12.2),requested=dict(usable_lead_incoming_min_mm=13.0,root_straight_mm=[3.7,3.8],inside_bend_radius_mm=[.70,.75],neutral_radius_max_mm=rc,stagger_mm=[5.03,5.13],board_above_straight_mm=[.20,.30],below_board_tail_mm=[.40,.50],worst_developed_middle_lead_mm=development,conditional_length_reserve_mm=13-development,installed_height_reservation_mm=23.0,finished_PTH_target_mm=1.5),status='Sourcebody/section verified; proposedQ13-FORM-Aneedsqualifiedjig/incomingselection/formeddrawing/firstarticle.13.0mmisNOTguaranteedbyST.'),dict(ref='BR1',MPN='W10G-E4/51',source='S3',documented=dict(body_diameter_mm=[8.84,9.86],body_height_mm=[4.1,5.6],lead_diameter_mm=[.71,.81],raw_lead_length_min_mm=25.4,raw_pitch_mm=[4.6,5.6]),requested=dict(pattern_mm=[5.5,5.5],pattern_error_per_axis_max_mm=.05,body_standoff_mm=[3,4],installed_height_max_mm=9.6,finished_PTH_target_mm=1.2),status='Documentdimensionsverified; jig/polarity/nonstrainedfitrequireassemblerfirstarticle.'),dict(ref='R1',MPN='AC05000004709JAC00',source='S4',documented=dict(body_length_max_mm=18,body_diameter_max_mm=7.5,lead_diameter_mm=[.77,.83]),requested=dict(formed_pitch_mm=25.4,body_bottom_standoff_mm=[5,5.5],body_axis_height_mm=[8.75,9.25],installed_body_top_max_mm=13,inside_bend_radius_proposal_mm=[1,1.1],root_support=True,finished_PTH_target_mm=1.1),status='Sourcebodyverified; selectedMPNdoesnotguaranteefactory25.4form. Suppliermustverifyusablelead/formdrawing; noMPNsubstitution.'),dict(ref='C1',MPN='450BXW15MEFR10X20',source='S5/S6',documented=dict(body_diameter_max_mm=10.5,body_length_max_mm=22,pitch_mm=[4.5,5.5],lead_diameter_nominal_mm=.6,vent_free_space_min_mm=2),requested=dict(PCB_pitch_mm=5,body_standoff_mm=[0,.5],installed_body_max_mm=22.5,vent_service_height_from_Bface_mm=24.5,finished_PTH_target_mm=1),status='Documentarymaximaandventrequirementverified; suppliermustalignleadswithoutcase/rootstress; noPETsleeveisolationcredit.'),dict(ref='F1',MPN='3403.0268.23',source='S7',documented=dict(technology='SMD, noinsertionleads',body_length_nominal_mm=15.4,body_square_nominal_mm=5.35,pad_mm=[3.75,5.6],pad_centre_pitch_mm=13.75),requested=dict(height_allocation_mm=6.0,assembly='SMD/reflow; verifyheightfromexactSTEP/terminationdatum'),status='CorrectnativeSMDmountverified. OlderRENDER12fictitiousfuseleadsarenotmanufacturingbasis.'),dict(ref='C4',MPN='EEHZA1J100P',source='S8',documented=dict(technology='SMD',body_diameter_max_mm=6.8,base_max_mm=[6.8,6.8],height_max_mm=6.1,terminal_overall_max_mm=7.8),requested=dict(assembly='Polarity,reflow,landmatching; noleadforming'),status='Documentmaximaverified; landprocessrequiresassemblerconfirmation.')]
put(M/'component-interfaces.json',dict(units='mm',PCB_nominal_mm=[45,60,1.6],PCB_thickness_requested_mm=[pcb_min,pcb_max],parts=parts,overall_physical_height_bound_mm=23+pcb_max+22.5,overall_with_C1_vent_service_bound_mm=23+pcb_max+24.5,envelope_status='Conditional interface bounds for supplierreview; not measuredfinishedassembly, enclosurefit or thermalqualification.'))
put(M/'assembly-calculations.json',dict(Q1_FORM_A=dict(developed_max_mm=development,raw_usable_incoming_request_mm=13,reserve_mm=13-development,installed_body_top_max_mm=16.4+3.8+2*rc+.3,source_min_inferred_mm=12.2,source_min_shortfall_against_proposed_max_mm=development-12.2,assumptions='Root3.7..3.8 beyond3.6maxwidenedsection;insideR.70...75,rectangularthickness<=.70,offset5.08±.05;PCB1.6±10%;above.2...3,tail.4...5. Suppliermustqualifyneutralaxis/bendmethod andactualusablelengthfromdrawndatum.'),T1=dict(pin_diagonal_nominal_mm=.6*math.sqrt(2),radial_insertion_budget_before_pin_position_limits_mm=(1.3-.6*math.sqrt(2))/2,flush_pin_tail_below_board_mm=[3.3-pcb_max,3.7-pcb_min],with_rejected_2mm_spacer_tail_mm=[3.3-pcb_max-2,3.7-pcb_min-2],source_full_pattern_tolerances_missing=True),proposed_fabrication_tolerance_budget=dict(finished_component_hole_plus_minus_mm=.05,copper_land_diameter_plus_minus_mm=.025,hole_land_registration_max_mm=.025),conditional_component_annulus_min_mm={r:(land-.025-hole-.05)/2-.025 for r,land,hole in [('T1',2,1.35),('Q1',2.25,1.5),('BR1',2,1.2),('R1',2.2,1.1),('C1',2,1)]},via_nominal_ring_mm=.2,via_finished_ring_status='Nominaldesignpreference only; filledviafinishedring/tolerances requireprocess-specificsupplierconfirmation. ComponentPTHtolerancebudgetisnotavendorqualifiedviaprocess.',scope='Calculated proposedacceptanceconstraints, notphysicalmeasurementormanufacturingcapability.'))
shutil.copyfile(P/'design-closure-02/transformer/construction-contract.json',M/'T1-winding-build-reference.json')
(M/'ASSEMBLY-AND-ISOLATION-REVIEW.md').write_text('''# RFQ13 engineering review - scope and disposition

The documentary dimensional and current-CAD engineering review is complete for a
manufacturer enquiry. Finished parts/assembly and safety acceptance are not claimed.
The exact package dimensions, conditional interfaces and calculations are in the
adjacent JSON and dimensioned PDF. Sources S1-S12 identify official manufacturer data.

T1 raw-courtyard mismatch is corrected: a complete30x30mm body reservation and30.5mm
courtyard replace the raw-only reservation. R10 moves0.5mmleft; C3 moves1.5mmleft;
R17 moves0.35mmright/0.4mmdown; the AUX_RAW corner moves0.6mmdown. Values/MPNs,
81physicalpins, measurementcopper and separate returnbranches are retained. Native
ERC/DRC/parity passes. P/S projected coppergap is at least10.725mm; retaining the
previously proposed0.35mmfinishedgrowth budget per domain leaves10.025mm. This closes
the earlier arithmetic shortfall under that explicitbudget; suppliers must confirm
actual tolerances/fillets. These are engineering screens, not invented IEC minima.

The3mm HV/quiet screen is a common-copper-layer rule. STARTUP_MID/VDD overlaps in
projection on different primary-domain layers: record functional solid-dielectric/
coupling review against actual pressed laminate, not a nonexistent all-layer3mmgap.
The source-bound native audit separately checks all-layer P/S projection. No unrelated
B.Cu copper lies beneath C1's10.5mmcase circle; retain2mmventspace beyonditsbodytop.

OPEN FOR SUPPLIER RESPONSE, NOT HIDDEN: exact finishedT1core/yoke/secondaryexitsection,
recognized insulation/material/processbasis, fullpinpattern and insertiontolerances;
Q1incoming13mmscreen/formingjig/firstarticle; BR1/R1supportedforming, C1strainfreefit;
actualPCBhole/registration/filledcap/laminate/film capability. PhysicallypresentNC
T1.3 staysprimary;7/8/9 staysecondary, allunwoundwithout hiddenjunctions. Core/yokes
are treatedprimary. IntactTIWmustcontinueintocontrolledterminalzones; baresecondary
wire cannotcrossprimary/core/yoke regions. Unspecifiedresin, ordinaryenamel, soldermask
and PETsleeves receive no reinforced-insulation credit. Buildermustreturn qualified
materials/sections and agree testingbasis; no testvoltage/duration is invented.

No blanketT1spacer:3.5±0.2mmpins with1.44..1.76mmPCBleave1.54..2.26mmtails flush;
2mmspacer canleave−0.46..+0.26mm. F1isSMDanddoesnotbelongamong25insertionholes.
Oldappearancefuseleads andnominalR1boxarenotconstructiondrawings. Housing retention,
finishedlampthermal/startup/fault/insulationqualification and energizedtestfacilities
remain outside a bare-board request. Existing parentcriteria remain unchanged/open.

The supplier may respond with a dimensioned redline or declare a requirement infeasible.
No substitution, relaxedspacing, terminalreassignment or fabricationstarts without
exact-file review and actual authorization. The current enquiry drafts are UNSENT.
''',encoding='utf-8')
(D/'fabrication/FABRICATION-NOTES.txt').write_text('''VELLUNEO RFQ13 - DFM AND QUOTATION ONLY; NOT PRODUCTION AUTHORIZATION

One45.000x60.000mm rectangular rigidPCB,4copperlayers F/In1/In2/B. Requestnamed
JLC04161H-7628 construction,nominal1.6mm,FR4Tg155,outer35um/inner15.2um,ENIG,
greenmask/whitelegend. Suppliermustconfirmactualmaterial/CTI/RTI and minimumpressed
dielectrics; nominalthickness1.6±10% is requested, not confirmed. Noimpedancetarget.

17designated mechanicallydrilled THROUGH vias: artworkland0.700mm,Excellonhole0.300mm,
nonconductiveepoxyfilled/coppercappedbothends,ENIGexposedcaps. Noordinarytenting/mask
plugging substitution. Suppliermuststateactualpredrill/finishedholedimensions,
registration/annularring/capplanarity/copperthickness andfilledviaqualification.
The0.200mmviaannulusisNOMINALdesigngeometry, notaguaranteedfinishedminimum.

25COMPONENT insertionholes MUSTremainopen;42PTHtotal,0NPTH,noslots/mountingholes.
ComponentExcellonvalues are requested FINISHED plated-hole targets, with supplier
predrill compensation: T1tenholes1.350mm,desired1.300..1.400mm;Q1three1.500;
BR1four1.200;R1two1.100;C1two1.000;J1/J2four1.600. Proposed±.050componenthole
tolerance and≤.025hole/landregistration requireexplicitcapabilityconfirmation.
Reportactualguaranteedlimits ifunavailable; doNOTmakeunapprovedchanges. F1andC4areSMD.

Commonorigin native(77.5,130)mm,outputXright/Yup. Gerber6decimalmm,Excellon3decimalmm;
coordinatequantization≤.0005mmperaxis.45x60outlineisroutecentreline,notstrokebounds.
9Gerberlayers+separatePTH/emptyNPTH+IPC-D-356supplied. Bare-boarde-test only.

Keepalllayers/finishedmetalclearofprotectedband nativeY82.900..92.135mm acrosswidth.
Noadditionalcopper/thieving/tooling/order-number/identificationmarks inthatregion.
SourcecopperP/Sminimum10.725mm andproposed.35mm/domainfinishedgrowthbudget are
customerengineeringconditions, not a standards certification. No slots maybesilently
added toclaimairgap. Exactproductionfilms/DFMredlines mustreturnforbuyerreview.

Quotationquantity5bareboards;noPCBAorstencilorder. Supplytraceableprocess/material
description,cost/leadtime andproductionfilmreviewoption. Thisrequestdoesnotapprove
manufacturing/payment,finishedtransformer/assembly or energizedtests.
''',encoding='utf-8')
(D/'supplier/PCB-ENQUIRY-UNSENT.txt').write_text('''Subject: DFM / quote only - Velluneo RFQ13,45x60mm4-layer,17filled/cappedvias

Please review Velluneo_RFQ13_BarePCB_DFM.zip against its manifest SHA256 and return
DFM findings plus a quote for5bare boards. This is a technical enquiry only.

Requested construction:JLC04161H-7628,nominal1.6mm,FR4Tg155,35umouter/15.2uminner,
ENIG,greenmask/whitelegend. Please identify actual laminate/CTI/RTI and minimumpressed
dielectrics. Confirm17specified0.700land/0.300Excellonthrough-vias receiveepoxyfill,
coppercaps andexposedENIG; leave25componentholesopen. Confirmfinishedcomponenthole
limits, especiallyT1Ø1.35 target/Ø1.30..1.40 acceptance, trueposition/registration and
annularring/capplanarity/mask/legend tolerances. Explain toolsize/finishedhole definitions.

Reviewexact9Gerberlayers,42PTH/0NPTH,45x60routecentreline andcommonorigin against
suppliedmaps/IPC-D-356. Noaddedmarks/tooling/copperinprotectedband. Returnguaranteed
processlimits, anyredline/substitution, actualproductionfilms beforefabrication,
cost/leadtime anddeliveryoptions. NoPCBA/stencil;noorder/payment/productionauthorization.

AttachmentsetsandSHA256are listedin RFQ13-manifest.json. Please respondbyquestionID
in supplier-response-checklist.csv. We will review infeasibility/redlines explicitly.
''',encoding='utf-8')
(D/'supplier/TRANSFORMER-ASSEMBLY-ENQUIRY-UNSENT.txt').write_text('''Subject: Construction / forming feasibility and quote only - Velluneo RFQ13

Please review the dimensioned RFQ13 drawing and interface/build-reference records.
We need a qualified builder's finishedT1drawing/STEP and forming/assemblyprocess proposal,
not merely a rawbobbin model. T1maximumcompletebody30x30x18mm,flushmount,all10pins5mm
pitch/22.5mmrows. P120turns1(dot)->5;A22turns2(dot)->4;S30turns6(dot)->10.
Pins3/7/8/9remainunwound;nohiddenjunction. ProposedLp2.304mH±10%,effectivePSleakage
≤20uH are RFQtargets;returnmeasurementmethods/frequency/amplitude/temperature/fixture.
Referencecorepair/former/yokes/materials/windingsequence are in T1-winding-build-reference.

Returntolerancedfinishedshape,fullpinpattern/clocking/coplanarity andinsertionassessment,
sections ofcore/yokes/primarypockets/intactTIWsecondaryexits/strippedjointzones and
insulationmaterials/EIS applicability. Noreinforcedcreditforordinarymask/enamel/resin.
Proposequalifiedpreparation/solder/testprocedures andactualtestbasis;do not transplant
wire-onlytemperaturetestsontobobbin. Identify anyinfeasibleinterface or neededredline.

ForQ1STF2N80K5quote Q13-FORM-A onlyif incomingusablelead≥13.0mm canbescreenedfromthe
drawndatum;this isnot STguaranteedmin. Worstproposeddevelopment12.7458mm includesPCB
1.6±10%,root3.7..3.8,insideR.70...75,5.08±.05offset,above.20...30,tail.40...50mm.
Returnformingjig/drawing/lotyield/installedheight≤23andfirstarticlefit evidence. No
forcedinsertion/lateralrootstress/rebending. BR1needscontrolled5.5mmpattern/polarity;
R1needsP25.4 andbodybottom5..5.5mmclearance;do notsubstitutefactory-formedMPNsilently.
C1max10.5x22mmrequiresstrainfreeP5fitand≥2mmventclearance;F1/C4areSMD.

Quoteprototypeconstruction/firstarticle/inspection separately. Return actual guarantees,
sampledrawing/measurements andunresolvedconditions. This enquirydoesnotauthorizeassembly,
production/payment or energizedtests. Pleaseuse supplier-response-checklist.csv IDs.
''',encoding='utf-8')
questions=[('PCB-01','PCB fabricator','Exactstack/laminate/CTI/RTI/minimumpresseddielectrics','Namedstacknominal1.6;returnactualguarantees'),('PCB-02','PCB fabricator','17specifiedfilled/cappedvias;25opencomponentholes','Confirmvia mapandnocap/fillcomponentholes'),('PCB-03','PCB fabricator','Finishedcomponenthole/trueposition/registrationlimits','T1target1.35,desired1.30..1.40;explicitpredrillcompensation'),('PCB-04','PCB fabricator','Finishedring/cap/mask/legendtolerances;DFMfilms','Exact-filefilm/redlineandnoaddedmetal/marksintheband'),('PCB-05','PCB fabricator','Quote5bareboards,e-test,cost/leadtime','NoorderorPCBAauthorization'),('T1-01','Transformer builder','Finished30x30x18/STEP/full10pinpattern','Builderdrawingandfirstarticle,notrawformerorappearance'),('T1-02','Transformer builder','Core/yoke/secondaryexitall-pathisolation','Sections/materialfunctions/procedures/testbasis'),('T1-03','Transformer builder','Turns/polarity/Lp/leakage/DCR/testmethods','Identifyactualguarantees and agreedconditions'),('ASM-01','Forming/assembly provider','Q13-FORM-Aincoming13.0mm/jig/height/fit','Returnqualifyingdrawing/yield/firstarticle;notSTguarantee'),('ASM-02','Forming/assembly provider','BR1/R1form/polarity/standoffs/tails/fillets','NoMPNsubstitutionorforcedinsertion'),('ASM-03','Assembly provider','C1vent/strainfreefit;F1/C4SMDprocess','≥2mmventspace,sourcepolarity/reflow,actualheightreview'),('REL-01','Qualified reviewer/buyer','Acceptexactredlines/films/firstarticle andtestbasis','Separateapprovalbeforeproduction/assembly/energization')]
import csv
with(D/'supplier/supplier-response-checklist.csv').open('w',newline='',encoding='utf-8')as f:
 w=csv.writer(f);w.writerow(['Question_ID','Owner','Required_response','Acceptance_evidence','Supplier_response','Evidence_reference','Review_status']);w.writerows([list(x)+['','','PENDING']for x in questions])
put(D/'review-status.json',dict(engineering_review_for_inquiry='completed subject to independentfinalreview',manufacturer_contact=False,ready_for_enquiry=False,order_ready=False,finished_dimension_physical_confirmation=False,finished_isolation_qualified=False,open_supplier_response_ids=[q[0]for q in questions],scope='Documentation/CAD andconditionalconstructionreview; supplier/physicalevidence notinvented.'))
print('Documented7componentinterfaces, proposedformingbounds,12supplierresponseitems; draftsUNSENT.')
