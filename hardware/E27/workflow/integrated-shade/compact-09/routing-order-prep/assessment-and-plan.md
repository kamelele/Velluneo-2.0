# SC09-ROUTE05: bare-PCB prototype fabrication preparation

Base: d011ef6a865f6dd7f06825f233b2465238ecba27, SC09-ROUTE04. Same branch; main is outside the write scope. The owner requests a bare JLCPCB laboratory prototype with manual assembly, not JLCPCBA, an assembled production lamp, a purchase or powered operation.

## Findings and bounded corrections

The strict geometric screen contains 12 copper-edge findings and 23 different-net findings. Five pad-pair conflicts are intrinsic to the unchanged SO-8, bridge and SMA lands: U1.3/4 approximately0.67mm, U1.2/4 approximately1.94mm and BR1.1/3,BR1.2/4,D1.1/2 approximately1.50mm against the proposed2mm functional surface target. Routing cannot make a1.27mm SO-8 pitch exceed2mm. The prior bounded package assessment is engineering evidence, not an approved standards waiver. Preserve both strict and bounded reports and assess the exact local geometry; do not lower global rules or claim these conflicts disappeared.

Eliminate avoidable edge failures with a minimal outline proposal51.2x33mm, at99.4..150.6/99.4..132.4mm. This changes the earlier50x32mm footprint by1.2x1mm and requires review of the resulting concrete packet. Keep all component pads, exact circuit and parts. Extend the capacitor body copper reserve into the added strip, preserve the physical5mm vent-face air condition, and inspect new edge geometry.

Move the ordinary through-via out of D1.2's SMA solder land. Use a short centred approach and preserve the output return topology; no filled/capped via process is proposed. Move the bottom230V legend away from the RF1 solder-mask aperture. Audit all remaining mask/silk/annular/hole/edge distances against published JLCPCB bare-fabrication limits. A same-net shared solder opening is an explicit manual assembly detail, not a different-net insulation concession.

## Verification and procurement

Check exact MPNs and native lands against primary datasheets; current distributor structured data is availability evidence, not reserved stock. Do not replace LYT1603 with LYT1604 merely because the footprint matches. Retain the same electrical design if the exact part can be sourced. Parts may be purchased separately; JLCPCB receives only the bare-board Gerber/drill package after a separate actual ordering instruction.

After the private implementer relinquishes its lease, the coordinator independently verifies the allowed diff and adopts the candidate. Repeat native ERC/DRC/parity, physical pin sets, refill freshness, full pair matrix, Kelvin/negative controls, source consumers and manufacturing dimensions/counts. Generate current native layer views, assembly drawings and3D, source-bound manufacturing ZIP and manual parts/assembly checklist. Four distinct independent roles inspect one frozen packet. Record stage gates honestly; do not invent human acceptance or physical qualification.

## Release scope

The inherited full-product requirements include enclosure, optics, actual electrical/thermal/surge/EMC/insulation measurements and human approvals. Those are not measurements that can be completed before fabricating a first unpowered sample. Preserve them as full-product/bring-up gates. Report bare-fabrication capability separately; do not relabel full Toolkit releaseFAIL asPASS or manufacture local assembly-provider confirmation. A final human release decision must cover the exact new dimensions, local package-spacing assessment, manufacturing artifacts and prototype-only scope.
