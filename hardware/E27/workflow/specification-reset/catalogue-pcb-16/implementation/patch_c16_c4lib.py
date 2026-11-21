from pathlib import Path
from c16_sexpr import parse,dumps,child,string
f=Path(__file__).resolve().parent/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16/design/libraries/Velluneo_Driver.pretty/Panasonic_ZA_D_Standard_Native.kicad_mod'
t=parse(f.read_text())
t=[g for g in t if not(isinstance(g,list) and g[0]=='fp_line' and string(child(g,'layer')[1])=='F.SilkS' and min(float(child(g,'start')[2]),float(child(g,'end')[2])) < -3.45)]
f.write_text(dumps(t)+'\n',encoding='utf-8',newline='\n')
