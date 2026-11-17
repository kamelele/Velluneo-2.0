# LIB-SOURCE-03 — independent Change Review

Reviewer: `/root/lib03_change`
Baseline: `ee9a89a873ff1b9f1546ddf95f0c4764e4823e7c`
Frozen candidate: 76 files, body digest `34bc0daeb396580530cf94d2577559d26c896200ad1dc43304242fbebe4e15a9`.

Recommendation: **ready_for_human_review for this bounded library delivery only**. No introduced blocker or major defect identified. This is not schematic-stage, placement, manufacturing or electrical-operation approval.

## Actual independent checks

- Recomputed the frozen-body digest and checked all 76 member byte counts/hashes: all match.
- Inspected the actual baseline diff. The schematic changes are confined to C2/C3 footprint and library-evidence fields, plus F1 library-evidence wording. The approved graph, parts/values, electrical types, rules and prior module bytes remain unchanged.
- Exported a **fresh KiCad 10.0.6 native netlist** to separate review scratch space. Independently compared physical net-member sets against the approved intent: all **31 components, 79 terminals, 22 nets and four NCs** match.
- Replayed the current schematic generator in an isolated minimal project copy, using current parts, aliases, graph and assignments. Generated schematic, symbol library, symbol table and BOM are **byte-identical** to the candidate.
- Independently loaded the new module through pcbnew 10.0.6: pad1 at `(-2.65,0)`, pad2 at `(2.65,0)`, both `1.50 x 5.40 mm`; courtyard `7.30 x 5.90 mm`.
- Visually inspected the saved primary KEMET Table3 page12 and SCHURTER page2 renderings. The native C-arrow interpretation, copper sizes and fuse separation agree with the candidate. V1/V2 are correctly treated as courtyard dimensions.
- Verified all five locally available primary-source hashes against `source-register.json`.
- Checked all **43 ZIP member hashes** against the package inventory and confirmed **18 active definitions** across the assignments.
- Inspected retained native/ERC/requirements/work-check evidence. I did not independently rerun ERC or claim a full work-check pass.

## Change assessment

The new `--output-dir`/`--bom` arguments preserve existing defaults while allowing current outputs to remain separate from historical packages. Explicit UTF-8/LF writes reproduce the saved CAD and avoid platform-dependent text changes. The native-verifier overlay adds the new independently sourced geometry without relaxing the prior contracts.

The current **integrate -> capture -> native checks** route is reproducible. The old pre-ECO `generate_remaining_footprints.py` remains historical and is not required by this route; its earlier reference assumptions are not a new regression introduced here.

Keeping the old KEMET module and F1 provisional identifier is adequately explained. F1 copper is unchanged, and the documentation limits the newly resolved evidence to native-source bytes and drawing confirmation.

## Retained limits and invalidation

Earlier native captures/checks remain historical for their own source bytes; the current packet supplies fresh checks and exports. No PCB exists, so spatial/routing/DRC/parity inspection is unavailable and no such pass is inferred.

U05-U09, full managed configuration, and inherited electrical/model/startup/clamp/thermal/insulation/process majors remain open. DensityB selection and source-confirmed dimensions do not establish assembly capability, fuse coordination or physical safety.

## Targeted final publication addendum

Reviewer: /root/lib03_change. Final frozen body f6f5d4992aae3db2066177fa7c134aea03d8292050199b25aa4b652721206231:76files; all byte counts/hashes independently verified.

Compared against prior candidate9a6590b290949c37edf02623a7191cca48bdc9fd: full schematicSVG is replaced in frozen inventory by schematic-svg-record.json. The localSVG still exists:808730bytes/SHA256ef28e00d0da764788f1e7b5f2afdef26b4e96d8d08b41567d4e210e585cea8b2, matching the record. Other changed frozen members are README, ZIP and package-check only. All43 current ZIP members match saved source; comparing old/new archives confirms only README changed. NativeCAD, geometry, primary-source evidence, native-check reports, PDF/PNG and smallfootprintSVG remain unchanged.

Prior independent native netlist/graph comparison, isolated generator replay, pcbnew geometry inspection and source-hash findings retain documented scope. I did not rerun unchanged native checks for this packaging-only delta.

**Recommendation: ready_for_human_review for bounded publication.** No new blocker or major identified. Full schematic/later gates remain unresolved; no electrical, PCB, manufacturing or physical-safety approval.
