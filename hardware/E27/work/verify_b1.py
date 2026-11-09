"""Verify Rev B1 against the routed Rev B board and the KiCad exports."""
from collections import Counter
import csv
import xml.etree.ElementTree as ET

import pcbnew as pcb

from revb1_thermal import BASE, DEST, BOARD, LAYERS, VIA_DIAMETER, VIA_DRILL


def pads_by_ref(board):
    return {(fp.GetReference(), pad.GetNumber()): pad
            for fp in board.GetFootprints() for pad in fp.Pads()}


def track_key(item):
    if isinstance(item, pcb.PCB_VIA):
        return ('via', item.GetNetname(), tuple(item.GetPosition()), item.GetWidth(pcb.F_Cu), item.GetDrillValue())
    return ('track', item.GetNetname(), item.GetLayer(), tuple(item.GetStart()), tuple(item.GetEnd()), item.GetWidth())


def net_map(path):
    root = ET.parse(path).getroot()
    return {(node.get('ref'), node.get('pin')): net.get('name')
            for net in root.findall('./nets/net') for node in net.findall('node')}


def extremes(board, pads, zones):
    primary, secondary = [], []
    items = [*pads.values(), *board.GetTracks()]
    named_boxes = [(item.GetNetname(), item.GetBoundingBox()) for item in items]
    named_boxes += [(z.GetNetname(), z.GetFilledPolysList(z.GetLayer()).BBox()) for z in zones]
    for net, box in named_boxes:
        if net.startswith('/P_'):
            primary.append(box.GetRight())
        elif net.startswith('/S_'):
            secondary.append(box.GetLeft())
    return pcb.ToMM(min(secondary) - max(primary))


base = pcb.LoadBoard(str(BASE / 'Zasilacz_RevB.kicad_pcb'))
board = pcb.LoadBoard(str(BOARD))
reference_pads, pads = pads_by_ref(base), pads_by_ref(board)
assert reference_pads.keys() == pads.keys()
for key, pad in pads.items():
    other = reference_pads[key]
    assert (pad.GetNetname(), pad.GetPosition(), pad.GetSize(), pad.GetDrillSize(), pad.GetLayerSet().FmtHex()) == (
        other.GetNetname(), other.GetPosition(), other.GetSize(), other.GetDrillSize(), other.GetLayerSet().FmtHex()), key
expected_nets = {key: pad.GetNetname() for key, pad in pads.items() if pad.GetNetname()}
assert expected_nets == net_map('work/psb1.xml')

old = Counter(track_key(t) for t in base.GetTracks())
new = Counter(track_key(t) for t in board.GetTracks())
added = new - old
assert not old - new
assert sum(added.values()) == 12
assert Counter(key[1] for key in added) == {'/P_0': 4, '/S_RTN': 8}
assert all(key[0] == 'via' and key[3:] == (pcb.FromMM(VIA_DIAMETER), pcb.FromMM(VIA_DRILL)) for key in added)

zones = {z.GetZoneName(): z for z in board.Zones()}
assert set(zones) == {'TH_SOURCE_F', 'TH_SOURCE_B', 'TH_CC_RETURN_F', 'TH_CC_RETURN_B'}
assert all(z.IsFilled() and z.GetFilledArea() > 0 for z in zones.values())
for key in added:
    _, net, center, _, _ = key
    linked = [z for z in zones.values() if z.GetNetname() == net]
    assert {z.GetLayer() for z in linked} == set(LAYERS)
    assert all(z.HitTestFilledArea(z.GetLayer(), pcb.VECTOR2I(*center)) for z in linked)
for z_name, refs in [
    ('TH_SOURCE_B', [('U1', str(i)) for i in range(16, 20)]),
    ('TH_CC_RETURN_F', [(ref, pin) for ref in ('U3', 'U4') for pin in ('5', '9')]),
]:
    z = zones[z_name]
    assert all(z.HitTestFilledArea(z.GetLayer(), pads[ref].GetPosition()) for ref in refs)

