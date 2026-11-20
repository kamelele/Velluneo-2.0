from pathlib import Path
import json,hashlib,csv,shutil
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';S=P/'supplier-review-13';D=P/'jlcpcb-quote-14';A=D/'assembly-feasibility';H=D/'support'
def put(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def txt(p,s):p.write_text(s,encoding='utf-8')
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def writecsv(p,cols,data):
 with p.open('w',encoding='utf-8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(data)
sources=[
 ('J1','https://cart.jlcpcb.com/quote','Live public quote fields, ZIP/RAR maximum100MB; actual account/upload not used.'),
 ('J2','https://jlcpcb.com/help/article/gerber-files-preparation','11/16/2026 guide: oneoutline, identified auxiliarysk selectionlayer forfilledvias; remarks must describe its usage.'),
 ('J3','https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-8','KiCadguide includespaste,innercopper,Protel,masksubtraction,DRC,Excellonmmdecimal,drillmap andindependentCAMcheck. Sharedplotdatum deliberately retained ratherthanexampleAbsolute.'),
 ('J4','https://jlcpcb.com/help/article/pcb-via-covering','Nonconductiveepoxy/coppercaps; diameter-specificselection orimage/remark; componentholes distinct. Noordinarytentingsubstitute.'),
 ('J5','https://jlcpcb.com/capabilities/pcb-capabilities','StandardPTH+0.13/-0.08mm;position±.075mm; tighter±.05hole optionlisted0.55..2mm multilayerENIGroundholes underPress-fit service. Actualregistration/minimumringneedsagreement.'),
 ('J6','https://jlcpcb.com/impedance','JLC04161H-7628nominalstack listed. Namedstackrequestdoesnotestablishminimumpressedmaterial/CTI/RTI.'),
 ('J7','https://jlcpcb.com/help/article/instructions-for-ordering','PDF/Excel/text buriedinGerberZIPmaybedisregarded. CriticalparametersmustbeformselectionsandPCBRemark.'),
 ('J8','https://jlcpcb.com/help/article/how-do-i-get-a-price-do-i-have-to-register-as-a-user','Calculatorforindicativeprice; quotationquestionssupport@jlcpcb.com withGerbersandnecessaryfiles. Noemailhasbeensent.'),
 ('J9','https://jlcpcb.com/help/article/how-to-confirm-the-production-file','Confirmproductionfile is alaterorderstage, normallyafterpayment; notapromiseoffreepreorderfilms. AskprequoteDFM separately.'),
 ('J10','https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad','BOM/CPLCSVheaderrequirements; actualpartmapping andplacementpreview requiredbeforeassemblyorder.'),
 ('J11','https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly','CPLdesignator/metricXY/TopBottom/positiveCCWrotation. Nativeexportangles retainedforquotation, notverifiedfeedercorrections.'),
 ('J12','https://jlcpcb.com/capabilities/pcb-assembly-capabilities','Two-sidedplacementStandardPCBA;minimum70x70mm;railsandfiducialsrequired. Manufacturerpanelproposalneededfor45x60mmindividualboard.'),
 ('J13','https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-parts-selection-service','Partsselection mayincura servicefeeandrequiresaccuratepackaging/MPN. No paidserviceisactivated orpriceassumedfrompublicform.')]
put(D/'jlcpcb-sources.json',dict(retrieved='2026-11-20 Europe/Warsaw',authority='Official JLCPCB public pages read in this task',sources=[dict(id=i,url=u,application=s)for i,u,s in sources],limitations='Public text inspected, not authenticated after-upload configuration or actual portal acceptance. No price, stock, account state or supplier acceptance claimed.'))
fields=[
 ('Base Material','FR-4','J1'),('Layers','4','J1'),('Dimensions','45 x 60 mm','Native source / J1'),('PCB Qty','5 finished individual boards, quotation basis','J1 / retained RFQ13 assumption'),('Product Type','Industrial/Consumer electronics','J1'),('Different Design','1','J1'),('Delivery Format','Single PCB for bare-board quote','J1'),('PCB Thickness','1.6 mm; request1.44..1.76','J1/J5'),('PCB Color','Green','J1'),('Silkscreen','White','J1'),('Surface Finish','ENIG','J1'),('Outer Copper Weight','1 oz; retain source nominal35um request','J1/J5'),('Inner Copper Weight','0.5 oz; source nominal15.2um foil construction, confirm actual','J1/J5/J6'),('Layer Stackup','JLC04161H-7628 exact named construction requested; no uncontrolled substitute','J6'),('Material Tg','FR-4 Tg155 request; actual laminate/CTI/RTI/minpressed dielectric ask support','RFQ13 / J5'),('Via Covering','Epoxy-Filled & Capped: all17 Ø0.300mmvias, selectedinSK; BOTHends; all25componentholesopen','J4'),('Min via hole size/diameter','0.30 mm hole /0.70 mm land','Native source / J1'),('Hole accuracy','Request±0.050mm on25listedcomponentholes; NOT standard+0.13/-0.08; soldered insertionholes, ask about tighter-hole service','J5'),('Hole/land registration','Request≤0.025mm; explicit nonstandard capability question, not public ±0.075position guarantee','RFQ13 / J5'),('Mark on PCB','Remove Mark / no added identifiers','J1'),('Electrical Test','Flying Probe Fully Test requested; unpowered bare-board continuity/shorts','J1'),('Gold Fingers','No','J1'),('Castellated Holes','No','J1'),('Edge Plating / V-cut / slots','None on individual bare board','Native source'),('Impedance Control','No controlled-impedance target; named stack still required','RFQ13 / J6'),('Confirm Production File','Yes, do not confirm automatically, if a later order is authorized; this is not freepreorderDFM','J9'),('PCB Assembly','OFF for bare-board quote. Separate manualStandardtwo-sidedfeasibility quote, not an immediatePCBAupload','J12'),('Stencil','OFF for standalone bare-board quote; include stencil/setup in separate assembly quotation','Owner scope')]
put(D/'quote-settings.json',dict(revision='JLC14',status='Prepared field values, not a submitted/live configured cart',form='https://cart.jlcpcb.com/quote',fields=[dict(field=a,value=b,basis=c)for a,b,c in fields],account_specific_options='If any requested option is absent/renamed/unavailable or auto-changes another field, use the manual support route and request written confirmation; do not select a weaker default.'))
remark='''JLC14: QUOTATION/DFM ONLY. 45x60mm,4L,1.6mm,ENIG; exact JLC04161H-7628 requested. Velluneo_JLC14.sk is AUXILIARY VIA-FILL SELECTION, NOT COPPER/OUTLINE: epoxy-fill and copper-cap BOTH ends of all17 marked Ø0.300mm vias only; leave25 component PTH open. T1 ten finishedholes1.350mm mustbe1.300..1.400mm; tighter±.050mm requested on all25 insertionholes (see holelist). Standard+0.13/-0.08mm is NOT accepted forT1. Quote tighter-hole service; these are soldered insertionholes, not press-fitterminals. Registration≤.025mm and all finishedring/cap limits need written capability response. Keep all copper layers free of additions in outputY37.865..47.100mm acrossX0..45; no thieving, tooling, markings or artwork changes. Confirm actual laminate/CTI/RTI and minimum pressed dielectrics. Confirm productionfiles before any separately authorized manufacture; no automatic acceptance. Critical requirements are in this remark and manual technical enquiry; attachments alone are not authorization.'''
txt(D/'PCB-REMARK-PASTE.txt',remark+'\n')
txt(D/'PCB-REMARK-SHORT.txt','''JLC14 QUOTE/DFM ONLY. Velluneo_JLC14.sk selects all17 Ø0.300mmvias for epoxyfill+coppercap BOTHends;25componentholes OPEN. T1finishedholes1.350mm REQUIRED1.300..1.400; standardPTHtoleranceNOTaccepted. ExactJLC04161H-7628. Writtenconfirmationofhole/registration/material/isolation-bandrequirementsneeded; see fulltechnicalenquiry. No automatic productionfile confirmation.\n''')
txt(H/'FABRICATION-REQUIREMENTS.txt','''JLC14 — QUOTATION AND TECHNICAL REVIEW ONLY

This handoff uses unchanged RFQ13 CAD. The Gerber ZIP is the current JLCPCB upload
archive. There is exactly one outline, Velluneo_JLC14.GKO, four copper layers in
GTL/G2L/G3L/GBL order, two mask, two legend, two paste layers, one Excellon XLN,
the auxiliary sk selection layer and the recommended human drill map. No duplicate
GM outline, native PCB, PDF, BOM or nested ZIP is inside the Gerber upload archive.
Paste files provide assembly reference; they are not an instruction to buy a stencil.

All files share the retained project plot datum: native(77.5,130)mm; outputX=x−77.5,
outputY=130−y. Boardbounds are0..45x0..60mm. The KiCad tutorial's Absolute origin
example is deliberately adapted to the same existing plot datum for BOTH Gerber and
drill (and SK/CPL), rather than mixing origins or mirroring the bottom side.

Quote five finished single45x60mm barePCBs, 4L, FR-4 nominal1.6mm±10%, Tg155 request,
ENIG, green/white, outer1oz / inner0.5oz. Request exactJLC04161H-7628 construction;
the source foil/core/prepreg numbers are nominal construction inputs, not minimum
finished-copper/dielectric guarantees. Return actual material, CTI/RTI and minimum
pressed dielectrics, finished copper, cap/ring and registration capability.

Epoxy-fill and copper-cap BOTHends of all17 Ø0.300mm throughvias markedin
Velluneo_JLC14.sk. The SK is auxiliary selection only, not an electrical copper
layer, boardoutline or extra drill operation. All25 component insertionholes remain
open. No other design hole isØ0.300mm; componenttargets are1.000..1.600mm.

Componentholes are FINISHED plated-hole targets, not uncompensated drilltool sizes.
Request±0.050mm for all25 listedholes; T1target1.350 mustbe1.300..1.400mm. Standard
JLCthroughhole+0.13/−0.08 wouldgive1.270..1.480mm and is not acceptedforT1. Please
quote the available tighter-hole service. These are soldered insertionholes, not
press-fit connector terminals. Return actual holeposition/landregistration limits;
requestedregistration≤0.025mm is not claimed supported by public±0.075mm position.
All conditional componentannulus calculations inRFQ13 require actual agreement.

Protected band acrossX0..45, outputY37.865..47.100mm, on all four copperlayers:
no addedcopper/tooling/thieving/marks. No slots or mountingholes on finishedboard.
Actual source projectedprimary/secondary coppergap≥10.725mm; proposed0.35mm/domain
finishingbudget is conditional and not a finishedinsulation qualification.

Critical requirements must be entered in PCBRemark and discussed with support;
JLC's orderingguide says extra PDF/text/Excel buried in aGerberZIP may be ignored.
Request pre-quote feasibility/DFM in writing. The later ConfirmProductionFile
service normally follows an order/payment and must not be presented as a free
pre-order film review. No production or charge is authorized by this enquiry.
''')
expected=json.loads((S/'checks/native-fabrication-input.json').read_text())['expected_drills'];component=[q for q in expected if q['kind']=='component'];assert len(component)==25
writecsv(H/'finished-component-holes.csv',['Pad','X_mm','Y_mm','Finished_target_mm','Requested_min_mm','Requested_max_mm','Process_note'],[dict(Pad=q['ref'],X_mm=f"{q['x_mm']:.6f}",Y_mm=f"{q['y_mm']:.6f}",Finished_target_mm=f"{q['diameter_mm']:.3f}",Requested_min_mm=f"{q['diameter_mm']-.05:.3f}",Requested_max_mm=f"{q['diameter_mm']+.05:.3f}",Process_note='Leave open; soldered insertion; tighter-hole service to confirm')for q in component])
stock=rows(S/'assembly-reference/BOM.csv');pos={q['Ref']:q for q in rows(H/'positions-native.csv')};assert len(stock)==len(pos)==33
held={'T1':'Custom finished transformer, builder drawing/insulation/firstarticle required','Q1':'Q13-FORM-A incoming usablelead>=13.0mm, jig/yield/firstarticle','BR1':'Controlled5.5mmsquareforming/polarity/standoff','R1':'SupportedP25.4forming/bodyclearance5.0..5.5mm','C1':'StrainfreeP5insertion/vent>=2mm','J1':'Inputwireoperation, wireconstruction/length not selected','J2':'Outputwireoperation, wireconstruction/length not selected'}
package={'F1':'UMT-H SMD','C4':'SMD hybrid electrolytic 6.3x5.8 nominal','U1':'SOT-23-6 / DBV','D1':'SMA','D2':'SMA','D3':'SMA','TVS1':'SMB','C2':'2220','C3':'2220','RT1':'0603'}
full=[];smt=[];cpl=[];allpos=[]
for q in stock:
 ref=q['Reference'];p=pos[ref];foot=package.get(ref)
 if foot is None:
  foot=next((s for s in('0603','0805','1206','2512')if s in q['Footprint']),q['Footprint'].split(':')[-1])
 row={'Comment':q['Value'],'Designator':ref,'Footprint':foot,'Quantity':1,'LCSC Part #':'','Manufacturer Part Number':q['MPN_or_custom_requirement']}
 full.append(dict(row,Quote_scope='Manual feasibility only: '+held[ref]if ref in held else'Two-sided SMT quote; exact LCSC/availability/centroid/feederangle unconfirmed'))
 coord={'Designator':ref,'Mid X':f"{float(p['PosX']):.6f}",'Mid Y':f"{float(p['PosY']):.6f}",'Rotation':f"{float(p['Rot'])%360:.6f}",'Layer':p['Side'].capitalize()}
 allpos.append(coord)
 if ref not in held:smt.append(row);cpl.append(coord)
assert len(smt)==len(cpl)==26 and {q['Designator']for q in smt}=={q['Designator']for q in cpl}
cols=['Comment','Designator','Footprint','Quantity','LCSC Part #','Manufacturer Part Number']
writecsv(A/'BOM_33_ALL_PARTS_MANUAL_QUOTE.csv',cols+['Quote_scope'],full)
writecsv(A/'BOM_26_SMT_QUOTE_REFERENCE.csv',cols,smt)
writecsv(A/'CPL_26_SMT_QUOTE_REFERENCE.csv',['Designator','Mid X','Mid Y','Rotation','Layer'],cpl)
writecsv(A/'POSITIONS_33_ENGINEERING_REFERENCE.csv',['Designator','Mid X','Mid Y','Rotation','Layer'],allpos)
writecsv(A/'MANUAL_OPERATIONS_7.csv',['Designator','Required_engineering_response'],[dict(Designator=r,Required_engineering_response=s)for r,s in held.items()])
txt(A/'READ_BEFORE_ASSEMBLY_QUOTE.txt','''JLC14 ASSEMBLY FEASIBILITY — MANUAL TECHNICAL QUOTATION ONLY

Quote 5 finished individual boards separately from bare PCB. Use full33partMPNlist
to assess sourcing/operations. OptionA:26SMTparts on BOTHsides; OptionB: additionally
assess the5THTparts and2wireoperations, each conditional on exactconstruction approval.
J1/J2 are wirepads, not a defined connector to procure. No wire type/length is invented.
F1 andC4 belong inSMT, not the5THToperations. T1 is a custom finishedtransformer,
not a stock EFD25bobbin/core that can substitute for the complete winding assembly.

The26SMT BOM and CPL have JLC-style headers, one row/reference, mm and Top/Bottom.
Their designator sets match. LCSC numbers deliberately remain blank: exact approved
MPNs are provided for manual matching. Do NOT claim availability or upload these
reference CSVs as an approved auto-PCBA order. Ask JLC for exact matching Cnumbers,
manufacturer suffix/package/ratings and availability; alternatives need explicitreview.
No paid partsselection service is activated. Ask about any fee before authorization.

Coordinates are native footprint origins, outputX=x−77.5/outputY=130−y, bothfaces
in the same top-view XY frame. Angles are retained nativeexport values normalized
to0..360degrees; no bottommirror or guessedfeederrotation correction is applied.
These are QUOTE_REFERENCE data, not approved machine centroids. Actual bodycentroids,
part-specific offsets/pin1/polarity andreelfeeder rotations must be checked after
exact librarypart matching in JLC's placementpreview; request corrected dataforreview.

Double-sided placement requires StandardPCBA, not the single-sidedEconomicroute.
JLC lists70x70mmminimum handling size and requires rails/fiducials. Our individual
45x60mmboard needs a returned panel/rail/tooling/fiducial proposal; simply adding
5mmrails doesnotnecessarilymeet both70mmdimensions. Quote tooling/panelquantity,
depanelization, stencil/setup and actual deliveredunit count separately. Preserve
the individual outline, isolationband,33partpositions and keep addedtooling offit.
No panelized Gerber, machine-adjusted CPL or stencil is approved by this enquiry.

For partialSMT quote: leaveall25componentinsertionholes open/unsoldered and do not
bridge them. Retain17specified filled/cappedvias. For a later fullTHTproposal, return
selective soldering/masking/inspection details and C1vent/formedpart/insulation process.
No energizedfunctionaltest or finishedinsulation qualification is requested as a
casual assemblyservice; testbasis andproductionauthorization remain separate.
''')
txt(D/'JLCPCB-ENQUIRY-UNSENT.txt','''To: support@jlcpcb.com
Subject: Technical DFM/quotation and separate assembly feasibility — Velluneo JLC14

Dear JLCPCB Technical Support,

Please review the attached JLC14 quotation handoff. This is a technical enquiry,
not an order or authorization to activate a paid service, manufacture or assemble.

1. BarePCB quotation: five finished individual45x60mmfourlayerFR-4boards, nominal
1.6mm, Tg155 request, ENIG,green/white,outer1oz/inner0.5oz. Request exactstack
JLC04161H-7628. Please return laminate/CTI/RTI/minimumpressed dielectric andfinished
copper guarantees. The GerberuploadZIP contains oneGKO,fourcopper,twoMask,twoSilk,
twoPaste,ExcellonXLN,drillmap andauxiliaryVelluneo_JLC14.sk.

The sklayer selects ALL17 Ø0.300mmvias for nonconductiveepoxyfill+coppercap BOTHends.
It is not copper/outline. Leaveall25componentholes open. T1's ten finishedholes
target1.350mm mustbe1.300..1.400mm; your standard+0.13/-0.08 is not acceptable here.
Please quote the tighter±0.050mm hole service for all25listed insertionholes.
These are soldered insertionholes, not press-fit terminals. Requestedhole/land
registration≤0.025mm also needs explicit capability agreement; return any inability
as a redline. Confirm actual finishedring/cap/planarity limits. No addedcopper,
tooling/thieving/marks in the protectedoutputY37.865..47.100mm bandacrossX0..45.
Please answer the attachedtechnical-response checklist and identify any infeasible
requirement before an order. A calculator figure alone is not a confirmedprocessquote.

2. Separate assemblyfeasibility/cost: quote26SMTparts on BOTHfaces using the33part
MPNlist and26SMTquote-reference BOM/CPL. Please identify exactmatchingLCSCnumbers,
suffixes/packages/ratings, availability, placementoffset/angle verification and any
sourcingservicefee before activation. No substitutions or paidselection approved.
Also assess the5THT and2wireoperations separately; T1/customwinding andformedparts
require their exactdrawings, acceptedconstruction andfirstarticles before assembly.

We understand two-sidedplacement requires StandardPCBA and the45x60mmpart needs
a≥70x70mmhandlingpanel/rails/fiducials proposal. Return this proposal, actualunit
andpanelquantities, setup/stencil/tooling/depanelization/parts/labor andleadtime
separately. Keep additions off thefinishedboard and preserve its isolationband.
ReferenceCPLs have no verifiedfeeder/centroid corrections and are not machine-ready.

Please advise what preliminaryDFM is available before ordering and any engineering
charge requiring separateapproval. We will request ConfirmProductionFile/noautomatic
confirmation if a laterorder is authorized; we understand processedfilms normally
follow that order/payment stage. No shippingaddress, paidservice, payment or production
authorization is supplied by this enquiry. Please quote shipping separately once
destination details are provided.

Regards,
Velluneo project — prepared draft, not yet sent
''')
questions=[('J14-PCB-01','PCB stack/material','Exactnamedstack,actualmaterial/CTI/RTI/minpressed dielectrics/finishedCu','Writtenprocessresponse'),('J14-PCB-02','Viafill/cap','17marked.300vias;25componentholesopen;bothendscoppercaps','SK/mapagreement andactualcap/ring/planaritylimits'),('J14-PCB-03','Tight componentholes','25listedholes±.050;T1ten1.300..1.400finished','Guaranteedsize/compensation andprice; nofalsepressfitcomponentclaim'),('J14-PCB-04','Registration/finishing','Requested≤.025registration;fillets/rings/finishinggrowthbudget','Actualguaranteedlimits orredline'),('J14-PCB-05','Isolationband/noedits','Noaddedcopper/tooling/marks inband;individual45x60retained','DFMexceptionresponse andlaterexactproductionfilmreview'),('J14-PCB-06','Quote/DFM scope','Bare5finishedunits,fullbaree-test,prequoteDFM/fees/leadtime','Writtenitemizedquote;nofreepreturnedfilmassumption'),('J14-ASM-01','Exact sourcing','26SMTexactMPNs/LCSC/package/stock/fees','Partmappingforreview;noalternativesauthorized'),('J14-ASM-02','Panel/handling','Standardbothsides,≥70x70handler,rails/fiducials/units','Panelproposal/actualdeliveredquantity/toolingcost'),('J14-ASM-03','Placement/process','Centroids/rotations/polarity/secondreflow/inspection','Correctedplacementpreview/data andprocessforreview'),('J14-ASM-04','Custom/THT/wires','5THT+2wireoperations;T1builder/formedparts/vent','Separatefeasibility,drawings/firstarticle/qualifiedprocess'),('J14-REL-01','Release','Noautomaticproductionfileconfirmation/order/energization','Exactowner/qualifiedrevieweracceptanceatalaterstage')]
writecsv(D/'JLCPCB-TECHNICAL-RESPONSES.csv',['ID','Topic','Required_response','Acceptance_evidence','Supplier_response','Status'],[dict(ID=i,Topic=t,Required_response=r,Acceptance_evidence=e,Supplier_response='',Status='PENDING')for i,t,r,e in questions])
txt(D/'README.md','''# JLC14 — JLCPCB-specific quote handoff

This packet adapts the unchanged RFQ13 isolated45x60mm33partdriver to JLCPCB's
public instructions read20November2026. Owner chose PCB plus separateassemblyfeasibility.
No account was accessed, file uploaded, enquiry sent, charge activated or order placed.

Use Velluneo_JLC14_Gerber_Upload.zip only in Addgerberfile at https://cart.jlcpcb.com/quote.
Use Velluneo_JLC14_Quote_Handoff.zip for the complete manualsupportenquiry. Do notupload
the fullhandoffZIP to theGerberfield. The Englishdraft is JLCPCB-ENQUIRY-UNSENT.txt;
the public quoteFAQ directs quotationquestions to support@jlcpcb.com withGerbers/files.
For the owner, START_HERE_PL.txt gives the exact sequence and the ready-to-paste remark.

Important JLC-specific corrections: addbothpasteGerbers, ONEGKO, namedG2L/G3Linnerlayers,
auxiliarySKmarked17viafillselection plusimage/map, exactformvalues andPCBRemark.
Do not rely on a PDF/texthiddeninGerberZIP beingread. Manufacturingartwork/pinholedata
are re-exported/independentlycompared to the alreadyreviewedsource, not rerouted.
Allfilesuseoneexistingplotdatum; the KiCadAbsoluteexample is deliberatelyadapted to
retainmatchingGerber/drill/SK/CPLcoordinates. Sourcefiles/rules/toolkitremainunchanged.

This is a prepared quotationpacket, not an approved or imported liveJLCcart. Thepublic
calculator canprovide an indicativeprice, but nonstandardholes/registration/material
andfilldetails require supportconfirmation. Actualproductionfilms normallyfollow
alaterorder/payment; no freepreorderfilms arepromised. No paidpartselectionauthorized.

Assembly is a separatemanualfeasibility enquiry.26SMTBOM/CPLhaveJLC-styleheaders but
LCSCIDs andactualcentroid/feedercorrections are notverified; theseareQUOTEREFERENCE,
not automaticassemblyorderfiles. Exact33partMPNs and7manualoperationsareincluded.
Standardtwo-sidedPCBA needs a≥70x70mmhandlingproposal/rails/fiducials; thefinished
boardremains45x60mm. No automaticpanel/toolingedits orsubstitutions areauthorized.

RFQ13 reviewedengineering, exactT1/formedpartfirstarticles, finishedinsulation,
functional/fault/thermalqualification and genuinehumanstage/releaseholds are retained.
JLC14 changes packaging/supportdocuments only; RFQ13 keeps authorityforactualCAD.
''')
txt(D/'START_HERE_PL.txt','''VELLUNEO JLC14 — PAKIET DO WYCENY JLCPCB

1. Rozpakuj Velluneo_JLC14_Quote_Handoff.zip.
2. Do https://cart.jlcpcb.com/quote w polu Add gerber file wybierz WYŁĄCZNIE
   Velluneo_JLC14_Gerber_Upload.zip. Nie wgrywaj całego pakietu jako Gerberów.
3. Ustaw: FR-4;4warstwy;45x60mm;5szt.;Industrial/Consumer;1projekt;SinglePCB;
   1.6mm;Green;White;ENIG;outer1oz;inner0.5oz;RemoveMark;FlyingProbeFullyTest.
   Poproś o dokładny stack JLC04161H-7628 i Tg155. ViaCovering:Epoxy-Filled&Capped.
   Wszystkie17przelotekØ0.300mm mają być wypełnioneepoksydem i zamkniętemiedzią
   z obu stron. Wszystkie25otworówelementów pozostają otwarte.
4. Wklej CAŁOŚĆ PCB-REMARK-PASTE.txt do PCBRemark. Gdy pole nie mieści tekstu,
   użyj PCB-REMARK-SHORT.txt i koniecznie przekaż pełny opis obsłudze. Nie usuwaj
   wymagań, żeby zmieścić formularz. Krytyczne ustalenia wymagają pisemnej odpowiedzi.
5. Sprawdź podgląd:4warstwy miedzi,jedenobrys45x60mm,42otwory,zeroNPTH/slotów;
   SK jest mapą17przelotek do wypełnienia, nie kolejną warstwąmiedzi/obrysem.
   Gdy automat źle rozpozna plik lub nie pozwala wybrać wymagań, użyj kontaktu
   technicznego. Samo przyjęcieZIP ani cena kalkulatora nie potwierdzają wykonania.
6. Przy tej płytce zalecana jest ręczna weryfikacjaprzezsupport@jlcpcb.com.
   Treśćgotowa:JLCPCB-ENQUIRY-UNSENT.txt. Załącz pakietwyceny lub osobno
   GerberZIP,mapęprzelotek,listęotworów,notatkiwykonania i dokumentacjęmontażową.
   JLC ostrzega, że PDF/TXT/Excel schowane wGerberZIP mogązostaćpominięte;
   dlatego wymagania są również wPCBRemark i treścizapytania.
7. WycenagołegoPCB:PCBAssemblyOFF,StencilOFF. Osobno poproś o ocenę i wycenę
   montażu26SMT na obustronach oraz możliwości5THT+2operacjiprzewodów.
   JLC wymaga dla montażu dwustronnegoStandardPCBA oraz odpowiedniegopanelu
   minimum70x70mm zszynami/fiducjalami. Nie powiększamy docelowejpłytki45x60;
   wykonawcamaprzesłaćrysunekpanelutechnologicznegodoweryfikacji.
8. BOM/CPL wassembly-feasibility to danereferencyjneDOZAPYTANIA, nie gotowepliki
   dozleceniaautomatycznegomontażu. Należy potwierdzićdokładneLCSCnumery/MPN,
   dostępność,centroidy,obroty,pin1/polaryzacjęorazwykonanieczęściformowanych/T1.
   Nie aktywuj płatnegodoboruczęści bez poznaniaopłat i osobnejdecyzji.
9. T1wymaga gotowychotworów1.300..1.400mm. StandardJLC+0.13/-0.08 daje dla1.35mm
   zakres1.270..1.480mm i NIEjestzaakceptowany. Wzapytaniu prosimyo dokładniejszą
   usługę±.050mm orazpotwierdzenierejestracji,materiałówiizolacji. To otworypod
   lutowaneelementy,niezłączaPressFit. NazwausługidokładnychotworówmożeużywaćPress-fit.
10. Na tymetapiewyłączniezapytanie/wycena. Nicniewysłano iniczegoniezamówiono.
    Nie klikaj płatności,zamówieniaani zatwierdzeniaprodukcji. Jeślipóźniejbędzie
    zamówienie,wybierzConfirmProductionFile bezautomatycznejakceptacji;JLCzwykle
    udostępniaprzetworzonefilmypoetapiezamówienia/płatności,nie jako gwarantowaną
    darmowąusługęprzedzamówieniem.
''')
# Draw an actual-coordinate via selection map, with legible ID/XY list outside board.
inv=json.loads((S/'checks/native-inventory.json').read_text());vias=inv['vias'];scale=12;ox=70;oy=110
im=Image.new('RGB',(1450,1040),'white');g=ImageDraw.Draw(im)
fontpath='C:/Windows/Fonts/arial.ttf';font=ImageFont.truetype(fontpath,21);small=ImageFont.truetype(fontpath,17);title=ImageFont.truetype(fontpath,29)
g.text((60,25),'JLC14 — 17 VIA FILL / CAP LOCATIONS',font=title,fill='#153b4f');g.text((60,66),'Top-view XY; orange = epoxy fill + copper cap BOTH ends; grey = leave OPEN',font=font,fill='#333333')
def point(x,y):return(ox+x*scale,oy+(60-y)*scale)
g.rectangle([point(0,60),point(45,0)],fill='#edf6f0',outline='#134e39',width=3)
g.rectangle([point(0,47.1),point(45,37.865)],fill='#f5e5e3');g.text((ox+4,oy+(60-46.5)*scale),'PROTECTED BAND — NO ADDITIONS',font=small,fill='#8e2929')
for q in component:
 x,y=point(q['x_mm'],q['y_mm']);rr=q['diameter_mm']*scale/2;g.ellipse((x-rr,y-rr,x+rr,y+rr),fill='white',outline='#6f7476',width=2)
for v in vias:
 x,y=point(v['output_x_mm'],v['output_y_mm']);g.ellipse((x-6,y-6,x+6,y+6),fill='#db651d',outline='#923800',width=2);dx,dy={8:(-20,5),10:(9,-20),12:(8,6)}.get(v['id'],(7,-15));g.text((x+dx,y+dy),str(v['id']),font=small,fill='#943700')
g.text((70,860),'Outline 45×60 mm; ALL 17 design holes Ø0.300 mm selected.',font=font,fill='#153b4f');g.text((70,893),'All 25 component holes Ø1.000–1.600 mm remain OPEN.',font=font,fill='#153b4f')
g.text((680,115),'ID     X(mm)       Y(mm)       Drill(mm)',font=font,fill='#153b4f')
for i,v in enumerate(vias):g.text((680,160+i*34),f"{v['id']:02d}      {v['output_x_mm']:8.3f}      {v['output_y_mm']:8.3f}       0.300",font=font,fill='#333333')
g.text((680,780),'SK layer: Velluneo_JLC14.sk',font=font,fill='#943700');g.text((680,820),'Auxiliary selection only; not copper or outline.',font=small,fill='#333333');g.text((70,950),'DFM/quotation reference from actual RFQ13 coordinates — not a fabrication acceptance or physical measurement.',font=small,fill='#444444')
im.save(H/'Velluneo_JLC14_via_fill_map.png');shutil.copyfile(H/'Velluneo_JLC14_via_fill_map.png',W.parent/'outputs/Velluneo_JLC14_via_fill_map.png')
put(D/'checks/assembly-format-check.json',dict(all_references=33,SMT_references=26,THT_operations=5,wire_operations=2,SMT_BOM_CPL_designator_sets_equal=True,LCSC_numbers_invented=False,LCSC_mapping_verified=False,native_export_rotations_normalized_only=True,machine_centroids_or_feeder_rotations_verified=False,format='CSV UTF8, metric mm, Top/Bottom; header-compatible quote reference only',source_BOM_sha256=hashlib.sha256((S/'design/BOM.csv').read_bytes()).hexdigest(),source_positions_sha256=hashlib.sha256((H/'positions-native.csv').read_bytes()).hexdigest(),portal_assembly_import_performed=False))
print('Prepared JLC settings/remarks/manualenquiry;33MPNs,26SMTquoteBOM/CPL,7operations,17viaactual-coordinate map',flush=True)
