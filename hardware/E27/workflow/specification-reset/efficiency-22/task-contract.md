# EFFICIENCY22 task contract

Base63c7a3fed59d7807bd1b71cf9058175b04a22f4b,21November2026. Owner explicitly
requests a better output diode and resistor optimization without weakening startup
or protection, updated efficiency/temperature calculations, toolkit/GitHub and
updated compendium. Root owns all new CAD/library/analysis/package writes.
Read-only bounded research actors: /root/eco22_diode and /root/eco22_resistors.
Four distinct read-only role contexts inspect the final frozen body.

Write scope: new efficiency-22 revision and compendium-23, plus index entry.
Historical C16/C17/VIS18/LED19/POWER20/COMPENDIUM21 remain byte-identical.
Candidate diode must retain200V or greater rating, preserve pin polarity and
appropriate fault/current/surge capability, fit a source-derived footprint and
have an exact catalogue purchase route. Account for reverse leakage/capacitance,
auxiliary voltage and PSR/no-load behavior, not only forward drop. Reject blind
100V replacements and optimistic hot/cold formula comparisons.

Resistor acceptance preserves input inrush/fuse coordination, bulk/output passive
discharge and control/fault-sense functions. Startup changes must meet source-
conditioned UVLO-on23V hot-leak corners and<=1s accepted startup target, with no
lower worst-case net charging margin or higher normal zero-draw VDD ceiling.
Use exact working-voltage/power/TCR/tolerance/footprint/source parts. Unknown
fault-sink/retry dynamics and measuredstartup remain retained holds. Reject
large resistor scaling that fails any adopted startup corner. Do not force a
nominal saving by removing protection or claiming unknown physical behavior.

Deliver comparative calculations with identical assumptions and explicit physical
uncertainty, updated native source/BOM/checks/exports as applicable, updated offline
ZIP containing current matched materials and dated sourcing, source hashes,
four real reviews and independent closure checks, GitHub publication/byte checks.
No order, manufacturer message, powered measurement or stage approval is implied.

Initial research contexts later received separate bounded implementation leases:
startup/ to /root/eco22_resistors and diode/ to /root/eco22_diode, both released.
See ownership.md. They are not final independent reviewers of their implementation.
