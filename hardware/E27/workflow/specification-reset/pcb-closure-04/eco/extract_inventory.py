"""Actual native land geometry for a proposed complete ECO placement search."""
from pathlib import Path
import json,copy,hashlib,pcbnew
D=Path(__file__).resolve().parent;P=D.parents[1]
parts=json.loads((D/'proposed-parts.json').read_text(encoding='utf-8'));assign=json.loads((D/'assignments.json').read_text(encoding='utf-8'));old={p['ref']:p for p in json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'))['parts']};rows=[]
for p in parts:
 ref=p['ref'];fpid=assign[ref]['footprint'];lib,name=fpid.split(':');libpath=D/('Velluneo_ECO04.pretty'if lib=='Velluneo_ECO04'else'libraries/Velluneo_Driver.pretty');fp=pcbnew.FootprintLoad(str(libpath),name);assert fp
 item=dict(ref=ref,mpn=p['mpn'],footprint=fpid,source_sha256=hashlib.sha256((libpath/(name+'.kicad_mod')).read_bytes()).hexdigest())
 pads=[]
 for pad in fp.Pads():
  pos=pad.GetPosition();size=pad.GetSize();drill=pad.GetDrillSize();pads.append(dict(pin=pad.GetNumber(),xy_mm=[pcbnew.ToMM(pos.x),pcbnew.ToMM(pos.y)],size_mm=[pcbnew.ToMM(size.x),pcbnew.ToMM(size.y)],drill_mm=pcbnew.ToMM(drill.x),drill_xy_mm=[pcbnew.ToMM(drill.x),pcbnew.ToMM(drill.y)],drill_shape=int(pad.GetDrillShape()),attribute=int(pad.GetAttribute()),shape=int(pad.GetShape()),local_layers=[int(n)for n in pad.GetLayerSet().Seq()],tht=pad.GetAttribute()==pcbnew.PAD_ATTRIB_PTH,circle=pad.GetShape()==pcbnew.PAD_SHAPE_CIRCLE))
 assert {x['pin']for x in pads}==set(p['pins'])
 corners=[]
 for g in fp.GraphicalItems():
  if g.GetLayer()==pcbnew.F_CrtYd and isinstance(g,pcbnew.PCB_SHAPE):
   if g.GetShape()==pcbnew.SHAPE_T_CIRCLE:
    pt=g.GetCenter();x,y,r=pcbnew.ToMM(pt.x),pcbnew.ToMM(pt.y),pcbnew.ToMM(g.GetRadius());corners.extend([[x-r,y-r],[x+r,y+r]])
   else:
    for pt in(g.GetStart(),g.GetEnd()):corners.append([pcbnew.ToMM(pt.x),pcbnew.ToMM(pt.y)])
 assert corners,ref;item['courtyard_bbox_mm']=[min(x for x,y in corners),min(y for x,y in corners),max(x for x,y in corners),max(y for x,y in corners)];item['pads']=sorted(pads,key=lambda x:int(x['pin']));rows.append(item)
 if ref in old and ref not in{'U1','BR1','Q1','T1'}:assert max(abs(a-b)for a,b in zip(item['courtyard_bbox_mm'],old[ref]['courtyard_bbox_mm']))<2e-6,ref
assert len(rows)==33 and sum(len(x['pads'])for x in rows)==81
(D/'native-inventory.json').write_text(json.dumps(dict(native_pcbnew=pcbnew.Version(),scope='Actual native proposed33-partland/courtyard geometry; not qualified forming, installedheight or operational evidence.',parts=rows),indent=2)+'\n',encoding='utf-8',newline='\n');print('native33part81padinventorysaved')
