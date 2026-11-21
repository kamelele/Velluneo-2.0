# T1 raw-bobbin footprint and completed position assignment

2026-11-17. This follow-up resolves the earlier footprint viewing ambiguity through source-correlated geometry. It completes candidate footprint assignment for all28 physical positions, using18 unique definitions and73 mapped terminals. It does not complete schematic-stage, finished-transformer, process, board, safety or functional acceptance.

## Actual view evidence

The exact TDK product page links an authentic STEP outline whose SHA256 is f6acdbbccb291fd39ac8028c163d7bdb47fa6849c8c7d94dce01076f05dfb2f0. Native PDFp3 explicitly identifies the pin1 corner marking. Actual BRep inspection finds one solid/430 faces, ten0.6mm-square pin-tip faces and a unique end chamfer matching that marked corner. Source-step-findings.json records the feature and pin-tip coordinates; source-step-inference.md records the exact native references and diagnostic commands. Original vendor STEP/PDF bytes are not redistributed here.

A separate read-only Reality context independently imported the STEP, reproduced the marked face/tips and checked camera handedness. Viewing from−Y toward+Y with screen-up+Z makes screen-right+X, so the front footprint coordinates are (X_STEP,−Z_STEP). Pin1 is at(−10,+11.25)mm: lower row1,2,3,4,5 and upper row10,9,8,7,6, left to right. This supports the native mounting-hole plan as the component-side realization. It is a reviewed geometric inference, not a manufacturer statement that the drawing literally saysTOP, a physical sample measurement or winding qualification.

An implementer's preliminary opposite proposal used reversed screen-down handedness. It was explicitly corrected before any shared CAD integration. The final footprint uses only the independently checked mapping above; the correction is preserved in the handoff rather than hidden.

## Actual footprint / project choices

T1 now references Velluneo_Driver:TDK_B66422W1010D001_EFD25_RAW_CANDIDATE. All ten physical pins are present, including deliberately unwound/NC3,7,8,9. Pin pitch5mm and row distance22.5mm come from native geometry. Project copper pads are2.4mm; the proposed finished plated hole1.35mm lies within the native mounting-hole1.3–1.4mm range. Actual drilling compensation, square-pin assembly tolerance and process acceptance remain open. Pin1 has a square copper pad and a local visual marker; other pads are round.

The fabrication body projection25.2×26mm and provisional courtyard25.7×26.5mm describe the RAW coilformer. They do not bound the complete core/yokes/winding/insulation/leadouts or qualify a reinforced-isolation distance. No copper route, PCB outline or actual component placement is generated. No 3D model is attached with an unverified placement transform.

## Fresh checks and retained gates

Current native KiCad10.0.6 verification covers all18 modules/28 assignments/73 terminals, including this ten-pad module and SMD/PTH sizes/layers/drills. The unchanged owner-approved graph still passes28components/73terminals/21nets/4NC. ERC reports zero enabled-check findings; the export's nonnumeric-reference warning remains open. Native SVG and updated schematic PDF export succeed.

Schematic requirements still fail U05–U09 and the full work check remains a managed-configuration/rules/ownership/realPCB failure. Every previous startup/clamp/model/input/service/thermal/safety major remains open. F1's source-visual gap, KEMET/project copper, THT leadforming, wire selection, mask/paste and assembly qualifications remain explicit. Completing pad assignment is not a working supply claim.

The preceding FOOTPRINT-02 reports reviewed the27-position candidate before this view resolution. Their source geometry scope is retained for the unchanged earlier17 modules; current post-T1 hashes and targeted final reviews are recorded here. The physical intent, circuit values, truthful symbol pin types and original three critical module bytes are unchanged. Current source includes the complete central assignments file; historical packages/reports are not relabelled current.
