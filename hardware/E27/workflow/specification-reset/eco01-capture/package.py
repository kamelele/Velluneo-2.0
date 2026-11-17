#!/usr/bin/env python3
"""Package saved native CAD and exact independent basis. No stage/release claim."""
from pathlib import Path
import json,hashlib,zipfile,fitz
P=Path(__file__).resolve().parent.parent;D=P/'eco01-capture'
pdf=fitz.open(D/'Velluneo_driver_ECO01.pdf');assert len(pdf)==1
pdf[0].get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False).save(D/'Velluneo_driver_ECO01.png')
pdf[0].get_pixmap(matrix=fitz.Matrix(2.6,2.6),clip=fitz.Rect(20,65,560,335),alpha=False).save(D/'input-discharge-detail.png')
g=json.loads((P/'schematic-intent/intended-connectivity.json').read_text())
files=[P/f for f in ['Velluneo_specification_reset.kicad_pro','Velluneo_specification_reset.kicad_sch','sym-lib-table','fp-lib-table','libraries/Velluneo_Driver.kicad_sym','schematic-intent/intended-connectivity.json','footprint-study/assignments.json','eco01-capture/README.md','eco01-capture/BOM.csv','eco01-capture/owner-intent-approval.md','eco01-capture/Velluneo_driver_ECO01.pdf']]
files+=list((P/'libraries/Velluneo_Driver.pretty').glob('*.kicad_mod'))
files += [P/b['path'] for b in g['basis_sources']]
manifest=[]
with zipfile.ZipFile(D/'Velluneo_driver_ECO01_KiCad.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(set(files)):
  b=f.read_bytes();path=f.relative_to(P).as_posix();info=zipfile.ZipInfo(path,date_time=(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  z.writestr(info,b);manifest.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
with zipfile.ZipFile(D/'Velluneo_driver_ECO01_KiCad.zip') as z:
 assert len(z.namelist())==len(manifest)
 for f in manifest:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256']
(D/'package-check.json').write_text(json.dumps({'status':'all archive member bytes hash-match saved current source','members':manifest,'zip_sha256':hashlib.sha256((D/'Velluneo_driver_ECO01_KiCad.zip').read_bytes()).hexdigest(),'not_toolkit_checkout_or_manufacturing_release':True},indent=2)+'\n')
print('ZIP verified',len(manifest),'members')
