"""Read-only terminal centering and short parallel-run stair-step audit."""
from pathlib import Path
import sys,json,math,collections,argparse,hashlib
import pcbnew as k
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
ap=argparse.ArgumentParser();ap.add_argument('--board',required=True);ap.add_argument('--project',required=True);ap.add_argument('--matrix',required=True);ap.add_argument('--assessment',required=True);ap.add_argument('--output',required=True);ap.add_argument('--actor',default='/root');a=ap.parse_args()
src=Path(a.board);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();before=sha(src);b=c.q.load_native(src);co=c.Checker(b,c.Contract(a.project,a.matrix,a.assessment));co.collect();native=list(b.GetTracks());tracks=[t for t in native if not isinstance(t,k.PCB_VIA)];objects={o.id:o for o in co.objects if o.kind=='track'}
def pt(p):return(k.ToMM(p.x),k.ToMM(p.y))
def relative(p):return[p[0]-100,p[1]-100]
def distance(p,s,e):
 dx,dy=e[0]-s[0],e[1]-s[1];d=dx*dx+dy*dy;t=max(0,min(1,((p[0]-s[0])*dx+(p[1]-s[1])*dy)/d)) if d else 0
 return math.hypot(p[0]-s[0]-t*dx,p[1]-s[1]-t*dy)
def record(t,p):return{'uuid':t.m_Uuid.AsString(),'centerline_distance_mm':distance(p,pt(t.GetStart()),pt(t.GetEnd())),'start_mm':relative(pt(t.GetStart())),'end_mm':relative(pt(t.GetEnd())),'width_mm':k.ToMM(t.GetWidth())}
vias=[];bad=[];spurs=[]
for v in native:
 if not isinstance(v,k.PCB_VIA):continue
 p=pt(v.GetPosition());radius=k.ToMM(v.GetWidth(k.F_Cu))/2;row={'uuid':v.m_Uuid.AsString(),'net':v.GetNetname(),'center_mm':relative(p),'diameter_mm':2*radius,'faces':{}}
 for layer in[k.F_Cu,k.B_Cu]:
  contacts=[record(t,p)for t in tracks if t.GetLayer()==layer and t.GetNetname()==v.GetNetname()and distance(p,pt(t.GetStart()),pt(t.GetEnd()))<=radius+k.ToMM(t.GetWidth())/2+.002]
  centered=[x for x in contacts if x['centerline_distance_mm']<=.001];row['faces'][b.GetLayerName(layer)]={'contacts':contacts,'centered_track_UUIDs':[x['uuid']for x in centered]}
  if contacts and not centered:bad.append({'via':row['uuid'],'net':row['net'],'center_mm':row['center_mm'],'face':b.GetLayerName(layer),'contacts':contacts})
  nearby=[t for t in tracks if t.GetLayer()==layer and t.GetNetname()==v.GetNetname()]
  if not any(distance(p,pt(t.GetStart()),pt(t.GetEnd()))<=.001 and k.ToMM(t.GetLength())>.4 for t in nearby):
   for t in nearby:
    if k.ToMM(t.GetLength())>.4:continue
    s,e=pt(t.GetStart()),pt(t.GetEnd());q=e if math.dist(p,s)<=.001 else s if math.dist(p,e)<=.001 else None
    if q is None:continue
    trunks=[u for u in nearby if u.m_Uuid!=t.m_Uuid and k.ToMM(u.GetLength())>.8 and .001<distance(p,pt(u.GetStart()),pt(u.GetEnd()))<=radius+k.ToMM(u.GetWidth())/2+.002 and distance(q,pt(u.GetStart()),pt(u.GetEnd()))<=.001 and min(math.dist(q,pt(u.GetStart())),math.dist(q,pt(u.GetEnd())))>.001]
    if trunks:spurs.append({'via':row['uuid'],'net':row['net'],'face':b.GetLayerName(layer),'center_mm':row['center_mm'],'short_stub_uuid':t.m_Uuid.AsString(),'stub_length_mm':k.ToMM(t.GetLength()),'trunk_junction_mm':relative(q),'trunk_UUIDs':[u.m_Uuid.AsString()for u in trunks]})
 vias.append(row)
