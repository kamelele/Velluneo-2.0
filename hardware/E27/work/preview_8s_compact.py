"""Build a compact unrouted 8S-D3 study, retaining the Rev K power placement."""

import argparse

import pcbnew as pcb

import build as k
from preview_8s_d3 import CONNECTORS, DRAFT, build_board

FRONT = pcb.F_Cu
BACK = pcb.B_Cu
TARGET = DRAFT / "Rozmieszczenie_8S_D3_Kompakt.kicad_pcb"

# Approximate centres keep output, protection and logic in separate clusters.
GROUPS = (
    (("C14",), (135, 76), FRONT, 0),
    (("J2", "J3"), (142, 79), FRONT, 90),
    (("U2", "C11", "C13", "C12", "R14", "R15", "R16", "R17", "R18", "R19"), (135, 94), FRONT, 0),
    (("U101", "R24", "D10", "C15", "C17", "C21"), (132, 75), BACK, 0),
    (("U102", "R25", "R26", "R27", "R28", "R29", "R30", "R31", "R32", "C22"), (138, 86), BACK, 0),
    (("U103", "U106", "C23", "C24", "R38", "C18"), (132, 96), BACK, 0),
    (("U104", "U105", "U107", "U108", "R33", "R34", "R35", "R37", "C19", "C20", "C25", "C26", "C27"),
     (139, 100), BACK, 0),
)


def bounds(box):
    return tuple(pcb.ToMM(value) for value in (
        box.GetLeft(), box.GetTop(), box.GetRight(), box.GetBottom()
    ))


def footprint_bounds(item, layer):
    item.BuildCourtyardCaches()
    outline = item.GetCourtyard(layer)
    return bounds(outline.BBox() if outline.OutlineCount() else item.GetBoundingBox(False, False))


def conflicts(first, second):
    a, b, c, d = first
    e, f, g, h = second
    gap = 0.22
    return a < g + gap and c + gap > e and b < h + gap and d + gap > f


def place_remaining(board, pending, planned, nets, root_uuid, right):
    occupied = {FRONT: [], BACK: []}
    for item in board.GetFootprints():
        layer = item.GetLayer()
        occupied[layer].append(footprint_bounds(item, layer))
        opposite = BACK if layer == FRONT else FRONT
        for pad in item.Pads():
            if pad.IsOnLayer(opposite):
                occupied[opposite].append(bounds(pad.GetBoundingBox()))

    parts = {part.get("ref"): part for part in pending}
    assigned = set()
    for references, (cx, cy), layer, orientation in GROUPS:
        for ref in references:
            part = parts[ref]
            assigned.add(ref)
            identifier = CONNECTORS.get(ref) or part.findtext("footprint")
            item = k.footprint(board, DRAFT, identifier, ref, part.findtext("value"), 0, 0, 0,
                               part.findtext("tstamps"), root_uuid,
                               {pin: nets[net] for pin, net in planned[ref].items()})
            if layer == BACK:
                item.Flip(item.GetPosition(), pcb.FLIP_DIRECTION_LEFT_RIGHT)
            item.SetOrientationDegrees(orientation)
            left, top, stop, bottom = footprint_bounds(item, layer)
            xs = range(254, 2 * right)
            if ref in CONNECTORS:
                # Mating face points towards the short right-hand edge.
                xs = [int(2 * (right - 5))]
                cy = 88 if ref == "J2" else 99
                cx = right - 5
            candidates = ((x / 2, y / 2) for x in xs for y in range(141, 208))
            for x, y in sorted(candidates, key=lambda xy: (xy[0] - cx)**2 + (xy[1] - cy)**2):
                box = (x + left, y + top, x + stop, y + bottom)
                if box[0] < 126.5 or box[1] < 70.35 or box[2] > right - 0.35 or box[3] > 103.65:
                    continue
                if any(conflicts(box, prior) for prior in occupied[layer]):
                    continue
                item.SetPosition(k.pt(x, y))
                occupied[layer].append(box)
                break
            else:
                raise ValueError(f"{ref} does not fit at {right - 75} mm on {layer}")
    assert assigned == set(parts), set(parts) - assigned


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=70)
    args = parser.parse_args()
    build_board(target=TARGET, right_edge=75 + args.width, place_remaining=place_remaining)
