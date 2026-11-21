# Independent Change review — SCH-CAPTURE-01

2026-11-17. Reviewer /root/spec_change. Sole written output: this report. Declared base0b79ac05d025fdcde1de0418874043a2d5f530b2. Read repository and locked toolkit project/Change instructions. Recommendation: **bounded draft-capture transfer is reviewable; no schematic-stage approval**. No new actionable Change defect in inspected final scope. Retain SCH-ANN-001, SCH-LIB-001, SCH-IF-001, U05–U09 and every existing electrical/model major.

## Exact scope and verification

Independently checked all24 frozen inputs; every file matches the manifest SHA256 e943699efa4298af0834ded387f172d37bce84781fb65678dbcf500f6a1400a6. Inspected actual saved native schematic, local library, project configuration, symbol table, generator, BOM, PDF/SVG scope, owner decision record and reports, rather than accepting screenshots alone. Inspected the coordinator's schematic-final image for semantic display and legibility. No generator or CAD/shared files were rewritten.

Graph canonical digest remains b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57. Restoring approval=null reproduces the exact earlier graph-file SHA2568344773bcf5a6228a099b481ef67b69e639ebd725af68ac44360831134995179. Therefore only its approval field changed. Actual record quotes owner “zatwierdzam działaj”, ties the decision to the earlier published graph/commit, and distinguishes capture authorization from approval of this later schematic. This is a faithful recorded provenance boundary, not authentication by a hash.

Independently parsed the coordinator's actual native KiCad10.0.6 XML export from .work/connectivity-netlist.xml, SHA2565fc00e3101d1dcea42aadd23ebba037f07cb71c867fa56110a83b7b65d65fe0b, using the locked parse_export/compare implementation. Comparison passes28 physical components/73 physical pins/21 nets/four explicit NCs. This is independent comparison of the real saved export, not a separately executed new native export. I did not rerun KiCad10/ERC/doctor; the host CLI is9.0.2, so it must not be represented as a10.0.6 verification. Actual recorded10.0.6 commands/results were inspected.

Source review confirms MB10S1+/2AC/3−/4AC; U1 functional HV7 with absent adjacent position; Q1 physical tab4 and drain2; explicit T1 dot and unused3/7/8/9 terminals; diode K/A and capacitor polarity; separate primary/secondary returns. Actual schematic has four NC markers and empty footprint fields. Internal J1/J2 do not purport to be the user-service dock. Local symbol table resolves a project-local original library. The physical graph is not copied from a legacy generic bridge or an unverified native-library footprint.

The three #FLG annotations declare BULK_POS, PRIMARY_GND and VDD source paths, with (power) semantics and zero-length power_out pins. Their absence from the native physical inventory was actually verified. U1 VDD/GND/HV stay power_in, VS/NTC/CS input and DRV output. No project ERC override, exclusions or waiver was inserted; project .kicad_pro contains meta only. These annotations do not establish startup/bias adequacy. The final ERC file has zero violations and includes error/warning/exclusion severities; it also visibly lists KiCad's four default ignored checks (single_global_label, four_way_junction, simulation_model_issue, footprint_filter). Thus zero findings means the checks actually enabled, not every possible ERC category or model/footprint qualification.

Inspected actual doctor/connectivity/ERC outputs and command exit statuses0. Requirements exits1 with U05–U09; full check exits2/configuration_error with missing managed rules/ownership/PCB-related configuration. Those failures and the native nonnumeric-reference warning are retained and disclosed. No severity laundering or empty-board substitute is used. SCH-ERC-001's three power-source-detection errors are addressed at the declared annotation/checking scope only; no old analog major is thereby closed.

BOM lists28 physical requirements with exact candidate MPNs/custom transformer/internal-wire requirements and explicit not-qualified footprints. This is not an order-ready JLC BOM. Library geometry/pad/insulation acceptance, current tolerance, startup, dynamics, faults, thermal behavior and physical measurements remain due.

Allowed new file paths are within the reset capture/project namespace. This workspace is a partial materialization without .git and does not contain a full legacy CAD tree, so I cannot independently attest an exhaustive old-CAD diff/no-overwrite check. The frozen paths and generator write targets do not target oldCAD or old libraries. Preserve remote baseline comparison at publication; this limitation is not a claim that legacy files were modified.

## Supplemental delivery metadata

Separately inspected derived package-manifest.json and archive. Archive SHA256e1aff901fc511eeec252e3e65358636958f4b3bc08d69d3f2dfca7f07d941175 matches metadata; independently ran ZIP CRC validation,30 members, no CRC error. I did not repeat every source-member byte comparison. Archive is accurately scoped as native draft/local symbols and selected evidence, not installed toolkit, PCB, qualified supply or manufacturing release.

## Disposition and invalidation

No new Change finding requiring a correction before clearly labelled draft transfer. This does not waive open SCH-ANN-001 numeric-reference ECO or physical-library/interface obligations. Every changed electrical pin/reference requires controlled intent/ECO and affected review; changing only labels/annotations still needs refreshed native export/ERC evidence. Later schematic-stage acceptance requires real circuit/interface/library evidence and actual owner decision. No PCB/DRC/spatial check or physical test is claimed here.

## Independently verified frozen file hashes

| File | SHA256 |
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
