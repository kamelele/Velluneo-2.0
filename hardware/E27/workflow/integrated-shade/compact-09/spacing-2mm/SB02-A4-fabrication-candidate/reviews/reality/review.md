# Reality Checker report - RC-SB02-A4-FINAL-20261124

- Task / stage: SC09-SB02-A4, final technical core for human review of a bare, unpowered laboratory PCB; manual assembly, 0-40 C. This review does not approve a supplier order, energization, a complete working power supply, or a finished lamp.
- Actual reviewer: /root/sb02_final_reality_review, a distinct read-only child context. No CAD, library, rule, core artifact or implementation changes were made. Only this report directory was written.
- Frozen input: outputs/SC09_SB02_2mm/core-manifest.json, SHA256 **286f47ac8239a97d379de4ce4aa3b9d92fe32f6df983ef1b0374216403fe8048**.
- Native PCB: **c75423f934b637d8b381745e72bed8440eceddb5020b956ee01f4b4426647564**. Native schematic: 02c7e026d23c30a037377a40a484a47e33ecf2aefdbe449c5470b90d25822cd4.
- Toolkit snapshot: **68b76376ff75d3e65fda4f599cb34afc154e4beb188fdfbbc3e87fa9dda95485**. Pinned toolkit revision: 86614c3b9b43713031e0ea481edbe26b71cd1b8f. KiCad 10.0.6.
- Independent intent: 6e431365a42294cd8377bb47eedbeb47a974b27a4fa3f9e00d52ca62ec122455. Gerber/drill ZIP: 16bd7eb892a2c286a1f2e2e2054b1ac71db0a54169f316328d470032ec0db897.
- Requirement coverage: SB02_SCOPE, SB02_GRAPH, SB02_ERC, SB02_PARTS, SB02_PLACEMENT and the routing, spacing, fabrication, fault and powered-qualification requirements in frozen source/requirements.json. Review uses declared intent, not the CAD as its own expected graph.

## Evidence and independent inspection

All paths in this section are relative to outputs/SC09_SB02_2mm unless explicitly prefixed otherwise.

1. I independently recalculated SHA256 for **all 234 manifest entries**: no missing files or mismatches. The supplied manifest hash matches. I did not rely on an implementer's hash assertion alone.
2. I loaded source/SC09_SB02.kicad_pcb directly with the native KiCad read API, without saving it. It has 36 footprints, 84 physical copper contacts and no zones. SHA256 before/after was identical. I independently compared all 83 unique (reference, physical pin) assignments from source/new-architecture/intended-connectivity.SB02-A.json with both the fresh native XML and native board: no missing, extra or different assignments. D1 has both K contacts, plus A; U1 has physically absent pin 3. Actual MPN fields and separate Values were inspected for the selected power/control parts; no Value-as-MPN substitution was used.
3. I read checks/native/commands.json, ERC.json and DRC.json. The fresh DRC invocation explicitly includes --schematic-parity, --all-track-errors, --severity-all and --refill-zones. ERC, DRC violations, unconnected items and schematic parity are empty. Native track_not_centered_on_via and tuning geometry checks are ignored in that report; these results are not represented as complete aesthetic routing verification. The separate source-bound routing-quality disposition covers the ten nearby via bevel flags. Native commands have a localized AppData diagnostic despite exit 0; actual fresh reports and exported artifacts exist and were hash verified, so the diagnostic is not hidden or treated as functional evidence.
4. I read checks/spacing-graph.json and its input hashes, the 190-row declared matrix, and checks/protected-bodies.json. The saved raw-copper report covers 32,905 different-net face pairs and all 190 matrix pairs with no finite exception. I independently extracted the minimum reported high-differential clearance: **2.0112 mm**, AC_FUSED to AC_N, B.Cu. The local control minimum is **0.3100 mm**, CC_REF to K_CTL, B.Cu. Reported copper-edge minimum is 1.049995 mm. These are CAD screening results, not measured factory dimensions, statutory creepage qualification, or all-fault insulation. Close manufactured dimensions must be inspected on receipt.
5. I visually inspected both full native copper raster views and both populated envelope projections. Native source coordinates independently confirm J1 at x149.15 and J2 at x102.05 on opposite board ends. Source placement is 51.2 x 39.5 mm. C5 is near U1 on the rear; the D1/T1/U1 switching region is compact. The dedicated R7 star report is source-bound and has no extra same-net force-return intersection outside its fixed terminals; its C8 return is still 18.11 mm and three vias, which does not prove loop performance. A tidy geometric route is not stability/EMC evidence.
6. I read checks/parts.json and the corrected native fields/Value comparisons, selected primary land screens, land-contracts.json, component-body/provenance metadata and the populated BOM. D1 body axes are now 6.2 x 6.6 mm, separate from its conservative 11.79 x 7.6 mm contact/body-registration display reservation. C7 maximum can and protected projection have explicit assembly conditions. The 22.4 mm figure is a planning envelope, not a guaranteed installed maximum: leads, solder and actual registration remain to be inspected. The native CLI only displayed a bare board; the populated projections are labelled engineering envelopes, not verified manufacturer CAD models.
7. I read checks/fabrication.json, the fabrication-tool review/adoption records and the release-artifact binding. The seven Gerbers, two drill files and flat ZIP are present and bound to this source. The fabrication audit reports source/artifact unchanged and compares tracks, contacts, via flashes, outline, drills and mask without increasing the 0.012 mm numeric comparison envelope. Reported separate mask-web minima are F0.75425/B0.370 mm versus a 0.1 mm target; edge minimum 1.05 mm. This is a digital export comparison, not factory process verification. HASL, thickness and copper weight remain explicit order selections.
8. I read the frozen calculations, fault scope, powered gates, fabrication profile, parts sourcing report, README and unpowered inspection plan. Paper preflight also inspected the primary LinkSwitch-TN2 p12 table and TI TL431 primary text. The 55 uA BP supply figure is a MIN table entry. TL431 initial reference tolerance uses VKA=Vref/IKA=10 mA, unlike the actual feedback circuit; the frozen calculations now explicitly exclude the resulting VKA/IKA dependencies from the initial current/OVP screen.

