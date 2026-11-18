# Reality review — PCB-DRAFT-01-r1

**Frozen body:** `4c6660ac66e2519c25a509f9848eb5e93ebf83126f40e06ff49bca7fc46c71a3`
**Base:** `7b75131667252634584552b4094c608cd88b9f2a`
**Verified members:** 143
**Recommendation:** **ready_for_human_review** for the isolated, unrouted engineering workspace. Product schematic, placement and routing acceptance remain unresolved.

## Actual evidence inspected

Read project instructions, relevant toolkit workflow/review requirements, current project requirements, task contract, gate audit, board-building/verification implementations, design contract, saved PCB, rules, model files, portable inventory and native reports. No build, render, electrical writer or native board modification was run.

- Ran the read-only frozen-packet verifier against the exact body above.
- Independently counted **31 footprints, 79 pads, 31 model references and zero track/via objects** in the saved PCB.
- Verified the portable ZIP hash and all **59 listed member hashes/sizes**.
- Inspected saved-board parity evidence: **22 functional nets, four singleton NC nets**, matching physical membership, outline **32 × 60 mm**, two copper layers and resolved model paths.
- Inspected actual native DRC JSON: **37 clearance violations**, **14 silkscreen violations**, **53 unconnected items**, and **zero schematic-parity findings**. These match the disclosed results; this is not a DRC-clean board.
- Inspected native-render input records, composition implementation and the displayed PCB preview. The preview contains actual KiCad geometry and openly identifies allocated component envelopes.
- Independently checked VRML units: the T1 box converts to **30 × 30 × 18 mm**. C1 uses the stated **10.5 mm diameter/22.5 mm installed** mesh allocation.
- Independently reproduced static screens: **0.349103 A**, **0.689587 A**, **48.3135 mA** ramp increment, and NTC resistance boundaries **7.2 kΩ/11.111 kΩ**.
- Independently reproduced the projected metal budget: **10.225 − 2 × 0.35 = 9.525 mm**.
- Hashed and read actual TI UCC2871x source pages 4–6 and SLUP419 page 10. The recorded source limits and their conditions match. SLUP419’s example concerns telecommunications, **400 VDC working voltage and 5,000 m altitude**; the packet correctly does not transfer its approval or conditions to this lighting product.

## Findings and remaining conditions

**No new bounded defect requiring correction before review of this workspace was identified.**

**R-PD01-01 — Major, open for placement/routing acceptance:** the actual native board retains 37 findings from the provisional HV/quiet screening rule.
**Owner:** coordinator/power-layout designer.
**Closure:** establish voltage-, waveform- and object-specific functional spacing requirements, resolve the resulting placement/routing constraints, and retain fresh native results. Blanket relaxation or suppressing package-related findings would not establish safety.

**R-PD01-02 — Major, retained for schematic acceptance:** static controller thresholds do not bound actual startup/fault peaks, pulse counts, retry energy, NTC-open safety or R1/F1/BR1 coordination.
**Owner:** power designer/coordinator.
**Closure:** supported circuit/state analysis across declared operating and fault conditions. Physical testing and supplier confirmation remain due where applicable; their absence does not prohibit authoring this explicitly provisional draft.

**R-PD01-03 — Major, retained for insulation/placement acceptance:** the copper reservation and 9.525 mm planning budget do not establish finished-transformer, core/yoke, leadout, surface or solid-insulation paths.
**Owner:** transformer/insulation designer with coordinator.
**Closure:** finished construction and tolerance geometry, actual working-voltage/waveform bounds, applicable lighting requirements and justified material/process rules.

**R-PD01-04 — Major, retained for affected acceptance gates:** component thermal limits, actual mounting boundary, wire/lead forming and assembly capability remain unqualified.
**Owner:** coordinator/assembly designer.
**Closure:** component-specific loss/temperature and mechanical/process evidence. Envelope models cannot substitute for these.

## Stage interpretation

The gate audit is supported by the inspected project requirements and toolkit branches: release confirmations, physical-test readiness and design-stage acceptance are distinct obligations. The owner’s explicit request supports this reversible engineering workspace; it does not manufacture schematic or placement approval.

Requirements exit **1**, work-check exit **2**, and native DRC exit **5** remain real failures. This recommendation accepts their honest presentation within the draft-review scope, not the underlying product conditions. No operating, safety, manufacturing or stage approval is granted.
