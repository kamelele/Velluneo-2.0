# Integrated startup/sampling independent review

VEL-STARTUP-01 r1, 2026-11-16. Preliminary analytical publication only; **circuit freeze remains blocked**. No working-hardware or stage-approval assertion.

## Final frozen inputs

| File | SHA-256 |
|---|---|
| calculate.py | b8a0e5f48d8029b9d4aaaceacbdf58d3496949f5f61a18fac0e4324fe21f5d2c |
| results.json | 267db0de602050e9f014e332e578d9cda85d450a7c67bdc918f15cbf8788a8ed |
| findings.md | 54684015cea595385f6cb781921efc3a956a860715192e219c5a20e35d6cd84c |
| parts.csv | cdf0474ec987d028eb987a8915a7bff39af35cdfb5ff0db2d485a8be103db580 |
| sources.json | 58d8ecfc0d3f305cea74d570bf2ee5d6e685329ca626861699d26e334ffdbb08 |
| task-and-contract.md | 1dcc6a6c77856d4295201bb1547eba767f00f458f046acef3bcd25bb6680eace |
| mosfet-model-check.py | 3b8b30fb1ffaad4818ab5fadb22e5ebe16a6563fbb659c84fee0c1b37e20925e |
| model-check-status.json | db7a58a6fdd26d05224160d0ed90a1d8a83bd5d74fdf41640bb19e491e623180 |
| model-check.log | 9e2bd8161411cd8ead986c2e4e1923501fdd1f9f0eb7e801086a9067eaed8057 |

All nine inputs are also identified by frozen-inputs.json. Review/index lifecycle metadata is separate. Native vendor documents/model are reference-only and not redistributed. The device specification r11 was freshly confirmed unchanged at Git blob6493b29bd33fbde1f3c61c5e995b11447cb83e9b. The main script asserts both canonical parent-result hashes before arithmetic. Baseline draft commit3f1fa94710b3a92dd957841619716d76c176f0e9.

## Actual independent final coverage

| Role / actual context | Checks performed | Recommendation |
|---|---|---|
| Reality /root/spec_reality | All nine inputs/hashes, charge-phase equations and nonlinear LED/ESR integration, divider/sampling allocations, native reference discrepancy, failed-model code/status/log. Unchanged main script executed in canonical staged repository layout and reproduced results.json exactly. Did not rerun the log-writing model experiment. | Ready for preliminary publication only. No new publication-blocking analytical defect; electrical majors remain open. |
| Overengineering /root/spec_simplicity | Nine input hashes, code/result/parts/contract and failed-model-record inspection. No full calculation/model rerun. | No new complexity finding. Three resistor refinements add no filter/bias stage/panel electronics. Resolve actual trajectories rather than add circuitry to unknowns; OE-LED-01 retained. |
| Completeness /root/spec_completeness | Nine hashes, stored-result reconciliation, available native-source integrity, equations, contract/requirement and failure-record coverage. No duplicate full run or independent PDF interpretation. | No new completeness finding for preliminary scope. Source test conditions, changed thresholds and failed-model limits remain explicit. |
| Change /root/spec_change | Nine hashes/native-source identity, canonical mirror code and dependency-loading prefix with both parent assertions; product preservation and source/failure claims. Separate final index inspection. No full numerical/model rerun. | No drift/false closure, catalogue/assembly guarantee or stage approval. Provisional values and retained major stops correctly tracked. |

All four contexts inspected the same final nine-file packet, without shared-file edits. The coordinator remains sole writer and cannot approve a product stage.

## Actual diagnostic implementer and failed tool evidence

A separate bounded diagnostic implementer, /root/model_compatibility, inspected the failed ST-model experiment without editing shared files. It independently reproduced aborts in isolated SPARSE and KLU trials; KLU was explicitly selected by .options klu and still aborted at20ps. Its numerical compatibility exploration found no validated remedy. It is not a fifth reviewer or a human approver.

The coordinator's reproducible check returns **exit1**, status failed_no_usable_transient, with an actual timestep-too-small abort at22.5ps. No trace reaches a valid gate-charge endpoint. The saved log hash agrees with model-check-status.json. This records absent model evidence, not a physical transistor defect. No Qg from that experiment is used in calculate.py. Availability of libngspice44.2 is not an installed-toolkit/CAD/environment pass; the encrypted UCC sources remain unexecuted.

## Reproduced analytical outcome and finding ledger

The canonical run reproduces128 cases, maximum permissible first-three-pulse interval proxies0.95161ms under the main budget and0.49847ms across the larger stress budget, and10.7802V worst takeover VDD under the assumed0.300ms acquisition plus separate0.100ms settling. They are conditional charge-accounting results, not IC timing guarantees.

| Finding | Severity / affected acceptance | Status / required evidence |
|---|---|---|
| RC-BIAS-001 | **Major / actual integrated startup** | Open; coordinator. Actual acquisition/settling, gate/base current, frequency law and auxiliary trajectories. Charge surplus cannot prove a controller timing bound. |
| RC-COMP-002 | **Major / actual protection and drain/SOA** | Open; coordinator. Hot dynamic clamp, repetitive heating, fault/stop latency, surge/SOA and changed-divider protection behavior. |
| RC-CLAMP-001 | Note / sampling-node dynamics | Open; coordinator. Total voltage-dependent capacitance, node-charge/current history and VS ringing. Conditional Q/I and pin-pole allocations do not verify the waveform. |
| RC-PROT-001 | Major / retained historical TPS circuit | Open, unchanged. New-controller investigations do not qualify that old circuit. |
| RC-PROT-002/003, RC-BIAS-003, OE-LED-01 | Existing control/fault/service/thermal/final comparison work | Retained open within their original scope. No measurements, full assembly route or whole-product qualification are invented. |

No new analytical correction was required by the four final reviews. Their publication recommendation does not close any electrical major, approve the new divider intent or authorize manufacturing.

## Integration and next concrete work

Submit the ten analytical/source/contract/model-status/review files plus the input manifest under driver-study/startup-candidate/ and update only driver-study/README.md on the existing draft branch. Main, requirements, historical studies, CAD/libraries and manufacturing files are unchanged. Canonical repository layout was exercised and final remote readback must match UTF-8 contents.

Next work requires actual controller acquisition/current/sampling evidence or a valid executable model, together with fresh changed-threshold fault/protection assessment. Keep the source-conditioned <=1uF VDD candidate; do not adopt the older10uF example by changing the limit. Do not infer physical test readiness, safe service delay, source/assembly confirmation, a schematic gate or product acceptance from this packet. No supplier message, purchase, merge or physical test occurred.
