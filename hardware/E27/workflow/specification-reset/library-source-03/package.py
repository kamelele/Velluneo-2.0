#!/usr/bin/env python3
"""Package saved draft source and render actual native exports; no PCB claim."""
from pathlib import Path
import json,hashlib,zipfile,fitz
D=Path(__file__).resolve().parent;P=D.parent
pdf=fitz.open(D/'Velluneo_driver_LIB03.pdf');assert len(pdf)==1
pdf[0].get_pixmap(matrix=fitz.Matrix(1.7,1.7),alpha=False).save(D/'Velluneo_driver_LIB03.png')
svg=next((D/'footprint-svg').glob('*.svg'));view=fitz.open(svg)
view[0].get_pixmap(matrix=fitz.Matrix(20,20),alpha=False).save(D/'KEMET_native_footprint.png')
g=json.loads((P/'schematic-intent/intended-connectivity.json').read_text())
files=[P/f for f in ['Velluneo_specification_reset.kicad_pro','Velluneo_specification_reset.kicad_sch','sym-lib-table','fp-lib-table','libraries/Velluneo_Driver.kicad_sym','schematic-intent/intended-connectivity.json','footprint-study/assignments.json','eco01-capture/owner-intent-approval.md']]
files+=list((P/'libraries/Velluneo_Driver.pretty').glob('*.kicad_mod'))
files += [P/b['path'] for b in g['basis_sources']]
files += [D/f for f in ['README.md','BOM.csv','source-basis.md','source-register.json','geometry-contract.json','Velluneo_driver_LIB03.pdf']]
members=[];dest=D/'Velluneo_driver_LIB03_KiCad.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(set(files)):
  b=p.read_bytes();n=p.relative_to(P).as_posix();info=zipfile.ZipInfo(n,(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
  members.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
with zipfile.ZipFile(dest) as z:
 for m in members:assert hashlib.sha256(z.read(m['path'])).hexdigest()==m['sha256']
report={'passed':True,'scope':'Every archive member byte matches saved source; standalone draft KiCad/evidence subset, not installed-toolkit repository or manufacturing release','members':members,'zip_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
(D/'package-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Packaged',len(members),'verified members and rendered actual native exports')
