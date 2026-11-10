"""Shorten routed copper without moving pads, vias, branches, or width transitions."""

import argparse
from collections import defaultdict
from math import hypot
from pathlib import Path

from uuid import uuid4
import re

import pcbnew as pcb

from revd_integrate import blocks, kind


def xy(point):
    return point.x, point.y


def shape(a, b, width):
    return pcb.SHAPE_SEGMENT(pcb.SEG(pcb.VECTOR2I(*a), pcb.VECTOR2I(*b)), width)


def length(path):
    return sum(hypot(b[0]-a[0], b[1]-a[1]) for a, b in zip(path, path[1:]))


def octilinear(path):
    return all(a[0] == b[0] or a[1] == b[1] or abs(a[0]-b[0]) == abs(a[1]-b[1])
               for a, b in zip(path, path[1:]))


def direct_paths(a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    diag = min(abs(dx), abs(dy))
    if not diag or abs(dx) == abs(dy):
        yield [a, b]
        return
    sx, sy = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
    axis_x, axis_y = abs(dx)-diag, abs(dy)-diag
    for first in (0, 4, 2, 1, 3):
        x = a[0] + sx * (axis_x * first // 4)
        y = a[1] + sy * (axis_y * first // 4)
        yield list(dict.fromkeys((a, (x, y), (x + sx*diag, y + sy*diag), b)))


def tracks(board):
    return [t for t in board.GetTracks() if type(t) is pcb.PCB_TRACK]


def chains(board):
    groups = defaultdict(list)
    joins = defaultdict(set)
    for t in tracks(board):
        key = t.GetLayer(), t.GetNetname(), t.GetWidth()
        groups[key].append(t)
        for pt in (t.GetStart(), t.GetEnd()):
            joins[key[:2], xy(pt)].add(key[2])

    for layer_net_width, items in groups.items():
        layer, net, _ = layer_net_width
        links = defaultdict(list)
        ends = [(xy(t.GetStart()), xy(t.GetEnd())) for t in items]
        for i, (a, b) in enumerate(ends):
            links[a].append(i)
            links[b].append(i)

        def boundary(pt):
            if len(links[pt]) != 2 or len(joins[(layer, net), pt]) != 1:
                return True
            point = pcb.VECTOR2I(*pt)
            return any(s.Collide(point) for s in anchors[layer, net])

        anchors = defaultdict(list)
        for fp in board.GetFootprints():
            for pad in fp.Pads():
                if pad.GetNetname() == net and pad.IsOnLayer(layer):
                    anchors[layer, net].append(pad.GetEffectiveShape(layer))
        for t in board.GetTracks():
            if type(t) is not pcb.PCB_TRACK and t.GetNetname() == net and t.IsOnLayer(layer):
                anchors[layer, net].append(t.GetEffectiveShape(layer))

        visited = set()
        for pt in links:
            if not boundary(pt):
                continue
            for start in links[pt]:
                route = []
                points = [pt]
                edge = start
                while edge not in visited:
                    visited.add(edge)
                    a, b = ends[edge]
                    points.append(b if points[-1] == a else a)
                    route.append(items[edge])
                    if boundary(points[-1]):
                        break
                    edge = next(i for i in links[points[-1]] if i != edge)
                if route and points[-1] != points[0]:
                    yield layer_net_width, points, route


def power_gap(a, b):
    """Mirror copper spacing of the power-board rules for early path screening."""
    if a and b and not (a.startswith("unconnected-") or b.startswith("unconnected-")):
        if a.startswith("/P_") != b.startswith("/P_"):
            return 8000000
    if all(n == "/P_N" or n.startswith("/P_L") for n in (a, b)):
        return 1500000
    if "/P_0" in (a, b):
        other = b if a == "/P_0" else a
        if other in ("/P_D", "/P_BULK", "/P_BR") or other.startswith(("/P_CL", "/P_VF_")):
            return 1100000
    return 0


class Copper:
    def __init__(self, board, gap, power):
        self.gap = gap
        self.power = power
        self.edge = board.GetBoardEdgesBoundingBox()
        self.by_layer = defaultdict(list)
        layers = [l for l in board.GetEnabledLayers().Seq() if pcb.IsCopperLayer(l)]
        for item in [*board.GetTracks(), *(pad for fp in board.GetFootprints() for pad in fp.Pads())]:
            for layer in layers:
                if not item.IsOnLayer(layer):
                    continue
                geometry = item.GetEffectiveShape(layer)
                bounds = geometry.BBox()
                self.by_layer[layer].append((item.GetNetname(), geometry, bounds))

    def allows(self, layer, net, path, width):
        for a, b in zip(path, path[1:]):
            copper = shape(a, b, width)
            if not self.edge.Contains(copper.BBox(self.gap)):
                return False
            box = copper.BBox(8000000 if self.power else self.gap)
            for other_net, other, other_box in self.by_layer[layer]:
                if other_net == net or not box.Intersects(other_box):
                    continue
                gap = max(self.gap, power_gap(net, other_net)) if self.power else self.gap
                if copper.BBox(gap).Intersects(other_box) and copper.Collide(other, gap):
                    return False
        return True

    def add(self, layer, net, path, width):
        for a, b in zip(path, path[1:]):
            geometry = shape(a, b, width)
            self.by_layer[layer].append((net, geometry, geometry.BBox()))


def simplify(points, layer, net, width, copper):
    # Work from the longest plausible span. Keep existing escapes where clearance is tight.
    i = 0
    result = [points[0]]
    while i < len(points)-1:
        for j in range(len(points)-1, i, -1):
            old = points[i:j+1]
            best = next((p for p in direct_paths(points[i], points[j])
                         if (len(p) < len(old) or
                             (len(p) == len(old) and (not octilinear(old) or length(old)-length(p) > 20000)))
                         and copper.allows(layer, net, p, width)), None)
            if best:
                result.extend(best[1:])
                i = j
                break
        else:
            i += 1
            result.append(points[i])
    return result


def optimize(source, output, gap, power):
    board = pcb.LoadBoard(str(source))
    copper = Copper(board, gap, power)
    edits = []
    for (layer, net, width), points, items in sorted(chains(board), key=lambda entry: -len(entry[2])):
        if power and net in {"/P_D", "/P_BULK", "/P_CL", "/P_CLMID", "/S_SW", "/S_DAMP"}:
            continue
        result = simplify(points, layer, net, width, copper)
        if result != points:
            copper.add(layer, net, result, width)
            edits.append((items, result))
    removed = {t.m_Uuid.AsString() for items, _ in edits for t in items}
    original = source.read_text(encoding="utf8")
    entries = [b for b in blocks(original)
               if kind(b) != "segment" or re.search(r'\(uuid "([^"]+)"\)', b)[1] not in removed]
    for items, path in edits:
        ref = items[0]
        layer, width, net = ref.GetLayerName(), ref.GetWidth()/1e6, ref.GetNetname()
        for a, b in zip(path, path[1:]):
            ax, ay, bx, by = (i/1e6 for i in (*a, *b))
            entries.append(f'(segment (start {ax:.6f} {ay:.6f}) (end {bx:.6f} {by:.6f}) '
                           f'(width {width:.6f}) (layer "{layer}") (net "{net}") (uuid "{uuid4()}"))')
    output.write_text("(kicad_pcb\n" + "\n".join(entries) + "\n)\n", encoding="utf8")
    print(f"{len(edits)} chains simplified")


def stats(path):
    board = pcb.LoadBoard(str(path))
    segments = tracks(board)
    print(path.name, len(segments), "segments,",
          round(sum(t.GetLength() for t in segments)/1e6, 2), "mm,",
          sum(not octilinear((xy(t.GetStart()), xy(t.GetEnd()))) for t in segments), "off angle,",
          sum(t.GetLength() < 200000 for t in segments), "shorter than 0.2 mm,",
          sum(isinstance(t, pcb.PCB_VIA) for t in board.GetTracks()), "vias")


if __name__ == "__main__":
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("source", type=Path)
    args.add_argument("output", type=Path, nargs="?")
    args.add_argument("--gap", type=float, default=.21)
    args.add_argument("--power", action="store_true")
    a = args.parse_args()
    stats(a.source)
    if a.output:
        optimize(a.source, a.output, pcb.FromMM(a.gap), a.power)
