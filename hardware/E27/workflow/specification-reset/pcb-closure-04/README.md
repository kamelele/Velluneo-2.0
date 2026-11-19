# PCB-CLOSURE-04-r3 — complete proposed spacing redesign

Base4eb215d273262ec4ba995fdf69e9118f9537aff1. The owner requests resolution of eight spacing reports and the capacitor return before routing. This packet now includes a **complete proposed33-part/81-pad rectangular41x60mm PCB**, matched schematic, libraries/models and fresh checks, under eco/. It is developed in isolation and is not silently adopted into the approved31-part circuit.

## Open the new complete proposal

Extract Velluneo_driver_return04_and_ECO.zip and open **eco/Velluneo_specification_reset.kicad_pro**. Native KiCad10.0.6 full-board checking reports **zero clearance violations, zero silkscreen violations, zero schematic-parity findings and54unconnected items**. There are no tracks/vias; exit5 is retained. The old eight nominal package findings are absent on this complete new candidate. Proposed schematic ERC is zero. All33MPNs/values/81pad shapes, drills, attributes, layers, transforms and23functionalnets/fourNC agree with source modules, native netlist and canonical pre-CAD unapproved intent. Numeric3mm/10mm screens and explicit global limits are retained without exclusions or severity reduction.

TVS-to-C1 return is **25.900622→4.472027mm** versus the prior40mm alternate; the Q1clampC1 endpoint chain43.122961→20.996621mm and T1three-leg sum39.109753→38.812533mm. These are distances between pads, not routed parasitics or operating waveforms. Bypass1.35mm, CS2.059mm, gate3.384mm, power-shunt5.642mm and shuntreturn2.7mm. **The sense R6–R9 endpoint grows to19.906mm** and needs dedicated Kelvin routing plus return/coupling review; this regression is not hidden by the shorter clamp metric. See eco/routing-intent.md and full checks.

## Real circuit and construction changes, still proposed

The old rigid lands cannot meet the3mm engineering screen merely by moving components. The concrete ECO uses UCC28701DBVR(noHVpin), two402kΩstartup resistors,80.6kΩR13,2.32ΩR9, W10Gbridge/STF2N80K5MOSFET with explicit proposed formed terminals, and2mm T1lands with unchanged1.35mmholes/5mmpitch. Source facts, process dimensions and unresolved conditions are in eco/README.md. Four separate coupons remain available, but their result is not substituted for the full-board result.

Root caught an initial13.6MΩ feed that omitted R13/C3. Review caught a later66.01V zero-draw equilibrium. The revised804kΩ/80.6kΩ feed includes bothVDDcapacitors/hotD2leakage, passes all64declared23Vcharging cases and bounds normal-line startup-feed-only equilibrium to33.866660V without assuming minimum controller draw. It adds about0.130Winitialhighlineloss. This is not an auxiliary/surge/commutation clamp, fault simulation or thermal test. New140kHzceiling and typical-onlyNTCthresholds require new operating/protection/magnetic/thermal assessment.

41x60mm is a trial,1mm wider than the last40mm. It does not change the lamp outer targetØ60x120mm or prove finished fit. Nominal rotated installed allocations need58.028755mm diameter, leaving just0.985623mm radial difference to the60mm OUTER target, limitingC1. Walls, mounting, wire, tolerances, lead forming, seating and120mm fit remain unqualified. Models in previews are allocations, not validated manufacturer models. Finished insulation at T1nominal3mm, annuli/fillets, terminal forming/registration and cross-face coupling remain explicit conditions.

## Retained old-circuit comparison

The root ZIP project is the earlier improved31-part/79-pad/40x60mm comparison, with return12.470815mm/Qchain28.804021mm. Its native report still has8packageclearance/0silk/53unconnected/0parity. It is preserved honestly and must not be confused with the new eco/33-part board. Approved active shared CAD, graph, requirements, rules and approval records remain unchanged.

Fresh toolkit schematic/placement requirements and work checks retain their failures. A human ECO/intent decision and actual technical closure are required before accepted routing; a yes alone does not establish electrical/process/insulation readiness. Four final independent roles review the frozen r3 packet, with actual outcomes recorded separately. No fabrication files, supplier contact, order or powered test is made.
