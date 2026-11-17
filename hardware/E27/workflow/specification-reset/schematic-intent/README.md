# Driver physical-pin intent — review packet r1

2026-11-17. One complete isolated flyback candidate,28 components,73 physical terminals,21 nets,4 explicit unused bobbin terminals. Sole shared writer: coordinator. GroupA source work by/root/model_compatibility and groupB by/root/support_design are implementer inputs, not independent reviews. No schematic or PCB has been generated from this graph.

Owner scope acceptance is preserved in owner-scope-acceptance.md. This new pin graph was created after that decision; approval remains null. Proposed exact intent digest: `b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57`. Review the readable parts-and-pin-map.csv and native pin basis alongside the full JSON.

The input is E27 230Vac nominal. F1/RIN/BR1/CBULK supply an isolated UCC28711DR+STN1NK80Z flyback. Proposed T1 is120:30:22 turns on EFD25/13/9; secondary and auxiliary rectifiers conduct during flyback off-time. Two0.47uF C0G capacitors supply VDD. Separate primary and isolated returns never join. TVS/steering-diode clamp returns to BULK_POS. Gate-source pull returns to the sense/source node. CS and controllerGND require a Kelvin layout; a net graph alone cannot demonstrate it. Outputbleeders20k+20k parallel and10uF hybrid cap are on isolated output.

## Source-derived corrections

- MB10S-13 native1+,2AC,3−,4AC; do not inherit the genericMB2S numbering.
- UCC28711 functionalHV7 is at the upper-right position, with a physically absent lead below. Generic mechanical appendix calls the geometric position8. The functional top-view table controls this proposed electricalgraph; custom library/land mapping must preserve the vacant position and be independently checked.
- STN1NK80Z tab is physical electricalpin4D, connected withpin2D.
- Panasonic outputcap is SMD V-chip6.3x5.8mm,105C max; not a radial5mm-pitch component.
- Diode1K/2A andcap1+/2−are explicitly local conventions, not invented vendor numbering.
- J1/J2 are internal insulated-wire solder terminations, not the user panel dock; tool-free/keyed/50cycle dock remains a placement contract.

## Actual checks and limitations

Inventory-check verifies unique complete terminal coverage, non-singleton nets and explicitNC. It is not nativeKiCad connectivity comparison, ERC, DRC, simulation or physicaltest. Final current tolerance and LED selection, startup current/charge, dynamicclamp/SOA, exact winding insulation and all prior major findings remain open for affected schematic acceptance.18–27V/~250mA is the analytical candidate envelope, not demonstrated rating.

Existing RC-BIAS-001,RC-COMP-002,RC-MODEL-001,RC-CTRL-MODEL-001,RC-PROT-001 retain their severity/history. No false major closure permits progression. No manufacturing output or order is authorized.

## Next permitted step

Four independent reviewers inspect this same frozen packet. Fix any resulting discrepancies before owner review. The rootAGENTS.md and pinned project instructions require real acceptance of the new independently prepared physical-pin intent before schematic generation; previous scope acceptance cannot be reassigned to this new digest. After genuine graph acceptance AND completion of the specification-stage gate and applicable pre-capture interface prerequisites, capture a draft nativeKiCad schematic and local libraries, then compare physical membership, runERC and assemble the next stage packet. Draft capture does not certify operation or waive later technical majors.
