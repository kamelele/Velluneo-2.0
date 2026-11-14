# Velluneo E27 8S KiCad draft

Task E27-8S-CAD-DRAFT has one writer, Codex. Its inputs are commit `c5dbe5d8dfb15dac398cac8574408646314b010b`, the [8S capture input](../../workflow/8s/driver-8s-capture-input.json) and Rev K reusable power-stage symbols and footprints. The owner answered “tak” to the request to create a separate draft KiCad project before full pin-intent approval, with outstanding circuitry identified on the drawing. The authorization covers this preview.

Scope is the native draft schematic, its local libraries, preview, netlist check and ERC report, and the generator in `work/rev8s_draft.py`. The acceptance checks for this task are successful export from KiCad, agreement with the draft pin map, and a legible rendering. Schematic, layout and production acceptance remain open.

## Open and review

Open [Zasilacz_8S_Draft.kicad_pro](Zasilacz_8S_Draft.kicad_pro) in KiCad. The [native schematic](Zasilacz_8S_Draft.kicad_sch), [full schematic preview](Schemat_8S.png) and [control detail](Sterowanie_8S.png) show the single 8S output and its protection. Rev K and Rev H are the archived 16-LED revision. [8S-D1 snapshot](https://github.com/kamelele/Velluneo-2.0/tree/5a20a9c7f85fb8baec4ab6956e26f457207b724b/hardware/E27/outputs/Zasilacz_8S_Draft)

- R9 is 0.130 Ω and R10 is 113 kΩ. The flyback regulates the single string. J3 has two contacts. J2 carries the S1/TH1 permit loop and the independent S2 path.
- Revision 8S-D2 adds hardware permit, startup blanking, POR and latched shutdown around the TPS3700 monitor. The physical candidate is captured in the [control pin map](../../workflow/8s/driver-8s-control-input.json). The candidate values and operating sequence are described in [the control note](../../workflow/8s/driver-8s-control.md).
- For the D2 snapshot, KiCad 10.0.8 exported 88 components, 246 connected pins and 17 explicit no-connects. They match the provisional base and control maps. The [draft check](Draft_Check.json) records the current revision source hashes and a passing digital-sequence model. ERC reports zero errors and one warning on the intentional SR-to-SEC_GND strap used for diode rectification. The warning remains visible. [ERC report](ERC.rpt)
- T1, connector drawings, cold-start envelope, actual blanking and turn-off timing, and fault retention require validation. Placement, final libraries, PCB and JLCPCB fabrication files remain pending. [Schematic-stage requirements check](../../workflow/8s/schematic-prep-check.json)

## 8S-D3 follow-up

The current schematic, image exports and verification report are D3. The circuit change adds a Schmitt buffer in the timer signal, revises three pull-ups, and adds explicit hold-supply and pulse resistor candidates. It exports 90 components and 252 connected pins. ERC reports 0 errors and the retained SR warning. The brownout and reset cases remain open before layout. [D3 review and correction record](../../workflow/8s/driver-8s-d3-review.md) · [D2 snapshot](https://github.com/kamelele/Velluneo-2.0/tree/cff8aa2640a1573fba135b6044f90b9f35f552bf/hardware/E27/outputs/Zasilacz_8S_Draft)
