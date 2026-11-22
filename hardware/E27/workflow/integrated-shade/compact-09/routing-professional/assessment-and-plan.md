# SC09-ROUTE02: orderly routing and opposite-edge terminals

The owner rejected the irregular bends visible in the ROUTE01 layer view and the input/output lands grouped along the lower board edge. The correction starts from immutable commit2327c0c2a86f98fac59d7e93f4e6a222c44ef444; its full packet remains available. `before.json` records the exact136 copied source hashes. Main remains outside write scope.

## Concrete defects

1. The previous line-of-sight simplifier tested clearance but allowed arbitrary segment angles. It reduced total track length while retaining visible multi-angle kinks and short intermediate flats. Clearance and connectivity checks alone do not establish an orderly routing geometry. Replace those shortcuts with planned axis/45degree paths and a separate angle/junction audit. Short package escapes must be individually bounded, rather than excusing long irregular routes.
2. J1 and J2 were both near the lower edge. The two wire-land footprints also contain diagonal pad offsets inherited from earlier crowding. That arrangement does not satisfy the owner's requested opposite-side wiring. Put mains input at the right edge and LED output at the left edge, orient the land pairs for outward wire access and label them. Changing bare-land spacing is a mechanical correction; it must not change electrical pin numbers or nets.
3. Merely moving J2 into the left capacitor projection would violate the selected both-face C6body/vent restriction. Coordinate the capacitor, formed leads, power-stage cluster and ports before routing. Use maximum physical body dimensions and explicit external vent clearance. Do not silently waive the body restriction or claim finished-lamp fit.

The fresh read-only baseline audit records55 non-axis/non45degree segments outside actual same-net pads, one acute two-track junction outside pads/vias and a minimum AC-to-LED terminal-centre distance of5.11mm. These metrics identify the geometry being corrected; terminal-centre distance is not electrical clearance or proof of insulation. The prior circuit, bounded electrical spacing checks and same-net Kelvin audit remain separate evidence.

## Implementation sequence

Preserve the previous source packet, define the corrected placement/terminal contract, inspect actual maximum-body/courtyard/pad geometry, preview and apply the pinned Toolkit configuration. The private implementer has the only CAD lease for `.work/routing02`; root owns later active-source adoption. An independent geometry contributor may inspect and recommend but cannot edit that candidate.

Route the direct C5 bypass and source paths, R5 force/Kelvin branches and compact power cluster deliberately. Route the input network toward the right edge and output/bleeders toward the left. Use a small number of meaningful45degree bends; do not substitute an arbitrary-angle straight-line simplifier. Preserve all electrical spacing floors and the original functional circuit/MPNs.

Require saved native ERC/DRC/parity/unconnected0, independent physical-pin equality, all55 bounded pair screens, saved-fill freshness, spatial/consumer agreement, actual Kelvin intersections and an independent angle/port audit. Inspect actual layer and native3D views for both faces before freezing the packet. Four distinct read-only roles review the same frozen engineering revision; findings require observable closure.

Refresh native source-bound exports, renders and the corrected engineering packet, then publish on the existing branch. Prior thermal predictions are not qualified measurements; strict spacing failures and full Toolkit human/physical/process gates remain visible. The task does not authorize an order, supplier message or powered test.
