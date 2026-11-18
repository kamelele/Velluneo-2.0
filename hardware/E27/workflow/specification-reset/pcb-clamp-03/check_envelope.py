"""Nominal radial allocation screen, explicitly not finished lamp or assembly fit."""
from pathlib import Path
import json,math,contextlib,io,importlib.util,hashlib
D=Path(__file__).resolve().parent;P=D.parent
spec=importlib.util.spec_from_file_location('geom',D/'verify_geometry.py');g=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(g)
heights={p['ref']:p for p in json.loads((P/'assembly-fit-01/height-contract.json').read_text(encoding='utf-8'))['parts']};bodies={p['ref']:p for p in json.loads((P/'assembly-fit-01/native-body-bounds.json').read_text(encoding='utf-8'))['parts']}
rows=[]
for ref,c in g.pos.items():
 bb=bodies[ref]['native_fab_stroke_bbox_mm'];h=heights[ref]['installed_envelope_mm']
 if ref=='T1':bb=[-15,-15,15,15];h=18
 globalbox=g.box(bb,c);zmax=.8+h;rad=math.hypot(max(abs(globalbox[0]),abs(globalbox[2])),zmax);rows.append(dict(ref=ref,x_range_mm=[globalbox[0],globalbox[2]],allocated_height_mm=h,outer_z_magnitude_mm=zmax,radial_corner_mm=rad,qualified=False))
boardradius=math.hypot(g.HALF_W,.8);maximum=max([(r['radial_corner_mm'],r['ref'])for r in rows]+[(boardradius,'PCB edge')]);assert maximum[0]<30
print(json.dumps(dict(trial_board_mm=[2*g.HALF_W,2*g.HALF_H],nominal_board_centerline_radial_diameter_mm=2*maximum[0],limiting_object=maximum[1],outer_lamp_target_diameter_mm=60,unallocated_radial_difference_to_outer_target_mm=30-maximum[0],body_allocations=rows,board_only_radius_mm=boardradius,finished_housing_assembly_fit_proven=False,scope='Nominal installed-allocation x/z projection about a centred board, not qualified seating/tolerance/termination/lead/bobbin/core/mount/wall/vent/wire fit. Outer60mm is not an available internal diameter. Longitudinal120mm, service access and thermal behavior are not requalified. Whole assembly fit must be repeated.'),indent=2))
