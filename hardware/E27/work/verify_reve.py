"""Read back the Rev E placement boards and check their geometry and links."""
from itertools import combinations
import re

import pcbnew as pcb

from studium_e import BASE, DEST, EDGE, BARRIER, secondary, outline, box_mm

SIZES = {'E_Jedna': (74, 32), 'E_Moc': (57, 32), 'E_Sterowanie': (30, 26)}


def footprints(b):
    return {f.GetReference():f for f in b.GetFootprints()}


def pins(fp):
    return {(p.GetNumber(),p.GetNetname()) for p in fp.Pads()}


def verify(name, originals):
    path = DEST / f'{name}.kicad_pcb'
    b = pcb.LoadBoard(str(path))
    fps = footprints(b)
    refs = set(originals)
    if name == 'E_Moc':
        refs = {ref for ref in refs if not secondary(ref)} | {'J101'}
    elif name == 'E_Sterowanie':
        refs = {ref for ref in refs if secondary(ref)} | {'J102'}
    assert fps.keys() == refs
    w,h = SIZES[name]
    outline_items = [s for s in b.GetDrawings() if s.GetLayer() == pcb.Edge_Cuts]
    points = {tuple(p) for s in outline_items for p in (s.GetStart(),s.GetEnd())}
    assert len(outline_items) == 4
    assert points == {(pcb.FromMM(x),pcb.FromMM(y)) for x in (75,75+w) for y in (70,70+h)}
    assert len(list(b.GetTracks())) == 0 and len(list(b.Zones())) == 0
    assert b.GetCopperLayerCount() == 2 and pcb.ToMM(b.GetDesignSettings().GetBoardThickness()) == 1.6
    profiles = [[],[]]
    primary_x,secondary_x = [],[]
    origin = pcb.VECTOR2I(pcb.FromMM(75),pcb.FromMM(70))
    for ref,fp in fps.items():
        if ref in originals:
            assert pins(fp) == pins(originals[ref]),ref
            assert fp.GetValue() == originals[ref].GetValue(),ref
            assert fp.GetLayer() == originals[ref].GetLayer(),ref
        else:
            assert str(fp.GetFPID().GetLibItemName()) == 'Harness_26V_RTN'
            assert pins(fp) == {('1','/S_RAW'),('2','/S_RTN')}
        side = 0 if fp.GetLayer() == pcb.F_Cu else 1
        profiles[side].append((ref,box_mm(outline(fp),origin)))
        for pad in fp.Pads():
            a = box_mm(pad.GetBoundingBox(),origin)
            if pad.GetDrillSize().x:
                profiles[1-side].append((ref,a))
            net = pad.GetNetname()
            if net.startswith('/P_'):
                primary_x.append(a[2])
            elif net and not net.startswith('unconnected-'):
                secondary_x.append(a[0])
    for side in profiles:
        for ref,(x1,y1,x2,y2) in side:
            assert min(x1,y1,w-x2,h-y2) >= EDGE-.001,ref
        for (ref,a),(other,c) in combinations(side,2):
            if ref != other:
                assert a[0]>=c[2] or c[0]>=a[2] or a[1]>=c[3] or c[1]>=a[3],(ref,other)
    if name == 'E_Sterowanie':
        assert not primary_x
        band = None
    else:
        band = min(secondary_x)-max(primary_x)
        assert band >= BARRIER-.001
        for ref in ('T1','D7','C6','R9'):
            assert ref in fps
    return len(fps),band,{n for fp in fps.values() for _,n in pins(fp) if n and not n.startswith('unconnected-')}


def main():
    src = footprints(pcb.LoadBoard(str(BASE)))
    results = {name:verify(name,src) for name in SIZES}
    assert results['E_Moc'][2] & results['E_Sterowanie'][2] == {'/S_RAW','/S_RTN'}
    lines = ['# Kontrola rozmieszczenia Rev E','']
    for name,(n,band,_) in results.items():
        w,h = SIZES[name]
        spacing = f' Pas między padami stron P/S w osi X wynosi {band:.2f} mm.' if band is not None else ' Wyłącznie sieci wtórne.'
        report = DEST / f'{name}_DRC.rpt'
        check = ''
        if report.exists():
            data = report.read_text(encoding='utf8')
            violations = re.search(r'Found (\d+) DRC violations',data)
            unconnected = re.search(r'Found (\d+) unconnected pads',data)
            assert violations and unconnected
            check = f' KiCad zgłasza {violations[1]} naruszeń reguł oraz {unconnected[1]} niepołączonych padów.'
        lines.append(f'- {name}, {w} × {h} mm i {n} obrysów obudów.{spacing}{check}')
    lines.extend(['','Porównano wszystkie oryginalne przypisania pinów, położenia obrysów na obu stronach i kolizje z padami otworów po stronie przeciwnej. Dwa nowe punkty wiązki mają identyczną polaryzację. Zapisane płytki nie zawierają ścieżek ani wypełnień. Wymagane są ponowne trasowanie, kontrola pętli mocy, pełny DRC oraz projekt pól cieplnych.'])
    (DEST/'Kontrola_RevE.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print({k:v[:2] for k,v in results.items()})


if __name__ == '__main__':
    main()
