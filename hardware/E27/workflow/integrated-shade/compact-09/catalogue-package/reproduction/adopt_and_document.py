from pathlib import Path
import json,csv,hashlib,shutil,math
H=Path(__file__).resolve().parent;ROOT=H.parents[2];R=ROOT/'work/Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';W=R/'hardware/E27/workflow/integrated-shade/compact-09';P=W/'catalogue-package';O=ROOT/'outputs/Velluneo_SC09_catalogue'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert load(H/'private-final-DRC.json')['violations']==[]
assert load(H/'thermal-spacing.json')['passed']
# Preserve original published inputs locally before the sole-writer adoption.
backup=H/'published-1705-backup';backup.mkdir(exist_ok=True)
for p in S.rglob('*'):
 if p.is_file() and '.work' not in p.relative_to(S).parts:
  d=backup/p.relative_to(S);d.parent.mkdir(parents=True,exist_ok=True)
  if not d.exists():shutil.copy2(p,d)
for p in (H/'project').rglob('*'):
 rel=p.relative_to(H/'project')
 if p.is_file() and not any(x in rel.parts for x in ['.work','__pycache__','release-candidate']) and p.suffix!='.kicad_prl':
  d=S/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
for d in ['checks','validation','views','fabrication','research','reproduction']: (P/d).mkdir(parents=True,exist_ok=True)
for n in ['T1-research.json','U1-L1-procurement.json','parts-procurement.json','selected-parts-electrical.json','capture-pin-review.json','catalogue-model-results.json','thermal-guards.json']:
 shutil.copy2(H/n,P/'research'/n)
for dirname in ['T1-sources','U1-L1-sources']:
 for p in (H/dirname).rglob('*'):
  if p.is_file():
   d=P/'research'/dirname/p.relative_to(H/dirname);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
for n in ['spacing-matrix.CAT01.json','package-assessment.CAT01.json']:shutil.copy2(H/n,P/'validation'/n)
for p in (H/'checker').glob('*.py'):shutil.copy2(p,P/'validation'/p.name)
for n in ['test-results.json']:shutil.copy2(H/'checker'/n,P/'checks'/n)
for n in ['SC09_CAT_przod_3D.png','SC09_CAT_tyl_3D.png']:shutil.copy2(O/n,P/'views'/n)
for p in H.glob('*.py'):shutil.copy2(p,P/'reproduction'/p.name)
bom=load(S/'bom-build.json');parts=load(H/'parts-procurement.json')['parts'];u=load(H/'U1-L1-procurement.json');rows=[]
for part in parts:
 refs=part['refs']
 if refs==['R7']:v=part['alternative'];mpn=v['MPN']
 else:
  choices=[v for v in part['sources'] if v.get('stock',v.get('stock_displayed_in_retrieved_distributor_page',0))]
  assert choices,refs
  v=next((v for v in choices if v.get('live_HTTP_verified')),choices[0]);mpn=part['current_MPN']
 rows.append({'References':','.join(refs),'Qty_per_PCB':len(refs),'MPN':mpn,'Vendor':v['vendor'],'Vendor_code':v.get('catalogue_id',''),'Buy_URL':v['direct_product_url'],'Datasheet_URL':next(c['source'] for c in bom['components'] if c['ref']==refs[0]),'MOQ':v.get('MOQ',1),'Multiple':v.get('multiple',1),'Observed_stock':v.get('stock',v.get('observed_indexed_stock',v.get('stock_displayed_in_retrieved_distributor_page',''))),'Evidence':'fresh public HTTP exact MPN' if v.get('live_HTTP_verified') else 'retrieved/indexed vendor listing; NOT live checkout stock','Observed_or_age':v.get('observed_utc',v.get('source_crawl_age_displayed','2026-11-21 research; age in source report'))})
v=u['U1']['purchase_path'];rows.append({'References':'U1','Qty_per_PCB':1,'MPN':'LYT1603D-TL','Vendor':'LCSC','Vendor_code':'C567687','Buy_URL':v['url'],'Datasheet_URL':u['U1']['technical_primary'],'MOQ':1,'Multiple':1,'Observed_stock':10,'Evidence':'fresh public HTTP exact MPN; NRND; JLC PCBA MOQ19 exceeds observed10','Observed_or_age':'2026-11-21 11:22 UTC'})
v=u['L1']['catalogue_purchase_paths'][0];rows.append({'References':'L1','Qty_per_PCB':1,'MPN':'768772332','Vendor':'DigiKey','Vendor_code':v['part_code'],'Buy_URL':v['url'],'Datasheet_URL':'https://www.we-online.com/components/products/datasheet/768772332.pdf','MOQ':1,'Multiple':1,'Observed_stock':142,'Evidence':'indexed exact vendor listing; direct live HTTP blocked','Observed_or_age':'2026-11-21 research; age in source report'})
rows.append({'References':'T1','Qty_per_PCB':1,'MPN':'MSS1210H-125KED','Vendor':'Coilcraft','Vendor_code':'MSS1210H-125KED','Buy_URL':'https://www.coilcraft.com/en-us/products/power/high-voltage-inductors/mss-mos-%281%29/mss1210h/mss1210h-125/','Datasheet_URL':'https://www.coilcraft.com/getmedia/52078704-21eb-4c2b-9b72-1e07b4a2e252/mss1210h.pdf','MOQ':1,'Multiple':1,'Observed_stock':1077,'Evidence':'manufacturer feed via Findchips; NOT directly live confirmed. Catalogue price USD3.68 qty1, no RFQ/custom winding','Observed_or_age':'2026-11-21 research; feed crawled about5days earlier'})
for r in rows:
 for n in [1,5,10]:r['Buy_qty_for_'+str(n)+'_PCBs']=max(r['MOQ'],math.ceil(r['Qty_per_PCB']*n/r['Multiple'])*r['Multiple'])
