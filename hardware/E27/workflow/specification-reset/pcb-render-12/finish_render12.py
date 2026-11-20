from pathlib import Path
import pcbnew as p,json,hashlib,shutil
W=Path(__file__).resolve().parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'pcb-render-12';source=P/'pcb-toolkit-11/design/Velluneo_driver.kicad_pcb';scene=D/'scene/Velluneo_assembled_RENDER_ONLY.kicad_pcb';a=p.LoadBoard(str(source));b=p.LoadBoard(str(scene))
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def native(board):
 return dict(parts=sorted((f.GetReference(),f.GetValue(),f.GetFieldText('MPN'),f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees(),int(f.GetLayer()))for f in board.GetFootprints()),pads=sorted((f.GetReference(),x.GetNumber(),x.GetNetname(),x.GetPosition().x,x.GetPosition().y,x.GetSize().x,x.GetSize().y,x.GetDrillSize().x,x.GetDrillSize().y,tuple(x.GetLayerSet().Seq()))for f in board.GetFootprints()for x in f.Pads()),copper=sorted((x.GetNetname(),int(x.GetLayer()),x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y,x.GetWidth(p.F_Cu)if isinstance(x,p.PCB_VIA)else x.GetWidth(),x.GetDrillValue()if isinstance(x,p.PCB_VIA)else 0)for x in board.GetTracks()))
assert native(a)==native(b);assert len(native(a)['parts'])==33 and len(native(a)['pads'])==81 and len(native(a)['copper'])==321
for f in b.GetFootprints():
 assert len(f.Models())==1
 assert (D/'scene'/f.Models()[0].m_Filename.replace('${KIPRJMOD}/','')).is_file()
j=json.loads((D/'model-provenance.json').read_text());assert j['source_sha256']==sha(source)
(D/'geometry-check.json').write_text(json.dumps(dict(passed=True,source_sha256=sha(source),render_board_sha256=sha(scene),parts=33,pads=81,copper_objects=321,component_poses_values_MPNs_pad_geometry_layers_and_copper_unchanged=True,all33models_present=True,scope='Presentation scene only; no production PCB/source edits or manufacturing/functional approval.'),indent=2)+'\n')
(D/'README.md').write_text('''# RENDER12 — assembled appearance of the selected board

Native KiCad10.0.6 high-quality raytraced views with component bodies, leads,
metal terminations, mounting detail and wire stubs. The one selected 45 x 60 mm
four-layer board retains exact source geometry/placement:33parts81pads304tracks
and17vias. Original TOOLKIT11 production sources are unchanged, proven by native
comparison and source hash. No circuit, placement, routing or acceptance change.

Velluneo_assembled_top_4K.png and bottom view show the actual board with generic
package bodies. Open scene/Velluneo_assembled_RENDER_ONLY.kicad_pcb to inspect.
This separate scene must not replace production CAD or manufacturing files.
Eight package assets come from the official archived KiCad 3D library, exact
tree b8b3cfdfad88ba66f21002b3de51dc6f7d55ba5a; URLs/hashes in model-provenance.json.
Their authorship/license headers and LICENSE.md remain with the models. Library
assets retain CC-BY-SA4.0 and the upstream electronic-design exception.

Custom transformer, formed-lead parts, ceramic bodies and wires use original
parametric appearance models. The transformer and formed constructions are
illustrative, not exact supplier-qualified mechanical models or a manufactured
sample. Appearance does not establish clearance in finished construction,
assembly/insulation qualification or operating safety. Existing technical/process
and release holds remain unchanged. No human stage is advanced by this render.

The native3Dscene is used rather than an AI-generated product photograph. Original
parametric visualization helpers are supplied; saved output is bound by hashes.
''',encoding='utf-8')
for n in('build_render12.py','render_assembled12.py','finish_render12.py'):shutil.copyfile(W/n,D/n)
rows=[dict(path=x.relative_to(D).as_posix(),sha256=sha(x),bytes=x.stat().st_size)for x in sorted(D.rglob('*'))if x.is_file()and x.suffix!='.kicad_prl'and x.name not in('frozen-files.json','review-record.json')and'reviews'not in x.parts]
body=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest();(D/'frozen-files.json').write_text(json.dumps(dict(body_sha256=body,files=rows,scope='Presentation-only scene/assets/outputs; reviews and local GUIstate excluded.'),indent=2)+'\n');print('Presentation scene verified and frozen',body,len(rows))
