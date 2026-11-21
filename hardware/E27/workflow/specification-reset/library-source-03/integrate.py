#!/usr/bin/env python3
"""Apply independently sourced C0G land contract, preserving historical modules."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent.parent; D=P/'library-source-03'
repo=P.parents[3]
doctor=json.loads((repo/'.work/toolkit-doctor.json').read_text())
assert doctor['passed'] and doctor['kicad_cli_version']=='10.0.6', 'Pinned doctor required before native CAD/library work'
g=json.loads((D/'geometry-contract.json').read_text())
def rect(w,h,layer,stroke):
 return f'(fp_rect (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width {stroke}) (type default)) (fill none) (layer "{layer}"))'
name=g['name'];cw,ch=g['courtyard_mm'];bw,bh=g['body_mm']
s=f'(footprint "{name}" (version 20241229) (generator "velluneo_libsource03") (layer "F.Cu") (descr "KEMET commercial C0G 2220 Table3 densityB native lands; reflow candidate, process and product qualification open") (attr smd)'
s+=f'(property "Reference" "REF**" (at 0 {-ch/2-1} 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15))))'
s+=f'(property "Value" "{name}" (at 0 {ch/2+1} 0) (layer "F.Fab") (effects (font (size .7 .7) (thickness .1))))'
s+=rect(cw,ch,'F.CrtYd',.05)+rect(bw,bh,'F.Fab',.1)
for y in [-2.9,2.9]:s+=f'(fp_line (start {-bw/2} {y}) (end {bw/2} {y}) (stroke (width .12) (type default)) (layer "F.SilkS"))'
for p in g['pads']:
 x,y=p['at'];w,h=p['size'];s+=f'(pad "{p["number"]}" smd rect (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask"))'
(P/f'libraries/Velluneo_Driver.pretty/{name}.kicad_mod').write_text(s+')\n',encoding='utf-8',newline='\n')
a_path=P/'footprint-study/assignments.json'; a=json.loads(a_path.read_text())
for ref in g['refs']:
 assert a[ref]['mpn']==g['mpn']
 a[ref]['footprint']='Velluneo_Driver:'+name
 a[ref]['status']='Native KEMET commercial C0G Table3 densityB copper; candidate only, reflow/process/assembly/insulation not qualified'
assert a['F1']['mpn']=='3403.0268.23'
a['F1']['status']='Native SCHURTER PDFp2 copper visually confirmed and source-hashed; historical WEB_PROVISIONAL name retained; body tolerances/process/assembly not qualified'
a_path.write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8',newline='\n')
h_path=P/'hardware.json';h=json.loads(h_path.read_text())
extra=['library-source-03/geometry-contract.json','library-source-03/integrate.py','library-source-03/source-register.json','library-source-03/source-basis.md',f'libraries/Velluneo_Driver.pretty/{name}.kicad_mod']
for f in extra:
 if f not in h['source_files']:h['source_files'].append(f)
h_path.write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Applied C2/C3 native densityB lands; F1 evidence wording; no graph, values or PCB change')
