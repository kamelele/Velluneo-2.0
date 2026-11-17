# Review report — PCB-READINESS-01-SIMPLICITY

- Date: 2026-11-17.
- Task / product stage: PCB-READINESS-01, bounded calculation and design-input development during schematic/library work; not complete schematic or PCB acceptance.
- Role: Overengineering Reviewer.
- Actual reviewer actor/context: `/root/ready_simplicity`, separate from the coordinator and startup, clamp and insulation implementers. Product repository remained read-only; this report is outside it.
- Declared base: `b1117ae2caecc037d9fc1253bd9c3a3c4effaaf2`.
- Final reviewed input: 87-member frozen body `9ade792922910aef78b194aa5eaaff6a3f73ac368f9d96fd0728b86dfb042956`.
- Recommendation: **ready_for_human_review for this bounded design-input packet only**. Complete schematic acceptance and PCB entry remain blocked. This recommendation is not a human approval, compliance finding or physical-test authorization.

## Scope and evidence

Read the project AGENTS.md, exact toolkit project instructions, existing-project guide, workflow, Overengineering role and common review template. Inspected the current product intent, task contract, proposed design contracts, source inventories, all five subject summaries, fault obligations, PCB-entry ledger and actual saved check results. Relevant requirements are R-SUPPLY/R-FAULT/R-EMPTY/R-THERMAL/R-BASE-LIFE/R-OFFLINE/R-ENV/R-REPLACE/R-SIZE/R-BUILD and U05–U11. Inspected the original product direction toward a simple isolated driver, passive replaceable LED panel and offline service, including the explicit condition that simpler architecture must preserve fault and residual-energy behavior.

Ran `verify_packet.py`: all87 member bytes verified against the final body. Independently checked the tracked diff against the declared base: only project-index.md and hardware.json differ among original files. Parsed old and current hardware.json and verified every field except source_files is identical, every previous source entry is retained, and all24 added entries exist. No changed rule, physical component, value, library, approval or requirement threshold is hidden in configuration adoption.

Independently summed the thermal allocations to4.0W and inspected model/script sizes: service-energy23lines, packet verifier9, clamp128, isolation42, startup122, native NTC curve47, startup verifier17 and thermal57. These are local purpose-specific analyses rather than a new application/framework. Actual saved check exits are thermal/service/startup-verification/doctor/connectivity/capture/ERC0, requirements1 and work-check2. I inspected these records; I did not rerun CAD or energized hardware and do not represent report inspection as physical validation.

## Proportionality of the proposed solution

Retaining R10/RAUX4.7ohm is proportionate. The old arbitrary auxiliary conduction fraction has been replaced by a coupled current solution; the matched2.2ohm comparison gains only12.9mV in the declared witness. That does not establish a useful need for a new value/ECO. The packet keeps native-controller, source-bias, AC-start and parasitic limitations visible rather than adding an external HV feed merely to repair a simplified calculation. Any future change still requires the actual source-conditioned requirement and affected checks.

Retaining the current clamp is also appropriate within this scope. The piecewise passive model distinguishes leakage-only transfer from full magnetic-energy diversion; lowering clamp voltage is not presented as a free improvement. Proposed20uH effective leakage and0.40W normal TVS allocation are measurable design conditions, with a declared normal-power hypothesis and explicit three-winding/fault/thermal gaps. They are not claimed characteristics of a purchasable or built transformer. Actual winding feasibility and source-conditioned hot dynamic behavior remain acceptance conditions.

Keeping the existing NTC while identifying its open fault is preferable to an unsupported substitute or extra component. The packet does not remove protection to reduce BOM, claim the controller's high typical shutdown protects all parts, or suggest that a shunt across the same NTC can create fail-low open-circuit behavior. Passive safety without NTC or a genuinely independent backup ECO remains required. This is an unresolved product obligation, not evidence that the current design is safe or that an extra circuit is unnecessary in the final product.

The material-system candidate reduces ambiguity without inventing qualification. FIS-B3, the two P/A wraps, retained four-wrap envelope and explicit supplier/material/exit-path conditions reuse the current core and pin map. The wider alternate winding band is rejected pending evidence rather than introducing another undocumented mechanical variant. The revised build can affect leakage, capacitance and AL; unchanged outer envelope is not used to waive those checks. No unconfirmed supplier capability is imported from source drawings.

The thermal and post-unplug analyses use the simplest useful networks: two passive heat nodes, component allocations, manufacturer-specific life screens and total stored energy plus cooling sensitivities. These expose concrete physical requirements without adding an unnecessary simulation platform or calling inverse budgets achieved performance. No generic potting, arbitrary thermal spacing or universal100s service wait is introduced.

## Reuse, duplication and retained gates

Two saved startup resolutions, corresponding worst trajectories and logs are justified by reproducibility and convergence inspection. Their85.7KB result files retain compact case summaries rather than every integration sample. The clamp stores reproducible grid identity/extrema and finite-R cases instead of a redundant full large grid. Prior analysis remains historical at its unchanged source scope. No need to remove evidence or consolidate independent analyses was found before publishing this bounded packet.

Manufacturer PDFs stay external with identities; actual-byte versus web-only/historical limitations are stated. The expired standards rendering is not adopted as numerical design evidence. I did not extract restricted machine text. No approved standard minimum, complete material recognition, real thermal path, measured leakage, controller model or supplier process is inferred from similar footprints or a source label.

**New bounded-task blocker/major/minor findings: none.** No mandatory simplification is proposed. The remaining native-controller/fault/NTC-open, transformer/material/process/core-to-terminal geometry, normative insulation, actual enclosure/thermal/lifetime, SOA and complete service obligations retain their stated owners and schematic/placement/routing/release gates in pcb-entry-contract.json. The requirements/work failures remain material product-stage blockers. No majority vote, reduced BOM or numerical convergence can close them.

The candidate contains no physical CAD delta, so earlier native geometry/intent evidence is reused only at its unchanged scope; this report does not refresh old functional or complete-stage approvals. A changed future circuit, winding, enclosure, process or thermal contract requires affected rechecks and review against the new exact packet.
