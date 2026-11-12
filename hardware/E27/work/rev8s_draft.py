"""Build the separate 8S draft schematic from the reviewed capture input."""

import hashlib
import json
from pathlib import Path
from shutil import copy2

import build as k
import power
import revk_power

NAME = "Zasilacz_8S_Draft"
DEST = Path("outputs") / NAME
CAPTURE = Path("workflow/8s/driver-8s-capture-input.json")
REV_H = Path("outputs/Zasilacz_RevH_Sterowanie")
PASSIVES = {"R", "C", "CP", "D", "Z", "L", "F", "MOV"}

POSITIONS = {
    "U1": (201.93, 138.43), "R22": (228.6, 73.66), "U2": (50.8, 185.42), "U101": (193.04, 184.15), "U102": (311.15, 184.15),
    "J2": (372.11, 184.15), "J3": (379.73, 203.2),
    "C11": (52.07, 215.9), "R14": (102.87, 215.9), "R15": (151.13, 215.9),
    "R16": (52.07, 227.33), "R17": (102.87, 227.33), "C12": (151.13, 227.33),
    "C13": (52.07, 238.76), "R18": (102.87, 238.76), "R19": (151.13, 238.76),
    "R24": (201.93, 204.47), "D10": (252.73, 204.47),
    "C14": (201.93, 215.9), "C15": (252.73, 215.9), "C17": (201.93, 227.33),
    "R25": (302.26, 215.9), "R26": (351.79, 215.9),
    "R27": (302.26, 227.33), "R28": (351.79, 227.33),
    "R29": (302.26, 238.76), "R30": (351.79, 238.76),
    "R31": (201.93, 238.76), "R32": (252.73, 238.76),
}
VALUES = {
    "U2": "TPS26600PWPR", "U101": "TPS7A1633DGNR", "U102": "TPS3700DDCR",
    "R9": "0.130R / 1%", "R10": "113k / 0.1%", "R14": "226k / 0.1%",
    "R15": "10k / 0.1%", "R16": "30.1k / 1%", "R17": "402k / 1%",
    "R18": "10k", "R19": "4.7k / 0.5W", "R24": "1k",
    "R25": "150k / 1%", "R26": "150k / 1%", "R27": "10k / 1%",
    "R28": "255k / 1%", "R29": "255k / 1%", "R30": "10k / 1%",
    "R31": "100k", "R32": "100k", "C11": "100n eff. min", "C12": "47n",
    "C13": "100n eff. min", "C14": "47u / 50V", "C15": "100n",
    "C17": "10u / 50V candidate", "D10": "BAV21W", "J2": "Interlocks",
    "J3": "8S LED output",
}
FP_0603 = "Resistor_SMD:R_0603_1608Metric"
FP_1206 = "Resistor_SMD:R_1206_3216Metric"
FOOTPRINTS = {
    "R9": FP_1206, "R19": FP_1206, "D10": power.SOD,
    "C11": power.C80, "C12": power.C60, "C13": power.C80, "C15": power.C80,
    "U2": "E27:PWP0016A", "U101": "E27:TPS7A16_DGN",
    "U102": "Package_TO_SOT_SMD:SOT-23-6",
}
DNP = {"C16", "R23"}

