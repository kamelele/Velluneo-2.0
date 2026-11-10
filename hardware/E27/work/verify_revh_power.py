"""Verify the Rev H damping layout against the archived Rev G board."""
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

import pcbnew as p

import revg_power as revg
import revh_power as revh
from verify_revf_power import pads, primary_tracks
from verify_revg_power import all_tracks
from collections import Counter


def main(netlist):
    base = p.LoadBoard(str(revg.DEST / f'{revg.NAME}.kicad_pcb'))
    board = p.LoadBoard(str(revh.DEST / f'{revh.NAME}.kicad_pcb'))
    old_pads, new_pads = pads(base), pads(board)
    assert new_pads.keys() - old_pads.keys() == {(ref, n) for ref in revh.DNP for n in ('1', '2')}
    for key, old in old_pads.items():
        new = new_pads[key]
        assert (old.GetNetname(), old.GetPosition(), old.GetSize(), old.GetDrillSize()) == (
            new.GetNetname(), new.GetPosition(), new.GetSize(), new.GetDrillSize()), key
    assert primary_tracks(base) == primary_tracks(board)
    previous, current = Counter(all_tracks(base)), Counter(all_tracks(board))
    assert not (previous - current)
    extra = current - previous
    for net, layer, start, end, _ in extra:
        assert net in ('/S_SW', '/S_GND', '/S_DAMP') and layer == p.F_Cu
        assert all(116e6 < x < 125e6 and 84e6 < y < 91e6 for x, y in (start, end))
    assert {fp.GetReference() for fp in board.GetFootprints() if fp.IsDNP()} == revh.DNP
    assert all(not pad.IsOnLayer(p.F_Paste) and pad.IsOnLayer(p.F_Mask)
               for (ref, _), pad in new_pads.items() if ref in revh.DNP)
    xml = {(node.get('ref'), node.get('pin')): net.get('name')
           for net in ET.parse(netlist).findall('./nets/net') for node in net.findall('node')}
    assert xml == {key: pad.GetNetname() for key, pad in new_pads.items() if pad.GetNetname()}
    assert xml['C16','1'] == '/S_SW' and xml['R23','2'] == '/S_GND'
    assert xml['C16','2'] == xml['R23','1'] == '/S_DAMP'
    assert xml['J101','1'] == '/S_RAW' and xml['J101','2'] == '/S_RTN'
    erc = (revh.DEST / 'ERC.rpt').read_text(encoding='utf8')
    drc = (revh.DEST / 'DRC.rpt').read_text(encoding='utf8')
    assert 'Errors 0  Warnings 0' in erc
    assert all(s in drc for s in ('Found 0 DRC violations', 'Found 0 unconnected pads', 'Found 0 Footprint errors'))
    edges = [g for g in board.GetDrawings() if g.GetLayer() == p.Edge_Cuts]
    assert len(edges) == 4 and {tuple(v) for g in edges for v in (g.GetStart(), g.GetEnd())} == {
        (p.FromMM(x), p.FromMM(y)) for x in (75, 130.5) for y in (70, 104)}
    zones = list(board.Zones())
    assert board.GetCopperLayerCount() == 2 and len(zones) == 2
    assert all(z.GetNetname() == '/P_0' and z.IsFilled() for z in zones)
    bounds = [(x.GetNetname(), x.GetBoundingBox()) for x in [*new_pads.values(), *board.GetTracks()]]
    bounds += [(z.GetNetname(), z.GetFilledPolysList(z.GetLayer()).BBox()) for z in zones]
    gap = p.ToMM(min(b.GetLeft() for n, b in bounds if n.startswith('/S_'))
                 - max(b.GetRight() for n, b in bounds if n.startswith('/P_')))
    assert gap >= 8.19, gap
    length = sum(((a[0] - b[0])**2 + (a[1] - b[1])**2)**.5 * count / 1e6 for (_, _, a, b, _), count in extra.items())
    print(f'{len(xml)} pin–net pairs; {sum(extra.values())} new segments ({length:.2f} mm); {gap:.3f} mm band')
    (revh.DEST / 'Weryfikacja_RevH.md').write_text(f"""# Kontrola płytki mocy Rev H

- KiCad wykazał 0 naruszeń ERC i DRC, 0 brakujących połączeń i 0 rozbieżności ze schematem. Niezależny odczyt porównał {len(xml)} przypisań pin–sieć.
- Zachowano trasowanie Rev G i położenia wszystkich poprzednich padów. Dodano {sum(extra.values())} odcinków ({length:.2f} mm łącznie) na F.Cu po stronie wtórnej. Ścieżki prowadzą do C16/R23. Części mają flagę DNP i pola lutownicze bez warstwy pasty.
- Obrys 55,5 × 34 mm, dwie warstwy i pas {gap:.3f} mm między projekcjami skrajnej miedzi stron w osi X. Tłumienie oscylacji i zachowanie cieplne wymagają prób.
""", encoding='utf8')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
