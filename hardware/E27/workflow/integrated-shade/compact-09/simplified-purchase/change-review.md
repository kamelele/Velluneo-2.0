# SC09-SB01 Change review

Reviewer: `/root/simple_change_review`, independent read-only context. Frozen manifest SHA-256: `8035ba4c7b87abf9926d00b1b05ab22d21cbc5357870bcd294a8142d240c8243`. PCB SHA-256: `a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`. All 166 manifest files verified unchanged at review.

Disposition: **ready for review as an engineering candidate only**. No new change-specific defect was found. This is not fabrication acceptance or a powered-test authorization.

The reviewer independently loaded the preserved original PCB from the checkpoint ZIP and the final saved candidate using KiCad 10.0.6 pcbnew. The 19-reference set, 46 physical pin partition, 11 nets, two copper layers and outline are unchanged. Only C1, C4, RV1, T1 and BR1 placements changed; both opposite-edge interfaces remain in their original positions. Project rules, custom DRC and three electronics-rule configuration/consumer files are byte-identical to the baseline. The exact retained independent intended graph also matches the fresh schematic netlist export.

Six electrical substitutions are present: RF1 10 to 47 ohms in the fusible FW20A family; C1 47 nF pulse film at 1000 V; TDK 275 VAC MOV; Wuerth 7687709152 1.5 mH high-voltage choke; Royalohm 3.65 ohm R6; US1M 1000 V diode. U1 changes tube/reel ordering only. The placement and local routing changes correspond to the changed package envelopes and removal of the sensitive feedback area from below T1.

An independent comparison of strict-spacing reports found the same 23 numerical signatures, including layer, type, net pair, object kinds, target and gap rounded to four decimals. **The full spacing result remains FAIL.** This is preservation of known bounded prototype limitations, not a fresh approval or compliance waiver. The frozen native ERC/DRC/parity reports each report zero findings; root remains responsible for final integrated execution.

Previous exact-source acceptance is stale for SB01. Retain changed-part assembly inspection and current, thermal, fault, nonlinear startup and surge test gates. Historical manufacturing artifacts are labelled and must not be used for this candidate. Remote branch and main verification is an integration responsibility; no remote state or physical test is invented in this review.

Documentation-only refresh: all manifest hashes were reverified after historical wording/key corrections. Native CAD, graph and rules are unchanged.

Final structured-note refresh: every manifest hash verified and every JSON input parsed successfully. Native CAD, graph and rules remain unchanged.
