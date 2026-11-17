# SCH-CAPTURE-01 — Independent Reality Checker review

- Actor: `/root/spec_reality`, distinct from root CAD writer and support/model implementers.
- Date: 2026-11-17. Candidate manifest SHA-256: `e943699efa4298af0834ded387f172d37bce84781fb65678dbcf500f6a1400a6`.
- Recommendation: `ready_for_human_review` for bounded native schematic-capture transfer only. This is not schematic-stage acceptance, working-circuit qualification, placement authorization or release approval.
- Approved physical intent digest retained: `b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57`.

## Actual evidence and coverage

Read device-repo/AGENTS.md and the locked 05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822 project/Reality instructions. Inspected all 24 frozen input identities, native saved schematic and local symbol definitions, generator, exact approved graph and decision record, BOM/hardware inventory, reports, source-declaration rationale and annotation experiments. Graph approval is recorded for capture, not retroactively assigned to the generated schematic.

All 24 hashes match. Independently parsed the actual saved schematic/local library: 28 physical instances plus exactly three nonphysical annotations; all 28 MPN fields match approved parts; all physical footprint fields remain empty. All 13 embedded symbol definitions match the local library after qualification of their symbol names. U1 supply pins1/4/7 remain power_in; pins2/3/5 input; pin6 output. Passive energy-transfer parts were not retagged as power outputs.

Inspected the actual native XML export at SHA-256 `5fc00e3101d1dcea42aadd23ebba037f07cb71c867fa56110a83b7b65d65fe0b`, matching the stored report. An independent XML comparison ignoring net names confirms all 21 physical net-member sets against approved intent, 28 component references, 73 terminals and four correctly marked T1 no-connects. No #FLG annotation appears as a physical XML component. No primary/isolated-return merge found. This is a comparison of actual source/export, not a fresh reviewer KiCad execution.

Visually inspected the provided final rendered sheet and inspected native source/export/PDF metadata plus the frozen SVG/PDF identities. The one-sheet native drawing is readable as a draft connection document; it is not placement geometry. Source/diagram checks preserve MB10S1+/3− and AC2/4, UCC functional HV7 with the vacant position, Q1 G1/D2/S3/D4 tab, DCL anode toward drain, TVS cathode toward clamp/anode toward bulk positive, polarized capacitor rails, raw-aux sensing before DAUX/RAUX, Kelvin sensing intent and gate pull to SENSE. T1 dot1/2/6 and endpoints5/4/10 preserve off-time auxiliary/secondary rectification. Existing native pin/polarity review remains applicable; no new footprint/pad qualification is implied.

The final ERC report contains zero sheet violations at included error/warning/exclusion severities. Its four native ignored-check categories (single_global_label, four_way_junction, simulation_model_issue, footprint_filter) remain visible; no project suppression/severity change was found in the minimal project file. This is not a claim that every possible ERC category or unassigned footprint has been validated. The real annotation warning remains recorded in native export output.

## Findings and closure scope

- **SCH-ERC-001: verified closed for the initial ERC source-declaration deficiency only.** Three explicit actual-path declarations are justified: bulk from mains/bridge/storage, primary ground from that same supply return, and VDD from internal HV startup followed by auxiliary rectification/storage. Their original source paths exist in the graph. Actual physical membership is unchanged and truthful U1 types remain. A declaration establishes none of the available current, startup timing, thermal or fault behavior; RC-BIAS-001 is not closed.
- **SCH-ANN-001: open, minor/native annotation and later schematic acceptance.** Approved role references remain nonnumeric; the actual exporter warns. The synthetic reference-only control supports that diagnosis but cannot erase the product warning. Closure is a controlled reference-map/intent decision and refreshed actual native exports/checks, not silent reference renaming.
- **SCH-LIB-001 / SCH-IF-001: retained open at their affected acceptance.** No physical footprints, transformer construction/insulation, final panel/electrical interface or dock qualification is supplied. Capture-transfer acceptance cannot close them.
- **Existing electrical/model/input/clamp/service/thermal majors: retained open unchanged.** No new calculation, controller/component simulation, physical measurement, sourcing, insulation or compliance result is claimed. The custom winding phase intent is not proof of a manufactured transformer.

No new blocking transfer defect was identified in this frozen draft. U05–U09 remain actual schematic-requirements errors. The full work check still fails on those and managed-configuration/PCB prerequisites; no PCB, DRC or rule/profile adoption is invented. These reported failures block formal stage acceptance, not delivery of the explicitly incomplete connection draft.

