"""Verify that the Rev H routing cleanup preserves control-board connections and thermal copper."""

from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import pcbnew as pcb

from revg_control import DEST as BASE, NAME as BASE_NAME, NEW_VIAS, LARGER_VIAS, point, vias
from smooth_tracks import tracks
from verify_revf_control import pins


DEST = Path('outputs/Zasilacz_RevH_Sterowanie')
NAME = DEST.name


def placement(board):
    return {fp.GetReference(): (fp.GetFPID().GetLibItemName(), tuple(fp.GetPosition()),
                                 fp.GetOrientationDegrees(), fp.GetLayer())
            for fp in board.GetFootprints()}


def lengths(board, net, layer=None):
    return sum(t.GetLength() for t in tracks(board) if t.GetNetname() == net
               and (layer is None or t.GetLayer() == layer))/1e6


def check(netlist):
    source = pcb.LoadBoard(str(BASE / f'{BASE_NAME}.kicad_pcb'))
    board = pcb.LoadBoard(str(DEST / f'{NAME}.kicad_pcb'))
    expected = {(node.get('ref'), node.get('pin')): net.get('name')
                for net in ET.parse(netlist).findall('./nets/net') for node in net.findall('node')}
    assert pins(source) == pins(board) == expected
    assert placement(source) == placement(board)
    assert vias(source) == vias(board)
    assert board.GetCopperLayerCount() == 4
    edges = [item for item in board.GetDrawings() if item.GetLayer() == pcb.Edge_Cuts]
    corners = {tuple(pt) for edge in edges for pt in (edge.GetStart(), edge.GetEnd())}
    assert len(edges) == 4 and corners == {(x*1000000, y*1000000) for x in (75, 105) for y in (70, 95)}
    assert lengths(board, '/REF') <= lengths(source, '/REF') + .001
    assert lengths(board, '/REF', pcb.In1_Cu) < 12
    zones = {z.GetLayer(): z for z in board.Zones() if z.GetNetname() == '/S_RTN'}
    filled = {layer: z.GetFilledPolysList(layer) for layer, z in zones.items()}
    assert set(filled) == {pcb.F_Cu, pcb.In1_Cu, pcb.B_Cu}
    plane = zones[pcb.In1_Cu].GetFilledArea()/1e12
    assert filled[pcb.In1_Cu].OutlineCount() == 1 and plane > 560
    front = filled[pcb.F_Cu]
    for ref, vias_by_ic in NEW_VIAS.items():
        pad = board.FindFootprintByReference(ref).FindPadByNumber('9').GetPosition()
        for xy in [*vias_by_ic, LARGER_VIAS[ref]]:
            pos = point(xy)
            assert all(polygon.Contains(pos) for polygon in filled.values())
            assert any(front.Contains(pos, i) and front.Contains(pad, i)
                       for i in range(front.OutlineCount()))
    drc = (DEST/'DRC.rpt').read_text(encoding='utf8')
    assert all(s in drc for s in ('Found 0 DRC violations', 'Found 0 unconnected pads', 'Found 0 Footprint errors'))
    assert 'Errors 0  Warnings 0' in (DEST/'ERC.rpt').read_text(encoding='utf8')
    print(f'{len(expected)} pin-net pairs; {len(vias(board))} unchanged vias; '
          f'{plane:.1f} mm² return plane; {lengths(board, "/REF"):.1f} mm REF; '
          f'{len(tracks(source))} to {len(tracks(board))} segments')


if __name__ == '__main__':
    check(sys.argv[1])
