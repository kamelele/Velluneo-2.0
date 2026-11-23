from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path.cwd();H=ROOT/'work/sc09-order-audit/fabrication';O=ROOT/'outputs/SC09_weryfikacja_i_kompendium/fabrication-candidate';data=json.loads((H/'parsed-gerbers.json').read_text());native=json.loads((H/'native-audit.json').read_text())
SCALE=32;M=70;W=int(51.2*SCALE+2*M);HH=int(33*SCALE+2*M);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
def xy(p):return((p[0]-99.4)*SCALE+M,(p[1]-99.4)*SCALE+M)
def drawfile(ext):
 im=Image.new('1',(W,HH),0);d=ImageDraw.Draw(im)
 for o in data[ext]['operations']:
  c=1 if o['polarity']=='dark' else 0
  if o['kind']=='region':d.polygon([xy(p)for p in o['points']],fill=c);continue
  if o['kind']=='line':
   w=o['aperture']['args'][0]*SCALE;a,z=xy(o['a']),xy(o['z']);d.line([a,z],fill=c,width=max(1,round(w)))
   for x,y in [a,z]:d.ellipse((x-w/2,y-w/2,x+w/2,y+w/2),fill=c)
  elif o['kind']=='flash':
   x,y=xy(o['position']);ap=o['aperture'];args=ap['args'];shape=ap['shape']
   if shape=='C':r=args[0]*SCALE/2;d.ellipse((x-r,y-r,x+r,y+r),fill=c)
   elif shape=='R':w,h=args[0]*SCALE,args[1]*SCALE;d.rectangle((x-w/2,y-h/2,x+w/2,y+h/2),fill=c)
   elif shape=='RoundRect':
    r=args[0]*SCALE;xs=args[1:9:2];ys=args[2:9:2];box=(x+min(xs)*SCALE-r,y-max(ys)*SCALE-r,x+max(xs)*SCALE+r,y-min(ys)*SCALE+r);d.rounded_rectangle(box,radius=r,fill=c)
   else:raise ValueError(shape)
 return im
out=[]
for side,cu,mask,silk in [('front','gtl','gts','gto'),('back','gbl','gbs','gbo')]:
 raw=drawfile(cu);im=Image.new('RGB',(W,HH),'white');im.paste((20,25,30),mask=raw)
 d=ImageDraw.Draw(im)
 for h in native['through_pad_inventory']:
  x,y=xy(h['position_mm']);r=h['drill_mm'][0]*SCALE/2;d.ellipse((x-r,y-r,x+r,y+r),fill='white')
 for v in native['via_inventory']:
  x,y=xy(v['position_mm']);r=v['drill_mm']*SCALE/2;d.ellipse((x-r,y-r,x+r,y+r),fill='white')
 d.rectangle((M,M,W-M,HH-M),outline=(80,100,115),width=2);d.text((M,20),f'SC09-SB01 actual Gerber copper / {side} / top-view coordinates',fill=(25,35,45),font=font);im.save(O/f'Gerber_copper_{side}.png');out.append(str(O/f'Gerber_copper_{side}.png'))
 # Literal production maskopenings/silk overlays; no mirroredbackgeometryinvented.
 im=Image.new('RGB',(W,HH),(245,247,249));d=ImageDraw.Draw(im);d.rectangle((M,M,W-M,HH-M),fill=(31,105,70));im.paste((155,175,155),mask=raw);im.paste((215,219,222),mask=drawfile(mask));im.paste((247,247,237),mask=drawfile(silk));d=ImageDraw.Draw(im)
 for h in native['through_pad_inventory']:
  x,y=xy(h['position_mm']);r=h['drill_mm'][0]*SCALE/2;d.ellipse((x-r,y-r,x+r,y+r),fill=(25,30,35))
 for v in native['via_inventory']:
  x,y=xy(v['position_mm']);r=v['drill_mm']*SCALE/2;d.ellipse((x-r,y-r,x+r,y+r),fill=(25,30,35))
 d.text((M,20),f'SC09-SB01 plotted mask + silk / {side} / top-view coordinates',fill=(25,35,45),font=font);im.save(O/f'Gerber_mask_silk_{side}.png');out.append(str(O/f'Gerber_mask_silk_{side}.png'))
print('\n'.join(out))

