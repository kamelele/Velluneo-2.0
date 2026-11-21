from pathlib import Path
import csv,json,hashlib,math,html
W=Path(__file__).resolve().parent
if W.name=='implementation':
 D=W.parent;P=D.parent;R=P.parents[3];W=R.parent
else:
 R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'catalogue-redesign-15'
def put(name,data):
 p=D/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def txt(name,s):
 p=D/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
# Human-read web observations, not an API inventory feed or stock reservation.
obs=[
 ('UCC28701DBVR','C2873258',0,5,'preorder'),('UCC28701DBVT','C2877623',0,5,'preorder'),
 ('NTCS0603E3104FXT','C191810',18337,1,'available',18216),('STD2N80K5','C222162',0,8,'preorder'),
 ('AC05AT0K04709JBW00','C5575510',0,3,'preorder'),('EEHZA1J100P','C542299',3,8,'preorder'),
 ('US1M-13-F','C99333',138150,1,'available',137575),('SMBJ160A','C224011',201,1,'available',200),
 ('STTH2R02A','C81455',2709,1,'available',2686),('CRCW080580K6FKEA','C2077343',127,1,'available'),
 ('CRCW25124R70FKEG','C242563',0,116,'preorder'),('SDB107-TP','C85265',301,1,'available',301),
 ('CRCW2512499KFKEG','C2077316',0,43,'preorder'),('CRCW080517K4FKEA','C4278979',540,1,'available'),
 ('CRCW060347K0FKEA','C844929',128485,1,'available'),('CRCW080551K1FKEA','C2085421',3,1,'available'),
 ('CRCW06031K96FKEA','C843925',6,1,'available'),('CRCW12062R55FKEA','C2085420',0,3471,'preorder'),
 ('3403.0268.23','C9900323345',0,441,'consign_only_unverified_manufacturer'),
 ('C2220C474J5GACTU','C2182274',0,2,'preorder'),('CRCW08054R70FKEA','C844849',13,1,'available'),
 ('CRCW060380K6FKEA','C844587',5087,1,'available'),('CRCW2512402KFKEG','C2087744',0,717,'preorder'),
 ('STTH1R02A','C2965280',451,1,'available'),('CRCW251220K0FKEG','C2078507',4,1,'available')]
