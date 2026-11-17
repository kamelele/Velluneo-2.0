# SCH-CAPTURE-01: authorized draft schematic capture

Inputs: owner-approved physical-pin intent b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57, published0b79ac05d025fdcde1de0418874043a2d5f530b2, r12 accepted scope and source-derived parts/pin contracts. No graph changes are authorized by implementation convenience. Sole CAD/library writer:/root. Bounded support auditor:/root/support_design, read-only shared sources. Four distinct review contexts remain Reality, Overengineering, Completeness and Change.

Allowed new sources: native root schematic/project, libraries/Velluneo_Driver.kicad_sym, sym-lib-table, schematic-capture generator/BOM/views/reports/lifecycle. Allowed metadata: actual graphapproval field only, hardware source inventory, current indexes. Preserve oldCAD/libraries and all analytical major findings.

Acceptance for this bounded capture task: actual KiCad10.0.6 opens/exports schematic; exact28-component/73-terminal inventory matches human-approved independent graph with fresh installed connectivity report; record actual unsuppressed ERC; render PDF/SVG and inspect legibility; export exact BOM with unresolved custom winding/internalwirepad/footprint choices explicit. No blank PCB or invented rule confirmation may be used to obtain a false full-stage pass.

This is draft schematic capture within an incomplete schematic stage. U05–U09 interface/implementation/physical-library and circuit/model majors still block stage acceptance. Do not claim working/safe/manufacturing-ready supply from graph or ERC. No physical testing is possible here. NativePCB/placement/routing and final manufacturing package follow their real later gates.