Evidence levels: the geometry/exports are CAD checks; numerical margins and electrical envelopes are conditional calculations; topology/package/assembly assessments are document and manual review. No circuit simulation or physical measurement was performed or inferred. I did not independently revisit every distributor offer live, qualify an assembly provider, or prove all manufacturer limits at temperature.

## Electrical reality and qualified scope

The intended load is approximately 20 series 3 V LEDs, nominal 134.5 mA and approximately 60 V LED forward voltage (~8.1 W LED power). Voltage follows the load. Input design range is 207-253 V AC/50 Hz. This is a positive nonisolated buck, entirely mains referenced; no SELV claim follows from the optocoupler or spacing matrix.

The 131.44-137.63 mA and 72.08-76.83 V values are initial 25 C screens with explicit TL431 voltage/current, drift, dynamic and thermal exclusions. They are not proved working limits. The 85 V/300 us OVP targets are not guaranteed latency/overshoot. Two references share the bias/opto/controller path and do not constitute independent safety disconnection. D2-open can invalidate the normal low-voltage control-domain envelope; a main power-switch short can put rectified mains on the output. These faults are preserved explicitly, not closed by the 190-pair screen.

Independent arithmetic spot checks agree with the paper scale: 253*sqrt(2)=357.796 V; 0.5*12 uF*Vpk^2=0.768108 J; the 47 ohm/-5% ideal initial current is 8.013 A. Continuous RF1 wattage does not qualify that pulse. At 85 V, R17/-1% carries 8.586 mA and dissipates 0.730 W; its conclusion is conditional on functioning OVP, not main-switch short. C6 maximum stored energy at 85 V is 0.29478 J. R20 worst normal paper power is about 0.129 W with its voltage-against-ambient distinction and protected body region documented.

No measured temperatures or efficiency exist. U1/T1/C6/C7/D1/R10/R17 temperatures are stop criteria, not estimates. The legacy copper heating screen does not establish complete-board temperature. Bare fabrication is useful to enable a separately qualified experimental activity; it does not close the RF1 pulse, hot magnetics, stability, startup, OVP, surge or fault tests.

