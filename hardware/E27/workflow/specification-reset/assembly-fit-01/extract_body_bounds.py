from pathlib import Path
import json,pcbnew,hashlib
D=Path(__file__).resolve().parent;P=D.parent;i=json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'));out=[]
for p in i['parts']:
 name=p['footprint'].split(':')[1];src=P/'libraries/Velluneo_Driver.pretty'/(name+'.kicad_mod');assert hashlib.sha256(src.read_bytes()).hexdigest()==p['source_sha256'];f=pcbnew.FootprintLoad(str(src.parent),name);boxes=[]
 for q in f.GraphicalItems():
  if q.GetLayer()!=pcbnew.F_Fab:continue
  b=q.GetBoundingBox();boxes.append([pcbnew.ToMM(b.GetLeft()),pcbnew.ToMM(b.GetTop()),pcbnew.ToMM(b.GetRight()),pcbnew.ToMM(b.GetBottom())])
 assert boxes,p['ref']
 out.append({'ref':p['ref'],'source_sha256':p['source_sha256'],'native_fab_stroke_bbox_mm':[min(b[0]for b in boxes),min(b[1]for b in boxes),max(b[2]for b in boxes),max(b[3]for b in boxes)],'scope':'Full nativeF.Fab graphicalbboxincludingcurves/strokes; not height inference or manufacturer acceptance.'})
print(json.dumps({'native_pcbnew':pcbnew.Version(),'parts':out},indent=2))
