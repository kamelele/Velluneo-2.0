from pathlib import Path
import json,math,csv
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor,Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/supplier-review-13';O=D/'drawings';O.mkdir(exist_ok=True)
inv=json.loads((D/'checks/native-inventory.json').read_text());interfaces=json.loads((D/'mechanics/component-interfaces.json').read_text());calc=json.loads((D/'mechanics/assembly-calculations.json').read_text());audit=json.loads((D/'checks/current-spacing-and-mounting.json').read_text());sources=json.loads((D/'mechanics/sources.json').read_text());pdf=O/'Velluneo_RFQ13_Dimensioned_Review.pdf';pw,ph=landscape(A4);c=canvas.Canvas(str(pdf),pagesize=(pw,ph));c.setTitle('Velluneo RFQ13 - dimensioned supplier review');c.setAuthor('Velluneo project / Codex assistant')
ink=HexColor('#152638');blue=HexColor('#186b94');gray=HexColor('#637282');orange=HexColor('#b16717');teal=HexColor('#258376');light=HexColor('#e8f0f4')
def txt(x,y,s,size=9,color=ink,bold=False):c.setFillColor(color);c.setFont('Helvetica-Bold'if bold else'Helvetica',size);c.drawString(x,y,str(s))
def para(x,y,w,s,size=9,color=ink):
 st=ParagraphStyle('body',fontName='Helvetica',fontSize=size,leading=size*1.35,textColor=color,spaceAfter=0);p=Paragraph(s,st);_,h=p.wrap(w,700);assert y-h>43,(s[:80],y,h);p.drawOn(c,x,y-h);return y-h-9
def header(n,title,sub):
 c.setFillColor(ink);c.rect(0,ph-84,pw,84,fill=1,stroke=0);txt(40,ph-31,'VELLUNEO / RFQ13',11,HexColor('#8ed9ef'),True);txt(40,ph-56,title,21,HexColor('#ffffff'),True);txt(40,ph-74,sub,8,HexColor('#d7e5ee'))
 c.setStrokeColor(HexColor('#d3dde3'));c.line(40,41,pw-40,41);txt(40,25,'DFM / QUOTATION ONLY  |  Dimensions in mm. Do not scale this drawing.',8,gray);txt(pw-158,25,'20 Nov 2026   |   %d / 7'%n,8,gray)
def dim(x1,y1,x2,y2,s):
 c.setStrokeColor(gray);c.setLineWidth(.5);c.line(x1,y1,x2,y2);a=math.atan2(y2-y1,x2-x1)
 for x,y,d in((x1,y1,a),(x2,y2,a+math.pi)):
  for k in(-.4,.4):c.line(x,y,x+4*math.cos(d+k),y+4*math.sin(d+k))
 txt((x1+x2)/2+3,(y1+y2)/2+5,s,8,gray)
def line(x1,y1,x2,y2,color=ink,width=.8):c.setStrokeColor(color);c.setLineWidth(width);c.line(x1,y1,x2,y2)
def box(x,y,w,h,color=blue,fill=None):
 c.setStrokeColor(color);c.setLineWidth(.8)
 if fill:c.setFillColor(fill)
 c.rect(x,y,w,h,fill=bool(fill),stroke=1)
