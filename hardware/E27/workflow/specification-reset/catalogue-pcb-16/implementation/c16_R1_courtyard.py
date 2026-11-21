from pathlib import Path
import json
from c16_sexpr import parse,dumps,child,children,string
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16';E=D/'design'
points=[(-13.85,-5.5),(-8.85,-5.5),(-8.85,-4),(8.85,-4),(8.85,-5.5),(13.85,-5.5),(13.85,5.5),(8.85,5.5),(8.85,4),(-8.85,4),(-8.85,5.5),(-13.85,5.5)]
def change(t):
 t[:]=[x for x in t if not(isinstance(x,list)and x[0]in('fp_line','fp_rect','fp_poly','fp_arc')and child(x,'layer')and string(child(x,'layer')[1])=='F.CrtYd')]
 for a,b in zip(points,points[1:]+points[:1]):t.append(['fp_line',['start',str(a[0]),str(a[1])],['end',str(b[0]),str(b[1])],['stroke',['width','0.05'],['type','default']],['layer','"F.CrtYd"']])
f=E/'Velluneo_C16.pretty/Vishay_AC05AT_WSZ_FACTORY.kicad_mod';t=parse(f.read_text());change(t);f.write_text(dumps(t)+'\n')
f=E/'Velluneo_driver.kicad_pcb';t=parse(f.read_text());r1=next(q for q in children(t,'footprint')if any(string(z[1])=='Reference'and string(z[2])=='R1'for z in children(q,'property')));change(r1);f.write_text(dumps(t)+'\n')
def capchange(t):
 t[:]=[x for x in t if not(isinstance(x,list)and x[0]in('fp_line','fp_rect','fp_circle')and child(x,'layer')and string(child(x,'layer')[1])=='F.CrtYd')]
 t.append(['fp_circle',['center','0','0'],['end','5.75','0'],['stroke',['width','0.05'],['type','default']],['fill','none'],['layer','"F.CrtYd"']])
f=E/'libraries/Velluneo_Driver.pretty/Rubycon_BXW_D10_P5_PROJECT_CANDIDATE.kicad_mod';t=parse(f.read_text());capchange(t);f.write_text(dumps(t)+'\n')
f=E/'Velluneo_driver.kicad_pcb';t=parse(f.read_text());cap=next(q for q in children(t,'footprint')if any(string(z[1])=='Reference'and string(z[2])=='C1'for z in children(q,'property')));capchange(cap);f.write_text(dumps(t)+'\n')
(D/'checks/R1-courtyard-source-review.json').write_text(json.dumps(dict(scope='Replace oversized enclosing rectangle with union contour; no copper or body position change and no clearance-rule relaxation.',source='https://www.vishay.com/docs/28730/acxx-at.pdf',body_max_xy_mm=[18,7.5],body_courtyard_lateral_margin_mm=.25,pads_mm=[4,10],pad_courtyard_margin_mm=.5,contour_local_mm=points,actual_assembly_process_qualification=False),indent=2)+'\n')
