from pathlib import Path
import json,pcbnew,hashlib,argparse
D=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--board',type=Path,default=D/'design/Velluneo_driver.kicad_pcb');ap.add_argument('--output',type=Path,default=D/'geometry-input.json');args=ap.parse_args();B=args.board;b=pcbnew.LoadBoard(str(B));b.BuildConnectivity();c=b.GetConnectivity();pads=[];key={}
for f in b.GetFootprints():
 for p in f.Pads():
  k=f.GetReference()+'.'+p.GetNumber();key[int(p.this)]=k;bb=p.GetBoundingBox();pads.append(dict(key=k,net=p.GetNetname().removeprefix('/'),xy=[pcbnew.ToMM(p.GetPosition().x)-100,pcbnew.ToMM(p.GetPosition().y)-100],box=[pcbnew.ToMM(bb.GetX())-100,pcbnew.ToMM(bb.GetY())-100,pcbnew.ToMM(bb.GetRight())-100,pcbnew.ToMM(bb.GetBottom())-100],layers=[i for i,n in enumerate((pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu))if p.IsOnLayer(n)],tht=p.GetAttribute()==pcbnew.PAD_ATTRIB_PTH))
groups=[];seen=set()
for f in b.GetFootprints():
 for p in f.Pads():
  if int(p.this)in seen:continue
  todo=[p];ids=set();members=set()
  while todo:
   o=todo.pop();i=int(o.this)
   if i in ids:continue
   ids.add(i)
   if i in key:members.add(key[i]);seen.add(i)
   todo.extend(c.GetConnectedItems(o))
  groups.append(sorted(members))
tracks=[]
for p in pads:
 original=next(q for f in b.GetFootprints()for q in f.Pads()if f.GetReference()+'.'+q.GetNumber()==p['key'])
 p['circle']=original.GetShape()==pcbnew.PAD_SHAPE_CIRCLE
 p['size_mm']=[pcbnew.ToMM(original.GetSize().x),pcbnew.ToMM(original.GetSize().y)]
for t in b.GetTracks():
 if isinstance(t,pcbnew.PCB_VIA):tracks.append(dict(net=t.GetNetname().removeprefix('/'),a=[pcbnew.ToMM(t.GetPosition().x)-100,pcbnew.ToMM(t.GetPosition().y)-100],b=[pcbnew.ToMM(t.GetPosition().x)-100,pcbnew.ToMM(t.GetPosition().y)-100],width=pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu)),layers=[0,1,2,3],via=True))
 else:tracks.append(dict(net=t.GetNetname().removeprefix('/'),a=[pcbnew.ToMM(t.GetStart().x)-100,pcbnew.ToMM(t.GetStart().y)-100],b=[pcbnew.ToMM(t.GetEnd().x)-100,pcbnew.ToMM(t.GetEnd().y)-100],width=pcbnew.ToMM(t.GetWidth()),layers=[{pcbnew.F_Cu:0,pcbnew.In1_Cu:1,pcbnew.In2_Cu:2,pcbnew.B_Cu:3}[t.GetLayer()]],via=False))
edges=[p for d in b.GetDrawings()if d.GetLayer()==pcbnew.Edge_Cuts for p in(d.GetStart(),d.GetEnd())];assert len(edges)==8
outline=[min(pcbnew.ToMM(p.x)-100 for p in edges),min(pcbnew.ToMM(p.y)-100 for p in edges),max(pcbnew.ToMM(p.x)-100 for p in edges),max(pcbnew.ToMM(p.y)-100 for p in edges)];keepouts=[]
for z in b.Zones():
 if z.GetIsRuleArea()and z.GetDoNotAllowTracks():
  bb=z.GetBoundingBox();keepouts.append(dict(box=[pcbnew.ToMM(v)-100 for v in(bb.GetX(),bb.GetY(),bb.GetRight(),bb.GetBottom())],layers=[i for i,l in enumerate((pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu))if z.IsOnLayer(l)],no_tracks=z.GetDoNotAllowTracks(),no_vias=z.GetDoNotAllowVias()))
out=dict(copper_layers=4,source_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),outline_bbox_mm=outline,rectangular_rule_areas=keepouts,pads=pads,tracks=tracks,connected_pad_groups=groups,scope='Actual saved native initial connectivity; net names are aliases, independent pin intent remains authoritative.')
out['component_sides']={f.GetReference():b.GetLayerName(f.GetLayer())for f in b.GetFootprints()}
args.output.write_text(json.dumps(out,indent=2)+'\n');print('pads',len(pads),'groups',len(groups),'tracks+vias',len(tracks))
