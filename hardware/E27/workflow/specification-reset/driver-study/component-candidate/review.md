# Component proposal r2: independent review and finding ledger

VEL-COMPONENT-01 r2, 2026-11-16. First published revision is r2 after correcting the internally reviewed 600 V candidate. **Preliminary analytical publication only; circuit freeze remains blocked.** No stage approval or working-hardware assertion.

## Frozen final technical packet

| File | SHA-256 |
|---|---|
| calculate.py | 645be3e3f09e4058a5d93f1a7e1fb946756a2720b9cdd06397e7ad2fa83de724 |
| results.json | d87c14c11e44aced0eabebf0346bd7d4d648f0d8fbc59fa76ebcfd18f4d60186 |
| findings.md | 20e3fa52fef24a9a206808da4a61e38dc88b401612ab7acbc7a6c75ce09a516d |
| parts.csv | ee193e149079fa015dbebcbed6bb70ce652a6bc18a50bddd5a4db9890ecbf68c |
| sources.json | 25b78c8429fc46db9c8450cdc4bc2865db11ab6a050cef582a619d15f30f6602 |
| verification-contract.md | eaa99a377d7a91d404632fbb978f475e44d8a439bb65ae3c6baa6382ed5ccd85 |

Six inputs are also listed in frozen-inputs.json. Review/index lifecycle metadata is separate. Native vendor files remain reference-only scratch inputs; their identities are preserved without redistributing their contents. Product r11 blob 6493b29bd33fbde1f3c61c5e995b11447cb83e9b was freshly confirmed unchanged through GitHub. Parent bias results hash is asserted by calculate.py; historical studies remain unchanged.

## Actual independent reviewers and final coverage

| Role / actual context | Evidence checked | Recommendation |
|---|---|---|
| Reality `/root/spec_reality` | Six final hashes; native KEMET values, Panasonic ratings/frequency factors, TDK paired-core AL/Amin and ST replacement rating tables; full final execution exactly reproduced results.json. Independently checked waveform ESR/LED/bleed coherence and step-size sensitivity (0.03799 mA peak difference). | Preliminary publication only. Narrow rating-choice correction verified; actual drain/clamp and startup major findings remain open. |
| Overengineering `/root/spec_simplicity` | Six final hashes; code/results/BOM/contract and targeted r2 change; no full rerun or independent manufacturer-table validation. | No new complexity finding. Two-cap reference and same-package 800 V substitution are bounded. Finished size/cost/source/thermal comparison remains open. |
| Completeness `/root/spec_completeness` | Six final hashes, native-source integrity, stored summaries and requirement/contract coverage; targeted r2 component consistency. No duplicate full run or independent PDF interpretation. | No new completeness finding for preliminary scope. Qualification gaps remain explicit. |
| Change `/root/spec_change` | Six final hashes/native-source identity, parent dependency and product/architecture preservation; targeted r2 rating/current-charge wording and proposed index. No duplicate full run. | No requirement drift or false acceptance. Final index keeps all major conditions. |

All four contexts inspected the final r2 changes and retained explicitly unaffected r1 scope. Their results recommend preliminary discussion/publication only, not circuit acceptance. The coordinator is the sole writer and cannot grant human approval.

## Finding history and acceptance stops

| Finding | Severity / scope | Status and observable closure |
|---|---|---|
| RC-COMP-001 | Major / inadequate initial MOSFET rating choice | **Verified closed narrowly by Reality.** At 357.8 V bus plus refreshed OVP reflection and assumed 100 V leakage overshoot, 608.974 V exceeds the initial 600 V rating. STN1NK60Z rejected, STN1NK80Z 800 V substituted; 16 ohm loss and typical-only 7.7 nC source wording corrected consistently. This is not a real transient/clamp pass. |
| RC-COMP-002 | **Major / actual drain-clamp-SOA qualification** | **Open**, coordinator. Bound leakage spikes, OVP/stop latency, mains surge and clamp faults; demonstrate device/clamp SOA and thermal margins. No closing assumption of a 100 V spike. Linked to retained fault work. |
| RC-BIAS-001 | **Major / UCC startup** | Open, coordinator. Effective reference capacitors narrow the gap, but ≤12 nC actual-drive charge, ≤4.3 mA draw and ≤0.300 ms acquisition remain hypotheses; actual auxiliary takeover/temperature envelope unqualified. |
| RC-PROT-001 | Major / historical TPS candidate | Open, unchanged. Substitution is not closure of the old circuit. |
| RC-PROT-002 / RC-PROT-003; RC-BIAS-003 | Retained actual control/fault/service/thermal | Open. Normal witnesses and lower linear flux do not prove repeated-fault immunity, insulation, accessible-energy or safe service delay. |
| OE-LED-01 | Retained final implementation comparison | Open. Verify optical/thermal/regulation/protection and finished size/source/assembly burden before selection. |

The internally reviewed r1 code hash was 49d7c76eb1ec011bbf2f22b7ef25753e107b34e36c962d0e231f594fee6e7f95 and results hash 0a2e7ae02dae6a2edbd371ec4bba16ad0465de82708607e6445b481b6da777eb; they are not the accepted final reproduction inputs. R2 preserves the rejected-candidate rationale/source and finding rather than erasing the fault.

## Integration scope

Submit eight new analytical/contract/review files to driver-study/component-candidate/ and update driver-study/README.md on the existing draft branch. No requirements, prior studies, CAD, libraries, manufacturing outputs or main-branch files change. The input parent commit is 0f1d8502c05f91f36c7a42a4e7bab58e0538aad0. Remote readback must exactly match submitted UTF-8 contents.

Actual evidence is analytical arithmetic, a constructed numerical storage/diode witness, manufacturer source inspection and independent reproduction. TI's additional PSpice library was encrypted and not run; native-series PDF retrieval failure is recorded, not passed. No installed-toolkit doctor, ERC/DRC, photometry/EMC/thermal/fault test, supplier message, order, merge or human stage approval occurred. Next engineering work is the real startup and drain/clamp/SOA envelope, followed by the remaining complete specification and electrical-interface intent gate.

## Separate public sourcing observation

On 2026-11-16 the coordinator opened JLCPCB's own [STN1NK80Z/C118277 listing](https://jlcpcb.com/partdetail/STMicroelectronics-STN1NK80Z/C118277). It lists Extended, SOT-223, SMT Assembly and Economic/Standard PCBA. This establishes a public catalog/assembly entry for the proposed switch only; no live quantity, reservation, quote, availability guarantee or whole-BOM assembly approval was obtained. Its electrical summary reflects older ratings, so the pinned native manufacturer rev2 remains the electrical authority. Search did not establish a JLCPCB route for all remaining exact references. This sourcing observation changes no frozen engineering input or claim of a complete assembly route.
