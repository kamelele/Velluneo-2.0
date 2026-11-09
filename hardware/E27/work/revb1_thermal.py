"""Add local, net-bound thermal copper to the Rev B reference design."""
import argparse
from math import dist
from pathlib import Path
from shutil import copy2, copytree

import pcbnew as pcb

BASE = Path('outputs/Zasilacz_RevB')
DEST = Path('outputs/Zasilacz_RevB1')
BOARD = DEST / 'Zasilacz_RevB1.kicad_pcb'
LAYERS = (pcb.F_Cu, pcb.B_Cu)
VIA_DIAMETER = .60
VIA_DRILL = .30
WINDOWS = (
    ('SOURCE', '/P_0', (85.2, 88.0, 100.8, 102.6)),
    ('CC_RETURN', '/S_RTN', (122.8, 92.0, 139.6, 102.6)),
)
VIA_GROUPS = (
    ('SOURCE', (99.5, 92.55), (97.2, 89.7, 100.5, 95.6), 6),
    ('CC_RETURN', (127.65, 95.25), (125.8, 93.45, 129.25, 97.65), 4),
    ('CC_RETURN', (134.1, 95.25), (131.8, 92.6, 138.4, 99.4), 4),
)
ZONE_MAINS_RULE = '''
(rule "Thermal copper to mains inputs"
 (constraint clearance (min 1.5mm))
 (condition "(A.Type == 'Zone' && A.NetName == '/P_0' && (B.NetName == '/P_N' || B.NetName =~ '/P_L*')) || (B.Type == 'Zone' && B.NetName == '/P_0' && (A.NetName == '/P_N' || A.NetName =~ '/P_L*'))"))
'''


def point(x, y):
    return pcb.VECTOR2I(pcb.FromMM(x), pcb.FromMM(y))


def xy(vec):
    return pcb.ToMM(vec.x), pcb.ToMM(vec.y)


def add_zone(board, name, net, bounds, layer):
    left, top, right, bottom = bounds
    zone = pcb.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(board.FindNet(net))
    zone.SetZoneName(f'TH_{name}_{"F" if layer == pcb.F_Cu else "B"}')
    zone.SetLocalClearance(pcb.FromMM(.32))
    zone.SetMinThickness(pcb.FromMM(.25))
    zone.SetPadConnection(pcb.ZONE_CONNECTION_THT_THERMAL)
    zone.SetThermalReliefGap(pcb.FromMM(.35))
    zone.SetThermalReliefSpokeWidth(pcb.FromMM(.38))
    zone.SetIslandRemovalMode(pcb.ISLAND_REMOVAL_MODE_ALWAYS)
    contour = zone.Outline()
    contour.NewOutline()
    for x, y in ((left, top), (right, top), (right, bottom), (left, bottom)):
        contour.Append(int(pcb.FromMM(x)), int(pcb.FromMM(y)))
    board.Add(zone)


def outline():
    DEST.mkdir(exist_ok=True)
    copytree(BASE / 'E27.pretty', DEST / 'E27.pretty', dirs_exist_ok=True)
    for source in list(BASE.glob('*.wrl')) + [BASE / f for f in ('E27.kicad_sym', 'sym-lib-table', 'fp-lib-table')]:
        copy2(source, DEST / source.name)
    for suffix in ('pro', 'sch', 'dru'):
        name = f'Zasilacz_RevB.kicad_{suffix}'
        source = (BASE / name).read_text(encoding='utf-8')
        if suffix == 'sch':
            source = source.replace('Zasilacz_RevB', 'Zasilacz_RevB1')
            source = source.replace('/ Rev B', '/ Rev B1').replace('rewizja B laboratoryjna', 'rewizja B1 laboratoryjna')
            source = source.replace('(rev "B")', '(rev "B1")')
        elif suffix == 'dru':
            source += ZONE_MAINS_RULE
        (DEST / name.replace('RevB', 'RevB1')).write_text(source, encoding='utf-8')
    board = pcb.LoadBoard(str(BASE / 'Zasilacz_RevB.kicad_pcb'))
    for item in board.GetDrawings():
        if isinstance(item, pcb.PCB_TEXT) and item.GetText() == 'E27 / REV B':
            item.SetText('E27 / REV B1')
            item.SetPosition(point(134.0, 102.6))
    for name, net, bounds in WINDOWS:
        for layer in LAYERS:
            add_zone(board, name, net, bounds, layer)
    assert pcb.SaveBoard(str(BOARD), board)


def via(board, net, center):
    item = pcb.PCB_VIA(board)
    item.SetViaType(pcb.VIATYPE_THROUGH)
    item.SetLayerPair(*LAYERS)
    item.SetPosition(point(*center))
    item.SetDrill(pcb.FromMM(VIA_DRILL))
    item.SetWidth(pcb.FromMM(VIA_DIAMETER))
    item.SetFrontTentingMode(pcb.TENTING_MODE_TENTED)
    item.SetBackTentingMode(pcb.TENTING_MODE_TENTED)
    item.SetNet(net)
    board.Add(item)


def grid(bounds):
    left, top, right, bottom = (round(x * 10) for x in bounds)
    return [(x / 10, y / 10) for x in range(left, right + 1) for y in range(top, bottom + 1)]


def stitch():
    board = pcb.LoadBoard(str(BOARD))
    obstacles = [p.GetBoundingBox() for f in board.GetFootprints() for p in f.Pads() if p.IsOnCopperLayer()]
    occupied = [xy(t.GetPosition()) for t in board.GetTracks() if isinstance(t, pcb.PCB_VIA)]
    offsets = ((0,0), (.33,0), (-.33,0), (0,.33), (0,-.33), (.23,.23), (.23,-.23), (-.23,.23), (-.23,-.23))
    for name, anchor, bounds, limit in VIA_GROUPS:
        zones = sorted((z for z in board.Zones() if z.GetZoneName().startswith('TH_' + name)),
                       key=lambda z: z.GetLayer())
        assert len(zones) == 2 and all(z.IsFilled() for z in zones), name
        chosen = []
        for x, y in sorted(grid(bounds), key=lambda pt: dist(pt, anchor)):
            center = (x, y)
            if any(dist(center, existing) < .94 for existing in occupied):
                continue
            if any(pcb.ToMM(b.GetLeft())-.38 < x < pcb.ToMM(b.GetRight())+.38
                   and pcb.ToMM(b.GetTop())-.38 < y < pcb.ToMM(b.GetBottom())+.38 for b in obstacles):
                continue
            if not all(z.HitTestFilledArea(z.GetLayer(), point(x+dx, y+dy)) for z in zones for dx,dy in offsets):
                continue
            via(board, zones[0].GetNet(), center)
            occupied.append(center)
            chosen.append(center)
            if len(chosen) == limit:
                break
        print(name, anchor, len(chosen), chosen)
        assert len(chosen) >= 2, (name, anchor, chosen)
    assert pcb.SaveBoard(str(BOARD), board)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step', choices=('outline', 'stitch'))
    args = parser.parse_args()
    if args.step == 'outline':
        outline()
    else:
        stitch()
