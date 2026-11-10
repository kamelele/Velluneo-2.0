"""Preserve Rev F circuitry and add thermal vias outside the AL5812 solder pads."""
from collections import Counter
from pathlib import Path
from shutil import copy2, copytree
import sys
from xml.etree import ElementTree as ET

import pcbnew as p

from verify_revf_control import DEST as BASE, NAME as BASE_NAME, pins


NAME = 'Zasilacz_RevG_Sterowanie'
DEST = Path('outputs') / NAME
NEW_VIAS = {'U3': [(102.55, 84.35), (102.55, 85), (102.55, 85.65)],
            'U4': [(99.15, 85.55), (99.2, 83.8)]}
LARGER_VIAS = {'U3': (99.6, 85), 'U4': (95.6, 85.5)}


def point(xy):
    return p.VECTOR2I(*(p.FromMM(v) for v in xy))


def mm(pt):
    return tuple(p.ToMM(pt))


def rebuild():
    DEST.mkdir(parents=True, exist_ok=True)
    copytree(BASE / 'E27.pretty', DEST / 'E27.pretty', dirs_exist_ok=True)
    for source in BASE.iterdir():
        if source.suffix in ('.wrl', '.kicad_sym') or source.name.endswith('lib-table'):
            copy2(source, DEST / source.name)
    copy2(BASE / 'BOM_RevF.csv', DEST / 'BOM_RevG.csv')
    for ext in ('pro', 'sch', 'pcb'):
        source = (BASE / f'{BASE_NAME}.kicad_{ext}').read_text(encoding='utf8')
        data = source.replace(BASE_NAME, NAME).replace('REV F', 'REV G').replace('Rev F /', 'Rev G /')
        (DEST / f'{NAME}.kicad_{ext}').write_text(data.replace('(rev "F")', '(rev "G")'), encoding='utf8')
    path = DEST / f'{NAME}.kicad_pcb'
    board = p.LoadBoard(str(path))
    net = board.FindNet('/S_RTN')
    for item in board.GetTracks():
        if isinstance(item, p.PCB_VIA) and item.GetNetname() == '/S_RTN' and mm(item.GetPosition()) in LARGER_VIAS.values():
            item.SetDrill(p.FromMM(.25))
            item.SetWidth(p.FromMM(.55))
    for positions in NEW_VIAS.values():
        for xy in positions:
            via = p.PCB_VIA(board)
            via.SetViaType(p.VIATYPE_THROUGH)
            via.SetLayerPair(p.F_Cu, p.B_Cu)
            via.SetPosition(point(xy))
            via.SetDrill(p.FromMM(.20))
            via.SetWidth(p.FromMM(.45))
            via.SetFrontTentingMode(p.TENTING_MODE_TENTED)
            via.SetBackTentingMode(p.TENTING_MODE_TENTED)
            via.SetNet(net)
            board.Add(via)
    assert p.SaveBoard(str(path), board)


def traces(board):
    return Counter((t.GetNetname(), t.GetLayer(), mm(t.GetStart()), mm(t.GetEnd()), t.GetWidth())
                   for t in board.GetTracks() if not isinstance(t, p.PCB_VIA))


def vias(board):
    return {(t.GetNetname(), mm(t.GetPosition())): (p.ToMM(t.GetWidth(p.F_Cu)), p.ToMM(t.GetDrillValue()))
            for t in board.GetTracks() if isinstance(t, p.PCB_VIA)}


def verify(netlist):
    old = p.LoadBoard(str(BASE / f'{BASE_NAME}.kicad_pcb'))
    board = p.LoadBoard(str(DEST / f'{NAME}.kicad_pcb'))
    schematic = {(node.get('ref'), node.get('pin')): net.get('name')
                 for net in ET.parse(netlist).findall('./nets/net') for node in net.findall('node')}
    assert pins(old) == pins(board) == schematic
    assert traces(old) == traces(board)
    old_vias, new_vias = vias(old), vias(board)
    expected = old_vias | {('/S_RTN', xy): (.55, .25) for xy in LARGER_VIAS.values()}
    expected |= {('/S_RTN', xy): (.45, .20) for row in NEW_VIAS.values() for xy in row}
    assert new_vias == expected and len(new_vias) == len(old_vias) + 5
    footprints = {fp.GetReference(): fp for fp in board.GetFootprints()}
    old_footprints = {fp.GetReference(): fp for fp in old.GetFootprints()}
    for ref, fp in footprints.items():
        prior = old_footprints[ref]
        assert (fp.GetFPID().GetLibItemName(), fp.GetPosition(), fp.GetOrientationDegrees()) == (
            prior.GetFPID().GetLibItemName(), prior.GetPosition(), prior.GetOrientationDegrees()), ref
    zones = {z.GetLayer(): z.GetFilledPolysList(z.GetLayer()) for z in board.Zones() if z.GetNetname() == '/S_RTN'}
    assert set(zones) == {p.F_Cu, p.In1_Cu, p.B_Cu} and zones[p.In1_Cu].OutlineCount() == 1
    for ref, xy in LARGER_VIAS.items():
        front, pad = zones[p.F_Cu], footprints[ref].FindPadByNumber('9')
        for via in [xy, *NEW_VIAS[ref]]:
            pos = point(via)
            assert all(poly.Contains(pos) for poly in zones.values())
            assert any(front.Contains(pos, i) and front.Contains(pad.GetPosition(), i)
                       for i in range(front.OutlineCount()))
            assert not any(d.HitTest(pos, p.FromMM(.30)) for f in footprints.values() for d in f.Pads())
    erc = (DEST / 'ERC.rpt').read_text(encoding='utf8')
    drc = (DEST / 'DRC.rpt').read_text(encoding='utf8')
    assert 'Errors 0  Warnings 0' in erc
    assert all(s in drc for s in ('Found 0 DRC violations', 'Found 0 unconnected pads', 'Found 0 Footprint errors'))
    print(f'{len(schematic)} unchanged pin–net pairs; 5 new and 2 enlarged thermal vias')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        rebuild()
    else:
        verify(sys.argv[1])
