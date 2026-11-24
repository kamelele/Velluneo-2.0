# SC09-SB02-A4 — bare PCB receipt and manual assembly inspection plan

Actor: /root/sb02_final_simplicity_review. Scope basis: intended-connectivity.SB02-A.json, calculations.SB02-A4.json, fault-scope.SB02-A4.json and assembly-geometry-notes.A4.json. This is a planning document, not a record of inspection, final-source acceptance or powered-test authorization. Bind the following checks to the final accepted source and fabrication manifest before use. Rejected final-source-v1/export-v1 are excluded.

## Receipt, before assembly

1. Identify the board revision, supplier lot and final Gerber/drill manifest. Compare the received board with the accepted front/back copper, mask and drill views. Confirm the intended 51.2 x 39.5 mm outline, two copper layers and specified 1.6 mm FR-4/1 oz/lead-free HASL process; record the actual supplier documents and measured dimensions.
2. Inspect both sides with magnification for shorts, broken tracks, damaged mask, debris, plating defects and displaced drills. Check the documented 2 mm high-voltage copper separations and the explicitly permitted 0.3 mm local control groups against the final views. Do not infer isolation or SELV from these distances or from solder mask.
3. Compare all holes, polarities, wire ports and D1's three physical copper contacts with the assembly drawing. Record defects before rework. Continuity measurements are unpowered and must be compared with the intended net graph; an ohmmeter cannot establish withstand voltage or powered function.

## Parts and manual assembly

1. Match received manufacturer, full MPN, package, pin numbering and polarity to the final BOM and primary land evidence. Preserve R16 as populated. Leave R18, R19, C9 and C10 unpopulated. J1 and J2 are wire solder ports; there are no purchased connector bodies.
2. Check the exact D1 package against its reserved assembly envelope before mounting; the displayed contact/assembly reservation is not a dimensioned plastic-body model. Form R10 leads for the documented flat placement without loading the body seals or violating the accepted clearances.
3. Seat the capacitor cans upright. Confirm the whole C7 can projection, including tilt, stays within the radius 5.45 mm protected reservation. Preserve capacitor vent space. Inspect rear BR1, trimmed leads and solder protrusions. The 22.4 mm planning envelope is not an accepted installed maximum or enclosure-fit result.
4. After assembly, inspect solder joints, bridges, component orientation and both faces beneath/around large bodies. Check continuity against the independent graph and confirm the AC input and LED output ports are on their respective opposite edges. Record the actual populated BOM, deviations and rework. Any substitution or changed copper requires affected verification.

## Handoff to a separately qualified powered-test activity

This plan stops before energization. It provides no procedure to insert mains faults or connect/disconnect an energized LED load. The nonisolated output is mains-referenced; CC and OVP share a feedback path and are not independent safety disconnection.

Before any powered activity, the responsible qualified human must document the exact assembled revision, guarded setup, external protection, instrumentation and voltage ratings, test-specific current/time/energy limits, stop conditions, temperature attachment points and handling/discharge verification. Inrush resistor pulse capability, feedback startup/hot authority, stability, open-load OVP response, LED-short behavior, surge and actual temperatures/efficiency remain unmeasured. The calculation file's temperatures and 85 V/300 microsecond values are acceptance targets, not demonstrated limits.

The isolated-C6 RC times apply only after all replenishment has stopped; input C7 can continue feeding the buck after AC removal. Neither a waiting period nor a bleeder estimate proves safe handling. The qualified operator must verify actual stored voltage using the documented setup.

A bare-board fabrication decision, this checklist, and clean CAD checks do not authorize a supplier order, powered testing or finished-lamp compliance.
