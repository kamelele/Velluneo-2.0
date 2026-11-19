from pathlib import Path
import pcbnew,json,re
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-prototype-09';E=D/'design';B=E/'Velluneo_driver.kicad_pcb';pro=B.with_suffix('.kicad_pro').read_bytes();b=pcbnew.LoadBoard(str(B));name='CRCW_2512_R14_SilkClear'
for f in b.GetFootprints():
 if f.GetReference()=='C4':f.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(97),pcbnew.FromMM(72.5)))
 if f.GetReference()=='R13':
  f.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(107),pcbnew.FromMM(128.4)));f.Reference().SetTextAngle(pcbnew.EDA_ANGLE(0,pcbnew.DEGREES_T))
 if f.GetReference()=='R14':
  for g in list(f.GraphicalItems()):
   if g.GetLayer()in(pcbnew.F_SilkS,pcbnew.B_SilkS)and isinstance(g,pcbnew.PCB_SHAPE):f.Remove(g)
  f.SetFPID(pcbnew.LIB_ID('Velluneo_Driver',name))
for p in(E/'libraries/Velluneo_Driver.pretty').glob('*.kicad_mod'):
 s=p.read_text().replace('(stroke (width 0.12)', '(stroke (width 0.15)');p.write_text(s)
src=E/'libraries/Velluneo_Driver.pretty/CRCW_2512_NativeReflow.kicad_mod';s=src.read_text().replace('CRCW_2512_NativeReflow',name);s=re.sub(r'\(fp_line .*?\(layer "F.SilkS"\)\)','',s);(src.parent/(name+'.kicad_mod')).write_text(s)
p=B.with_suffix('.kicad_sch');s=p.read_text();s='\n'.join(line.replace('Velluneo_Driver:CRCW_2512_NativeReflow','Velluneo_Driver:'+name)if '(property "Reference" "R14"'in line else line for line in s.splitlines())+'\n';p.write_text(s)
pcbnew.SaveBoard(str(B),b);B.with_suffix('.kicad_pro').write_bytes(pro)
p=E/'BOM.csv';s=p.read_text();s='\n'.join(line.replace('Velluneo_Driver:CRCW_2512_NativeReflow','Velluneo_Driver:'+name)if line.startswith('R14,')else line for line in s.splitlines())+'\n';p.write_text(s)
