from pathlib import Path
from decimal import Decimal as D
import json,hashlib,datetime
H=Path(__file__).resolve().parent
plan=json.loads((H/'purchase-plan.json').read_text(encoding='utf-8'))
# A budgeting conversion is not a supplier PLN quote or an observed exchange rate.
base=sum((D(r['ext_net']) for r in plan['parts'] if r['currency']=='PLN'),D(0))
usd=sum((D(r['ext_net']) for r in plan['parts'] if r['currency']=='USD'),D(0))
vat=D('1.23');tm_ship=D('12.18');dk_ship_lo=D('80');dk_ship_hi=D('98.40')
scenarios=[]
for fx in ['4.00','4.50','5.00']:
 net=base+usd*D(fx);gross=net*vat
 scenarios.append({'USD_PLN_budget_assumption':fx,'not_live_exchange_rate':True,'parts_net_PLN':str(net),'parts_gross_PLN':str(gross.quantize(D('.01'))),'total_gross_PLN_shipping80':str((gross+tm_ship+dk_ship_lo).quantize(D('.01'))),'total_gross_PLN_shipping98_40':str((gross+tm_ship+dk_ship_hi).quantize(D('.01')))})
cost={'date':'2026-11-24','status':'BUDGET_ESTIMATE_NOT_CURRENT_QUOTE','scope':'One power PCB: exact selected electronics, MOQ excess, TME+DK prepaid shipping. Excludes barePCB/LED/consumables/labour.','known_PLN_net':str(base),'C6_USD_net':str(usd),'scenarios':scenarios,'practical_budget_gross_PLN':'180','budget_meaning':'Rough parts+shipping budget, not price guarantee; final supplier checkout overrides. Indexed DK prices may vary.','TME_C6_current':{'EEUFS2A151':{'stock':0,'MOQ':200,'multiple':200,'unit_net_PLN':'2.60','evidence':'c6-tme.json'},'EEUFS2A151B':{'stock':0,'MOQ':250,'unit_net_PLN':'2.90','evidence':'c6b-tme.json'},'decision':'Neither is a stocked 1-piece option. Retain exact unsuffixed C6 from DigiKey.'},'packaging_equivalence':{'base':'EEUFS2A151','permissible_packaging_option':'EEUFS2A151B','selected':False,'electrical_and_body':'100V150uF20%,105C10000h,1400mA100kHz,43mohm,12.5dia20long5pitch; same manufacturer table.','difference':'Bulk unformed bag versus standard ammo lead taping. Manual trimming/forming still must preserve manufacturer limits.','not_equivalent':'EEUFS2A151L/LB are10dia25long and1200mA44mohm; not approved.','primary_sources':['https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFS2A151','https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFS2A151B']},'limitations':['DigiKey current direct availability unverified: publicHTTP403. All DK numerical observations are supplier-indexed, dated explicitly.','C6 PLN supplier price still not observed; estimated conversion is separate from purchase BOM.','Shipping VAT80/98.40 handled as scenarios, not asserted final payable charge.']}
(H/'cost-estimate.json').write_text(json.dumps(cost,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
plan['all_parts_shipping_budget']='cost-estimate.json; estimate only;180PLNroughbudget'
plan['C6_TME_current']='exactunsuffixedstock0MOQ200;Bsuffixedstock0MOQ250;retainDKexactbaseMPN'
plan['unresolved']=['DigiKey directHTTP403; indexed stock is not present-day reservation.','C6 Polish PLN supplier price not directly observed: only separate budgeting conversion provided.','Final supplier stock, delivery/VAT and basket rounding require confirmation before purchase; no orders made.']
(H/'purchase-plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
d=json.loads((H/'handoff.json').read_text(encoding='utf-8'));d['status']='FROZEN_CANDIDATE_FOR_COORDINATOR_REVIEW';d['freeze_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();d['open']=cost['limitations'];d['deliverable_sha256']={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in H.iterdir() if x.is_file() and x.name!='handoff.json'}
(H/'handoff.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(scenarios));print('plan_sha256',d['deliverable_sha256']['purchase-plan.json'])
