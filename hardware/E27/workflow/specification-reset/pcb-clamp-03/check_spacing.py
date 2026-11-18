"""Independent nominal package gap derivation; no standards/process qualification."""
from pathlib import Path
import json,math,itertools,hashlib
D=Path(__file__).resolve().parent;P=D.parent
inventory={p['ref']:p for p in json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'))['parts']}
pairs=[('BR1','1','3',1.5,'BULK_POS - PRIMARY_GND'),('Q1','1','2',1.1,'DRAIN - GATE'),('Q1','2','3',1.1,'DRAIN - SENSE'),('U1','6','7',1.94,'BULK_POS/HV - DRV'),('T1','1','2',2.6,'BULK_POS - PRIMARY_GND'),('T1','4','5',2.6,'DRAIN - AUX_RAW')]
rows=[]
for ref,a,b,expected,voltage in pairs:
 pads={p['pin']:p for p in inventory[ref]['pads']}
 def box(p):
  x,y=p['xy_mm'];w,h=p['size_mm'];return[x-w/2,y-h/2,x+w/2,y+h/2]
 aa,bb=box(pads[a]),box(pads[b]);gap=math.hypot(max(aa[0]-bb[2],bb[0]-aa[2],0),max(aa[1]-bb[3],bb[1]-aa[3],0));assert abs(gap-expected)<1e-8
 rows.append(dict(ref=ref,pins=[a,b],nominal_copper_bbox_gap_mm=gap,screen_mm=3,rigid_translation_rotation_side_invariant=True,voltage_difference=voltage,land_basis='raw-bobbin project proposal'if ref=='T1'else'retained manufacturer recommended land geometry',status='unresolved; no exemption or pass'))
print(json.dumps(dict(pairs=rows,unique_pairs=6,native_report_count=8,bulk_ideal_253Vac_crest_V=253*math.sqrt(2),aux_ideal_Qon_V=-253*math.sqrt(2)*22/120,bulk_minus_aux_ideal_Qon_V=253*math.sqrt(2)*(1+22/120),source_inventory_sha256=hashlib.sha256((P/'compact-60/mechanics/native-inventory.json').read_bytes()).hexdigest(),scope='Calculated nominal rigid geometry and ideal normal-voltage examples only. No transient/fault bound, solder/process/finished insulation qualification or permission to relax rules.'),indent=2))
