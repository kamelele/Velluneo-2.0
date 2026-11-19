"""Native KiCad image plus a saved-native-track engineering view, no AI imagery."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,importlib.util,hashlib,argparse
D=Path(__file__).resolve().parent;E=D/'design';S=D/'studies/sense';ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--polish',action='store_true');args=ap.parse_args();pl=args.polish
spec=importlib.util.spec_from_file_location('g',E/'full_geometry.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);native=json.loads((S/'native-track-export.json').read_text());im=Image.new('RGB',(1800,1160),'#f4f7fa');dr=ImageDraw.Draw(im)
def text(x,y,s,size=24,bold=False,color='#233b52'):
 f=ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf'if bold else'segoeui.ttf'),size);dr.text((x,y),s,font=f,fill=color)
text(40,22,'Velluneo · sterowanie i pomiar prądu'if pl else'Velluneo · controller and current-path refinement',36,True)
text(40,77,'41 × 60 mm · 33 elementy · poprawione rozmieszczenie i osobny szkic połączeń'if pl else'41 × 60 mm · 33 components · refined placement and separate connection study',24)
text(40,130,'Główna płytka — widok KiCada'if pl else'Main PCB — native KiCad view',25,True)
text(945,130,'Próbne połączenia pomiarowe'if pl else'Exploratory current-path connections',25,True)
p=E/'.work/native-top.png';pic=Image.open(p).convert('RGB');pic.thumbnail((850,760));im.paste(pic,(40+(850-pic.width)//2,180+(760-pic.height)//2))
scale=10.6;cx,cy=1295,560
def pt(x,y):return(cx+x*scale,cy+y*scale)
box=[*pt(-20.5,-30),*pt(20.5,30)];dr.rectangle(box,fill='#123f37',outline='#658277',width=3)
band=json.loads((E/'full-build-result.json').read_text())['actual_copper_free_band_y_mm'];dr.rectangle([*pt(-20.5,band[0]-100),*pt(20.5,band[1]-100)],fill='#56706b')
for key,pad in g.pads.items():
 bb=pad['box'];b=[*pt(bb[0],bb[1]),*pt(bb[2],bb[3])];front=pad['tht']or g.pos[pad['ref']]['side']=='F';col='#e8cf6b'if front else'#579ea9'
 if pad['circle']:dr.ellipse(b,fill=col if front else None,outline=col,width=2)
 else:dr.rectangle(b,fill=col if front else None,outline=col,width=2)
 if pad['tht']:
  x,y=pt(*pad['centre']);dr.ellipse((x-2.5,y-2.5,x+2.5,y+2.5),fill='#123f37')
colors={'/SENSE':'#ff9b48','/CS':'#f4f4cc','/PRIMARY_GND':'#b9f0b5'}
for t in native['tracks']:
 pp=[pt(*q)for q in t['points_mm']];dr.line(pp,fill=colors[t['net']],width=max(3,round(t['width_mm']*scale)))
for r in('C1','U1','R6','R9'):
 c=g.pos[r];x,y=pt(c['x_mm'],c['y_mm']);text(x+12,y-25,r,18,True,'#ffffff')
text(965,915,'SENSE: 24,42 mm · CS: 1,93 mm · powrót: 2,70 mm'if pl else'SENSE: 24.42 mm · CS: 1.93 mm · return: 2.70 mm',22,True)
text(40,972,'Główna płytka: 0 naruszeń odstępów i nadruku · bez ścieżek'if pl else'Main PCB: 0 clearance/silk violations · unrouted',24,True)
text(40,1013,'Osobny szkic: 8 odcinków ścieżek · 0 naruszeń DRC · 51 połączeń pozostaje niewykonanych'if pl else'Separate study: 8 track segments · 0 DRC violations · 51 unconnected items remain',23)
text(40,1056,'Bryły są rezerwą gabarytów. Sterowanie, powroty prądu i izolacja nadal wymagają weryfikacji.'if pl else'Bodies are envelope allocations. Control, return paths and insulation still require verification.',22)
text(40,1097,'Próbne ścieżki nie oznaczają zatwierdzenia trasowania ani gotowości do produkcji.'if pl else'Exploratory tracks do not establish routing acceptance or manufacturing readiness.',22)
args.output.parent.mkdir(parents=True,exist_ok=True);im.save(args.output)
(D/'preview-inputs.json').write_text(json.dumps(dict(native_KiCad_image_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),saved_native_track_export_sha256=hashlib.sha256((S/'native-track-export.json').read_bytes()).hexdigest(),AI_generated=False,preview_sha256=hashlib.sha256(args.output.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8',newline='\n');print(str(args.output))
