"""Actual saved 31-position preparation data; no synthetic copper or AI imagery."""
from pathlib import Path
import json,math,argparse,html
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent;P=D.parent
ap=argparse.ArgumentParser();ap.add_argument('--polish',action='store_true');ap.add_argument('--png',type=Path);args=ap.parse_args()
r=json.loads((D/'layout-proposal.json').read_text(encoding='utf-8'));pos=r['positions'];inv=json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'));parts={p['ref']:p for p in inv['parts']}
body={p['ref']:p['native_fab_stroke_bbox_mm']for p in json.loads((P/'assembly-fit-01/native-body-bounds.json').read_text(encoding='utf-8'))['parts']};heights={p['ref']:p['installed_envelope_mm']for p in json.loads((P/'assembly-fit-01/height-contract.json').read_text(encoding='utf-8'))['parts']}
im=Image.new('RGB',(1800,1250),'#f3f6fa');dr=ImageDraw.Draw(im,'RGBA');svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="1250" viewBox="0 0 1800 1250"><rect width="1800" height="1250" fill="#f3f6fa"/>']
def text(x,y,s,size=20,col='#243b53',bold=False):
 f=ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf'if bold else'segoeui.ttf'),size);dr.text((x,y),s,font=f,fill=col);svg.append(f'<text x="{x}" y="{y+size*.85}" font-family="Segoe UI,sans-serif" font-size="{size}" fill="{col}"'+(' font-weight="700"'if bold else'')+'>'+html.escape(s)+'</text>')
def poly(p,col,stroke='#527568',w=1):
 dr.polygon(p,fill=col,outline=stroke,width=w);svg.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}'for x,y in p)+f'" fill="{col}" stroke="{stroke}" stroke-width="{w}"/>')
def line(p,col='#7a8ea2',w=1):
 dr.line(p,fill=col,width=w);svg.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}'for x,y in p)+f'" fill="none" stroke="{col}" stroke-width="{w}"/>')
def rect(b,col,stroke='#527568',w=1):poly([(b[0],b[1]),(b[2],b[1]),(b[2],b[3]),(b[0],b[3])],col,stroke,w)
pl=args.polish
text(45,24,'Velluneo · prostokątna płytka zasilacza 32 × 60 mm'if pl else'Velluneo · rectangular power-driver preparation 32 × 60 mm',32,bold=True)
text(45,73,'31 elementów / 79 pól · podgląd przygotowawczy, bez ścieżek'if pl else'31 components / 79 pads · pre-CAD geometry proposal, no tracks',23)
text(45,109,'Półprzewodniki odsunięte spod transformatora; izolacja i działanie przy usterkach nadal otwarte.'if pl else'Semiconductors clear of transformer projection; electrical fault and insulation gates remain open.',19)
sec={'C4','D3','J2','R11','R12'}
for side,cx in(('F',300),('B',850)):
 cy=570;s=10
 text(cx-155,165,('Przód'if side=='F'else'Tył — widok przez płytkę')if pl else('Front F'if side=='F'else'Back B — common front coordinates'),22,bold=True)
 rect([cx-160,cy-300,cx+160,cy+300],'#166b5a','#123e38',2)
 # The T1 allocation is explicit on front; dashed projection is drawn on back.
 t=pos['T1'];b=[-15,-22,15,8]
 if side=='B':
  for yy in range(int(b[1]*s),int(b[3]*s),12):line([(cx+b[0]*s,cy+yy),(cx+b[0]*s,cy+min(yy+6,b[3]*s))],'#7ca99a');line([(cx+b[2]*s,cy+yy),(cx+b[2]*s,cy+min(yy+6,b[3]*s))],'#7ca99a')
 for ref,c in pos.items():
  if c['side']!=side:continue
  b=c['courtyard_bbox_mm'];color='#8b76ac'if ref in sec else'#60758a'
  if ref=='T1':color='#314e70'
  if ref=='C1':color='#438eaf'
  if ref=='R1':color='#bd8e40'
  rect([cx+b[0]*s,cy+b[1]*s,cx+b[2]*s,cy+b[3]*s],color,'#c4d5df')
  text(cx+c['x_mm']*s-10,cy+c['y_mm']*s-9,ref,13,'#ffffff',True)
 for ref,c in pos.items():
  for pp,b in zip(parts[ref]['pads'],c['pads']):
   if side!=c['side']and not pp['tht']:continue
   rect([cx+b[0]*s,cy+b[1]*s,cx+b[2]*s,cy+b[3]*s],'#e5bd63','#f8dea0')
   if pp['tht']:
    x=cx+(b[0]+b[2])*s/2;y=cy+(b[1]+b[3])*s/2;rr=pp['drill_mm']*s/2;dr.ellipse((x-rr,y-rr,x+rr,y+rr),fill='#173f36');svg.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#173f36"/>')
 text(cx-125,cy-337,'Wyjście do LED'if pl else'Isolated output / LED',17)
 text(cx-123,cy+316,'Wejście 230 V AC'if pl else'230 V AC input',17)
 line([(cx-184,cy-300),(cx-184,cy+300)]);text(cx-230,cy-25,'60 mm',17)
 line([(cx-160,cy+352),(cx+160,cy+352)]);text(cx-29,cy+358,'32 mm',17)
