> Current project source now has all28 candidate footprint assignments. See [latest packet](../transformer-footprint/README.md) and its all-footprints ZIP for current checks. The earlier task/source/package scope below is historical, not an updated claim of completed physical/process or schematic-stage qualification.

> Historical initial capture context. The root schematic, generator and BOM now include three candidate footprint assignments under [FOOTPRINT-01](../footprint-study/README.md). Current source/check hashes are there; the initial capture ZIP/reviews retain their original scope and are not a current footprint-library acceptance.

# Velluneo E27 driver — native KiCad schematic draft

SCH-CAPTURE-01, 2026-11-17. Native KiCad10.0.6 source, not a manufactured or qualified power supply. Open ../Velluneo_specification_reset.kicad_pro or its .kicad_sch. The adjacent sym-lib-table resolves ../libraries/Velluneo_Driver.kicad_sym relative to the project; no third-party symbol library is required. Physical footprints are deliberately not assigned while exact pad/insulation/process choices remain unqualified.

## Actual deliverables

- Editable schematic and local symbols, with every approved physical terminal represented.
- Native exported Velluneo_driver.pdf and svg/Velluneo_specification_reset.svg.
- BOM.csv with28 physical components/requirements; custom transformer and internal wire terminations are explicitly not stocked MPNs. No JLC stock or assembly confirmation is asserted.
- Source generator generate_driver.py: deterministic capture from the pre-existing approved graph/parts, never an exporter that creates expected intent from the schematic.
- Fresh native connectivity, unsuppressed ERC, doctor, requirements and full-work-check records, with actual commands/exits in command-results.json.

## Circuit and source intent

The rectified mains supply includes250mA fuse,47ohm input limiter, MB10S bridge and15uF/450V bulk buffer. The isolated flyback candidate uses UCC28711DR, STN1NK80Z and a custom120:30:22 EFD25 winding. The primary is dot1→5, auxiliary dot2→4, secondary dot6→10. T1 unwound raw-bobbin terminals3/7/8/9 are explicit NC. DCL/TVS1 return clamp energy to BULK_POS. DAUX/RAUX and two470nF C0G capacitors provide the proposed bias supply. Output has STTH2R02A,10uF/63V SMD hybrid and two20kohm parallel bleeders.

J1/J2 are internal insulated-wire terminations, not the user-replaceable dock. Output18–27V/~250mA is the analytical candidate envelope, not a demonstrated rating. The primary return and isolated output negative never join. The single-sheet drawing is a connection document, not PCB placement; graphical distances do not establish insulation.

Actual owner acceptance of the exact independent pin graph is recorded in owner-intent-approval.md, digest b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57. That approval authorizes capture; it does not approve this newly generated schematic or its operation.

## Current checks and limitations

The native export compares successfully against28 components,73 terminals,21 nets and4 explicit NCs. Graph agreement is distinct from ERC, circuit simulation and physical tests. Final native ERC exits0 with zero findings after three documented, non-physical power-source declarations; see power-source-declarations.md. U1 types and physical graph are unchanged; no severity/exclusion/waiver is added. Native netlist export still warns about the approved nonnumeric role references; SCH-ANN-001 remains open, and no reference is silently renamed.

The standalone schematic requirements gate remains incomplete at U05–U09. The full work check cannot pass before managed rules/profile adoption and a real PCB; its configuration failure is preserved in check-work.json. No empty board or invented supplier confirmation is substituted. No PCB/DRC, routing, Gerbers or order is included.

RC-BIAS-001, RC-COMP-002, RC-MODEL-001, RC-CTRL-MODEL-001, RC-PROT-001 and retained input/clamp/service/thermal findings remain open at their original affected acceptance. Startup behavior, actual hot switching/clamp/SOA, winding construction/insulation, exact LED/current tolerances, faults, thermal and physical library/process verification are still needed. No laboratory measurement is claimed.