observations=[dict(mpn=a,code=b,stock=c,MOQ=d,status=e,available_order_quantity=f[0] if f else None,url='https://jlcpcb.com/partdetail/'+b,checked='2026-11-20',method='Read-only JLCPCB visible UI; settled product detail or exact-MPN result row')for a,b,c,d,e,*f in obs]
put('evidence/jlcpcb-stock.json',dict(date='2026-11-20',caution='Stock is transient and unreserved. Available Order Qty differs from stock; search-row stock is not that quantity. Preorder is not stocked. Manufacturer datasheet governs ratings, not marketplace fields. Initial unhydrated zero-result searches were discarded.',observations=observations))
jo={x['mpn']:x for x in observations}
dk='https://www.digikey.com/en/products/detail/vishay-dale/'
# refs, selected MPN, maker, value, package, stocked external fallback, quantity,
# MOQ, source observation kind. Distributor pages themselves are primary inventory sources.
data=[
 ('F1','3403.0268.23','Schurter','250mA slow;277Vac/250Vdc;1.5kA breaking','UMT-H SMD','https://www.mouser.com/en/ProductDetail/Schurter/3403.0268.23?qs=mBwMfv9Clf3HFr6S0f%252B%2FLQ%3D%3D',1074,1),
 ('R1','AC05AT0K04709JBW00','Vishay','47ohm 5W 5%;flameproof pulse wirewound;NOT a specified fusible resistor','AC05-AT WSZ factory SMD','https://www.digikey.com/en/products/detail/vishay/AC05AT0K04709JBW00/17372614',425,1),
 ('BR1','SDB107-TP','MCC','1000V 1A;IFSM30A;I2t3.735A2s','SDB-1 SMD','https://jlcpcb.com/partdetail/C85265',301,1),
 ('C1','450BXW15MEFR10X20','Rubycon','15uF 450V;10000h/105C','radial Dmax10.5 Lmax22 pitch5','https://www.mouser.com/en/ProductDetail/Rubycon/450BXW15MEFR10X20?qs=T3oQrply3y8hle4J6fSxPA%3D%3D',988,1),
 ('R2 R3 R14 R15','CRCW2512499KFKEG','Vishay','499k 1% 100ppm;1W 500V manufacturer Umax','2512',dk+'CRCW2512499KFKEG/1173746',8529,1),
 ('U1','UCC28701DBVT','Texas Instruments','same IC/pinout as DBVR;different packing quantity','SOT23-6 DBV','https://www.mouser.com/en/ProductDetail/Texas-Instruments/UCC28701DBVT?qs=rg6Iqu58vpU9cO7MIDHsMA%3D%3D',445,1),
 ('Q1','STD2N80K5','STMicroelectronics','800V 2A;RDSmax4.5ohm','DPAK TO252','https://nl.farnell.com/en-NL/stmicroelectronics/std2n80k5/mosfet-n-ch-800v-2a-to-252/dp/2807239',3133,1),
 ('T1','74215','MYRRA','factory-wound;120P:27S:14A;Lp1.8mH +/-10%;0.50Apk primary','E16 THT;19x16x19.5mm max','https://pl.farnell.com/myrra/74215/flyback-transformer-th-1-5a/dp/4461577',48,1),
 ('D1','US1M-13-F','Diodes Incorporated','1000V ultrafast','SMA','https://www.digikey.com/en/products/detail/diodes-incorporated/US1M-13-F/1811111',402223,1),
 ('TVS1','SMBJ160A','Littelfuse','160V standoff;178..197V breakdown;259V@2.3A;600W10/1000us','SMB','https://www.digikey.com/en/products/detail/littelfuse-inc/SMBJ160A/688307',1330,1),
 ('C2 C3','C2220C474J5GACTU','KEMET','470nF 50V 5% C0G;retain dielectric','2220','https://www.digikey.com/en/products/detail/kemet/C2220C474J5GACTU/1874823',7682,1),
 ('R4','CRCW080551K1FKEA','Vishay','51.1k 1% 100ppm;conservative125mW','0805',dk+'CRCW080551K1FKEA/1175832',41943,1),
 ('R5','CRCW080517K4FKEA','Vishay','17.4k 1% 100ppm;conservative125mW','0805',dk+'CRCW080517K4FKEA/1180922',12860,1),
 ('R6','CRCW06031K96FKEA','Vishay','1.96k 1% 100ppm;conservative100mW','0603','https://www.digikey.ca/en/products/detail/vishay-dale/CRCW06031K96FKEA/1174699',4259,1),
 ('R7','CRCW08054R70FKEA','Vishay','4.7ohm 1% 100ppm;conservative125mW','0805','https://www.mouser.com/en/ProductDetail/Vishay/CRCW08054R70FKEA?qs=gLraRG2UF0ZMAtzHfV2Yww%3D%3D',107786,1),
 ('R8','CRCW060347K0FKEA','Vishay','47k 1% 100ppm;conservative100mW','0603',dk+'CRCW060347K0FKEA/1180000',136394,1),
 ('R9','CRCW12062R55FKEA','Vishay','2.55ohm 1% 100ppm 250mW','1206',dk+'CRCW12062R55FKEA/1961809',103789,1),
 ('D2','STTH1R02A','STMicroelectronics','200V 1.5A;trrmax30ns','SMA','https://www.ozdisan.com/en/p/rectifier-diodes-389/stm-stth1r02a-456902',8458,1),
 ('R10','CRCW25124R70FKEG','Vishay','4.7ohm 1% 100ppm 1W;snubber value pending leakage validation','2512',dk+'CRCW25124R70FKEG/1963001',31546,1),
 ('D3','STTH2R02A','STMicroelectronics','200V 2A','SMA','https://www.micros.com.pl/en/product/dp-stth2r02a%2C110134.html',5000,1),
 ('C4','EEHZA1J100P','Panasonic','10uF 63V hybrid;120mohm ESR100kHz;10000h105C','SMD hybrid6.3mm,Hmax6.1','https://www.digikey.com/en/products/detail/panasonic-electronic-components/EEH-ZA1J100P/3088129',853,1),
 ('R11 R12','CRCW251220K0FKEG','Vishay','20k 1% 100ppm;1W 500V manufacturer Umax','2512',dk+'CRCW251220K0FKEG/1199277',11,1),
 ('RT1','NTCS0603E3104FXT','Vishay','100k 1%;B4100 +/-1%;NOT B3950','0603','https://www.mouser.com/en/ProductDetail/Vishay-BC-Components/NTCS0603E3104FXT?qs=I%2FaSOo0oSyTJIlTZ0fPPbw%3D%3D',8334,1),
 ('R13','CRCW060380K6FKEA','Vishay','80.6k 1% 100ppm;conservative100mW','0603',dk+'CRCW060380K6FKEA/1180027',61330,1),
 ('R16 R17','CRCW2512402KFKEG','Vishay','402k 1% 100ppm;1W 500V manufacturer Umax','2512',dk+'CRCW2512402KFKEG/1173741',5829,1),
]
baseline=list(csv.DictReader((P/'jlcpcb-quote-14/assembly-feasibility/BOM_33_ALL_PARTS_MANUAL_QUOTE.csv').open(encoding='utf-8-sig',newline='')))
old={x['Designator']:x for x in baseline}; rows=[]
for refs,mpn,maker,value,package,url,stock,moq in data:
 for ref in refs.split():
  j=jo.get(mpn)
  selected_jlc=bool(j and j['status']=='available')
  route=dict(supplier='JLCPCB' if selected_jlc else ('Farnell' if 'farnell' in url else 'external distributor'),url=j['url'] if selected_jlc else url,mode='JLCPCB stocked assembly listing; quantity/attrition and process confirmation still required' if selected_jlc else 'external stocked part; JLCPCB Global Sourcing/consignment or separate assembly to be agreed',stock=j['stock'] if selected_jlc else stock,MOQ=j['MOQ'] if selected_jlc else moq)
  rows.append(dict(ref=ref,manufacturer=maker,mpn=mpn,value=value,package=package,quantity_per_board=1,old_mpn=old[ref]['Manufacturer Part Number'],old_value=old[ref]['Comment'],changed=mpn!=old[ref]['Manufacturer Part Number'],checked='2026-11-20',jlcpcb=j,preferred_purchase=route,external_stock_source=dict(url=url,stock=stock,MOQ=moq,method='Distributor-page read by assigned sourcing context; R4/R6/R9 additionally read in root web search',reservation=False),assembly_release=False))
  if ref in ('R11','R12','D3'):
   rows[-1]['external_stock_source']['MOQ']='not independently confirmed; do not assume full-reel minimum or small-lot acceptance'
  if ref=='BR1':rows[-1]['external_stock_source']['method']='JLCPCB UI listing; this is not an external-distributor fallback'
