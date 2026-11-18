# Corrected boundary: authoring a draft versus accepting a stage

Read-only implementer /root/compact_led_heat inspected the actual requirements and pinned toolkit code at this base. Root checked the named source locations. This is not a rules waiver or a new product requirement.

- requirements-and-plan.md U03 and current addendum explicitly say an external pre-fabrication reviewer is not an owner prerequisite; the coordinator and four independent contexts perform design reviews. Proposed process constraints may remain explicit while engineering is performed.
- The actual U11 still requires material/stackup/copper/service evidence before placement/process acceptance. U12/U13 and laboratory bookings concern affected physical tests/release, not authoring a file. Current requirements are unchanged.
- In the exact toolkit scripts/pcb_rules.py, the mandatory fabrication confirmation/assembly confirmation/full barrier-card checks are within the release branch (aroundline323). docs/reviews.md still requires power/startup/protection calculations for schematic acceptance, and scoped clearance/creepage/rule evidence at routing.
- docs/agent-workflow.md still requires genuine human stage decisions. A draft does not manufacture one. R-FAULT/R-THERMAL still require designed fault cases and justified trip/restart/sensor-fault behavior before schematic acceptance; later measured fault/thermal screens are distinct.

Therefore: author the explicitly provisional native PCB workspace requested by the owner; keep schematic/placement/routing acceptance blocked where actual criteria remain open. No final ordered board, laboratory test, supplier confirmation or full lighting compliance is inferred.
