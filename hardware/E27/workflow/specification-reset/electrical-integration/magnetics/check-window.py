import cadquery as cq,json,hashlib,pathlib,argparse
P=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description='Source-pinned nominal bobbin/core winding-envelope collision diagnostic; no physical/insulation approval.')
parser.add_argument('--bobbin-step',required=True,type=pathlib.Path)
parser.add_argument('--core-step',required=True,type=pathlib.Path)
parser.add_argument('--output',type=pathlib.Path,default=P/'window-results.json')
args=parser.parse_args()
bobpath=args.bobbin_step
corepath=args.core_step
for path,expected in [(bobpath,'f6acdbbccb291fd39ac8028c163d7bdb47fa6849c8c7d94dce01076f05dfb2f0'),(corepath,'062a59009fed08ba69f30db6acdb0448a2e1f085f2e5882620ddc56f0536783f')]:
 actual=hashlib.sha256(path.read_bytes()).hexdigest()
 if actual!=expected:
  raise ValueError(f'Native source SHA256 mismatch: {path}; expected {expected}, got {actual}')
bob=cq.importers.importStep(str(bobpath)).val()
raw=cq.importers.importStep(str(corepath)).val()
# Source core: Xwidth25,Ydepth0..12.5,Zsection-9.1..0.
# Bobbin: winding axisZ, barrelX+-6.55,Y+-3.45, boreY+-2.75.
# Core centerpostZ[-5.8,-.6] is centered at-3.2; transform accordingly.
cp=raw.rotate((0,0,0),(1,0,0),-90).translate((0,3.2,12.5))
cn=cp.rotate((0,0,0),(0,1,0),180)
core=cq.Compound.makeCompound([cp,cn])
nominal_core_bobbin_collision=core.intersect(bob).Volume()
def rounded(w,h,r,length):
 return cq.Workplane('XY').sketch().rect(w,h).vertices().fillet(r).finalize().extrude(length/2,both=True).val()
# Native barrel continuous outline: flatsX+-6.55, Y+-3.45, cornerR2.
inner=rounded(13.1,6.9,2.,10.5)
rows=[]
for wire,build in [(.3,2.293),(.4,2.503)]:
 outer=rounded(13.1+2*build,6.9+2*build,2+build,10.5)
 env=outer.cut(inner)
 b=env.BoundingBox()
 rows.append(dict(TEX_E_mm=wire,radial_build_mm=build,envelope_bbox=[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax],nominal_bobbin_intersection_mm3=env.intersect(bob).Volume(),nominal_core_intersection_mm3=env.intersect(core).Volume(),nominal_side_core_gap_mm=9.35-(6.55+build),PDF_side_dimension_only_gap_mm=(18.7-.6-13.1)/2-build,axial_straight_barrel_margin_per_side_mm=(16.2-10.5)/2))
# Models generated here are analysis solids, not assembly/CAD projectdeliverables.
result=dict(nominal_core_bobbin_intersection_mm3=nominal_core_bobbin_collision,sources=dict(bobbin_step_sha256=hashlib.sha256(bobpath.read_bytes()).hexdigest(),core_step_sha256=hashlib.sha256(corepath.read_bytes()).hexdigest()),native_nominal_geometry=dict(bobbin_flange_inner_faces_Z_mm=[-8.3,8.3],barrel_straight_extent_Z_mm=[-8.1,8.1],barrel_envelope_XY_mm=[13.1,6.9],barrel_corner_radius_mm=2.,core_inner_side_planes_X_mm=[-9.35,9.35],core_half_transform='rotateX -90deg; translate(0,3.2,12.5); secondhalfrotateY180deg'),candidates=rows,limitations=['Collision-free nominal STEP is not tolerance/insulation clearance acceptance.','Source nominal two ungapped halves are conservativelyused for window collision; actualgappedcore center-post removal does not narrow externalwindow.','PDF-side dimension-only screen uses coreinnerwidth18.7+/-0.6 and bobbinbarrelwidth13.1-0.2; it omits lateraloffset, assemblytolerance, windingdistortion, seamsoutsidebudget, leadouts, yokes andqualification.'])
args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
