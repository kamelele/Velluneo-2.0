from pathlib import Path
import json,hashlib,pcbnew
D=Path(__file__).resolve().parent;P=D.parents[1];R=P.parents[3]
assign=json.loads((P/'footprint-study/assignments.json').read_text(encoding='utf-8'));parts={p['ref']:p for p in json.loads((P/'electrical-integration/proposed-parts.json').read_text(encoding='utf-8'))};g=json.loads((P/'schematic-intent/intended-connectivity.json').read_text(encoding='utf-8'))
out=[]
for ref,a in assign.items():
 name=a['footprint'].split(':')[1];f=P/'libraries/Velluneo_Driver.pretty'/(name+'.kicad_mod');fp=pcbnew.FootprintLoad(str(f.parent),name);assert fp is not None
 pads=[];ext=[]
 for pad in fp.Pads():
  pos=pad.GetPosition();sz=pad.GetSize();dr=pad.GetDrillSize();x,y,w,h=[pcbnew.ToMM(v)for v in [pos.x,pos.y,sz.x,sz.y]]
  pads.append({'pin':pad.GetNumber(),'xy_mm':[x,y],'size_mm':[w,h],'drill_mm':pcbnew.ToMM(dr.x),'tht':pad.GetAttribute()==pcbnew.PAD_ATTRIB_PTH});ext += [(x-w/2,y-h/2),(x+w/2,y+h/2)]
 court=[];fab=[]
 for item in fp.GraphicalItems():
  layer=item.GetLayer()
  if layer not in [pcbnew.F_CrtYd,pcbnew.B_CrtYd,pcbnew.F_Fab]:continue
  if hasattr(item,'GetStart')and hasattr(item,'GetEnd'):
   for v in [item.GetStart(),item.GetEnd()]:
    (fab if layer==pcbnew.F_Fab else court).append([pcbnew.ToMM(v.x),pcbnew.ToMM(v.y)])
 def box(xs):return [min(v[0]for v in xs),min(v[1]for v in xs),max(v[0]for v in xs),max(v[1]for v in xs)]if xs else None
 out.append({'ref':ref,'mpn':a['mpn'],'footprint':a['footprint'],'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pads':pads,'copper_bbox_mm':box(ext),'courtyard_bbox_mm':box(court),'fab_endpoints_bbox_mm':box(fab),'has_THT':any(p['tht']for p in pads),'height_mm':None,'height_status':'Must be assigned from exactsource/process; no fabricated native3Dmodelheight'})
report={'base':'9f6f999aba18ca06b4bdc5ff4d0bf6148bb3fe94','native_pcbnew':pcbnew.Version(),'scope':'Actual footprint pad/courtyard/fab geometry inventory for independent compactmechanical/spatial study, not productPCB placement or3Dfit proof','parts':out,'graph_nets':g.get('nets'),'graph_top_keys':list(g)}
(D/'native-inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'parts':len(out),'pins':sum(len(p['pads'])for p in out),'geometry':[{k:v for k,v in p.items()if k in ['ref','courtyard_bbox_mm','copper_bbox_mm','has_THT']}for p in out],'graphkeys':list(g)},indent=2))
