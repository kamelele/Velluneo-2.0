from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'work/Velluneo-2.0'; S=R/'hardware/E27/variants/integrated-shade/SC09_compact'; W=R/'hardware/E27/workflow/integrated-shade/compact-09'; P=W/'prototype-package'; O=ROOT/'outputs/Velluneo_SC09_PCB'
P.mkdir(exist_ok=True); (P/'checks').mkdir(exist_ok=True); (P/'views').mkdir(exist_ok=True); (P/'fabrication').mkdir(exist_ok=True)
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
h=load(S/'hardware.json'); h['netclasses'][0]['track_width']=.3
h['source_files']=sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file() and not any(x in p.relative_to(S).parts for x in ['.work','.electronics-rules','__pycache__']) and p.suffix not in ['.kicad_prl','.bak'])
save(S/'hardware.json',h)
g=load(S/'footprint-geometry.json')
g['R7']['courtyard_polygon_mm']=[[-1.5,-1.5],[1.5,-1.5],[1.5,1.5],[1.25,1.5],[1.25,6.05],[-1.25,6.05],[-1.25,1.5],[-1.5,1.5]]
for ref in ['J1','J2']:
 g[ref].pop('courtyard_polygon_mm',None)
 g[ref]['courtyard_polygons_mm']=[[[p['center_mm'][0]+dx,p['center_mm'][1]+dy] for dx,dy in [(-p['size_mm'][0]/2-.25,-p['size_mm'][1]/2-.25),(p['size_mm'][0]/2+.25,-p['size_mm'][1]/2-.25),(p['size_mm'][0]/2+.25,p['size_mm'][1]/2+.25),(-p['size_mm'][0]/2-.25,p['size_mm'][1]/2+.25)]] for p in g[ref]['pads']]
save(S/'footprint-geometry.json',g)
b=load(S/'bom-build.json'); b['status']='Exact populated CAD candidate for manually assembled laboratory prototype; procurement and qualification open.'; save(S/'bom-build.json',b)
t=load(S/'thermal-planning.json'); t['total_driver_loss_planning_W']=[.9,1.7];t['not_additive_guarantee']='Updated planning allocation after custom 180-turn T1. Not a proven upper bound; RF1 RMS input, magnetics core loss, switching loss and capacitor ripple require measurement. Reference-board efficiency is not inherited.'
for c in t['component_screens']:
 if c['ref']=='T1': c.update(proposed_DCR_max_25C_ohm=2.7,proposed_DCR_max_100C_ohm=3.6,proposed_core_loss_budget_W=.4,copper_screen_at_300mA_W=.324,total_planning_budget_W=.724,qualification='Supplier-built custom 180-turn AWG32 coil is not measured; saturation during IC maximum fault current remains unresolved.')
 if c['ref']=='R8A_R8B': c['ref']='R8_R9'
save(S/'thermal-planning.json',t)
spatial={'revision':'SC09-routed-lab-50x32','status':'Engineering placement review, NOT an approved Toolkit spatial contract','outline_mm':[50,32],'board_thickness_mm':1.6,'front_contract_max_mm':15,'bottom_contract_max_mm':2.9,'overall_contract_max_mm':19.5,'original_target_mm':[50,25,20],'size_deviation':'Width is 7 mm greater than the earlier proposed maximum. Ordinary bulb cavity fit is NOT demonstrated; do not claim target met.','C6':{'body_projection_relative_mm':[6.5,.25,28.5,13.25],'vent_reserve_mm':5,'front_no_copper_projection_relative_mm':[6.5,.25,33.5,13.25],'interpretation':'Back copper behind intact FR4 is allowed only as documented engineering interpretation. No sleeve insulation credit. Verify formed leads, support and vent volume physically.'},'power_loop':['C4.1','U1.4','U1 SOURCE','R5/R6','T1.8','D1.1','D1.2','C4.2'],'kelvin':'Separate R5/R6 sense branch to U1.3; power-current branch to T1/D1 remains separate until sense resistor junction. See critical-routing.json.','returns':'C5 BP/SOURCE local bypass, SOURCE connected thermal planes and dedicated through via, D1 anode/DC_RETURN planes. No SELV return.','spacing':'All 55 net pairs independently screened; finite SO8/bridge/SMA package-land concessions explicitly bounded and not IEC insulation qualification.','assembly':'Manual prototype; two bare-wire interfaces, custom formed R7/RF1/C6 and custom T1 require actual jig/sample fit verification.','formal_spatial_gate':'hardware.product.spatial_file remains null. No fabricated approval digest or unsupported chamfered-outline contract.'}
save(P/'spatial-review.json',spatial)
save(P/'track-width-rationale.json',{'change':'POWER preferred track width .4 to .3 mm; global floor unchanged .3 mm','basis':'35 um copper, .3 mm width -> .0105 mm2. A 100 mm trace has approximately .164 ohm at 20C, .213 ohm at 100C. At .1352 A approximately 3.9 mW/100mm hot. At planning .3 A RMS approximately 19.2 mW/100mm hot. Pulse/fault limits remain component/prototype qualification questions.','calculation':'rho_Cu=.01724 ohm mm2/m; alpha=.00393/K. Not an IPC temperature-rise certification.','critical_paths':'Wider .4/.6 mm SOURCE branches retained; exact widths captured from native PCB.'})
for name in ['SC09_przod_3D.png','SC09_tyl_3D.png']: shutil.copy2(O/name,P/'views'/name)
for name in ['checker.py','kernel_sc08.py','tests.py']:
 (P/'validation').mkdir(exist_ok=True);shutil.copy2(ROOT/'work/compact09/checker'/name,P/'validation'/name)
shutil.copy2(ROOT/'work/compact09/checker/root-lab-functional-assessment-v5.json',P/'validation/package-land-assessment.json')
shutil.copy2(ROOT/'work/compact09/spacing-thermal/spacing-contract.proposed.json',P/'validation/spacing-matrix.json')
print(P)
