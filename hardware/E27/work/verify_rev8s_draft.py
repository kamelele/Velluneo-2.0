"""Check the D2 export and exercise the permit logic at its digital boundaries."""

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from xml.etree import ElementTree

from rev8s_draft import CAPTURE, CONTROL, DEST, NAME, POWER_SOURCES, source_parts


@dataclass
class Protection:
    ready_latched: bool = False
    fault_latched: bool = False

    def step(self, *, por=True, hold_ready=True, switch=True, blank_done=False, fault=False):
        if not por:
            self.ready_latched = False
            self.fault_latched = False
        else:
            self.ready_latched |= hold_ready
            self.fault_latched |= blank_done and fault
        permit = por and self.ready_latched and not self.fault_latched
        return permit and switch


def check_sequence():
    circuit = Protection()
    assert not circuit.step(por=False)
    assert not circuit.step(hold_ready=False)
    assert circuit.step(fault=True)
    assert circuit.step(blank_done=True)
    assert not circuit.step(switch=False)
    assert circuit.step(hold_ready=False, fault=True)
    assert not circuit.step(hold_ready=False, blank_done=True, fault=True)
    assert not circuit.step(switch=False)
    assert not circuit.step()
    assert not circuit.step(por=False)
    assert circuit.step()

    short_at_start = Protection()
    assert short_at_start.step(fault=True)
    assert not short_at_start.step(hold_ready=False, blank_done=True, fault=True)
    assert not short_at_start.step()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def verify(export):
    plan = source_parts()
    tree = ElementTree.parse(export)
    components = {part.get("ref"): part for part in tree.findall("./components/comp")}
    assert set(components) == set(plan)
    expected = {(ref, pin): net for ref, part in plan.items() for pin, net in part["pins"].items()}
    actual = {}
    for net in tree.findall("./nets/net"):
        name = net.get("name").lstrip("/")
        for node in net.findall("node"):
            ref, pin = node.get("ref"), node.get("pin")
            key = (ref, pin)
            assert key not in actual, key
            actual[key] = None if node.get("pintype", "").endswith("no_connect") else name
    assert actual == expected, [
        (key, actual.get(key), expected.get(key))
        for key in actual.keys() | expected.keys()
        if actual.get(key) != expected.get(key)
    ]
    assert components["R9"].findtext("value") == "0.130R / 1%"
    assert components["R10"].findtext("value") == "113k / 0.1%"
    assert {ref for ref, part in components.items() if part.find("property[@name='dnp']") is not None} == {"C16", "R23"}
    assert len([pin for ref, pin in actual if ref == "J3"]) == 2
    assert set(components).isdisjoint({"J101", "J102", "U3", "U4"})

    erc = DEST / "ERC.rpt"
    text = erc.read_text(encoding="utf-8-sig")
    errors, warnings = map(int, re.search(r"Errors (\d+)  Warnings (\d+)", text).groups())
    assert (errors, warnings) == (0, 1)
    assert "[pin_to_pin]" in text and "Symbol U1 Pin 5 [SR" in text
    check_sequence()
    schematic = DEST / f"{NAME}.kicad_sch"
    flag_count = schematic.read_text(encoding="utf-8").count('(lib_id "power:PWR_FLAG")')
    assert flag_count == len(POWER_SOURCES)
    for file in (schematic, erc):
        file.write_bytes(file.read_bytes().replace(b"\r\n", b"\n"))
    report = {
        "status": "draft_map_match",
        "revision": "8S-D2",
        "exporter": tree.findtext("./design/tool"),
        "schematic_sha256": digest(schematic),
        "base_draft_map_sha256": digest(CAPTURE),
        "control_map_sha256": digest(CONTROL),
        "erc_sha256": digest(erc),
        "components": len(components),
        "connected_pins": sum(net is not None for net in actual.values()),
        "explicit_no_connects": sum(net is None for net in actual.values()),
        "power_source_annotations": flag_count,
        "erc_errors": errors,
        "erc_warnings": warnings,
        "permit_sequence_model": "passed",
        "approved_connectivity_contract": False,
    }
    payload = json.dumps(report, indent=2) + "\n"
    (DEST / "Draft_Check.json").write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")


if __name__ == "__main__":
    verify(Path("workflow/8s/.work/rev8s-draft.xml"))
