"""Read-only native KiCad 10.0.6 bare-board manufacturing screen.

Independent native outer polygon distances include max 0.002mm approximation.
Not supplier CAM acceptance, normative insulation, solder or electrical qualification.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, math, sys, zipfile
import pcbnew as k

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'))
import kernel_sc08 as q

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def poly(o,layer):
 p=k.SHAPE_POLY_SET();o.TransformShapeToPolygon(p,layer,0,k.FromMM(.002),k.ERROR_OUTSIDE)
 if p.IsEmpty():raise RuntimeError('Empty native shape '+str(o))
 return p
def pos(p):return [k.ToMM(p.x),k.ToMM(p.y)]
def gap(a,b,cap=3):return q.actual_gap(a,b,cap)

ap=argparse.ArgumentParser();ap.add_argument('--board',required=True);ap.add_argument('--output',required=True);ap.add_argument('--fabrication');ap.add_argument('--zip');ap.add_argument('--actor',default='/root/r05_fabrication');a=ap.parse_args()
src=Path(a.board);source_hash=sha(src);b=q.load_native(src);caps=Path(__file__).with_name('jlcpcb-capabilities-2026-11-22.json')
out={'actor':a.actor,'script_author':'/root/r05_fabrication','board_sha256':source_hash,'tool':k.GetBuildVersion(),'source_changed':False,'capabilities_file':str(caps),'capabilities_sha256':sha(caps),'script_sha256':sha(__file__),'scope':'Bare PCB manufacturing screen. No CAM acceptance, safety/product qualification or actual solder/process measurement.','approximation_mm':.002,'findings':[],'notes':[]}
def fail(i,**d):out['findings'].append({'id':i,**d})
edges=[x for x in b.GetDrawings()if x.GetLayer()==k.Edge_Cuts]
if len(edges)!=4 or any(x.GetShape()!=k.SHAPE_T_SEGMENT for x in edges):raise RuntimeError('Only current four-edge rectangular outline supported')
v=[tuple(pos(x.GetStart()))for x in edges]+[tuple(pos(x.GetEnd()))for x in edges];xs=sorted(set(p[0]for p in v));ys=sorted(set(p[1]for p in v))
if len(xs)!=2 or len(ys)!=2 or any(v.count(p)!=2 for p in set(v)):raise RuntimeError('Outline open, nonrectangular or ambiguous')
x0,x1=xs;y0,y1=ys
out['board']={'dimensions_mm':[x1-x0,y1-y0],'thickness_mm':k.ToMM(b.GetDesignSettings().GetBoardThickness()),'layers':b.GetCopperLayerCount(),'closed_rectangular_outline':True}
if b.GetCopperLayerCount()!=2:fail('FAB_LAYERCOUNT')
copper=[];masks=[];holes=[];smd=[];widths=[];visible=[]
for f in b.GetFootprints():
 for p in f.Pads():
  ident=f.GetReference()+'.'+p.GetNumber();dr=k.ToMM(p.GetDrillSize().x)
  if dr:
   if p.GetDrillSize().x!=p.GetDrillSize().y:raise RuntimeError('Noncircular hole unsupported')
   holes.append({'id':ident,'pos':pos(p.GetPosition()),'d':dr,'annulus':(min(k.ToMM(p.GetSize().x),k.ToMM(p.GetSize().y))-dr)/2,'kind':'component'})
  else:smd.append((ident,p))
  for L,M in [(k.F_Cu,k.F_Mask),(k.B_Cu,k.B_Mask)]:
   if not p.IsOnLayer(L):continue
   pp=poly(p,L);copper.append((ident,L,pp,p.GetNetname(),'pad'))
   if p.IsOnLayer(M):
    mp=k.SHAPE_POLY_SET(pp);ex=p.GetSolderMaskExpansion(M)
    if ex:mp.Inflate(ex,k.CORNER_STRATEGY_ROUND_ALL_CORNERS,1)
    masks.append((ident,L,mp,p.GetNetname()))
for t in b.GetTracks():
 ident=str(t.m_Uuid.AsString())
 if isinstance(t,k.PCB_VIA):
  d=k.ToMM(t.GetDrill());diam=k.ToMM(t.GetWidth(k.F_Cu));holes.append({'id':ident,'pos':pos(t.GetPosition()),'d':d,'annulus':(diam-d)/2,'kind':'via'})
  for L in [k.F_Cu,k.B_Cu]:copper.append((ident,L,poly(t,L),t.GetNetname(),'via'))
 else:
  widths.append(k.ToMM(t.GetWidth()));copper.append((ident,t.GetLayer(),poly(t,t.GetLayer()),t.GetNetname(),'track'))
out['drill']={'total':len(holes),'component_count':sum(x['kind']=='component'for x in holes),'via_count':sum(x['kind']=='via'for x in holes),'tools_mm':sorted(set(x['d']for x in holes)),'minimum_annulus_mm':min(x['annulus']for x in holes),'minimum_component_annulus_mm':min(x['annulus']for x in holes if x['kind']=='component')}
if min(x['d']for x in holes)<.3:fail('FAB_DRILL_UNEXPECTED_PREMIUM',actual=min(x['d']for x in holes))
if min(x['annulus']for x in holes)<.2:fail('FAB_ANNULUS',actual=min(x['annulus']for x in holes),target=.2)
hm=min((math.dist(x['pos'],y['pos'])-(x['d']+y['d'])/2,x['id'],y['id'],.45 if x['kind']=='component'or y['kind']=='component'else.2)for x,y in itertools.combinations(holes,2))
out['drill']['minimum_hole_wall_gap_mm']=hm
for x,y in itertools.combinations(holes,2):
 d=math.dist(x['pos'],y['pos'])-(x['d']+y['d'])/2;target=.45 if x['kind']=='component'or y['kind']=='component'else.2
 if d<target:fail('FAB_HOLE_SPACING',a=x['id'],b=y['id'],gap=d,target=target)
out['track_widths_mm']=sorted(set(widths))
if min(widths)<.1:fail('FAB_TRACK_WIDTH',actual=min(widths),target=.1)
emin=(100,None)
for ident,L,p,net,kind in copper:
 bb=q.bbox(p);d=min(k.ToMM(bb[0])-x0,k.ToMM(bb[1])-y0,x1-k.ToMM(bb[2]),y1-k.ToMM(bb[3]))
 if d<emin[0]:emin=(d,[ident,b.GetLayerName(L)])
 if d<.2:fail('FAB_COPPER_EDGE',object=ident,layer=b.GetLayerName(L),gap=d,target=.2)
out['minimum_copper_edge_mm']=emin
cm=(100,None)
for x,y in itertools.combinations(copper,2):
 if x[1]!=y[1]or x[3]==y[3]or not q.close(x[2],y[2],.5):continue
 d=gap(x[2],y[2],.5)
 if d<cm[0]:cm=(d,[x[0],y[0],b.GetLayerName(x[1])])
 target=.15 if x[4]==y[4]=='pad'else.1
 if d+.004<target:fail('FAB_DIFFERENT_NET_COPPER',a=x[0],b=y[0],gap=d,target=target)
out['minimum_different_net_copper_gap_mm']=cm
mm=(100,None);compound=[]
for x,y in itertools.combinations(masks,2):
 if x[1]!=y[1]or not q.close(x[2],y[2],.8):continue
 d=gap(x[2],y[2],.8)
 if d<mm[0]:mm=(d,[x[0],y[0],b.GetLayerName(x[1])])
 if d<.1:
  if set([x[0],y[0]])=={'R7.1','R4.1'}and x[3]==y[3]=='/M':compound.append({'a':x[0],'b':y[0],'layer':b.GetLayerName(x[1]),'net':'/M','gap_mm':d,'disposition':'Intentional shared same-net solderable window. Hand assembly order/fillet inspection required. No insulating bridge or different-net clearance credit is claimed.'})
  else:fail('FAB_MASK_BRIDGE',a=x[0],b=y[0],gap=d,target=.1)
out['minimum_mask_aperture_gap_mm']=mm;out['intentional_compound_mask_windows']=compound
vip=[]
for h in holes:
 if h['kind']!='via':continue
 for ident,p in smd:
  if p.GetNetname()=='':continue
  L=p.GetLayer()
  if L not in [k.F_Cu,k.B_Cu]:continue
  shp=poly(p,L);hole=k.SHAPE_POLY_SET();hole.NewOutline();radius=h['d']/2/math.cos(math.pi/64)
  for j in range(64):hole.Append(k.FromMM(h['pos'][0]+radius*math.cos(2*math.pi*j/64)),k.FromMM(h['pos'][1]+radius*math.sin(2*math.pi*j/64)))
  if q.close(hole,shp,0):vip.append({'via':h['id'],'pad':ident,'hole_pos':h['pos'],'hole_diameter_mm':h['d']})
out['open_via_holes_inside_SMD_pads']=vip
if vip:fail('FAB_OPEN_VIA_IN_PAD',objects=vip)
silk=[]
for o in list(b.GetDrawings())+[z for f in b.GetFootprints()for z in list(f.GraphicalItems())+[f.Reference(),f.Value()]]:
 if o.GetLayer()not in[k.F_SilkS,k.B_SilkS]or isinstance(o,k.PCB_TEXT)and not o.IsVisible():continue
 ident=o.GetText()if isinstance(o,k.PCB_TEXT)else str(o.m_Uuid.AsString());L=k.F_Cu if o.GetLayer()==k.F_SilkS else k.B_Cu;pp=poly(o,o.GetLayer());silk.append((ident,L,pp))
 if isinstance(o,k.PCB_TEXT):
  row={'text':ident,'height_mm':k.ToMM(o.GetTextHeight()),'stroke_mm':k.ToMM(o.GetTextThickness()),'layer':o.GetLayerName()};visible.append(row)
  if row['height_mm']<1 or row['stroke_mm']<.15:fail('FAB_SILK_SIZE',**row)
sm=(100,None)
for x,y in itertools.product(silk,masks):
 if x[1]!=y[1]or not q.close(x[2],y[2],2):continue
 d=gap(x[2],y[2],2)
 if d<sm[0]:sm=(d,[x[0],y[0],b.GetLayerName(x[1])])
 if d+.004<.15:fail('FAB_SILK_PAD_CLEARANCE',text=x[0],pad=y[0],layer=b.GetLayerName(x[1]),gap=d,target=.15)
out['visible_silk']=visible;out['minimum_silk_mask_gap_mm']=sm
mt=(100,None)
for x,y in itertools.product(masks,copper):
 if x[1]!=y[1]or x[3]==y[3]or y[4]!='track'or not q.close(x[2],y[2],.5):continue
 d=gap(x[2],y[2],.5)
 if d<mt[0]:mt=(d,[x[0],y[0],b.GetLayerName(x[1])])
 if d+.004<.09:fail('FAB_MASK_TO_NEIGHBOR_TRACE',pad=x[0],track=y[0],gap=d,target=.09)
out['minimum_mask_to_different_net_trace_mm']=mt
if a.zip:
 z=zipfile.ZipFile(a.zip);out['archive']={'path':a.zip,'sha256':sha(a.zip),'members':z.namelist(),'CRC_pass':z.testzip()is None}
 if len(z.namelist())!=9:fail('FAB_ZIP_MEMBER_COUNT',actual=len(z.namelist()),expected=9)
 if a.fabrication:
  bad=[n for n in z.namelist()if z.read(n)!=(Path(a.fabrication)/n).read_bytes()];out['archive']['members_differing_from_export_directory']=bad
  if bad:fail('FAB_ZIP_EXPORT_MISMATCH',files=bad)
out['input_unchanged']=sha(src)==source_hash
if not out['input_unchanged']:raise RuntimeError('Read-only audit input changed concurrently')
out['passed']=not out['findings'];out['remaining_limits']=['Intentional M shared solderable window is explicitly reported; no maskbridge claimed there.','Supplier CAM acceptance, exact part sample inspection, manual leadforming/support and solder inspection remain separate.','Manufacturing limits do not override project functional matrix, human release review or physical bring-up limits.']
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':out['passed'],'findings':out['findings'],'output':a.output}))
