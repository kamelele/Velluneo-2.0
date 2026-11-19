"""Isolated experimental plated-slot coupon; never changes main T1 assignment."""
from pathlib import Path
import pcbnew,json,shutil
D=Path(__file__).resolve().parent;S=D/'studies/t1-oval';S.mkdir(parents=True,exist_ok=True);E=D/'design';B='T1_oval_process_study';L=S/'Velluneo_T1Study.pretty';L.mkdir(exist_ok=True)
fp=pcbnew.FootprintLoad(str(E/'Velluneo_ECO04.pretty'),'TDK_EFD25_Pad2p0_PROJECT');assert fp
fp.SetReference('T1');fp.SetValue('UNADOPTED OVAL PROCESS STUDY');fp.SetFPID(pcbnew.LIB_ID('Velluneo_T1Study','TDK_EFD25_PlatedOval_STUDY'))
for p in fp.Pads():p.SetShape(pcbnew.PAD_SHAPE_OVAL);p.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(1.85),pcbnew.FromMM(2.15)));p.SetDrillShape(pcbnew.PAD_DRILL_SHAPE_OBLONG);p.SetDrillSize(pcbnew.VECTOR2I(pcbnew.FromMM(1.10),pcbnew.FromMM(1.35)))
pcbnew.PCB_IO_KICAD_SEXPR().FootprintSave(str(L),fp)
assert(L/'TDK_EFD25_PlatedOval_STUDY.kicad_mod').exists()
b=pcbnew.BOARD();b.Add(fp);fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(50),pcbnew.FromMM(50)));parts={p['ref']:p for p in json.loads((E/'proposed-parts.json').read_text())};nets={}
for p in fp.Pads():
 name=parts['T1']['pins'][p.GetNumber()]or'NC_'+p.GetNumber()
 if name not in nets:n=pcbnew.NETINFO_ITEM(b,'/'+name,len(nets)+1);b.Add(n);nets[name]=n
 p.SetNet(nets[name])
for a,z in[((30,30),(70,30)),((70,30),(70,70)),((70,70),(30,70)),((30,70),(30,30))]:
 g=pcbnew.PCB_SHAPE();g.SetShape(pcbnew.SHAPE_T_SEGMENT);g.SetLayer(pcbnew.Edge_Cuts);g.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[0]),pcbnew.FromMM(a[1])));g.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(z[0]),pcbnew.FromMM(z[1])));g.SetWidth(pcbnew.FromMM(.05));b.Add(g)
assert pcbnew.SaveBoard(str(S/(B+'.kicad_pcb')),b);shutil.copyfile(E/'Velluneo_specification_reset.kicad_pro',S/(B+'.kicad_pro'))
(S/(B+'.kicad_dru')).write_text('(version 1)\n(rule "T1_STUDY_FUNCTIONAL_3mm" (condition "(A.NetName == \'/BULK_POS\' && B.NetName == \'/PRIMARY_GND\') || (B.NetName == \'/BULK_POS\' && A.NetName == \'/PRIMARY_GND\') || (A.NetName == \'/AUX_RAW\' && B.NetName == \'/DRAIN\') || (B.NetName == \'/AUX_RAW\' && A.NetName == \'/DRAIN\')") (constraint clearance (min 3 mm)))\n',encoding='utf-8',newline='\n')
(S/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Velluneo_T1Study") (type "KiCad") (uri "${KIPRJMOD}/Velluneo_T1Study.pretty") (options "") (descr "Isolated unadopted process study")))\n',encoding='utf-8',newline='\n')
print('Saved isolated10-padoval coupon; mainCAD andT1assignment untouched.')
