# Independent Change review — pre-CAD intent and accepted-scope synchronization

2026-11-17. Actual reviewer: /root/spec_change. Read-only inspection; sole output is this report. Declared remote baseline:2578929a50d68ce576d10348b9865001273e5bd8. This review does not independently certify a full repository checkout or compare a newly generated native CAD export, because this packet contains no new CAD.

Recommendation: **ready for owner review of the new graph**, with specification evidence integration and applicable pre-capture interface prerequisites still required. **Scoped scope-synchronization pass**, not specification-stage approval. No new actionable Change defect found in the final frozen inputs. All original circuit/model majors retain their scope and severity.

## Actual inspection and execution

Read repository AGENTS.md, installed project instructions, Change role and intended-connectivity instructions. Inspected all11 packet inputs and supplemental5-file synchronization inputs; all hashes independently match their manifests. Independently recomputed the canonical intent excluding approval: `b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57`. Exact graph-file SHA256 is `8344773bcf5a6228a099b481ef67b69e639ebd725af68ac44360831134995179`; these identify different objects and are not interchangeable.

Independently ran the locked connectivity.validate_intent function with Python bytecode disabled. It returned successfully. Separately enumerated28 components/73 terminals/21 nets/four T1 no-connects: every physical terminal is assigned exactly once, no extra/missing/duplicate terminal; readable CSV matches parts.json and the actual net membership. All seven basis-source paths and digests are bound to inspected files. All12 registered native PDF files match the stated byte lengths and SHA256 values. Native URLs are separately recorded; local_evidence_path is honestly local evidence, not a portable dependency guarantee.

Visually inspected native UCC functional-pin page3, MB10S page1 and EFD25 bobbin page3. UCC28711 functional pin7HV is upper-right with the lower vacant position; physical custom mapping must preserve this layout and cannot be inherited from an ordinary compact seven-pin or generic SOIC8 footprint. MB10S native1+/2AC/3−/4AC matches the graph. TDK bobbin1 opposes10, with the declared custom winding terminals and unused3/7/8/9 explicit. Inspected remaining native-derived pin/polarity manuscripts and graph, without claiming an independent exhaustive visual audit of every PDF drawing or an authored library footprint. Q1 tab4 and drain2 share DRAIN; local diode1K/2A and capacitor1+/2− contracts are explicit. T1 polarity follows the declared off-time rectification convention. Primary and secondary net sets do not merge; this is electrical membership, not insulation evidence.

## Change and approval boundaries

The new source-derived numbering explicitly supersedes the generic legacy bridge/controller assumptions; no old CAD, old approval, or model D/G/S order is accepted as the physical-pin basis. New symbols/footprints, pad positions, winding construction, creepage and Kelvin geometry must still be independently inspected at the relevant later stage. This review does not perform semantic native-CAD parity, ERC, DRC or spatial checks before CAD exists.

The recorded owner message accepts the preceding scope/desired-performance summary. It predates this graph and is not approval of its digest. approval remains null, and README expressly requires real owner acceptance of this exact new intent plus specification-stage completion and applicable pre-capture prerequisites. Neither this review nor the inventory-check pass supplies that decision.

Architecture A, offline covered-base tool-free replacement, common three-colour base, eventual family requirements and one initially measured colour by30September2027 are preserved. J1/J2 are internal wire terminations; they do not silently replace the keyed user dock or its50-cycle obligation. Analytical18–27V/~250mA and component values remain an engineering candidate, without a false30V product constraint or proven supply rating.

Revision12 addendum explicitly supersedes old pending-scope wording; the historical body is retained as history. The machine resolutions of U01/U02/U03/U04/U14/U15/U16 reflect accepted planning criteria from the exact earlier finalization packet, not measurements or technical qualification. U05–U13/U17 retain their applicable implementation, material, interface, laboratory and release work. requirements.json evidence is still empty: E-SPEC-SCOPE-REVIEW is a pending integration reference, not an established evidence pass. Fresh integrated preflight and final review evidence remain required before a formal specification gate. Finalization/review.md remains a historical pre-owner-decision record, not an updated approval.

RC-BIAS-001, RC-COMP-002, RC-MODEL-001, RC-CTRL-MODEL-001 and RC-PROT-001 remain open. No circuit freeze, model pass, safety compliance, JLC stock/assembly guarantee, manufacturing authorization or physical measurement is inferred.

## Findings and invalidation

No new Change finding requiring correction before owner graph review. Preserve the existing major findings and stage blockers. Any later pin-membership, part/terminal-map or basis-source change requires refreshed canonical digest, affected reviews and genuine owner intent decision; earlier scope acceptance cannot be reassigned. When CAD is generated, compare a fresh native physical-pin export and inspect actual saved symbols/footprints before treating connectivity or schematic verification as passed.

## Pre-CAD packet frozen inputs

| File | Independently verified SHA256 |
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

## Scope synchronization frozen inputs

| File | Independently verified SHA256 |
|---|---|
| requirements-and-plan.md | a0c2867d511313741495cf9d2696590e756c0d6a335d7180df5409cc6532b34e |
| requirements.json | de7f1386defa830eed6a79d793b4584704601978caa41f05d1d13b690d31ab8b |
| finalization/decision-packet.md | ea6ef879ed417a6ced7360e1434ce873637becf548e33cf261296bcfa9401fba |
| finalization/review.md | 112fc650642c2871de6ddb6a1612b7ad469f8dfe5b9a27d14c0b782f3ae5d4ba |
| schematic-intent/owner-scope-acceptance.md | 724c17767acef7f4768c870529746470e837d427348d708051a41b3c17cc2500 |
