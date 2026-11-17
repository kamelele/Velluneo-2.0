# FOOTPRINT-01 — three native critical footprint candidates

2026-11-17. This is schematic/library work within the still-incomplete schematic stage. It creates actual local `.kicad_mod` files and assigns them to U1, BR1 and Q1. It does not create or approve a product PCB, placement or manufacturing release.

| Reference | Exact part | Native local footprint | Physical terminals |
|---|---|---|---|
| U1 | UCC28711DR | Velluneo_Driver:UCC28711DR_SOIC7_HV7 | 1–7; functional HV7 at the top-right geometric position; vacant position retained |
| BR1 | Diodes MB10S-13 | Velluneo_Driver:MB10S_Diodes_MBS_1P_2AC_3N_4AC | 1+, 2AC, 3−, 4AC |
| Q1 | STN1NK80Z | Velluneo_Driver:STN1NK80Z_SOT223_Tab4 | 1G, 2D, 3S, 4D-tab |

The three modules are in ../libraries/Velluneo_Driver.pretty and are resolved through ../fp-lib-table. Open the current root KiCad project to inspect their schematic assignments. Native SVG exports and PNG renderings in this folder show the actual footprint geometry, not a fabricated PCB screenshot.

## Source and engineering choices

Native manufacturer documents and exact saved hashes/pages are recorded in native-ucc-mbs-basis.md, native-ucc-mbs-geometry.json and native-stn-basis.md. TI's land-pattern example uses metric pad dimensions1.55×0.60mm, columns5.4mm and pitch1.27mm; the right-side HV–DRV gap remains2.54mm. Diodes' MBS suggested pattern gives1.00×2.15mm pads,2.50mm column spacing and derived5.35mm row spacing. ST's recommended SOT223 pattern gives three1.2×1.5mm lands and a3.3×1.5mm tab,2.3mm pitch and6.4mm row spacing. Native ST tab4 is preserved instead of merging it into pad2.

Coordinates use a project-chosen centered component/top-side frame, X right and Y down. geometry-contract.json distinguishes native copper dimensions from project choices. Body outlines use recorded maximum dimensions and a centered display convention, not a 3D/measured model. Rectangular copper corners are an explicit project choice where native radius is unspecified. Courtyards are provisional handling envelopes, not electrical insulation distances or confirmed assembly clearances. Mask/paste layers are present without explicit margin/reduction overrides; final fabrication/assembly profile selection and mask/paste qualification remain open. No soldering yield or high-voltage withstand claim follows.

## Actual checks

- Genuine pinned KiCad/pcbnew10.0.6 doctor and footprint parsing pass.
- Native pad number, count, exact coordinates, sizes and SMD/layer inventory agree with the source-derived contract: U1 seven pads, BR1 four, Q1 four including the drain tab. Reserved courtyard body/pad containment is checked; it does not establish board clearance or component-placement fit.
- Fresh installed physical connectivity comparison passes the unchanged owner-approved graph:28 components,73 terminals,21 nets and4 explicit NCs.
- Native ERC exits0 with zero reported findings under its recorded default checks; source declarations and truthful U1 types remain unchanged.
- Native footprint SVG and updated schematic PDF export succeed. The coordinator visually inspected the rendered footprint exports.
- Schematic requirements still exit1 at U05–U09; full work check still exits2 for incomplete managed configuration/rules/ownership and absent realPCB. Those failures remain in reports.

## Retained gaps

Only three of28 items now have these source-backed candidate footprints. Other footprints, the finished transformer's winding/pin-view/insulation construction, panel electrical and mechanical interfaces, actual board/enclosure fit, process confirmation and every existing electrical/model/thermal/safety major remain open. SCH-LIB-001 is partially addressed, not closed. Native nonnumeric-reference warning SCH-ANN-001 remains open; no approved reference or expected physical graph is silently renamed.

The earlier schematic-capture frozen report is historical for the initial capture: current schematic, generator, source inventory and BOM changed through this controlled footprint integration. Current evidence is in this folder and its frozen-inputs.json. Earlier bare-project ZIP remains an earlier artifact; use the new three-footprint package when available for these assignments. No previous report is relabelled current by changing its hashes.
