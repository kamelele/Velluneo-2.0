"""Check Rev K pinout, bridge pads, thermal stitching and the separation of the PCB sides."""

from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import pcbnew as p

import revh_power
import revk_power as rev
from verify_revf_power import pads
from smooth_tracks import tracks

THERMAL = {(100.35, 92.45), (99.9, 93.15), (98.95, 91.9), (100.45, 91.2)}
HOT = {'/P_D', '/P_BULK', '/P_CL', '/P_CLMID', '/S_SW', '/S_DAMP'}


def hot_tracks(board):
    return sorted((t.GetNetname(), t.GetLayer(), tuple(t.GetStart()), tuple(t.GetEnd()), t.GetWidth())
                  for t in tracks(board) if t.GetNetname() in HOT)


def main(netlist):
    old = p.LoadBoard(str(revh_power.DEST / f'{revh_power.NAME}.kicad_pcb'))
    board = p.LoadBoard(str(rev.DEST / f'{rev.NAME}.kicad_pcb'))
    current = pads(board)
    schematic = {(node.get('ref'),node.get('pin')):net.get('name')
                 for net in ET.parse(netlist).findall('./nets/net') for node in net.findall('node')}
    assert schematic == {key: d.GetNetname() for key,d in current.items() if d.GetNetname()}
    assert {str(n): current['BR1', str(n)].GetNetname() for n in range(1,5)} == {
        '1': '/P_BR', '2': '/P_N', '3': '/P_0', '4': '/P_LR'}
    for key, prior in pads(old).items():
        if key[0] == 'BR1':
            continue
        new = current[key]
        assert (new.GetNetname(), new.GetPosition(), new.GetSize(), new.GetDrillSize()) == (
            prior.GetNetname(), prior.GetPosition(), prior.GetSize(), prior.GetDrillSize()), key
    assert {tuple(p.ToMM(current['BR1',str(n)].GetSize())) for n in range(1,5)} == {(1.2,1.8)}
    assert hot_tracks(board) == hot_tracks(old)
    assert {f.GetReference() for f in board.GetFootprints() if f.IsDNP()} == revh_power.DNP
    assert all(not pad.IsOnLayer(p.F_Paste) and pad.IsOnLayer(p.F_Mask)
               for (ref, _), pad in current.items() if ref in revh_power.DNP)
    edge = [g for g in board.GetDrawings() if g.GetLayer() == p.Edge_Cuts]
    assert len(edge) == 4 and {tuple(v) for g in edge for v in (g.GetStart(), g.GetEnd())} == {
        (p.FromMM(x), p.FromMM(y)) for x in (75,130.5) for y in (70,104)}
    zones = {z.GetLayer():z for z in board.Zones()}
    assert board.GetCopperLayerCount() == 2 and set(zones) == {p.F_Cu, p.B_Cu}
    assert all(z.GetNetname() == '/P_0' and z.IsFilled() for z in zones.values())
    fill = {l: z.GetFilledPolysList(l) for l,z in zones.items()}
    pad18 = current['U1','18'].GetPosition()
    vias = {tuple(p.ToMM(t.GetPosition())): t for t in board.GetTracks() if isinstance(t,p.PCB_VIA)}
    for xy in THERMAL:
        via = vias[xy]
        center = via.GetPosition()
        assert via.GetNetname() == '/P_0' and (via.GetWidth(p.F_Cu), via.GetDrillValue()) == (600000,300000)
        assert fill[p.F_Cu].Contains(center)
        assert any(fill[p.B_Cu].Contains(center,i) and fill[p.B_Cu].Contains(pad18,i)
                   for i in range(fill[p.B_Cu].OutlineCount()))
    bounds = [(item.GetNetname(),item.GetBoundingBox()) for item in [*current.values(),*board.GetTracks()]]
    bounds += [('/P_0',poly.BBox()) for poly in fill.values()]
    gap = p.ToMM(min(b.GetLeft() for n,b in bounds if n.startswith('/S_'))
                 - max(b.GetRight() for n,b in bounds if n.startswith('/P_')))
    assert gap >= 8.19, gap
    drc = (rev.DEST/'DRC.rpt').read_text(encoding='utf8')
    assert all(s in drc for s in ('Found 0 DRC violations','Found 0 unconnected pads','Found 0 Footprint errors'))
    assert 'Errors 0  Warnings 0' in (rev.DEST/'ERC.rpt').read_text(encoding='utf8')
    print(f'{len(schematic)} pin-net pairs; {gap:.3f} mm projected barrier; '
          f'{len(tracks(old))} to {len(tracks(board))} segments; '
          f'P_0 fill {zones[p.F_Cu].GetFilledArea()/1e12:.1f} + {zones[p.B_Cu].GetFilledArea()/1e12:.1f} mm²')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