def boardmap(ox,oy,side):
 sc=4.3;mirror=side=='B';fx=lambda x:ox+(45-x if mirror else x)*sc;fy=lambda y:oy+y*sc
 box(ox,oy,45*sc,60*sc,ink)
 c.setFillColor(HexColor('#fff2d8'));c.rect(ox,fy(37.865),45*sc,9.235*sc,fill=1,stroke=0)
 critical={'T1':(30,30),'Q1':(10.4,4.6),'R1':(18,7.5),'BR1':(9.86,9.86),'C1':(10.5,10.5),'C4':(6.8,6.8),'F1':(15.4,5.35),'C3':(5.7,5),'R10':(6.3,3.2),'R17':(6.3,3.2)}
 for f in inv['parts']:
  if f['side']!=side or f['ref']not in critical:continue
  dx,dy=critical[f['ref']];a=math.radians(f['rotation_deg']);x,y=f['x_mm']-77.5,130-f['y_mm']
  if f['ref']=='Q1':x+=math.sin(a)*(-2.3);y-=math.cos(a)*(-2.3)
  bw=abs(math.cos(a))*dx+abs(math.sin(a))*dy;bh=abs(math.sin(a))*dx+abs(math.cos(a))*dy
  col=blue if side=='F'else teal;c.setStrokeColor(col);c.setFillColor(HexColor('#e8f3f6')if side=='F'else HexColor('#e3f1eb'))
  if f['ref']in('C1','C4','BR1'):c.circle(fx(x),fy(y),bw*sc/2,fill=1,stroke=1)
  else:c.rect(fx(x)-bw*sc/2,fy(y)-bh*sc/2,bw*sc,bh*sc,fill=1,stroke=1)
  txt(fx(x)-7,fy(y)+bh*sc/2+4,f['ref'],7.5,col,True)
 for q in inv['pads']:
  if side+'.Cu'not in q['layers']:continue
  x,y=fx(q['output_x_mm']),fy(q['output_y_mm']);c.setStrokeColor(orange);c.setFillColor(HexColor('#efd283'))
  if q['drill_mm'][0]:
   c.circle(x,y,q['size_mm'][0]*sc/2,fill=1,stroke=1);c.setFillColor(HexColor('#ffffff'));c.circle(x,y,q['drill_mm'][0]*sc/2,fill=1,stroke=0)
  else:
   dx,dy=q['size_mm'];a=math.radians(q['rotation_deg']);w=(abs(math.cos(a))*dx+abs(math.sin(a))*dy)*sc;h=(abs(math.sin(a))*dx+abs(math.cos(a))*dy)*sc;c.rect(x-w/2,y-h/2,w,h,fill=1,stroke=1)
 dim(ox,oy-18,ox+45*sc,oy-18,'45.000');dim(ox-23,oy,ox-23,oy+60*sc,'60.000')
 txt(ox,oy+60*sc+25,'FRONT (F)'if side=='F'else'BACK (B), viewed from underside',11,ink,True)
 txt(ox,oy-41,'Origin: bottom-left, X right / Y up'if side=='F'else'X mirrored for back-side viewing',7.5,gray)
header(1,'Board and critical assembly interfaces','Selected isolated driver | 33 components / 81 pads | Four copper layers | Source '+inv['source_board_sha256'][:16])
boardmap(115,177,'F');boardmap(516,177,'B')
para(40,104,760,'Shaded band: copper-free reservation on all four layers. The transformer body bridges this band and needs its own finished insulation construction. Critical body limits are shown; pads and mounting coordinates come from current CAD. Refer to the native project for full placement.',9)
c.showPage()
header(2,'Finished-hole and insertion map','Coordinates are front-view manufacturing coordinates: X right, Y up from bottom-left route centreline.')
holes=[q for q in inv['pads']if q['drill_mm'][0]];holes.sort(key=lambda q:(q['ref'],int(q['pin'])));assert len(holes)==25
xs=[42,125,207,289,365];labels=['Terminal','X','Y','Hole target','Land']
for x,t in zip(xs,labels):txt(x,487,t,9,blue,True)
for i,q in enumerate(holes):
 y=466-i*13.1
 if i%2==0:c.setFillColor(HexColor('#f1f5f7'));c.rect(40,y-3,383,13,fill=1,stroke=0)
 for x,t in zip(xs,[q['id'],'%.3f'%q['output_x_mm'],'%.3f'%q['output_y_mm'],'%.3f'%q['drill_mm'][0],'%.3f'%q['size_mm'][0]]):txt(x,y,t,8)
y=486
for s in ['<b>25 open component holes + 17 selectively filled vias = 42 PTH.</b> There are no NPTH holes, slots or mounting holes. F1 and C4 are SMD.',
'The tabulated component diameters are requested <b>finished plated-hole targets</b>. The PCB supplier must state pre-drill compensation and guaranteed limits. Excellon entries alone are not a finished-hole measurement.',
'T1 target: <b>1.350 mm</b>; desired acceptance <b>1.300-1.400 mm</b>, matching the nominal TDK mounting-hole recommendation. Full pin-pattern tolerance and insertion fit still require builder confirmation.',
'Proposed component-hole tolerance: +/-0.050 mm; hole/land registration <=0.025 mm. These are requests, not confirmed capabilities. Return a redline if unavailable.',
'Via coordinates and treatment are separately listed in <b>designated-filled-vias.csv</b>. Their finished-ring/cap process needs its own guarantee; the 0.200 mm nominal ring is not a finished minimum.']:
 y=para(456,y,338,s,9)
