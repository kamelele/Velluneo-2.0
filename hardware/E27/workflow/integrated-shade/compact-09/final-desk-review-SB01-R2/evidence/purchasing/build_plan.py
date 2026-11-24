from pathlib import Path
import csv,json,hashlib,datetime
from decimal import Decimal as D
H=Path(__file__).resolve().parent;P=H.parents[1]/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
source=list(csv.DictReader((P/'bom-build.csv').open(encoding='utf-8-sig')))
old=json.loads((P/'procurement.SB01.json').read_text(encoding='utf-8'))['parts']
urls={r['refs'][0]:r['url'].replace('/en/','/pl/') for r in old}
urls.update(RF1='https://www.digikey.pl/pl/products/detail/bourns-inc/FW20A47R0JA/4211449',L1='https://www.digikey.pl/pl/products/detail/vishay-beyschlag-draloric-bc-components/PR02FS0201000KR500/6691142',C5='https://www.digikey.pl/pl/products/detail/samsung-electro-mechanics/CL21B475KAFNNNE/3891055',R4='https://www.tme.eu/pl/details/erj6enf1242v/rezystory-smd/panasonic/')
live={r['ref']:r for f in ['acquisition.json','retry-tme.json'] for r in json.loads((H/f).read_text(encoding='utf-8')) if r.get('http_status')==200}
live['R4']=json.loads((H/'r4-retry.json').read_text(encoding='utf-8'))
# No historical procurement prices are used. Indexed observations below are explicitly not live stock.
dk={
 'RF1':('FW20A47R0JACT-ND',973,'2.07','PLN','last month','Cut tape'),
 'L1':('BC3366CT-ND',4994,'1.81','PLN','2 months','Cut tape'),
 'C4':('',13460,'3.95','PLN','last month','Bulk; exact MPN, SKU not observed'),
 'C5':('1276-2969-1-ND',172936,'1.85','PLN','2 months','Cut tape'),
 'R5':('311-.68LYCT-ND',4603,'1.44','PLN','2 months','Cut tape'),
 'T1':('',1712,'13.14','PLN','2 months','Cut tape; choose MOQ1'),
 'C6':('PCE5231-ND',566,'1.89','USD','3 weeks','Bulk'),
 'R7':('PPCQF390KCT-ND',17138,'1.40','PLN','2 months','Cut tape'),
 'R8':('',60541,'0.38','PLN','last month','Cut tape; SKU not directly observed, verify MPN')}
tmeprice={'RV1':'.89','BR1':'2.18','C1':'3.21','U1':'1.75','R4':'.40','R6':'.095','D1':'1.34'}
rows=[]
for r in source:
 ref=r['Reference']
 if ref in ['J1','J2','R9']:continue
 qty=2 if ref=='R8' else 1;refs='R8,R9' if ref=='R8' else ref
 row={'refs':refs,'mpn':r['MPN'],'value':r['Value'],'qty_fitted':qty,'purchase_qty_min':100 if ref=='R6' else qty,'moq':100 if ref=='R6' else 1,'multiple':100 if ref=='R6' else 1,'supplier':'TME' if ref in tmeprice else 'DigiKey','url':urls[ref],'manufacturer_source':r['Source'],'vat_rate_assumed':'.23','observed_on':'2026-11-24','assembly_note':''}
 if ref in tmeprice:
  e=live[ref];prod=e['products'][0];row.update(supplier_sku=prod['sku'],observed_stock=prod['offers']['inventoryLevel'],unit_net=tmeprice[ref],currency='PLN',evidence_freshness='LIVE_DIRECT',evidence_file=ref+'.html',evidence_utc=e['captured_utc'],package_to_buy='Cut tape or individual part; no full reel',indexed_age='')
 else:
  sku,stock,price,cur,age,pack=dk[ref];row.update(supplier_sku=sku,observed_stock=stock,unit_net=price,currency=cur,evidence_freshness='SUPPLIER_INDEXED_NOT_LIVE',evidence_file='indexed-evidence.json',evidence_utc='',package_to_buy=pack,indexed_age=age)
 if ref=='C6':row['price_source_url']='https://www.digikey.com/en/products/detail/panasonic-industry/EEU-FS2A151/9597035';row['assembly_note']='EEUFS2A151 / EEU-FS2A151 same manufacturer part punctuation; do not substitute B suffix without review. Polish PLN quote remains missing.'
 if ref=='L1':row['assembly_note']='PR02-FS 100 ohm resistor at legacy L1 position. DO NOT BUY old 768772332 choke. Upright manual lead forming.'
 if ref=='U1':row['assembly_note']='SO8 tube exact LYT1603D; NRND, TME stock exhaustion notice. Recommended buy 3 total.'
 if ref=='R6':row['assembly_note']='100 minimum purchase, 1 fitted, 99 spare automatically. TME stock exhaustion notice. Embedded public-page price .095 PLN net; display rounds to .10 PLN.'
 row['ext_net']=str(D(row['unit_net'])*row['purchase_qty_min']);row['ext_gross_assuming23']=str(D(row['ext_net'])*D('1.23'));row['optional_spares_add']=2 if ref in ['RF1','L1','U1','BR1','D1'] else 0
 rows.append(row)
