"""Apply the Rev G RCD candidate to the saved Rev F power board."""
from dataclasses import replace
from pathlib import Path
import re
from shutil import copy2

import pcbnew as pcb

import build as k
import revf_power as revf
from revd_integrate import blocks, kind


NAME = 'Zasilacz_RevG_Moc'
DEST = Path('outputs') / NAME
CAP = 'Capacitor_SMD:C_1206_3216Metric'
RESISTOR = 'SR1206JR-7W82KL'
PART_CODES = {'C3': 'C342846', 'D5': 'C99333', 'R4': 'C7319643', 'R22': 'C7319643'}


def devices():
    replacements = {
        'C3': dict(val='2.2n / 630V', footprint=CAP, part='C3216C0G2J222JT000N', notes='C0G'),
        'D5': dict(val='US1M', part='US1M-13-F'),
        'R4': dict(val='82k / 0.5W', connection={1: 'P_CL', 2: 'P_CLMID'}, part=RESISTOR, maker='YAGEO'),
    }
    parts = [replace(d, **replacements[d.ref]) if d.ref in replacements else d for d in revf.devices()]
    r4 = next(d for d in parts if d.ref == 'R4')
    r22 = replace(r4, ref='R22', connection={1: 'P_CLMID', 2: 'P_BULK'}, schematic=(213.36, 73.66))
    return [*parts, r22]


def point(vector):
    return pcb.ToMM(vector.x), pcb.ToMM(vector.y)


def footprint(board, parts, ref, xy, rotation):
    part = parts[ref]
    fp = k.footprint(board, DEST, part.footprint, ref, part.val, *xy, rotation, '0'*32, '0'*32,
                     {str(i): board.FindNet('/' + net) for i, net in part.connection.items()})
    fp.Flip(fp.GetPosition(), pcb.FLIP_DIRECTION_LEFT_RIGHT)
    fp.SetOrientationDegrees(rotation)
    return fp


def adapt_board(parts, paths):
    # Remove the old taps feeding R4 and C3. Keep the P_BULK run from
    # the front capacitor to the primary supply via the lower branch.
    remove_bulk = {
        frozenset(((90.9375, 89.65), (90.9, 89.7))),
        frozenset(((90.9, 89.7), (90.9, 89.8))),
        frozenset(((90.9, 89.8), (90.0, 90.7))),
        frozenset(((90.0, 90.7), (90.0, 90.9))),
        frozenset(((90.0, 90.9), (89.9, 91.0))),
        frozenset(((89.9, 91.0), (89.9, 91.3))),
        frozenset(((89.9, 91.3), (86.7, 94.5))),
        frozenset(((90.9, 89.7), (92.6, 91.4))),
        frozenset(((92.6, 91.4), (92.9, 91.4))),
        frozenset(((92.9, 91.4), (93.9, 92.4))),
        frozenset(((93.9, 92.4), (94.2, 92.4))),
        frozenset(((94.25, 92.4), (94.2, 92.4))),
    }
    remove_cl = {
        frozenset(((96.15, 92.4), (96.2, 92.4))),
        frozenset(((96.2, 92.4), (95.2, 91.4))),
    }
    original = (revf.DEST / f'{revf.NAME}.kicad_pcb').read_text(encoding='utf8')
    kept = []
    for item in blocks(original):
        tag = kind(item)
        if tag == 'footprint' and '(property "Reference" "C3"' in item:
            continue
        if tag == 'segment' and '(layer "B.Cu")' in item:
            points = frozenset(tuple(map(float, xy)) for xy in re.findall(
                r'\((?:start|end) ([\d.]+) ([\d.]+)\)', item))
            if ('(net "/P_BULK")' in item and points in remove_bulk) or (
                    '(net "/P_CL")' in item and points in remove_cl):
                continue
        if tag == 'footprint' and '(property "Reference" "BR1"' in item:
            item = re.sub(r'\(model "[^"]+OnSemi_751EP[^"]+"', '(model "${KIPRJMOD}/MB10S_751EP.wrl"', item)
        kept.append(item.replace('"E27 / REV F MOC"', '"E27 / REV G MOC"') if tag == 'gr_text' else item)
    target = DEST / f'{NAME}.kicad_pcb'
    target.write_text('(kicad_pcb\n' + '\n'.join(kept) + '\n)\n', encoding='utf8')

    board = pcb.LoadBoard(str(target))
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    midpoint = pcb.NETINFO_ITEM(board, '/P_CLMID')
    board.Add(midpoint)
    fps['C3'] = footprint(board, parts, 'C3', (94.05, 92.35), 180)
    fps['R22'] = footprint(board, parts, 'R22', (89.4, 93.2), 270)
    fps['R4'].FindPadByNumber('2').SetNet(midpoint)
    for ref, fp in fps.items():
        fp.SetPath(pcb.KIID_PATH(paths[ref]))
        fp.SetValue(parts[ref].val)

    def pad(ref, n):
        return point(fps[ref].FindPadByNumber(n).GetPosition())

    def route(net, points, width):
        k.track(board, board.FindNet('/' + net), points, width, pcb.B_Cu)

    route('P_CLMID', [pad('R4', '2'), (90.9375, 90.2), pad('R22', '1')], .25)
    x, y = pad('R22', '2')
    route('P_BULK', [(86.7, 94.5), (x, 94.5), (90.7, 94.5)], .34)
    route('P_BULK', [(x, 94.5), (x, y)], .34)
    x, y = pad('C3', '2')
    route('P_BULK', [(94.2, 92.4), (x + .05, 92.4), (x, y)], .29)
    x, y = pad('C3', '1')
    route('P_CL', [(95.2, 91.4), (x, y)], .29)

    assert pcb.SaveBoard(str(target), board)


if __name__ == '__main__':
    DEST.mkdir(parents=True, exist_ok=True)
    for source in revf.DEST.iterdir():
        if source.is_dir() and source.name == 'E27.pretty':
            (DEST / source.name).mkdir(exist_ok=True)
            for footprint_path in source.iterdir():
                copy2(footprint_path, DEST / source.name / footprint_path.name)
        elif source.suffix in ('.wrl', '.kicad_sym') or source.name.endswith('lib-table'):
            copy2(source, DEST / source.name)
    for ext in ('pro', 'dru'):
        data = (revf.DEST / f'{revf.NAME}.kicad_{ext}').read_text(encoding='utf8').replace(revf.NAME, NAME)
        if ext == 'dru':
            data = data.replace("A.NetName == '/P_CL'", "A.NetName =~ '/P_CL*'")
            data = data.replace("B.NetName == '/P_CL'", "B.NetName =~ '/P_CL*'")
        (DEST / f'{NAME}.kicad_{ext}').write_text(data, encoding='utf8')
    copy2(revf.E / 'MB10S_751EP.wrl', DEST / 'MB10S_751EP.wrl')
    parts = devices()
    _, paths = revf.write_schematic(parts, destination=DEST, name=NAME, revision='G')
    adapt_board({part.ref: part for part in parts}, paths)
