# Protection proposal review and open selection blocker

VEL-PROTECTION-01 r1, 2026-11-16. Preliminary diagnostic publication only. **Circuit selection/freeze remains blocked by unresolved major finding RC-PROT-001.** This is not a formal specification approval packet, protection qualification, human engineering sign-off or authorization for CAD/manufacturing/testing.

## Frozen evidence

| File | SHA-256 |
|---|---|
| calculate.py | 7f2ca22f695b4b5869f73c8a41d9ccac9bbd6c071208065cceb3a87ef2501655 |
| results.json | ccb5560b3ee2895c0e9c9347e39954205e048a9059729d9139923ea96484d0f7 |
| findings.md | 960bb26f63448799a35e2312dcca4f48b3ce625f93c6e6eae94b883cf7e0a717 |
| fault-contract.md | 7243935742a549c0908f89c4bc0db2f5d9954f3e46a17adc31bde584993b27a4 |
| sources.json | 1320a992d4f8e9ae0ef557052f6cdaef5df95043f9af282a38ccd429a2c91739 |
| Updated driver-study/control-and-alternative.md r2 | a70e4794a0bdda0a194efeabdc0a79d0e03667e4f32bf03f7723625ad4f14db1 |
| Updated driver-study/README.md | ba70087687a29d7acefa463e95bef9e2ee5ead246320edff3ef1ded6839f92f8 |

All four actual independent read-only contexts inspected the same six-file technical input. The index was a separate targeted Change review. Native TI PDFs are reference-only and are not redistributed; their hashes and sizes are recorded in sources.json. Product packet r11 Git blob 6493b29bd33fbde1f3c61c5e995b11447cb83e9b was confirmed unchanged through GitHub before this work.

## Actual reviewer coverage

| Role / context | Actual evidence checked | Outcome / remaining findings |
|---|---|---|
| Reality Checker /root/spec_reality | Full script execution reproduced results.json exactly, including the verified-dependency 474 kohm bus overlay. Native hashes/sizes and readable SLVA511 Figures 7/13 checked; interpretation of ZCD filtering versus optional compensation/gate discharge independently supported. | Preliminary diagnostic discussion only; circuit freeze blocked. RC-PROT-001 major; RC-PROT-002 actual control/fault stress; RC-PROT-003 service/thermal acceptance. |
| Overengineering Reviewer /root/spec_simplicity | Six hashes and read-only diagnostic/contract/code/source review. No duplicate full solver run; numerical/physical verification assigned separately. | No new unnecessary-complexity blocker. Before accepting a precision guard compare verified winding/OVP/supply changes for lower total burden. OE-LED-01 complete common-requirements implementation comparison remains open. |
| Completeness Reviewer /root/spec_completeness | Six hashes, native source integrity, stored-result summaries, 96 normal cases and 54 refreshed input cases reconciled; packet r11 fault/access/thermal coverage checked. No full solver rerun or independent PDF interpretation. | No completeness finding within preliminary scope; explicitly not circuit freeze or formal approval. |
| Change Reviewer /root/spec_change | Six hashes, native source integrity, packet r11 preservation and targeted old-control-note correction checked against native SLVA511 text. No duplicate full solver run. Separate index links/scope/major-blocker status checked. | No new Change finding. No 40 V limit, service/startup delay, hardware selection or stage approval inferred. |

## Open findings and acceptance stop

| Finding | Severity / scope | Required closure evidence |
|---|---|---|
| RC-PROT-001 | **Major: controller/circuit selection** | Resolve coupled VCC guard/auxiliary/bootstrap design. Integrate actual consumption, control timing, guard loading/current limiting, capacitor stability, temperature and startup speed. Existing 0.56 V lower / 0.85 V upper illustrative VCC margins and 3.31 ms bootstrap margin are insufficiently qualified. Independent affected review is required before freeze. |
| RC-PROT-002 | Note: fault protection | Actual reset, blanking, turn-off, retry and OVP stop behavior. The four-pulse assumption and linear current/flux/energy proxies are not hard bounds. |
| RC-PROT-003 | Note: service/thermal | Persistent-fault heat, output-capacitor short discharge, continued conversion after unplugging, discharge faults and whole-lamp thermal recovery. |
| OE-LED-01 | Existing open architecture/interface comparison | Actual regulation, optical/storage/thermal, protection, assembly and source burden under common requirements. |

Publication preserves the diagnostic work and its explicit stop condition; it does not accept the blocked candidate. No majority vote or author receipt closes these findings. No human approval is simulated.

## Targeted historical correction and dependencies

The old control note is updated from r1 to r2 solely to narrow the implication of a mandatory independent active SCP detector and date the clarification. Native source inspection supports lower-threshold operation with ZCD filtering/clamping; optional compensation/gate-discharge additions are not recast as a mandatory active short detector. The earlier numerical script/results are unchanged, and their original r1 reviews retain only unaffected scope. This record supplies the actual targeted r2 review.

Rstart changed from 680 kohm in the older buffer study to 474 kohm in the diagnostic set. The new script checks SHA-256 432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea for the sibling primary-buffer script, imports it without altering its file, and refreshes the relevant 54 cases. The overlay was not falsely attributed a new half-step sweep. No historical record is overwritten as a pass for the changed input.

The ATL431 static interval is a feasibility screen, not an implemented stable current-limited guard. Original datasheet electrical-condition coverage, live sourcing, complete safety classification, controller/SPICE dynamics and physical operation were not independently qualified in this review.

No CAD, ERC/DRC, installed-toolkit check, supplier communication, order, reservation, BOM upload or physical test occurred. Next authorized analytical work must address RC-PROT-001 before a complete controller/protection proposal is frozen.
