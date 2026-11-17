from pathlib import Path
import cadquery as cq,fitz
from PIL import Image
p=Path(__file__).resolve().parent;s=cq.importers.importStep('tmp/fp02-a/tdk-efd25.step')
# Rotate about X: (X,Y,Z)->(X,-Z,Y). Looking from transformed-Znegative
# then rotating image180 gives screenright original+X, screendown original-Z.
t=s.rotate((0,0,0),(1,0,0),90)
cq.exporters.export(t,str(p/'top-explicit.svg'),opt={'width':1100,'height':1200,'projectionDir':(0,0,-1),'showAxes':False,'showHidden':False,'strokeWidth':.08,'marginLeft':40,'marginTop':40})
d=fitz.open(str(p/'top-explicit.svg'));d[0].get_pixmap().save(str(p/'top-pre-rotate.png'))
Image.open(p/'top-pre-rotate.png').rotate(180).save(p/'component-top-Xright-minusZdown.png')
Image.open(p/'front-zminus.png').rotate(180).save(p/'front-native-orientation.png')
d=fitz.open('component-study/source/efd25.pdf');d[2].get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(32,615,280,777)).save(str(p/'native-pin1-front-crop.png'))
print('explicitviewsrendered')
