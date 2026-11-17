# PCB-READINESS-01 — startup, protection, thermal and insulation

Continued from b1117ae2caecc037d9fc1253bd9c3a3c4effaaf2 on17November2026. This packet contains executed calculations and specific inputs for further design. **PCB entry remains blocked.** The31-component/79-terminal/22-net/4NC schematic, part values and libraries are unchanged. There is no new product PCB, routing or manufacturing package.

- [Startup and protection](startup-protection/README.md): coupled winding-current solution,64corners with4.7ohm and a matched2.2ohm comparison, at two numerical resolutions. Lowest calculated VDD11.6839V;2.2ohm gains only12.9mV in the matched comparison. Retain4.7ohm. This diagnostic does not contain a validated native controller model.
- [Clamp energy and transformer](clamp/README.md):1536analytic cases,16finite-R trajectories at two resolutions and9reference cases. Proposed effective T1 leakage<=20uH and TVS normal loss allocation0.40W under the declared normal scenario. Actual transformer parameters and fault pulse trains remain unverified.
- [Thermal design and lifetime](thermal/README.md): proposed thermal paths<=7K/W for4W driver loss and<=3.5K/W for8W light-compartment heat at40C ambient. Conditional node target68C; capacitor localair<=70C and actualcore-rise<=10K. These are physical-design requirements, not measured performance.
- [T1 insulation construction](isolation/README.md): concrete FIS-B3 material-system candidate and revised tape allocation with two P/A wraps. Worst proposed winding envelope remains2.293mm. Pad-row separation does not establish ferrite, leadout or core insulation.
- [Post-unplug energy](service-energy.md): conditional total stored-energy bound, including one open bulk-discharge branch.100s is an electrical calculation screen for the declared cases; no user waiting instruction is selected.

The exact manufacturer R/T calculation places electrical NTC trip at80.8–96.6C. A short commands shutdown; an open removes this external protection. Acceptance requires demonstrated passive safety with that fault, or a separately developed/reviewed backup ECO. No unsupported extra components were adopted to mark the issue closed.

The owner confirms no full standards access. A discovered61347-1 copy displays expired/member access; that restriction was not bypassed, and hidden table text is not adopted as a design basis. Normative separation and test requirements remain to be legitimately confirmed. The previous8mm planning reserve is not an adopted standard minimum. See isolation/standards-access-note.md.

[Exact PCB-entry criteria](pcb-entry-contract.json) bind new results and remaining obligations to owners and gates. Calculations narrow uncertainty; they do not substitute accepted schematic, transformer/enclosure drawings and confirmed insulation rules. U05–U11 or owner stage decisions were not changed. Fresh tool results and four independent reviews apply only to their declared scopes.
