# Independent Change review — FOOTPRINT-01

2026-11-17. Actual reviewer /root/spec_change. Declared remote baseline f55cfde460fee8027adcbcd65d2211755b1f8a12. Read-only shared inspection; sole written output is this report. Repository/locked project and Change-review instructions apply.

Recommendation: **bounded three-candidate library transfer is reviewable**, without schematic/library stage, placement, process or manufacturing approval. No new actionable Change defect found within inspected scope. Existing SCH-LIB-001 is partly addressed, not closed.

## Exact inspection and checks

All36 source hashes independently match frozen-inputs.json, SHA256a3f351dd2f27b40ae531ba18f56a3d6c625698d1f3a623b64981dce71ee745f2. Inspected actual saved three.kicad_mod files, fp-lib-table, assigned schematic/generator, source manuscripts/geometry contracts, BOM, native geometry and export reports, commands/status and README/task boundaries. Viewed actual UCC native-derived footprint rendering; other module coordinate/pad semantics inspected in saved source. Did not run a second native10.0.6 footprint load/ERC/export or independently re-audit every manufacturer land drawing. Actual pinned native execution reports retain their own scope, not my execution.

Independently extracted pad numbers/coordinates/sizes from the three saved modules and compared with geometry-contract.json: exact agreement for seven U1 pads, four BR1 pads and four Q1 pads; every pad is SMD with F.Cu/F.Paste/F.Mask. U1 has HV7 at upper right, vacant row opposite VS2, correct larger HV–DRV gap, no pad8. BR1 preserves1+/2AC/3−/4AC in the documented top-view convention. Q1 preserves tab4 separately from drain lead2; it is not silently substituted with generic TabPin2. Local fp-lib-table resolves ${KIPRJMOD}/libraries/Velluneo_Driver.pretty. This checks saved candidate geometry/membership, not soldering yield or electrical insulation.

Source-backed copper dimensions are distinguished from project-selected rectangular corners, centered origins/body display, provisional courtyards and inherited/unqualified mask/paste settings. The work does not label these engineering choices as manufacturer requirements or approved assembly dimensions. Only three of28 physical components gain assignments. BOM remains28 entries, current duplicate BOMs are byte-identical, and unresolved process/other-package choices are explicit.

The approved intent file remains SHA256b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a; all seven basis-source hashes remain valid. Independently parsed the current actual native10.0.6 netlist export, SHA256ad07402f08d9d405514d7c9640e1c153693ea96a854519a3a1049bd618e6a310, through locked parse_export/compare: unchanged approved digest b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57,28 components/73 terminals/21 nets/fourNC, no discrepancy. This is my independent comparison of the actual saved export, not a second native export run.

Prior capture manifest comparison identifies precisely four changed previously frozen paths: schematic, hardware.json, capture generator and BOM. Unchanged project/symbol library/table/approved graph and historical evidence keep their old hashes. New fp-lib-table and.pretty namespace are additional paths. README correctly calls initial capture evidence/ZIP historical and points to the current footprint packet; no old report hash is relabelled a verification of the changed schematic. The workspace is a partial materialization without Git history; exhaustive remote legacy-CAD diff/no-overwrite confirmation remains a coordinator publication check, not independently claimed here. The actual inspected writer targets stay in the reset namespace.

Recorded doctor/native-footprint/export/connectivity/ERC commands succeed. Native ERC reports zero violations under its recorded defaults, without changed U1 types or added exclusion/waiver claims. Requirements exits1 and full check exits2 remain visible with unresolved U05–U09/configuration/rules/ownership/real-board gaps. Nonnumeric-reference warning remains open. No spatial/board DRC, PCB, copper, enclosure-fit, order or physical measurement is invented.

## Disposition and remaining acceptance

No new Change finding requiring correction before explicitly labelled candidate transfer. Retain SCH-ANN-001, SCH-LIB-001, SCH-IF-001, all circuit/model majors and current later-stage blockers. Physical winding construction, remaining packages, mask/paste/courtyard/process and board insulation/thermal acceptance remain due. An unchanged graph approval authorizes faithful capture; it does not approve these later land patterns or their eventual board use. Later assignment/pad/reference or source changes invalidate affected geometry/connectivity/ERC evidence and require controlled review.

## Independently verified source hashes

