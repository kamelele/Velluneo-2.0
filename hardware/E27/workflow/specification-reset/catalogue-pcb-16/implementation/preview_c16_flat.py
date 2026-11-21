from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16';j=json.loads((D/'checks/saved-geometry.json').read_text());a=json.loads((D/'checks/native-audit.json').read_text());V=D/'preview';V.mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17);big=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',36)
for layers,name in [([0,3],'C16_both_faces.png'),([1,2],'C16_inner_layers.png')]:
 im=Image.new('RGB',(2220,1570),'#101820');dr=ImageDraw.Draw(im);dr.text((75,30),'VELLUNEO C16  |  45 × 60 mm  |  4 warstwy',font=big,fill='white')
 for ix,layer in enumerate(layers):
  left=100+ix*1080;top=190;s=20
  def xy(q):
   x=q[0]+22.5
   if layer==3:x=45-x
   return left+x*s,top+(q[1]+30)*s
  dr.text((left,115),['Góra • F.Cu','Wewnętrzna • In1.Cu','Wewnętrzna • In2.Cu','Spód • B.Cu (widok od spodu)'][layer],font=font,fill='white')
  dr.rounded_rectangle((left-2,top-2,left+902,top+1202),radius=8,fill='#173f34',outline='#c5cfd1',width=3)
  # Transparent-board interpretation is not implied: each panel shows only its named copper layer.
  for t in j['tracks']:
   if layer not in t['layers']:continue
   if not t['via']:
    color=['#efac63','#ed8598','#a3a4e9','#72b7f2'][layer];width=max(1,round(t['width']*s));dr.line([xy(t['a']),xy(t['b'])],fill=color,width=width)
    for pp in(t['a'],t['b']):
     x,y=xy(pp);rr=width/2;dr.ellipse((x-rr,y-rr,x+rr,y+rr),fill=color)
  for q in j['pads']:
   if layer not in q['layers']:continue
   box=q['box'];aa=xy(box[:2]);bb=xy(box[2:]);r=[min(aa[0],bb[0]),min(aa[1],bb[1]),max(aa[0],bb[0]),max(aa[1],bb[1])]
   if q['circle']:dr.ellipse(r,fill='#e6c26b')
   elif q['tht']:dr.rounded_rectangle(r,radius=min(r[2]-r[0],r[3]-r[1])/2,fill='#e6c26b')
   else:dr.rectangle(r,fill='#e6c26b')
   source=next(z for z in a['pads']if z['id']==q['key']);h=source['hole_mm']*s/2;x,y=xy(q['xy'])
   if h:dr.ellipse((x-h,y-h,x+h,y+h),fill='#101820')
  for t in j['tracks']:
   if t['via']:
    x,y=xy(t['a']);r=t['width']*s/2;dr.ellipse((x-r,y-r,x+r,y+r),fill='#b4b6a2');dr.ellipse((x-3,y-3,x+3,y+3),fill='#101820')
  if layer in(0,3):
   for f in a['parts']:
    if f['side']!=('F.Cu'if layer==0 else'B.Cu'):continue
    pos=[v-100 for v in f['xy_mm']];x,y=xy(pos);label=f['ref'];bb=dr.textbbox((x,y),label,font=small);ww=bb[2]-bb[0]
    dr.text((x-ww/2,y-28),label,font=small,fill='white')
  dr.text((left,1420),'Rzeczywiste zapisane ścieżki i pola • bez korpusów 3D',font=small,fill='#c1cbd0')
 dr.text((100,1505),'ERC 0  •  DRC 0  •  brak niepołączonych punktów  •  wersja do przeglądu',font=font,fill='#dce8ec')
 im.save(V/name)
(V/'flat-preview-provenance.json').write_text(json.dumps(dict(source_board_sha256=j['source_sha256'],scope='CAD-derived layer diagram from fresh native pad/track/via extraction; B.Cu mirrored for physical underside view. Reference labels are diagram overlays, not final silk. Not a 3D assembly photograph.'),indent=2)+'\n')
print('Both-face and inner-copper previews saved')
