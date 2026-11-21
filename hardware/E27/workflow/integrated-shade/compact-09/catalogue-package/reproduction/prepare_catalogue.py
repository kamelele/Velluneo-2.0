from pathlib import Path
import json,hashlib,shutil,csv
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];R=ROOT/'work/Velluneo-2.0';ORIG=R/'hardware/E27/variants/integrated-shade/SC09_compact';S=HERE/'project';S.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p in ORIG.rglob('*'):
 rel=p.relative_to(ORIG)
 if not p.is_file() or any(k in rel.parts for k in ['.work','release-candidate','__pycache__']) or p.suffix=='.kicad_prl':continue
 dest=S/rel;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,dest)
request={'actual_owner':'Kamil','date':'2026-11-21','actual_quote':'Wszystkie elementy zasilacza musza byc dostepne do zamowienia, najlepiej od razu z kart katalogowych jlcpcb ale jesli to bedzie problem to nie jest to mus','scope':'Catalogue-orderable electronics only; no one-off/custom-wound T1. PreferJLCPCB/LCSC,othercommercialsuppliersallowed. Prior50x32/manualprototype/process/autonomousengineeringauthorityretained.','not_inferred':['actualpurchase','allpartsinJLCPCBAstock','snapshot-boundindividualmapapproval','powered-testorproductqualification']};save(S/'owner-catalogue-only-request.json',request)
bom=load(S/'bom-build.json');bom['revision']='SC09-CAT01';bom['status']='Engineering catalogue-only revision. Source offers have individually graded freshness; no reservation/cart/order claimed.'
for c in bom['components']:
 if c['ref']=='T1':
  c.update(mpn='MSS1210H-125KED',value='1.2mH 10% 400V',kind='inductor',pins={'1':'LED_PLUS','2':'FB_INDUCTOR'},source='https://www.coilcraft.com/getmedia/52078704-21eb-4c2b-9b72-1e07b4a2e252/mss1210h.pdf',package='2-terminal SMD,12.3x12.3x10.2max',body_or_reservation_mm=[12.3,12.3,10.2],notes='Standard catalogue Coilcraft part; no custom winding. ManufacturerMOQ1price$3.68;Findchipsmanufacturerfeedreports1077,notdirectliveconfirmed/reserved. Confirm actualvendoravailabilityatcheckout. ±10%L/bias/hotpaper assumptionsnotmeasurement.',assembly='Manufacturerrecommendedtwo5.5x3.0mmpadsat0,±4.75;nonpolarcoil;designpin1LED/pin2FB.No3rdpinorNC.')
 if c['ref']=='L1':c.update(mpn='768772332',value='3.3mH 10% 400V',source='https://www.we-online.com/components/products/datasheet/768772332.pdf',package='radialP5,8.3diameterx10max',body_or_reservation_mm=[8.3,8.3,10.5],notes='WurthWE-TIHVcatalogue400V;DCR7.08ohmmax@20C,Irms.25A,Isat.27A@10%;normalmanualfreeleadformingandfitinspection. DCRlossdelta~2.18mW@100C60mARMSvsoldRenco.',assembly='P5manufacturerrecommended1.2holes;retaincompatibleP5.0038landpattern. Leadpitchtolerancehandledbygentlefreeleadadjustment,notrigidguarantee.')
 if c['ref']=='R7':c.update(mpn='HVR2500003903FR500',source='https://www.vishay.com/docs/30260/hvr2537.pdf',notes='StandardcatalogueHVR25replacement390k1%/.25W/1600VDC/200ppm;bodyL2max7.5,D2.5,lead.58±.05. RetainstandingP4.8forming. UseHVRaging/deratingdata;doNOTtransferVR25theta140K/W.',assembly='StandingP4.8manualleadformingfromcataloguepart;existingphysicalenvelopeconservative. Sampleinspectionbeforeassemblyacceptance.')
save(S/'bom-build.json',bom)
with (S/'bom-build.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Quantity','MPN','Value','Footprint','Assembly','Primary source'])
 for c in bom['components']:w.writerow([c['ref'],1,c['mpn'],c['value'],'E27SC09:SC09_'+c['ref'],c.get('assembly',''),c['source']])
basis={'revision':'SC09-CAT01','author':'/root,engineeringdesignimplementation','original_owner_A1_graph_sha256':sha(ORIG/'intended-connectivity.A1.json'),'design_change':'OnlyT1physicalterminalmappingchanges8→2andremovesunwound4;selectedstockL1/R7keep2terminalnonpolarfunctions. Expectedgraphdefinedfrommanufacturerterminaldataandapprovedfunctionalbaselinebeforecapture.','owner_request_file':'owner-catalogue-only-request.json','owner_request_sha256':sha(S/'owner-catalogue-only-request.json'),'selected_BOM_sha256':sha(S/'bom-build.json'),'research_inputs':[{'path':n,'sha256':sha(HERE/n)} for n in ['T1-research.json','U1-L1-procurement.json','parts-procurement.json','selected-parts-electrical.json']],'approval_scope':'Userauthorizesautonomouscatalogueengineering;noindividualhumanapprovalofthisnewexactgraphisfabricated.'};save(S/'source-basis.CAT01.json',basis)
g=load(ORIG/'intended-connectivity.A1.json');g.update(revision='SC09-CAT01',basis=basis['design_change'],basis_sources=[{'path':n,'sha256':sha(S/n)} for n in ['source-basis.CAT01.json','bom-build.json','owner-catalogue-only-request.json']],no_connects=[],approval=None)
for c in g['components']:
 if c['ref']=='T1':c['units']=[{'name':'A','pins':['1','2']}]
