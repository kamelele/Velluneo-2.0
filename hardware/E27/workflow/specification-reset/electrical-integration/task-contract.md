# Task ELEC-CLOSE-01

Parent: accepted specification r12, draft PR1, remote baseline bb28f9c81f902f3e9de92dfab5ac17fce0e75fb4. Stage: schematic preparation, not schematic acceptance. Requirements R-SUPPLY/R-LIGHT/R-CCT/R-COMPAT/R-OFFLINE/R-FAULT/R-EMPTY/R-THERMAL/R-BASE-LIFE; open contracts U05–U09 remain.

Goal: improve actual startup/source/winding/input evidence, identify deterministic passive-discharge weakness, independently prepare a specific physical-pin ECO and expose unresolved optical/regulation/capacitor budgets. No target relaxation, placement, routing, manufacturing, sourcing order or invented bench measurement.

| Actor | Write ownership | Required handoff |
|---|---|---|
| /root | electrical-integration root files; project-index current entry after integration | Numerical reproduction, proposed graph/BOM, actual native results, same frozen packet and lifecycle records |
| /root/model_compatibility | electrical-integration/startup/ only | Source registers,128ramp/768hybrid cases, exact reproduction, limitations |
| /root/support_design | electrical-integration/magnetics/ only | Winding/loss construction, actual source-solid check, exact reproduction, limitations |
| /root/spec_reality | Read-only frozen sources; review output tmp/eclose-review-reality.md | Reality Checker |
| /root/spec_simplicity | Read-only frozen sources; review output tmp/eclose-review-simplicity.md | Overengineering Reviewer |
| /root/spec_completeness | Read-only frozen sources; review output tmp/eclose-review-completeness.md | Completeness Reviewer |
| /root/spec_change | Read-only frozen sources; review output tmp/eclose-review-change.md | Change Reviewer |
| Kamil Stępak | Actual human intent/stage decisions | Exact graph acceptance if chosen; no agent approval substitution |

All CAD/library write leases remain with/root and inactive in this task. Existing canonical graph, requirements/hardware configuration, schematic, libraries and assignments must remain byte-identical. Only electrical-integration/ and project-index current summary may be published. Vendor originals remain external; preserve URLs/hashes. Source/input changes during review require renewed affected review.

Acceptance checks: fresh reproducible calculations at stated domains; all handoff hashes and numerical values compared; proposed31component/79pin graph unique/complete membership and BOM/native basis consistency; fresh native checks honestly scoped to unchanged28-position graph; all four distinct readonly reviews of same frozen input; no hidden physical test/stage approval claim. Existing major findings may remain for an explicitly incomplete schematic-preparation packet, but stop acceptance of a finished schematic or subsequent PCB.

Stop/escalate: unexplained reproducibility failure, shared write, unsupported source rating, changed intent without actual owner decision, review conflict or unresolved safety/physics finding. No new user deadline/budget is invented. The September2027 prototype remains the product objective, not an approval for unverified release.
