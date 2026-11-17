#!/usr/bin/env python3
"""Raw-bobbin land candidate from independently correlated native PDF/STEP pin1 view."""
from pathlib import Path
import json
P=Path(__file__).resolve().parent.parent;D=P/'transformer-footprint';L=P/'libraries/Velluneo_Driver.pretty'
name='TDK_B66422W1010D001_EFD25_RAW_CANDIDATE'
pads=[]
for i,n in enumerate([10,9,8,7,6]):pads.append({'number':str(n),'at':[-10+5*i,-11.25],'size':[2.4,2.4],'drill':1.35,'type':'thru_hole','shape':'circle'})
for i,n in enumerate([1,2,3,4,5]):pads.append({'number':str(n),'at':[-10+5*i,11.25],'size':[2.4,2.4],'drill':1.35,'type':'thru_hole','shape':'rect' if n==1 else 'circle'})
def rect(w,h,layer,width):return f'(fp_rect (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))'
content=f'(footprint "{name}" (version 20241229) (generator "velluneo_t1_candidate") (layer "F.Cu") (descr "Raw TDK bobbin, component-side pin1 derived from native PDF/STEP geometry; finished transformer and process not qualified") (attr through_hole) (property "Reference" "REF**" (at 0 -14.5 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15)))) (property "Value" "{name}" (at 0 14.5 0) (layer "F.Fab") (effects (font (size .7 .7) (thickness .1)))) '+rect(25.2,26,'F.Fab',.1)+rect(25.7,26.5,'F.CrtYd',.05)+rect(25.5,26.3,'F.SilkS',.12)+'(fp_circle (center -13.3 11.25) (end -13.15 11.25) (stroke (width .1) (type default)) (fill none) (layer "F.SilkS"))'
for a in pads:
 x,y=a['at'];content+=f'(pad "{a["number"]}" thru_hole {a["shape"]} (at {x} {y}) (size 2.4 2.4) (drill 1.35) (layers "*.Cu" "*.Mask"))'
(L/(name+'.kicad_mod')).write_text(content+')\n')
g={'units':'mm','view':'Component side viewed from STEP-Ynegative toward+Y; screenright+X/screendown-Z; footprint(X,-Z)','source_geometry':'Native marked corner correlation and actualSTEP pin tips; source-step-inference.md/source-step-findings.json/independent-view-review.md','source_pitch_mm':5,'source_rows_mm':22.5,'native_recommended_hole_range_mm':[1.3,1.4],'project_drill_mm':1.35,'project_copper_pad_mm':[2.4,2.4],'drill_note':'Proposed finished plated-hole target within source mounting-hole range; actual fabrication compensation/tolerance and square-pin assembly remain unqualified','body_mm':[25.2,26],'courtyard_mm':[25.7,26.5],'body_note':'RAW bobbin only; finished winding/core/yokes/leadouts/insulation envelope remains unknown. Courtyard is provisional, not a finished transformer or safety reserve.','mask_paste':'*.Mask without override; no paste onthroughholes; managedprocessunqualified','name':name,'pads':pads,'ref':'T1','status':'Source-correlated TOPview raw-bobbin copper/drill candidate; no physical/build/safety qualification'}
(D/'geometry-contract.json').write_text(json.dumps(g,indent=2)+'\n')
f=P/'footprint-study/assignments.json';a=json.loads(f.read_text());a['T1']={'mpn':'CUSTOM:EFD25_120_30_22','footprint':'Velluneo_Driver:'+name,'status':g['status']};assert len(a)==28;f.write_text(json.dumps(a,indent=2)+'\n')
print('T1rawbobbin candidate created/assigned;28positions,18modules; noPCB')
