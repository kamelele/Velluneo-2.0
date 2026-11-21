# C16 — actual catalogue-part driver PCB candidate

Open **design/Velluneo_driver.kicad_pro**. Actual revised33-position80-pad,
45x60mm four-layer schematic AND fully connected PCB. MYRRA74032 is factory
wound; STFW2N105K5 has straight factory leads. R4/R5/R6/R9 updated. Native
ERC0/DRC0/parity0/unconnected0 at saved checks; independent pre-capture graph agrees.
See engineering-change.md, calculations.json, selected-bom.json and checks/.

This is a review candidate, NOT an order release. Transformer fault static-rating
incompatibility and Q1 copper geometry have design corrections. Fault peak timing,
actual shoulder/assembly fit, magnetic/clamp characterization and process/product
qualification remain explicit in bring-up-and-assembly.md and toolkit gate reports.
Revised human intent/spatial/stage approvals are absent; never infer them from the
owner's authorization to implement. Historical RFQ13/JLC14 packages are stale forC16.

preview/C16_both_faces.png shows saved outer-layer copper from both sides;
preview/C16_inner_layers.png shows the two inner copper layers. These are CAD
diagrams with explanatory labels, not assembled3D renders or manufactured photos.
The corrected T1 component-side pin ordering is explicitly verified in checks/.
No simulation, measurement or stage approval is fabricated.
