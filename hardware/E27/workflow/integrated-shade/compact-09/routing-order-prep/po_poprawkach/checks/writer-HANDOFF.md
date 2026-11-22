# SC09-ROUTE05 manufacturing preparation handoff

Actual implementer: `/root/r05_spacing`. **CAD write lease is relinquished.** The coordinator may now adopt the private candidate and independently verify the integrated sources. No active customer source, `main`, supplier order or powered test was changed by this implementer.

Authoritative structured receipt: [HANDOFF.json](HANDOFF.json). Candidate project: `work/Velluneo-2.0/.work/routing05`. Base branch commit: `d011ef6a865f6dd7f06825f233b2465238ecba27`.

Final PCB SHA256: `3b9188b60e65c67e45f43cd6b55243fc1fee33aa202559efe423ba11768e97f3`.

## Actual changes

The proposed outline is 51.2 x 33.0 mm, bounded by absolute KiCad coordinates `[99.4,99.4,150.6,132.4]`. This adds 0.6 mm material at the left, right and top and 0.4 mm at the bottom. It eliminates all twelve previous 1 mm edge-screen findings without moving components. All nineteen raw footprint blocks, their pads, models, physical pin assignments, MPNs and circuit remain byte-identical. Nine vias remain fixed; the tenth moves as described below. Customer positions measured from the new board left/top must use 99.4 mm as the origin, while the engineering route-purpose map retains the original 100 mm origin for before/after comparison.

The C6 both-face protected area extends upward to the new board top at 99.4 mm. The 5 mm vent-air reservation remains measured from the actual capacitor vent face at y=100 mm, not from the newly shifted board edge. Actual support, lead forming and fixture fit remain unmeasured.

Ordinary through-via `d355cf10-6774-48cf-99c2-adaaa67f5a00` moves from `(121.2,116.2)` to `(122.6,116.2)` mm, outside the D1.2 SMD pad. Diameter/drill remain 0.75/0.30 mm. The F.Cu trunk copper path is unchanged; its two segments are merely re-split at the new via centre. A single 0.4 mm-wide horizontal B.Cu segment connects from `(121.2,116.2)` inside D1.2 to the via centre. This avoids an unnecessary short diagonal. D1.2 pad centre is `(121.2,116.0)`; starting 0.2 mm off-centre inside its large pad does not change connectivity. The via annulus is 0.175 mm beyond the adjacent pad copper boundary; the hole no longer lies in the SMD soldermask opening. No filled/capped via-in-pad process is requested.

The B.Cu `230 V` silkscreen moves upward by 0.6 mm, from `(145,126.8)` to `(145,126.2)`, resolving the previous mask-clearance shortfall. The front revision text changes R04 to R05. The common solderable window formed by overlapping R4.1/R7.1 copper is the same M net; it remains an explicitly documented manual assembly joint, not an asserted mask bridge between different potentials.

The managed copper-edge floor is strengthened from 0.5 to 1.0 mm through Toolkit preview/review/apply. All other electrical/native floors and all 55 pair targets/package assessments are unchanged. Additional explicit DFM settings are 0.15 mm silk clearance, 1.0/0.15 mm minimum text height/stroke, 0.09 mm mask-to-different-net copper clearance and native 0.10 mm minimum mask web. These stricter settings pass native DRC without exclusions or severity relaxation.

## Configuration provenance

Existing outline and C6 area geometry were deliberately migrated to match the new independent spatial proposal before configuration adoption; generated custom rules were not hand-edited. The initial preview `dfa635451503b08c345437c7787bf2c7595ed844b7909c2577f044afbb2d5efd` changed only resolved placement/routing consumers for the spatial contract and was applied by transaction `537f23ed6f4ad738669d3f8b84419edef3a7c3e6803630da2e824cf53d47267f`.

Strengthening the native edge floor used preview `b6107e2667bf44a03b0718b8b82ad821336f342f3693c2935341d1285ce908be` and transaction `38bc6a0aa73a8c1cb64ede4f51278520594b1e9f28519a54a08c58705c35311d`. The final configuration preview `fb05cc64a8f1cb234022a9d7529a02c76ce0d4a7ccdac530a70fedd531223777` has an empty diff. Actual generated consumers and custom rules were inspected; the stronger edge floor is 1.0 mm, other floors remain unchanged, and stricter nonmanaged DFM settings are preserved.

Final routing revalidation consumes digest `ff06e4dbac18c87bcd33a5044f1794c10051b680092b1126fefca1ba245716c4`. Trace authoring used the separately recorded initial spatial consumer `58746ab9f405d8ef6c5238957be090d191a90cb46632e4c17f9afd1d7a6c71e3`. The full `seed-authoring.json` records both phases truthfully and binds every actual native copper UUID/purpose to the current PCB hash. Configuration plans, diffs, preview and apply journals remain inside the private `.work` directory for the coordinator's inspection; no approval was fabricated.

## Current actual checks

- Native KiCad 10.0.6 ERC, DRC, unrouted and schematic parity: zero findings.
- All 55 bounded functional pair checks: PASS, with the same original finite package floors/margins. Strict original screen: zero edge findings and 23 package/escape spacing findings remain visible. Conservative minimum edge distance is 1.099988 mm.
- Bare JLCPCB manufacturing screen: PASS with zero findings; the remaining common M mask window is explicitly reported.
- Geometry audit: axis/45 routing only, zero acute tips, duplicate segments or collinear merge candidates; AC right / LED left remains unchanged.
- All ten via approaches are centred on their trace-fed faces; zero short parallel stairs or short via side-spurs.
- Kelvin audit: PASS with 18 native sense objects, no missing UUIDs or extra force/sense junction outside the physical R5 pad. C5/source paths and SOURCE pour policy remain unchanged.
- Native inventory: 126 trace segments, 10 through-vias, total trace length 330.731734584 mm. No new component or part number.
- Native whole-layer PDF and rendered layer PNGs were exported and visually inspected. They are native CAD plots; no synthetic copper is used.

Exactly eight copied source files change: PCB, project settings, generated custom rules, hardware.json, spatial-constraints.json and the three `.electronics-rules` configuration/consumer files. The other 130 copied files remain byte-identical. Current customer metadata, source/archive registration, fabrication files, assembly drawings, 3D renders and final human-review packet are coordinator responsibilities after adoption. Do not reuse older export hashes.

Full Toolkit release, actual qualified insulation/thermal/fault/surge/EMC behavior, physical inspection and exact human stage acceptance remain unperformed. This candidate is engineering evidence for review, not manufacturing or powered-operation approval.