for ref in ('J1','J2'):
 rows.append(dict(ref=ref,manufacturer='Alpha Wire',mpn='5854/7 BK005 + 5854/7 RD005',value='pair of wire solder pads; wire raw material selected, finished harness NOT defined',package='24AWG 7/32 PTFE;UL1213 600Vrms105C',quantity_per_board=None,old_mpn=old[ref]['Manufacturer Part Number'],old_value=old[ref]['Comment'],changed=True,checked='2026-11-20',jlcpcb=None,preferred_purchase=dict(supplier='Mouser',url='https://www.mouser.com/en/c/wire-cable/?insulation+material=Polytetrafluoroethylene+%28PTFE%29&wire+gauge+-+awg=24+AWG',stock='BK103 / RD31 spools; source category',MOQ='1 spool per colour;100ft /30.48m each',mode='Buy wire raw material; final cut lengths, sleeving and strain relief require assembly definition'),assembly_release=False))
rows.sort(key=lambda x:list(old).index(x['ref']))
put('selected-bom.json',dict(revision='CAT15',status='Stock-sourced engineering selection; NOT a fabrication or PCBA upload BOM',basis='b31e08da7c2b7e2b81717df6e9f2d094b04fed39',date='2026-11-20',unit_count=len(rows),fitted_electronic_positions=31,wire_pad_pairs=2,all_positions_have_purchase_route=True,factory_wound_transformer=True,custom_winding_required=False,stock_unreserved=True,components=rows))
np,ns,na,lp,rcs,rs1,rs2=120,27,14,.0018,2.55,51100,17400
calc=dict(assumptions=dict(eta_transformer=.9,Vccr=.319,normal_CS_threshold_V=.75,RS1_ohm=rs1,RS2_ohm=rs2,RCS_ohm=rcs,TD_s=126.5e-9,KLC=25,VFsecondary=.8,VFaux=.8,nominal_VS_regulation_V=4.05),Np_over_Ns=np/ns,Na_over_Ns=na/ns,RCS_for_250mA=.319*(np/ns)*.9/(2*.25),nominal_current_A=.319*(np/ns)*.9/(2*rcs),normal_Ipk_A=.75/rcs,static_fault_Ipk_at_1p6V_A=1.6/rcs,RLC_ohm=25*rs1*rcs*126.5e-9*(np/na)/lp,CV_boundary_V=4.05*(ns/na)*(1+rs1/rs2)-.8,VDD_at_20V=(20+.8)*na/ns-.8,VDD_at_27V=(27+.8)*na/ns-.8,VDD_margin_output_floor_V=(8.45+1+1)*ns/na-.5,CC_demag_frequency_at_24V_Hz=.425*(24+.8)*(np/ns)/(lp*.75/rcs),estimated_copper_gap_active_1p55mm=math.hypot(12.2,1.5)-1.55,all_9_PTH_2mm_gap=math.hypot(12.2,.4)-2,all_9_PTH_1p5mm_gap=math.hypot(12.2,.4)-1.5,DPAK_maker_pad_gap_mm=1.8)
put('calculations/transformer-screen.json',dict(status='Analytical screen only; no simulation or measurement',results=calc,normal_candidate_output_V=[20,27],old_18V_low_end_retained=False,unresolved=['Per-cycle/jitter and abnormal pulse stress versus0.50Apk; static1.6V screen exceeds0.50A','Actual transformer leakage, DCR, saturation/reset and clamp energy','VDD takeover/cold start/short/open recovery','Optical750..850lm and completed lamp thermal evidence','Component-level insulation approval versus lighting-product conditions','DPAK package-local3mm rule incompatibility; no waiver granted']))
pinmap={'1':'PGND_AUX_RETURN','2':'AUX_RAW (dot)','3':'physically absent','4':'DRAIN (dot)','5':'physical pin; no winding shown; no external connection','6':'BULK_P','7':'SECONDARY_RAW (dot)','8':'S2 tap; winding-connected; external NC','9':'S1 tap; winding-connected; external NC','10':'OUT_NEG'}
put('interfaces/transformer-pin-intent.json',dict(status='Proposed independent source-based intent, before new schematic; NOT owner-approved',mpn='74215',view_basis='Manufacturer bottom-view pin drawing; mirror X for top-side PCB footprint',pins=pinmap,windings=[dict(pins=[4,6],turns=120),dict(pins=[2,1],turns=14),dict(pins=[7,10],turns=27),dict(pins=[8,10],turns=17),dict(pins=[9,10],turns=6)],unused_pins_are_not_unwound=True))
sources=[('MYRRA74215','https://myrra.com/wp-content/uploads/2019/11/74215-Datasheet.pdf','Pinout/dots/windings, dimensions, currents, insulation; manufacturer does not specify leakage/DCR/frequency here'),('MYRRAfamily','https://myrra.com/flyback/','S3 operating window19.2..28.8V; do not misuse S2 for27V'),('TIcontroller','https://www.ti.com/lit/ds/symlink/ucc28700.pdf','SLUSB41A;UCC28701 belongs to this family;CC/VS/RLC/thresholds and caveat that limits are average levels'),('STD2N80K5','https://www.st.com/resource/en/datasheet/std2n80k5.pdf','DPAK pinout,800V/2A and manufacturer land pattern; RthJA conditional'),('SDB107','https://www.mouser.com/datasheet/2/258/SDB101_SDB107_SDB_1_-2510779.pdf','MCCRev4-1-12072023; polarity, geometry and reduced surge versus W10G'),('AC05AT','https://www.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf','Factory WSZ pads; do not call AC-AT a guaranteed fusible resistor'),('CRCW','https://www.vishay.com/docs/20035/dcrcwe3.pdf','14Apr2026;2512rated500V per manufacturer, contradicts marketplace300V; conservative small-size power retained'),('TVS','https://www.littelfuse.com/assetdocs/tvs-diodes-smbj-series-datasheet?assetguid=ba555e99-a12d-4f72-a0b6-86b06c67171e','SMBJ160A primary manufacturer2.3A at259V; do not copy LCSC1.9A'),('C4','https://industrial.panasonic.com/content/data/CP/PDF/ABA0000PE428.pdf','Hybrid ZA; preserve ESR/ripple/life'),('D1','https://www.diodes.com/assets/Datasheets/ds16008.pdf','US1M genuine maker identity'),('wire','https://www.micro-semiconductor.com/datasheet/b4-5854-7-BK005.pdf','Alpha Wire source drawing; UL1213105C differs from MIL200C')]
put('evidence/source-register.json',dict(checked='2026-11-20',sources=[dict(id=a,url=b,scope=c)for a,b,c in sources],inventory_sources='Exact distributor URLs and dated observed counts are alongside every selected-bom.json position; JLC UI observations are separate. Search-crawler/distributor readings are not a guaranteed future allocation.'))
txt('engineering-change.md','''# CAT15 — selected factory-stock redesign basis

The owner explicitly excludes custom windings. Select MYRRA **74215**, a complete
factory-wound catalogue transformer; Farnell Poland4461577 shows48 units,MOQ1,
24.86PLN net on20Nov2026. Do not buy obsolete74015 or a bare bobbin/core kit.
The existing RFQ13/JLC14 transformer and production files do not meet this requirement.

Keep the isolated CC architecture and select120:27:14 turns,1.8mH. Use S3 pins7–10;
S1/S2 are real connected taps, externally unused. Follow the independent pin-intent
file. 19x16x19.5mm is the maximum body;19.5mm is HEIGHT. This is0.5mm higher than
the earlier18mm reservation, although substantially smaller in plan. Complete lamp
diameter60x120mm remains a target, not a proven enclosure fit.

Selected adaptation: R4=51.1k, R6=1.96k, R9=2.55ohm; R5=17.4k stays. Nominal
current is~250mA, CV boundary~29.95V and a **20..27V analytical load window** is
proposed. The old18V lower end is not carried forward. None of these screens proves
the required750..850lm at the diffuser; the final LED panel remains to be matched.
TD126.5ns and transformer efficiency90% are assumptions. Do not treat average CS
thresholds/frequency or static1.6V as proven individual-cycle bounds. The1.6V/RCS
fault screen exceeds the transformer's0.50Apk rating; abnormal stress is OPEN.

Select factory SMD R1=AC05AT0K04709JBW00, BR1=SDB107-TP and Q1=STD2N80K5 to remove
customer lead forming. U1=DBVT is a packaging-only choice. TVS1=LittelfuseSMBJ160A
has an actually stocked route. Keep F1: AC-AT is not a specified fusible resistor.
BR1's30A surge is lower than the former50A: rerun inrush/fuse/bridge coordination.
The new T1's unpublished leakage/DCR cannot inherit the custom transformer's20uH
assumption or thermal calculation. R10/TVS are stocked starting selections, not a
qualified new clamp; repeat clamp/reset/diode/thermal calculations and bench tests.

## Exact mechanical holds before applying new placement/routing

The proposed libraries below are source-dimension inputs, not accepted production
footprints. The old custom footprint must never be assigned to74215.

* T1: nine physical pins, missing3; row12.2mm, primarypitch2.7, secondarypitch3.5,
  recommended drill1.1mm, pin0.60+/-0.10, row tolerance+/-0.5,pitch+/-0.25mm.
  All2mm PTH lands give only10.2066mm nominal P/S copper separation and fail10.7mm.
  All1.5mm lands give10.7066mm but insufficient annulus under the earlier illustrative
  process budget. Candidate six1.55mm active PTH plus three NPTH clearance holes for
  unused5/8/9 gives10.7419mm nominal active copper gap. Unused pin metal and winding
  taps still exist. Validate real annulus, insertion, paste/mask, external metal,
  tolerances and component internal insulation separately; NPTH is not a safety waiver.
* Q1: manufacturer's DPAK land pattern has only1.8mm between drain tab and gate/source
  lands. This fails the unchanged project3mm HV/quiet floor. The datasheet's630Vrms
  footprint note supports investigation, not an automatically authorized exception.
  A demonstrably usable modified footprint or an explicit reviewed package-local
  policy decision is required before applying Q1. Never lower the global3mm rule.
* BR1: pad1=plus top-right,2=AC bottom-right,3=minus top-left,4=AC bottom-left,
  in TOP view. Maker assigns polarity, not numeric pad IDs; this is an explicit local
  mapping to check against the new symbol. Pads1.19x1.52, pitch5.21x8.74mm; P/N gap4.02mm.
* R1: maker WSZ pads4x10mm, centres22.7mm, innergap18.7mm; factory lead shape.
  ~10mm maximum height allowance. Keep away from C1, polymer and touchable enclosure.
* C1 remains stock radial; no forced pitch forming. Preserve2mm vent space and full
 10.5x22mm worst-case body allowance.

## Assembly and handoff

The proposal has29 electronic SMT positions, T1/C1 THT and two wire-pad pairs.
JLCPCB's listing is not supplier acceptance of the complete board. Source the exact
outside parts via agreed Global Sourcing/consignment or a separate assembly operation.
Quantity, feeder attrition, lead times, two-sided handling/panelization, native
centroids/rotations and the finished harness remain to be agreed after actual CAD.
No new CPL, Gerber ZIP or 'order-ready' PCBA BOM is emitted from stale coordinates.
''')
txt('README.md','''# CAT15 — orderable-component selection,20 November2026

**Selected transformer: MYRRA74215, factory-wound and sold complete. No custom winding.**
See [selected BOM](selected-bom.json), [JLCPCB dated stock](evidence/jlcpcb-stock.json),
[engineering change](engineering-change.md) and [transformer pin intent](interfaces/transformer-pin-intent.json).

Every one of33 baseline positions has a purchase route:31 electronic positions and
two wire-pad pairs with bought wire material. This is a component procurement
selection, not a completed harness or a qualified new assembled PCB. JLCPCB stock,
preorders and external stock are distinguished. No stock has been reserved.

R1/BR1/Q1 use factory SMD packages. R4/R6/R9 adapt the circuit to stock T1; U1
packing and TVS maker are explicit choices. The old transformer footprint does not
fit. Q1 package clearance, T1 abnormal current/leakage, startup/faults and insulation
remain concrete engineering holds, explained in engineering-change.md and checks.

**RFQ13/JLC14 archives are historical and must not be ordered for this new variant.**
Native product schematic/PCB, rules and old checks are unchanged. No proposed
part is represented as a validated drop-in; no new native/CAM pass is claimed.
No supplier was contacted, no upload/order/payment or physical test was performed.
Toolkit manifest remains b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97.

Review scope: exact sourcing/ECO proposal only. The next implementation must resolve
the identified current/clearance holds, capture the new pin map, validate libraries,
redo affected placement/routing and produce freshly matched manufacturing files.
The owner and independent review gates remain distinct from catalogue availability.
''')
# Small static, inspectable procurement view; not a product render.
body=[]
for x in rows:
 j=x['jlcpcb'];status=('JLC stock '+str(j['stock']) if j and j['status']=='available' else 'External stock / '+(j['status'] if j else 'not JLC-qualified'))
 body.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>'for v in (x['ref'],x['mpn'],x['value'],status))+f'<td><a href="{html.escape(x["preferred_purchase"]["url"],quote=True)}">Purchase source</a></td></tr>')
