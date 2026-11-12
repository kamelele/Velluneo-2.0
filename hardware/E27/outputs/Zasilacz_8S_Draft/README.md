# Velluneo E27 8S KiCad draft

Task E27-8S-CAD-DRAFT has one writer, Codex. Its inputs are commit `c5dbe5d8dfb15dac398cac8574408646314b010b`, the [8S capture input](../../workflow/8s/driver-8s-capture-input.json) and Rev K reusable power-stage symbols and footprints. The owner answered “tak” to the request to create a separate draft KiCad project before full pin-intent approval, with outstanding circuitry identified on the drawing. The authorization covers this preview.

Scope is the native draft schematic, its local libraries, preview, netlist check and ERC report, and the generator in `work/rev8s_draft.py`. The acceptance checks for this task are successful export from KiCad, agreement with the draft pin map, and a legible rendering. Schematic, layout and production acceptance remain open.

## Open and review

Open [Zasilacz_8S_Draft.kicad_pro](Zasilacz_8S_Draft.kicad_pro) in KiCad. The [native schematic](Zasilacz_8S_Draft.kicad_sch) and the [image exported from KiCad](Schemat_8S.png) show one 8S output and the protection on the same schematic. Rev K and Rev H remain the archived 16-LED revision.

- R9 is 0.130 Ω and R10 is 113 kΩ. The flyback regulates the single string. The two AL5812 and the power/control link are absent. J3 has two contacts. J2 carries the S1/TH1 permit loop and the independent S2 path.
- The TPS26600 path, the auxiliary hold supply and the TPS3700 short and hold-ready monitor are on the sheet. The permit driver, startup blanking, reset and latch are labeled open. The draft therefore has no complete enable path. Transformer, connector and cold-start limits remain to be confirmed. The local footprints are candidate or legacy patterns for schematic work. 3D models and placement remain outside this draft.
- KiCad 10.0.8 exported 69 components, 177 connected pins and 14 explicit no-connects. All match the provisional [capture input](../../workflow/8s/driver-8s-capture-input.json). The [draft check](Draft_Check.json) records the source hashes. ERC reports seven power-driver errors and two singleton labels at the incomplete permit interface. There is no approved whole-board connectivity result. [ERC report](ERC.rpt)
- There is no PCB, verified layout or JLCPCB manufacturing package for this draft. No manufacturing approval was given. See the [schematic-stage requirements check](../../workflow/8s/schematic-prep-check.json) for remaining product inputs.