assert len(rows)==16 and sum(r['Qty_per_PCB'] for r in rows)==17
assert {ref for r in rows for ref in r['References'].split(',')}=={c['ref'] for c in bom['components'] if c['ref'] not in ['J1','J2']}
rows.sort(key=lambda r:r['References']);save(P/'SC09_catalogue_buy_list.json',{'revision':'SC09-CAT01','date':'2026-11-21','all_electrical_references_covered':True,'stock_reserved':False,'all_live_verified':False,'JLC_full_PCBA_confirmed':False,'parts':rows})
with (P/'SC09_catalogue_buy_list.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
shutil.copy2(S/'bom-build.csv',P/'SC09_BOM.csv');shutil.copy2(S/'bom-build.json',P/'SC09_BOM.json')
hw=load(S/'hardware.json');hw['product']['special_requirements']=[x for x in hw['product']['special_requirements'] if 'CustomT1' not in x]+['SC09-CAT01catalogueT1;noone-offwinding;normalmanualaxialleadformingandsampleinspectionremain'];save(S/'hardware.json',hw)
for n in ['T1-custom-contract.json','bom-proposal.json','source-basis.json']:
 p=S/n
 if p.exists():
  d=load(p);d['historical_status']='SUPERSEDED by SC09-CAT01; NOT current procurement, pin mapping, assembly or release evidence. See source-basis.CAT01.json and bom-build.json.';save(p,d)
req=load(S/'requirements.json');req['revision']='SC09-CAT01';req['catalogue_revision_notice']='Existing EV-* and A/A1 approvals are historical and not approval of changed CAT01 pins/parts. Active current evidence: catalogue-engineering-status.json. Full product release is not passed.'
for q in req['requirements']:
 if q['id'] in ['C_ARCH','C_PARTS','C_GRAPH','C_PROTECTION','C_PACKINGCOST']:
  q['previous_acceptance_historical']=q['acceptance'];q['revision']='SC09-CAT01';q['evidence_ids']=[]
  q['acceptance']={'C_ARCH':'Catalogue nonisolated laboratory buck with19references46physicalpins11nets; no invented current human approval.','C_PARTS':'17electronics/16unique catalogueMPNs with exact manufacturer ratings and individually graded supplier offers; live availability recheck before purchase. No custom-wound T1.','C_GRAPH':'Independent CAT01 intent46pins0NC agrees with fresh schematic export and PCB; new graph approval remains null.','C_PROTECTION':'Recalculate chosen catalogue magnetic/R7 corners, clearly separate paper screens from unperformed fault/surge/thermal qualification.','C_PACKINGCOST':'50x32mm PCB, estimated module50x32x19.5mm; normal manual assembly, supplier price/stock not reserved.'}[q['id']]
save(S/'requirements.json',req)
status={'revision':'SC09-CAT01','owner_request':'owner-catalogue-only-request.json','current_BOM':'bom-build.json','current_intent':'intended-connectivity.CAT01.json','current_intent_human_approval':None,'authority':'Actualownerautonomousengineeringandcatalogue-onlyrequest; individualstageapprovalsarenotfabricated.','historical_sources':'SC09-A/A1 approvals, customT1 contracts and previous proposals remain historical; never apply to CAT01.','current_research_package':'../../../../workflow/integrated-shade/compact-09/catalogue-package/research','full_product_release_passed':False,'physical_tests_performed':False,'order_placed':False}
save(S/'catalogue-engineering-status.json',status)
(S/'README.md').write_text('# SC09-CAT01 catalogue-only laboratory driver\n\nCurrent KiCad sources retain the SC09_compact basename. Current map is intended-connectivity.CAT01.json:19references,46pins,11nets,0NC. T1 is standard Coilcraft MSS1210H-125KED, two SMD terminals; L1 is Wurth768772332; R7 is VishayHVR2500003903FR500. No custom winding. Prior A/A1 custom-coil maps, approvals and proposals are historical and do not authorize these changed pins.\n\n50x32mm board, approximately19.5mm assembled envelope; nonisolated mains-referenced laboratory prototype only. Current package and source-bound checks: hardware/E27/workflow/integrated-shade/compact-09/catalogue-package in the repository. All17 electrical positions have catalogue purchase paths; J1/J2 are bare wire lands. Catalogue offers and fresh live stock are distinguished, no cart/reservation/order or full JLC PCBA qualification claimed.\n\nCAT01 graph approval remains null. FullToolkit release is not passed. Current engineering checks cannot establish physical temperatures, surge/fault performance or finished lamp safety. Normal manual lead forming/support/sample inspection of RF1/R7/C6 and qualified guarded measurements remain required. See catalogue-engineering-status.json.\n',encoding='utf-8')
for n in ['symbol-pin-verification.json']:
 p=S/n
 if p.exists():
  d=load(p);d['catalogue_revision']='SC09-CAT01';d['current_graph']='intended-connectivity.CAT01.json';d['historical_notes']='Any prior custom-winding contract statement is superseded. No new human graph approval claimed.';save(p,d)
(P/'README.md').write_text('# SC09-CAT01 catalogue-only engineering package\n\nCurrent revision replaces the custom coil. Use ONLY this catalogue-package with current SC09_compact KiCad sources. The sibling prototype-package and its older ZIPs are historical custom-T1 artwork and are not interchangeable.\n\nBoard50x32mm,2layers,1.6mmFR4,1oz,lead-freeHASL,manualassembly,no stencil. Nominal230V50Hz207–253V screen;20seriesLEDs,~60V,~133.44mAexternal LED current,~8.006W; regulated total135.20mA includes1.765mAbleeders. Nonisolated output is mains referenced.\n\nSC09_catalogue_buy_list.csv/JSON/PDF covers17electronic positions/16uniqueMPNs with supplier URLs, MOQs and evidence freshness. Seven uniqueMPNs have freshLCSCstock; remaining offers are distributor/manufacturer listings, not all live checkout confirmations. T1 manufacturerfeed reports stock; directlive confirmation unavailable. U1 is NRND and only10observed atLCSC; JLCMOQ19 is NOT a confirmed PCBA path. No custom winding, no orders or supplier messages.\n\nNative CAD checks, independent bounded geometry checks and source-bound manufacturing exports are provided for engineering review. FullToolkit release remains FAIL: physical qualification and exact CAT01 stage approval are absent; oldA1 approval is not transferred. No declaration of a qualified supply/finished bulb or unconditional order release. Before any board purchase inspect supplier CAM and the current fabrication-readiness record.\n',encoding='utf-8')
(P/'OPEN_ITEMS.md').write_text('# Explicit remaining checks\n\n1. Recheck actual stock/checkout for every exactMPN, especially manufacturer-directT1 and low-stockNRNDU1. Listings are not reserved. No fullJLCPCBA route is confirmed.\n2. Actual CAT01 human stage approval and completeToolkitproductgates are absent; priorA1 is historical. FullreleaseFAIL is explicit.\n3. SupplierCAMpreview/process acceptance before bareboardcheckout; no purchase made.\n4. Cataloguepart sample fit, RF1/R7/C6 normal manualleadforming, supports/vent/wire strainrelief and solder protrusion. R7planned11.5mm; overall19.5mm remains MOV dominated.\n5. Guarded qualified laboratory measurements: LEDcurrent/ripple, openloaddynamicOVP≤90Vtarget, one-open discharge, temperatures0–40Cambient, hot DCbias/coreloss, startup/fault/surge/EMC/insulation. None performed.\n6. No hotplug/dimming; disconnect and discharge before changing LED module. All conductors are mains referenced; enclosure accessibility and finishedlamp qualification remain outside this bare prototype.\n',encoding='utf-8')
shutil.copy2(W/'prototype-package/BRINGUP.md',P/'BRINGUP.md')
with (P/'BRINGUP.md').open('a',encoding='utf-8') as f:f.write('\n\nCAT01 supersedes every customT1 sample/winding task with factoryMSS1210H-125KED sample/rating/fit inspection. Use currentcatalogue-part electricalreport; noVR25thermalresistance transfer toHVR25. No poweredtestsperformed or authorizedbythisdocument.\n')
shutil.copy2(W/'prototype-package/order-parameters.json',P/'order-parameters.json')
(W/'CURRENT_PACKET.md').write_text('# Current packet: SC09-CAT01 catalogue-only\n\nUse catalogue-package/README.md and current SC09_compact CAD. The older prototype-package, order-review-inputs, customT1 contracts and old SC09_Pakiet_prototyp_lab.zip are historical1705d20/customcoil scope and do not fit the new catalogueT1. CAT01 removes customwinding; changed physicalpin map requires fresh checks and does not inheritA1humanapproval. Root is soleCADwriter; main outsidewrite scope.\n',encoding='utf-8')
print('Adopted catalogue CAD;16 purchasing rows/17electricalrefs; historical package explicitly retained, not current.')
