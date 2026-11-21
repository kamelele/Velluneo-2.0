from pathlib import Path
from c16_sexpr import parse,dumps,child,children,string
W=Path(__file__).resolve().parent;E=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16/design'
def fix(t):
 t[:]=[q for q in t if not(isinstance(q,list)and q[0]=='fp_line'and child(q,'layer')and string(child(q,'layer')[1])=='F.SilkS')]
 t.append(['fp_circle',['center','0','0'],['end','5.5','0'],['stroke',['width','0.15'],['type','default']],['fill','none'],['layer','"F.SilkS"']])
f=E/'libraries/Velluneo_Driver.pretty/Rubycon_BXW_D10_P5_PROJECT_CANDIDATE.kicad_mod';t=parse(f.read_text());fix(t);f.write_text(dumps(t)+'\n')
f=E/'Velluneo_driver.kicad_pcb';t=parse(f.read_text());fp=next(q for q in children(t,'footprint')if any(string(z[1])=='Reference'and string(z[2])=='C1'for z in children(q,'property')));fix(fp);f.write_text(dumps(t)+'\n')
