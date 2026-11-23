# Overengineering review — SIMPLE-SB01-FINAL-01

Actual reviewer: `/root/simple_simplicity_review`, 23 November 2026. The implementation and component researchers are separate contexts.

Reviewed candidate: **SC09-SB01**, PCB SHA-256 `a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`. The frozen review manifest SHA-256 is `8035ba4c7b87abf9926d00b1b05ab22d21cbc5357870bcd294a8142d240c8243`; I independently checked all 166 listed file hashes with no mismatch.

Recommendation: **ready_for_human_review for procurement simplicity and proportionality only**. No new overengineering blocker was identified. This is not fabrication approval, an electrical qualification or a waiver of other open findings.

## Independent inspection

I loaded the preserved baseline and final PCB read-only with pinned KiCad 10.0.6. Both have the same 19 references, two copper layers and identical outline. Five positions changed: C1, C4, RV1, T1 and BR1. Six part values/identities changed: RF1, C1, RV1, R6, T1 and D1. The track/via count increased from 136 to 155; inspection of the handoff ties the affected routes to the changed packages and removal of sensitive routing below the magnetic body. Neither source was saved by this review.

The final procurement list has 16 unique MPNs and 17 fitted electronic positions. Seven MPNs are sourced from TME and nine from DigiKey. Independent decimal summation gives:

- Consumed components: 49.2161399 PLN net / 60.535852077 PLN gross.
- Minimum purchases: 59.1161399 PLN net / 72.712852077 PLN gross.
- Two deliveries in the declared budget: 115.50 PLN gross.
- One-build conditional total: **188.212852077 PLN gross**, approximately 190 PLN.

R6's minimum of 100 pieces accounts for 99 spare resistors and 12.177 PLN gross beyond consumed component cost. The earlier research cost remains explicitly historical; `integrated_cost_SBO1` matches the current arithmetic.

## Simplicity assessment

The two-basket approach is proportionate. It eliminates separate Mouser and Coilcraft deliveries without forcing an unqualified all-TME magnetic component or the larger SC10 design. L1, R7 and C6 remain the original parts; there is no new controller, protection IC, fuse/resistor subsystem, output-capacitor bank, layer or connector.

The six substitutions have concrete purposes. RF1 changes within the same Bourns fusible family and footprint to damp the modeled input transient. C1's larger 1 kV pulse-rated part addresses the approximately 706 V C1 screen; a smaller 630 V part would not be justified merely because RF1 reduces initial dV/dt. T1 is an HV energy inductor available in the existing DigiKey basket; its move and local routing changes follow manufacturer guidance about sensitive traces beneath it. D1's 1 kV rating adds margin in the same package after the bus screen approached the former 600 V rating. R6 avoids the former separate purchase while retaining a two-resistor sense network. The MOV package change follows its actual lead geometry.

Keeping one original C5 in the DigiKey basket is cheaper than buying TME's minimum ten pieces. This correctly optimizes the total purchase rather than maximizing the number of TME line items.

## Findings and limits

**SIMPLE-SB01-01 — note, procurement handoff:** the approximately 190 PLN figure is a conditional budget, not a final checkout quote or an assembled-board price. It uses declared exchange rates, conservative DigiKey delivery VAT, and excludes the bare PCB, assembly, LED panel and housing. Keep those limits visible.

**SIMPLE-SB01-02 — note, release/energization:** no simplification proposed here removes physical current, thermal, fault or surge qualification. Frozen native ERC/DRC/parity reports are clean, while full strict spacing is explicitly false with 23 findings. This role does not close or approve those dispositions, nor transfer the former board's exact fabrication acceptance to this changed source.

No independent supplier checkout, reservation, payment, powered test or manufacturing qualification was performed. Render/manufacturing visual quality was not re-certified in this role. The companion native inventory and JSON record exact checks, scope and evidence. Any change to the frozen input requires a fresh review or explicit retained-scope assessment.


## Final documentation rebind

Final manifest `8035ba4c7b87abf9926d00b1b05ab22d21cbc5357870bcd294a8142d240c8243` was independently reverified after structured documentation corrections: 166 file hashes match; exact PCB hash and total procurement cost remain unchanged. The scoped recommendation is retained for this final input.
