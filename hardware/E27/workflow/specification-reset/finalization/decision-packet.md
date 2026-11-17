# Velluneo P0: specification decisions proposed before schematic

VEL-SPEC-FINALIZE-01 r1,2026-11-17. Current product authority is requirements-and-plan.md r11. This document completes concrete engineering proposals for the remaining specification questions. **Proposed for owner review, not owner-approved.** It does not certify an electrical design or resolve later circuit/model/physical findings. Latest owner instruction includes eventual measurements; no connected hardware or instruments are available and no physical results exist.

## Scope and owner decision

Prepare one isolated constant-current driver in a covered E27 base, one initially4000K replaceable LED panel and the eventual removable milky diffuser. The complete lamp target remains750–850lm/Ra>=80. The common-base family remains2700/4000/6500K, with no user settings. No WiFi/app/wall dimmer. First demonstration by30September2027 needs one complete measured configuration; completing all three by that demonstration date is desirable; eventual three-colour common-base compatibility and family optical requirements remain required. Owner approves desired behavior/scope and stage progression, not numerical electrical certification.

Configuration evidence is explicit: P0-4000 is the first proposed build; FAMILY-3 is the eventual three-panel combination. One measured panel cannot pass all-colour matching. Future family evidence must show each complete-lamp flux and brightest/dimmest<=1.10 on the same base. Unbuilt configurations remain unverified. Existing requirement IDs and accepted intent are preserved; any later machine-contract synchronization must retain that distinction.

## U01: proposed supply and operation envelope

Normal design/test envelope207–253Vac at49–51Hz, nominal230Vac50Hz; no120V requirement. These are engineering proposals around the owner's230V50Hz use, not a claim of complete public-supply conformity. Existing bus integration covers207/230/253V at50Hz; frequency corners, hot/cold starts and disturbances must be added to implementation checks. Constructed400Vbus examples are stress diagnostics, not a normal-input rating or surge pass.

Propose turn-on within1s after a normal cold power-on, continuous emission without repeated restarting, and at least90% of the eventual stabilized flux by1s. The1s criterion concerns start/on-state behavior; the later30min protocol defines thermal/photometric stabilization. No repetitive restarting is permitted in healthy steady operation. Existing startup-charge analysis is conditional and has not demonstrated this behavior. Test all declared line/ambient corners, output initial states and repeated switching later. No DC-supply experiment can alone pass the AC-input requirement.

## U02: lifetime and prototype evidence

Retain panel15000h/L70 and base5-year design target,10-year aspiration; neither is presently demonstrated. At8–12h/day, five years means14600–21900operatinghours plus calendar aging. Assess each exact component using its manufacturer life/temperature/stress basis after actual operating temperatures are available. The BXW10000h105C endurance is not a direct5-year lamp claim; do not substitute a generic10C-doubling formula for product-specific evidence.

For one-off P0, propose100h continuous burn-in at the qualified normal test condition, with zero catastrophic failures and final stabilized flux>=95% of initial. This is a prototype workmanship/early-drift screen, not a15000h or population reliability test. Report configuration, conditions and uncertainty. Do not attach B50 or a statistical survival fraction to one sample. Family lifetime/population claims remain a later separate qualification task. Retain50full replacement/reclosure cycles minimum;100stretch, including contact and retention checks.

## U03: fabrication and assembly proposal

Propose JLCPCB2-layerFR4,1.6mm,2oz outer copper,green soldermask,lead-freeENIG for the driver. The supplier publishes corresponding generic fabrication options; this is a process proposal, not an order-specific laminate/CTI/stackup confirmation. Required thermal/insulation material properties must be specified and confirmed before placement/process acceptance. Do not assume soldermask supplies a safety-insulation barrier.