| File | SHA256 |
|---|---|
| hardware.json | 432bf71f6310d038bc77722c4355e1aaa772c9a0123936b1346993e4e5b3efe0 |
| fp-lib-table | 43087dad28dd81785c75c80de00a43e57a804233247bb1ab231fefd394afccb5 |
| Velluneo_specification_reset.kicad_sch | 3882e395df609ba96ab8ad3c27895e292103eef1d19bd9ffe491c0cf10826fcd |
| Velluneo_specification_reset.kicad_pro | a0f1aed1d2d10ccad132f3f162c666494c14c25cae67ec5490c3efa1f4455a7c |
| sym-lib-table | ae491b3cef7acb7c1cd3a75083670a5e1c99444e4c01e230e3757724fa1ba398 |
| libraries/Velluneo_Driver.kicad_sym | a83b3e6805eab01297799f033350774fd1ac9c280472f7bd2b564abf407caf60 |
| schematic-capture/generate_driver.py | 1ba0871b18f847d629879732b1199496232d56d08c10d555e5a9a5079679e61c |
| schematic-capture/BOM.csv | 314f2d5e55f1db5f1adc9450ff3d7f09df9c2c49fa2ac92756f246abdf913060 |
| schematic-intent/intended-connectivity.json | b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a |
| libraries/Velluneo_Driver.pretty/MB10S_Diodes_MBS_1P_2AC_3N_4AC.kicad_mod | bcb61b86077c0befe787d45ba0b056c501d47edd3b1cdd96596489004b025f4f |
| libraries/Velluneo_Driver.pretty/STN1NK80Z_SOT223_Tab4.kicad_mod | f1b8edf66033160f5165cb03e9bd5d579b107ceceda4ca7340bc40d4d0cf1306 |
| libraries/Velluneo_Driver.pretty/UCC28711DR_SOIC7_HV7.kicad_mod | bbefd0cca0948ac2e7cbb2dd72de07704e9e18e39963371ef723b69b4a102d82 |
| footprint-study/BOM.csv | 314f2d5e55f1db5f1adc9450ff3d7f09df9c2c49fa2ac92756f246abdf913060 |
| footprint-study/MB10S_Diodes_MBS_1P_2AC_3N_4AC.png | 307e5447106e22da718568503fc2ed9ed124b0a1e0ba71ad8ea6aa38b301a8d1 |
| footprint-study/README.md | cc714e42c381137b42f61270dd651e63e0df76d0962e2c28be9ec7b2f39ccbf3 |
| footprint-study/STN1NK80Z_SOT223_Tab4.png | a0601203bdedde07cbbd02cfb92bae7a9dec5df9d86d53cd8a768f34e9d9c4d2 |
| footprint-study/UCC28711DR_SOIC7_HV7.png | e9558956f50107411b7256add6776c262cb172a10a249c7430a8543b89330dcf |
| footprint-study/Velluneo_driver_3_footprints.pdf | 7fb82ff03127b4248f6946aeef985ebc314f5f8a15ae9337d45124c896b6a770 |
| footprint-study/assignments.json | 12002256a71cae27b70eb0e3cbc4982f01627eb55e16cfa2ff02fd787e067b53 |
| footprint-study/check-work.json | 1c3e3a0698b75f871fee0df09596fdbadab21b7b6fe1799175eef78d75aa45ae |
| footprint-study/command-results.json | a7aead32be0181be639d453fc91367f0e34ea49f0cf565ea90583b232eb8e4d8 |
| footprint-study/connectivity.json | 42e3d9444b957c38f10ffc7d39a4225d6cca5b75d6cbd6b4f60725bf073ac610 |
| footprint-study/doctor.json | 3004b39891f39f9e04f109d2b76424e09491471d6536f06e95a3bdd536fe7c1e |
| footprint-study/erc.json | 6e44402e1c46a7a50af15706c7b9cd6785dc70514f709058a3b99e68d8fa260c |
| footprint-study/generate_critical_footprints.py | 3d425259ca4633f75d6d9eb489011040a135b8feeea4f53ba97096b49a788ff4 |
| footprint-study/geometry-contract.json | 64aaa5af681733ac94767242f42f7430ccfd602e6ea219de1e8b540ec7613e3a |
| footprint-study/native-geometry-check.json | 6279c78ca700f7956fbb6b9dfe4d7bd12b8b5123fa8e9633a3a6f47552b09547 |
| footprint-study/native-stn-basis.md | 77f957bffa983df2b2a6c474db9845720830e0cd9a1636b993046dcb12b7bd91 |
| footprint-study/native-svg/MB10S_Diodes_MBS_1P_2AC_3N_4AC.svg | 45342df2c00cd96b821c315b70b5817374810eab97bc512f9bbd332ea89aa7f4 |
| footprint-study/native-svg/STN1NK80Z_SOT223_Tab4.svg | 5bc47d32946fcfdd8f6d77885857523cf3ed741fd6099db7533c96099a18b1a2 |
| footprint-study/native-svg/UCC28711DR_SOIC7_HV7.svg | f265edd32a025efe9681ea320ec84b0e89a6a9f3bf436173f641f191e9a7cca2 |
| footprint-study/native-ucc-mbs-basis.md | 875bd96ce642841fe56af28e181a671560b49d6f6b7989a722d003630c7897f5 |
| footprint-study/native-ucc-mbs-geometry.json | 25fab371c12bb70853cabb4595feacb09ec860b3cbe5e789ef1146fdb21c2af7 |
| footprint-study/requirements-schematic.json | 2533ce43dcf30924ed6c638778a49207a0b76d81b2e330642bb4682c946fb174 |
| footprint-study/task-contract.md | 4da3b1bba42ad689e85dbad1f2e1a52d51bc18899559590227ab119bc32efa87 |
| footprint-study/verify_native_footprints.py | 72dbfbd0ad9e8a8b37e1b0344822856c494252014ec31f4ee6e099b0158294af |
