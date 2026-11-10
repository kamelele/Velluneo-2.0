"""Package Rev F single-board fabrication and SMT quote files from KiCad exports."""
from collections import Counter, defaultdict
import argparse
import csv
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import pcbnew as pcb

from revf_power import devices
import revg_power

OUT=Path('outputs')
NAMES=('Zasilacz_RevF_Moc','Zasilacz_RevF_Sterowanie',revg_power.NAME,'Zasilacz_RevG_Sterowanie')
D=OUT/'Zasilacz_RevD_JLCPCB'
GERBER_SUFFIXES={'.gtl','.gbl','.gto','.gbo','.gts','.gbs','.gtp','.gbp','.gm1'}


def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path,columns,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(columns)
        writer.writerows(rows)


def complete_power_bom(folder,footprints):
    previous={item['Ref']:item for item in read_csv(D/'BOM_pelny_RevD.csv')}
    rows=[]
    revg=folder.name==revg_power.NAME
    for part in (revg_power.devices() if revg else devices()):
        assert part.ref in footprints
        previous_item=previous.get(part.ref,{})
        code=revg_power.PART_CODES.get(part.ref) if revg else None
        source='JLCPCB, dokładny MPN' if code else previous_item.get('Źródło','')
        code=code or previous_item.get('LCSC Part #','')
        rows.append((part.ref,part.val,part.part,part.footprint,code,source))
    write_csv(folder/('BOM_RevG.csv' if revg else 'BOM_RevF.csv'),('Ref','Wartość','MPN','Footprint','LCSC Part #','Źródło'),rows)


def position_files(board,footprints,working,folder):
    placements=read_csv(working/'smd.csv')
    by_ref={x['Ref']:x for x in placements}
    assert len(placements)==len(by_ref)
    smd={ref for ref,f in footprints.items() if f.GetAttributes() & pcb.FP_SMD}
    assert smd==by_ref.keys(),smd^by_ref.keys()
    origin=board.GetDesignSettings().GetAuxOrigin()
    for ref,row in by_ref.items():
        pos=footprints[ref].GetPosition()
        assert abs(float(row['PosX'])-pcb.ToMM(pos.x-origin.x))<.00001,ref
        assert abs(float(row['PosY'])-pcb.ToMM(origin.y-pos.y))<.00001,ref
        assert row['Side']==('top' if footprints[ref].GetLayer()==pcb.F_Cu else 'bottom'),ref
    revision='G' if folder.name.startswith('Zasilacz_RevG_') else 'F'
    source_bom=read_csv(folder/f'BOM_Rev{revision}.csv')
    ref_bom={row['Ref']:row for row in source_bom}
    assert len(ref_bom)==len(source_bom) and set(ref_bom)=={r for r in footprints if not r.startswith('TP')}
    offer=defaultdict(list)
    outside=[]
    for ref,p in ref_bom.items():
        code=p['LCSC Part #']
        if ref not in smd:
            why='Montaż THT do uzgodnienia lub wiązka'
        elif not re.fullmatch(r'C\d+',code):
            why='Dokładny MPN poza zweryfikowanym katalogiem'
        elif ref=='L1':
            why='Sprawdzić zapas montażowy lub uzgodnić dostawę własną'
        else:
            assert p['MPN'],ref
            offer[(p['MPN'],p['Footprint'].split(':',1)[-1],code)].append(ref)
            continue
        outside.append((ref,p['Wartość'],p['MPN'],p['Footprint'],code,why))
    included={x for refs in offer.values() for x in refs}
    complement={x[0] for x in outside}
    assert not (included & complement) and included | complement == set(ref_bom)
    factory=folder/'JLCPCB_DO_WYCENY'
    factory.mkdir(exist_ok=True)
    write_csv(factory/'BOM_JLCPCB.csv',('Comment','Designator','Footprint','LCSC Part #'),
              ((mpn,','.join(refs),fp,code) for (mpn,fp,code),refs in offer.items()))
    write_csv(factory/'CPL_JLCPCB.csv',('Designator','Mid X','Mid Y','Layer','Rotation'),
              ((r,x['PosX'],x['PosY'],x['Side'].title(),f"{float(x['Rot'])%360:.6f}") for r,x in by_ref.items() if r in included))
    write_csv(factory/'Poza_importem.csv',('Ref','Wartość','MPN','Footprint','LCSC Part #','Powód'),outside)
    exported_bom=[r for row in read_csv(factory/'BOM_JLCPCB.csv') for r in row['Designator'].split(',')]
    exported_cpl=[row['Designator'] for row in read_csv(factory/'CPL_JLCPCB.csv')]
    assert Counter(exported_bom)==Counter(exported_cpl)==Counter(included)
    return len(placements),len(included),len(complement)


def pack_board(name,working):
    folder=OUT/name
    board=pcb.LoadBoard(str(folder/f'{name}.kicad_pcb'))
    footprints={f.GetReference():f for f in board.GetFootprints()}
    if name in (NAMES[0],revg_power.NAME):
        complete_power_bom(folder,footprints)
    mounted,included,other=position_files(board,footprints,working,folder)
    count=board.GetCopperLayerCount()
    allowed=set(GERBER_SUFFIXES)
    if count==4: allowed|={'.g1','.g2'}
    files=[path for path in sorted(working.iterdir()) if path.suffix in allowed]
    assert {f.suffix for f in files}==allowed,[f.name for f in files]
    drills=[f for f in working.glob('*.drl') if re.search(r'^X[-\d.]',f.read_text(encoding='ascii'),re.MULTILINE)]
    assert drills
    outline=next(f for f in files if f.suffix=='.gm1')
    verts={(int(x),int(y)) for x,y in re.findall(r'X(\d+)Y(\d+)D0[12]\*',outline.read_text(encoding='ascii'))}
    box=(55.5,34) if count==2 else (30,25)
    x,y=(int(v*1e6) for v in box)
    assert verts=={(0,0),(x,0),(0,y),(x,y)},(verts,box)
    package=folder/'JLCPCB_DO_WYCENY'/f'{name}_Gerber.zip'
    with ZipFile(package,'w',ZIP_DEFLATED) as out:
        for file in [*files,*drills]:
            out.write(file,file.name)
    with ZipFile(package) as out:
        assert out.testzip() is None and len(out.namelist())==len(allowed)+len(drills)
    print(f'{name}: {count} layers, {mounted} SMD, {included} in quote, {other} listed separately')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('board',choices=NAMES)
    ap.add_argument('working',type=Path)
    args=ap.parse_args()
    pack_board(args.board,args.working)