Prefer supplier-populated SMDs plus an explicitly agreed THT/custom-transformer route. AC05resistor18x7.5mm, bulk capacitor10x20mm and customEFD25 transformer materially affect fit/assembly. Full supplier assembly remains the goal; university manual completion remains the already accepted fallback. A complete matched BOM, sourcing/assembly exceptions, transformer winding/insulation construction and inspection plan are required before release. No quote, stock reservation, provider confirmation or order is invented. One available LED colour is sufficient for the first assembly route.

## U04: standards/applicability direction

The replaceable light source makes **semi-luminaire** the engineering classification lead rather than automatically treating the product as a non-dismantlable integrated lamp. This is an inference from the IEC60598-1:2024 scope and definitions as published in the official GSO adoption preview, especially definitions3.64/3.65; E27 alone does not determine classification. Resolve the exact complete-product branch before claiming conformity.

| Object or check | Proposed source family | Status and first required use |
|---|---|---|
| Complete replaceable-source construction | IEC60598-1:2024 including semi-luminaires, applicable part2 if configuration requires it | Classification/design assessment; full applicable clause access before adopting numerical construction/insulation/test limits. |
| Integrated LED controlgear | IEC61347-1:2024 and IEC61347-2-13:2024 | Native IECscope verified; component/controlgear implementation and later testing. |
| Replaceable LED module | IEC62031:2026 | Module scope already researched; do not transfer module compliance to complete lamp. |
| Lighting emissions and immunity | CISPR15:2018+AMD1:2024 with applicable interpretation; IEC61547:2020 | Exact configuration/method/limits must be bound before EMC test; no emission/immunity pass. |
| Input harmonics | IEC61000-3-2:2018+AMD1:2020+AMD2:2024 and applicable interpretation | Assess exact lighting class/power route before claiming compliance. Averaged current FFT alone is insufficient. |
| Temporal light and photobiology | Existing PstLM/SVM plan; applicable IECphotobiological method | Measurement-method/safety assessment before testing/demonstration. No photometric or photobiological pass inferred from current ripple. |

This is a source-backed applicability proposal, not a legal/CE certificate, purchased standards access or a numerical insulation table. Polish/ENadoption and harmonization must be verified for any commercial release. Full-clause access gaps are retained for the affected implementation gate; they are not filled with generic8mm/3kV values. No mandatory outside pre-design reviewer is introduced.

## U14: optical acceptance and concrete reference

Proposed distribution/appearance reference: PhilipsCoreProLEDbulbND8-60WA60E27827,12NC929002306208,806lm,matt plastic. Native SignifyPDF identifies60mmdiameter/108mmlength and an ordinary domestic light distribution. Use an actual identified sample for comparisons; catalogue values are not measurements of that sample. Reference colour is not imposed on the4000K first panel; reference use is distribution/appearance only.

Propose CCT windows2700±150K,4000±200K,6500±300K, retainingRa>=80 and whole-lamp750–850lm after the diffuser. These tolerances are engineering proposals requiring owner acceptance; exact LEDbins still need to fit them. Retain PstLM<=1.0 and SVM<=0.4 as proposed full-output temporal-light criteria from the existing plan. No dimming test is required forP0.

Photometry baseline230Vac50Hz,ambient25±1C,base-up unless a required comparison states otherwise,complete diffuser/housing fitted. Stabilize at least30min and until three readings5min apart change by<0.5%; extend stabilization if needed. Record line power, ambient,LEDboard temperature,instrument/calibration/uncertainty and matched sample IDs. Use an appropriate integrating-sphere/spectroradiometric method for flux/CCT/Ra; source-family claims need their actual variants measured.

For distribution, define0degrees through the bulb tip and180toward theE27cap. Measure matched normalized polar intensity for prototype/reference with identical geometry; propose prototype90degree intensity per lumen>=75% of the reference's corresponding value. Cap-direction emission is not required. Propose appearance pass/fail: with the fitted diffuser, individual emittingLEDpoints must not be distinguishable at0.5m viewing distance at0/45/90degrees in two perpendicular azimuth planes under100–300lx ambient illumination. Compare against the identified reference and retain matched,unsaturated photographs at identical exposure/distance. Perform direct-view assessment only after the applicable optical-safety readiness assessment. This is a testable proposal, not an inherited220–360degree requirement or a claim about the unbuilt diffuser.

