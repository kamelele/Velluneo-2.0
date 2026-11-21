from pathlib import Path
import json,hashlib,math,pcbnew as k
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';Q=ROOT/'work/compact09/order-closure'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
p=S/'SC09_compact.kicad_pcb';oldsha=hashlib.sha256(p.read_bytes()).hexdigest();b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(p));before={(f.GetReference(),a.GetNumber()):(a.GetNetname(),a.GetPosition().x,a.GetPosition().y,a.GetSize().x,a.GetSize().y) for f in b.GetFootprints() for a in f.Pads()}
for f in b.GetFootprints():
 if f.GetReference()=='T1':
  for pad in f.Pads():pad.SetDrillSize(k.VECTOR2I(k.FromMM(1.2),k.FromMM(1.2)))
lib=k.FootprintLoad(str(S/'E27SC09.pretty'),'SC09_T1')
for pad in lib.Pads():pad.SetDrillSize(k.VECTOR2I(k.FromMM(1.2),k.FromMM(1.2)))
k.FootprintSave(str(S/'E27SC09.pretty'),lib);assert k.SaveBoard(str(p),b,True)
assert before=={(f.GetReference(),a.GetNumber()):(a.GetNetname(),a.GetPosition().x,a.GetPosition().y,a.GetSize().x,a.GetSize().y) for f in b.GetFootprints() for a in f.Pads()}
g=load(S/'footprint-geometry.json')
for pad in g['T1']['pads']:pad['drill_mm']=1.2
g['T1']['root_hole_fit_revision']='All3finishedholes1.20mm; unchanged1.8mmlands,pincoordinates,nets. Radialcoilpositiontol.15; seeT1contract.';save(S/'footprint-geometry.json',g)
t=load(S/'T1-custom-contract.json');t['revision']='T1-EE10-CONTRACT-03-180T-RADIAL-FIT';d=t['designed_mechanical_requirements'];d['terminal_position_tolerance_convention']='Maximum RADIAL displacement of each terminal centre from nominal top-view coordinate<=0.15mm. This is a custom supplier acceptance requirement, not observed finished-part capability.';d['PCB_pad_selection']='FinishedPTH1.20mm,roundcopperland1.80mm. Samepins1/4/8andcoordinates. Requirephysical3pingo-no-gogauge; do notforceanonmatchingcoil.'
report={'before_sha256':oldsha,'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'finished_hole_nominal_mm':1.2,'assumed_hole_minus_tolerance_mm':.08,'pin_diameter_max_mm':.55,'coil_position_radial_max_mm':.15,'PCB_position_assumed_per_axis_mm':.075,'PCB_position_radial_worst_mm':math.sqrt(2)*.075,'available_radial_clearance_mm':(1.2-.08-.55)/2,'combined_radial_error_mm':.15+math.sqrt(2)*.075,'radial_fit_reserve_mm':(1.2-.08-.55)/2-.15-math.sqrt(2)*.075,'nominal_annulus_mm':(1.8-1.2)/2,'annulus_at_plus0p13_drill_before_registration_mm':(1.8-1.33)/2,'basis':'https://jlcpcb.com/capabilities/pcb-capabilities, hole+0.13/-0.08mm,position±.075mm; conservativeper-axisPCBinterpretation. Coilpositionclarifiedradialexplicitcustomcontract. Noqualificationofactualsupplierpartorindependentregistrationclaim.','unchanged':'All47pins,nets,centres,outercopperpadgeometryunchanged.'}
d['hole_fit_arithmetic']=report;save(S/'T1-custom-contract.json',t);save(Q/'T1-hole-fit.json',report);print(json.dumps(report))
