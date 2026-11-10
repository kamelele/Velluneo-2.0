"""Audit the routed valley-fill study against its KiCad netlist and copper geometry."""

from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import pcbnew as pcb

from verify_revf_control import pins


DEST = Path('outputs/Studium_RevL_ValleyFill')
NAME = 'Zasilacz_RevL_Studium'


def verify(netlist):
    board = pcb.LoadBoard(str(DEST / f'{NAME}.kicad_pcb'))
    assert board.GetCopperLayerCount() == 4
    expected = {(node.get('ref'), node.get('pin')): net.get('name')
                for net in ET.parse(netlist).findall('./nets/net') for node in net.findall('node')}
    assert pins(board) == expected and len(expected) == 125
    for ref, nets in {
        'BR1': ('P_BR', 'P_N', 'P_0', 'P_LR'),
        'C2': ('P_BULK', 'P_VF_A'), 'C17': ('P_VF_B', 'P_0'),
        'D10': ('P_VF_CH', 'P_VF_A'), 'D11': ('P_VF_A', 'P_0'), 'D12': ('P_BULK', 'P_VF_B'),
        'C18': ('P_BULK', 'P_0'), 'J101': ('S_RAW', 'S_RTN'),
    }.items():
        assert tuple(expected[ref,str(n)] for n in range(1,len(nets)+1)) == tuple('/'+net for net in nets)
    cap = board.FindFootprintByReference('C17')
    assert all(tuple(pad.GetSize()) == (1350000,1350000)
               and tuple(pad.GetDrillSize()) == (800000,800000) for pad in cap.Pads())
    edges = [g for g in board.GetDrawings() if g.GetLayer() == pcb.Edge_Cuts]
    assert len(edges) == 4 and {tuple(v) for g in edges for v in (g.GetStart(),g.GetEnd())} == {
        (pcb.FromMM(x), pcb.FromMM(y)) for x in (75,130.5) for y in (70,104)}
    plane, = list(board.Zones())
    assert plane.GetLayer() == pcb.In1_Cu and plane.GetNetname() == '/P_0'
    fill = plane.GetFilledPolysList(pcb.In1_Cu)
    assert fill.OutlineCount() == 1
    parts = [*board.GetTracks(), *(pad for fp in board.GetFootprints() for pad in fp.Pads())]
    boxes = [(part.GetNetname(),part.GetBoundingBox()) for part in parts]
    boxes.append(('/P_0',fill.BBox()))
    separation = (min(b.GetLeft() for n,b in boxes if n.startswith('/S_'))
                  - max(b.GetRight() for n,b in boxes if n.startswith('/P_')))/1e6
    assert separation >= 8.19
    drc = (DEST/'DRC.rpt').read_text(encoding='utf8')
    assert all(s in drc for s in ('Found 0 DRC violations','Found 0 unconnected pads','Found 0 Footprint errors'))
    assert 'Errors 0  Warnings 0' in (DEST/'ERC.rpt').read_text(encoding='utf8')
    traces = sum(type(t) is pcb.PCB_TRACK for t in board.GetTracks())
    vias = sum(isinstance(t,pcb.PCB_VIA) for t in board.GetTracks())
    print(f'{len(expected)} pin-net pairs; projected gap {separation:.3f} mm; '
          f'In1.Cu {plane.GetFilledArea()/1e12:.2f} mm²; {traces} segments, {vias} vias')


if __name__ == '__main__':
    verify(sys.argv[1])
