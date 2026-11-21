"""Read-only SC09 saved-copper matrix screen; not IEC or insulation qualification.

Reuse exact native polygon collector from separately reviewed SC08 kernel, with
SC09-specific independent A1 intent binding and all 55 explicit pair targets.
No CAD input is ever saved. Unsupported geometry stops, rather than vanishing.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,sys
import pcbnew as k
import kernel_sc08 as q

HERE=Path(__file__).resolve().parent
LOCAL={'BP','M','SW_SOURCE','FB_INDUCTOR'}
def dump(path,data):Path(path).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def dig(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()

class Contract:
 def __init__(self,project,matrix,exceptions=None):
  self.project=Path(project);self.synthetic=False;self.input_hashes={}
  ip=self.project/'intended-connectivity.A1.json';intent=load(ip);self.input_hashes[str(ip)]=q.sha(ip)
  self.matrix_path=Path(matrix);m=load(matrix);self.input_hashes[str(matrix)]=q.sha(matrix)
  if m['input_graph']['sha256']!=q.sha(ip):raise q.Unsupported('Matrix refers to different A1 graph')
  self.nets={r['id'] for r in intent['nets']}
  if len(self.nets)!=11:raise q.Unsupported('Expected eleven independent SC09 A1 nets')
  self.mapping={'/'+n:n for n in self.nets}
  self.expected={(p['ref'],p['pin']):'/'+r['id'] for r in intent['nets'] for p in r['pins']}
  for p in intent['no_connects']:
   if (p['ref'],p['pin'])!=('T1','4'):raise q.Unsupported('Unexpected NC identity')
   native='unconnected-(T1-UNWOUND-Pad4)';self.mapping[native]='EXPLICIT_NC';self.expected[('T1','4')]=native
  self.refs={r for r,p in self.expected};self.matrix={}
  for r in m['pair_matrix']:
   pair=frozenset([r['net_a'],r['net_b']])
   if len(pair)!=2 or pair in self.matrix:raise q.Unsupported('Duplicate/invalid matrix pair')
   self.matrix[pair]=r
   expect=.25 if pair<=LOCAL else (1. if pair=={'LED_PLUS','DC_RETURN'} else 2.)
   if r['surface_creepage_target_mm']!=expect:raise q.Unsupported('Matrix does not match independently declared SC09 screen '+str(pair))
  if set(self.matrix)!=set(map(frozenset,itertools.combinations(self.nets,2))):raise q.Unsupported('Missing/extra matrix pairs')
  self.minimum={'track_width':.2,'hole_size':.3,'annular_width':.2,'edge_clearance':1.}
  self.exceptions=[];self.areas=[];self.outline=None
  if exceptions:
   ep=Path(exceptions);ed=load(ep);self.input_hashes[str(ep)]=q.sha(ep)
   if not ed.get('authorized_for_bounded_geometry_screen_by'):raise q.Unsupported('Exception proposal is not authorized for this bounded screen')
   if ed.get('A1_graph_sha256')!=q.sha(ip) or ed.get('matrix_sha256')!=q.sha(matrix):raise q.Unsupported('Exception basis hashes do not match')
   self.exceptions=ed['exceptions']
   edge=ed.get('edge_clearance_target_mm',1.)
   if edge not in [.5,1.]:raise q.Unsupported('Only explicit root .5mm lab or strict1mm edge screen supported')
   self.minimum['edge_clearance']=edge
 def width(self,native):return self.minimum['track_width']
 def gap(self,a,b):
  if a==b:return 0.
  if 'EXPLICIT_NC' in (a,b):return .3
  return self.matrix[frozenset([a,b])]['surface_creepage_target_mm']

class Checker(q.Checker):
 def check_outline(self):
  edges=[]
  for x in self.board.GetDrawings():
   if x.GetLayer()!=k.Edge_Cuts:continue
   if x.GetShape()!=k.SHAPE_T_SEGMENT:raise q.Unsupported('Only actual closed straight native Edge.Cuts supported')
   a,b=x.GetStart(),x.GetEnd();edges.append(((a.x,a.y),(b.x,b.y)))
  pts=set(p for edge in edges for p in edge)
  if not edges or len(edges)!=len(pts) or any(sum(p in e for e in edges)!=2 for p in pts):raise q.Unsupported('Open/branched/duplicate outline')
  first=edges.pop();vertices=[first[0],first[1]]
  while edges:
   e=next((e for e in edges if vertices[-1] in e),None)
   if e is None:raise q.Unsupported('Multiple disjoint outlines/slots unsupported')
   edges.remove(e);vertices.append(e[1] if vertices[-1]==e[0] else e[0])
  if vertices[-1]!=vertices[0]:raise q.Unsupported('Open outline')
  p=k.SHAPE_POLY_SET();p.NewOutline()
  for x,y in vertices[:-1]:p.Append(x,y)
  if p.IsSelfIntersecting():raise q.Unsupported('Self-intersecting outline')
  self.native_outline=p;self.outline_vertices=[[k.ToMM(x),k.ToMM(y)] for x,y in vertices[:-1]]

 def validate_exception(self,e):
  ref=e.get('ref');pins=e.get('pins');floor=e.get('proposed_drawn_floor_mm');margin=e.get('escape_margin_mm')
  if ref=='U1':
   if pins==['3','4']:nets=['FB_INDUCTOR','BUS_FILTERED'];minimum=.60
   elif pins==['2','4']:nets=['M','BUS_FILTERED'];minimum=1.80
   else:raise q.Unsupported('Only explicit U1pin3/4 and2/4 pairs supported')
   if e.get('nets')!=nets or floor<minimum:raise q.Unsupported('U1 exception identity/floor invalid')
  elif ref=='BR1':
   if pins not in [['1','3'],['2','4']] or floor<1.40:raise q.Unsupported('Only exact bridge adjacent pair/floor supported')
   expect=[self.c.mapping[self.c.expected[(ref,p)]] for p in pins]
   if e.get('nets')!=expect:raise q.Unsupported('Bridge exception net identity invalid')
  elif ref=='D1':
   if pins!=['1','2'] or e.get('nets')!=['FB_INDUCTOR','DC_RETURN'] or floor<1.40:raise q.Unsupported('Only explicit D1pin1/2 and1.40mm floor supported')
  else:raise q.Unsupported('Unsupported exception reference')
  if e.get('layers')!=['B.Cu'] or e.get('escape_layers')!=['B.Cu'] or set(e.get('except_object_types',[]))!={'pad','track'}:raise q.Unsupported('Exception types/layers must be exact B pad/track')
  limit=1. if ref=='U1' and pins==['3','4'] else .3
  if not isinstance(margin,(int,float)) or not 0<=margin<=limit:raise q.Unsupported('Exception pad-bbox margin exceeds explicit '+str(limit)+'mm bound')

 def exception_region(self,e):
  self.validate_exception(e)
  objs=[x for x in self.objects if x.kind=='pad' and x.layer=='B.Cu' and x.owner in [(e['ref'],p) for p in e['pins']]]
  if len(objs)!=2:raise q.Unsupported('Exception needs exactly two actual pads')
  bb=[q.bbox(x.shape) for x in objs];m=k.FromMM(e['escape_margin_mm'])
  bounds=[min(b[0] for b in bb)-m,min(b[1] for b in bb)-m,max(b[2] for b in bb)+m,max(b[3] for b in bb)+m]
  frozen=e.get('region_bbox_mm')
  if not isinstance(frozen,list) or len(frozen)!=4 or [round(x*1e6) for x in frozen]!=bounds:raise q.Unsupported('Frozen package exception region differs from actual transformed paired pads '+str(e['ref'])+str(e['pins']))
  return q.rectangle(frozen)

 def collect(self):
  # Kernel collects courtyards for package concessions, whereas SC09 concessions
  # deliberately use only the frozen paired-pad box plus its exact scoped margin.
  ex=self.c.exceptions;self.c.exceptions=[]
  try:super().collect()
  finally:self.c.exceptions=ex
  for e in ex:self.validate_exception(e)

 def run(self):
  self.collect();self.pair_minima={};edge_min=None
  edge=self.c.minimum['edge_clearance']
  safe=k.SHAPE_POLY_SET(self.native_outline)
  safe.Inflate(-k.FromMM(edge),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(q.ERROR_MM))
  for o in self.objects:
   self.stats['per_face_objects'][o.kind]=self.stats['per_face_objects'].get(o.kind,0)+1
   if not q.clipped(o.shape,safe,False).IsEmpty():self.fail('copper_edge_setback',id=o.id,layer=o.layer,target_mm=edge)
   lo,hi=0.,25.
   for _ in range(20):
    mid=(lo+hi)/2;inside=k.SHAPE_POLY_SET(self.native_outline);inside.Inflate(-k.FromMM(mid),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(q.ERROR_MM))
    if inside.IsEmpty() or not q.clipped(o.shape,inside,False).IsEmpty():hi=mid
    else:lo=mid
   if edge_min is None or lo<edge_min['conservative_gap_mm']:edge_min={'id':o.id,'layer':o.layer,'net':o.net,'conservative_gap_mm':round(lo,6)}
   if o.net=='EXPLICIT_NC' and o.kind!='pad':self.fail('routed_explicit_nc',id=o.id)
  for a,b in itertools.combinations(self.objects,2):
   if a.layer!=b.layer or a.net==b.net:continue
   self.stats['different_net_face_pairs']+=1
   key=(tuple(sorted([a.net,b.net])),a.layer)
   old=self.pair_minima.get(key)
   # Bounding rectangle lower bound avoids expensive polygon queries when no
   # shape pair can improve an already known exact conservative minimum.
   aa,bb=q.bbox(a.shape),q.bbox(b.shape);dx=max(aa[0]-bb[2],bb[0]-aa[2],0);dy=max(aa[1]-bb[3],bb[1]-aa[3],0)
   lower=math.hypot(dx,dy)/1e6
   if old is None or lower<=old['conservative_gap_mm']+.0001:
    upper=math.hypot(max(abs(aa[0]-bb[2]),abs(bb[0]-aa[2])),max(abs(aa[1]-bb[3]),abs(bb[1]-aa[3])))/1e6+.001
    gap=q.actual_gap(a.shape,b.shape,upper)
    if old is None or gap<old['conservative_gap_mm']:self.pair_minima[key]={'conservative_gap_mm':gap,'a':a.id,'b':b.id,'kinds':[a.kind,b.kind]}
   self.spacing(a,b)
  rows=[]
  for pair,r in sorted(self.c.matrix.items(),key=lambda x:sorted(x[0])):
   names=tuple(sorted(pair));bylayer={ly:self.pair_minima.get((names,ly)) for ly in q.LAYERS}
   rows.append({'nets':list(names),'surface_target_mm':r['surface_creepage_target_mm'],'route_air_target_mm':r['route_clearance_target_mm'],'by_layer':bylayer})
  regions=[{'exception_index':i,'ref':e['ref'],'pins':e['pins'],'nets':e['nets'],'layer':'B.Cu','pad_bbox_plus_margin_mm':e['escape_margin_mm'],'actual_region_bbox_mm':[k.ToMM(x) for x in q.bbox(self.exception_region(e))],'floor_mm':e['proposed_drawn_floor_mm']} for i,e in enumerate(self.c.exceptions)]
  return {'passed':not self.findings,'findings':self.findings,'stats':self.stats,'all_55_pair_minima':rows,'nc_pair_minima':[{'nets':list(pair),'layer':ly,**v} for (pair,ly),v in self.pair_minima.items() if 'EXPLICIT_NC' in pair],'copper_edge_target_mm':edge,'copper_edge_minimum':edge_min,'actual_outline_vertices_mm':self.outline_vertices,'finite_exception_ids_used':sorted(self.used),'actual_finite_exception_regions':regions}

def run(board,project,matrix,exceptions=None):
 before=q.sha(board);r={'board_sha256':before,'checker_sha256':q.sha(__file__),'kernel_sha256':q.sha(HERE/'kernel_sc08.py'),'kicad_version':k.GetBuildVersion(),'limits':['Planar same-face saved-copper surface-distance screen, no soldermask credit; not three-dimensional air/solder creepage, component-body qualification or IEC compliance.','Conservative outward native polygons max approximation error0.002mm; fail may be conservative near exact target.','Only straight tracks, throughvias, native supported pad polygons, saved filled zones and one closed straight native outline; unsupported copper stops.','DRC, refill freshness, schematic parity, accessibility, solder joints, thermal tests and actual inspection remain separate.','Package concessions, if explicitly supplied with actor and hashes, are bounded laboratory geometric assessments, not standards waivers.']}
 try:
  if k.GetBuildVersion()!='10.0.6':raise q.Unsupported('Pinned KiCad10.0.6 required')
  c=Contract(project,matrix,exceptions);b=q.load_native(board)
  raw=q.raw_track_nets(board);loaded={str(t.m_Uuid.AsString()):t.GetNetname() for t in b.GetTracks()}
  if raw!=loaded:raise q.Unsupported('Raw saved track/via net identities changed at load')
  r.update(raw_native_track_net_parity=True,input_hashes=c.input_hashes,exceptions_applied=bool(c.exceptions));r.update(Checker(b,c).run())
 except Exception as e:r.update(passed=False,stopped=True,error=type(e).__name__+': '+str(e))
 r['board_sha256_after']=q.sha(board);r['input_unchanged']=before==r['board_sha256_after']
 if not r['input_unchanged']:r['passed']=False
 return r

def main():
 p=argparse.ArgumentParser();p.add_argument('--board',required=True);p.add_argument('--project',required=True);p.add_argument('--matrix',required=True);p.add_argument('--exceptions');p.add_argument('--report',required=True);a=p.parse_args()
 r=run(a.board,a.project,a.matrix,a.exceptions);dump(a.report,r)
 print(json.dumps({x:r.get(x) for x in ['passed','stopped','error','stats','board_sha256','input_unchanged']}));return 0 if r['passed'] else 1
if __name__=='__main__':sys.exit(main())
