# SCH-PWR-ANNOTATION-01 bounded implementer result

The actual KiCad10.0.6 export experiment supports adding native power:PWR_FLAG declarations without adding physical component/pin nodes to the XML netlist. This is a synthetic fixture result, not product source or independent review. Shared product CAD/intent were read-only, and the launcher mounted device-repo read-only. All outputs are in tmp/power-annotation/.

## Actual fixture comparison

| Fixture | Physical XML components/pins | Relevant ERC error | Native netlist stdout |
|---|---:|---:|---|
| base | J1,U1 /2 | power_pin_not_driven:1 | empty |
| flag | J1,U1 /2 | power_pin_not_driven:0 | empty |
| physical-source | J1,PS1,U1 /3 | power_pin_not_driven:0 | empty |
| nonnumeric | JIN,ULOAD /2 | power_pin_not_driven:1 | annotation-errors warning |

Flag fixture adds the native library power:PWR_FLAG definition, normal #FLG01 instance, at the existing TEST_SUPPLY net. The embedded definition retains `(power)`, native power_out pin1, normal in_bom/on_board values and native descriptive intent. Only the qualified library identifier was changed when embedding the unmodified symbol definition. U1 remains power_in; J1 remains passive. Export omits #FLG01 entirely from both components and net nodes. Base and flag physical graphs are exactly equal, including net name, components, pin numbers and pin types. Their normalized physical-graphSHA256 is19c71a540118eb82c4dc86035f16dcb7998f5d3d62823aa505de64fcc7e7f1e3. Full XML byte hashes differ because schematic source metadata differ; no byte-equality claim.

The physical-source control instead adds a normal PS1 power_out pin. PS1 appears in both XML components and net nodes. Thus normal physical power_out terminals are not silently discarded by this export.

The definition was taken from host-installed KiCad9 native power library `/usr/share/kicad/symbols/power.kicad_sym`, embedded verbatim apart from qualified symbol name, and parsed/exported/checked using the genuine pinned KiCad10.0.6 runtime. This tests exact native-symbol semantics under10.0.6; it does not claim a separately installed10.0.6 symbol-library release. Source-libraryhash and fixturehashes are in inputs.json; native-flag-definition.sexpr preserves the actual symbol text.

No synthetic fullERCpass is claimed. Unsuppressed unrelated endpoint_off_grid warnings and library-configuration warnings remain: base3+2, flag4+3, physical-source4+3, nonnumeric3+2. They are recorded in realJSON output; no rules were changed. The relevant power-pin error was isolated, not concealed.

## Annotation warning diagnosis

The numeric base exports without warning. Changing only physical reference strings U1/J1 to ULOAD/JIN, with matching instance references and project path, reproduces exactly:

`Warning: schematic has annotation errors, please use the schematic editor to fix them`

XML retains those nonnumeric references. Nonnumeric reference suffixes are therefore a demonstrated sufficient cause, independent of symbol unit/common structure. This does not prove that every possible warning on product sources has only that cause. Approved product role-reference IDs must not be silently renamed. Root should record this real native warning separately from the successful physical graph comparison, and obtain a controlled reference-map decision if native numeric annotation is later required.

## Integration recommendation and limits

Use native PWR_FLAG only as an explicit ERC declaration of a real documented source path. For this candidate the coordinator can justify BULK_POS/HV from the mains/bridge/bulk path, primary return from that same source return, and VDD from the internal HV startup path followed by auxiliary rectification/storage. These statements describe connectivity/source intent, not guaranteed startup, current capability, measured supply availability or fault behavior. Preserve truthful U1 power_in types. Do not treat flags as a waiver or as validation of those physical paths.

After adding justified flags, the sole product writer must regenerate nativeXML and compare the exact approved physical graph, expecting28components/73physicalpins, then rerun actual ERC. Synthetic equality supports that mechanism but does not replace the actual product comparison.

## Reproducibility

- `make.py`: generates synthetic baseline/flag/physical-source fixtures. Nonnumeric fixture differs only reference strings/project instance name; its complete saved source is included.
- `run`: genuine bwrap Ubuntu26.10/KiCad10.0.6; rootfs and product repository read-only, evidence directory writable at/runtime. Configuration/HOME are confined to evidence.
- Actual commands for each CASE=base,flag,physical-source,nonnumeric:

```bash
tmp/power-annotation/run kicad-cli sch export netlist --format kicadxml -o /runtime/CASE.xml /runtime/CASE.kicad_sch
tmp/power-annotation/run kicad-cli sch erc --format json --severity-all -o /runtime/CASE-erc.json /runtime/CASE.kicad_sch
```

All commands returned0. Default ERC CLI exit0 is not a no-violation claim; JSON contents above are authoritative. Real source/export/ERC files and stdout logs are preserved. `summarize.py` computes graph comparison and counts in results.json. commands.json preserves actual toolstdout/stderr/returncodes; no output or warning was suppressed.
