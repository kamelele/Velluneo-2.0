# SB01 bare PCB: JLCPCB order preparation

## Use this one manufacturing archive

`SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip` is the unchanged, source-bound
eight-file manufacturing archive. Upload this ZIP only after acceptance of
SB01-FAB-LOCAL-01. Do not upload this entire evidence directory, a historical
SC09/SB02 archive, BOM, positions or KiCad source to the bare-PCB order.

The ZIP contains top/bottom copper, top/bottom mask, top/bottom legend,
one board outline and one PTH drill file. There are no NPTH holes in this
design, so the empty NPTH export is deliberately excluded. All eight member
bytes were compared to the reviewed native exports, and ZIP integrity passed.

## Settings

Choose FR-4, 2 layers, 1.6 mm thickness, 1 oz outer copper, lead-free HASL,
green soldermask and white legend. The outline is 51.2 x 33.0 mm. Select a
single design supplied as individual boards, with no PCBA or stencil service.
Request the factory continuity/short test. Quantity is the owner's choice.
No price, shipping method or actual order is agreed by this packet.
The supplied masks govern via openings; avoid an automatic override that
changes the reviewed artwork. No controlled impedance, blind/buried/filled
vias, castellations or edge plating are required.

These process choices are supported by the published JLCPCB capabilities
checked 24 November 2026: https://jlcpcb.com/capabilities/pcb-capabilities .
Factory fabrication limits are not electrical insulation acceptance criteria.

## Final supplier preview check

No supplier upload has been performed. In JLCPCB's processed-file preview,
verify 51.2 x 33.0 mm, exactly two copper layers, one rectangular outline,
matching PTH hits, both masks and both legends. Check there is no scaling,
mirroring, extra panel outline or missing drill layer. The preview is still
a pending order-time check, not a completed observation. Stop and resolve
any supplier engineering question before payment; do not permit an unreviewed
change to copper, drill locations or mask artwork.

## What is and is not closed

The existing native ERC/DRC/parity and source-to-Gerber geometry audit pass;
delivery integrity also passes. Native default ignored check keys remain
visible in delivery-verification.json; separate R1 geometry checks cover
via entries. No new native run is claimed for this unchanged-source delivery.

Five manufacturer land-pair constraints and 18 local approaches at BR1,
U1 and D1 remain below the generic 2 mm target. Strict comparison remains
FAIL23. Four independent roles reviewed the exact local-spacing assessment,
not an assertion that the finished board is safe to energize.

SB01-FAB-LOCAL-01 proposes fabrication of an UNASSEMBLED, UNPOWERED bare
laboratory test article only. Its explicit owner acceptance remains pending.
The latest continuation request is preserved verbatim in the delivery record;
it is not rewritten as an exact deviation approval. No order is submitted.
The full Toolkit release remains FAIL. Startup/surge stress, finished
clearances, operating temperatures and powered fault qualification remain
open; owner acceptance of bare fabrication cannot close those physical issues.

The conditional input-filter screen predicts roughly 706.3/588.7 V peaks
under simplified assumptions, not measured or guaranteed worst-case bounds.
This is why nominal 230 VAC and manufacturer land patterns alone do not
justify powered use. This packet does not authorize energization or live tests.

## Evidence and retained reviews

Reviewed assessment commit: e14abce13d5805f7a8d63d66b62abad921364b42.
See ../local-spacing-assessment-SB01/ASSESSMENT.md and its core/review manifests.
The complete unchanged R1 engineering evidence is at
../routing-verification-SB01-R1/README.md. The previous four-role assessment
reviews retain their geometry/stress/source scope because all source guards,
manufacturing bytes and frozen assessment inputs are unchanged. An additional
independent delivery check reviews this directory and its claims. Neither
retention nor that recommendation constitutes owner approval.

The packaging coordinator owns this directory; no shared CAD/library writer
is assigned because no design edit is required. The owner owns the pending
fabrication decision and quantity. Supplier processing review and payment
remain later actions; powered qualification is a separate task.
