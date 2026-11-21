# Clamp proposal independent review and integration ledger

VEL-CLAMP-01 r1, 2026-11-16. **Preliminary publication only; circuit freeze remains blocked.** Owner alone grants human stage approval. No new measurement, vendor simulation, fabrication or hardware validation.

## Final frozen technical inputs

| File | SHA-256 |
|---|---|
| calculate.py | 30407004a83248fce0dcc7936b3029d9e14d04fd29471ce494ed81fc187d03f8 |
| results.json | 29827b4ef38f66a4f11dde07d7410c1170753ebc86767e94fa52af6624690bcc |
| findings.md | d845580e58c41ae836d360f5d40cb6898010c13d6d022f50bc16b9aba32da08f |
| parts.csv | e6e69627c7fb65b6ca06c4348b12524a724eac9dbf3fa961eba24d42a0d37474 |
| sources.json | fc69b76d1ac51da0d9eb7032b44c3fc00f1167df83c4aad7d26b5ddd41d90415 |
| task-and-contract.md | a5b6d7b2aac139467bca1bd2d9e79130e6ffbc26ad66419dcffb378e754337af |

Six files are also identified by frozen-inputs.json; lifecycle review/index are separate. Product r11 was freshly confirmed unchanged at Git blob6493b29bd33fbde1f3c61c5e995b11447cb83e9b. Exact native source identities are recorded without redistributing vendor documents. Parent component results hash is asserted before execution. The final path change left all numerical inputs/results unchanged.

## Actual actors, coverage and retained scope

| Role / context | Actual final evidence | Recommendation |
|---|---|---|
| Reality `/root/spec_reality` | Six final hashes, native source tables and identities, clamp polarity, RCD energy map, direct avalanche/fault/reset/thermal formulas. Final unchanged code executed in canonical repository layout and reproduced results.json exactly. | Ready for preliminary publication; no circuit approval or electrical-major closure. RC-CLAMP-001 note retained. |
| Overengineering `/root/spec_simplicity` | Six final hashes, code/result/component/contract inspection, targeted canonical path correction and retained unaffected scope. No duplicate full run or independent dynamic-device validation. | No new complexity finding. Fewer clamp parts do not prove lower total finished-transformer cost. OE-LED-01 stays open. |
| Completeness `/root/spec_completeness` | Six final hashes/native-source integrity, numerical-summary reconciliation and requirement/contract coverage; targeted path correction. No full rerun or independent PDF interpretation. | No new completeness finding for preliminary scope. Startup, sampling, thermal, fault/surge, assembly and service qualification remain open. |
| Change `/root/spec_change` | Six final hashes/source identities and product preservation; discovered path-layout defect; independently checked final canonical dependency-loading/hash prefix, mirror equality and coordinator output equality. Separately reviewed index delta. No duplicate full numerical sweep. | CH-CLAMP-001 independently verified closed. Ready for preliminary publication only. No false electrical closure or stage acceptance. |

All four contexts reviewed the same technical packet; the only correction was the canonical dependency path and refreshed code hash. Other five inputs did not change. Reviewers explicitly retained unaffected original coverage. The separate corrected driver-index patch is covered by Change review, including table formatting and all major stop conditions.

## Finding history / circuit acceptance stops

| ID | Severity / affected acceptance | Status / owner / observable evidence |
|---|---|---|
| CH-CLAMP-001 | Major / reproducible publication and handoff | **Independently verified closed by Change.** Initial script used scratch sibling component-study rather than declared repository sibling component-candidate. Corrected code uses only ../component-candidate/results.json, without fallback. A matching canonical staging layout contains the pinned dependency; coordinator and Reality full execution reproduce exact frozen results. Initial code hash29281bacd5c786e9d2c5f0fe4810d0b6816e1bebcce47a53f23272484ac1bd4f is superseded, not the final execution input. |
| RC-COMP-002 | **Major / actual drain-clamp-SOA qualification** | **Open**, coordinator. Actual hot I-V, voltage-dependent capacitance, diode recovery, layout spikes, repetitive avalanche heating, mains surge path, fault detection/stop latency and device/clamp SOA/temperature. The696.5V endpoint is not a hot/surge bound. |
| RC-CLAMP-001 | Note / minimum-current sampling and startup | Open, coordinator. Include TVS voltage-dependent capacitance, blocking-diode behavior and clamp-node charge history before avalanche. Ideal constant-avalanche reset cannot bound charging or VS ringing. This refines existing waveform obligations; no fake model of those effects is claimed. |
| RC-BIAS-001 | **Major / integrated UCC startup** | **Open**, coordinator. Actual acquisition/gate/bias/auxiliary and clamp influence remain unknown. Removing a47nF comparison capacitor does not verify the prior conditional startup budget. |
| RC-PROT-001 | Major / retained historical TPS path | Open, unchanged. Neither controller substitution nor clamp study qualifies that old circuit. |
| RC-PROT-002/003; RC-BIAS-003 | Retained control/fault/service/thermal work | Open. Counterexample pulse counts are not safe operating allowances, actual fault timing or survival evidence. |
| OE-LED-01 | Retained full implementation comparison | Open. Validate finished-transformer insulation/coupling/fit and optical/control/thermal/source/assembly burden before selection. |

No majority vote or coordinator receipt closes an electrical major or advances a stage. Independent reviews accept only the correctness/candor of this preliminary publication.

## Verified scope and next evidence

The result is a concrete preferred diode/TVS branch and a source-pinned comparison, not a complete circuit or JLCPCB-ready package. Direct-clamp leakage≤1% is a proposed engineering target, not a measured or supplier-confirmed fact. Do not reduce insulation to meet it. The5W TVS infinite-heatsink value and600W duty-limited pulse rating are not adopted as continuous bulb ratings. The VBR coefficient is explicitly not a guaranteed Vclamp temperature curve.

Next bounded work: quantify pre-avalanche clamp-node charging/VS reset and integrate actual gate/bias acquisition; establish finished-transformer coupling/insulation and hot repetitive clamp behavior. Retain source-specific fault timing, input surge and full service-energy evidence. No real waveform or numeric prototype result is invented.

Submit only eight new files under driver-study/clamp-candidate/ plus driver-study/README.md on the existing draft branch, based on e951517b2becf6ecb2002f2d5ad5c17aa3cb2d3f. Historical studies, requirements, CAD/libraries/main remain unchanged. Integration requires exact remote UTF-8 readback. No merge, schematic gate, installed-toolkit pass, order, supplier message or physical test occurred.