# The first and second groups of each device are drawn on opposite sides.
PIN_GROUPS = {
    "U1": (
        ((13, "V", "input"), (14, "BPP", "power_in"), (16, "S", "passive"),
         (17, "S", "passive"), (18, "S", "passive"), (19, "S", "passive"),
         (24, "D", "passive"), (15, "NC", "no_connect")),
        ((1, "IS", "input"), (2, "GND", "power_in"), (3, "FB", "input"),
         (4, "BPS", "power_in"), (5, "SR", "output"), (6, "VO", "power_in"),
         (7, "FWD", "input"), (8, "NC", "no_connect"), (9, "NC", "no_connect"),
         (10, "NC", "no_connect"), (11, "NC", "no_connect"), (12, "NC", "no_connect")),
    ),
    "U2": (
        ((1, "IN", "power_in"), (2, "IN", "power_in"), (3, "UVLO", "input"),
         (5, "OVP", "input"), (7, "SHDN", "input"), (9, "GND", "power_in"),
         (8, "RTN", "passive"), (17, "PAD", "passive"), (4, "NC", "no_connect")),
        ((15, "OUT", "power_out"), (16, "OUT", "passive"), (6, "MODE", "input"),
         (11, "ILIM", "passive"), (12, "dVdT", "passive"), (10, "IMON", "output"),
         (14, "FLT", "open_collector"), (13, "NC", "no_connect")),
    ),
    "U101": (
        ((8, "IN", "power_in"), (5, "EN", "input"), (4, "GND", "power_in"),
         (9, "PAD", "passive"), (6, "NC", "no_connect")),
        ((1, "OUT", "power_out"), (2, "DNC", "no_connect"),
         (3, "PG", "open_collector"), (7, "DELAY", "output")),
    ),
    "U102": (
        ((5, "VDD", "power_in"), (2, "GND", "power_in"),
         (3, "INA+", "input"), (4, "INB-", "input")),
        ((1, "OUTA", "open_collector"), (6, "OUTB", "open_collector")),
    ),
    "J2": (
        ((1, "S1 / TH1 feed", "passive"), (2, "S1 / TH1 return", "passive"),
         (3, "S2 input", "passive"), (4, "S2 return", "passive")), (),
    ),
    "J3": (((1, "LED+", "passive"), (2, "LED-", "passive")), ()),
}


def symbol_layout(ref, kind):
    if kind in PASSIVES:
        graphic, pins = power.two(kind)
        return kind, graphic, pins, ((1, -3.81, 0), (2, 3.81, 0)), 3.81

    if ref in PIN_GROUPS:
        left, right = PIN_GROUPS[ref]
        half = 12.7 if ref in {"U1", "U2", "J2"} else 8.89
        height = 1.27 * (max(len(left), len(right)) + 1)
        definitions = [
            (pin, name, side * (half + 2.54), round(1.27 * (len(group) - 1 - 2 * index), 3),
             0 if side < 0 else 180, pin_type)
            for side, group in ((-1, left), (1, right))
            for index, (pin, name, pin_type) in enumerate(group)
        ]
        symbol_name = ref
    else:
        half, height, legacy = power.complex_pins(kind)
        definitions = [(*pin, "passive") for pin in legacy]
        symbol_name = kind
    graphic = k.box(-half, height, half, -height, "background")
    if ref == "U1":
        graphic += k.poly([(0, -height), (0, height)])
    pins = [k.pin(n, name, x, y, angle, kind=pin_type)
            for n, name, x, y, angle, pin_type in definitions]
    ends = [(n, x, y) for n, _, x, y, _, _ in definitions]
    return symbol_name, graphic, pins, ends, height + 2.54


def source_parts():
    capture = json.loads(CAPTURE.read_text(encoding="utf-8"))
    for basis in capture["basis_files"]:
        assert hashlib.sha256((CAPTURE.parent / basis["path"]).read_bytes()).hexdigest() == basis["sha256"]
    return capture["parts"]


def copy_custom_footprint(footprint):
    if not footprint.startswith("E27:"):
        return
    filename = footprint.split(":")[1] + ".kicad_mod"
    for reference in (revk_power.DEST, REV_H):
        source = reference / "E27.pretty" / filename
        if source.is_file():
            copy2(source, DEST / "E27.pretty" / filename)
            return
    raise FileNotFoundError(filename)