links=collections.defaultdict(list)
for t in tracks:
 for p in[t.GetStart(),t.GetEnd()]:links[(t.GetNetname(),t.GetLayer(),p.x,p.y)].append(t)
stairs=[];widthsteps=[]
def entirely_in_terminal(t):
 o=objects[t.m_Uuid.AsString()]
 return any(x.layer==o.layer and x.net==o.net and x.kind in['pad','via']and c.q.clipped(o.shape,x.shape,False).IsEmpty()for x in co.objects)
for t in tracks:
 if k.ToMM(t.GetLength())>.31 or entirely_in_terminal(t):continue
 s,e=t.GetStart(),t.GetEnd();ls=links[(t.GetNetname(),t.GetLayer(),s.x,s.y)];le=links[(t.GetNetname(),t.GetLayer(),e.x,e.y)]
 if len(ls)!=2 or len(le)!=2:continue
 x=next(x for x in ls if x.m_Uuid!=t.m_Uuid);y=next(x for x in le if x.m_Uuid!=t.m_Uuid)
 def vector(q,node):
  z=q.GetEnd()if pt(q.GetStart())==pt(node)else q.GetStart();return(z.x-node.x,z.y-node.y)
 dx,dy=vector(x,s);ex,ey=vector(y,e);mx,my=e.x-s.x,e.y-s.y
 if dx*ey-dy*ex==0 and dx*ex+dy*ey<0 and dx*my-dy*mx!=0:stairs.append({'middle_uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'face':b.GetLayerName(t.GetLayer()),'start_mm':relative(pt(s)),'end_mm':relative(pt(e)),'length_mm':k.ToMM(t.GetLength()),'outer_UUIDs':[x.m_Uuid.AsString(),y.m_Uuid.AsString()]})
for key,ts in links.items():
 if len(ts)!=2 or ts[0].GetWidth()==ts[1].GetWidth():continue
 net,ly,x,y=key;p=k.VECTOR2I(x,y);vectors=[]
 for t in ts:
  q=t.GetEnd()if(t.GetStart().x,t.GetStart().y)==(x,y)else t.GetStart();vectors.append((q.x-x,q.y-y))
 (dx,dy),(ex,ey)=vectors
 if dx*ey-dy*ex==0 and dx*ex+dy*ey<0:widthsteps.append({'net':net,'face':b.GetLayerName(ly),'junction_mm':relative(pt(p)),'widths_mm':[k.ToMM(t.GetWidth())for t in ts],'UUIDs':[t.m_Uuid.AsString()for t in ts]})
r={'actual_actor':a.actor,'PCB_sha256':before,'source_unchanged':sha(src)==before,'via_count':len(vias),'vias':vias,'offcenter_via_faces':bad,'short_parallel_run_stair_steps':stairs,'collinear_width_step_candidates':widthsteps,'junction_acceptance_pass':not bad and not stairs,'limits':'1um centreline tolerance, actual saved straight traces and circular throughvias. Width-step candidates require engineering review; this geometry audit does not prove electrical spacing, impedance, Kelvin topology, physical assembly or safety.'}
r['short_side_spur_vias']=spurs;r['junction_acceptance_pass']=r['junction_acceptance_pass']and not spurs
r['spur_scope']='A short side branch joining the interior of a passing long track; a centred two-leg L endpoint approach is not a side-spur defect.'
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'PCB_sha256':before,'vias':len(vias),'offcenter_faces':len(bad),'short_stairs':len(stairs),'short_via_side_spurs':len(spurs),'width_step_candidates':len(widthsteps),'junction_pass':r['junction_acceptance_pass']}))
