# SC08-B laboratory PCB thermal proposal

Read-only engineering research by /root/driver_research. Supplied source revision910870c38028a6aabff9f38baeabf7d6ae916b8b; actual model bytes are hashed in thermal-budget-results.json. No native schematic, placement, routing or board file edited/generated. Original finished-lamp requirements remain. This proposes assumptions for unpowered prototype PCB fabrication; it does not claim successful energized qualification.

## Numerical basis

calculate_budget.py actually re-executes all21 SC08-B RC/samplehold cases with passive loss instrumentation and checks that every original numerical output remains unchanged. Its results are mathematical screens, not a manufacturer silicon model, switching SPICE, CFD or measurement.

- Input RF pair:1.394..2.681W, equal nominal split0.697..1.341W each.
- R7:0.906..1.627W using average current squared plus modeled ripple, rather than confusing average current with RMS. Allocate2W normal to preserve trim/ripple margin; reassess if calibrated current or ripple exceeds the proposal.
- U1 DRAIN RMS maximum0.1092A. Applying the12.9ohm100C datasheet test resistance gives0.1538W conduction screen. Supply, switching/Coss, diode-recovery and layout losses are not thereby established. Allocate1W to U1 for initial thermal planning and verify actual SOURCE temperature.
- C5 modeled ripple RMS maximum0.1319A. This is not frequency-resolved ESR heating or proof of life/ripple qualification.
- At maximum modeled COUT113.233V: conservative auxiliary-feed total2.517W, worst individual mixed-tolerance resistor0.442W; U3 no-credit-for-load upper power0.319W.
- At145V: mixed individual feed0.761W; with one other feed shorted1.090W. Existing90C local-ambient allowance is1.147W. U3 conservative one-feed-short power0.502W;80C local ambient and85K/W yields122.67C junction budget, not achieved temperature.
- Reserve8..10W total board heat including other semiconductor, bleeder, magnetic and capacitor losses. This is a planning envelope, not measured efficiency. Do not sum mutually inconsistent corner maxima and call the result actual dissipation.

## Proposed fabrication-stage boundary

Use140x100mm rectangular FR4,2layers,1oz,1.6mm as a spacious laboratory candidate, not a lamp-base fit claim. Retain the approved assembly process unless the owner approves a change. No outline is saved by this research. Final outline, mounting holes, thermal regions and their source/return nets need independent spatial review before placement.

Assume0..40C laboratory ambient, clean dry air, initially vertical board in a guarded fixture, no enclosure or fan, at least25mm unobstructed air around both faces and20mm from nearby surfaces/fixtures. Define exact tested orientation before qualification. Mounting metal must not become an unassessed heatsink or bridge mains domains.

An intentionally coarse whole-board check: two140x100mm faces have0.028m2 area. A combined convection/radiation coefficient6..10W/m2K and8..10W yields average rise29..60K. These coefficients are engineering sensitivity inputs, not a predicted temperature distribution. This demonstrates why a140x100mm free-air experiment is plausible and a100x70mm crowded board is substantially less forgiving; it proves neither a cool capacitor nor local junction compliance.

## Thermal region constraints for spatial-intent review

1. Hot resistor zone near an outer edge; prefer its warmed air path away from C5/control. RF1/RF2 and R7 have proposed body-to-board standoff5mm, with lead forming supported by the exact component instructions. Keep roughly10mm between hot resistor bodies and20mm from their bodies to C5, PhotoMOS and reference parts. These are thermal planning distances, not certified insulation clearances. Leave access to all body centres and leads for temperature probes.
2. Six715ohmHP feed resistors form their own heat-spreading strip, not a close cluster around U3/PhotoMOS/C5. Start with about5mm body-edge spacing and own copper for each net. Do not merge their different-potential copper merely to spread heat.
3. U3 anode/tab=DC_RETURN: start with an approximately20x20mm local copper region on each side linked by a via array, subject to creepage/clearance and current-return review. A practical starting array is6..9 vias,0.3mm finished drill,0.6mm pads. The required effective theta<=85K/W remains a target. TI's52K/W package reference is not proof that this1oz pattern achieves it. Preserve quiet reference/measurement routing; do not share sense return with switching currents.
4. U1 SOURCE is a fast switching node in this high-side buck. Provide a compact local thermal island and reserve space for enlargement during review; approximately25x25mm top copper is an initial area budget. Opposite-side SOURCE copper is optional only after examining capacitive coupling, return-loop geometry, test access and EMI tradeoffs. Do not deploy a blanket two-sided SOURCE plane or call it quiet ground. The datasheet's100/80K/W D-package references use232/645mm2 of2oz copper; they cannot be transferred directly to this1oz board.
5. Cool zone: C5 and PhotoMOS away from rising hot air and resistor radiation; C5 vent unobstructed. Place C4/C10 and sense resistor close to FB/SOURCE pins with Kelvin intent, outside the hot resistor zones. Decoupling/current-loop integrity takes precedence over arbitrarily increasing copper area.

All these copper islands remain hazardous mains-referenced. SOURCE heatsinking and DC_RETURN heatsinking are different nets. Thermal area does not establish insulation, accessible-metal safety or mains creepage. A numeric domain/edge/mounting-hole/probe-access matrix remains mandatory for PCB design; the0.2mm fabrication minimum is not that matrix.

## Temperature allocations and later validation

These are proposed laboratory targets/stop conditions, not manufacturer limits unless identified. Instrument uncertainty must be included: reaching a stop condition requires de-energization/review, not continued operation to a component absolute maximum.

