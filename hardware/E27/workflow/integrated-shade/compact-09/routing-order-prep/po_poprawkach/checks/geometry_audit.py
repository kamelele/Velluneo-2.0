"""Read-only axis/45-degree, terminal-position and routing-junction audit."""
from pathlib import Path
import sys,json,math,collections,hashlib,argparse
import pcbnew as k
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
ap=argparse.ArgumentParser();ap.add_argument('--board',required=True);ap.add_argument('--project',required=True);ap.add_argument('--matrix',required=True);ap.add_argument('--assessment',required=True);ap.add_argument('--output',required=True);ap.add_argument('--actor',default='/root');a=ap.parse_args()
src=Path(a.board);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();before=sha(src);b=c.q.load_native(src);co=c.Checker(b,c.Contract(a.project,a.matrix,a.assessment));co.collect();objects={o.id:o for o in co.objects if o.kind=='track'};pads=[o for o in co.objects if o.kind=='pad'];tracks=list(b.GetTracks());rows=[];duplicates=[];seen={};joints=collections.defaultdict(list)
for t in tracks:
 if isinstance(t,k.PCB_VIA):continue
 u=t.m_Uuid.AsString();s=t.GetStart();e=t.GetEnd();dx=abs(e.x-s.x);dy=abs(e.y-s.y);angle=math.degrees(math.atan2(dy,dx));aligned=min(dx,dy,abs(dx-dy))<=1000;o=objects[u]
 within=[p.id for p in pads if p.layer==o.layer and p.net==o.net and c.q.clipped(o.shape,p.shape,False).IsEmpty()]
 row={'uuid':u,'net':t.GetNetname(),'layer':b.GetLayerName(t.GetLayer()),'start_mm':[k.ToMM(s.x)-100,k.ToMM(s.y)-100],'end_mm':[k.ToMM(e.x)-100,k.ToMM(e.y)-100],'length_mm':k.ToMM(t.GetLength()),'acute_axis_angle_deg':angle,'axis_or45_within1um':aligned,'fully_inside_same_net_pad':within};rows.append(row)
 key=(t.GetNetname(),t.GetLayer(),t.GetWidth(),tuple(sorted([(s.x,s.y),(e.x,e.y)])))
 if key in seen:duplicates.append([seen[key],u])
 seen[key]=u
 for p in[s,e]:joints[(t.GetNetname(),t.GetLayer(),p.x,p.y)].append(t)
 irregular=[r for r in rows if not r['axis_or45_within1um']and not r['fully_inside_same_net_pad']]
 bends=[];collinear=[]
for key,ts in joints.items():
 if len(ts)!=2:continue
 net,layer,x,y=key;point=k.VECTOR2I(x,y)
 if any(o.layer==b.GetLayerName(layer)and o.native_net==net and o.kind in['pad','via']and o.shape.Contains(point)for o in co.objects):continue
 vectors=[]
 for t in ts:
  s=t.GetStart();e=t.GetEnd();p=e if(s.x,s.y)==(x,y)else s;vectors.append((p.x-x,p.y-y))
 (dx,dy),(ex,ey)=vectors;norm=math.hypot(dx,dy)*math.hypot(ex,ey)
 if not norm:continue
 inside=math.degrees(math.acos(max(-1,min(1,(dx*ex+dy*ey)/norm))))
 row={'UUIDs':[t.m_Uuid.AsString()for t in ts],'net':net,'layer':b.GetLayerName(layer),'point_mm':[k.ToMM(x)-100,k.ToMM(y)-100],'inside_angle_deg':inside}
 if inside<89.9:bends.append(row)
 if inside>179.99 and ts[0].GetWidth()==ts[1].GetWidth():collinear.append(row)
ports={f.GetReference():{p.GetNumber():{'net':p.GetNetname(),'x_mm':k.ToMM(p.GetPosition().x)-100,'y_mm':k.ToMM(p.GetPosition().y)-100}for p in f.Pads()}for f in b.GetFootprints()if f.GetReference()in['J1','J2']}
opposite=all(p['x_mm']>=47 for p in ports['J1'].values())and all(p['x_mm']<=3 for p in ports['J2'].values());minimum=min(math.dist([x['x_mm'],x['y_mm']],[y['x_mm'],y['y_mm']])for x in ports['J1'].values()for y in ports['J2'].values())
r={'actual_actor':'/root','PCB_sha256':before,'read_only_source_unchanged':sha(src)==before,'ports':ports,'AC_right_LED_left':opposite,'minimum_AC_LED_pad_center_separation_mm':minimum,'track_segments':len(rows),'through_vias':sum(isinstance(t,k.PCB_VIA)for t in tracks),'total_track_length_mm':sum(x['length_mm']for x in rows),'non45_outside_actual_same_net_pads':irregular,'exact_duplicates':duplicates,'acute_two_track_junctions_outside_pads_vias':bends,'collinear_merge_candidates_not_in_pad_via':collinear,'shorter_than0_3mm_outside_pads':[x for x in rows if x['length_mm']<.3 and not x['fully_inside_same_net_pad']],'all_segments':rows,'geometry_acceptance_pass':opposite and not irregular and not duplicates and not bends,'limits':'1um centreline alignment tolerance. This does not establish electrical clearance, copper-width/courtyard compliance, parasitic behavior, thermal performance or physical safety; those are separately checked. Collinear candidates and short runs are review diagnostics, not automatic electrical faults.'}
r['actual_actor']=a.actor
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({key:r[key]for key in['PCB_sha256','AC_right_LED_left','minimum_AC_LED_pad_center_separation_mm','track_segments','through_vias','total_track_length_mm','geometry_acceptance_pass']}));print('Non45',len(irregular),'acute',len(bends),'duplicates',len(duplicates),'collinear_candidates',len(collinear))
