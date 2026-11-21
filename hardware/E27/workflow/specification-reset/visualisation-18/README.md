# VIS18 - current C16 3D and copper views

Current45x60mm four-layer C16 PCB, matching C17manufacturing data. Native KiCad10.0.6
4064x3056 highquality raytraced (requested4096x3072; native renderer crop) top/bottom views and a combined presentation image.
All31 electronicpositions have appearance models; J1/J2wirepadpairs have no invented
harness. Two copper diagrams show allfourlayers; bottom is physically mirrored.
Componentreference labels on copper diagrams are explanatory overlays, not native silk.

Production CAD/manufacturing exports are unchanged. geometry-and-models.json binds
the exact source hash and proves33positions/80pads/333copperobjects unchanged using
native comparisons. Only model references/visibility and presentation plot selections
change in scene/Velluneo_C16_VISUAL_ONLY.kicad_pcb. Do not use it for manufacture.

The eight generic KiCadpackage models are retained from exact upstream tree
b8b3cfdfad88ba66f21002b3de51dc6f7d55ba5a with original headers and LICENSE.md
(CC-BY-SA4.0 plus upstream electronic-design exception). Other bodies are original
parametric appearance models. MYRRA74032 uses its current26.5x22.5x26.5mm reserved
envelope/ninepins; Q1uses its straightlead29.7mm height reservation and3mm shoulder
standoff. T1/Q1details, mountinghole, fuse/cap bodies are representative, not approved
supplierSTEP geometry or measuredfit. No artificial part marking or product photograph.

AllC16/C17physical/process/insulation/thermal/fault/firstfit/humanreleaseholds remain.
Rendering does not qualify assembly or operation. No suppliercontact/upload/order,
payment or poweredtest. This presentation task advances no engineering approval stage.
