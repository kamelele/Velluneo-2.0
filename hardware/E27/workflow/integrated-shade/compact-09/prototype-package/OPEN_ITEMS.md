# Current stage dispositions

## Closed design/fabrication preparation issues

- SIZE: actual owner accepts50×32mmPCB. Earlier25mmwidth deviation is closed; actual bulb cavity fit is still not claimed.
- LEGEND: eight texts changed to0.15mmstroke/1mmheight to match the checked fabrication basis.
- T1HOLE: all three native/canonical/declared holes1.20mm, same1.8mmlands and pin centres. Radialcoilposition tolerance≤0.15mm explicitly stated; residual declared fit screen≈0.029mm. Actual sample gauging still required before assembly acceptance.
- UPLOAD:9file supplierZIP excludes optional mismatching .gbrjob metadata. Lead-freeHASL, material/layers/thickness/copper/outline are explicit.
- REGISTRATION: existing six manufacturing artifact classes are registered with exact source snapshot and hashes. Raw hardware.json is excluded from source_files to avoid a self-hash cycle; its complete design configuration is still automatically bound by the pinned Toolkit. No approvals are invented.

See final scoped bare-board-readiness.json for actual independent closure evidence. Supplier CAM preview/quote/order are not performed by this repository work.

## Later assembly, powered investigation and product obligations retained

1. Coil supplier/sample:180turnAWG32EE10, geometry/gauge, inductance, hotDCbias, DCR, insulation and core loss. NRND IC availability and complete parts basket remain procurement risks.
2. Actual formed R7/RF1/C6 and soldered lead fit, support, vent volume and wire strain relief. The drawing contract is not an inspected assembly.
3. LED current/ripple/line/temperature regulation and actual optical output; nominal133.4mALED is a calculation.
4. DynamicOVP/C6peak, discharge, shorted IC/sense/diode/bleeder faults, coil saturation and MOV/RF1 surge/fusing coordination. No physicalPASS.
5. Component temperatures/losses and life. T1 thermal sensitivity can exceed90°C target at40°Cambient; change design if measurements fail.
6. Guarded test fixture/operator/probe limits, qualified insulation/EMC/safety basis and finished lamp contact/enclosure/cavity obligations. Instructions do not replace access barriers.
7. Full Toolkit product release retains unresolved spatial/provider/exactstage/evidence gates. A separate bare-board fabrication audit does not relabel that report as PASS.

No purchase, supplier message or powered test was performed. These remaining obligations prevent assembled-product or powered-use acceptance; they are not falsely declared measured before a barePCB prototype exists.
