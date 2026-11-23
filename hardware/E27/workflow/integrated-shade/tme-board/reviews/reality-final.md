# Reality Checker — REAL-TME-FINAL-01

Actual reviewer: `/root/tme_reality`. Candidate: `SC10-TME-A-DRAFT`, 23 November 2026.

Source digest: `86c78b4be01ec98c0227b2ce02a5600e4c6f7527d1007f378b6b368268d3d2a2`.

Recommendation: **blocked for fabrication acceptance, ordering and energization**. The separate routed engineering candidate exists; this is not a finding that no design work was completed.

## Verified evidence

I independently checked all 91 source files and 22 artifacts against their declared SHA-256 hashes and reproduced the canonical source digest. A read-only load with pinned KiCad 10.0.6 showed 25 footprints, 65 pads and 207 track/via objects. There are 10 front-side and 15 back-side positions, including wire pads. T1 primary pins 4–5 and seven separate NC terminal nets match the intended functions. No source bytes were changed.

I reran the pinned intended-connectivity comparison against the frozen native XML. The physical graph agrees: 65 pins, 15 functional nets and seven NCs. The sole formal comparison error is the missing current human intent approval; graph agreement does not create that approval. The frozen native reports show zero ERC, DRC, unconnected and schematic-parity findings.

I visually inspected the final schematic PDF and both frozen native 3D renders. Both input capacitors now read 150 nF / 630 V. The three 47 µF capacitors, four 97.6 kΩ divider resistors, separate fuse/resistor/MOV and primary-only magnetic component are present. AC and LED ports occupy opposite ends. No obvious body overlap was observed. The models remain illustrative engineering envelopes, not supplier-certified STEP files or physical fit evidence.

I independently reproduced the nominal calculations: 135.203 mA total output, 133.439 mA external LED current after bleeders, 77.9613 V static OVP and 34.1783 seconds for a single remaining bleeder to discharge 90 V to 5 V. These are calculations, not measurements.

## Findings

1. **REAL-TME-01 — blocker: T1 fault current.** The MYRRA 74089 primary is specified for 0.85 A peak. The LYT1603D restart limiter is characterized at 1.06–1.24 A at 25°C. Normal-operation margin does not cover this different condition, and the input fuse is not a cycle-by-cycle 0.85 A limiter. Close this with an appropriate magnetic/current-limiting redesign or a manufacturer-supported, bounded fault envelope. Owner: electrical/root.

2. **REAL-TME-02 — blocker: nonlinear input transient.** The final ideal linear model produces 406.916 V at C1, 407.613 V at C4 and 1.398385 A through L1. L1's published 0.3 A condition is a typical 10% inductance drop, not a guaranteed hot limit or impulse-voltage rating. The two 630 V capacitors fix the demonstrated 400 V part mismatch, but do not establish a nonlinear saturation or surge bound. Obtain applicable transient data or redesign the filter, then qualify it within an approved fixture. Owner: electrical/root.

3. **REAL-TME-03 — blocker: fuse, MOV and resistor coordination.** F1 is rated 100 mA, 250 VAC and 50 A breaking capacity. Its maximum melting integral of 0.0013 A²s at ten times rated current is not maximum total clearing energy. A MOV short occurs before R1, so it bypasses the resistor. Define an enforceable prospective-fault limit, resolve the declared 253 VAC upper input, and compare actual clearing behavior with resistor overload/pulse behavior. Include repetitive startup-pulse endurance. Owner: electrical/root.

4. **REAL-TME-04 — major: operating and thermal envelope.** The minimum-on-time margin depends on unverified hot/bias inductance factors and an assumed IC thermal reserve. The extended lower OVP screen is 68.913 V, leaving only 0.913 V at the proposed 68 V load before ripple. Hot DCR, core loss, magnetic RMS rating and actual current/ripple remain unqualified. Measure against explicit limits, including T1 local air at or below 50°C; narrow or redesign the load window if necessary. Owner: electrical/root.

5. **REAL-TME-05 — major: current purchasing availability.** The final BOM has 23 electronic positions and 16 unique electronic MPNs, plus two wire-pad interfaces. Every electronic MPN has a TME offer, but some positive stock counts remain cached. Confirm exact current stock and prototype MOQ before buying. HTTP 429 is neither zero stock nor passed availability. Owner: procurement/root.

6. **REAL-TME-06 — closed for this exact source.** The preliminary inconsistent input-capacitance record and missing C1 voltage log have been corrected. The interim 47 nF / 400 V C1 was rejected after its modeled peak reached 454.29 V. Final BOM, schematic and model agree on two 150 nF / 630 V parts. This closure does not qualify nonlinear transients or surge behavior.

7. **REAL-TME-07 — blocker: functional routing clearance.** The final assessment contains 401 object-pair findings spanning 41 net pairs, with all 231 target pairs enumerated and no approved exceptions. One concrete example is D1.2 (`/DC_RETURN`) to track `64adb25b-cd4e-4c1b-aa08-6c0f3531b5d3` (`/BUS_FILTERED`): 0.350001 mm against the declared 2 mm target. Actual high-differential-voltage routing therefore remains below the target. These findings cannot collectively be dismissed as cosmetic package effects. Reroute/reposition or establish an independently justified, specifically approved disposition for each affected object, then rerun the full assessment. Owner: PCB/root.

## Scope limits

I inspected the dedicated Kelvin contact report and independently read the actual feedback pin assignment. The implementer's contact test is geometry evidence; it is not an independent analogue or EMC measurement. No powered test, supplier upload, purchase, physical thermal qualification or human approval occurred. Previous SC09 acceptance does not apply to this changed source.

The companion JSON records the exact manifest hash, primary sources, detailed findings and reviewed evidence. This final report supersedes the preliminary review only for the frozen digest above. Any change requires a fresh review or an explicit retained-scope assessment.
