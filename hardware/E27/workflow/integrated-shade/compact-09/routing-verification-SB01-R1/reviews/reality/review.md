# Review report — SB01-R1-REALITY

- Task/stage: existing SC09-SB01 routing/placement/production-file verification;
  final technical candidate for bare, unpowered laboratory PCB human review.
- Role/actual actor: Reality Checker, `/root/sb01_r1_final_reality`, distinct from
  the native implementer and the baseline diagnostic actors.
- Frozen core manifest SHA256:
  `97f362117453cb296a588d0d835dfad7a4bea9931d2c35bd32300ecc238c462f`.
- PCB SHA256:
  `532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.
- Schematic SHA256:
  `16cbd188b02399d2eecd0965939a2f07cda1e96a40c45574b9d7d791a0ff22a4`.
- Toolkit snapshot:
  `f834905c883e608cee4dc5f8d8050f7689bdafa138911e3820f9d6d3b3f0c692`.
- Recommendation: **ready_for_human_review**, restricted to the existing bare,
  unpowered PCB technical candidate. This is neither an order approval nor a claim
  that powered function, spacing safety, finished-product requirements or full
  Toolkit release has passed.

## Independent inspection and coverage

I checked every one of the 262 frozen core file hashes before and after this
review. No core/source/artifact was edited. I ran my own fresh native KiCad 10.0.6
netlist export, ERC and DRC with schematic parity, all-track-errors and all
severities. Results are zero ERC violations, zero native DRC violations, zero
unconnected items and zero schematic-parity issues. Raw native ignored keys remain
visible in `fresh-DRC.json`; this is not a claim that every native rule type ran.

I independently compared actual native pad memberships and my fresh XML export to
the independent SB01 intent: 19 references, 46 physical contacts/unique pin
memberships and 11 nets agree. Actual MPN properties match the canonical BOM for
the electronic parts. U1's packaging suffix is now LYT1603D as selected in that
BOM; Value, silicon and SO8 land pattern are unchanged.

My direct normalized source-text comparison to the immutable baseline proves
exactly one U1 MPN property replacement in each native PCB/SCH file. No other
native text changed. Copper, current paths, body reservations, placements,
polarities, footprints and model bindings are therefore retained exactly. Native
`.pro` and `.dru` hashes match the baseline. I independently stripped only the two
intent/constraint digest fields from the old/new generated consumer JSONs and
confirmed all remaining numeric/region/block content is identical. This closes the
reported stale-consumer synchronization problem without relaxing any physical rule.

I inspected the current copper preview and the source-bound R5 Kelvin/T1/C6 checks.
The baseline geometry check found one intended quiet-to-force contact within the
physical R5 pad, no BP/M/Kelvin sense route under the maximum T1 body projection,
and no copper within the C6 reserved region. Exact unchanged copper makes this a
justified retained geometric scope, not a new field/EMC/temperature measurement.
The reviewed placement evidence reports 17 nonoverlapping populated-body
reservations. The 1 mm C6/T1 geometric body gap and 5 mm vent-air requirement still
require actual assembly/fixture inspection.

I examined the actual thermal and electrical planning inputs and recalculated the
simple nominal power arithmetic: 60 V x 133.438741 mA = 8.00632446 W. The stated
79.2209–87.9205% range follows mathematically from the assumed 1.1–2.1 W driver loss;
it is not evidence that the hardware achieves that loss/efficiency. T1's hot/bias
inductance, core loss and thermal resistance remain explicitly assumed, and its
conditional upper temperature exceeds the retained 90 C target. OVP's 90 V target,
hot regulation/minimum-on margin, inrush/MOV coordination and discharge arithmetic
are not qualified dynamic or safe-handling guarantees. No measurements were found
or inferred.

The new unpowered inspection plan correctly uses current T1 Wuerth 7687709152,
C1 KEMET R76, R7 HVR25 and other SB01 parts rather than the obsolete Coilcraft/TDK/
VR25 live-test text retained historically in the project. It stops before powered
activity and explicitly requires a responsible qualified human, actual guarded
fixture, instrumentation and current/time/energy limits before that later gate.

I verified the retained 3D image hashes and their original a66e97... review input
manifest. Native source/model identity justifies keeping those geometry views for
this metadata-only update. I do not treat appearance models as vendor fit data or
claim the present native renderer produced new populated images.

## Findings and retained gates

No **new** blocking or major native-CAD defect was found within this bounded
verification update. The following existing limitations remain open, not waived:

1. **R1-REALITY-EXISTING-SPACING — major; full electrical/safety gate.** The fresh
   strict comparison has the same 23 object pairs and gaps as the independently
   reproduced baseline: five intrinsic BR1/U1/D1 land pairs plus 18 associated
   escapes. The smallest intrinsic gap is 0.670002 mm, not 2 mm. A human instruction
   to retain this controller does not establish insulation coordination or a
   standards deviation. Owner: qualified electrical reviewer/product owner.
   Closure: an exact-source, application-specific qualified spacing/stress
   assessment and actual assembly/required validation evidence, or an explicitly
   authorized physical redesign. This report does not close that gate.
2. **R1-REALITY-EXISTING-POWER — major; powered prototype/product gate.** Current,
   stability/startup, hot magnetics, OVP dynamics, fault/surge/inrush, temperatures,
   capacitor lifetime and enclosure heat flow remain unmeasured. The output is
   mains referenced. Owner: qualified test investigator/product owner. Closure:
   an approved actual setup with numerical external protection/stops and recorded
   measurements at relevant corners, followed by affected design review. No live
   test is authorized by this report.
3. **R1-REALITY-EXISTING-ASSEMBLY — open; assembly gate.** R6 sample/termination fit,
   RF1/R7 lead forming/support, horizontal C6 placement/vent space, wire restraint
   and real soldered clearances require physical inspection. Owner: assembler and
   qualified reviewer. Closure: actual identified samples/assembly records and
   measured fit/clearances against current drawings. Bare-board fabrication alone
   cannot supply that evidence.
4. **R1-REALITY-EXISTING-PROCESS — blocker to full Toolkit release.** The actual
   `checks/toolkit/release.json` remains FAIL for existing requirement evidence,
   human decisions and downstream provider/process qualification. Source/artifact
   freshness repairs do not manufacture those approvals. Owner: product owner and
   the relevant qualified reviewer/provider. Closure: genuine evidence and exact
   decisions, then fresh affected Toolkit checks. No supplier order is implied.

## Invalidation and remaining evidence

The baseline purchasing-field check was invalid for U1's chosen tube suffix and is
superseded by the corrected actual-field checks. Earlier manufacturing artifact
bindings are historical and cannot be reused by name alone. This packet has fresh
source-bound exports and corrected pointers, but no source acceptance is inherited.

The unchanged copper/geometry/model scope is explicitly retained and independently
verified. Any subsequent numerical-rule, footprint, copper, component or source
change invalidates affected conclusions and requires a new freeze/review. This
recommendation covers only the exact core hash above and does not approve
manufacture, energized operation or a finished lamp.

Independent machine-readable evidence: `verification-summary.json`,
`fresh-netlist.xml`, `fresh-ERC.json`, `fresh-DRC.json` and `verify.py` in this external
review directory. These are outside their own frozen source inputs.