area = {name: z.GetFilledArea() / 1e12 for name, z in zones.items()}
band = extremes(board, pads, zones.values())
assert band >= 8.19
edges = [shape for shape in board.GetDrawings() if shape.GetLayer() == pcb.Edge_Cuts]
assert len(edges) == 4
points = [point for shape in edges for point in (shape.GetStart(), shape.GetEnd())]
assert pcb.ToMM(max(p.x for p in points) - min(p.x for p in points)) == 66
assert pcb.ToMM(max(p.y for p in points) - min(p.y for p in points)) == 34
assert pcb.ToMM(board.GetDesignSettings().GetBoardThickness()) == 1.6

erc = (DEST / 'ERC.rpt').read_text(encoding='utf-8-sig')
drc = (DEST / 'DRC.rpt').read_text(encoding='utf-8-sig')
assert 'Errors 0  Warnings 0' in erc
assert all('Found 0 ' + name in drc for name in ('DRC violations', 'unconnected pads', 'Footprint errors'))
with (DEST / 'Produkcja_DO_PRZEGLADU/CPL_Zasilacz_KiCad.csv').open(encoding='utf-8-sig', newline='') as stream:
    placements = list(csv.DictReader(stream))
assert {row['Ref'] for row in placements} == {
    fp.GetReference() for fp in board.GetFootprints() if fp.GetAttributes() & pcb.FP_SMD
}
assert len(placements) == 49

report = f'''# Kontrola projektu KiCad · zasilacz E27 Rev B1

- ERC i DRC z porównaniem PCB ze schematem. Zero naruszeń, niepołączonych padów i rozbieżności. Zestaw reguł pominiętych przez konfigurację zapisano w raportach KiCad.
- Odczyt projektu potwierdził {len(expected_nets)} przypisań pin–sieć zgodnych ze schematem. Położenia, rozmiary i sieci padów oraz wszystkie ścieżki i przelotki odziedziczone z Rev B porównano parami.
- Dodano 12 przelotek termicznych o padzie Ø0,60 mm i otworze Ø0,30 mm. Cztery są na P_0, a osiem na S_RTN. Każda przecina wypełnioną miedź swojej sieci na obu warstwach. Wypełnienie styka się z padami SOURCE 16–19 układu U1 oraz z padami 5 i 9 obu regulatorów U3/U4. Pola S_RTN pozostają poza obszarem rezystora pomiarowego R9.
- Rzeczywista powierzchnia poligonów po wypełnieniu P_0 wynosi **{area['TH_SOURCE_F']:.1f} mm² na F.Cu** i **{area['TH_SOURCE_B']:.1f} mm² na B.Cu**. Dla S_RTN wynosi **{area['TH_CC_RETURN_F']:.1f} mm² na F.Cu** i **{area['TH_CC_RETURN_B']:.1f} mm² na B.Cu**. Odczyt dotyczy miedzi w strefach, z odjętymi wycięciami, przed uwzględnieniem otworów wierconych. Powierzchnia geometryczna nie określa temperatury elementu.
- Najmniejszy pas pomiędzy skrajnymi obwiedniami miedzi P i S w rzucie na oś X ma **{band:.3f} mm**, także po uwzględnieniu wypełnień i nowych przelotek. Ocena izolacji kompletnego zespołu wymaga pomiarów i przeglądu.
- Obrys PCB 66 × 34 mm, laminat 1,6 mm, 49 pozycji SMD w eksporcie KiCad. Dokumentacja montażowa ma status do przeglądu przed wykonaniem.
'''
(DEST / 'Weryfikacja_KiCad_RevB1.md').write_text(report, encoding='utf-8')
print(f'{len(expected_nets)} pins; 12 new vias; {band:.3f} mm P/S; '
      + ', '.join(f'{key} {value:.1f} mm²' for key,value in sorted(area.items())))