## U15: thermal environment and test arrangement

Retain dry indoor/open-or-ventilated fixtures,10–40C ambient and every orientation. First reproducible arrangement: bareE27 lampholder supporting only the cap, no surrounding shade or contacting housing,still air,no forced fan; keep nearby walls/objects at least200mmaway. This is the open-fixture baseline, not qualification of every marketed ventilated fixture. Record chamber circulation and support heat conduction.

Analyze/test base-up,base-down,horizontal at10/25/40C, plus any intermediate position identified as worse. Identify thermal steady state through all critical temperatures changing<1K/hour for at least1hour, with at least3hours operation unless a justified longer settling time is needed. Record LEDboard/junction estimate,transformer,main switch,clamp,rectifiers,bulk/bias/output capacitors,contact andhousing temperatures. Compare each against source-conditioned component and material limits, then life targets. No currently assumed local85C value passes this matrix.

## U16: service, access, faults and recovery

The primary driver remains behind a separate cover when the diffuser is removed; only LEDpanel/mount is user accessible. Require insulation/access assessment of the complete assembly in normal and relevant single-fault conditions. The base can be energized without a panel, but live replacement remains excluded. Contact shrouding/keying/partial insertion must be defined before placement; soldermask alone is not an accessible-part safeguard.

Propose service-access design goals: after unscrewing, accessible conductor voltage<=5VDC, accessible stored energy<=0.5mJ and intended handled surfaces<=45C before replacement. These are conservative project goals, not adopted universal safety thresholds. Derive the instruction wait time from worst-case complete-lamp discharge and cooling measurements; no numerical wait time is currently approved. Bulk energy may continue to feed the output after unscrewing, so an isolated outputRCtime does not set the full wait time. Assess removed panel energy and bleeder-open/short faults separately.

Required functional fault outcomes: absent/open/hard-short panel must not damage the base or require a fuse/reset replacement; offline replacement followed by normal power cycling restores light. Use continuous no-load/fault thermal assessment with an initial24h endurance screen after steady state, and repeated recovery cycles. Individual LEDshort/open,wrong/partial insertion and brief contact bounce require separate cases. These are future test requirements, not authorization to energize hardware or proof that present protection meets them.

Preferred thermal behavior is automatic inhibition/retry using the existing controllerNTC function, rather than extra smart features. The proposed100k4100K sensor's approximate88C beta-law trip is not a guaranteed whole-product safe cutoff. Final trip/restart/lag and sensor-open/short behavior must protect actual parts/materials and be verified before schematic acceptance; no sensor fault is silently waived.

## Actual state and next gates

All product decisions above are either retained r11 intent or explicitly proposed refinements. U01–U04/U14–U16 remain open in the current machine contract until a genuine decision and corresponding reviewed evidence are integrated. The fresh installed requirements run returns incompleteness, not a tool failure or pass. Owner approval and independent physical-pin connectivity intent are still required before generating the product schematic underAGENTS.md. Later placement/routing/release approvals remain separate. Agent agreement does not grant them.

The exactKiCad10.0.6/pcbnew environment now executes and toolkitdoctor passes. Toolkit qualification ran128unit tests:127passed and oneWindows-specificskip; all101nativeCAD scenariospassed. Those are tool/example tests, not VelluneoERC/DRC, simulation or measurements. No productCAD or manufacturing file is created by this packet.

RC-BIAS-001/RC-COMP-002 and component/controller-model majors retain their original affected acceptance. Ordinary pre-schematic calculation work continues; no major is relabelled closed to advance. Physical measurements need actual built hardware,calibrated instruments,responsible personnel,declared limits and stop conditions. None is connected or available to the assistant now; latest owner instruction includes their eventual completion without creating fictitious results.
