# Startup and sampling task contract

DRV-STARTUP-01; specification investigation. Sole writer/coordinator `/root`. Baseline draft3f1fa94710b3a92dd957841619716d76c176f0e9. Allowed writes: driver-study/startup-candidate/* plus driver-study/README.md. Requirements r11 remains authoritative. No CAD/library/configuration ownership or stage approval.

Dependencies: exact component-candidate/results.json and clamp-candidate/results.json hashes asserted by calculate.py. Canonical run layout is driver-study/{startup-candidate,component-candidate,clamp-candidate}; scratch folder names are not embedded as fallbacks. Native documents/model/runtime identities are recorded in sources.json, reference-only. Lifecycle review/index excluded from their own input manifest.

Task acceptance is preliminary reproducible analysis: separate acquisition/settling/charging loads, preserve source conditions, supply exact resistor references, propagate changed divider thresholds, state pin/node-charge limits and expose failed model execution. Acceptance does not close any major electrical finding.

| Next required evidence / coordinator owner | Observable condition |
|---|---|
| Startup | Actual first-three-pulse/settling/current/auxiliary traces or a valid controller model. Check the conditional0.300ms+0.100ms design hypothesis and actual gate/base draw across relevant corners; do not inherit a reference design's timing or use nominal IHV as a whole-trajectory bound. |
| Sampling | Actual total pin/probe capacitance, clamp-node charging/current history, leakage reset and VS ringing/sample timing. The8.65pF and14/21/28nC allocations are hypotheses, not measured limits of the parts. |
| Divider/current control | Verify new80.6k/17.4k/1.40k references, native voltage/power/temperature/footprint data, actual turn-off delay/line compensation and refreshed normal/CV/OVP/fault behavior. No VS filter capacitor by default. |
| Protection/integration | Hot dynamic diode/TVS and MOSFET repetitive/SOA behavior, input surge, actual transformer insulation/coupling, persistent-fault heat and offline service-energy/cooling. Keep RC-COMP-002/RC-BIAS-001 major/open. |
| Source/setup | Retain≤1uF recommended VDD path pending source clarification; failed ST component transient is not a model pass. Full trusted-toolkit/environment/specification and manufacturing gates remain separate. |

Later lab execution requires named hardware/setup revisions, responsible person, suitable rated instruments and explicit numeric stop conditions before energization. Probe capacitance can alter the VS waveform; account for it. Do not attach a normal grounded probe to a live mains-primary reference. This contract supplies no test authorization or invented measurements.

Diagnostic implementer `/root/model_compatibility` independently investigated only the failed component-model compatibility, read-only on shared files. It is not a reviewer or a human approver. Four distinct read-only final reviewers remain Reality `/root/spec_reality`, Overengineering `/root/spec_simplicity`, Completeness `/root/spec_completeness`, Change `/root/spec_change`. Record actual final input coverage and any independent closure in review.md. The owner alone approves stages.
