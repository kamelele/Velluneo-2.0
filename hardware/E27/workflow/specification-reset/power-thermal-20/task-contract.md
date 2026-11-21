# POWER-THERMAL-20 task contract

Date: 21 November 2026. Base: 797d9038d55b0de8747ac0b48bde627f376da408.
Owner request: calculate driver input power, efficiency and component temperature
estimates to determine cooling, apply the toolkit and save to Velluneo GitHub.

Coordinator / sole writer: /root. Read-only research: /root/thermal20_loss_research
(charge/energy accounting and exact component losses),
/root/thermal20_component_research (exact thermal ratings and network scope).
Four separate final review contexts are assigned after freezing the body.

Scope: new analytical packet only, plus project-index entry. C16 CAD/BOM/rules,
C17 manufacturing, VIS18 and LED19 remain read-only. No new component, enclosure,
stage approval, supplier contact, order or physical test is authorized by this task.
Relevant requirements: existing input/output/current, compact60 geometry,
ambient10..40C, thermal/lifetime, transformer ambient50C and isolation constraints.
Their authoritative sources are bound by input-binding.json, not rewritten here.

Acceptance: replayable source-bound loss and charge/energy budget; steady-state
line-current model with power factor distinguished from efficiency; assumptions
and sensitivities for unpublished magnetics/switching/thermal data; component
temperature scenarios separating air, board, lead/case and junction; cooling targets
and measurement plan; pinned-toolkit doctor; old production hashes preserved;
four independent read-only role reviews on one frozen body; GitHub publication
and byte verification. Physical operating and manufacturing holds remain open.

The input current is total regulated secondary output: account for R11/R12
bleeders before assigning LED current. etaXFMR is an assumed aggregate parameter
including winding/core/leakage/bias, never claimed overall converter efficiency.
No published MYRRA DCR/leakage/core/thermal-rise data is available; component
allocation and heat-path scenarios are explicitly illustrative, not new limits.