txt('parts-preview.html','''<!doctype html><html lang="en"><meta charset="utf-8"><title>CAT15 — selected orderable parts</title><style>body{font:15px system-ui;margin:32px;color:#17222a;max-width:1400px}h1{font-size:25px}aside{background:#fff2cd;padding:16px}table{border-collapse:collapse;width:100%;margin-top:24px}td,th{text-align:left;padding:10px;border-bottom:1px solid #ccd2d7}small{color:#52616a}a{color:#075caf}</style><h1>Velluneo — selected catalogue parts</h1><p>Complete factory-wound transformer: <b>MYRRA 74215</b> · Farnell4461577 · observed48pcs · MOQ1 · 24.86PLN net</p><aside><b>Procurement selection; PCB redesign remains open.</b> All33 positions have a purchase route. Stock20Nov2026, unreserved. Wire raw material is not a finished harness. Previous Gerbers do not fit these changes.</aside><table><thead><tr><th>Reference</th><th>Exact manufacturer part</th><th>Selection</th><th>Observed route</th><th>Link</th></tr></thead><tbody>'''+''.join(body)+'''</tbody></table><p><small>Source: linked manufacturer/distributor/JLCPCB pages,20November2026. No order, stock reservation or physical qualification.</small></p></html>''')
print(json.dumps(dict(positions=len(rows),electronic=31,jlc_stocked_positions=sum(bool(x['jlcpcb'] and x['jlcpcb']['status']=='available')for x in rows),changed_positions=[x['ref']for x in rows if x['changed']],calculation=calc),indent=2))
