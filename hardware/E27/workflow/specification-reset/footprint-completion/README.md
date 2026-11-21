> Subsequent T1 source correlation: the official STEP marking and native PDF were independently correlated, resolving the component-side view for a raw-bobbin candidate. See [transformer-footprint](../transformer-footprint/README.md) for the latest28-position/18-definition source and reports. The27-position task history below retains its earlier evidence scope.

# FOOTPRINT-02 — 27 assigned positions, one deliberately unresolved transformer

2026-11-17. Continued schematic/library work; no productPCB or placement is created. The current project has17 unique local footprint definitions assigned to27 of28 physical component positions. The three earlier critical modules remain byte-identical. This task adds14 definitions for24 positions and retains the exact owner-approved physical connectivity.

## What is now assigned

| Group | References | Geometry evidence |
|---|---|---|
| Vishay chip resistors | RB1,RB2,RCS,RVS1,RVS2,RG,RLC,RGS,RAUX,RBO1,RBO2 | Manufacturer REFLOW copper patterns for0603/0805/1206/2512; no WAVE-table substitution |
| NTC | RT1 | Its own native0603 pattern, not the CRCW pattern |
| ST SMA rectifiers | DAUX,DOUT | Exact native recommended dimensions |
| Diodes SMA rectifier | DCL | Its separate native suggested pattern |
| Panasonic output capacitor | COUT | Native standard-productD/D8 land pattern, not vibration-proof variant |
| TVS | TVS1 | Explicit engineered realization of native inequalities, not falsely fixed native dimensions |
| KEMET2220 capacitors | CV1,CV2 | Project candidate1.8×5.8mm pads at±2.55mm; native exact part supplies body/termination bounds but no established land prescription |
| Bulk capacitor / axial limiter | CBULK,RIN | Explicit hole/copper/lead-forming proposals; actual part tolerances and assembly remain open |
| Fuse | F1 | Provisional official-web text transcription; original drawing bytes/direct visual verification remain open |
| Internal wire terminations | J1,J2 | Project-only7.62mm pitch,3.2mm pad,1.6mm finished-hole proposal; actual wire/insulation/strain relief not selected |

Native source identities/pages/hashes and the exact source-versus-proposal boundary are in source-register.json, passive-and-bobbin-basis.md, power-part-basis.md and fuse-source-gap.md. A hashed transcription is not a hash of the inaccessible fuse PDF. Body/courtyard/mask/paste conventions remain project choices. Rectangle/circle drawings are not measured component models, assembly guarantees or high-voltage spacing rules. The fuse body representation is nominal/untoleranced, not a qualified maximum.

## T1 is unassigned for a specific reason

The native TDK coilformer and mounting-hole plans are mirrored and lack an explicit component-side viewing convention. Pin pitch5mm, row spacing22.5mm and opposite pairs are known; the correct front-copper pin1 orientation is not yet established. An official linked STEP outline was retrieved and hashed, but inspected metadata supplies no numbered pin map and its geometry has not been accepted. Two unaccepted mirrored proposals remain documented in passive-and-bobbin-basis.md. No generic transformer footprint is silently assigned.

Before T1 assignment, establish the actual component-side pin1 convention from an authentic numbered/marked model, manufacturer clarification or an actual marked bobbin, then independently review it. Copper annulus, winding insulation, complete finished-transformer envelope/leadouts and process acceptance remain separate. No manufacturer message or physical inspection occurred here.

## Actual verification

Native KiCad/pcbnew10.0.6 reads all17 modules. Exact pad number/coordinate/size/type/layer/drill comparisons pass. Symbol-to-footprint inventory covers63 terminals on27 assigned positions; T1's10 terminals remain outside footprint assignment. This is not a board-parity or DRC pass.

Fresh installed graph comparison still passes the full28-component/73-terminal/21-net/4NC approved intent, including the unassigned T1 schematic symbol. Native ERC reports zero enabled-check findings; the nonnumeric-reference export warning remains SCH-ANN-001. Native SVG exports show all17 definitions; representative PNG renders are included. No source symbol pin types, severity overrides or physical graph values were changed.

Schematic requirements remain incomplete at U05–U09; full work check remains a configuration failure with missing managed rules/ownership/realPCB. Existing RC startup/clamp/model/input/service/thermal/safety majors remain open. SCH-LIB-001 is advanced, not closed for finished source/process qualification. Source-backed copper and a clean ERC do not establish a working supply.

## Current source and package

Open the root KiCad project with its project-local symbol/footprint tables. Central footprint assignments remain ../footprint-study/assignments.json. The old critical generator now merges its own three assignments instead of erasing later additions; this generator writes only its14 new modules and24 assignments. Neither creates CAD-derived expected intent or a PCB. Historical FOOTPRINT-01/capture reports and packages remain scoped to their old Git revisions; current evidence is this folder's frozen inputs and reports.
