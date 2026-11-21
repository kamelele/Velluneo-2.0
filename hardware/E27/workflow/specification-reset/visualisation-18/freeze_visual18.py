from pathlib import Path
import json,hashlib,shutil
W=Path(__file__).parent;R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'visualisation-18'
src=P/'catalogue-pcb-16/design/Velluneo_driver.kicad_pcb';assert hashlib.sha256(src.read_bytes()).hexdigest()=='3c13b9d2048a6d6b1c830c75445d27412516f0c0fb03d6c5285b8c2f69067f78'
for name in ['Velluneo_C16_top_4K.png','Velluneo_C16_bottom_4K.png','Velluneo_C16_3D_both_sides.png','Velluneo_C16_outer_connections.png','Velluneo_C16_inner_connections.png']:assert (D/name).is_file()and(D/name).stat().st_size>10000
(D/'visual-check.json').write_text(json.dumps(dict(source_geometry_verified=True,source_board_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),native_comparison='33componentposes/MPNs/values80padgeometry/netmembership333track/viaobjects identical',component_appearance_models=31,manufacturing_sources_or_exports_modified=False,visual_inspection='Coordinator inspected final both-face render composite and both layer sheets; full boards visible, labels/31componentmodels represented, actualtracks and physicalbottommirror retained.',limitations='Generic/envelope appearance, not exact manufacturer3D/firstfit; currentretainedprocess/physical/humanholds unaffected.'),indent=2)+'\n')
shutil.copyfile(W/'freeze_visual18.py',D/'freeze_visual18.py')
idx=R/'hardware/E27/workflow/project-index.md';s=idx.read_text();heading='''## Current native 3D and connection views - VIS18, 21 November 2026

[VIS18](specification-reset/visualisation-18/README.md) presents currentC16/C17
45x60mm4layerdriver: bothface4Kclass nativeKiCad raytraces with31electronicappearance
models, plus currentouter/innercopperdiagrams. Native comparison retains33positions,
80pads333copperobjects and exactsourcehash. Currentfactory74032 andstraightTO3PF
envelopes replace historicalcustom/formedpartappearances. J1/J2remainwirepadswithout
inventedharness. Generic/envelopemodels are visualization, not supplierSTEP/firstfit.
ProductionCAD, C17manufacturingfiles, rules and allphysical/process/humanholds unchanged.

'''
if '## Current native 3D and connection views - VIS18,'not in s:idx.write_text(s.replace('# E27 workflow index\n\n','# E27 workflow index\n\n'+heading,1),encoding='utf-8')
records=[dict(path=p.relative_to(D).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)for p in sorted(D.rglob('*'))if p.is_file()and not any(q in p.relative_to(D).parts for q in ('.work','reviews','__pycache__'))and p.suffix!='.kicad_prl'and p.name not in ('frozen-files.json','review-record.json','integration-record.md')]
body=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();(D/'frozen-files.json').write_text(json.dumps(dict(base_commit='cafb6ec53fd55275bfe92ef97a77166a58a93ed3',body_sha256=body,files=records,scope='Presentation data only. Reviews/lifecycle excluded; C16/C17 manufacturing sources unchanged.'),indent=2)+'\n');print(body,len(records))
