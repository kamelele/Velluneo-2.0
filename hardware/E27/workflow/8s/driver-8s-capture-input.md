# Velluneo E27 one-board 8S schematic capture input

The current KiCad and JLCPCB baseline is Rev K power plus Rev H control for two eight-LED strings. Fresh KiCad 10.0.8 XML exports from the archived schematics confirmed that Rev K uses a 0.11 Ω sense resistor and 110 kΩ upper feedback resistor, and Rev H uses two AL5812 regulators, two separate cathodes at J3 and an inter-board link.

The [8S capture input](driver-8s-capture-input.json) defines candidate component and pin changes for a separate 8S revision. The input is owned by Codex and based on the archived Rev K design definitions for the reused input and flyback, and the 8S requirements, independent pin review and short-protection study for the changed secondary.

- Use R9 0.130 Ω and R10 113 kΩ. Keep D8 pin 1 cathode on SEC_GND and pin 2 anode on LED_RTN. Route the single load return through R9 with Kelvin sense to U1.
- Integrate U2, its OVP divider and the protection supply on the driver. Remove J101 and J102 and route RAW and the return locally. Remove U3 and U4 and their two regulated cathode paths. Replace J3 with two pins. J3-1 is LED+ after S2, J3-2 is LED− to LED_RTN.
- Map the short and hold-ready monitor and its auxiliary supply. The exported input explicitly marks the permit-driver, startup timer, reset and latch network as open. The new circuit also needs the final connector and transformer drawings and closure of the cold-string electrical envelope. The values and device identifiers in the draft are candidates.

The file is a pre-CAD design input. Its format is separate from the toolkit whole-board connectivity contract, which requires every physical pin, explicit unused-pin reasons, independent review and owner acceptance of its exact digest. No schematic, PCB or fabrication package was generated from it. [Schematic requirements check](schematic-prep-check.json)

The owner later authorized the separate [8S-D1 KiCad draft](../../outputs/Zasilacz_8S_Draft/README.md), captured from this provisional input.
