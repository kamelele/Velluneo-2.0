# Independent model evidence review and integration

VEL-MODEL-01 r1,2026-11-16. Preliminary publication only; circuit/model acceptance remains blocked. No human stage decision, working-hardware claim or full converter simulation.

## Final frozen inputs

| File | SHA256 |
|---|---|
| run_checks.py | c597ea51625e1ec4d3b222612f6e42d162c4c8b26339ef4ba3f92be914fd07bb |
| results.json | 407dd27ca59e1ebd7d8e38ead7cf1d327c7bb235696b9c44d466c20b0552deda |
| native-transient.log | 1739283e35202448f6dbf3405da689bf46a86c1dc3c522b6393374a869aa905e |
| cv-coarse.csv | 9426098963b5e51be7b085dd9c3a3bcd3567b488f710de170131a41651607e06 |
| cv-fine.csv | 0edb46f0eb0dc17b28f1f68c2faa843bd71330cec1f6fcbf38c9e5d42e32b43b |
| sources.json | cc84924e75d18f1ac29b61768360afef3703679c521b6fba730979b920d78701 |
| findings.md | 2699785d1f5733bdb13f2fd0da69cbe6570d2393dd01a90ce11bbd5761f5f0a5 |
| task-and-contract.md | b4650c11ea5b7eb72847116efec66d93133f590162c265d47e07393c1a12f15f |

Manifest and this review are lifecycle metadata outside the eight input files. Native sources are reference-only; numeric model parameters were retained. Productr11 freshly confirmed at blob6493b29bd33fbde1f3c61c5e995b11447cb83e9b, draft baselinec78cbf4e0d4d7d977ac5e7017a00244db7a63773.

## Actual separate read-only coverage

| Role / actual context | Inspection and execution | Recommendation |
|---|---|---|
| Reality /root/spec_reality | Eight hashes, independent native datasheet-table/calculation check; unchanged script executed in isolated tmp/reality-model-run, expected exit1. Results, both CSVs and native-transient log reproduced byte-for-byte. Final source-only metadata refresh checked separately, numerical scope retained. | Ready for preliminary publication; no electrical/model pass. |
| Overengineering /root/spec_simplicity | Eight hashes; code/results/log/contract and bounded alternative scope inspected. Both CSV integrals independently recomputed. No simulator rerun or independent source-table validation. Final source-only refresh separately checked. | No new complexity finding; no parameter fitting/extra circuit/topology justified by unknown evidence. |
| Completeness /root/spec_completeness | Eight hashes, sourcePDF identities, extracted native-table conditions, code/log/results and CSV arithmetic; no duplicate simulation or PDF-render inspection. Final derived-artifact/archive metadata checked; seven unchanged inputs retain earlier scope. | No preliminary publication defect; no physical/model approval. |
| Change /root/spec_change | Eight hashes, requirement preservation, source-conditioned comparison and final driver-index addition inspected. No numerical rerun. Independently verified final metadata and evidence-table corrections. | Preliminary publication after two minor documentation fixes, now independently closed. |

CH-MODEL-001 (minor): source URLs and derived-payload hashes were ambiguous; corrected by explicit artifact types, extraction details and separate downloaded-archive hashes. CH-MODEL-002 (minor): blank line split the added index row; removed. Change independently verified both corrections. The source metadata change altered only sources.json; remaining seven input hashes and executed numerics are unchanged. All four final reviewers cover final inputs or explicitly retained unchanged scope. No vote or diagnostic implementer substitutes for these inspections.

## Acceptance and retained findings

Actual RC smoke/DC/AC execution and failed native-POLY transient are documented. The native-POLY capability gap was corrected locally; model transient convergence and capacitance representativeness were not. Byte-for-byte reproduction confirms reproducibility, not physical accuracy. Diagnostic implementer /root/model_compatibility supplied plugin compatibility evidence only; it is not a fifth reviewer or human approver.

RC-MODEL-001 remains major/open for switching-model acceptance. RC-BIAS-001 and RC-COMP-002 remain major/open; RC-CLAMP-001 and all retained protection/service/thermal findings remain open within their original scope. No Qg, actual controller startup, hot clamp/SOA, manufacturing, insulation or laboratory pass is inferred. Candidate STD2N80K5 is not selected. No independent reviewer waived missing source/measurement evidence.

Integration scope: add the eight inputs, frozen-inputs.json and this review under driver-study/model-qualification/; update only driver-study/README.md on existing draft branch. Preserve requirements, main, prior studies, CAD/libraries and manufacturing files. Verify remote contents at resulting revision. This is neither formal specification acceptance nor authorization to start CAD, order, merge or energize hardware. Next task is discriminating controller/drive/node-charge evidence, as owned in task-and-contract.md.
