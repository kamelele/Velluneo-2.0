# ECO-01 — owner-authorized native KiCad capture

2026-11-17. RevisionSCH-ECO01-02. Base remote commit4d8dcfc671b4963a55b342409b8d75fd0bf1439b. The owner approved the exact pre-CAD ECO-01 map in this conversation: [actual decision](owner-intent-approval.md). Accepted intent digest5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8;31physical components,79terminals,22nets,4explicitNC pins. This is **implemented schematic capture**, not a completed/qualified supply or schematic-stage acceptance.

## Applied change

- FormerRB1/RB2 are nowR2/R3:499kohm CRCW2512499KFKEG, using the existing native-source2512 footprint instead of1206. Their series branch remains BULK_POS→BLEED_MID→PRIMARY_GND.
- R14/R15 add an independent identical499k+499k series branch, through separate BLEED_MID_B. The common rails/trace fault scope still needs layout/safety review.
- R13 CRCW06031M00FKEA adds1Mohm fromVDD toPRIMARY_GND; its startup-budget effect is already calculated separately in the accepted ECO preparation packet.
- Existing R/C/D reference aliases are exactly those reviewed in electrical-integration/reference-aliases.json. Other active-device/controller/sense/clamp/bulk/transformer values and every existing physical pin membership are preserved after aliasing. The old native annotation warning is absent in the fresh export.

No new footprint shape or symbol pin type was invented/relaxed: existing18 local modules are reused, all now assigned to31positions. No physical PCB was created, no copper routed and no DRC/parity/manufacturing claim is made. Panel dock and transformer finished construction remain unqualified.

## Actual checks

| Check | Result | Scope |
|---|---|---|
| Installed toolkit doctor | Exit0; locked Ubuntu26.10/KiCad10.0.6/pcbnew10.0.6, preview0.7.1-preview.3 | Actual tool environment; not product validation. |
| Native library verification | Exit0;18unique modules,31assigned positions,79mapped physical terminals | Exact numbered copper/layers/drills/size/position versus independently prepared library geometry contracts. Process/insulation/thermal qualification remains. |
| Intended graph versus native schematic | Exit0;79pins/22nets/4NC, approved ECO digest matches | Every physical membership checked. Exportstdout/stderr empty; prior annotation warning no longer reported. Not function/physical isolation. |
| Independent part/MPN/footprint/BOM contract versus nativeXML | Pass;31components/79terminals | All source-part numbers and footprint assignments agree with the pre-CAD inventory, including four2512 bleeders and0603 bias bleeder. Does not prove supplier stock. |
| Native ERC, all severities | Exit0;0reported enabled-check violations | Recorded default ignored-check list retained; project settings/severities unchanged. |
| Native PDF/SVG export | Exit0, one A3 sheet | Saved-source views; root inspected rendered sheet. |
| Requirements, schematic stage | Exit1; U05–U09 unresolved | Actual incomplete-stage result; no waiver or changed requirement threshold. |
| Full work check, schematic stage | Exit2,configuration_error | Managed profile/rules/ownership adoption and actualPCB remain incomplete; full check not passed. |

Complete commands/stdout/stderr:command-results.json. Independent native graph report:connectivity.json. Actual defaultERCignoredchecks:erc.json. All existing RC-BIAS-001,RC-COMP-002,RC-MODEL-001,RC-CTRL-MODEL-001,RC-PROT-001,RC-INPUT-001 and electrical-integration findings remain open except the narrowly scoped native annotation warning, subject to independent closure review. ECO implementation does not by itself close the discharge/system-safety findings.

## Current files and historical evidence

- [Editable native KiCad bundle](Velluneo_driver_ECO01_KiCad.zip): project, schematic, local symbols/footprints/tables, currentBOM and exact approved graph/source basis; open Velluneo_specification_reset.kicad_pro in KiCad10.0.6.
- [Native schematic PDF](Velluneo_driver_ECO01.pdf), [rendered sheet](Velluneo_driver_ECO01.png), [input detail](input-discharge-detail.png), and nativeSVG in svg/.
- [Current BOM](BOM.csv):31positions with exact candidateMPNs/footprint mapping, not supplier-readyBOM or availability evidence.
- Active independently prepared parts inventory is **electrical-integration/proposed-parts.json**. Its filename is historical: actual owner approval is now in the active canonical graph. The original schematic-intent/parts.json must remain immutable because it is a hashed historical basis of this exact accepted graph, along with the newer overriding independent ECO parts. Neither is derived from KiCad.
- Active graph is schematic-intent/intended-connectivity.json; only its approval metadata differs from the pre-decision proposed graph. The proposal file and complete electrical-integration packet remain unchanged as historical review evidence. Their approval=null correctly records the former review state and is not the current active decision.
- schematic-capture/generate_driver.py now uses the exact accepted ECOgraph/parts and writes this currentBOM; it reproduces the source deterministically. Older captures, PDFs, ZIPs, hashes and reviews are historical for their own revisions. Do not relabel their28-position reports current.

The editableZIP is a standalone KiCad draft and evidence subset, **not the installed toolkit repository**. Full launcher/configuration/rules checks must run in the device repository with its actual locked dependency; unpacking theZIP alone does not install that environment. Review/manufacturing/physical-test authority is not included in a file package.

## Engineering limits and next work

The dual bleeder adds~.128W at high-line crest; selected single-resistor-fault RC/rating calculations from electrical-integration/results.json remain conditional. No complete user waiting time is determined. Open items include startup/gate/aux dynamics, hot dynamicclamp/SOA/surge/fault/recovery, full input capacitor ripple, finitewinding/AC/core/aux loss propagation, all-corner current/flux regulation, interface/thermal/lifetime and physical construction/process evidence. See the inherited finding ledger; no additional product direction is needed merely to continue these design tasks.

No physical measurement occurred here, no university instrument is connected, and no fabricated supply has been tested. The next work is to resolve those technical findings while maintaining the accepted architecture; a material architecture change would be presented as a concreteECO. Placement/routing requires completion and actual approval of the schematic stage and independent spatial intent, not another approval of this already acceptedECO.

## Reproduction

From the repository: use the installed pcb-toolkit.py launcher/locked runtime, doctor first. Execute schematic-capture/generate_driver.py only when actual intent approval/basis hashes match. Verify footprints with footprint-completion/verify_native_library.py OUTPUT_JSON (writes only that output). Run connectivity, nativeERC/PDF/SVG, requirements --stage schematic and check --mode work --stage schematic as recorded in command-results.json. Run eco01-capture/verify_capture.py against the fresh native XML for independentMPN/footprint/BOM checks. Run eco01-capture/package.py after saved source/checks to rebuild images and the deterministic editableZIP; PyMuPDF is required for raster views. The ZIP excludes itself, reviews and frozen lifecycle manifests to avoid recursive hashes. Package creation is not manufacture or release approval.
