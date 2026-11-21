import cadquery as cq
from pathlib import Path
import fitz,json
p=Path(__file__).resolve().parent;s=cq.importers.importStep('tmp/fp02-a/tdk-efd25.step')
for name,direction in [('yminus',(0,-1,0)),('yplus',(0,1,0)),('front-zminus',(0,0,-1)),('isometric',(-1,-1,-1))]:
 dest=p/(name+'.svg');cq.exporters.export(s,str(dest),opt={'width':1200,'height':1100,'projectionDir':direction,'showAxes':True,'showHidden':False,'strokeWidth':.08,'marginLeft':40,'marginTop':40})
 doc=fitz.open(str(dest)); doc[0].get_pixmap().save(str(p/(name+'.png')))
faces=[]
for i,f in enumerate(s.faces().vals()):
 b=f.BoundingBox();c=f.Center()
 try:n=f.normalAt().toTuple()
 except:n=None
 faces.append({'i':i,'type':f.geomType(),'area':f.Area(),'centre':c.toTuple(),'normal':n,'box':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]})
(p/'faces.json').write_text(json.dumps(faces,indent=2)+'\n')
print('rendered')
