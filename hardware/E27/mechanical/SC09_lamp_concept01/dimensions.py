from pathlib import Path
from reportlab.pdfgen import canvas
import pypdfium2 as pdf,json
O=Path('outputs/SC09_zarowka_3D');c=canvas.Canvas(str(O/'SC09_wymiary_i_dopasowanie.pdf'),pagesize=(980,760));c.setTitle('SC09 - bulb concept dimensions')
s=4.5;x0=100;y0=440
p=lambda a,r:(x0+a*s,y0+r*s)
def line(a,b):c.line(*a,*b)
def label(x,y,t,size=11):c.setFillColorRGB(.08,.11,.15);c.setFont('Helvetica',size);c.drawString(x,y,t)
def dim(a,b,t,vertical=False):
 c.setStrokeColorRGB(.15,.25,.35);line(a,b)
 if vertical:
  for x,y in [a,b]:line((x-5,y-3),(x+5,y+3))
  label(a[0]+8,(a[1]+b[1])/2,t)
 else:
  for x,y in [a,b]:line((x-3,y-5),(x+3,y+5))
  label((a[0]+b[0])/2-35,a[1]+8,t)
label(55,720,'SC09 / CONCEPT 01 - proposed bulb assembly',21);label(55,697,'Actual SC09-SB01 PCB unchanged. All dimensions in mm. Mechanical concept, not production enclosure.',11)
c.setStrokeColorRGB(.35,.4,.45);c.setLineWidth(1.8)
for sign in [-1,1]:
 path=c.beginPath();path.moveTo(*p(0,sign*4));path.lineTo(*p(5,sign*13.5));path.lineTo(*p(26,sign*13.5));path.lineTo(*p(26,sign*15));path.lineTo(*p(110,sign*39));path.lineTo(*p(111.6,sign*39));
 import math
 for i in range(1,41):
  t=i*math.pi/80;path.lineTo(*p(111.6+32*math.sin(t),sign*39*math.cos(t)))
 c.drawPath(path)
 # inner cone
 line(p(26,sign*13),p(110,sign*37))
# conservative entire electronics envelope
c.setStrokeColorRGB(.08,.42,.26);c.setFillColorRGB(.90,.96,.92);c.rect(*p(55,-9.75),51.2*s,19.5*s,fill=1,stroke=1)
label(*p(58,2),'SC09 envelope',12);label(*p(58,-3),'51.2 x 33 x 19.5',11)
c.setStrokeColorRGB(.55,.58,.61);line(p(110,-36),p(110,36));line(p(111.6,-36),p(111.6,36))
dim(p(0,-49),p(143.6,-49),'143.6 overall');dim(p(154,-39),p(154,39),'78 max OD',True)
dim(p(55,17),p(106.2,17),'51.2 PCB length');label(820,650,'LED panel: diameter72',12);label(820,630,'Body wall: nominal2',12);label(820,610,'Diffuser height:32',12)
# Cross section at tight end
cx,cy=180,110;rs=2.3;c.setStrokeColorRGB(.4,.45,.5);c.circle(cx,cy,21.285714*rs);c.setStrokeColorRGB(.08,.42,.26);c.rect(cx-16.5*rs,cy-9.75*rs,33*rs,19.5*rs)
label(255,145,'Tight-end cross section at axial55',12);label(255,125,'Internal diameter42.57; envelope diagonal38.33',11);label(255,105,'Minimum radial gap2.12; board-to-panel axial gap3.8',11)
label(55,35,'Fit PASS for the proposed ideal envelope only. Fixings, formed leads, tolerances, insulation and thermal tests remain due.',10)
c.save();d=pdf.PdfDocument(str(O/'SC09_wymiary_i_dopasowanie.pdf'));d[0].render(scale=2).to_pil().save(O/'SC09_wymiary_i_dopasowanie.png')