over=H/'live-overrides.json'
if over.exists():
 for row in rows:
  x=json.loads(over.read_text(encoding='utf-8')).get(row['refs'])
  if x:row.update(x);row['ext_net']=str(D(row['unit_net'])*row['purchase_qty_min']);row['ext_gross_assuming23']=str(D(row['ext_net'])*D('1.23'))
totals={}
for supplier in ['TME','DigiKey']:
 totals[supplier]={}
 for cur in ['PLN','USD']:
  totals[supplier][cur+'_net']=str(sum((D(r['ext_net']) for r in rows if r['supplier']==supplier and r['currency']==cur),D(0)))
body={'revision':'SB01 R2 purchasing candidate','actor':'/root/r2_purchasing','date':'2026-11-24','source_revision':'872adddb3da9b3dbfa57e5c81ef7ba51da2a841c','status':'PROPOSED_FOR_COORDINATOR_REVIEW_NOT_ORDERED','scope':'Power PCB only. 17 fitted electronic parts /16 unique MPNs, excludes LED module, bare PCB and consumables. J1/J2 bare solder ports are not connectors.','parts':rows,'totals':totals,'shipping':{'TME':{'source':'https://www.tme.eu/pl/how-to-buy/7428/Sposob-i-koszty-transportu/','standard_gross_PLN':'17.10','Pocztex_gross_PLN':'12.18','condition':'Prepaid domestic parcel below25kg/value10000PLN for Pocztex; no COD.'},'DigiKey':{'source':'https://www.digikey.pl/pl/help-support/delivery-information/delivery-time-and-cost','below_300PLN_shipping_published_PLN':'80','conservative_gross_budget_PLN':'98.40','shipping_VAT_status':'Policy does not explicitly identify VAT inclusion of80PLN;98.40assumes23%;checkout required.','DDP':'UPS/FedEx prepaid; avoid marketplace and unbudgeted CPT charges.'}},'unresolved':['DigiKey directHTTP403; indexed stock is not present-day reservation. Coordinator browser facts may supersede.','C6 Polish PLN price not yet directly observed; no exact all-PLN quote may be claimed.','Checkout final delivery/VAT/price and stock need confirmation; no purchase action taken.'],'canonical_sources_sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['bom-build.csv','procurement.SB01.json','SC09_compact.kicad_pcb','SC09_compact.kicad_sch']}}
(H/'purchase-plan.json').write_text(json.dumps(body,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
keys=list(dict.fromkeys(k for r in rows for k in r))
with (H/'purchase-bom.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
print(json.dumps(totals));print('fitted',sum(r['qty_fitted'] for r in rows),'unique',len(rows))
