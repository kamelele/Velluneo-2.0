# FOOTPRINT-01 — source-backed critical physical libraries

2026-11-17. Device baseline f55cfde460fee8027adcbcd65d2211755b1f8a12. Scope is schematic/library work, not PCB placement. The user instructed continued work. Existing schematic-stage electrical/interface/safety and process blockers remain open.

Root is the sole writer of shared native libraries, schematic, generator and configuration. Implementer /root/model_compatibility inspects native UCC28711/MB10S land and terminal drawings; /root/support_design inspects STN1NK80Z. Their outputs are evidence inputs, not independent approvals. Four distinct existing reviewer contexts inspect the same frozen integration after execution.

Create three project-local candidate footprints with exact approved physical numbering: UCC28711 functional1..7 including upper-rightHV7 and absent adjacent lead; DiodesMB10S1+/2AC/3-/4AC; STN1NK80Z1G/2D/3S/4drain-tab. Preserve native mechanical/land pattern dimensions and distinguish source-recommended lands, arithmetic derivations and project choices. No datasheet ambiguity may be filled with an invented fact.

Acceptance for this bounded library task: source hashes/pages and view conventions; native KiCad10.0.6 footprint parse/load; independent pad count/number/coordinate/size checks and native rendered views; if assigned to schematic, unchanged human-approved physical graph and fresh ERC. Include every new local library/table in source_files. No generated rules, board outline, component placement, copper, release file or order is authorized by this task. Libraries remain candidates until independent source/assembly review; neither the task nor tool success qualifies insulation, thermal behavior, JLC process capability or the complete supply.
