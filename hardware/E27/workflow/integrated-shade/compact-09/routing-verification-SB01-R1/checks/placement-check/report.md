# SC09-SB01 baseline placement, assembly and thermal-layout diagnostic

Actor: `/root/sb01_refine_placement_check`. Scope: independent read-only baseline
inspection, not final candidate review or acceptance. Input native PCB SHA256:
`a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`.
No CAD, configuration, component or production file was written.

## Result

No new preventable component-placement collision or primary-land defect was found
in this bounded inspection. Broad relocation of components is not justified by
these results. Keep the existing 51.2 x 33 mm board, selected parts, opposite-edge
wire ports and protected C6 area. A shorter input filter feed can be evaluated by
the sole writer, with fresh clearance, topology and export checks; a reduction in
the number of strict report entries would not close intrinsic package spacing.

## Native placement and assembly geometry

Seventeen populated electronic-body reservations were transformed from their
independent source-local coordinates into actual native footprint poses. All
local pad maps matched native contacts, including the bottom-side transform.
There are no positive-area same-face intersections of those body reservations.
C1, RV1 and T1 use the current SB01 maximum dimensions rather than obsolete
historical model-info entries. R6 uses a deliberately conservative planning
reservation because the exact Royalohm termination/sample fit remains open.

The C6 maximum horizontal can and T1 maximum body have a 1.0 mm geometric gap.
RF1 to C6 is approximately 26.97 mm. The input L1 body is approximately 17.20 mm
from U1; C1 to U1 is approximately 6.9 mm. These are geometric separations, not
predictions of temperature or electrical insulation ratings. The protected C6
reserve and the additional 5 mm vent-air requirement remain in force. Native
courtyard-overlap, hole and copper-edge checks are enabled as errors in the source
project; their passing result is separate evidence, not assumed from this screen.

The minimum native trace width is 0.3 mm. Minimum annular ring is 0.225 mm, above
the project 0.2 mm floor and the cited JLCPCB two-layer absolute minimum 0.18 mm.
It is below the supplier's preferred 0.25 mm value. This is not an observed
fabrication-rule violation, and enlarging all vias merely for a preference can
reduce copper spacing; only adopt a resize if the complete route checks show a
net benefit. Supplier fabrication limits do not establish mains safety.

## Practical signal and power layout

C5 is already connected directly to the nearby BP/SOURCE terminals. Centerline
paths are 2.9196 mm from C5.1 to U1.1 and 2.9196 mm from C5.2 to U1.8. Measuring
instead to SOURCE pin5 produces 6.7296 mm because it includes travelling down the
connected SOURCE row; that does not show the bypass capacitor is remote.

The independently traced BP/SOURCE bypass and U1.3-to-R5.2 quiet sense paths do
not enter the maximum T1 body projection on either face. Power-force routing on
FB_INDUCTOR under the coil must not be misclassified as the quiet sense branch
merely because it has the same net name. Centerline/inside-pad path proxies are
recorded in `baseline-paths.json`; they are not field or inductance simulations.

The PI LYTSwitch-1 primary guidance supports keeping C5 directly across BP/SOURCE,
feedback/current-sense components close and quiet, the switching commutation loops
compact, and the input filter separated from switching nodes. This inspection
found no reason to undo those relationships. Moving C5 or spreading the quiet
network merely to make the view more symmetric would not be an improvement.

## Independent primary land spotchecks

The actual native lands for BR1, D1, U1 and T1 match the literal dimensions from
their manufacturer drawings: Diodes MBS/SMA, PI D08A and Wuerth 7687709152.
The source PDFs and their hashes, dimensions, pitch tests and results are retained
in `primary-land-spotchecks.json`. The bridge and diode pin mappings and actual
bottom-side transforms were inspected; no polarity change is proposed.

These checks also explain why their exact manufacturer lands cannot all satisfy
an undifferentiated 2 mm pad-gap screen. Do not shrink the lands, rename nets or
claim a safety exception from these dimensional checks.

## Existing assembly and qualification conditions

- RF1 and R7 upright lead forming, and C6 horizontal lead forming, remain manual
  engineering proposals requiring an actual sample, support, lead trimming and
  solder inspection. A model or courtyard does not qualify the forming process.
- R6 uses retained manual prototype lands; exact Royalohm termination overlap and
  solder-joint inspection remain open. No substitution is recommended here.
- J1 and J2 are wire solder ports, not connector bodies. Wiring strain relief,
  insulation and a guarded fixture are downstream mechanical obligations.
- The old `R7-standing-contract.json` refers to the preceding VR25 description and
  old position context. Use the current HVR25 MPN, native geometry and current
  assembly record; do not silently apply its old thermal or jig assumptions.
- The BOM package text for T1 still says 1280 although the authoritative selected
  MPN is 7687709152 and its actual 1210 geometry is used. Correct or explicitly
  label that historical text before assembly; do not change the coil or lands.
- Historical `Models/MODEL_INFO.json` and catalogue-model summaries predate SB01
  substitutions. The current bound C1/RV1/T1 WRL maximum envelopes are updated,
  so those historical summaries should not be used to infer current dimensions.

No temperature, efficiency, hot inductance, startup, surge or fault measurement
has occurred. Retain the current individual thermal stops and conditional loss
models. In particular, the proposed 0–40 C laboratory environment does not qualify
operation in a sealed bulb. Physical thermal evaluation belongs to the actual
assembled/enclosed unit. This baseline review does not approve an order or powered
test and does not close the declared intrinsic-package spacing or full Toolkit
release gates.

## Evidence and unchanged-input verification

- `baseline-placement.json`: actual native contacts, body reservations, gaps,
  trace width, annular-ring inventory and unchanged source hash.
- `baseline-paths.json`: independent bypass/quiet-force path differentiation and
  conservative magnetic-body projection screen.
- `primary-land-spotchecks.json`: four exact primary-derived land/pitch checks.
- Three small read-only checker scripts are retained beside these reports.

Primary guidance: [PI LYTSwitch-1 Rev B](https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf),
[JLCPCB manufacturing capabilities](https://jlcpcb.com/capabilities/pcb-capabilities).
Exact local manufacturer PDF hashes are in the spotcheck report.