para(40,92,760,'All dimensions govern. Native and Excellon coordinates are reconciled within 0.0005 mm export rounding per axis. Component orientation and polarity must follow the exact pin/net map and source BOM, not a generic appearance model.',8.5)
c.showPage()
header(3,'T1 finished transformer - requested interface','Source S1 validates the raw former. Complete wound/core/yoke/lead-out dimensions require the builder drawing.')
ox,oy,sc=76,208,7;box(ox,oy,30*sc,30*sc,blue,HexColor('#e8f3f6'))
for rowy,pinnames in((3.75,['1','2','3','4','5']),(26.25,['10','9','8','7','6'])):
 for i,num in enumerate(pinnames):
  x=ox+(5+i*5)*sc;y=oy+rowy*sc;c.setStrokeColor(orange);c.setFillColor(HexColor('#ffffff'));c.circle(x,y,1.35*sc/2,fill=1,stroke=1);txt(x-3,y-16,num,8,ink,True)
dim(ox,oy-25,ox+210,oy-25,'30.0 MAX');dim(ox-27,oy+3.75*sc,ox-27,oy+26.25*sc,'22.50');dim(ox+5*sc,oy+225,ox+10*sc,oy+225,'5.00 pitch')
txt(ox+37,oy+108,'Complete body allocation',10,blue,True)
txt(ox+26,oy+88,'Clips / tape / sleeves included',8,blue)
para(48,156,270,'P: <b>120 turns, 1 (dot) to 5</b><br/>A: <b>22 turns, 2 (dot) to 4</b><br/>S: <b>30 turns, 6 (dot) to 10</b><br/>Pins 3 / 7 / 8 / 9 remain unwound, physically present and without hidden junctions.',9)
box(344,278,165,99,blue);line(325,278,532,278,ink,1.5);box(325,268,207,10,gray,HexColor('#d9e4e9'));dim(527,278,527,377,'18 MAX');txt(344,389,'Side: requested envelope',9,blue,True);txt(338,249,'Flush mounting datum',8,gray)
y=483
for s in ['<b>Finished maximum 30 x 30 x 18 mm.</b> Include core, two yokes, seams, sleeves and exit bends. Return a toleranced drawing and STEP; the raw 25.2 x 26.0 mm former graphic is not the finished body.',
'Raw former S1: height <=12.9 mm; pins 3.5 +/-0.2 mm, nominal 0.6 mm square. Nominal diagonal is 0.8485 mm. No full-pattern pin tolerances are guaranteed here.',
'With requested PCB 1.44-1.76 mm, flush pin tails calculate 1.54-2.26 mm. A blanket 2 mm spacer can leave pins short and is excluded.',
'Return sections through core/yokes, primary exits, intact secondary TIW exits and stripped/soldered zones. Treat core/yokes as primary-domain objects.',
'Lp 2.304 mH +/-10% and effective P/S leakage <=20 uH are RFQ targets. Return actual test conditions, polarity and DCR records; no measurements are claimed.']:
 y=para(562,y,240,s,8.7)
c.showPage()
header(4,'Q13-FORM-A - Q1 forming proposal','STF2N80K5 / TO-220FP type B | Proposed process interface, not an ST-qualified formed component.')
box(76,400,122,55,ink,HexColor('#e7ecef'));txt(81,425,'Q1 case, lower section',8,ink);txt(78,469,'Datum: actual body exit plane',8,gray)
sc=25;x0,y0=118,400;rc=1.075;root=3.75;points=[(x0,y0),(x0,y0-root*sc)]
for i in range(1,19):
 a=math.pi-i*math.pi/36;points.append((x0+rc*sc+rc*sc*math.cos(a),y0-root*sc+rc*sc*math.sin(a)-rc*sc))
# Complete an illustrative S-jog with a tangent quarter bend on each end.
yh=y0-(root+rc)*sc;xa=x0+rc*sc;xb=x0+(5.08-rc)*sc
points=[(x0,y0),(x0,y0-root*sc)]
for i in range(1,19):
 a=math.pi+i*math.pi/36;points.append((xa+rc*sc*math.cos(a),y0-root*sc+rc*sc*math.sin(a)))
points.append((xb,yh))
for i in range(1,19):
 a=math.pi/2-i*math.pi/36;points.append((xb+rc*sc*math.cos(a),y0-(root+2*rc)*sc+rc*sc*math.sin(a)))
