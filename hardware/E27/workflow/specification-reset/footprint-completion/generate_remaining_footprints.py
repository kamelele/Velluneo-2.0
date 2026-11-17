#!/usr/bin/env python3
"""Source-backed / explicitly project-proposed libraries, without product PCB placement."""
from pathlib import Path
import json,math
P=Path(__file__).resolve().parent.parent;D=P/'footprint-completion';L=P/'libraries/Velluneo_Driver.pretty'
parts={a['ref']:a for a in json.loads((P/'schematic-intent/parts.json').read_text())}
A=json.loads((D/'passive-geometry.json').read_text());B=json.loads((D/'power-pad-candidates.json').read_text());defs=[];assign={}
def two(centre,size,typ='smd',drill=None):
 return [{'number':str(i+1),'at':[sgn*centre,0],'size':size,'type':typ,'shape':'circle' if typ=='thru_hole' else 'rect',**({'drill':drill} if drill else {})} for i,sgn in enumerate([-1,1])]
def add(name,refs,pads,body,status,source,polar=False,bodycircle=False,body_note='Source maximum body plan; centered depiction is a project convention'):
 assert all(set(p['number'] for p in pads)==set(parts[r]['pins']) for r in refs)
 extx=max([body[0]/2]+[abs(p['at'][0])+p['size'][0]/2 for p in pads]);exty=max([body[1]/2]+[abs(p['at'][1])+p['size'][1]/2 for p in pads])
 court=[2*math.ceil((extx+.25)*20)/20,2*math.ceil((exty+.25)*20)/20]
 defs.append({'name':name,'refs':refs,'pads':pads,'body_mm':body,'courtyard_mm':court,'body_circle':bodycircle,'polar':polar,'evidence_status':status,'source_basis':source,'body_note':body_note})
 for r in refs:assign[r]={'mpn':parts[r]['mpn'],'footprint':'Velluneo_Driver:'+name,'status':status+'; candidate only, process/insulation/assembly not qualified'}
body={'0603':[1.65,.95],'0805':[2.2,1.4],'1206':[3.3,1.75],'2512':[6.5,3.3]}
refs={'0603':['RLC','RGS'],'0805':['RVS1','RVS2','RG'],'1206':['RB1','RB2','RCS'],'2512':['RAUX','RBO1','RBO2']}
for size,rr in refs.items():
 a=A['crcw_reflow'][size];add('CRCW_'+size+'_NativeReflow',rr,two(a['centres'][1][0],a['pad_size']),body[size],'native manufacturer REFLOW copper dimensions','passive-and-bobbin-basis.md; Vishay20035p11')
a=A['ntcs0603'];add('NTCS0603_NativeReflow',['RT1'],two(a['centres'][1][0],a['pad_size']),[1.75,.95],'native recommended copper dimensions','passive-and-bobbin-basis.md; Vishay29056p2')
add('KEMET_2220_PROJECT_CANDIDATE',['CV1','CV2'],two(2.55,[1.8,5.8]),[6.1,5.4],'PROJECT engineered copper, no manufacturer land prescription established','passive-and-bobbin-basis.md; exact part body/termination bounds only; copper1.8x5.8/centres+/-2.55 project choice')
byref={x['ref']:x for x in B['components']}
for rr,name,b,polar in [(['DAUX','DOUT'],'ST_STTH_SMA_Native',[4.6,2.9],True),(['DCL'],'Diodes_US1M_SMA_Native',[4.6,2.92],True),(['TVS1'],'Vishay_SMBJ_PROJECT_CANDIDATE',[4.57,3.94],True),(['COUT'],'Panasonic_ZA_D_Standard_Native',[6.8,6.8],True),(['F1'],'SCHURTER_UMTH_WEB_PROVISIONAL',[15.4,5.35],False),(['CBULK'],'Rubycon_BXW_D10_P5_PROJECT_CANDIDATE',[10.5,10.5],True),(['RIN'],'AC05_P25p4_FORMED_PROJECT_CANDIDATE',[18,7.5],False)]:
 x=byref[rr[0]];add(name,rr,x['pads'],b,x['evidence_status'],'power-part-basis.md'+('; fuse-source-gap.md' if rr[0]=='F1' else ''),polar,rr[0]=='CBULK',body_note='Nominal untoleranced source representation; NOT qualified maxima' if rr[0]=='F1' else 'Source body envelope; forming/leadout/assembly tolerances remain open')
