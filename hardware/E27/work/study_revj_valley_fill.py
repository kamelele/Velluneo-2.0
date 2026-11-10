"""Create the Rev J electrical and placement study from the routed Rev H reference."""
from dataclasses import replace
from itertools import product
from math import dist
from pathlib import Path
from shutil import copy2, copytree
import re

import pcbnew as p

import build as k
import power
import revf_power
import revh_power as revh
from revd_integrate import blocks, kind


NAME = 'Zasilacz_RevJ_Studium'
DEST = Path('outputs/Studium_RevJ_ValleyFill')
CAP = 'Capacitor_THT:CP_Radial_D6.3mm_P2.50mm'
HF = 'Capacitor_SMD:C_1210_3225Metric'
CHARGE = 'Resistor_SMD:R_2512_6332Metric'
COIL = 'E27:WE_PD2_HV_7850_Studium'
REPLACE = {'C1', 'C2', 'L1', 'R5'}
ADD = {'C17', 'C18', 'C19', 'D10', 'D11', 'D12', 'R24', 'R25', 'R26', 'R27'}


def devices():
    changed = {
        'C2': dict(val='3.3u / 400V', footprint=CAP, part='EGW2GM3R3E12OTG',
                   maker='AISHI', connection={1: 'P_BULK', 2: 'P_VF_A'}),
        'L1': dict(val='1.2mH / 400V', footprint=COIL, part='768775312', maker='Wurth'),
        'R6': dict(val='1.8M HV', part='CRCW20101M80JNEF', maker='Vishay'),
        'R7': dict(val='1.8M HV', part='CRCW20101M80JNEF', maker='Vishay'),
    }
    current = [replace(d, **changed[d.ref]) if d.ref in changed else d for d in revh.devices()]
    new = [
        ('C17', '3.3u / 400V', CAP, ('P_VF_B', 'P_0'), (40.64, 124.46), 'CP', 'EGW2GM3R3E12OTG'),
        ('D10', 'NRVUS1MFA', 'Diode_SMD:D_SOD-123F', ('P_VF_CH', 'P_VF_A'), (73.66, 124.46), 'D', 'NRVUS1MFA'),
        ('D11', 'NRVUS1MFA', 'Diode_SMD:D_SOD-123F', ('P_VF_A', 'P_0'), (107.95, 124.46), 'D', 'NRVUS1MFA'),
        ('D12', 'NRVUS1MFA', 'Diode_SMD:D_SOD-123F', ('P_BULK', 'P_VF_B'), (138.43, 124.46), 'D', 'NRVUS1MFA'),
        ('R24', '91R impulsowy', CHARGE, ('P_VF_CH', 'P_VF_RM'), (40.64, 139.70), 'R', 'HDSC2512-91RJT18'),
        ('R25', '91R impulsowy', CHARGE, ('P_VF_RM', 'P_VF_B'), (73.66, 139.70), 'R', 'HDSC2512-91RJT18'),
        ('R26', '1M HV', power.R12, ('P_BULK', 'P_VF_A'), (107.95, 139.70), 'R', 'RV1206FR-071ML'),
        ('R27', '1M HV', power.R12, ('P_VF_B', 'P_0'), (138.43, 139.70), 'R', 'RV1206FR-071ML'),
        ('C18', '150n / 630V', HF, ('P_BULK', 'P_0'), (40.64, 154.94), 'C', 'C3225X7T2J154K200AC'),
        ('C19', '100n / 630V (DNP)', HF, ('P_BULK', 'P_0'), (73.66, 154.94), 'C', 'C3225X7T2J104K160AE'),
    ]
    for ref, value, fp, nets, schematic, symbol, part in new:
        current.append(power.Device(ref, value, fp, dict(enumerate(nets, 1)), (0, 0), schematic, symbol, part=part))
    return current


def lib_files():
    DEST.mkdir(parents=True, exist_ok=True)
    copytree(revh.DEST / 'E27.pretty', DEST / 'E27.pretty', dirs_exist_ok=True)
    for file in revh.DEST.iterdir():
        if file.name.endswith('lib-table') or file.suffix in ('.kicad_sym', '.wrl'):
            copy2(file, DEST / file.name)
    for ext in ('pro', 'dru'):
        data = (revh.DEST / f'{revh.NAME}.kicad_{ext}').read_text(encoding='utf8')
        (DEST / f'{NAME}.kicad_{ext}').write_text(data.replace(revh.NAME, NAME), encoding='utf8')
    power.custom(DEST, COIL.split(':')[1], 'Wurth 7850 / provisional study land pattern',
                 8.0, 7.8, k.smd(1, -2.5, 0, 3.0, 2.0) + k.smd(2, 2.5, 0, 3.0, 2.0),
                 model=(4.9, '0.20 0.20 0.20'))


def placement(board):
    return {f.GetReference(): f for f in board.GetFootprints()}


def rect(box, margin=0):
    return (box.GetLeft() - margin, box.GetTop() - margin, box.GetRight() + margin, box.GetBottom() + margin)


def overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def place_near(board, fp, preferred, rotations):
    existing = [f for f in board.GetFootprints() if f.GetReference() != fp.GetReference()]
    layer = fp.GetLayer()
    other_side = p.B_Cu if layer == p.F_Cu else p.F_Cu
    outlines = [f.GetCourtyard(layer) for f in existing if f.GetLayer() == layer]
    outlines = [(c, rect(c.BBox())) for c in outlines if c.OutlineCount()]
    body_pads = [d for f in existing for d in f.Pads()]
    body_limits = [(d, rect(d.GetBoundingBox(), p.FromMM(.27))) for d in body_pads]
    opposite = [f.GetCourtyard(other_side) for f in existing if f.GetLayer() == other_side]
    opposite = [(c, rect(c.BBox())) for c in opposite if c.OutlineCount()]
    through = [(d, rect(d.GetBoundingBox())) for d in body_pads if d.HasHole()]
    options = [(x / 10, y / 10) for x, y in product(range(780, 1001, 2), range(720, 1031, 2))]
    for x, y in sorted(options, key=lambda xy: dist(xy, preferred)):
        fp.SetPosition(k.pt(x, y))
        for rotation in rotations:
            fp.SetOrientationDegrees(rotation)
            courtyard = fp.GetCourtyard(layer)
            limits = rect(courtyard.BBox())
            left, top, right, bottom = limits
            if left < 75.3e6 or top < 70.3e6 or right > 103e6 or bottom > 103.7e6:
                continue
            if any(overlap(limits, box) and courtyard.Collide(c, 0) for c, box in outlines):
                continue
            if any(overlap(limits, box) and courtyard.Collide(d.GetPosition(), p.FromMM(.75))
                   for d, box in through):
                continue
            lands = [(d, rect(d.GetBoundingBox())) for d in fp.Pads()]
            if any(overlap(box, limit)
                   for d, box in lands for pad, limit in body_limits
                   if any(d.IsOnLayer(l) and pad.IsOnLayer(l) for l in (p.F_Cu, p.B_Cu))):
                continue
            if any(overlap(box, limits) and c.Collide(d.GetPosition(), p.FromMM(.75))
                   for c, limits in opposite for d, box in lands if d.HasHole()):
                continue
            if max(d.GetBoundingBox().GetRight() for d in fp.Pads()) > 100.9e6:
                continue
            print(f'{fp.GetReference()}: {x:.2f}, {y:.2f}, {rotation} deg {"F" if layer==p.F_Cu else "B"}')
            return
    raise RuntimeError(f'No placement for {fp.GetReference()}')


def rebuild():
    lib_files()
    parts = devices()
    sheet, paths = revf_power.write_schematic(parts, destination=DEST, name=NAME, revision='J',
                                               dnp_refs=revh.DNP | {'C19'})
    sch = DEST / f'{NAME}.kicad_sch'
    sch.write_text(sch.read_text(encoding='utf8').replace('01   WEJŚCIE, PROSTOWNIK I FILTR',
                   '01   WEJŚCIE, PROSTOWNIK I VALLEY-FILL / STUDIUM'), encoding='utf8')
    source = (revh.DEST / f'{revh.NAME}.kicad_pcb').read_text(encoding='utf8')
    kept = []
    for item in blocks(source):
        tag = kind(item)
        if tag == 'footprint':
            ref = re.search(r'\(property "Reference" "([^"]+)"', item)[1]
            if ref in REPLACE:
                continue
        if tag in ('segment', 'via', 'zone') and '(net "/P_' in item:
            continue
        kept.append(item.replace('REV H MOC', 'REV J / STUDIUM') if tag == 'gr_text' else item)
    pcb = DEST / f'{NAME}.kicad_pcb'
    pcb.write_text('(kicad_pcb\n' + '\n'.join(kept) + '\n)\n', encoding='utf8')
    board = p.LoadBoard(str(pcb))
    footprints = placement(board)
    for net in sorted({n for d in parts for n in d.connection.values()}):
        if not board.FindNet('/' + net):
            board.Add(p.NETINFO_ITEM(board, '/' + net))
    preferred = {'L1': (84.7, 90.9), 'C17': (94.8, 89.7), 'C2': (91.4, 96.4),
                 'C1': (97.1, 71.8), 'R5': (95.6, 94.8), 'C18': (99.0, 84.7), 'D10': (85.5, 91), 'D11': (83.7, 96.7),
                 'D12': (97.0, 94.8), 'R24': (86.0, 100.7), 'R25': (85.4, 74.0),
                 'R26': (89.2, 102.2), 'R27': (98.0, 79.8), 'C19': (98.0, 88.5)}
    front = {'L1', 'C2', 'C17', 'C18', 'C19', 'D12'}
    for part in parts:
        if part.ref not in REPLACE | ADD:
            fp = footprints[part.ref]
            fp.SetPath(p.KIID_PATH(paths[part.ref]))
            fp.SetValue(part.val)
            continue
    for ref in preferred:
        part = next(d for d in parts if d.ref == ref)
        fp = k.footprint(board, DEST, part.footprint, ref, part.val, *preferred[ref], 0,
                         paths[ref].split('/')[-1], sheet,
                         {str(n): board.FindNet('/' + net) for n, net in part.connection.items()})
        if ref not in front:
            fp.Flip(fp.GetPosition(), p.FLIP_DIRECTION_LEFT_RIGHT)
        if ref == 'C19':
            fp.SetDNP(True)
        place_near(board, fp, preferred[ref], (0, 90, 180, 270))
    assert p.SaveBoard(str(pcb), board)


if __name__ == '__main__':
    rebuild()