## Findings and closure status

### RC-SB02-01 - formal release approvals remain absent

- Severity/gate: blocking for formal release/order acceptance; not a newly discovered geometry defect and not a blocker to presenting this candidate for human review.
- Exact object: frozen checks/toolkit/full-release.json and summary.json, snapshot 68b76376ff75d3e65fda4f599cb34afc154e4beb188fdfbbc3e87fa9dda95485.
- Rule: pinned AGENTS stages and verification/release; actual human acceptance must cover exact intent, spatial contract, stages and artifacts. Generic local PCBA/provider confirmation is also missing in the configured process.
- Evidence/consequence: Toolkit release actually FAILS for missing/stale intent/spatial/stage/artifact acceptance and provider confirmation. Neither root's technical PASS nor this review can be reported as full release approval.
- Owner/closure: coordinator and authorized human; obtain genuine snapshot-bound decisions, resolve the configured provider scope truthfully, then rerun affected Toolkit release. Do not invent approvals or relax rules.
- Status: OPEN, explicit and accurately disclosed in the packet.

### RC-SB02-02 - powered performance and faults remain unqualified

- Severity/gate: major for powered testing or operating/product acceptance; outside the requested unpowered bare-board candidate boundary.
- Exact objects: frozen calculations.SB02-A4.json, fault-scope.SB02-A4.json and prototype-powered-gates.json, bound through the core manifest above.
- Evidence/consequence: no guaranteed RF1 startup pulse qualification, measured hot current/inductance, loop stability, OVP transient, temperatures or fault limits. Near LED short, VOUT-fed bias can collapse, so nominal CC is not established. Input C7 can replenish C6 after removal of AC.
- Owner/closure: qualified responsible test operator, not yet assigned. Define guarded setup, protection/instrument ratings, test-specific current/time/energy limits and measured pass/stop evidence before the relevant test. No mains or fault test is authorized by this report.
- Status: OPEN as future qualification, not mislabeled as a closed electrical check.

### RC-SB02-03 - native populated render/installed fit unavailable

- Severity/gate: informational for bare fabrication; mechanical/powered integration remains unqualified.
- Exact objects: frozen checks/native-bare-render.json, views/*envelopes*.png, source/land-contracts.json and assembly inspection plan.
- Evidence/consequence: native CLI omitted component bodies. Conservative source-derived envelopes communicate the design without proving exact D1 body registration, lead trim/solder height or enclosure fit.
- Owner/closure: assembly/integration owner; inspect actual parts and assembly dimensions. A qualified native/vendor render may replace the current presentation only with updated provenance.
- Status: accurately disclosed; no required CAD fix for the bare-board decision.

Paper preflight findings closed in this frozen packet: explicit TL431 VKA/IKA exclusions, isolated-C6/no-replenishment discharge condition, LED-short bias-collapse condition, repeated placement sentence cleanup, and D1 body-axis versus display-reservation distinction. I verified the integrated content, not merely the author's response. Historical Value-as-MPN and non-parity DRC reports are excluded; corrected actual-field/Value checks and native schematic-parity invocation are the relevant evidence.

## Recommendation

**ready_for_human_review**, strictly for the frozen **bare, unpowered, manually assembled laboratory PCB fabrication candidate**. No new blocker/major CAD or export defect was found within that boundary. All 234 core entries matched, intent/XML/native connectivity agreed, and the current source-bound numerical checks plus manual inspection support the candidate's technical presentation.

This is not ready-for-order authorization or a full Toolkit release PASS. RC-SB02-01 must remain visible; RC-SB02-02 prevents importing a functioning/safe power-supply claim into the bare-board decision. The exact-source human review is the next acceptance step. This report neither submits an order nor approves energization.

## Re-review / invalidation

Earlier SC09/LYT1603D, ROUT05, SB01, final-source-v1/export-v1 and pre-parity-correction reports do not transfer to this packet. This report supersedes my paper preflight only for the exact frozen core above. Any source, intent, matrix, component, geometry, rule, manufacturing artifact or claim change requires affected re-review; a matching old report name is insufficient. A new core manifest requires an explicit retained-scope explanation or renewed review.