- RF1/RF2: local air<=85C; per-part normal power<=1.5W planning limit. TE rates2W at70C and derates toward155C; linear chart interpretation gives1.647W at85C.1.341W nominal modeled maximum leaves0.306W, but unequal tolerances/current and real HF pulses still need checking. Propose body target<=110C, stop at120C as an engineering fixture limit. Distinguish local air from hot coating temperature. The TE data includes pulse/fusing conditions; no assertion that any fault opens quickly follows from the word fusible.
- R7 AC05: source ratings P40=5W and P70=4.7W. Use local air<=70C, normal RMS power<=2W, body target<=130C and provisional stop150C. These body limits are conservative laboratory choices, not a universal datasheet surface-temperature rating. At90mA and maximum resistance the4.117W fault screen is belowP70 but may still exceed the chosen body limit; that is a reason to stop/revise, not to claim indefinite short-circuit operation.
- Feed HP2512: retain local ambient<=90C and film<=155C. At stated board mounting conditions1.5W*(155-90)/(155-70)=1.147W. Measured terminal/body temperatures and a justified thermal interpretation must establish film margin; IR surface temperature alone is not the resistive-film temperature. Propose top-surface target<=120C, stop130C pending engineering interpretation.
- U3 TL431BQPK: preserve local ambient<=80C, effective theta<=85K/W, Tj design<=125C and the0.502W one-feed-short allocation. Tab area is on DC_RETURN. Record top/tab temperatures and use a validated thermal model/appropriate metric; do not equate top-case temperature with junction. Propose top-surface target<=105C, stop110C as an early laboratory safeguard, while retaining the junction calculation/qualification requirement.
- U1 LYT0006D: manufacturer checklist requires SOURCE pin<=110C at maximum output, minimum line and hottest ambient. Choose normal SOURCE-pin target<=100C and stop105C before uncertainty reaches110C. SOURCE temperature requires an appropriately isolated measurement system; a grounded instrument must not be attached as though SOURCE were a quiet ground. Junction loss/thermal interpretation remains separate.
- PhotoMOS U4/U5: retain package<=70C as the existing experimental acceptance condition (catalog ambient range extends to85C but does not extend25C Ron/timing guarantees). Each path alone must achieve drive>=5.3mA, hotRon<=50ohm and the prescribed shutdown timing. At imposed20mA clamp current and50ohm the output dissipation is20mW, plus roughly8..12mW LED power: nearby resistor heating can dominate self-heating. No current-sharing credit.
- C5 EEUED2C151: exact official page gives16x25mm,P7.5,160V,150uF,+/-20%,-25..105C,630mA120Hz. Do not substitute the151S18x20mm variant by name similarity. Propose can target<=70C and stop80C; actual ripple waveform, frequency factors and DC leakage must be checked. Use measured ripple<=0.30Arms as an initial engineering acceptance target, not as a substitute for the supplier's frequency/temperature calculation. Voltage criteria remain normal<=123V/fault<=145V. The1.45mA leakage figure is a20C rated-voltage test, not a demonstrated hot leakage limit. No lifetime figure is calculated from a generic10C rule.
- C4/C10: keep local body<=85C for the proposed Ceff assessment, although X7R has a broader category range. Actual combined capacitance>=18uF at0..2V over the accepted temperature/aging conditions is required; bias/aging reserve factors are not guaranteed material data. Check capacitor self-heating and current-loop stability after trim.

## Fault/bring-up scope

At145V,Cmax180uF, stored energy is1.892J; zero-voltage R7 initial current0.3348A and peak power48.55W. That pulse and repeated retry heating need waveform/temperature assessment. A voltage-energy bound does not bound indefinite R7 heating. With MOSFET short or loss of regulation, fuse opening and thermal containment are not established by present normal-operation models; do not authorize unattended or indefinite energized faults.

PCB fabrication can proceed without first measuring a nonexistent board only after the human accepts this explicitly bounded design basis, its remaining risks and staged reviews. Later energized work requires a named qualified human owner, documented guarded/isolated and energy-limited setup, appropriate probe ratings, test sequence and hardware/time/temperature stop arrangements. That owner is currently unknown and is not invented here. Initial calibration/normal operation precedes hot single-actuator and fault/surge qualification; record actual conditions and do not convert plans into PASS evidence.

## Primary sources and procurement note

- TE exact product: https://www.te.com/en/product-6-2176792-5.html . TE-authored1773451ED05/25 PDF, mirrored by distributor because official document retrieval failed: https://docs.rs-online.com/0347/A700000015048280.pdf .
- Vishay HP: https://www.vishay.com/docs/20043/crcwhpe3.pdf . Film155C, specified mounting thermal conditions, correct HP grades required.
- Vishay AC05: https://wwwlegacy.vishay.com/docs/28730/ac_ac-at_ac-ni.pdf ,28730Rev05-Dec-2024. Preserve pulse shape/repetition/temperature conditions; resistance-value curves are not universal energy ratings.
- TI TL431: https://www.ti.com/lit/ds/symlink/tl431.pdf ,SLVS543S. PK52K/W is a package reference.
- Power Integrations: https://www.power.com/sites/default/files/documents/lytswitch-0_family_datasheet.pdf ,RevB06/15,thermal references and SOURCE110C checklist.
- C5 exact identity: https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUED2C151 . Linked current catalog https://industrial.panasonic.com/cdbs/www-data/pdf/RDF0000/ABA0000C1258.pdf recommends EE for new designs and contains EOL-marked rows. Exact151-row EOL association has NOT been visually confirmed here: web screenshot tool returned only text, no inspectable pixels. Verify actual legacy-part availability before assembly purchasing; do not silently change approved geometry. Known-pattern bare PCB fabrication and component procurement are distinct decisions.
- PhotoMOS: https://mediap.industry.panasonic.eu/assets/download-files/import/semi_eng_rf1a_aqy22_v_cr10.pdf .

No component source was contacted. No CAD or shared repository file was changed. Only this research folder was written.
