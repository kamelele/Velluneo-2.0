# Startup evidence acquisition plan

Plan only; no generated product schematic, executable Velluneo simulation, measurement or test authorization. Coordinator owns preparation; owner supplies eventual execution location and approves product stages. Controller and component-model qualification remain prerequisites to acceptance. This plan is a specification research fixture definition, not a CAD-stage waiver.

## Keep the diagnostics separate

| Run | Inputs and intent | Observable completion |
|---|---|---|
| A: vendor compatibility | Unchanged pinned SLUM464 project in compatible simulator. Preserve forced bias, ideal switch and original analysis settings. | Actual runtime/version/log and complete or failed10ms trace. Never reuse bundled output as this result. |
| B: model scope | Exact variant and applicable features identified; startup/state-machine, drive-current and supply-current coverage explicitly recorded. | Source justification or declared measurements for each claimed feature. Unknown features remain unknown; A alone cannot pass B. |
| C: proposed base sensitivity | Separate fixture with candidate bulk buffer, transformer and auxiliary turns, actual divider/compensation and output network from pinned component/startup studies. Remove the vendor artificial VDD support only in this separate candidate fixture. | Cold-start bias, gate/control, primary/secondary/auxiliary and node-charge trajectories, including failed start or hiccup. Approximate switch cases remain sensitivities. |

Do not change a10V VDD target,12nC gate-charge hypothesis or node-capacitance allocation merely to pass C. Preserve2x470nF proposed VDD path and resolve native recommended-capacitance/reference discrepancy before proposing a larger reservoir. Native model D/G/S order is not a physical pin/footprint contract. No NTC connection or physical pin graph is frozen here.

## Required source-bound run inputs

Record exact circuit revision, source model/module hashes and adaptations, simulator build, supply/bulk initial conditions, line condition, output/precharge state, temperature, LED law/bin assumptions, capacitance tolerance/ESR, transformer winding model/leakage, bias loads and switch/clamp models. Use the existing canonical studies and their stated corners; do not independently invent corner values or imply their sensitivities are guaranteed component limits.

Start with one diagnostic case; expand to declared low/high input, cold/hot sensitivities, capacitance corners, normal/open/missing/short panel and power cycling only after the first fixture is qualified. Simulation fault cases are not physical-test authorization. Output-state/temperature assumptions must be explicit; neither forced initial VDD nor an artificial bias supply may be hidden in a cold-start claim.

## Export and interpret

Export numerical time-series with units, reference/polarity, enough bandwidth and a convergence/time-step comparison suited to the event. Retain full run/error logs and actual final simulation time. Required channels are VDD, DRV/gate, CS, VS, bulk/output/auxiliary/drain voltages, primary/secondary currents and modeled currents into/out of the VDD capacitor including drive demand. If the model does not expose credible supply current, capacitor-voltage appearance alone cannot validate the startup charge budget.

Identify first gate rise, first three complete pulses, post-acquisition settling, auxiliary support onset and minimum VDD through takeover. Compare the actual acquisition and current trajectory against the conditional0.300ms/0.100ms and10V targets from startup-candidate; these are engineering hypotheses, not manufacturer guarantees. Integrate signed VDD-capacitor charge and reconcile all modeled supply/drive contributions. Include actual gate-drive amplitude;7.7nC at0–10V typical is not a guaranteed bound at another drive voltage.

For VS/clamp analysis, identify leakage reset, voltage-dependent drain charging and demagnetization/sample window together. Do not infer a physical current floor or total-node-charge bound from Q/I alone. The existing14/21/28nC allocations and AC31.66nC proxy are different conditional quantities, neither a measured waveform. Failed convergence, absent current fidelity or unqualified models must remain visible instead of being interpolated into missing evidence.

## Physical evidence alternative

If suitable simulation coverage remains unavailable, prepare a separate laboratory fixture/readiness packet before any energization: exact hardware and isolation construction, responsible university personnel, rated instruments/probes, source/loads, numerical normal/fault/stop limits, stored-energy handling and measurement uncertainty. None is established by this plan. No test dates, hardware, safety approval or measured results are fabricated. Physical evidence can address component/current/model gaps, but a successful start alone cannot establish insulation, EMC, thermal lifetime or full product compliance.
