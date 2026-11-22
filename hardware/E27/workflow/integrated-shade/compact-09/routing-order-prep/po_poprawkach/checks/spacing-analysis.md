# SC09-ROUTE05 independent spacing feasibility

Actual actor: `/root/r05_spacing`. Initial read-only source: SC09-ROUTE04 PCB SHA256 `9b73c61c34dc28fceff2e9d2265fcfb1280053245c9840f4e7c0bb39d782fa87`, branch commit `d011ef6a865f6dd7f06825f233b2465238ecba27`. The subsequent coordinator-authorized private implementation is recorded separately in `writer/HANDOFF.md` and `writer/HANDOFF.json`.

The original strict report contains 35 findings: 12 copper-edge findings and 23 different-net spacing findings. `spacing-object-inventory.json` binds each finding to actual native pad/track coordinates, width, net and UUID. All twelve edge findings are avoidable and were eliminated by the 51.2 x 33 mm outline proposal. The 1 mm target is now also enforced by native managed configuration, with conservative minimum 1.099988 mm.

Five pad pairs intrinsically miss the generic 2 mm surface target with the current exact manufacturer lands:

- BR1.1 / BR1.3: 1.500002 mm, BUS_RECT / DC_RETURN.
- BR1.2 / BR1.4: 1.500002 mm, AC_FUSED / AC_N.
- U1.2 / U1.4: 1.940002 mm, M / BUS_FILTERED.
- U1.3 / U1.4: 0.670002 mm, FB_INDUCTOR / BUS_FILTERED.
- D1.1 / D1.2: 1.500002 mm, FB_INDUCTOR / DC_RETURN.

U1 adjacent pin pitch is only 1.27 mm before subtracting land widths. No board enlargement, component relocation or trace reroute can turn its 0.67 mm land gap into 2 mm while retaining the device and correct manufacturer footprint. Reducing land widths or assigning a different net name to force a passing report would not be a valid fix. Other package gaps likewise persist when moved rigidly anywhere on the PCB.

The eighteen remaining strict entries involve short escape tracks near these same BR1/U1 pad pairs. Their gaps range 0.770001–1.924644 mm; they are all inside the already declared finite pad/escape assessment scope, and do not identify unrelated long field copper failing outside that scope. For example any B.Cu escape beginning in the small U1.4 land is initially closer than 2 mm to U1.3. Choosing another exit may reduce duplicate report entries but cannot close the controlling intrinsic land gap. A new via-in-pad process merely to reduce the report count would add manufacturing complexity and would not remove the pad-pair failure.

The strict original report must therefore remain FAIL with its five intrinsic pad-pair failures and associated escape observations unless the architecture/parts/footprints are genuinely changed or an authorized person accepts an exact qualified deviation. The existing bounded PASS is an engineering laboratory geometry assessment, not that approval and not normative insulation qualification. No new exception, floor reduction, masking credit or global target change was introduced. There is no claim that ordering a bare PCB proves mains safety.

All permitted avoidable geometric manufacturing issues found in this scope have concrete corrections in the private candidate: edge material reserve, D1.2 ordinary via moved outside its SMD pad, and silkscreen clearance. Components, MPNs, graph, Kelvin/C5 requirements and manual assembly remain unchanged. See the final source-bound reports in `writer/` and the coordinator's complete release-review packet for current dispositions.
