"""Read-only inventory of true two-track right-angle elbows, excluding branches."""
from pathlib import Path
import sys,json,math,hashlib,argparse,collections
import pcbnew as k
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
ap=argparse.ArgumentParser();ap.add_argument('--board',required=True);ap.add_argument('--project',required=True);ap.add_argument('--matrix',required=True);ap.add_argument('--assessment',required=True);ap.add_argument('--output',required=True);ap.add_argument('--actor',default='/root');a=ap.parse_args();src=Path(a.board);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();before=sha(src);b=c.q.load_native(src);co=c.Checker(b,c.Contract(a.project,a.matrix,a.assessment));co.collect();tracks=[t for t in b.GetTracks()if not isinstance(t,k.PCB_VIA)];nodes=collections.defaultdict(list)
for t in tracks:
 for p in[t.GetStart(),t.GetEnd()]:nodes[(t.GetNetname(),t.GetLayer(),p.x,p.y)].append(t)
def on_segment(p,t):
 s=t.GetStart();e=t.GetEnd();dx,dy=e.x-s.x,e.y-s.y;px,py=p.x-s.x,p.y-s.y;d=dx*dx+dy*dy
 return d and abs(dx*py-dy*px)<=1000*math.sqrt(d)and -1000*math.sqrt(d)<=px*dx+py*dy<=d+1000*math.sqrt(d)
rows=[]
for key,ts in nodes.items():
 if len(ts)!=2:continue
 net,layer,x,y=key;p=k.VECTOR2I(x,y)
 if any(t.GetNetname()==net and t.GetLayer()==layer and t not in ts and on_segment(p,t)for t in tracks):continue
 vectors=[]
 for t in ts:
  q=t.GetEnd()if(t.GetStart().x,t.GetStart().y)==(x,y)else t.GetStart();vectors.append((q.x-x,q.y-y))
 (dx,dy),(ex,ey)=vectors;den=math.hypot(dx,dy)*math.hypot(ex,ey)
 if not den:continue
 angle=math.degrees(math.acos(max(-1,min(1,(dx*ex+dy*ey)/den))))
 if abs(angle-90)>.001:continue
 terminals=[o.id for o in co.objects if o.layer==b.GetLayerName(layer)and o.native_net==net and o.kind in['pad','via']and o.shape.Contains(p)]
 rows.append({'net':net,'layer':b.GetLayerName(layer),'point_mm':[k.ToMM(x)-100,k.ToMM(y)-100],'tracks':[t.m_Uuid.AsString()for t in ts],'inside_terminals':terminals,'leg_lengths_mm':[k.ToMM(t.GetLength())for t in ts]})
r={'actual_actor':a.actor,'PCB_sha256':before,'source_unchanged':sha(src)==before,'right_angle_two_track_corners':rows,'outside_terminal_90_corners':[x for x in rows if not x['inside_terminals']],'terminal_contained_corners':[x for x in rows if x['inside_terminals']],'limits':'Two-track topology and exact native endpoint geometry only. Excludes actual branches, pad/via-contained joins. A residual exposed corner requires a reasoned electrical/mechanical review, not automatic floor relaxation.'};Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'PCB_sha256':before,'total_90_corners':len(rows),'outside_terminals':len(r['outside_terminal_90_corners']),'inside_terminals':len(r['terminal_contained_corners'])}))
