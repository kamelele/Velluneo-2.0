# PCB-DRAFT-01 — native driver PCB editing has started

18 November 2026. Base7b75131667252634584552b4094c608cd88b9f2a. The owner explicitly requested starting PCB work and continued driver engineering. This packet contains a real native editable KiCad10.0.6 PCB, not another drawn packing plan. It is an **unrouted engineering workspace**, not accepted schematic/placement/routing, manufacturing release or an operating qualified supply.

## Open the actual board

Download Velluneo_driver_PCB_draft.zip, extract it, open Velluneo_specification_reset.kicad_pro and then its PCB editor. The archive includes matched schematic/PCB, local symbol/footprint libraries, proposed rules and all envelope3Dmodels; it needs no external library/model download. The repository board uses the original basename in this isolated packet; local library tables point to ../libraries. The portable archive changes only those table URIs to its included libraries folder.

There are31components/79physicalpads,22functionalnets and4individual KiCad synthetic NC nets for T1.3/7/8/9. Those singleton nets do not introduce connections to the unwound terminals. Symbol UUID association, values, MPN fields, footprint IDs and physical membership match the saved schematic. PCB netnames use the native KiCad labels/auto-names; build-result.json records the complete logical-to-native mapping. All four sides of the32x60mmoutline are native Edge.Cuts; thickness is1.6mm/two copper layers. The proposed2oz/ENIG manufacturing route remains unconfirmed; this workspace is not a verified stackup or supplier order.

The final driver-entry-02 component coordinates and sides are transferred exactly, with100mmoffset. In particular, C2 is behind U1 and no semiconductor courtyard overlaps the30x30T1allocation. Models are explicit project body/envelope allocations from retained native F.Fab bounds and installed-height proposals. The T1bluebox is a required30x30x18mm allocation, not a finished verified transformer. C1 is an explicit cylindrical mesh,10.5mmdiameter and22.5mminstalled allocation. A first native render omitted the VRML cylinder primitive; an explicit mesh corrected the display. Native renders of both sides were visually inspected after that correction. Other models are bounding prisms, not vendor STEP models.

## Isolation and functional spacing in the actual file

A real F.Cu/B.Cu rule area spans globalY83.100..93.025mm across the board. New tracks, pads, vias and pours are prohibited there. A scoped candidate clearance rule reserves10mm nominal between primary/secondary functional and NC-row nets. Actual native geometry gives10.225mm minimum projected pad-box distance; subtracting the proposed0.35mmper-domain solder/position allowance leaves9.525mm, not10mmfinished metal clearance.

The design contract uses the legitimate TI SLUP419p10 telecommunications worked example only as a planning-method reference. Its400VDC example is not a400Vrms lighting approval. Actual working RMS, repetitive peaks,106kHz assessment, air/surface/solid paths, CTI/material/process and IEC61347/60598 branch remain unresolved. No coating/mask credit, unlicensed standard, transferred certification or nonexistent insulation test is used. No slot is selected. Core/yokes are primary-hazard objects until their completed construction is assessed.

A separate proposed3mmprimary-HV-to-quiet rule deliberately exposes unfinished primary layout and inherent package spacing. It is an engineering screening rule, not a justified normative blanket limit. Its37clearance findings remain visible; there are no exceptions or exclusions added to hide them. A voltage-/object-specific assessment is required before adopting final rules. The previous all-position pad-box pass did not assess these local functional spacings.

## Actual checks

- Saved/reloaded native board:31footprints/79pads; all expected physical net sets and4NCsingletons match; all MPN/value fields, model paths and rectangle dimensions checked. Maximum pad-box difference from the prior independent proposal is about7.11e-15mm.
- Native schematic/PCB parity: **zero findings** after correcting native net aliases and matching the actual Description/MPN fields. No pin-type, NC or circuit changes were used.
- Native DRC: **exit5**,37clearance,3silk-edge,5silk-overlap and6silk-over-copper findings;53unconnecteditems. The board has zero routed tracks/vias and is not DRC-clean. Existing native default ignored checks remain listed; no new suppression was introduced.
- Fresh installed toolkit doctor and intended-graph comparison pass; native all-severity ERC reports zero findings. Actual schematic requirementsU05-U09 still exit1 and work check exits2 configuration_error. The isolated draft does not silently adopt managed configuration or change those results.
- Native SVG and ray-traced3D exports were executed on the saved board. Preview composition uses the actual native pixels, not AI imagery or fictional copper.

Full command/status records and actual native reports are in checks/. Every result has limited scope; passing parity/geometry does not establish electrical behavior or safety.

## Startup, protection and transformer design work

design-contract.json records exact retained UCC28711 source limits and executable calculations: VDD steady9–35V, start19–23V/off7.7–8.5V; static normal/backup CS screens0.34910/0.68959A;48.31mAideal current ramp during280nsblanking at the chosen high-line/Lp corner. These are not proven dynamic fault peaks. The source startup minimum is atVDD0/HV100V; no complete HV-source charging law or minimum fault-discharge current is supplied by those table points. No guaranteed retry spacing or11Wfault ceiling is invented. NTC pin3 interface thresholds are explicit; RT1-open thermal safety remains open.

The active31-position circuit and R1 regularAC05 are preserved. The previously sourced safety-fusible candidate remains unapplied: its230Vac fusing test does not qualify207–253Vac/hot-repeated-charge coordination. No NRND-reference controller or unmatched transformer is silently substituted. The read-only reference audit found materially different CV ceilings/current programming/thermal coverage, so rebuilding around them would be a real ECO, not a shortcut.

T1 retains P1→5/A2→4/S6→10 and four unwound pins. Raw1.35mmfinishedholes/2.4mmpads,5mmpitch/22.5mmrows and the source pin projection are retained. The C2 winding/material/cut-length/DCR contract remains the manufacturing proposal. Finished yoke registration, primary bridge, TIW exit/bend/termination zones and tolerances are still missing. The raw footprint courtyard is not a finishedT1courtyard. The whole30x30keepout on both copper sides suggested by an implementer was not adopted blindly: it would invalidate the present passive placement and does not establish the missing metal/leadout geometry. Actual finished construction can require a placement/footprint revision. No2mmstandoff is added.

## Stage distinction and next design work

The earlier coordinator treated supplier/physical-test/full-qualification needs too broadly as a prohibition on authoring any PCB. The actual requirements permit engineering design with explicit provisional inputs. This corrects that mistake, not the technical source limits. gate-audit.md gives the exact distinction. The current owner instruction authorizes this working draft; it is not recorded as approving the unresolved schematic stage. No approval field or unknown requirement was changed.

The next CAD work is to resolve the local HV/quiet and sensitive return/loop placement findings, then route using an approved spatial/rule contract after the genuine stage decisions. Startup/fault/NTC-open design, input coordination, finishedT1/insulation, thermal boundary, wire/lead-form/process and materials still need closure before their respective acceptance gates. No final Gerbers, fabrication, powered test or order is authorized. Native PCB editing has started; full driver qualification has not been completed.
