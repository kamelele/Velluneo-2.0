"""Actual native KiCad render and SVG copper views; no generated board imagery."""
from pathlib import Path
import argparse,json,hashlib,io
from PIL import Image,ImageDraw,ImageFont
import fitz
D=Path(__file__).resolve().parent;C=D/'studies/four-layer-comparison';ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--polish',action='store_true');a=ap.parse_args();pl=a.polish
metric_path=D/'route-metrics.json';metrics=json.loads(metric_path.read_text());metric=metrics['four_layer'];assert hashlib.sha256((C/'Velluneo_four_layer_COMPARISON.kicad_pcb').read_bytes()).hexdigest()==metrics['four_layer_board_sha256']
def number(value):return f'{value:.1f}'.replace('.',',')if pl else f'{value:.1f}'
im=Image.new('RGB',(1800,1280),'#f1f5f8');draw=ImageDraw.Draw(im)
def text(x,y,s,size=24,bold=False,fill='#203e55'):
 font=ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf'if bold else'segoeui.ttf'),size);draw.text((x,y),s,font=font,fill=fill)
text(40,22,'Velluneo · prostokątna płytka zasilacza'if pl else'Velluneo · rectangular power-driver PCB',36,True)
text(40,77,'43 × 60 mm · 33 elementy · porównawczy wariant 4-warstwowy'if pl else'43 × 60 mm · 33 components · unadopted four-layer comparison',25)
text(40,128,'Rzeczywisty podgląd KiCada'if pl else'Actual native KiCad view',25,True)
native=C/'native-top.png';pic=Image.open(native).convert('RGB');pic.thumbnail((920,760));im.paste(pic,(30+(920-pic.width)//2,180+(760-pic.height)//2))
inputs=[native,metric_path]
for i,(name,label)in enumerate([('front','F.Cu'),('inner1','In1.Cu'),('inner2','In2.Cu'),('back','B.Cu')]):
 path=C/('route-'+name+'.svg');inputs.append(path);doc=fitz.open(stream=path.read_bytes(),filetype='svg');pix=doc[0].get_pixmap(matrix=fitz.Matrix(3,3),alpha=False);p=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB');p.thumbnail((330,365));x=1000+(i%2)*390;y=180+(i//2)*405
 text(x,y-38,label,23,True);im.paste(p,(x+(330-p.width)//2,y))
report=json.loads((D/'design/checks/four-layer-drc.json').read_text());assert not report['violations']and not report['unconnected_items']and not report['schematic_parity']
text(40,1010,'KiCad: 0 naruszeń DRC · 0 brakujących połączeń · zgodność ze schematem'if pl else'KiCad: 0 DRC violations · 0 unconnected items · 0 schematic parity findings',26,True)
text(40,1056,f'Powrót masy sterownika: {number(metric["ic_return_planar_mm"])} mm (wcześniej 38,7 mm). Zachowana osobna gałąź pomiarowa.'if pl else f'IC return: {number(metric["ic_return_planar_mm"])} mm (previously 38.7 mm). Dedicated measurement branch retained.',23)
text(40,1100,f'Pozostaje długa ścieżka sterowania tranzystorem ({number(metric["drv_planar_mm"])} mm); ocena zakłóceń jest otwarta.'if pl else f'The {number(metric["drv_planar_mm"])} mm driver trace remains a risk; switching/noise performance is unverified.',23)
text(40,1144,'Proces 4-warstwowy niezatwierdzony. Wariant 2-warstwowy ma nadal 5 brakujących połączeń.'if pl else'Four-layer process is unapproved. The separate two-layer candidate still has 5 unconnected items.',23)
text(40,1188,'Bryły 3D to rezerwy gabarytów. Izolacja, wykonanie i dopasowanie do obudowy pozostają otwarte.'if pl else'3D bodies are envelope allocations. Finished insulation, process and housing fit remain open.',23)
a.output.parent.mkdir(parents=True,exist_ok=True);im.save(a.output)
if not pl:
 (D/'preview-inputs.json').write_text(json.dumps(dict(board_sha256=hashlib.sha256((C/'Velluneo_four_layer_COMPARISON.kicad_pcb').read_bytes()).hexdigest(),inputs=[dict(path=p.relative_to(D).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in inputs],AI_generated=False,preview_sha256=hashlib.sha256(a.output.read_bytes()).hexdigest(),scope='Actual saved CAD views; no qualification or approved process inferred.'),indent=2)+'\n')
print(a.output)
