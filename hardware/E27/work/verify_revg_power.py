"""Check the Rev G change scope and the assembled power schematic/PCB pairing."""
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import pcbnew as p

import revf_power as revf
import revg_power as revg
from verify_revf_power import pads, primary_tracks


def all_tracks(board):
    def signature(item):
        if isinstance(item, p.PCB_VIA):
            return item.GetNetname(), -1, tuple(item.GetPosition()), item.GetWidth(p.F_Cu), item.GetDrillValue()
        return item.GetNetname(), item.GetLayer(), tuple(item.GetStart()), tuple(item.GetEnd()), item.GetWidth()

    return sorted(signature(item) for item in board.GetTracks() if item.GetNetname().startswith('/S_'))


def main(netlist):
    old = p.LoadBoard(str(revf.DEST / f'{revf.NAME}.kicad_pcb'))
    new = p.LoadBoard(str(revg.DEST / f'{revg.NAME}.kicad_pcb'))
    old_pads, new_pads = pads(old), pads(new)
    changed_pads = {('C3', '1'), ('C3', '2'), ('R4', '2')}
    assert new_pads.keys() - old_pads.keys() == {('R22', '1'), ('R22', '2')}
    for key in old_pads.keys() - changed_pads:
        a, b = old_pads[key], new_pads[key]
        assert (a.GetNetname(), a.GetPosition(), a.GetSize(), a.GetDrillSize()) == (
            b.GetNetname(), b.GetPosition(), b.GetSize(), b.GetDrillSize()), key
    before, after = primary_tracks(old), primary_tracks(new)
    removed, added = before - after, after - before
    for net, layer, *geom in removed.keys() | added.keys():
        assert net in ('/P_BULK', '/P_CL', '/P_CLMID') and layer == p.B_Cu, (net, layer)
        for x, y in geom[:2]:
            assert 86e6 < x < 98e6 and 85e6 < y < 95e6, (net, x, y)
    assert all_tracks(old) == all_tracks(new)
    xml = {(node.get('ref'), node.get('pin')): net.get('name')
           for net in ET.parse(netlist).findall('./nets/net') for node in net.findall('node')}
    assert xml == {key: pad.GetNetname() for key, pad in new_pads.items() if pad.GetNetname()}
    assert {key for key, net in xml.items() if net == '/P_CLMID'} == {('R4', '2'), ('R22', '1')}
    assert xml['J101', '1'] == '/S_RAW' and xml['J101', '2'] == '/S_RTN'
    erc = (revg.DEST / 'ERC.rpt').read_text(encoding='utf8')
    drc = (revg.DEST / 'DRC.rpt').read_text(encoding='utf8')
    assert 'Errors 0  Warnings 0' in erc
    assert all(s in drc for s in ('Found 0 DRC violations', 'Found 0 unconnected pads', 'Found 0 Footprint errors'))
    edges = [g for g in new.GetDrawings() if g.GetLayer() == p.Edge_Cuts]
    assert len(edges) == 4 and {tuple(v) for g in edges for v in (g.GetStart(), g.GetEnd())} == {
        (p.FromMM(x), p.FromMM(y)) for x in (75, 130.5) for y in (70, 104)}
    zones = list(new.Zones())
    assert new.GetCopperLayerCount() == 2 and len(zones) == 2
    assert all(z.GetNetname() == '/P_0' and z.IsFilled() for z in zones)
    bounds = [(x.GetNetname(), x.GetBoundingBox()) for x in [*new_pads.values(), *new.GetTracks()]]
    bounds += [(z.GetNetname(), z.GetFilledPolysList(z.GetLayer()).BBox()) for z in zones]
    gap = p.ToMM(min(b.GetLeft() for n, b in bounds if n.startswith('/S_'))
                 - max(b.GetRight() for n, b in bounds if n.startswith('/P_')))
    assert gap >= 8.19, gap
    area = {new.GetLayerName(z.GetLayer()): z.GetFilledArea() / 1e12 for z in zones}
    (revg.DEST / 'Weryfikacja_RevG.md').write_text(f"""# Kontrola płytki mocy Rev G

- KiCad wykazał 0 naruszeń ERC i DRC, 0 brakujących połączeń oraz 0 rozbieżności PCB ze schematem. Niezależny odczyt porównał {len(xml)} przypisań pin–sieć.
- Względem Rev F usunięto {sum(removed.values())} segmentów, dodano {sum(added.values())}. Zmiany tras obejmują wyłącznie tylną stronę przy RCD. Prowadzenie strony wtórnej i J101 są identyczne z Rev F.
- PCB ma 55,5 × 34 mm i dwie warstwy. Pas w osi X między skrajną miedzią pierwotną i wtórną wraz z wypełnieniami wynosi {gap:.3f} mm. Wypełnienia P_0 mają {area['F.Cu']:.1f} mm² na F.Cu i {area['B.Cu']:.1f} mm² na B.Cu.
- Tę rewizję zweryfikowano cyfrowo. Kryteria pomiarowe określa [analiza RCD](Analiza_RCD.md).
""", encoding='utf8')
    print(f'{len(xml)} pin–net pairs; {gap:.3f} mm projected isolation band')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
