# Reality Checker review — SC09-SB01

Actual independent reviewer: /root/simple_reality_review. Date: 2026-11-23.
Frozen manifest SHA256: `8035ba4c7b87abf9926d00b1b05ab22d21cbc5357870bcd294a8142d240c8243`.
PCB SHA256: `a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`.
All 166 manifest files independently verified; zero hash mismatches. Final native probe rerun read-only on the integrated source.

**Recommendation: ready_for_human_review for this bounded engineering/procurement candidate. This is not fabrication, order, energization or product-safety approval.**

No remaining demonstrated static component-selection limit failure in reviewed bounded desk screens after 47 ohm RF1 and 1 kV D1 corrections. Final native topology and sensitive-node geometry checks pass; residual uncertainty is explicitly retained at later release/test gates.

## Evidence and scope

The declared target is a laboratory bare PCB with manual assembly, 230 V/50 Hz Poland/EU, 207–253 V planning range, 0–40 C ambient, approximately135 mA/60 V LED string. No energized tests were performed. Independent KiCad10.0.6 ERC and DRC/parity reports contain zero violations, zero unconnected items and zero parity issues under configured rules. Separate full strict spacing remains FAIL with23 findings.

The final native probe verifies12 changed-part pin/net memberships, no BP/M copper underneath the maximum T1 body, and a connected U1.3–R5.2 sense path outside that body. This checks topology and geometry; it does not prove feedback dynamics or EMC.

Independent 253sqrt2 V unloaded linear filter screens identified a630 V C4 overvoltage with the retained10 ohm RF1. Replacing RF1 with47 ohm in the same fusible family reduces modeled maxima to588.698 V on C4 and706.299 V on the new1 kV C1. This closes the specific selection flag. Typical-inductance assumptions cease to be reliable under saturation, so the numbers are not a guaranteed physical upper bound. 100/150 ohm alternatives were screened, but unavailable100 ohm stock was not selected.

T1 normal desk estimates fit catalog RMS/working-voltage limits and minimum-on-time margin. Conditional estimated body temperature58–107 C at40 C ambient does not establish the retained90 C target. Typical0.8 A Isat is a10% inductance-drop point, not an absolute current limit; neither a simplistic fault-current comparison nor a favorable nominal current proves startup/fault operation. MOV21 J is lower than the prior23 J; clamp and fusible-resistor coordination remain measurement gates. US1M improves reverse headroom without a topology change.

Primary documents and exact component observations are recorded in reality.json. Own calculation scripts/results and native ERC/DRC reports are beside this review. Availability is a dated observation, not a reservation.

## Findings and re-review

### REAL-SB01-01 — verified_closed

**major; gate: desk component selection; object: RF1/C1/L1/C4.**
Original retained 10 ohm input resistor produced 662.913 V across 630 V C4 in an independent unloaded linear input-filter step screen.
Specific modeled normal-startup rating flag required correction.
Evidence: reality.input-screen.py/json; reality.damping-screen.py/json. Final RF1 FW20A47R0JA closes this specific linear screen: C4 588.698 V, C1 706.299 V, L1 differential 324.453 V, C1 dV/dt 179.470 V/us. At 60 mArms, resistance tolerance and 2% hot increase, resistor loss 0.1812 W versus 2 W nominal.
Closure / remaining evidence: 47 ohm same-family fusible resistor and 1 kV pulse C1 present in frozen source. Linear-model flag is closed; nonlinear L1, hot startup, pulse life, surge and clearing are not qualified by this calculation.
Owner: implementer; independent verification /root/simple_reality_review.

### REAL-SB01-02 — verified_closed

**major; gate: magnetic-sensitive placement; object: T1/U1.3/R5.2/BP/M.**
New WE-PD HV manufacturer guidance prohibits sensitive traces underneath the inductor body.
An inherited smaller-body placement could invalidate feedback/noise assumptions.
Evidence: Final native read-only probe: maximum 12.5 mm square projected body at [114.25,115.75,126.75,128.25]; no BP/M overlap and no overlap of connected U1.3-to-R5.2 sensing path. Power connection terminating at T1.2 is distinguished from low-current sensing.
Closure / remaining evidence: Final native geometry passes this explicitly bounded check. No EMC or dynamic feedback proof inferred.
Owner: implementer; independent verifier.

### REAL-SB01-03 — verified_closed

**minor; gate: thermal and electrical planning documentation; object: active specification and prototype gates.**
Inherited current, C1 rating-basis and T1 thermal-target statements needed reconciliation with replacement parts and revised losses.
Stale thresholds could mislead prototype testing.
Evidence: Frozen active metadata retains T1 90 C planning target; C1 individual conservative stop 80 C overrides grouped 85 C; input current reconciled to revised 1.1–2.1 W loss budget. R7 thermal assumptions no longer inherit unrelated VR25 data.
Closure / remaining evidence: Corrected frozen metadata inspected; no measurements claimed.
Owner: implementer; independent verifier.

### REAL-SB01-04 — open

**major; gate: energized testing and functional qualification; object: T1/L1/RF1/MOV/U1 and thermal system.**
No physical startup, steady-state, fault, hot-restart, surge or temperature measurements exist for the replacement magnetic component and protection combination.
Desk screens cannot establish reliable current regulation, actual saturated inductance, AC core loss, MOV/fuse coordination or safe fault behavior.
Evidence: Declared no_physical_measurements; prototype-gates.SB01.json. T1 0.8 A Isat is typical at 10% inductance drop, not an absolute current maximum. 0.52 Arms rating and assumed core-loss/thermal resistance do not bound all real switching losses. Conditional 58–107 C estimate exceeds retained 90 C target in its high case.
Closure / remaining evidence: Competent controlled lab measurements with declared stop conditions: LED current/ripple, peak startup and restart currents/voltages, hot operation at 40 C ambient, T1 temperature and current-limit recovery; nonlinear L1/surge/fault/protection verification. Do not claim closure from appearance, Isat comparison or resistor energy integral.
Owner: prototype test owner.

### REAL-SB01-05 — open

**major; gate: exact-snapshot fabrication/release scope; object: 23 strict-spacing findings.**
Full strict-spacing check still FAILS. Twenty-three reported numeric violation signatures match the prior baseline; matching does not transfer prior human acceptance to this changed source.
Cannot label this new candidate fully spacing-passed or generally safety-qualified.
Evidence: Independent Counter comparison of sorted nets/kinds, conservative gap rounded to 4 decimals and target: baseline routing-order-prep/po_poprawkach/checks/strict-spacing.json and final candidate-views/strict-spacing.json both 23 and equal. Native DRC pass uses configured rules and does not override this separate check.
Closure / remaining evidence: Exact new snapshot requires explicit bounded fabrication review/acceptance or design correction meeting stricter targets. All product/energization qualifications remain separate.
Owner: release decision owner.

## Release boundaries

Original prototype acceptance does not cover new magnetic part, changed protection parts, updated footprints or thermal/startup assumptions. New native checks bind this exact board only.
Human review of exact bounded candidate and residual spacing scope before fabrication release; later measured bring-up and protection/thermal qualification before any functional safety claims.

The23 strict-spacing signatures are numerically unchanged from the prior baseline; that is regression evidence, not inherited acceptance. No findings were hidden or silently waived. No circuit, CAD source or input manifest was changed by this reviewer.
