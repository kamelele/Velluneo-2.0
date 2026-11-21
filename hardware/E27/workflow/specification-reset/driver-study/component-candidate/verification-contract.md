# Component-candidate verification contract and handoff

Task DRV-COMPONENT-01; specification; sole writer/coordinator `/root`; baseline draft commit 0f1d8502c05f91f36c7a42a4e7bab58e0538aad0. Owner alone grants stage approval. No CAD write lease. Paths: new driver-study/component-candidate/* plus driver-study/README.md index. Do not modify prior frozen studies or requirements. Product packet r11 blob 6493b29bd33fbde1f3c61c5e995b11447cb83e9b retained.

Acceptance for this task: exact component reference choices, native source identity, reproducible component/current/storage and magnetic sensitivities, explicit current/temperature/timing assumptions, independent four-role review, saved draft artifacts. This is not circuit acceptance. Input manifest freezes code/results/findings/parts/sources/this contract. Review metadata and index target are separately scoped to avoid self-reference.

## Concrete remaining checks before a complete circuit proposal

| ID / owner | Observable evidence | Consequence if absent/fails |
|---|---|---|
| COMP-VDD / coordinator | Two selected capacitors total including all added capacitance ≤1 uF and adequate local high-frequency bypass; actual component/routing bounds. | Recalculate storage/startup and decoupling; no extra bypass without budget. |
| COMP-START / coordinator, later lab execution by named responsible human | Actual gate/auxiliary demand and first-three-cycle timing across startup, temperature, input and output-capacitance corners. Conditional design hypothesis: total draw ≤4.3 mA and initial acquisition ≤0.300 ms for the 20.592 uF sensitivity. Review actual current waveform/charge, not only average. | RC-BIAS-001 remains major/open. A test plan is not measurement; no circuit freeze from this hypothesis. |
| COMP-MAG / coordinator | Finished transformer winding/insulation/leakage/copper/core-loss data; normal and fault reset/clamp/SOA waveforms, saturation/current/temperature limits and recovery. | Normal/backup linear flux comparison cannot qualify short survival. |
| COMP-COUT / coordinator | Effective output capacitance and ESR/ripple over actual operation/age; low-frequency control ripple included; manufacturer frequency derating and optical measurements. | 63 V/1 A table rating and nominal static-LED witness do not qualify the lamp. |
| COMP-SOURCE / coordinator | Exact manufacturer-approved parts and JLCPCB component/transformer assembly route, or explicit manual fallback for the first sample. No contact/order authorized by this task. | Candidate list stays partial; do not publish a ready-to-order BOM. |

## Later laboratory evidence outline, not authorization or ready-to-run procedure

Before execution, name hardware/enclosure/cabling revisions, responsible human and equipment with ratings, exact test limits and stop conditions. Missing insulation, clamp, device/SOA or accessible-energy limits block that test; this document supplies none by invention.

Capture VDD, DRV/gate, CS and VS with appropriately isolated/differential methods and record their reference/polarity; correlate output voltage/current and mains conditions. Verify initial acquisition/auxiliary takeover and output-capacitance extremes; then assess normal/no-load/open/short/power-cycle recovery using the exact reviewed protection arrangement. Whole-lamp temperature, service delay, photometry/flicker and EMC use separate methods and accepted limits. Do not apply an ordinary grounded oscilloscope clip to a live primary. University/experienced-person support is recorded, but specific setup readiness is not established.

Stop and correct on UVLO cycling in normal operation, loss of control/reset, unbounded current/voltage/ringing, exceeded device/SOA/thermal limits, unsafe access or an invalid measurement setup. Numerical trip/output/service limits must be filled from the final reviewed circuit and applicable assessment before physical execution. No purchase, energization or prototype measurements are claimed or authorized here.

Four distinct read-only reviewers inspect the same final manifest: Reality `/root/spec_reality`, Overengineering `/root/spec_simplicity`, Completeness `/root/spec_completeness`, Change `/root/spec_change`. Actual reproduction/source scope and findings belong in review.md. Coordinator receipt and continued analytical work do not constitute human gate approval.