add('InternalWirePair_P7p62_D1p6_PROJECT_CANDIDATE',['J1','J2'],two(3.81,[3.2,3.2],'thru_hole',1.6),[0,0],'PROJECT pad/hole choice; actual wire not selected','Project internal insulated-wire termination; pitch7.62mm, copper3.2mm,finishedhole1.6mm; wire bundle fit/insulation/strainrelief/solder process must be specified before placement',body_note='No connector body; these pads do not define a user-service dock or a selected wire gauge')
def q(s):return json.dumps(str(s))
def line(x1,y1,x2,y2,layer='F.Fab',w=.1):return f'(fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width {w}) (type default)) (layer {q(layer)}))'
def rect(w,h,layer='F.Fab',width=.1):return f'(fp_rect (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width {width}) (type default)) (fill none) (layer {q(layer)}))'
for a in defs:
 cw,ch=a['courtyard_mm'];bw,bh=a['body_mm'];graphics=rect(cw,ch,'F.CrtYd',.05)
 if a['body_circle']:graphics+=f'(fp_circle (center 0 0) (end {bw/2} 0) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))'
 elif bw>0:graphics+=rect(bw,bh)
 sy=max([bh/2]+[abs(p['at'][1])+p['size'][1]/2 for p in a['pads']])+.25
 if bw:
  graphics+=line(-bw/2,-sy,bw/2,-sy,'F.SilkS',.12)+line(-bw/2,sy,bw/2,sy,'F.SilkS',.12)
 if a['polar'] or a['refs'][0]=='J1':
  # Pin1 is K for diodes and + for capacitors: number/source binding, not identical polarity function.
  p1=a['pads'][0];x=p1['at'][0];y=p1['at'][1]-p1['size'][1]/2-.45
  graphics+=f'(fp_circle (center {x} {y}) (end {x+.12} {y}) (stroke (width .1) (type default)) (fill none) (layer "F.SilkS"))'
  mark='+' if a['refs'][0] in ['COUT','CBULK'] else '' if a['refs'][0]=='J1' else 'K'
  mx=0 if bw else p1['at'][0];my=-bh/2+.8 if a['refs'][0] in ['COUT','CBULK'] else -2.2 if not bw else 0
  graphics+=f'(fp_text user {q(mark+"1")} (at {mx} {my} 0) (layer "F.Fab") (effects (font (size .65 .65) (thickness .1))))'
 copper=''
 for p in a['pads']:
  x,y=p['at'];w,h=p['size'];t=p['type'];dr=f'(drill {p["drill"]})' if t=='thru_hole' else '';layers='"*.Cu" "*.Mask"' if t=='thru_hole' else '"F.Cu" "F.Paste" "F.Mask"'
  copper+=f'(pad {q(p["number"])} {t} {p["shape"]} (at {x} {y}) (size {w} {h}) {dr} (layers {layers}))'
 attr='through_hole' if a['pads'][0]['type']=='thru_hole' else 'smd'
 content=f'(footprint {q(a["name"])} (version 20241229) (generator "velluneo_fp02") (layer "F.Cu") (descr {q(a["evidence_status"]+"; prototype candidate, no process/board qualification")}) (attr {attr}) (property "Reference" "REF**" (at 0 {-ch/2-1} 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15)))) (property "Value" {q(a["name"])} (at 0 {ch/2+1} 0) (layer "F.Fab") (effects (font (size .7 .7) (thickness .1)))) '+graphics+copper+')\n'
 (L/(a['name']+'.kicad_mod')).write_text(content)
old=json.loads((P/'footprint-study/assignments.json').read_text());old.update(assign);assert set(old)==set(parts)-({'T1'} if 'T1' not in old else set())
(P/'footprint-study/assignments.json').write_text(json.dumps(old,indent=2)+'\n')
(D/'geometry-contract.json').write_text(json.dumps({'units':'mm','view':'component/top side,Xright/Ydown; all centered origins are local project conventions','courtyards':'Provisional body/pad extent +0.25mm roundedoutward to0.05mm; NOT insulation/process/thermal clearance','mask_paste':'No overrides; inherited project profile not yet adopted/qualified','parts':defs,'unassigned':[{'ref':'T1','reason':'Native plan views mirrored; component-side pin1/orientation not established, no footprint assigned','closure':'Establish view from authentic numbered/marked model, manufacturer confirmation, or actual marked bobbin; then source/view review before assignment'}]},indent=2)+'\n')
print('Generated',len(defs),'new uniquefootprintsfor',len(assign),'additionalrefs; assigned',len(old),'of28; T1isownedbyseparateviewintegration')