## Verification limits and next acceptance

I did not run the generator, a new KiCad export/ERC, the synthetic experiment or the full installed tool suite, and did not write shared source/check directories. Existing native report identities, actual XML and saved source were inspected independently. PWR semantics and graph agreement do not establish analog operation, Kelvin geometry, switching loops, insulation or source adequacy. Only the owner or authorized human can accept this generated schematic stage after its true prerequisites are complete; prior graph approval grants capture authority only.

## Exact frozen input identities

| File relative to specification-reset | SHA-256 |
|---|---|
| Velluneo_specification_reset.kicad_sch | a1dd64aa6832a0c587adbc5f50ebc7dd0623b6924fa116a34ad8402224b278b3 |
| Velluneo_specification_reset.kicad_pro | a0f1aed1d2d10ccad132f3f162c666494c14c25cae67ec5490c3efa1f4455a7c |
| sym-lib-table | ae491b3cef7acb7c1cd3a75083670a5e1c99444e4c01e230e3757724fa1ba398 |
| libraries/Velluneo_Driver.kicad_sym | a83b3e6805eab01297799f033350774fd1ac9c280472f7bd2b564abf407caf60 |
| hardware.json | e8ad62ae163f335b79997a57c1b77948b491c7405360376f65fd5bf5b48f9207 |
| schematic-intent/intended-connectivity.json | b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a |
| schematic-capture/generate_driver.py | 1c0b68676a379edbe88b0b154a475abfa48ff5b672cd46f984a2c91c2cff7f92 |
| schematic-capture/README.md | c45fca95954ca8b78c2451a46a0ba406a54e40feeb38ad69f4085ed5faedc0c3 |
| schematic-capture/BOM.csv | 49565369d943088cbf392750bfdb32efe06559bdb8939c5ab1427b2199854fc2 |
| schematic-capture/Velluneo_driver.pdf | 086cc651e3ef5ee5318f1737801f8345ebc7b9838ab0c3a04513630bbebd26c7 |
| schematic-capture/svg/Velluneo_specification_reset.svg | c4e553e59e9d76305da6feabc9881ff3dc88116769dbc381954f54977b2b0689 |
| schematic-capture/owner-intent-approval.md | 7447a600c61f531ba54de6ec6ebf249a1f64d7c32980187c0adbeb946d3b6f16 |
| schematic-capture/task-contract.md | 9f00bd743405d7656540b3c93f043dcc7ecc2f3462c4f8e30331c662f9f23372 |
| schematic-capture/power-source-declarations.md | 5136724ee8ea91986da460fba46373a532fbac530198d834c52dd9ffab8dfddc |
| schematic-capture/finding-ledger.md | 2220d2e296f55a6d410ad1ba4ac23800fde948f625806864081f24e51577b9a9 |
| schematic-capture/support-pin-type-audit.md | c36143507e3dff18367b0dd9817b77479c9417a66bc1b6a0c33754a4742ea6ea |
| schematic-capture/power-annotation-experiment.md | 1a7ed5fcfe18819cc769052c0c08881c54dd5175b02173afbb9a2e1c67fcab22 |
| schematic-capture/power-annotation-experiment.json | 5aeb013cef31337e9cf21d3aee4086d572a023fa7c997a94e55e9cd584410eab |
| schematic-capture/doctor.json | 3004b39891f39f9e04f109d2b76424e09491471d6536f06e95a3bdd536fe7c1e |
| schematic-capture/connectivity.json | 8b74b9132874325463a404b7741d7423d29275c67eedb2a1e4df89fb213a4489 |
| schematic-capture/erc.json | 521986d92e1d7882cd143b89d95eecdb15d6351fe7bfd047f19088e5ec413d67 |
| schematic-capture/requirements-schematic.json | 2533ce43dcf30924ed6c638778a49207a0b76d81b2e330642bb4682c946fb174 |
| schematic-capture/check-work.json | 81328489ff31f04f1d3903a58ff6e74db9848e6eb32dfae7098455a33c594628 |
| schematic-capture/command-results.json | ecaebe4e91ec6959b51c42439b5f2eea752f75f361f024535b2496eaab5aa028 |

Only tmp/sch-review-reality.md was written. No CAD, library, expected graph, report, rule, approval or physical hardware was changed.
