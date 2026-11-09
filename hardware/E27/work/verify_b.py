import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pcbnew as p

out = Path('outputs')
directory = out / 'Zasilacz_RevB'
board = p.LoadBoard(str(directory / 'Zasilacz_RevB.kicad_pcb'))
parts = json.loads(Path('work/catalog_b.json').read_text(encoding='utf-8'))
expected = {(c['ref'], pin): net for c in parts for pin, net in c['connection'].items()}
xml = ET.parse('work/psb.xml')
schematic = {(node.get('ref'), node.get('pin')): net.get('name').lstrip('/')
             for net in xml.findall('./nets/net') for node in net.findall('node')}
footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}
pads = {(ref, pad.GetNumber()): pad.GetNetname().lstrip('/')
        for ref, fp in footprints.items() for pad in fp.Pads() if pad.GetNetname()}
assert expected == schematic == pads
assert set(footprints) == {c['ref'] for c in parts}

entry = {
    ('J1','1'):'P_L', ('J1','2'):'P_N',
    ('F1','1'):'P_L', ('F1','2'):'P_LF', ('R1','1'):'P_LF', ('R1','2'):'P_LR',
    ('RV1','1'):'P_LR', ('RV1','2'):'P_N',
    ('BR1','1'):'P_BR', ('BR1','2'):'P_0', ('BR1','3'):'P_LR', ('BR1','4'):'P_N',
    ('J2','1'):'S_ENFEED', ('J2','2'):'S_EN', ('J2','3'):'S_FUSED', ('J2','4'):'S_LED_PLUS',
    ('J3','1'):'S_LED_PLUS', ('J3','2'):'S_LED_KA', ('J3','3'):'S_LED_KB',
}
assert all(pads[pin] == net for pin, net in entry.items())
edges = [shape for shape in board.GetDrawings() if shape.GetLayer() == p.Edge_Cuts]
coords = [xy for e in edges for xy in (e.GetStart(), e.GetEnd())]
assert len(edges) == 4
assert max(c.x for c in coords) - min(c.x for c in coords) == p.FromMM(66)
assert max(c.y for c in coords) - min(c.y for c in coords) == p.FromMM(34)

primary, secondary = [], []
for item in [pad for fp in footprints.values() for pad in fp.Pads()] + list(board.GetTracks()):
    name = item.GetNetname().lstrip('/')
    box = item.GetBoundingBox()
    if name.startswith('P_'):
        primary.append(box.GetRight())
    elif name.startswith('S_'):
        secondary.append(box.GetLeft())
band = p.ToMM(min(secondary) - max(primary))
assert band >= 8.0, band

with (directory / 'Produkcja_DO_PRZEGLADU/CPL_Zasilacz_KiCad.csv').open(encoding='utf-8-sig', newline='') as f:
    positions = list(csv.DictReader(f))
assert len(positions) == len({row['Ref'] for row in positions})
assert {row['Ref'] for row in positions} == {
    ref for ref, fp in footprints.items() if fp.GetAttributes() & p.FP_SMD
}
with (out / 'BOM_Zasilacz_RevB.csv').open(encoding='utf-8-sig', newline='') as f:
    bom = {row['Oznaczenie']: row for row in csv.DictReader(f)}
assert set(bom) == set(footprints)
assert all(bom[c['ref']]['MPN'] == c['part'] for c in parts)
assert 'Errors 0  Warnings 0' in (directory / 'ERC.rpt').read_text(encoding='utf-8-sig')
drc = (directory / 'DRC.rpt').read_text(encoding='utf-8-sig')
assert all(f'Found 0 {key}' in drc for key in ['DRC violations','unconnected pads','Footprint errors'])

(out / 'Weryfikacja_KiCad_RevB.md').write_text(f'''# Weryfikacja KiCad 10.0.8 · Rev B

- Sprawdzono 66 × 34 mm na warstwie Edge.Cuts oraz wszystkie {len(pads)} przypisania pin–sieć na podstawie założeń, listy połączeń ze schematu i odczytu PCB. Osobno sprawdzono kolejność zabezpieczeń przed mostkiem, pinout BR1 oraz J2/J3.
- Zmierzony odstęp między skrajnymi obwiedniami miedzi sieci P i S w rzucie na oś x wynosi **{band:.3f} mm**. Odczyt uwzględnia obie warstwy, pady, ścieżki i przelotki. Geometria PCB jest częścią oceny izolacji zmontowanego zespołu.
- ERC oraz DRC z porównaniem PCB do schematu zakończyły się bez naruszeń. Listy reguł pominiętych przez konfigurację są w raportach KiCad.
- Zgodność {len(bom)} pozycji elektrycznych BOM z PCB i {len(positions)} pozycji SMD w eksporcie montażowym sprawdzono osobno. Pliki Gerber, wierceń i montażowe są przeznaczone do przeglądu przez wykonawcę. Potwierdzenia wymagają kierunki, niestandardowe footprinty oraz montaż dwustronny.
- Pomiary na fizycznym prototypie i badania bezpieczeństwa są do wykonania według planu prób.
''', encoding='utf-8')
print(f'{len(pads)} pins, {len(bom)} parts, {len(positions)} SMT positions, {band:.3f} mm copper band')
