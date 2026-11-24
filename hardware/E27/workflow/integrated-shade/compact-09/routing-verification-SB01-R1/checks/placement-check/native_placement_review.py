"""Read-only independent component envelope and practical manufacturing screen."""
from pathlib import Path
import json,math,hashlib,itertools
import pcbnew as k
H=Path(__file__).resolve().parent;S=H.parent/'baseline';src=S/'SC09_compact.kicad_pcb'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(src);b=k.LoadBoard(str(src));g=json.loads((S/'footprint-geometry.json').read_text());model=json.loads((S/'Models/MODEL_INFO.json').read_text());models={r['ref']:r for r in model['models']};refs={f.GetReference():f for f in b.GetFootprints()}
override={'C1':([-9.25,-3.85,9.25,3.85],13.6,'Current selected KEMET R76 primary maximum in footprint description; old model rejected.'),'RV1':([-2.2,-4.5,2.2,4.5],11,'Current TDK S07K275 maximum from footprint description; old model rejected.'),'T1':([-6.25,-6.25,6.25,6.25],10.5,'Wuerth 7687709152 primary12.0+/-0.5 square/10.5 maximum.'),'R6':([-1.65,-.85,1.65,.85],.7,'Conservative1206 planning reservation; exact Royalohm termination/sample fit remains unqualified, not manufacturer guaranteed dimensions.')}
rows=[];warnings=[];bodymaps={}
for ref,f in refs.items():
 pads=list(f.Pads());actual={p.GetNumber():p for p in pads};row={'ref':ref,'side':'B'if f.IsFlipped()else'F','position_mm':[k.ToMM(f.GetPosition().x),k.ToMM(f.GetPosition().y)],'angle_deg':f.GetOrientationDegrees(),'description':f.GetLibDescription(),'pads':[{'pin':p.GetNumber(),'position_mm':[k.ToMM(p.GetPosition().x),k.ToMM(p.GetPosition().y)],'size_mm':[k.ToMM(p.GetSize().x),k.ToMM(p.GetSize().y)],'drill_mm':[k.ToMM(p.GetDrillSize().x),k.ToMM(p.GetDrillSize().y)],'net':p.GetNetname()}for p in pads]}
 if ref in ['J1','J2']:rows.append(row);continue
 box,height,basis=override.get(ref,(g[ref]['max_body_bbox_xy_mm'],g[ref]['planned_max_above_PCB_mm'],g[ref]['design_basis'])) if ref not in override else override[ref]
 # Explicit screen-coordinate rotation; native bottom transform mirrors local Y.
 theta=math.radians(-f.GetOrientationDegrees());co,si=math.cos(theta),math.sin(theta)
 def transform(x,y):
  if f.IsFlipped():y=-y
  return(row['position_mm'][0]+co*x-si*y,row['position_mm'][1]+si*x+co*y)
 corners=[transform(x,y)for x in [box[0],box[2]]for y in [box[1],box[3]]]
 glob=[min(x for x,y in corners),min(y for x,y in corners),max(x for x,y in corners),max(y for x,y in corners)]
 row.update(body_bbox_global_mm=glob,height_mm=height,basis=basis);bodymaps[ref]=glob
 # Check mapping with first two independent source-local pad coordinates.
 comparisons=[]
 for p in g[ref]['pads']:
  n=p.get('number');loc=p.get('center_mm')
  if n in actual and loc:
   x,y=transform(*loc);ap=actual[n].GetPosition();comparisons.append(math.hypot(x-k.ToMM(ap.x),y-k.ToMM(ap.y)))
 row['geometry_local_pad_mapping_max_error_mm']=max(comparisons)if comparisons else None
 if comparisons and max(comparisons)>.00001:warnings.append({'ref':ref,'type':'stored-local-geometry-transform-mismatch','maximum_error_mm':max(comparisons)})
 rows.append(row)
def gap(a,z):
 dx=max(a[0]-z[2],z[0]-a[2],0);dy=max(a[1]-z[3],z[1]-a[3],0);return math.hypot(dx,dy)
overlaps=[]
for a,z in itertools.combinations([x for x in rows if'body_bbox_global_mm'in x],2):
 if a['side']!=z['side']:continue
 aa,zz=a['body_bbox_global_mm'],z['body_bbox_global_mm'];ix=min(aa[2],zz[2])-max(aa[0],zz[0]);iy=min(aa[3],zz[3])-max(aa[1],zz[1])
 if ix>0 and iy>0:overlaps.append({'refs':[a['ref'],z['ref']],'bbox_intersection_mm':[ix,iy],'note':'Bounding reservation intersection; assess actual body shape before asserting collision.'})
heatpairs={a+'-'+z:gap(bodymaps[a],bodymaps[z])for a,z in [('RF1','C6'),('T1','C6'),('R7','C6'),('L1','U1'),('C1','U1')]}
minimum_track=min(k.ToMM(t.GetWidth())for t in b.GetTracks()if not isinstance(t,k.PCB_VIA));ann=[]
for f in refs.values():
 for p in f.Pads():
  d=p.GetDrillSize();sz=p.GetSize()
  if d.x:ann.append({'object':f.GetReference()+'.'+p.GetNumber(),'ring_mm':min(k.ToMM(sz.x-d.x),k.ToMM(sz.y-d.y))/2})
for t in b.GetTracks():
 if isinstance(t,k.PCB_VIA):ann.append({'object':t.m_Uuid.AsString(),'ring_mm':(k.ToMM(t.GetWidth(k.F_Cu))-k.ToMM(t.GetDrillValue()))/2})
report={'actor':'/root/sb01_refine_placement_check','scope':'Read-only baseline mechanical/assembly/layout screen; not final role review, powered qualification or measured thermal result.','board_sha256':before,'native_version':k.GetBuildVersion(),'source_unchanged':before==sha(src),'parts':rows,'same_face_body_reservation_intersections':overlaps,'stored_geometry_warnings':warnings,'heat_and_filter_body_reservation_gaps_mm':heatpairs,'minimum_track_width_mm':minimum_track,'annular_ring_minimum_mm':min(x['ring_mm']for x in ann),'annular_ring_inventory':ann,'limits':['R6 exact Royalohm lands/terminations require actual sample solder inspection.','Native manufacturer-neutral body/courtyard reservations and custom axial/horizontal lead forming do not qualify assembly or enclosure fit.','No component temperature is predicted from the geometry alone.','JLC manufacturing minima are distinct from mains insulation criteria.']}
(H/'baseline-placement.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({key:report[key]for key in ['board_sha256','source_unchanged','same_face_body_reservation_intersections','stored_geometry_warnings','heat_and_filter_body_reservation_gaps_mm','minimum_track_width_mm','annular_ring_minimum_mm']}))
