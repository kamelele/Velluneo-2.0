from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

out = Path('outputs')
root_files = [
    'Raport_E27_RevB.md', 'BOM_Zasilacz_RevB.csv', 'Plan_prob_RevB.md', 'Weryfikacja_KiCad_RevB.md',
    'Raport_E27_RevA.md', 'BOM_E27_RevA.csv', 'Mechanizm_E27_RevA.svg',
]
files = [out / f for f in root_files]
for folder in ['Zasilacz_RevB', 'Wklad_LED']:
    files.extend(f for f in sorted((out / folder).rglob('*')) if f.is_file() and f.suffix != '.kicad_prl')
assert all(f.is_file() and f.stat().st_size > 0 for f in files)
with ZipFile(out / 'E27_RevB_pakiet_KiCad.zip', 'w', ZIP_DEFLATED) as z:
    for f in files:
        z.write(f, f.relative_to(out).as_posix())
with ZipFile(out / 'E27_RevB_pakiet_KiCad.zip') as z:
    assert len(z.namelist()) == len(set(z.namelist())) == len(files)
    assert z.testzip() is None
print(len(files), 'verified archive entries')
