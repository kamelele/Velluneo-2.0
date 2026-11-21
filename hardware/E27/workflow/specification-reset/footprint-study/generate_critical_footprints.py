#!/usr/bin/env python3
"""Three source-backed copper land candidates. No PCB, 3D model or qualified process."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent.parent;D=P/'footprint-study';L=P/'libraries/Velluneo_Driver.pretty';L.mkdir(exist_ok=True)
def q(s):return json.dumps(str(s))
def rectangle(x,y,layer,width):return f'(fp_rect (start {-x} {-y}) (end {x} {y}) (stroke (width {width}) (type default)) (fill none) (layer {q(layer)}))'
def pad(n,x,y,w,h):return f'(pad {q(n)} smd rect (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask"))'
items=[
 {'ref':'U1','mpn':'UCC28711DR','name':'UCC28711DR_SOIC7_HV7','body_mm':[3.98,5.0],'height_max_mm':1.75,'courtyard_mm':[7.5,5.5],'pads':[('1',-2.7,-1.905,1.55,.6),('2',-2.7,-.635,1.55,.6),('3',-2.7,.635,1.55,.6),('4',-2.7,1.905,1.55,.6),('5',2.7,1.905,1.55,.6),('6',2.7,.635,1.55,.6),('7',2.7,-1.905,1.55,.6)],'source':'TI SLUSB86C PDFp3 functional/p35 package/p36 land example; functional7 at geometric8; source metric values adopted','source_sha256':'762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248'},
 {'ref':'BR1','mpn':'MB10S-13','name':'MB10S_Diodes_MBS_1P_2AC_3N_4AC','body_mm':[4.95,4.1],'courtyard_mm':[5.5,8.0],'pads':[('1',1.25,-2.675,1.,2.15),('2',1.25,2.675,1.,2.15),('3',-1.25,-2.675,1.,2.15),('4',-1.25,2.675,1.,2.15)],'source':'Diodes DS39045Rev3-2 PDFp1 functions/p4 suggested lands; rowcentres7.50-2.15=5.35mm','source_sha256':'a46066843f6b010bffdb85fe3162573330e70bd481df3c5ef9000eeb59e6a77c'},
 {'ref':'Q1','mpn':'STN1NK80Z','name':'STN1NK80Z_SOT223_Tab4','body_mm':[6.7,3.7],'height_max_mm':1.8,'courtyard_mm':[7.2,8.4],'pads':[('1',-2.3,3.2,1.2,1.5),('2',0.,3.2,1.2,1.5),('3',2.3,3.2,1.2,1.5),('4',0.,-3.2,3.3,1.5)],'source':'ST DS14259Rev2 PDFp1 functions/p8 outline/p9 Figure20 recommended lands; rowcentres6.4mm','source_sha256':'b2e23ffd24302bb78fd42dddbd25155a0833f785765aba20ef38fdff6aabf03b'}]
for a in items:
 x,y=[b/2 for b in a['body_mm']];cx,cy=[b/2 for b in a['courtyard_mm']]
 props=f'(property "Reference" "REF**" (at 0 {-cy-1} 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15)))) (property "Value" {q(a["name"])} (at 0 {cy+1} 0) (layer "F.Fab") (effects (font (size .7 .7) (thickness .1))))'
 graphics=rectangle(x,y,'F.Fab',.1)+rectangle(cx,cy,'F.CrtYd',.05)
 # Silk only at body edges away from lands, not a replacement for verified courtyard.
 if a['ref']=='U1':
  for yy in [-y-.15,y+.15]:graphics+=f'(fp_line (start {-x} {yy}) (end {x} {yy}) (stroke (width .12) (type default)) (layer "F.SilkS"))'
 elif a['ref']=='BR1':
  for xx in [-x-.15,x+.15]:graphics+=f'(fp_line (start {xx} {-y}) (end {xx} {y}) (stroke (width .12) (type default)) (layer "F.SilkS"))'
 else:graphics+=rectangle(x+.15,y+.15,'F.SilkS',.12)
 # Pad1 marker is on the package side, not an additional solder pad.
 p1=a['pads'][0];mx=p1[1];my=p1[2]+(-.7 if p1[2]<0 else .7)
 # Keep mark beyond pad end, not at a fixed offset that could overlap the copper.
 my=p1[2]+(-1 if p1[2]<0 else 1)*(p1[4]/2+.4)
 graphics+=f'(fp_circle (center {mx} {my}) (end {mx+.15} {my}) (stroke (width .1) (type default)) (fill none) (layer "F.SilkS"))'
 content=f'(footprint {q(a["name"])} (version 20241229) (generator "velluneo_fp_capture") (layer "F.Cu") (descr {q(a["mpn"]+"; source-backed copper candidate; process and board qualification incomplete")}) (tags "candidate source-checked") (attr smd) '+props+graphics+''.join(pad(*p) for p in a['pads'])+')\n'
 (L/(a['name']+'.kicad_mod')).write_text(content)
assignment={a['ref']:{'mpn':a['mpn'],'footprint':'Velluneo_Driver:'+a['name'],'status':'Source-backed candidate copper lands; mask/paste/courtyard/assembly and board qualification remain open'} for a in items}
existing_assignments=json.loads((D/'assignments.json').read_text()) if (D/'assignments.json').exists() else {}
existing_assignments.update(assignment)
(D/'assignments.json').write_text(json.dumps(existing_assignments,indent=2)+'\n')
(D/'geometry-contract.json').write_text(json.dumps({'units':'mm','view':'Component/top side; Xright/Ydown; centered origins and body centre display are project conventions','copper_corner_choice':'rectangular; TI native rounded-corner radius unspecified so no false native radius claimed','courtyard_choice':'Project provisional visual handling envelope approximately0.25mm above source body/padextents, roundedoutward; NOT insulation distance or process-approvedcourtyard','mask_paste_choice':'F.Mask/F.Paste present; no explicit margin or paste reduction overrides; inherited project rules are not yet adopted/qualified','parts':items},indent=2)+'\n')
(P/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Velluneo_Driver") (type "KiCad") (uri "${KIPRJMOD}/libraries/Velluneo_Driver.pretty") (options "") (descr "Source-backed critical footprint candidates; process qualification incomplete")))\n')
print('Created3localfootprintcandidates; noPCB')
