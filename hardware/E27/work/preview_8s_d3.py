"""Build the unrouted 8S-D3 placement study from the current KiCad export."""

from pathlib import Path
import re
from xml.etree import ElementTree

import pcbnew as pcb

import build as k

ROOT = Path("outputs")
DRAFT = ROOT / "Zasilacz_8S_Draft"
POWER = ROOT / "Zasilacz_RevK_Moc"
CONTROL = ROOT / "Zasilacz_RevH_Sterowanie"
TARGET = DRAFT / "Rozmieszczenie_8S_D3.kicad_pcb"
EXPORT = Path("workflow/8s/.work/rev8s-draft.xml")
CONNECTORS = {
    "J2": "Connector_JST:JST_GH_SM04B-GHS-TB_1x04-1MP_P1.25mm_Horizontal",
    "J3": "Connector_JST:JST_GH_SM02B-GHS-TB_1x02-1MP_P1.25mm_Horizontal",
}
# PCB origin in millimetres, orientation, back side.
PLACEMENT = {
    "C14": (137.4, 77, 0, False),
    "U2": (151, 75.6, 0, False),
    "J2": (154, 85.6, 90, False),
    "J3": (154, 97.7, 90, False),
    "U101": (125.5, 76.5, 0, True),
    "U102": (133, 76.5, 0, True),
    "U103": (142, 76.5, 0, True),
    "U106": (151, 76.5, 0, True),
    "U104": (132, 83.5, 0, True),
    "U105": (139, 83.5, 0, True),
    "U107": (146, 83.5, 0, True),
    "U108": (153, 83.5, 0, True),
    "R24": (130, 86, 0, False),
    "D10": (135, 86, 0, False),
    "C17": (140, 86, 0, False),
    "C11": (147.5, 80, 0, False),
    "C13": (146, 84.6, 0, False),
}
SIDE_SLOTS = {
    False: [(x, y, 0, False) for y in (90.5, 94, 97.5, 101) for x in (132.5, 137.3, 142.1, 146.9)],
    True: [(x, y, 0, True) for y in (86.7, 89.3, 91.9, 94.5, 97.1, 99.7, 102)
           for x in (131.8, 137.0, 142.2, 147.4, 152.6)],
}


def build_board(*, target=TARGET, right_edge=159, place_remaining=None):
    schematic = (DRAFT / "Zasilacz_8S_Draft.kicad_sch").resolve()
    data = ElementTree.parse(EXPORT)
    assert Path(data.findtext("./design/source")).resolve() == schematic
    assert data.findtext("./design/sheet/title_block/rev") == "8S-D3"
    root_uuid = re.search(r'\(uuid "([^"]+)"\)', schematic.read_text(encoding="utf-8"))[1]
    base = pcb.LoadBoard(str(POWER / "Zasilacz_RevK_Moc.kicad_pcb"))
    previous = {item.GetReference(): item for item in base.GetFootprints()}
    board = pcb.BOARD()
    board.SetCopperLayerCount(2)
    board.GetDesignSettings().SetBoardThickness(pcb.FromMM(1.6))
    vertices = [(75, 70), (right_edge, 70), (right_edge, 104), (75, 104), (75, 70)]
    for start, end in zip(vertices, vertices[1:]):
        k.shape(board, pcb.Edge_Cuts, start, end)

    pin_nets = {}
    for net in data.findall("./nets/net"):
        for pin in net.findall("node"):
            if "no_connect" not in pin.get("pintype", "").split("+"):
                pin_nets.setdefault(pin.get("ref"), {})[pin.get("pin")] = net.get("name").lstrip("/")
    nets = k.nets_for(board, (net for pins in pin_nets.values() for net in pins.values()))
    front = iter(SIDE_SLOTS[False])
    back = iter(SIDE_SLOTS[True])
    pending = []
    for part in data.findall("./components/comp"):
        ref = part.get("ref")
        if place_remaining is not None:
            if ref not in previous:
                pending.append(part)
                continue
        if place_remaining is None and ref in PLACEMENT:
            x, y, angle, flipped = PLACEMENT[ref]
        elif ref in previous:
            former = previous[ref]
            position = former.GetPosition()
            x, y = pcb.ToMM(position.x), pcb.ToMM(position.y)
            angle, flipped = former.GetOrientationDegrees(), former.GetLayer() == pcb.B_Cu
        else:
            slot = next(front, None) if ref.startswith("R") else None
            x, y, angle, flipped = slot or next(back)
        name = CONNECTORS.get(ref) or part.findtext("footprint")
        assert name, ref
        mapping = {pin: nets[net] for pin, net in pin_nets.get(ref, {}).items()}
        item = k.footprint(board, DRAFT, name, ref, part.findtext("value"), x, y, 0,
                           part.findtext("tstamps"), root_uuid,
                           mapping)
        if flipped:
            item.Flip(item.GetPosition(), pcb.FLIP_DIRECTION_LEFT_RIGHT)
        item.SetOrientationDegrees(angle)
        item.SetDNP(part.find("property[@name='dnp']") is not None)
        assert {pin for pin in mapping} <= {pad.GetNumber() for pad in item.Pads()}, ref

    if place_remaining is not None:
        place_remaining(board, pending, pin_nets, nets, root_uuid, right_edge)
    assert pcb.SaveBoard(str(target), board)
    contents = target.read_text(encoding="utf-8")
    for directory in (POWER, CONTROL):
        for model in directory.glob("*.wrl"):
            contents = contents.replace(f'${{KIPRJMOD}}/{model.name}',
                                        f'${{KIPRJMOD}}/../{directory.name}/{model.name}')
    assert not re.search(r'\$\{KIPRJMOD\}/[^/]+\.wrl', contents)
    target.write_text(contents, encoding="utf-8", newline="\n")
    saved = pcb.LoadBoard(str(target))
    assert not list(saved.GetTracks())
    assert len(list(saved.GetFootprints())) == len(data.findall("./components/comp"))
    for fp in saved.GetFootprints():
        connected = {pad.GetNumber(): pad.GetNetname().lstrip("/")
                     for pad in fp.Pads() if pad.GetNetCode() > 0}
        assert connected == pin_nets.get(fp.GetReference(), {}), fp.GetReference()
    print(f"{len(list(saved.GetFootprints()))} footprints, {right_edge - 75} x 34 mm, unrouted")


if __name__ == "__main__":
    build_board()
