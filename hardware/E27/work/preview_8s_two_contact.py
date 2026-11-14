"""Place unconnected footprint candidates on the saved compact D4 outline."""
from pathlib import Path

import pcbnew as pcb

import build as k
from preview_8s_compact import BACK, FRONT, bounds, conflicts, footprint_bounds

SOURCE = Path("outputs/Zasilacz_8S_D4/Zasilacz_8S_D4.kicad_pcb")
DEST = Path("outputs/Zasilacz_8S_D5_Studium")

REMOVED = {
    "J2", "C14", "R17", "R18", "R24", "D10", "U103", "U104", "U105", "U106",
    "U107", "U108", "R33", "R34", "R35", "R37", "R38", "C18", "C19", "C20",
    "C23", "C24", "C25", "C26", "C27", "R25", "R26", "R27", "R28", "R29",
    "R30", "R31", "R32",
}
R0603 = "Resistor_SMD:R_0603_1608Metric"
R1206 = "Resistor_SMD:R_1206_3216Metric"
SOT23 = "Package_TO_SOT_SMD:SOT-23"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
SOIC14 = "Package_SO:SOIC-14_3.9x8.7mm_P1.27mm"

GROUPS = (
    (FRONT, (137, 76), (
        ("U110", "ATtiny404", SOIC14),
    )),
    (FRONT, (138, 84), (
        ("Q101", "Probe pass switch", SOT23), ("R101", "1.1k probe A", R1206),
        ("R102", "1.1k probe B", R1206), ("Q102", "Probe level shift", SOT23),
        ("R103", "Probe gate pull-up", R0603), ("R104", "Probe gate feed", R0603),
        ("R105", "Probe enable pull-down", R0603), ("ZD101", "Probe gate clamp", "Diode_SMD:D_SOD-323"),
    )),
    (BACK, (137, 79), ( ("C103", "Logic bypass", C0603),
        ("J101", "UPDI test pads", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical_SMD_Pin1Left"),
        ("R109", "Logic gate feed", R0603), ("R110", "SHDN pull-down", R0603),
        ("R111", "RAW divider high", R0603), ("R112", "RAW divider low", R0603),
        ("C104", "RAW divider filter", C0603),
    )),
    (BACK, (136, 99), (
        ("U111", "INA181A1 load current", "Package_TO_SOT_SMD:SOT-23-6"),
        ("R106", "0.22R load shunt", R1206), ("C101", "Current monitor bypass", C0603),
        ("R107", "Contact divider high", R0603), ("R108", "Contact divider low", R0603),
        ("C102", "Contact divider filter", C0603),
    )),
    (BACK, (138, 89), (
        ("U112", "Probe hardware timeout reserve", "Package_TO_SOT_SMD:SOT-23-6"),
        ("R113", "Timeout scale", R0603), ("C105", "Timeout scale", C0603),
        ("Q103", "Bleeder switch", SOT23), ("R114", "Bleeder gate default", R0603),
        ("R115", "Bleeder control", R0603), ("TH101", "Board thermistor", R0603),
        ("R116", "Thermistor divider", R0603), ("R117", "Hard-short divider high", R0603),
        ("R118", "Hard-short divider low", R0603), ("R119", "Comparator pull-up", R0603),
        ("R120", "Hardware override isolation", R0603),
    )),
)


def place():
    board = pcb.LoadBoard(str(SOURCE))
    previous = {f.GetReference(): f for f in board.GetFootprints()}
    assert REMOVED <= previous.keys()
    for ref in REMOVED:
        board.Delete(previous[ref])
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            pad.SetNetCode(0)
    occupied = {FRONT: [], BACK: []}
    for footprint in board.GetFootprints():
        layer = footprint.GetLayer()
        occupied[layer].append(footprint_bounds(footprint, layer))
        opposite = BACK if layer == FRONT else FRONT
        occupied[opposite].extend(bounds(pad.GetBoundingBox()) for pad in footprint.Pads()
                                  if pad.IsOnLayer(opposite))
    for layer, (cx, cy), parts in GROUPS:
        for ref, value, identifier in parts:
            f = k.footprint(board, DEST, identifier, ref, value, 0, 0, 0, k.uid(), k.uid(), {})
            if layer == BACK:
                f.Flip(f.GetPosition(), pcb.FLIP_DIRECTION_LEFT_RIGHT)
                f.SetOrientationDegrees(0)
            left, top, right, bottom = footprint_bounds(f, layer)
            candidates = ((x / 2, y / 2) for x in range(254, 290) for y in range(141, 208))
            for x, y in sorted(candidates, key=lambda point: (point[0] - cx)**2 + (point[1] - cy)**2):
                box = (x + left, y + top, x + right, y + bottom)
                if box[0] < 126.5 or box[2] > 144.65 or box[1] < 70.35 or box[3] > 103.65:
                    continue
                if any(conflicts(box, prior) for prior in occupied[layer]):
                    continue
                f.SetPosition(k.pt(x, y))
                occupied[layer].append(box)
                break
            else:
                raise ValueError(f"No room for {ref}")
    DEST.mkdir(exist_ok=True)
    target = DEST / "8S-D5-Studium.kicad_pcb"
    assert pcb.SaveBoard(str(target), board)
    # Board-relative models now resolve from the new study directory.
    data = target.read_text(encoding="utf-8")
    for library in (SOURCE.parent, SOURCE.parent.parent / "Zasilacz_RevK_Moc"):
        for model in library.glob("*.wrl"):
            data = data.replace(f"${{KIPRJMOD}}/{model.name}", f"${{KIPRJMOD}}/../{library.name}/{model.name}")
    target.write_text(data, encoding="utf-8", newline="\n")
    restored = pcb.LoadBoard(str(target))
    corners = {(point.x, point.y) for drawing in restored.GetDrawings()
               if drawing.GetLayer() == pcb.Edge_Cuts for point in (drawing.GetStart(), drawing.GetEnd())}
    assert corners == {(pcb.FromMM(x), pcb.FromMM(y)) for x in (75, 145) for y in (70, 104)}
    assert not list(restored.GetTracks())
    assert all(pad.GetNetCode() == 0 for fp in restored.GetFootprints() for pad in fp.Pads())
    added = sum(len(parts) for _, _, parts in GROUPS)
    assert len(list(restored.GetFootprints())) == len(previous) - len(REMOVED) + added
    print(f"{len(previous)} original, {len(REMOVED)} removed, {added} added; {len(list(restored.GetFootprints()))} positions; 70 x 34 mm")


if __name__ == "__main__":
    place()