for net in g['nets']:
 for p in net['pins']:
  if p['ref']=='T1' and p['pin']=='8':p['pin']='2'
assert sum(len(n['pins']) for n in g['nets'])==46
save(S/'intended-connectivity.CAT01.json',g)
hw=load(S/'hardware.json');hw['product']['connectivity_file']='intended-connectivity.CAT01.json';hw['release_files']={};save(S/'hardware.json',hw)
# Adapt the authoring program, retaining original component/sheet IDs and actual power source types.
t=(HERE.parent/'capture.py').read_text();t=t.replace("S=R/'hardware/E27/variants/integrated-shade/SC09_compact'","S=Path(__file__).resolve().parent/'project'").replace("W=R/'hardware/E27/workflow/integrated-shade/compact-09'","W=Path(__file__).resolve().parent/'capture-evidence'")
t=t.replace('root=Path(__file__).resolve().parents[1]','root=Path(__file__).resolve().parents[2]')
t=t.replace("g=load(S/'intended-connectivity.A1.json')","g=load(S/'intended-connectivity.CAT01.json')")
t='\n'.join(line for line in t.splitlines() if not line.startswith('assert dg==') and not line.startswith("assert load(S/'owner-A1-map-approval"))
t=t.replace("elif k=='inductor':art=poly(","elif k=='inductor':\n  if r=='T1':p={'2':(-7.62,0,0),'1':(7.62,0,180)}\n  art=poly(")
t=t.replace("route(pp('R5','2'),pp('T1','8'))","route(pp('R5','2'),pp('T1','2'))")
t='\n'.join(line for line in t.splitlines() if not line.startswith("items.append(f'(no_connect(at {pp(\"T1\",\"4\")"))
t=t.replace("'T1':'1mH / EE10'","'T1':'1m2 / 400V catalogue'").replace("'R7':'390k / VR25'","'R7':'390k / HVR25'")
t=t.replace('VELLUNEO SC09-A | COMPACT NON-ISOLATED LED DRIVER | WORKING SCHEMATIC','VELLUNEO SC09-CAT01 | CATALOGUE NON-ISOLATED LED DRIVER | WORKING SCHEMATIC').replace('nominal 135 mA / 60 V / 8.1 W','total ~135 mA, LED ~133 mA / 60 V / ~8 W LED')
t=t.replace('T1: single winding, 180 turns AWG32 (custom contract); pins 1-8; pin 4 retained unwound NC. NOT an isolation transformer.','T1: catalogue MSS1210H-125KED, 1.2mH / 400V, two SMD terminals. No custom winding; NOT an isolation transformer.')
t=t.replace('Nominal LED current = (0.279 / 0.57321) / 3.6 = 135.2 mA; actual corners unmeasured.','Estimated total = 135.2 mA; LED ~133.4 mA at 60 V after bleeders; actual corners unmeasured.')
t=t.replace('Local footprints: manufacturer lands plus explicit custom T1/RF1 assembly contracts. Physical winding, forming and temperature qualification remain required.','Catalogue T1/L1/HVR25 and manufacturer lands; manual lead forming for RF1/R7/C6. Stock/thermal/fault qualification remain separate.')
t=t.replace('Velluneo SC09-A compact driver working schematic','Velluneo SC09-CAT01 catalogue driver working schematic').replace('SC09-A1 draft','SC09-CAT01 engineering')
t=t.replace("'actual_approved_intent_digest':dg","'engineering_intent_digest':dg").replace("'physicalpins':47,'NC':1","'physicalpins':46,'NC':0").replace('Generated19symbols/47pinsworkingSC09schematic','Generated19symbols/46pinscatalogueSC09schematic')
(HERE/'capture_stock.py').write_text(t+'\n',encoding='utf-8')
notice='SC09 custom-T1 package does not satisfy the new catalogue-only requirement. CAT01 is being engineered; do not order the previous board expecting the stock T1 to fit. Commit1705d20 results remain historical and apply only to that custom-coil revision. No order placed.\n';(ROOT/'outputs/Velluneo_SC09_PCB/SC09_catalogue_redesign_notice.txt').write_text(notice)
print('Privatecatalogueprojectprepared:19references/46pins/11nets/0NC;customerCADunchanged')
