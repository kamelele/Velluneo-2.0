# Bias-repair task, dependencies and handoff

Task DRV-BIAS-REPAIR-01; parent DRV-CONTROL; specification investigation; 2026-11-16. Coordinator/sole implementation writer `/root`; authorized stage approver is the owner, not an agent. Baseline draft branch `spec/owner-interview-reset-2026-11-14`, last published commit before this task `2a6c9afb04993e0f8580e98f33c5ca6b91fb8cf9`. Main is untouched.

## Inputs and ownership

- Product packet r11 requirements-and-plan.md Git blob `6493b29bd33fbde1f3c61c5e995b11447cb83e9b`, freshly confirmed through GitHub on 2026-11-16. Requirements R-SUPPLY/R-COMPAT/R-FAULT/R-EMPTY/R-THERMAL/R-OFFLINE/R-LIGHT/R-BUILD.
- Protection r1 open RC-PROT-001/002/003 and fault contract; no historical evidence erased or repurposed as a pass.
- Primary-buffer code dependency SHA-256 `432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea`, checked by the new script before import. No write lease on that dependency.
- Native manufacturer sources/identities in sources.json. References remain scratch inputs; raw vendor documents are not redistributed in the device repo.
- Sole write scope: new `driver-study/bias-repair/` analytical artifacts and the driver's investigation index. No CAD/library/configuration/approved-intent changes.
- Four read-only contexts: `/root/spec_reality`, `/root/spec_simplicity`, `/root/spec_completeness`, `/root/spec_change`; coverage and outcomes recorded in review.md. No overlapping file writer.

Goal: compare one bounded controller substitution against the observed bias/bootstrap problem; preserve architecture A and panel simplicity. Non-goals: broad topology survey, final BOM, actual switching simulation, circuit freeze, stage approval, supplier communication or manufacturing/testing.

## Checks / acceptance scope

The calculation checks independent normal-cycle charge/energy identities and hashes its bus-model dependency. Saved results cover 2592 normal witnesses and 54 refreshed input cases. Four-file frozen manifest is frozen-inputs.json; lifecycle/task/review metadata are excluded to avoid self-hash cycles. Native source tables/formulas and numerical reproduction are independently reviewed with explicit coverage.

Publication acceptance means a reproducible, candid preliminary comparison. It does not mean RC-PROT-001 is closed. Independent Reality review assigns the replacement startup qualification its own major/open ID RC-BIAS-001; it also prevents circuit freeze. Circuit acceptance stops on unqualified startup acquisition, effective capacitors/gate draw, sampled control, magnetic/fault response, sourcing and remaining specification dependencies. No CAD check or installed-toolkit doctor was run; none passed. The existing incomplete specification preflight is not superseded by this narrower study.

## Next bounded acceptance criteria

1. Name an exact VDD capacitor combination whose total effective capacitance remains within 0.75–1.0 uF, and output capacitance within the assumed effective/maximum envelope, over actual operating bias/temperature/tolerance/age. Confirm ripple/ESR/voltage and assembly route.
2. Name a suitable MOSFET/drive path and close actual gate+bias draw against the assumed 6 mA budget, including startup and CV/low-frequency operation.
3. Bound the first-three-cycle acquisition and auxiliary takeover with supported controller timing evidence or a valid executable model/appropriate later laboratory evidence. Endpoint IHV and a constructed average-current ramp do not suffice.
4. Resolve normal sample/leakage/reset/clamp behavior and short-circuit pulse/average stresses against the actual transformer and devices. A 0.368 T linear backup proxy is not a fault-survival demonstration.
5. Refresh affected full comparison/specification inputs and independent reviews before asking the owner for a concrete stage decision. No fabricated independent closure or human approval.