boardy=y0-(root+2*rc+.25)*sc;points.extend([(x0+5.08*sc,boardy),(x0+5.08*sc,boardy-1.6*sc-.45*sc)])
for a,b in zip(points,points[1:]):line(*a,*b,gray,4)
box(61,boardy-40,270,40,blue,HexColor('#dceaf0'));txt(65,boardy-24,'PCB: nominal 1.6; request 1.44-1.76',8,blue)
dim(x0,160,x0+5.08*sc,160,'5.08 +/-0.05 offset');dim(91,y0-root*sc,91,y0,'root 3.7-3.8')
para(50,125,304,'Two supported bends, no repeated forming or forced insertion. Radius is measured on the inside; calculation uses the neutral radius. The drawing is schematic; supplier must return the exact formed geometry and datum definition.',8.5)
y=483
for s in ['<b>Source S2:</b> body width 10.0-10.4, thickness 4.4-4.6, height 15.9-16.4; leads up to 1.00 x 0.70. Widened root ends at <=3.6 mm. Source L3-L6 extrema imply 12.2 mm conservatively; this is not a guaranteed usable forming length.',
'<b>Proposed incoming screen:</b> usable lead length >=13.0 mm from the drawn body datum. Supplier must confirm availability, lot yield and measurement method. Do not label 13.0 mm as an ST specification.',
'<b>Proposed form bounds:</b> root 3.70-3.80; inside radius 0.70-0.75; offset 5.03-5.13; above-PCB straight 0.20-0.30; below-PCB tail 0.40-0.50 mm.',
'Worst neutral-axis development: <b>12.7458 mm</b>, including PCB max 1.76. Conditional reserve against a screened 13.0 mm is <b>0.2542 mm</b>. These bounds require jig/first-article proof, not just arithmetic.',
'Requested installed-height reservation: <=23.0 mm. The proposed body-top bound calculates 22.7 mm. Native land 2.25 / finished-hole target 1.50; confirm full pattern and non-strained insertion.',
'S9 supplies generic handling guidance, not qualification of this MOSFET form. Any alternative form or MPN needs an explicit reviewed redline.']:
 y=para(388,y,414,s,9)
c.showPage()
header(5,'Mounted-body and service-clearance requirements','Dimensional facts are sourced; standoffs and forming interfaces are proposed for supplier confirmation.')
for x,t in((48,'R1 / FRONT'),(312,'BR1 / BACK'),(577,'C1 / BACK')):txt(x,480,t,12,blue,True)
box(70,328,108,45,teal,HexColor('#e1efe7'));line(50,296.5,248,296.5,blue,2)
for x,end in((47.8,70),(200.2,178)):line(end,350,x,350,gray,2);line(x,350,x,282,gray,2)
dim(47.8,310,200.2,310,'P25.4');dim(225,296.5,225,328,'5.0-5.5 below body')
para(48,260,230,'<b>AC05:</b> L<=18, D<=7.5, wire 0.77-0.83. Request P25.4 forming with supported roots and body-bottom standoff 5.0-5.5. Body top <=13.0 mm. Current MPN does not guarantee a factory-formed pitch.',9)
c.setStrokeColor(teal);c.setFillColor(HexColor('#e1efe7'));c.circle(415,383,34.5,fill=1,stroke=1)
for dx in(-19.25,19.25):
 for dy in(-19.25,19.25):c.circle(415+dx,383+dy,3,fill=0,stroke=1)
