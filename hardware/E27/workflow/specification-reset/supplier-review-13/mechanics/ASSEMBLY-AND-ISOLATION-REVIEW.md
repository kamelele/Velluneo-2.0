# RFQ13 assembly and insulation engineering review

The documentary and current-CAD review is complete for technical enquiry. Physical part
dimensions and finished insulation are not qualified by this review. The dimensioned PDF,
component-interfaces.json, assembly-calculations.json and official sources S1–S12 define
the exact facts, conditional calculations and supplier acceptance requests.

## Corrections completed in the current CAD

The former-only T1 reservation is replaced by a requested finished body of 30 × 30 × 18 mm
and a 30.5 mm courtyard. R10 moves 0.5 mm left; C3 1.5 mm left; R17 0.35 mm right and
0.4 mm down. The AUX_RAW corner moves 0.6 mm down. All 81 pin assignments, values/MPNs,
SENSE/CS copper and separate return branches are retained. Native ERC/DRC/parity pass.

Primary/secondary projected and common-layer copper separation is at least 10.725 mm.
With the retained proposed 0.35 mm finished-growth allowance on each domain, the remaining
budget is 10.025 mm. This closes the earlier arithmetic shortfall under that explicit
assumption. It does not establish a manufacturer's tolerances or an IEC minimum.

The 3 mm HV/quiet rule is a common-copper-layer screen. STARTUP_MID on B.Cu and VDD on
In2.Cu overlap in projection within the primary domain. This requires confirmation of
minimum pressed dielectric and functional dielectric/coupling assessment. It is not a
P/S crossing or an invented all-layer 3 mm clearance. The separate all-layer P/S audit
includes physically present NC pins. All board zones are exclusion areas, not omitted pours.

C1's maximum 10.5 mm case circle contains no unrelated B.Cu copper. Reserve at least
2 mm free space beyond its vent. The requested maximum mounted body height is 22.5 mm
and the service envelope is 24.5 mm from the bottom PCB face. Sleeve/PET is not credited
as reinforced insulation. F1 and C4 are SMD; F1 has no insertion leads or holes.

## Dimensions and forming: documentary closure and supplier hold

TDK's raw former drawing establishes 12.9 mm maximum height and 3.5 ± 0.2 mm pins, not
the complete wound, clipped and sleeved transformer envelope. The 30 × 30 × 18 mm finished
envelope is a procurement limit requiring a returned drawing/STEP and first-article check.
PCB thickness is 1.44–1.76 mm. Flush mounting leaves 1.54–2.26 mm pin tails; adding a
blanket 2 mm spacer can leave −0.46 to +0.26 mm and is excluded.

Q1 proposal Q13-FORM-A requires incoming usable leads ≥13.0 mm, a specified datum,
root straight 3.70–3.80 mm, inside bend radius 0.70–0.75 mm and offset 5.08 ± 0.05 mm.
The worst calculated developed length is 12.745752 mm, leaving 0.254248 mm only if
the incoming screen is met. This is not a datasheet guarantee. The supplier must return
selection yield, jig/formed drawing and a first-article fit. No pin reassignment is allowed.
R1 requires supported forming, body-bottom height 5.0–5.5 mm and maximum body top 13 mm.
BR1 requires supported forming to the native 5.5 mm square pattern and 3–4 mm standoff.
C1 must fit without lead or seal strain; exact lead diameter/position limits remain open.

## Transformer insulation and mounting disposition

T1.3 remains primary; T1.7/8/9 remain secondary. These physical terminals are unwound,
without hidden junctions. Core and yokes are treated as primary. Intact secondary TIW
must continue into controlled terminal zones; bare secondary wire cannot cross primary,
core or yoke regions. The proposed winding build is a reference for supplier review,
not an accepted electrical insulation system. Unspecified resin, enamel, soldermask,
PET sleeves and an unqualified 0.5 mm wall receive no reinforced-insulation credit.

The builder must return exact core/yoke and secondary exit/strip sections, insulation
materials and qualified process, full pin pattern, finished dimensions and a proposed
test basis for review. No unavailable standards table or test voltage/duration is invented.
The PCB manufacturer must confirm laminate/pressed dielectric, hole position/registration,
finished annular rings and filled/capped-via process, and return production films.

These supplier responses are explicit open acceptance inputs in supplier-response-checklist.csv.
No substitution, terminal change, relaxed spacing or production start is authorized by
the enquiry. Housing retention, complete-lamp fit/thermal performance and powered
startup/fault/insulation qualification remain outside the bare-board request. Parent
requirements are retained. Agent reviews do not replace real stage/release approval.
