# PCB-PLACEMENT-02 — native driver placement improved

18 November 2026. Continues PCB-DRAFT-01 at cd5071af73a4fe66ed8bfd93a77f7445b3aa030f. The owner authorized continued engineering and GitHub publication. This is an editable, unrouted engineering draft, not accepted schematic/placement/routing or a qualified mains supply. Rectangular driver trial remains **32 × 60 mm**, 31 parts/79 pads, within the continuing whole-lamp target Ø60 × 120 mm; actual whole-assembly fit is not established here. Only the LED insert is circular.

## Open and inspect

Extract Velluneo_driver_PCB_placement02.zip and open Velluneo_specification_reset.kicad_pro, then its PCB editor. Matched schematic, rules, 31 envelope models and complete local symbol/footprint libraries are included. Repository library tables reference ../libraries; the portable copies reference included libraries. Native front/back SVG and actual native 3D renders are supplied. Models are allocated body envelopes, not qualified vendor STEP geometry; T1 is a 30 × 30 × 18 mm reservation, not a finished transformer.

## Concrete changes and verification

The full V4 placement is recorded in placement-proposal.json and applied with native pcbnew by edit_board.py. Existing copper lands, drills, mask, footprint definitions, circuit, MPNs, values and all rules remain unchanged. The actual copper-free rule area follows the moved domain pad extents, with the same flags/layers. Visible reference fields were repositioned, without hiding them, by place_references.py; the 16 moves are recorded separately. Two rejected coordinator-only proposal experiments were not adopted because they introduced courtyard conflicts. The final proposal matches the saved native board, verified independently for all 79 transformed pads.

Native DRC reduced 37 clearance findings to **8**, eliminating all **29 intercomponent** findings under the unchanged 3 mm screen. The remaining 8 reports are 6 package-internal pad pairs (PTH duplicates across copper layers): BR1.1/3, Q1.1/2 and 2/3, U1.6/7, T1.1/2 and 4/5. These are retained, not waived. Silkscreen findings decreased from 14 to **1**, an R9/RT1 graphic overlap. No text was hidden or copper/library geometry removed to clean the report. There remain **53 unconnected items and zero tracks/vias**. DRC exits 5; the board is not DRC-clean. Native schematic parity has **zero findings**, and all physical net memberships, 22 functional nets plus 4 singleton NC nets, values and MPNs match.

Independent scalar geometry checks find no same-face courtyard conflicts with 0.1 mm planning gap, opposite-face THT/courtyard conflicts with 0.4 mm joint allowance, semiconductor courtyards under the T1 allocation or outline overruns. Minimum pad edge is 0.55 mm. P/S projected pad-box minimum is 10.225 mm including unwound terminals; the earlier 0.35 mm-per-domain process proposal would leave 9.525 mm. These checks do not qualify actual assembly, tolerance, creepage, solid insulation or thermal paths. Opposite-face SMD projected HV/quiet gaps below 3 mm are listed separately; they are not common-layer air-clearance DRC failures, but solid-dielectric/coupling assessment remains open.

CS pad-centre distance improves 14.434 → 0.457 mm, gate resistor-to-gate 13.086 → 2.060 mm, drain 12.702 → 9.042 mm. These are unrouted centre distances, not measured electrical improvements. Clamp three external-leg lower bound worsens 41.541 → 49.600 mm (+19.4%); clamp layout requires further work before routing acceptance. The current V4 is not declared optimal. NTC location/thermal coupling is unqualified; prior assembly-fit or cooling claims do not transfer to this placement.

Fresh KiCad 10.0.6 saved-board parity, geometry, ERC, toolkit doctor and graph checks pass at their scopes. Schematic requirements still exit 1 (U05–U09); work check still exits 2 configuration_error. Full command records and raw reports are retained. No managed configuration, severity, exclusions, approval, requirement or waiver was changed.

## Electrical and insulation conditions remain explicit

The exact controller startup/fault/NTC limits, input coordination and magnetic/insulation proposals remain in PCB-DRAFT-01/design-contract.json and the earlier closure packets. This placement iteration does not create a guaranteed dynamic fault ceiling, retry time, RT1-open thermal protection, qualified transformer build, measured loss/temperature or lighting-standard approval. Actual construction, winding/yoke/TIW leadout geometry, tolerances and materials can require a footprint/placement revision.

The retained blanket 3 mm HV/quiet rule is an unresolved engineering screen, not an adopted normative lighting limit. AUX_RAW is bipolar during switching; low average auxiliary voltage is not a valid spacing basis. Source-specific functional voltage/waveform and object assessment is still needed for package and cross-face construction. No mask/coating credit or reduced exemption is invented. The unchanged 10 mm domain reservation similarly does not establish finished insulation compliance. No board order, manufacturing output, supplier contact or powered test is made.

## Review and next step

Root is sole CAD writer. Bounded read-only implementer handoffs are documented; four independent role reviewers inspect the same frozen packet. Their publication recommendation is distinct from human product-stage decisions. Next work is to resolve the remaining artwork collision and clamp placement tradeoff, justify functional/package/cross-face spacing with actual construction, then proceed under genuine schematic/placement/routing decisions. This packet advances the real PCB workspace while retaining all acceptance gaps.