# Perspective uses allocated native F.Fab boxes and installed heights, not vendor 3D models.
faces=[]
def projection(v):
 x,y,z=v;return(1415+8.5*x+4.2*z,565+7.1*y-3*z)
def cuboid(name,b,col):
 x,y,z,X,Y,Z=b;v=[(x,y,z),(X,y,z),(X,Y,z),(x,Y,z),(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]
 for face,shade in[((0,1,2,3),.7),((4,7,6,5),1),((0,4,5,1),.8),((1,5,6,2),.9),((2,6,7,3),.8),((3,7,4,0),.9)]:
  p=[v[i]for i in face];rgb=tuple(int(int(col[i:i+2],16)*shade)for i in(1,3,5));color='#%02x%02x%02x'%rgb
  faces.append((sum(q[2]-.15*q[0]+.2*q[1]for q in p)/len(p),[projection(q)for q in p],color))
cuboid('PCB',[-16,-30,-.8,16,30,.8],'#238a70')
for ref,c in pos.items():
 b=body[ref]
 if ref=='T1':bb=[c['x_mm']-15,c['y_mm']-15,c['x_mm']+15,c['y_mm']+15]
 else:
  points=[]
  for xx in(b[0],b[2]):
   for yy in(b[1],b[3]):
    if c['side']=='B':yy=-yy
    a=math.radians(c['angle_deg']);points.append((xx*math.cos(a)+yy*math.sin(a)+c['x_mm'],-xx*math.sin(a)+yy*math.cos(a)+c['y_mm']))
  bb=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)]
 h=heights[ref];z0,z1=(.8,.8+h)if c['side']=='F'else(-.8-h,-.8)
 color='#334f73'if ref=='T1'else'#428ba8'if ref=='C1'else'#bd9448'if ref=='R1'else'#64768a'
 cuboid(ref,[bb[0],bb[1],z0,bb[2],bb[3],z1],color)
for _,p,c in sorted(faces):poly(p,c,'#465a6b')
text(1210,165,'Obrysy 3D elementów'if pl else'Component envelope perspective',22,bold=True)
text(1210,200,'Wysokości montażowe wymagają potwierdzenia'if pl else'Installed heights remain unqualified',17)
text(1210,871,'T1: rezerwa 30 × 30 × 18 mm'if pl else'T1 allocation: 30 × 30 × 18 mm',19,bold=True)
text(1210,903,'Prawdziwe pola z bibliotek KiCad'if pl else'Pad geometry from local KiCad libraries',18)
text(45,1040,'Zmiana dotyczy tylko przygotowania zasilacza. Obudowa i radiator poza tym etapem.'if pl else'Driver-only preparation. No lamp housing or radiator change in this task.',22,bold=True)
text(45,1081,'Pozostało: rozruch i zwarcia, transformator, izolacja, temperatura i proces montażu.'if pl else'Open: startup/fault bounds, finished transformer, insulation, local temperatures and assembly.',20)
text(45,1122,'To nie jest gotowy projekt PCB ani wynik pomiaru. Nie pokazano fikcyjnych ścieżek.'if pl else'This is not a product PCB or measurement. No fictional tracks are drawn.',20)
text(45,1171,'Wszystkie widoki wynikają z zapisanego układu 31 elementów; tył ma wspólne współrzędne z przodem.'if pl else'All views use the saved 31-position proposal; back view shares front coordinates, not a bottom-view mirror.',17)
if args.png:args.png.parent.mkdir(parents=True,exist_ok=True);im.save(args.png)
if not pl:(D/'driver-preview.svg').write_text(''.join(svg)+'</svg>\n',encoding='utf-8',newline='\n')
print(json.dumps({'components':len(pos),'pads':sum(len(c['pads'])for c in pos.values()),'polish':pl,'png':str(args.png)if args.png else None}))
