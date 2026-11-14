# 8S-D4 supply-valid inhibit draft

Task E27-8S-D4. Codex owns the schematic generator, D4 capture input, verification script, compact preview generator, and new D4 output directory. Base is `73b075d1cb768e4106da7fd0a0a8540388c2d282`, including the separate D3 compact study. Inputs are the D3 pin map and restart study at `09420abdd2750daf150ddc5855eb7dc23076cb35`, requirements REQ-CC, REQ-CONTACT, REQ-INTEGRATION and REQ-JLC, and the pinned workflow reference in the index.

Capture a secondary supply-valid clamp as a candidate. Check exact pin and footprint agreement, native ERC, the static threshold and sink bounds, and fit on the 70 × 34 mm outline with native DRC. Keep this at the draft schematic and placement-study level. Fault retention, formal isolation review, routing and release remain pending. The project owner is the stage approval authority.

The detector is TPS3711DDCT (U109). It runs from RAW so it can pull SHDN low after V3V3_HOLD falls. C28 bypasses RAW locally. R39 and R40 set the falling threshold to 2.921–3.073 V and the rising threshold to 2.943–3.149 V in the static initial-tolerance calculation. R33 is 1.2 kΩ. At a 0.25 V clamp point, the source-current screen including the 10 µA eFuse allowance is 2.633 mA. With an assumed 2.35 V at the permit return, worst-case initial resistor tolerances in that screen give 2.083 V at SHDN. The eFuse datasheet calls for at least 1 V to enable. The calculation needs bench confirmation with the actual contacts and simultaneous rail transitions. [TI detector](https://www.ti.com/lit/ds/symlink/tps3711.pdf) · [TI eFuse](https://www.ti.com/lit/ds/symlink/tps2660.pdf)

The candidate part numbers and JLCPCB catalog entries are recorded in the [D4 capture input](driver-8s-inhibit-input.json). The drawing uses provisional JST GH footprints on J2 and J3 to match the placement study. Retain the existing connector validation task. U109, C28, R39 and R40 fit on the front face on the secondary side. The static arrangement does not establish routing room or the actual copper separation after routing. The eFuse clamp shares the logic return. Its response with a fast rail collapse, startup delay, RAW surges and a U101 pass-short fault remains to be validated. An arbitrary LDO short can also exceed the logic absolute maximum. This detector is an undervoltage clamp; the overvoltage fault needs its own design check. The existing volatile short latch still loses state after the held rail is fully discharged.

## Verification

Run these from hardware/E27 with KiCad 10.0.8 and its Python.

- `python work/rev8s_draft.py --revision 8S-D4` builds the candidate.
- `python work/verify_rev8s_draft.py --revision 8S-D4` exports and compares the pin map. There are 94 footprints including two DNP positions, 264 connected pins, and 18 explicit no-connects. ERC reports zero errors and the existing SR strap warning.
- `python work/check_8s_restart.py` passes the threshold and state screens. The state check illustrates a retained policy and the implemented latch is still volatile.
- `python work/preview_8s_compact.py --revision 8S-D4` builds and reloads the unrouted two-layer board, checking net assignment.
- `kicad-cli pcb drc --schematic-parity -o outputs/Zasilacz_8S_D4/DRC.rpt outputs/Zasilacz_8S_D4/Zasilacz_8S_D4.kicad_pcb` reports zero geometric violations, zero schematic/PCB discrepancies, and 203 unrouted connections. Physical insulation review, routing and test evidence are outstanding.

[KiCad project and renders](../../outputs/Zasilacz_8S_D4/README.md) · [ERC](../../outputs/Zasilacz_8S_D4/ERC.rpt) · [DRC](../../outputs/Zasilacz_8S_D4/DRC.rpt)

Next design decision is the behavior after complete logic-rail loss following a short. Check preservation of lockout and restart conditions before a routing-stage review. The 70 × 34 mm outline is a placement target.

## Independent review and corrections

The read-only Reality Checker, Completeness Reviewer and Change Reviewer independently inspected the initial D4 candidate (schematic SHA-256 `3f9f54d1fadfda7a381efe9c2e5f61ca9d77e7509296ffd66983214f1675a51c`). The Change Reviewer compared it to D3 and found no changes to existing pin connections. The Completeness Reviewer compared 282 terminals, all 94 footprint assignments and the two unnetted mounting pads. The coordinator moved C28 adjacent to U109, replaced the original wave-solder-only R39 with the SMT Yageo C863197 candidate, and bound placement generation to SHA-256 checks of the schematic and export. The threshold screen keeps the original conservative 1% bound for R39. Sourcing and current stock need confirmation at quote. [Yageo R39 at JLCPCB](https://jlcpcb.com/partdetail/YAGEO-RT0603DRE0764K9L/C863197)

Open review findings include qualifying the blanking timer from the actual eFuse enable event, J2 pin 2-to-3 cross-short overstress, the U101 pass-short case, concurrent RAW and held-rail recovery, and keeping U109 RAW within its 36 V operating limit. For example, a degraded 1.3 V permit-return signal can raise SHDN to about 1.16 V while the U108 timer path still reads low. Keep D4 at draft stage pending these findings. Review of the initial candidate does not approve the corrected board or the formal schematic stage. [TI SN74LVC1G17](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf)

The independent Overengineering Reviewer inspected the corrected schematic and an intermediate placement. The reviewer recommended keeping the four-part clamp for comparison while leaving reset policy open. A mains-cycle reset needs independent mains-loss evidence. A service reset needs an approved procedure and a verified persistent state. A retry policy needs measured pulse energy and thermal bounds before choosing an implementation.

- Zasilacz_8S_D4.kicad_pcb SHA-256 `4977daa2d493db92ff8689fc5adec42bbce15e707538a918a455b14de296823c`
- DRC.rpt SHA-256 `b0f3c7d82dfcb2643cce10a71c99602a547a8a747058094b6547e11c7d53641f`
