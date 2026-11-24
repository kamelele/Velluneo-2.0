# Current engineering head: SB01 R2 RC correction (24 November 2026)

The [reviewed R2 package](startup-correction-SB01-R2/README.md) is adopted as an **unreleased engineering head**, after four independent reviews of core `ddb90c1270fbfce6e8b64862b64e442b1f56bc66d86071a32232ea3b73235e80`. [Integration record](startup-correction-SB01-R2/integration.json).

The physical legacy L1 slot now takes PR02FS0201000KR500 100 ohm/2 W resistor, not the old choke. Use the current R2 BOM CSV/JSON and R2 positions; inherited historical basket/critical-part wording is not R2 purchase authority. Same 51.2 x 33 mm, 19-position board, same copper and eight-file manufacturing ZIP. The passive RC calculation removes intentional input LC resonance, not surge/active-converter/fault/hot qualification. Strict spacing FAIL23 and full Toolkit release FAIL remain. No human acceptance, supplier upload, purchase or powered test is fabricated. SB02 remains inactive. Existing owner decisions below apply to their exact historical snapshots.

## Previous packet record (preserved)

# Current packet: SB01 R1 bare-PCB order preparation (24 November 2026)

Use the [current delivery instructions](bare-PCB-order-delivery-SB01/ORDERING.md) and [unchanged manufacturing ZIP](bare-PCB-order-delivery-SB01/SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip). The [local spacing assessment](local-spacing-assessment-SB01/ASSESSMENT.md) is complete for geometry/classification only. SB01-FAB-LOCAL-01 explicit owner acceptance remains pending; strict FAIL23 and full Toolkit release FAIL remain visible. No powered qualification, supplier upload, processed-file preview or order is claimed. All SB01 CAD/rules/manufacturing bytes remain unchanged from R1. SB02 is inactive. The historical decision below applies to its recorded snapshot, not a fabricated approval of this current proposal.

## Historical packet record (preserved)

# Current packet: SC09-ROUTE05

Corrected routing: [package](routing-order-prep/po_poprawkach/README.md), [assessment and plan](routing-order-prep/assessment-and-plan.md), [thermal and spacing limits](routing-order-prep/thermal-and-spacing-basis.md). Native sources remainSC09_compact with unchangedCAT01circuit.

Before checkpoint: d011ef6a865f6dd7f06825f233b2465238ecba27 / [before state](routing-order-prep/before.json). Catalogue-package and olderprototype-package are historical. Current PCB51.2x33mm, two layers; oppositeleft/rightports, C6caninsidePCB and5mmfreeairfromactualventface. Full Toolkit productreleaseFAIL remains explicit; no humanapproval/physicaltest/order fabricated.


Current lifecycle update22Nov2026: Kamil accepted the exact bare-PCB/manual prototype scope and disclosed local-spacing limits. [Actual decision](routing-order-prep/owner-fabrication-approval.json). The frozen source/native/fabrication bytes are unchanged; full-product release remainsFAIL, no purchase or powered test.
