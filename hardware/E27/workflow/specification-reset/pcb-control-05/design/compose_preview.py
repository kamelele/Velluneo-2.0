"""Lay out actual native KiCad renders; all component shapes are declared envelopes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,json,hashlib
D=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--polish',action='store_true');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
im=Image.new('RGB',(1800,1120),'#f4f7fa');dr=ImageDraw.Draw(im);pl=args.polish
def text(x,y,s,size=24,bold=False,color='#233b52'):
 f=ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf'if bold else'segoeui.ttf'),size);dr.text((x,y),s,font=f,fill=color)
text(45,25,'Velluneo · pełna propozycja PCB zasilacza'if pl else'Velluneo · complete proposed power-driver PCB',34,True)
text(45,76,'Prostokąt 41 × 60 mm · 33 elementy · 81 pól · bez ścieżek'if pl else'Rectangle 41 × 60 mm · 33 components · 81 pads · unrouted',24)
text(45,124,'Przód płytki'if pl else'Front side',24,True);text(925,124,'Tył płytki'if pl else'Back side',24,True)
sources=[]
for side,x in(('top',40),('bottom',920)):
 p=D/'.work'/('native-'+side+'.png');pic=Image.open(p).convert('RGB');pic.thumbnail((840,720),Image.Resampling.LANCZOS);im.paste(pic,(x+(840-pic.width)//2,165+(720-pic.height)//2));sources.append({'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
text(45,918,'Rzeczywisty plik .kicad_pcb — widoki wyrenderowane bezpośrednio przez KiCada.'if pl else'Real .kicad_pcb file — views rendered directly by KiCad.',25,True)
text(45,963,'Modele pokazują rezerwowane obrysy elementów; nie są zatwierdzonymi modelami producentów.'if pl else'Models show allocated component envelopes, not qualified manufacturer mechanical models.',21)
text(45,1001,'KiCad: 0 zgłoszeń odstępów i nadruku · powrót do C1: 4,47 mm* · 54 połączenia do wykonania.'if pl else'KiCad: 0 clearance/silk findings · C1 return 4.47 mm* · 54 unconnected items.',21)
text(45,1040,'* Odległość między polami. Nowy układ i wyprowadzenia wymagają zatwierdzenia oraz dalszych kontroli.'if pl else'* Pad endpoint distance. New circuit/terminal construction is proposed, unapproved and unqualified.',21)
args.output.parent.mkdir(parents=True,exist_ok=True);im.save(args.output)
if not pl:(D/'preview-native-inputs.json').write_text(json.dumps({'native_render_inputs':sources,'composite_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),'AI_generated':False,'qualified_component_geometry':False},indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'output':str(args.output),'actual_native_views':len(sources),'polish':pl}))
