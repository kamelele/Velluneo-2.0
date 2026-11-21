# Reality review — PIN-REALITY-01 and SCOPE-SYNC-REALITY-01

- Actual reviewer: `/root/spec_reality`, independent of the writer and source implementers.
- Date: 2026-11-17. Scope: pre-CAD physical-terminal intent and bounded r12 accepted-scope synchronization only.
- Recommendation: `ready_for_human_review` of the new physical-pin intent; content review pass for the specification-scope sync. Neither recommendation is circuit, schematic, manufacturing or physical-safety acceptance.
- Exact connectivity intent digest: `b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57`. Graph approval is null and must remain unapproved until a genuine decision bound to this digest.

## Evidence and actual checks

Read root AGENTS.md, pinned project instructions, coordinated workflow, existing-project guide and Reality Checker role. Inspected every frozen file, the finalization decision/review and r12 addendum/machine unknown resolutions. All 11 intent and five scope-sync hashes match below.

Independently enumerated 28 components and 73 terminals: 69 connected terminals plus four explicit T1 NC terminals. Every terminal appears exactly once, every net has at least two members, and CSV/parts/JSON agree. The two electrical domains have disjoint net membership. This is inventory/manual electrical review, not KiCad export comparison, ERC, DRC or physical insulation validation.

Checked all 12 registered local native evidence files against source hashes and byte sizes. Directly viewed native rendered MB10S p1, UCC functional p3 and mechanical outline, TDK bobbin p3, MOSFET p1, both ST rectifiers p1, US1M p1, SMBJ p1 and Panasonic family polarity/dimension page. Prior native capacitor/resistor/source-conditioned operating-limit reviews are retained only in their original scope. The native component/source artifacts are inspected evidence, not actual lot measurements or assembly approval.

Manual functional checks: MB10S pin1 positive/pin3 negative and AC2/4; UCC VDD1/VS2/NTC3/GND4/CS5/DRV6/HV7 with the vacant right-row position; Q1 G1/D2/S3/D4; steering diode anode at drain and TVS cathode at clamp/anode at bulk-positive; aux/output rectifiers anodes at flyback-positive undotted ends and cathodes toward positive storage; polarized capacitors positive toward their positive rail; nonpolar C0G capacitors across VDD/primary return; gate-source pull to SENSE, CS series compensation and primary low-pad GND; two isolated-output 20k bleeders in parallel. No polarity or functional net-membership defect found.

Transformer phase check: primary dot1 is BULK_POS and finish5 is DRAIN. Equal-polarity auxiliary dot2 is PRIMARY_GND and secondary dot6 is OUTPUT_NEG. Thus their undotted ends4/10 are negative during primary switch-on and positive during flyback switch-off, matching DAUX/DOUT anodes. Pins3/7/8/9 have no winding or electrical net. This is a new custom winding intent, not a TDK finished-transformer promise. Physical winding, insulation, leakage, losses, leadouts and phase/withstand acceptance remain unqualified.

## Findings / preserved obligations

No new blocker or major defect in the bounded physical-pin intent was identified.

- PIN-REALITY-001 — note, library/footprint gate: preserve UCC upper-right functional HV7 at the physical omitted-lead geometry despite the generic outline's geometric 8 label; preserve Q1 native drain-tab4 (or a separately reviewed explicit alias). Observable closure is an independent native symbol/footprint-to-physical-position check plus fresh generated-CAD membership comparison. Coordinator owns this already-disclosed next check; this is not owner approval of a footprint.
- PIN-REALITY-002 — note, transformer/placement/process gates: engineered terminal and dot assignments do not establish isolation, fit, leakage target or a manufacturable winding. Require the actual winding/insulation/leadout contract and appropriate later checks. No new demand for measurements before ordinary draft capture is introduced.
- SCOPE-REALITY-001 — note, evidence integration: current requirements.json has no evidence objects while resolved specification questions refer to E-SPEC-SCOPE-REVIEW. The coordinator explicitly identified this as pending. Create a genuine review/owner-source-bound record and rerun the fresh installed requirements matrix before claiming a formal machine gate pass. A placeholder ID alone is not evidence or stage approval.

Existing RC-BIAS-001, RC-COMP-002, RC-MODEL-001, RC-CTRL-MODEL-001, RC-PROT-001 and sampling/fault/service/thermal/process obligations remain open in their original affected scope. This review closes none of them.

## Bounded scope-sync conclusion

The r12 addendum and U01/U02/U03/U04/U14/U15/U16 resolutions are consistent with accepted desired behavior, planning/test methods, proposed process direction and the scoped owner-decision record. Supply/frequency, optical criteria, single-prototype versus future-family evidence, thermal arrangements, fault/recovery and service goals are not represented as measurements. Lifetime screens do not purport to prove population reliability. Source-family/classification leads do not establish full-clause conformity. U05-U13/U17 implementation, interface, insulation, material/process and test-readiness obligations remain open at their declared gates.

The scope decision predates the new graph and cannot approve it. The graph README now explicitly preserves full specification and pre-capture interface prerequisites. This is a content pass for scope synchronization, not an assertion that its pending evidence linkage, fresh preflight or formal acceptance already exists.

## Exact inspected physical-pin inputs

| File | SHA-256 |
|---|---|
| owner-scope-acceptance.md | 724c17767acef7f4768c870529746470e837d427348d708051a41b3c17cc2500 |
| native-source-register-secondary.json | 7c3333ec2122c8f57f053e7ba81ac329d61acaaab696ef3dca3735f5a36844c9 |
| inventory-check.json | ff20c54cf9b930a3583c0cbc1dad81b614b7c680ce7ff5524d91a2af4637a098 |
| native-source-register-primary.json | 41b7de71c5abe4b5630ab500f2657f02640b035bb6a02aee68d071b0d55797af |
| intended-connectivity.json | 8344773bcf5a6228a099b481ef67b69e639ebd725af68ac44360831134995179 |
| parts.json | 808295707d760d62e198794e6f406f1879cdff322e48412e9bd4d2df784bc221 |
| README.md | 5afdbec11c699794faeb966c573f4cdcda98e28a455bbd1af9c8579956e4c78a |
| pin-basis-primary.md | f02c2faa3cf05bd833c44a56180a7f53140158d84717fa14907b37ea9d7d56a4 |
| parts-and-pin-map.csv | fd296432fbae64d14542b0b589399ba6ea1a497b7dc4da1d0a3a94929f6ca0d3 |
| local-terminal-contract.md | 6b82a32d748c79b55f9b0e83b7c651575417e410e839f9e03b9bdd76e00167ee |
| pin-basis-secondary.md | 6323b4bf6d7661210e3081af8eeb39779bf153d198120fdaf24f8b81467ebc32 |

## Exact inspected scope-sync inputs

| File | SHA-256 |
|---|---|
| requirements-and-plan.md | a0c2867d511313741495cf9d2696590e756c0d6a335d7180df5409cc6532b34e |
| requirements.json | de7f1386defa830eed6a79d793b4584704601978caa41f05d1d13b690d31ab8b |
| finalization/decision-packet.md | ea6ef879ed417a6ced7360e1434ce873637becf548e33cf261296bcfa9401fba |
| finalization/review.md | 112fc650642c2871de6ddb6a1612b7ad469f8dfe5b9a27d14c0b782f3ae5d4ba |
| schematic-intent/owner-scope-acceptance.md | 724c17767acef7f4768c870529746470e837d427348d708051a41b3c17cc2500 |

Only this isolated review report was written. No CAD, source-contract edit, simulation, test, supplier action, order or human approval was performed.
