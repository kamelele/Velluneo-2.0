# Clamp task, ownership and next verification contract

DRV-CLAMP-01; specification; baseline draft e951517b2becf6ecb2002f2d5ad5c17aa3cb2d3f. Sole writer/coordinator `/root`. Allowed writes: driver-study/clamp-candidate/* and investigation index. No CAD/library/configuration lease. Requirements packet r11 remains authoritative, blob6493b29bd33fbde1f3c61c5e995b11447cb83e9b. Parent component results hashd87c14c11e44aced0eabebf0346bd7d4d648f0d8fbc59fa76ebcfd18f4d60186 is asserted before calculation.

Acceptance for preliminary task publication: exact candidate components/polarities, native source identity, controller-aware full/minimum-current reset checks, energy-consistent numerical evidence, explicit startup/fault/thermal limits, independent four-role review and remote readback. This is not acceptance of the circuit. Lifecycle review/index remain outside their own technical manifest.

| Check / coordinator owner | Observable evidence required |
|---|---|
| Transformer | Finished construction/insulation/coupling specification and leakage measurement method; proposed direct-clamp Llk/Lp≤1% target verified without relaxing insulation. If not met, recalculate power/reset/thermal and affected source decisions. |
| Avalanche and blocking diode | Actual I–V–temperature behavior, repetitive pulse/average thermal capability, forward/reverse recovery and parasitic spikes on the intended PCB. Table259V@2.3A25°C and50V allowance are insufficient as hot/surge bounds. |
| Controller timing | Leakage reset/VS waveform satisfies native600ns minimum-current and2.2us maximum-current guidance; approximately100mVpp VS ring criterion and sampling-time margin checked. Startup acquisition/fault shutdown/retry measured or supported by a valid controller model. |
| Input/device protection | Whole input surge path, HV/bulk/rectifier ratings, clamp component faults, MOSFET/clamp SOA and thermal behavior. RC-COMP-002 stays major until independently checked. |
| Integrated startup | Actual gate/bias draw, auxiliary takeover and clamp influence; retain RC-BIAS-001 major. No automatic inheritance of the parent's conditional4.3mA/0.300ms example. |
| Product recovery/access | Exact reviewed normal/no-load/panel-open/panel-short/offline-replacement/power-cycle sequence, persistent-fault heat and service-energy/cooling evidence. No powered panel insertion. |
| Manufacturing | Exact supplier/assembly route for one full driver plus one panel, transformer and housing interface; no complete JLCPCB-ready BOM or fit approval currently. |

The user performs later mains-side laboratory work with university support. This contract is not a ready-to-run test procedure or energization authorization: hardware/setup revisions, responsible person, rated instruments, numeric stop limits and physical readiness must be established before execution. No test measurements are invented.

Four independent read-only contexts inspect final frozen code/results/findings/parts/sources/this contract: Reality `/root/spec_reality`, Overengineering `/root/spec_simplicity`, Completeness `/root/spec_completeness`, Change `/root/spec_change`. Record actual execution/source coverage and every finding in review.md. Publication recommendations cannot close major findings, grant human stage approval or authorize schematic/manufacturing work. The owner remains the stage approver; no external engineer is imposed before calculations.
