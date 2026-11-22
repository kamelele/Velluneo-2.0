# SC09-ROUTE01 corrected routing packet

Current native source: hardware/E27/variants/integrated-shade/SC09_compact. Functional circuit/MPNs remainCAT01; routing isROUTE01. Exact before checkpoint:f7074024129f5b7890427ed463ec0c085617ace0, preserved in ../przed_poprawkami. Earlier catalogue-package is historical.

Read SC09_routing_review.pdf, checks/before-after-metrics.json, SC09_layers.pdf and both native3DPNGs. Fresh checks: ERC0,DRC0,unrouted0,schematicparity0,46pin/11net equality, bounded55pairsPASS, KelvinsemanticPASS with negativecontrols. Strict intrinsicpackage screenFAIL is intentionally retained.

PCB50x32x1.6mm,2L1oz. C6maximumcan extends0.25mmleft; externalvent requires2.5mmfreeair abovePCB. Approximate19.5mmassemblyheight is a planning envelope, not inspected sample qualification. Source thermal copper has changed; no inherited U1temperature prediction applies.

SC09_ROUTE01_Gerbers_drills.zip has7layers+2drills,27PTH/0NPTH. Assemblypositions are manual reference, not a qualified automaticPCBAfile. Native embeddedVRML includes all17electronicmodels. Illustrativemodels are not manufacturer-certified fit. FullcomponentSTEPassembly remains unsupported; no misleading assemblySTEP is supplied.

FullToolkitproductreleaseFAIL: genuine exactstage decisions, provider/process confirmation and physicalcurrent/OVP/thermal/fault/EMC/insulation tests remain open. This packet is an engineering review result, not an unconditional order/use release. No purchase or supplier communication.
