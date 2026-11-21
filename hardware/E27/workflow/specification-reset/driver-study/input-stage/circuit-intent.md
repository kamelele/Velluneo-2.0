# Velluneo isolated constant-current supply: consolidated circuit intent P0

2026-11-17. **Pre-schematic research intent**, not an approved/generated schematic, complete physical-pin contract, build package or verified working supply. This consolidates the existing UCC28711 candidate and adds concrete input, rectifier and temperature-sensing references. Architecture A/common simple panels unchanged. Numerical initial values are candidates; parts.csv distinguishes newly supported references. Source/measurement gaps remain owned in findings.md.

## Functional connections

| Domain / function | Proposed connection and initial value | Evidence or remaining limit |
|---|---|---|
| E27 input | Two mains contacts feed bridge AC inputs; one path contains F1 then RIN in series. No polarity/neutral safety reliance. | F1 UMT-H250mA277VAC; RIN47ohm AC05. Not an approved fuse/disconnection/surge coordination. |
| Rectified primary | BR1 positive is BUS+, negative is PGND. CBULK15uF450V spans BUS+–PGND, positive toBUS+. RB1/RB2 are series499k across the same nodes. | No direct primary conductor is exposed for panel service. Physical enclosure and insulation remain unverified. |
| Flyback primary | T1 primary120turn flyback input end toBUS+, other end toDRAIN. Q1 drain toDRAIN, source toSENSE; RCS2.37ohm SENSE–PGND. | EFD25/13/9 candidate, Lp2.304mH±10%; finished insulation/winding/pin design not qualified. STN1NK80Z800V retained candidate, not newly validated. |
| Clamp | US1M anodeDRAIN/cathodeCLAMP; unidirectional SMBJ160A cathodeCLAMP/anodeBUS+. | Same preferred direct-clamp polarity as clamp-candidate. Hot repetitive behavior, dynamic drain/SOA and input surge unresolved. Do not add comparison RCD parts by default. |
| Controller power | UCC28711 VDD to2x470nF C0G/PGND; HV toBUS+; GND toPGND. Auxiliary22turn flyback-positive end via DAUX anode/cathode toVDD, returnPGND. | DAUX STTH1R02A. Exact charge-path impedance/pulsed current and VDD overshoot remain to be selected/verified. No artificial external bias in claimed self-start. |
| Current/gate control | UCC CS via1.40k toSENSE. DRV drives Q1 gate through tuning resistance; gate-return and controller-return have separate high-current/Kelvin routing intent. | Actual gate resistor/pulldown references, source/sink trajectory, delay, local loop and source sense must be finalized; no value is invented to complete a BOM. |
| Voltage/sample control | Auxiliary sense node to80.6k thenVS;17.4k VS–PGND. No VS filter capacitor by default. | Existing startup-candidate thresholds/sampling allocations; actual waveform capacitance/ringing pending. |
| Thermal control | UCC NTC toNTCS0603E3104FXT toPGND, mounted at a selected primary-side base hot spot. |100k/4100K candidate, approximate88C nominal trip. Sensor temperature/lag is not LED junction or housing temperature; open sensor loses this external protection. |
| Isolated output | T1 secondary30turn flyback-positive end toDOUT anode; DOUT cathodeOUT+. Secondary returnOUT−. COUT positiveOUT+, negativeOUT−; candidate10uF63V PanasonicEEHZA1J100P. | DOUT STTH2R02A200V, not an unsupported100V substitution. Existing output-capacity/current/LED sensitivities retained. |
| Replaceable panel | OUT+/OUT− feed common simple LED panel. Nominal10k output-bleed functional position remains from earlier studies. | Exact bleed parts/redundancy, connector/polarity/keying, accessible residual energy and cooling limits still open. No safe access voltage/time is selected. |
| Separation | PGND/auxiliary return and OUT− are separate electrical domains; magnetic coupling through finished insulatedT1 only in this intent. | No Ycapacitor, PE connection or conductive return bridge is selected. This text proves no physical insulation, creepage, touch-current or product-safety class. |

Controller reference: native SLUSB86C maps VDD1,VS2,NTC3,GND4,CS5,DRV6,HV7. This seven-pin numbering must be checked against the exact package drawing; do not copy older reference drawings labeling HV8. The MOSFET model D/G/S terminal order is not a physical footprint map. Numeric bridge/diode/custom-transformer pad mapping and complete intended connectivity require independent native-package review before schematic generation.

## Consolidated material direction

Retain UCC28711DR, STN1NK80Z,120:30:22 EFD25, proposed80.6k/17.4k/1.40k and2x470nF bias path as the existing investigated base. Prefer15uF BXW over the10uF comparison after this input screen. Add candidate MB10S-13, UMT-H250mA,47ohmAC05,2x499k bleeder, STTH2R02A, STTH1R02A and Vishay100k4100K NTC. The practical cost of pulse margin is an18x7.5mm resistor and10x20mm capacitor body; transformer/clearance/lead-bend dimensions still dominate fit. This does not select a board outline or promise an E27 envelope fit.

parts.csv is the new partial candidate BOM, not a complete procurement list. Exact gate, auxiliary charging, current-sense, output-bleed, filter/surge and connector positions cannot be silently filled from generic examples. A main-input fuse is not intended to operate during a recoverable panel fault; that requirement still needs actual fault-current/temperature proof. No full JLCPCB-assembled route or stock reservation exists; THT resistor/capacitor and custom transformer need explicit assembly planning. No order or supplier message occurred.
