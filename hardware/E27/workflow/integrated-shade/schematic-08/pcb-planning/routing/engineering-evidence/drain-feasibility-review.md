# U1 DRAIN escape reality check

Actor: `/root/route_drain_feasibility`, independent of the routing implementer and CAD writer. Scope: native geometric feasibility of U1.4 escape only. Recommendation: **changes_requested** at routing acceptance; no fabrication, thermal, electrical or standards qualification.

## Finding RC-ROUTE-DRAIN-01 — major, open

Input is accepted placement PCB SHA256 `c503ff1b7660022d665ed4fabbc536c8f05d72899694a1d2da2c8a84ec6357d5`. The actual generated custom rule `HW-NETCLASS-AC_BUS` sets a **hard minimum 0.6 mm** track width for `/DRAIN_BLOCKED`. The global 0.3 mm minimum does not override it. The exact native U1 courtyard is stepped; its rounded offset by the maximum approved 1 mm is the largest possible component escape envelope. Generic foreign-pair spacing outside that envelope is 4 mm; added vias have no component exception.

The 0.6 mm conductor cannot cross this envelope while retaining the current full-copper exception scope and generic spacing. This is stronger evidence than failed A* or a rectangular pad approximation:

- Native inward foreign-pad polygons for U1 pins 1,2,5,6,7,8 were used, with 0.0002 mm approximation error. Inward polygons overestimate available gap and therefore favor feasibility.
- The complete rounded envelope boundary was sampled at no more than 0.0025 mm, giving 12,694 samples.
- At every sample, a witness point at radius 0.295 mm lies at least 0.005 mm outside the envelope and closer than 4 mm to a foreign pad. The least severe witness still has only 3.933628 mm available gap. Maximum center interpolation and curve/rounding uncertainty is 0.001652 mm, so the witness remains inside the 0.3 mm radius copper at any continuous crossing and remains outside the true envelope.
- The 0.3 mm hypothetical trace experiment leaves 26 uncovered samples, so that experiment does not establish impossibility for narrower traces. Such a trace would violate the actual 0.6 mm native minimum and is not an authorized solution.
- An added through via cannot bypass the problem inside the envelope. A 0.05 mm grid covering its entire enclosing rectangle gives continuous foreign-pad clearance upper bound 4.298915 mm. Even the smallest 0.7 mm via permitted by 0.3 mm drill plus 0.2 mm annulus needs 4.35 mm center clearance. The proposed 0.8 mm via needs 4.4 mm. A via outside the envelope would first require the blocked front trace to leave it.

Evidence: `boundary_probe.py`, `boundary-report.json`, `disk-boundary-report.json`, `via_probe.py`, `via-envelope-report.json`. Original customer CAD was read only. The proof uses only U1 foreign pads; other components cannot improve feasibility.

## Concrete correction proposal, not approved

Preserve native 0.6 mm routing and all global 4 mm targets. Propose **1.5 mm maximum local escape only for the exact U1 pin pair 2/4**, retaining its existing local floor, exact nets, F.Cu pad/track scope and actual pin ownership. Keep all other exceptions, including U1 pair4/5, at 1 mm. No via or zone exception is proposed. The initial two-pair experiment is retained for comparison; a subsequent minimal-change experiment proved that extending pair4/5 is unnecessary.

Proposed F.Cu centerline, width 0.6 mm:

`(107.525,41.905) → (107.525,43.65) → (105.5,44.15) → (104.5,44.0)`

Proposed through via: center `(104.5,44.0)`, diameter 0.8 mm, drill 0.3 mm.

The in-memory native full-copper check against root's critical/thermal candidate SHA256 `5f82894e6de8fd263dfcb28bf86b09a0b9ea2574095bc47138b61a2c806aaf3a` shows that 1.5 mm removes all new track-versus-pad and track-versus-track findings. Increasing to 2 mm produces no additional benefit for this path. The via passes full generic spacing against every existing pad, track and filled zone on both faces with no exception. The path still conflicts with the current SOURCE front copper zone at about 3.346 mm. That zone must be clipped/refilled around the new actual DRAIN copper at the normal 4 mm target plus design margin; the zone cannot inherit the proposed component exception. Final SOURCE continuity and thermal area must be checked again.

Evidence: `proposal_minimal_probe.py`, `drain-minimal-proposal-report.json`; initial broader comparison retained as `proposal_probe.py`, `drain-proposal-report.json`. This is explicitly a hypothetical changed-contract experiment; it is not an active source/rule update or a claim that the routed board passes. No CAD was saved by this reviewer.

Correction owner: `/root`. Observable closure: actual owner decision on the specific changed basis/escape scope, fresh matching spatial/configuration consumers, actual saved route and refilled SOURCE zones, then independent full-copper validation, native checks and affected reviews on the resulting revision. The current routing gate must remain unaccepted until that work is complete. The final four routing reviews remain due.
