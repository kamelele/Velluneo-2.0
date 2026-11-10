"""Add an unpopulated D7 damping network to the routed Rev G power board."""
from dataclasses import replace
from pathlib import Path
from shutil import copy2, copytree

import pcbnew as p

import build as k
import power
import revf_power as revf
import revg_power as revg


NAME = 'Zasilacz_RevH_Moc'
DEST = Path('outputs') / NAME
DNP_FOOTPRINTS = {'C16': (revg.CAP, 'C_RC_1206_Hand'), 'R23': (power.R80, 'R_RC_0805_Hand')}
DNP = set(DNP_FOOTPRINTS)
PART_CODES = revg.PART_CODES | {'C2': 'C473172', 'D6': 'C154734', 'R8': 'C114541',
                               'R9': 'C4000855', 'C9': 'C508852', 'C7': 'C2179181'}


def devices():
    sourcing = {
        'R8': dict(part='RC0805FR-0747RL', maker='YAGEO'),
        'R9': dict(part='ERJ-6DSFR11V', maker='Panasonic'),
        'C9': dict(part='C3216X7R1E225K160AE', maker='TDK'),
        'C7': dict(val='68p / 250V', part='GQM1875C2E680GB12D', maker='Murata'),
    }
    parts = [replace(d, **sourcing[d.ref]) if d.ref in sourcing else d for d in revg.devices()]
    parts += [
        power.Device('C16', 'C_RC (DNP)', 'E27:C_RC_1206_Hand', {1: 'S_SW', 2: 'S_DAMP'}, (119.95, 88.10), (288.29, 125.73), 'C', 90),
        power.Device('R23', 'R_RC (DNP)', 'E27:R_RC_0805_Hand', {1: 'S_DAMP', 2: 'S_GND'}, (123.3, 85.8), (328.93, 125.73), 'R', 0),
    ]
    return parts


def rebuild():
    DEST.mkdir(parents=True, exist_ok=True)
    copytree(revg.DEST / 'E27.pretty', DEST / 'E27.pretty', dirs_exist_ok=True)
    for source in revg.DEST.iterdir():
        if source.suffix in ('.wrl', '.kicad_sym') or source.name.endswith('lib-table'):
            copy2(source, DEST / source.name)
    for ext in ('pro', 'dru', 'pcb'):
        data = (revg.DEST / f'{revg.NAME}.kicad_{ext}').read_text(encoding='utf8')
        (DEST / f'{NAME}.kicad_{ext}').write_text(data.replace(revg.NAME, NAME).replace('REV G MOC', 'REV H MOC'), encoding='utf8')
    for standard, name in DNP_FOOTPRINTS.values():
        library, footprint = standard.split(':')
        data = (k.LIB / f'{library}.pretty' / f'{footprint}.kicad_mod').read_text(encoding='utf8')
        data = data.replace(f'"{footprint}"', f'"{name}"').replace(' "F.Paste"', '')
        (DEST / 'E27.pretty' / f'{name}.kicad_mod').write_text(data, encoding='utf8')
    parts = devices()
    sheet, paths = revf.write_schematic(parts, destination=DEST, name=NAME, revision='H', dnp_refs=DNP)
    path = DEST / f'{NAME}.kicad_pcb'
    board = p.LoadBoard(str(path))
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    damp = p.NETINFO_ITEM(board, '/S_DAMP')
    board.Add(damp)
    for part in parts:
        if part.ref in DNP:
            fps[part.ref] = k.footprint(board, DEST, part.footprint, part.ref, part.val, *part.xy, part.rot,
                                       paths[part.ref].split('/')[-1], sheet,
                                       {str(n): board.FindNet('/' + net) for n, net in part.connection.items()})
            fps[part.ref].SetDNP(True)
        else:
            fps[part.ref].SetPath(p.KIID_PATH(paths[part.ref]))
            fps[part.ref].SetValue(part.val)

    def pad(ref, n):
        return revg.point(fps[ref].FindPadByNumber(n).GetPosition())

    def route(net, points):
        k.track(board, board.FindNet('/' + net), points, .29, p.F_Cu)

    x, y = pad('C16', '1')
    route('S_SW', [pad('D7', '1'), (117.8, 90.4), (117.8 + 90.4 - y, y), (x, y)])
    x, y = pad('C16', '2')
    end_x, end_y = pad('R23', '1')
    route('S_DAMP', [(x, y), (x + y - end_y, end_y), (end_x, end_y)])
    x, y = pad('R23', '2')
    route('S_GND', [(116.6, 84.5), (x - (y - 84.5), 84.5), (x, y)])
    assert p.SaveBoard(str(path), board)


if __name__ == '__main__':
    rebuild()
