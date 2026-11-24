# SC09 SB02-A3 design-input checkpoint

This is an engineering input checkpoint for the owner-authorized controller redesign.
It is not a frozen routed PCB or a manufacturing release. Native layout work and
independent verification continue separately. No Gerbers in this directory are
approved for fabrication, and the original SC09 manufacturing files do not describe
the changed controller circuit.

- Owner direction: change the controller to obtain real 2 mm high-differential gaps.
- Controller: LNK3206P positive buck, with optically coupled constant-current and
  overvoltage feedback. The LED output remains mains referenced, without galvanic
  isolation or an independent main-switch-short disconnect.
- Independent intent: 36 positions, 83 electrical pins, 84 copper contacts and
  20 nets. D1 has two separate physical cathode contacts. Four compensation
  positions are deliberately unpopulated; their values are not qualified.
- Normal-operation spacing matrix: 190 explicitly enumerated pairs, with 2 mm
  high-differential targets and 0.3 mm declared local domains. Healthy bias clamp D2
  is assumed for the local 20 V domain; the fault-scope document records its limits.
- Target outline: 51.2 x 33 mm. Conservative component/PCB height planning is
  22.4 mm, including the 2.6 mm rear bridge and +0.16 mm board thickness allowance.
  This does not include installation vent reserve or untrimmed solder leads.
- Electrical calculations are conditional paper estimates. Startup, hot magnetics,
  current, stability, fault latency, inrush pulse qualification, efficiency and
  temperatures have not been physically verified.

This checkpoint does not record exact-source human acceptance, a supplier order,
powered-test authorization or finished-product compliance. The working branch is
`concept/integrated-shade-nonisolated-buck`; main is excluded.
