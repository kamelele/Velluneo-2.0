"""Named Q1 land-only refinement; same source pins, holes and centres."""
from pathlib import Path
import pcbnew,json
D=Path(__file__).resolve().parent;E=D/'design';L=E/'Velluneo_ECO04.pretty';old='STF2N80K5_Stagger5p08_PROJECT';new='STF2N80K5_Stagger5p08_Pad2p25_PROJECT'
f=pcbnew.FootprintLoad(str(L),old);assert f;f.SetFPID(pcbnew.LIB_ID('Velluneo_ECO04',new))
for p in f.Pads():assert p.GetShape()==pcbnew.PAD_SHAPE_CIRCLE and abs(pcbnew.ToMM(p.GetDrillSize().x)-1.5)<1e-9;p.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(2.25),pcbnew.FromMM(2.25)))
pcbnew.PCB_IO_KICAD_SEXPR().FootprintSave(str(L),f);assert(L/(new+'.kicad_mod')).exists()
p=E/'assignments.json';j=json.loads(p.read_text());j['Q1']['footprint']='Velluneo_ECO04:'+new;j['Q1']['status']='CONTROL05 named2.25mm-land refinement; same source pins/1.5mmholes/stagger; physical forming and process pending';p.write_text(json.dumps(j,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Q1 named2.25mm-land variant, unchangedholes/centres; fresh fullchecks required.')
