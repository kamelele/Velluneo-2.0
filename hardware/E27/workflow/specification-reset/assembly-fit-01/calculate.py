"""Conditional all-part assembly envelopes; no thermal/electrical qualification."""
from pathlib import Path
import json,math,itertools,hashlib
D=Path(__file__).resolve().parent;P=D.parent
C=json.loads((D/'assembly-contract.json').read_text(encoding='utf-8'));L=json.loads((D/'packing-diagnostic.json').read_text(encoding='utf-8'));H=json.loads((D/'height-contract.json').read_text(encoding='utf-8'));B=json.loads((D/'native-body-bounds.json').read_text(encoding='utf-8'));I=json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'));bd=C['board'];cup=C['cup'];hm={p['ref']:p for p in H['parts']};fb={p['ref']:p['native_fab_stroke_bbox_mm']for p in B['parts']}
def write(n,o):(D/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def xy(x,y,c):
 if c['side']=='B':y=-y
 if c['angle_deg']==90:x,y=y,-x
 return x+c['x_mm'],y+c['y_mm']
def project(b,c):
 v=[xy(x,y,c)for x in(b[0],b[2])for y in(b[1],b[3])];return[min(p[0]for p in v),min(p[1]for p in v),max(p[0]for p in v),max(p[1]for p in v)]
def partbox(ref,c):
 b=fb[ref]
 if ref=='T1':b=[-15,-15,15,15]
 if ref=='C1':b=[-5.25,-5.25,5.25,5.25]
 if ref=='R1':b=[-9,-3.75,9,3.75]
 if ref in('J1','J2'):return c['courtyard_bbox_mm']
 return project(b,c)
def radius(z):
 k=cup['lower_outer_profile_Z_R_mm']
 if z<=k[0][0]:return k[0][1]
 for (a,r),(b,s)in zip(k,k[1:]):
  if z<=b:return r+(s-r)*(z-a)/(b-a)
 return k[-1][1]
def sdf_roundrect(x,d,box,r):
 a,b,c,e=box;qx=abs(x-(a+c)/2)-(c-a)/2+r;qy=abs(d-(b+e)/2)-(e-b)/2+r
 return math.hypot(max(qx,0),max(qy,0))+min(max(qx,qy),0)-r
def room(x,d,z,worst=False):
 er=cup['cavity_erosion_mm']if worst else 0
 wall=cup['nose_overlap_radial_stack_mm']if cup['nose_joint_Z_mm'][0]<=z<=cup['nose_joint_Z_mm'][1]else cup['proposed_wall_mm']
 radial=radius(z)-wall-er-math.hypot(x,d)
 if z>=cup['upper_cavity_from_Z_mm']:
  radial=min(radial,-sdf_roundrect(x,d,cup['upper_inside_X_D_box_mm'],cup['upper_inside_corner_r_mm'])-er)
 return min(radial,z-(cup['floor_inner_Z_mm']+(.3 if worst else 0)),(cup['cover_inner_Z_mm']-(.3 if worst else 0))-z)
def minimum_clearance(box,worst):
 x0,d0,z0,x1,d1,z1=box;zs=sorted(set([z0,z1]+[v for v in[30,34,40,56,63]if z0<=v<=z1]));return min(room(x,d,z,worst)for x in(x0,x1)for d in(d0,d1)for z in zs)
def collide(a,b):return all(a[i]<b[i+3]and b[i]<a[i+3]for i in range(3))
parts=[]
for ref,c in L['positions'].items():
 p=hm[ref];b=partbox(ref,c);sgn=1 if c['side']=='F'else-1;mount=bd['normal_midplane_D_mm']+sgn*bd['thickness_mm']/2;h=p['installed_envelope_mm'];normal=sorted([mount,mount+sgn*h]);box=[b[0],normal[0],bd['center_Z_mm']-b[3],b[2],normal[1],bd['center_Z_mm']-b[1]]
 worsts=[]
 for mx,md,th in itertools.product([-bd['mount_X_bound_mm'],bd['mount_X_bound_mm']],[-bd['mount_D_bound_mm'],bd['mount_D_bound_mm']],[bd['thickness_mm']-bd['thickness_tol_mm'],bd['thickness_mm']+bd['thickness_tol_mm']]):
  seat=bd['normal_midplane_D_mm']+md+sgn*th/2;ds=sorted([seat,seat+sgn*h]);tol=bd['part_position_bound_mm'];zerr=bd['mount_Z_bound_mm']+tol
  worsts.append([b[0]+mx-tol,ds[0],box[2]-zerr,b[2]+mx+tol,ds[1],box[5]+zerr])
 wc=min(minimum_clearance(q,True)for q in worsts)
 parts.append(dict(ref=ref,side=c['side'],height=p['installed_envelope_mm'],body_XY_bbox_mm=b,nominal_box_X_D_Z_mm=box,nominal_cavity_clearance_mm=minimum_clearance(box,False),worst_allocated_cavity_clearance_mm=wc,height_qualified=False))
# Correlated global board pose cancels for inter-part collision; only individual +/-0.10 location errors expand X/Z.
collisions=[]
for a,b in itertools.combinations(parts,2):
 aa=a['nominal_box_X_D_Z_mm'][:];bb=b['nominal_box_X_D_Z_mm'][:]
 for q in(aa,bb):q[0]-=.1;q[2]-=.1;q[3]+=.1;q[5]+=.1
 if collide(aa,bb):collisions.append([a['ref'],b['ref']])
# Full-face capacitor vent reservation, independently including the required extra2mm.
c1=next(v for v in parts if v['ref']=='C1');b=c1['body_XY_bbox_mm'];ventmin=999
for mx,md,th in itertools.product([-.3,.3],[-.3,.3],[1.5,1.7]):
 seat=.6+md-th/2;vd=seat-hm['C1']['installed_envelope_mm']-C['vent_keepout_mm']
 for x in(b[0]+mx-.1,b[2]+mx+.1):
  for z in(c1['nominal_box_X_D_Z_mm'][2]-.6,c1['nominal_box_X_D_Z_mm'][5]+.6):ventmin=min(ventmin,room(x,vd,z,True))
# Required guide clearances; tolerance correlation is explicit rather than adding impossible independent offsets.
guide={'channel_width_mm':32.3,'channel_tol_mm':.1,'board_width_mm':32,'board_width_tol_mm':.15,'min_width_insertion_clearance_mm':32.2-32.15,'maximum_achievable_X_float_mm':(32.4-31.85)/2,'slot_width_mm':2.0,'slot_width_tol_mm':.1,'min_thickness_insertion_clearance_mm':1.9-1.7,'maximum_achievable_D_float_mm':(2.1-1.5)/2,'retention_strength_qualified':False}
rail_candidates=[]
for zc in range(57,80):
 rails=[]
 for sg in(-1,1):
  xlo,xhi=sorted([sg*15.6,sg*17])
  rails.extend([[xlo,-1.0,zc-1.5,xhi,-.4,zc+1.5],[xlo,1.6,zc-1.5,xhi,2.2,zc+1.5]])
 hit=[]
 for v in parts:
  q=v['nominal_box_X_D_Z_mm'][:];q[0]-=.4;q[3]+=.4;q[2]-=.6;q[5]+=.6
  if any(collide(q,rr)for rr in rails):hit.append(v['ref'])
 if not hit:rail_candidates.append(zc)
nom=sum(v['nominal_mm']for v in C['axial_chain']);tt=sum(v['required_plusminus_mm']for v in C['axial_chain']);cool=C['cooler'];minpart=min(parts,key=lambda p:p['worst_allocated_cavity_clearance_mm'])
outer=cup['upper_outer_X_D_box_mm'];r=cup['upper_outer_corner_r_mm'];uppermax=max(math.hypot(x,d)for x in[outer[0]+r,outer[2]-r]for d in[outer[1]+r,outer[3]-r])+r
web=(cool['finished_OD_mm']-cool['OD_plusminus_mm'])/2-uppermax-cool['pocket_nominal_cup_gap_mm']-.2
old=json.loads((P/'rectangular-driver-01/packing-diagnostic.json').read_text(encoding='utf-8'));delta=[{'ref':ref,'before':{k:old['positions'][ref][k]for k in['x_mm','y_mm','angle_deg','side']},'after':{k:c[k]for k in['x_mm','y_mm','angle_deg','side']}}for ref,c in L['positions'].items()if any(c[k]!=old['positions'][ref][k]for k in['x_mm','y_mm','angle_deg','side'])]
result={'scope':'Conditional bounding-envelope calculation, not measured or supplier-qualified fit/thermal/electrical performance. All installed height/process allowances remain unqualified.','coordinate_transform':'WorldX=boardX; worldD is normal to powerPCB with midplane+0.6mm; worldZ=61-boardY. Board spansZ31..91, not a transverse rounddisc.','part_count':len(parts),'nominal_height_mm':nom,'worst_required_chain_height_mm':nom+tt,'required_chain_plusminus_mm':tt,'target_height_mm':120,'height_budget_pass':nom+tt<=120,'finished_max_diameter_mm':max(cool['finished_OD_mm']+cool['OD_plusminus_mm'],2*max(v[1]for v in cup['lower_outer_profile_Z_R_mm'])+.2),'target_diameter_mm':60,'part_results':parts,'body_collision_pairs_with_individual_XZ_tolerance':collisions,'minimum_cavity_clearance_ref':minpart['ref'],'minimum_allocated_cavity_clearance_mm':minpart['worst_allocated_cavity_clearance_mm'],'fullface_C1_vent2mm_reservation_residual_clearance_mm':ventmin,'upper_cup_max_nominal_radius_mm':uppermax,'minimum_allocated_cooler_metal_web_mm':web,'guide':guide,'unused_side_rail_candidate_centers_mm':rail_candidates,'layout_delta':delta,'conditional_geometry_pass':all(v['worst_allocated_cavity_clearance_mm']>=.3 for v in parts)and not collisions and ventmin>=0 and nom+tt<=120 and web>=.8,'PCB_entry_ready':False,'residuals':['Finished T1 maximum not qualified.','F1 maximum tolerance and BR1/ST-SMA seating datums unresolved.','Installed solder/stand-off/guide/lead-form tolerances are required design inputs, not confirmed capability.','RubyconventtableMAX/MIN conflict needs clarification;2mm is explicitprojectreserve, not claimednorm.','Actual cap, insulating material/EIS, bushing/contact/wire/strain-relief, service retention and fabrication capability unselected/unqualified.','Custom annular radiator has no transferred MPS60 Rth and no demonstrated all-orientation cooling.','LED MCPCB and offset central opening/connector remain mechanical proposals, not captured panelPCB.']}
# Through-hole tails on the opposite board face, with explicitlyunqualified3mm normaltrim/solder bound.
joints=[];joint_hits=[]
for ip in I['parts']:
 ref=ip['ref'];lc=L['positions'][ref];sg=1 if lc['side']=='F'else-1;seat=.6-sg*.8;ds=sorted([seat,seat-sg*3])
 for pp,bp in zip(ip['pads'],lc['pads']):
  if not pp['tht']:continue
  jb=[bp[0]-.4,ds[0],61-bp[3]-.4,bp[2]+.4,ds[1],61-bp[1]+.4];hits=[]
  for v in parts:
   if v['ref']==ref or v['side']==lc['side']:continue
   aa=jb[:];bb=v['nominal_box_X_D_Z_mm'][:]
   for q in(aa,bb):q[0]-=.1;q[3]+=.1;q[2]-=.1;q[5]+=.1
   if collide(aa,bb):hits.append(v['ref'])
  if hits:joint_hits.append([ref,pp['pin'],hits])
  joints.append({'ref':ref,'pin':pp['pin'],'box_X_D_Z_mm':jb,'qualified':False})
result['opposite_face_joint_body_collision_cases']=joint_hits
result['joint_normal_trim_solder_bound_mm']=3.0
result['joints']=joints
oldvent=min(room(x,vd,z,True)for x in[-15.15,-3.85]for vd in[-25.05]for z in[42,55])
result['prior_RECT01_fullface_vent_reservation_clearance_mm']=oldvent
result['prior_RECT01_vent_fit_pass_under_same_bounds']=oldvent>=0
result['conditional_geometry_pass'] &= not joint_hits
result['service_fit']={'bore_minus_bushing_min_diameter_mm':14.3-14.1,'panel_passage_minus_stem_min_diameter_mm':12.3-12.1,'ID_minus_connector_max_min_diameter_mm':10.3-9.6,'source_status':'Requiredprojectdimensions, no selectedconnector/bushing or contact qualification'}
result['assembly_sequence_scope']='UppercupwideopenbottomZ40 presentduringPCBloading; separatejoinersleeve34..42 addedafterPCB, thenlowernose andlid withendcradles. Analyticalsweepconstraints inassembly-path.json; actualwirebend/tooling/retentionforce/materialqualificationopen.'
result['residuals'].append('Pressure relief gas escape/pressure containment is not qualified by the2mm geometric vent reservation.')
write('results.json',result);write('layout-delta.json',{'base':'ca97899c8d5e8bf04947a97a43d5114d98ff4993','scope':'UNAPPLIED analytical position refinement only; electricalCAD/graph/library unchanged. C1movesinward for ventspace; T1/R1/C1 separateopposedbodyprojections; F1rotates to restoreall31fit.','changes':delta})
assert len(parts)==31 and len(rail_candidates)>=2
assert result['conditional_geometry_pass'],result
print(json.dumps({k:result[k]for k in['part_count','nominal_height_mm','worst_required_chain_height_mm','finished_max_diameter_mm','minimum_cavity_clearance_ref','minimum_allocated_cavity_clearance_mm','fullface_C1_vent2mm_reservation_residual_clearance_mm','minimum_allocated_cooler_metal_web_mm','body_collision_pairs_with_individual_XZ_tolerance','opposite_face_joint_body_collision_cases','conditional_geometry_pass']}))