def rebuild():
    part_data = source_parts()
    historical = {part.ref: part for part in revk_power.devices()}
    _, _, sheet = k.begin(NAME, "Schematic draft", .19, .55)
    definitions = {}
    items = [
        k.note("VELLUNEO E27 / ZASILACZ 8 LED W SZEREGU", 17, 20, 2.8),
        k.note("SCHEMAT ROBOCZY  •  230 V AC  •  JEDNA PCB  •  DO PRZEGLĄDU", 17, 29, 1.55),
        k.note("Wejście i filtr", 18, 39, 1.5),
        k.note("Przetwornica izolowana", 155, 39, 1.5),
        k.note("Regulacja napięcia i prądu szeregu", 276, 39, 1.5),
        k.note("R9: 0,130 Ω   |   R10: 113 kΩ   |   prąd LED ok. 271 mA (wstępnie)", 270, 152, 1.17),
        k.note("Odcięcie eFuse", 18, 163, 1.5),
        k.note("Podtrzymanie układu ochrony", 170, 163, 1.5),
        k.note("Monitor zwarcia i wyjście", 283, 163, 1.5),
        k.note("J2-1 → S1 NO → TH1 NC → J2-2. J2-3 → S2 NO → J2-4.", 18, 252, 1.25),
        k.note("OTWARTE: sterownik PERMIT, zwłoka rozruchu, reset i zatrzask po zwarciu.", 18, 260, 1.42),
        k.note("Do weryfikacji: T1, dobór styków, zimny start i limity zabezpieczeń.", 18, 267, 1.22),
    ]
    for ref, part in part_data.items():
        prior = historical.get(ref)
        kind = prior.kind if prior else ref.rstrip("0123456789")
        if ref in {"C14"}:
            kind = "CP"
        if ref in PIN_GROUPS and ref != "U1":
            kind = ref
        footprint = FOOTPRINTS.get(ref)
        if footprint is None:
            footprint = prior.footprint if prior else FP_0603 if ref.startswith("R") else ""
        copy_custom_footprint(footprint)
        value = VALUES.get(ref, part["value"])
        raw_x, raw_y = POSITIONS[ref] if ref in POSITIONS else prior.schematic
        x, y = (round(round(value / 1.27) * 1.27, 3) for value in (raw_x, raw_y))
        name, graphic, pins, ends, gap = symbol_layout(ref, kind)
        symbol = f"E27:EightS_{name}"
        definitions[symbol] = k.symbol(symbol, ref.rstrip("0123456789"), graphic, pins, kind not in PASSIVES)
        assert {str(pin) for pin, _, _ in ends} == set(part["pins"]), ref
        placed = k.placed(symbol, ref, value, footprint, x, y, k.uid(), NAME, sheet, part["pins"])
        placed = placed.replace(k.prop("Reference", ref, x, y - 3.81), k.prop("Reference", ref, x, y - gap))
        placed = placed.replace(k.prop("Value", value, x, y + 3.81), k.prop("Value", value, x, y + gap))
        if ref in DNP:
            placed = placed.replace("(dnp no)", "(dnp yes)", 1)
        items.append(placed)
        for number, dx, dy in ends:
            xx, yy = round(x + dx, 3), round(y - dy, 3)
            net = part["pins"][str(number)]
            if net is None:
                items.append(f'(no_connect (at {xx} {yy}) (uuid "{k.uid()}"))')
            else:
                label_x = round(xx + (2.54 if dx > 0 else -2.54), 3)
                items.extend((k.wire(xx, yy, label_x, yy),
                              k.label(net, label_x, yy, 0 if dx > 0 else 180)))

    k.schematic(DEST, NAME, sheet, "Velluneo E27 / 8S / SCHEMATIC DRAFT",
                list(definitions.values()), items, "A3", "8S-D1")
    schematic = DEST / f"{NAME}.kicad_sch"
    text = schematic.read_text(encoding="utf-8")
    k.save(schematic, text.replace('(date "2026-11-09")', '(date "2026-11-12")', 1))
    k.save(DEST / "sym-lib-table", '(sym_lib_table (version 7) (lib (name "E27") (type "KiCad") '
           '(uri "${KIPRJMOD}/E27.kicad_sym") (options "") (descr "Velluneo 8S draft")))')
    k.save(DEST / "fp-lib-table", '(fp_lib_table (version 7) (lib (name "E27") (type "KiCad") '
           '(uri "${KIPRJMOD}/E27.pretty") (options "") (descr "Velluneo draft footprints")))')


if __name__ == "__main__":
    rebuild()
