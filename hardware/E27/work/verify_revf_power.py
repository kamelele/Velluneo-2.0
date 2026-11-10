"""Verify the split power board against its schematic and Rev D primary geometry."""
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
import sys

import pcbnew as p

from revf_power import D,DEST,NAME,SIZE

def pads(b):
    return {(f.GetReference(),d.GetNumber()):d for f in b.GetFootprints() for d in f.Pads()}

def primary_tracks(b):
    out=[]
    for t in b.GetTracks():
        net=t.GetNetname()
        if not net.startswith('/P_'): continue
        if isinstance(t,p.PCB_VIA):
            out.append((net,'via',tuple(t.GetPosition()),t.GetWidth(p.F_Cu),t.GetDrillValue()))
        else:
            out.append((net,t.GetLayer(),tuple(t.GetStart()),tuple(t.GetEnd()),t.GetWidth()))
    return Counter(out)

def main():
    original=p.LoadBoard(str(D/f'{D.name}.kicad_pcb'))
    board=p.LoadBoard(str(DEST/f'{NAME}.kicad_pcb'))
    old=pads(original)
    now=pads(board)
    assert primary_tracks(original)==primary_tracks(board)
    for key,x in now.items():
        if key[0]=='J101': continue
        y=old[key]
        assert x.GetNetname()==y.GetNetname() and x.GetPosition()==y.GetPosition() and x.GetSize()==y.GetSize() and x.GetDrillSize()==y.GetDrillSize(),key
    tree=ET.parse(sys.argv[1])
    xml={(node.get('ref'),node.get('pin')):net.get('name')
         for net in tree.findall('./nets/net') for node in net.findall('node')}
    assert xml=={key:x.GetNetname() for key,x in now.items() if x.GetNetname()}
    assert xml['J101','1']=='/S_RAW' and xml['J101','2']=='/S_RTN'
    erc=(DEST/'ERC.rpt').read_text(encoding='utf8')
    drc=(DEST/'DRC.rpt').read_text(encoding='utf8')
    assert 'Errors 0  Warnings 0' in erc
    assert all(s in drc for s in ('Found 0 DRC violations','Found 0 unconnected pads','Found 0 Footprint errors'))
    assert board.GetCopperLayerCount()==2
    e=[g for g in board.GetDrawings() if g.GetLayer()==p.Edge_Cuts]
    assert len(e)==4 and {tuple(q) for g in e for q in (g.GetStart(),g.GetEnd())} == {
        (p.FromMM(x),p.FromMM(y)) for x in (75,75+SIZE[0]) for y in (70,70+SIZE[1])}
    zones=list(board.Zones())
    assert len(zones)==2 and all(z.GetNetname()=='/P_0' and z.IsFilled() for z in zones)
    bounds=[(x.GetNetname(),x.GetBoundingBox()) for x in [*now.values(),*board.GetTracks()]]
    bounds.extend((z.GetNetname(),z.GetFilledPolysList(z.GetLayer()).BBox()) for z in zones)
    gap=p.ToMM(min(b.GetLeft() for n,b in bounds if n.startswith('/S_'))-max(b.GetRight() for n,b in bounds if n.startswith('/P_')))
    assert gap>=8.19,gap
    area={board.GetLayerName(z.GetLayer()):z.GetFilledArea()/1e12 for z in zones}
    assert len(area)==2
    count=sum(primary_tracks(board).values())
    (DEST/'Weryfikacja_RevF.md').write_text(f"""# Kontrola płytki mocy Rev F

- ERC, DRC i porównanie ze schematem przeszły bez naruszeń. Odczyt porównał {len(xml)} przypisań pin–sieć ze schematem.
- Zachowano wszystkie {count} segmenty i przelotki sieci pierwotnych Rev D oraz pozycje, wielkości i sieci odziedziczonych padów. Nowe wyprowadzenie J101 ma S_RAW na 1 i S_RTN na 2.
- Laminat 55,5 × 34 mm, dwie warstwy. Najwęższy pas w osi X między skrajną miedzią pierwotną i wtórną, razem z wypełnieniami, wynosi {gap:.3f} mm. Wypełnienia P_0 odprowadzające ciepło mają {area['F.Cu']:.1f} mm² na F.Cu i {area['B.Cu']:.1f} mm² na B.Cu.
- Wartości wynikają z geometrii PCB. Izolacja transformatora i gotowego zespołu oraz temperatura wymagają pomiarów.
""",encoding='utf8')
    print(f'{len(xml)} pin–net pairs; {count} unchanged primary routing items; {gap:.3f} mm isolation band')

if __name__=='__main__':
    main()
