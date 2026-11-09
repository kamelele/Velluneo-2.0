"""Generate the Rev C mechanical-only KiCad drawing and its SVG preview."""
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import pcbnew as pcb


@dataclass(frozen=True)
class Block:
    label: str
    x: float
    y: float
    w: float
    d: float
    h: float
    reserved: bool = False


WIDTH, DEPTH, THICKNESS = 64, 39, 1.6
BARRIER, BAND = 34.15, 8.2
TOP = (
    Block('RV1', 0.8, 1.0, 20.6, 18.4, 9.0),
    Block('C2', 0.8, 21.0, 20.7, 11.8, 12.0),
    Block('T1 EFD20', 22.0, 7.5, 24.3, 22.0, 10.5),
    Block('CY1', 27.65, 0.8, 13.0, 5.8, 11.0),
    Block('L1', 22.1, 30.2, 8.4, 8.4, 10.0),
    Block('C6A', 47.2, 1.3, 10.8, 10.8, 10.5),
    Block('C6B', 47.2, 12.9, 10.8, 10.8, 10.5),
    Block('D7', 47.2, 24.5, 7.6, 5.7, 2.5),
    Block('J1', 1.0, 34.0, 8.0, 3.2, 0, True),
    Block('J2', 60.0, 1.3, 3.2, 10.2, 0, True),
    Block('J3', 60.0, 29.0, 3.2, 7.7, 0, True),
)
BOTTOM = (
    Block('F1', 1.3, 1.3, 18.4, 5.9, 5.35),
    Block('R1', 0.8, 9.1, 18.3, 5.5, 5.0),
    Block('BR1', 1.3, 16.2, 6.2, 5.2, 2.8),
    Block('U1', 27.15, 16.5, 14.0, 9.9, 2.65),
    Block('U2', 48.0, 3.6, 7.8, 5.6, 1.2),
    Block('U3', 48.0, 24.5, 5.85, 3.6, 1.1),
    Block('U4', 48.0, 29.2, 5.85, 3.6, 1.1),
    Block('RV1 PTH', 19.45, 8.0, 2.2, 9.0, 0, True),
    Block('C2 PTH', 18.8, 22.5, 2.6, 8.8, 0, True),
    Block('T1 PTH', 24.25, 9.0, 2.7, 19.0, 0, True),
    Block('T1 PTH', 41.4, 9.0, 2.7, 19.0, 0, True),
    Block('CY1 PTH', 27.65, 0.8, 13.0, 5.8, 0, True),
    Block('L1 PTH', 22.1, 30.2, 8.4, 8.4, 0, True),
) + tuple(b for b in TOP if b.reserved)


def validate(blocks):
    for b in blocks:
        assert 0 <= b.x < b.x + b.w <= WIDTH and 0 <= b.y < b.y + b.d <= DEPTH, b
    for a, b in combinations(blocks, 2):
        separated = (a.x + a.w <= b.x or b.x + b.w <= a.x
                     or a.y + a.d <= b.y or b.y + b.d <= a.y)
        assert separated, (a, b)


def vec(x, y):
    return pcb.VECTOR2I(pcb.FromMM(x + 80), pcb.FromMM(y + 60))


def rect(board, x, y, w, d, layer):
    item = pcb.PCB_SHAPE()
    item.SetShape(pcb.SHAPE_T_RECT)
    item.SetStart(vec(x, y))
    item.SetEnd(vec(x + w, y + d))
    item.SetLayer(layer)
    item.SetWidth(pcb.FromMM(.15))
    board.Add(item)


def label(board, value, x, y, layer, size=.85):
    item = pcb.PCB_TEXT(board)
    item.SetText(value)
    item.SetPosition(vec(x, y))
    item.SetLayer(layer)
    item.SetTextSize(pcb.VECTOR2I(pcb.FromMM(size), pcb.FromMM(size)))
    item.SetTextThickness(pcb.FromMM(.14))
    board.Add(item)


def make_kicad(path):
    board = pcb.BOARD()
    board.GetDesignSettings().SetBoardThickness(pcb.FromMM(THICKNESS))
    rect(board, 0, 0, WIDTH, DEPTH, pcb.Edge_Cuts)
    rect(board, BARRIER - BAND / 2, 0, BAND, DEPTH, pcb.Dwgs_User)
    label(board, '64 x 39 mm | MODEL MECHANICZNY | BEZ MIEDZI', 32, -3.0, pcb.Dwgs_User, 1.1)
    for blocks, layer in ((TOP, pcb.F_Fab), (BOTTOM, pcb.B_Fab)):
        for b in blocks:
            rect(board, b.x, b.y, b.w, b.d, layer)
            label(board, b.label, b.x + b.w / 2, b.y + b.d / 2, layer)
    assert not board.GetTracks() and not board.GetFootprints()
    pcb.SaveBoard(str(path), board)


def make_svg(path):
    lines = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 330" role="img">',
             '<title>Model gabarytowy zasilacza E27 Rev C</title>',
             '<rect width="760" height="330" fill="#f3f6f8"/>',
             '<g font-family="Segoe UI,Arial,sans-serif" fill="#162f3a">',
             '<text x="24" y="32" font-size="23" font-weight="bold">E27 Rev C · Model gabarytowy</text>',
             '<text x="24" y="55" font-size="13">PCB 64 × 39 mm · obie strony we wspólnym rzucie XY</text>']
    scale = 5.35
    for title, blocks, ox in (('Góra', TOP, 24), ('Dół', BOTTOM, 392)):
        oy = 95
        lines.extend([f'<text x="{ox}" y="86" font-size="15" font-weight="bold">{title}</text>',
                      f'<rect x="{ox}" y="{oy}" width="{WIDTH*scale}" height="{DEPTH*scale}" fill="white" stroke="#78919b"/>',
                      f'<rect x="{ox+(BARRIER-BAND/2)*scale}" y="{oy}" width="{BAND*scale}" height="{DEPTH*scale}" fill="#efe7bd"/>'])
        for b in blocks:
            x, y, w, d = (ox + b.x*scale, oy + b.y*scale, b.w*scale, b.d*scale)
            fill, stroke = ('#edf0f2', '#6c8391') if b.reserved else ('#c6e6e2', '#36706c')
            lines.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{d:.2f}" fill="{fill}" stroke="{stroke}"/>')
            size = 7 if b.w < 4 else 10
            if b.w < 4:
                lines.append(f'<text transform="translate({x+w/2:.2f} {y+d/2:.2f}) rotate(-90)" font-size="{size}" text-anchor="middle" dominant-baseline="middle">{b.label}</text>')
            else:
                lines.append(f'<text x="{x+w/2:.2f}" y="{y+d/2+3:.2f}" font-size="{size}" text-anchor="middle">{b.label}</text>')
    lines.extend(['<text x="24" y="320" font-size="12">Żółty · rezerwa 8,2 mm na izolację. Szary · rezerwy na wyprowadzenia i przewody.</text>', '</g></svg>'])
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    validate(TOP)
    validate(BOTTOM)
    out = Path('outputs/Studium_RevC')
    out.mkdir(parents=True, exist_ok=True)
    make_kicad(out / 'E27_RevC_Gabaryty.kicad_pcb')
    make_svg(out / 'E27_RevC_Gabaryty.svg')
    height = max(b.h for b in TOP) + THICKNESS + max(b.h for b in BOTTOM)
    print(f'{WIDTH} × {DEPTH} × {height:.2f} mm. Checked {len(TOP)+len(BOTTOM)} mechanical envelopes.')