box(380,300,69,39,teal,HexColor('#e1efe7'));line(355,279,478,279,blue,2);dim(483,279,483,300,'3-4 standoff')
para(312,260,230,'<b>W10G:</b> body D<=9.86, H<=5.6; leads 0.71-0.81, raw length >=25.4. Request controlled 5.5 square pattern, polarity and no insertion spring load. Body top <=9.6 mm under proposed standoff.',9)
box(633,283,63,132,teal,HexColor('#e1efe7'));line(595,280,753,280,blue,2);c.setStrokeColor(orange);c.setDash(3,2);c.rect(627,415,75,12,fill=0,stroke=1);c.setDash();txt(710,418,'>=2 free vent',8,orange,True)
para(577,260,225,'<b>Rubycon BXW:</b> D<=10.5, body L<=22; source lead pitch 5.0 +/-0.5. Request strain-free alignment to PCB P5, body standoff <=0.5 and at least 2 mm free space beyond the vent. No adhesive or cover over the vent.',9)
para(48,133,754,'<b>SMD only:</b> F1 (UMT-H) has 15.4 x 5.35 nominal body/square dimensions and 3.75 x 5.6 lands at P13.75. Confirm exact assembled height within the 6.0 mm allocation. C4 maximum body/base is 6.8 x 6.8, height 6.1, terminal span 7.8. Neither part requires insertion-lead forming.',9)
para(48,79,754,'<b>Conditional assembly bounds:</b> front reservation 23.0 + PCB max 1.76 + C1 body/standoff 22.5 = 47.26 mm physical height; including C1 vent service space gives 49.26 mm. These are proposed interface bounds, not measured dimensions or proof of final enclosure fit.',8.5)
c.showPage()
header(6,'Isolation and mounting engineering review','Completed for a supplier enquiry. Exact supplier responses and physical acceptance remain separate.')
y=483
for s in ['<b>Current native checks:</b> zero ERC / DRC / unconnected / schematic-parity findings. Physical pin/net map, values and MPNs are retained. Dedicated SENSE/CS copper and separate return branches remain unchanged.',
'<b>Finished T1 allocation:</b> raw-only courtyard corrected to a 30.5 square reservation around the requested 30 square body. Three local part moves and one AUX_RAW corner correction clear this reservation and add P/S margin.',
'<b>Actual P/S projected and common-layer gap:</b> >=10.725 mm. After the retained proposed 0.35 mm growth/error allowance per domain, the arithmetic remainder is >=10.025 mm. Supplier capability must confirm the budget.',
'<b>HV/quiet common-layer gap:</b> >=3.000 mm. Primary STARTUP_MID/VDD cross-layer projection overlaps; functional dielectric/coupling review depends on actual laminate. Do not describe it as an all-layer 3 mm gap.',
'<b>C1 check:</b> no unrelated B.Cu pad, track or via intersects its D10.5 case circle. Preserve the additional 2 mm vent zone and do not credit the PET sleeve as reinforced insulation.']:
 y=para(42,y,365,s,9)
y=483
for s in ['<b>Builder deliverables:</b> complete T1 outline/STEP; full pin-pattern tolerances; core/yoke/secondary-exit sections; recognized material functions and qualified joining/test procedures. No stripped secondary wire across core/yoke/primary regions.',
'<b>Forming/assembly deliverables:</b> Q1 incoming selection and formed drawing/jig/first article; BR1/R1 polarity and root-supported forming; C1 non-strained insertion and vent access; F1/C4 reflow/height review.',
'<b>Fabricator deliverables:</b> finished-hole and registration limits, selective filled/capped via treatment, actual material/pressed dielectric information, DFM redlines and exact production films.',
'<b>Retained limits:</b> physically present NC T1.3 is primary; 7/8/9 are secondary, all unwound. No reinforced credit for ordinary mask, enamel or unspecified resin. Available sources do not establish an IEC test voltage or finished winding qualification.',
'<b>Release sequence:</b> obtain and review supplier answers, drawings and first articles, then authorize exact production/assembly scope. Finished-lamp thermal, startup, fault and energized insulation tests remain open under their existing criteria.']:
 y=para(438,y,365,s,9)
c.showPage()
header(7,'Source documents and response records','Primary sources reviewed on 20 November 2026. Original diagrams use sourced numeric facts; source figures are not copied.')
y=487
for s in sources:
 text='<b>'+escape(s['id']+' - '+s['title'])+'</b><br/><link href="'+escape(s['url'])+'" color="#186b94">'+escape(s['url'])+'</link>'
 y=para(42,y,758,text,7.7)
para(42,81,758,'Please answer the 12 numbered items in supplier-response-checklist.csv and attach evidence references. Unanswered fields remain PENDING. The enquiry drafts are not sent; no production or payment authorization is implied.',8.5)
c.save()
with(O/'component-hole-targets.csv').open('w',newline='',encoding='utf-8')as f:
 w=csv.writer(f);w.writerow(['Terminal','X_mm','Y_mm','Requested_finished_hole_mm','Land_mm']);w.writerows([[q['id'],q['output_x_mm'],q['output_y_mm'],q['drill_mm'][0],q['size_mm'][0]]for q in holes])
print('Created7-page dimensioned supplierreview',pdf)
