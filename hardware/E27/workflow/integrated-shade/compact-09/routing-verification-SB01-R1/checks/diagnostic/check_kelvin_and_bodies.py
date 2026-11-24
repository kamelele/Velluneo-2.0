"""Exact polygon contacts and protected-body checks on baseline; no CAD mutation."""
from pathlib import Path
import json,sys,hashlib
import pcbnew as k
H=Path(__file__).resolve().parent;ROOT=H.parents[2];P=H.parent/'baseline'
sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
pcb=P/'SC09_compact.kicad_pcb';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(pcb)
b=c.q.load_native(pcb);co=c.Checker(b,c.Contract(P,ROOT/'work/routing-improvement/spacing-matrix.CAT01.json',None));co.collect()
rows=json.loads((H/'baseline-diagnostic.json').read_text());sense=next(x for x in rows['paths']if x['from']=='U1.3'and x['to']=='R5.2');ids=set(sense['object_ids'])-{'U1.3','R5.2'}
quiet=[o for o in co.objects if o.id in ids];r5={o.layer:o.shape for o in co.objects if o.id=='R5.2'};findings=[];hits=0
for a in quiet:
 for z in co.objects:
  if a.layer!=z.layer or z.net!='FB_INDUCTOR' or z.id in ids|{'R5.2','U1.3'}:continue
  overlap=c.q.clipped(a.shape,z.shape)
  if overlap.IsEmpty():continue
  hits+=1
  if a.layer in r5:overlap.BooleanSubtract(r5[a.layer])
  if not overlap.IsEmpty():findings.append({'sense':a.id,'force_or_other':z.id,'face':a.layer,'area_outside_R5_pad_mm2':overlap.Area()/1e12})
fs={f.GetReference():f for f in b.GetFootprints()};t=fs['T1'].GetPosition();x,y=k.ToMM(t.x),k.ToMM(t.y);box=[x-6.25,y-6.25,x+6.25,y+6.25]
def rect(bb):
 p=k.SHAPE_POLY_SET();p.NewOutline()
 for x,y in[(bb[0],bb[1]),(bb[2],bb[1]),(bb[2],bb[3]),(bb[0],bb[3])]:p.Append(k.FromMM(x),k.FromMM(y))
 return p
t1=rect(box);under=[]
for a in co.objects:
 if a.net not in ['BP','M']and a.id not in ids:continue
 overlap=c.q.clipped(a.shape,t1)
 if not overlap.IsEmpty():under.append({'id':a.id,'net':a.net,'face':a.layer,'area_mm2':overlap.Area()/1e12})
c6=rect(json.loads((P/'spatial-constraints.json').read_text())['areas'][0]['rectangle_mm']);c6hits=[]
for a in co.objects:
 if not c.q.clipped(a.shape,c6).IsEmpty():c6hits.append({'id':a.id,'net':a.net,'face':a.layer})
result={'actor':'/root/sb01_refine_diagnostic','board_sha256':before,'quiet_path_UUIDs':sorted(ids),'quiet_copper_face_objects':len(quiet),'same_net_intersections_checked':hits,'quiet_force_contacts_outside_R5_pad':findings,'Kelvin_geometry_pass':bool(ids)and not findings,'T1_max_body_mm':box,'BP_M_or_Kelvin_sense_under_T1':under,'T1_sensitive_copper_pass':not under,'C6_reserved_area_hits':c6hits,'C6_reservation_pass':not c6hits,'source_unchanged':before==sha(pcb),'limits':'Endpoint path identifies actual sense branch; outward saved-copper polygons prove local contacts only, not impedance or magnetic/noise/thermal performance. T1 square12.5 maximum body; C6 existing both-face reservation. No physical measurement or approval.'}
(H/'kelvin-and-bodies.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
