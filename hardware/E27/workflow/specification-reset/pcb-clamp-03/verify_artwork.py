"""Exact library/schematic delta proof for the isolated optional silkscreen correction."""
from pathlib import Path
import hashlib,json,pcbnew
D=Path(__file__).resolve().parent;P=D.parent;O=P/'pcb-placement-02';name='CRCW_1206_NativeReflow';variant=name+'_ClippedSilk';B='Velluneo_specification_reset'
source=P/'libraries/Velluneo_Driver.pretty'/(name+'.kicad_mod');local=D/'libraries/Velluneo_Driver.pretty'/(variant+'.kicad_mod')
a=source.read_text(encoding='utf-8');b=local.read_text(encoding='utf-8');restored=b.replace('"'+variant+'"','"'+name+'"').replace('(fp_line (start -0.15 1.15)','(fp_line (start -1.65 1.15)');assert a==restored
oldsch=(O/(B+'.kicad_sch')).read_text(encoding='utf-8');newsch=(D/(B+'.kicad_sch')).read_text(encoding='utf-8');assert newsch.count('Velluneo_Driver:'+variant)==1;assert newsch.replace('Velluneo_Driver:'+variant,'Velluneo_Driver:'+name)==oldsch
board=pcbnew.LoadBoard(str(D/(B+'.kicad_pcb')));fps={f.GetReference():f for f in board.GetFootprints()};assert len(fps)==31 and all(f.Reference().IsVisible()for f in fps.values());assert fps['R9'].GetFPID().GetLibItemName().c_str()==variant
assert (D/(B+'.kicad_dru')).read_bytes()==(O/(B+'.kicad_dru')).read_bytes()
for p in (P/'libraries').rglob('*'):
 if p.is_file():assert (D/'libraries'/p.relative_to(P/'libraries')).read_bytes()==p.read_bytes(),p.name
print(json.dumps(dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),variant_sha256=hashlib.sha256(local.read_bytes()).hexdigest(),exact_allowed_text_delta=['footprint variant name','one optional F.SilkS bottom-line start x -1.65 to -0.15 mm'],copper_drills_mask_paste_Fab_courtyard_unchanged=True,reference_visibility_preserved=31,schematic_only_artwork_footprint_ID_change=True,all_original_library_copies_byte_identical=True,scoped_rules_byte_identical=True,scope='Artwork geometry consistency, not component/process or electrical qualification.'),indent=2))
