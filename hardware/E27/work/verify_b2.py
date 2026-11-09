"""Check the exported adapter against the schematic and design inputs."""
import csv
from pathlib import Path
import xml.etree.ElementTree as ET

import pcbnew as pcb

from revb2_guard import NAME, PARTS, SIZE, PIN_NAMES

folder = Path('outputs') / NAME
board = pcb.LoadBoard(str(folder / (NAME + '.kicad_pcb')))
footprints = {f.GetReference():f for f in board.GetFootprints()}
assert footprints.keys() == {p.ref for p in PARTS}
pins = {(ref,pad.GetNumber()):pad.GetNetname() for ref,fp in footprints.items() for pad in fp.Pads()}
expected = {
    (p.ref,str(n)):('/'+net if net else f'unconnected-({p.ref}-{PIN_NAMES[p.kind][n-1]}-Pad{n})')
    for p in PARTS for n,net in p.pins.items()
}
export = ET.parse('work/revb2-netlist.xml')
schematic = {(pin.get('ref'),pin.get('pin')):net.get('name')
             for net in export.findall('./nets/net') for pin in net.findall('node')}
assert pins == expected == schematic, (pins.items() ^ expected.items(), pins.items() ^ schematic.items())
assert all(not name.startswith('/P_') for name in pins.values())
edge = [s for s in board.GetDrawings() if s.GetLayer() == pcb.Edge_Cuts]
points = [p for s in edge for p in (s.GetStart(),s.GetEnd())]
assert len(edge) == 4
assert (pcb.ToMM(max(p.x for p in points)-min(p.x for p in points)),
        pcb.ToMM(max(p.y for p in points)-min(p.y for p in points))) == SIZE
with (folder / 'Produkcja_DO_PRZEGLADU/CPL_RevB2.csv').open(encoding='utf-8-sig',newline='') as stream:
    placements = list(csv.DictReader(stream))
assert {row['Ref'] for row in placements} == {p.ref for p in PARTS if p.kind not in {'PORT','TP'}}
with (folder / 'BOM_RevB2.csv').open(encoding='utf-8-sig',newline='') as stream:
    bom = list(csv.DictReader(stream))
assert {r['Ref'] for r in bom} == {p.ref for p in PARTS if p.kind != 'TP'}
assert 'Errors 0  Warnings 0' in (folder/'ERC.rpt').read_text(encoding='utf-8-sig')
drc = (folder/'DRC.rpt').read_text(encoding='utf-8-sig')
assert all(f'Found 0 {key}' in drc for key in ('DRC violations','unconnected pads','Footprint errors'))
print(f'{len(pins)} pin mappings, {len(bom)} BOM rows and {len(placements)} SMT placements verified.')
