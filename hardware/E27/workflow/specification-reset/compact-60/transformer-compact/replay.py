"""Replay retained actual bobbin geometry; no new STEP import or finished-build claim."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
INPUTS = [
    'transformer-footprint/source-step-faces.json',
    'transformer-footprint/source-step-findings.json',
    'design-closure-02/transformer/construction-contract.json',
    'design-closure-02/transformer/results.json',
]
hashes = {s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in INPUTS}
assert hashes[INPUTS[0]] == 'fb4872226bbccab48e8622123bcab8856e4d342a4b3c8fec575714f74500fef4'
faces = json.loads((ROOT / INPUTS[0]).read_text())
assert len(faces) == 430
box = [min(f['box'][i] for f in faces) if i % 2 == 0 else max(f['box'][i] for f in faces) for i in range(6)]
feet = [f for f in faces if f['i'] in [170, 191, 306, 369]]
assert len(feet) == 4
assert all(abs(f['centre'][1] - 6.75) < 1e-6 and f['normal'][1] > .99 for f in feet)
pins = [f for f in faces if f['type'] == 'PLANE' and abs(f['centre'][1] - 10.25) < 1e-6 and abs(f['area'] - .36) < 1e-6]
assert len(pins) == 10
plane = 6.75
q = json.loads((ROOT / INPUTS[2]).read_text())
g = q['geometry_mm']
assert q['turns'] == {'P': 120, 'A': 22, 'S': 30}
raw_top = plane - box[2]
shell_top = plane + g['outer_regular_shell_XY'][1] / 2
result = {
    'kind': 'Retained-source geometry replay and conditional construction envelope; not finished-source CAD or measured build',
    'input_sha256': hashes,
    'fresh_STEP_import': False,
    'face_count': len(faces),
    'raw_STEP_bbox_Xmin_Xmax_Ymin_Ymax_Zmin_Zmax_mm': box,
    'mount_plane_STEP_Y_mm': plane,
    'support_face_ids': [f['i'] for f in feet],
    'pin_tip_STEP_Y_mm': 10.25,
    'nominal_pin_projection_from_mount_plane_mm': 10.25 - plane,
    'raw_bobbin_above_PCB_nominal_mm': raw_top,
    'raw_bobbin_plan_tolerance_max_mm': [25.2, 26.0],
    'C2_regular_coil_shell_plan_width_and_axial_band_mm': [g['outer_regular_shell_XY'][0], g['selected_active_band']],
    'C2_regular_coil_shell_top_above_PCB_mm': shell_top,
    'C2_regular_coil_top_below_nominal_bobbin_top_mm': raw_top - shell_top,
    'pin_projection_source_tolerance_mm': [3.3, 3.7],
    'PCB_thickness_design_requirement_mm': [1.5, 1.7],
    'flush_pin_protrusion_below_PCB_mm': [3.3 - 1.7, 3.7 - 1.5],
    'with_2mm_standoff_protrusion_below_PCB_mm': [3.3 - 1.7 - 2, 3.7 - 1.5 - 2],
    'hypothetical_0p8mm_min_protrusion_max_standoff_mm': 3.3 - 1.7 - .8,
    'protrusion_0p8_scope': 'Arithmetic sensitivity only; actual joint acceptance/process must set required protrusion.',
    'raw_bobbin_plan_margin_inside_28square_each_side_mm': [(28 - 25.2) / 2, (28 - 26) / 2],
    'limits': [
        'Raw bobbin is not finished transformer. Core, two yokes, terminal wraps, tubes and wire exits require separate maximum bounds.',
        '25.7x26.5 courtyard is a raw-bobbin pad/body allocation; cannot be promoted to finished transformer envelope.',
        'C2 end-pocket axial arithmetic does not establish actual bend radius, local clearance or builder capability.',
        'No normal/fault thermal, EIS adoption, core/yoke-to-TIW leadout isolation or supplier approval is established here.',
        'No circuit, pin map, KiCad or approved construction altered.'
    ]
}
assert result['C2_regular_coil_top_below_nominal_bobbin_top_mm'] > 0
assert result['with_2mm_standoff_protrusion_below_PCB_mm'][0] < 0
(HERE / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: 430 retained faces, 4 mount feet, 10 pin tips; mount plane6.75, raw height12.9; 2mm spacer fails pin reach worst case.')
