# Implementer handoff — startup/protection

Actor /root/readiness_startup. Input b1117ae2caecc037d9fc1253bd9c3a3c4effaaf2, unchanged approved31-position ECO graph. Exclusive write lease was this startup-protection directory; no shared CAD/library/requirements/configuration/graph changes. The coordinator may integrate/review this saved result. No independent or human approval is recorded by the implementer.

## Actual output

- calculate.py: standard-library coupled ideal-transformer/diode-branch DCM diagnostic plus interval screens.64 current4.7ohm cases and one matched2.2ohm sensitivity; both80 and160 integration-step runs actually executed.
- results-80.json/results-160.json: compact numeric summaries; actual sampled worst traces in worst-trajectory-*.json; actual stdout in run-*.log.
- verify.py and verification.json/log: independently stated KCL/energy/convergence invariants. Maximum VDD refinement difference6.745uV, KCL residual9.37e-15A and fine-step off-energy residual2.34e-12J. Not native-controller validation.
- ntc_curve.py and ntc-native-curve.json/log: exact active-part primary Vishay R/T coefficients, source SMD1 tolerance algorithm and electrical trip interval80.8002-96.5712C, plus source URLs/byte hashes. Native B25/85 reconstruction4099.999999995K checks coefficient use. Vendor originals remain outside the repository and are not executed/redistributed.
- README.md/fault-contract.md: conditions, actual design decisions, thermal tracking/sensor-open contract, VDD crest and fault/recovery obligations.

Actual commands: calculate.py --source-dir EXTERNAL_DIR --steps80; repeat --steps160; ntc_curve.py --source-dir EXTERNAL_DIR; verify.py. All valid final commands exit0. The first draft had a syntax error corrected before valid numerical runs; no failed draft result is claimed successful. No tool/CAD version changed and no physical test was executed.

## Integration decisions

Retain active RAUX4.7ohm: worst declared coupled diagnostic VDD11.683899V; matched2.2ohm improves only12.9mV, insufficient reason by itself to change the part. The auxiliary conduction window is solved from branch currents instead of chosen as a flat2%. This advances the RC-BIAS evidence but does not qualify actual TI startup/fault behavior or close that major.

Retain current RT1 pending the root thermal contract. Full native R/T calculation refines the beta-only estimate; normal68C sensor target leaves12.8002K to earliest electrical trip. Latest electrical trip leaves8.4288K to105C,13.4288K to110C and28.4288K to125C before actual lag/gradient/other error. Open RT1 loses the external shutdown; either passive normal/fault thermal safety must hold without it, or a separate concrete backup ECO is needed. Short RT1 commands shutdown. No lower NTC value or backup component is silently adopted.

No new graph is proposed because this subtask establishes no unavoidable current-value failure. No clamp or NTC ECO is approved. Native-source/current-voltage conditions, actual assembly temperatures, first-three/VS/CS/gate/parasitic/fault behavior and the complete1s AC-start criterion remain owned integration/verification gaps. Source table165C controller shutdown is typical and above other part limits; it is not a safe fallback for NTC-open.

## Review focus and retained gates

Reality/Change review should inspect the branch equations, behavioral actuator boundary, omitted VS-divider load, source/test conditions, native NTC tolerance port and exact matched comparison. Completeness should preserve original requirement/finding IDs, source hashes, physical-test separation and all remaining acceptance conditions. Simplicity should assess retaining the current parts versus an unsupported extra protection/RAUX ECO.

This handoff requests independent review, not full schematic/PCB readiness. Root owns final source inventory, fresh toolkit/native checks, final frozen manifest, all four role reports, finding closure decisions and publication. No specification threshold is changed merely to make a check pass.
