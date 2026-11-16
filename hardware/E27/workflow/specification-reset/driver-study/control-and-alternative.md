# Current programming, startup and integrated-switch comparison

VEL-FLYBACK-CTRL-01 r2, 2026-11-16 (r1 dated 2026-11-14). Specification investigation; product packet r11 and owner-selected architecture A remain authoritative. No schematic or component selection is approved. Read with `feasibility.md` r2 and its unchanged `results.json`.

## Engineering outcome

TPS92310 remains a comparison baseline, not a selected controller. The normal-operation calculation has now been connected to an actual current-programming equation and a DC-fed startup-resistance screen. A new constraint is that its isolated-mode hard overcurrent threshold cannot simply be relied upon to protect the exploratory transformer. A lower-threshold reference configuration exists but changes controller configuration and protection details; copying only the threshold is invalid.

LYTSwitch-5 remains a credible integrated-switch alternative. Its demonstrated isolated circuit is primary-side sensed, without a transoptor. An initial conversational reading of a small figure incorrectly described a transoptor; that statement is withdrawn. The full DER-528 circuit and operating description, not the small figure, establish this comparison. No transoptor or secondary feedback circuitry is added to the panel or base by this study.

## Current-setting calculation

TI's design equation uses R_ISNS = 0.14 * (Np/Ns) / I_output. The 0.14 V figure is a design reference, not an independently established accuracy limit. With exploratory ratio 4:1:

| Comparison resistance | Ideal total secondary current | LED current at 21 V with illustrative 10 kohm bleeder |
|---|---:|---:|
| 2.21 ohm | 253.39 mA | 251.29 mA |
| 2.24 ohm | 250.00 mA | 247.90 mA |
| 2.26 ohm | 247.79 mA | 245.69 mA |

Regulation must include auxiliary secondary loads: the output capacitor supplies the panel and bleeder, so the controlled average is not all LED current. At 18–27 V the illustrative bleeder diverts 1.8–2.7 mA. No resistor, bleeder or final common LED current is selected. The code includes resistor +/-1% sensitivity only; it does not claim total +/-1% current accuracy. Delay, sensing, transformer behavior, operating mode, ripple and actual controller/reference tolerances remain unqualified.

## Overcurrent and transformer interaction

TI lists isolated-mode hard threshold 3.2–3.6 V. With the comparison 2.21 ohm +/-1%, that corresponds to 1.434–1.645 A before delay. A linear extrapolation through the exploratory 3.6–4.4 mH and 200-turn/31 mm2 magnetic model gives 0.832–1.168 T. This is a warning index, not a physically valid prediction through saturation. It cannot be treated as adequate transformer protection. It does not prove the actual controller reaches that current: control-loop action, short-circuit low-frequency transitions and saturation dynamics were not simulated.

TI's separate SLVA511 conventional-flyback example uses a lower-threshold configuration, nominal 0.64 V, with its ZCD filtering/clamp network. It is a physically isolated transformer application even though the mode table calls that controller setting non-isolated. That manufacturer's specific use does not authorize a pin-level design here. Regulation/timing compatibility and the ZCD filtering/clamp network require verification together. Detailed native Figure 13 inspection on 2026-11-16 does not establish a separate active short-circuit detector as mandatory: the optional line-compensation network and rapid gate turn-off circuit must not be conflated with one. This narrows the earlier wording, without qualifying SCP in Velluneo.

Applying the lower comparator's 0.59–0.68 V table range to the same comparison resistor gives 0.264–0.311 A before delay. Adding the illustrative 210 ns typical propagation delay gives a worst sampled current near 0.332 A and a worst sampled linear flux near 0.233 T. These two maxima are from different corners. The delay is not a guaranteed maximum; neither result qualifies hot saturation or short-circuit survival. The lower threshold leaves much less normal-current margin than the isolated-mode threshold, so both nuisance triggering and faults must be checked. No sense resistor, MODE connection or external protection circuit is released.

## Startup trade-off, not completed startup validation

The following proposal feeds startup through a resistor from an assumed smoothed DC bus, unlike an AC-fed reference implementation. Screen: bulk 200–357.796 V; resistor +/-1%; VCC capacitor 10 uF +/-20%; startup sink 14.75 uA; upper start threshold 29 V; initially discharged VCC. The closed-form RC solution includes that constant startup sink. It excludes bridge/bus rise and controller transition behavior.

| Total startup resistance | Calculated charge to 29 V at low-bus/max-RC corner | Resistor dissipation at high bus, VCC=18.3 V | Maximum source current at VCC=10.4 V |
|---|---:|---:|---:|
| 430 kohm | 0.846 s | 0.271 W | 0.816 mA |
| 680 kohm | 1.366 s | 0.171 W | 0.516 mA |
| 1 Mohm | 2.065 s | 0.116 W | 0.351 mA |

The larger resistor reduces continuous heat while delaying initial light. A 680 kohm series total is worth further calculation, not selected hardware. The upper table-current comparison against the listed 0.9 mA non-switching operating draw is only a preliminary auto-restart screen; that datasheet test value is not verified across the full VCC waveform. Resistor voltage rating, series split, fault energy and heat at its PCB location remain undecided.

With minimum assumed capacitance 8 uF, falling from the earliest 23 V startup threshold to 15.7 V supplies 29.2/11.68/5.84 ms at hypothetical 2/5/10 mA constant draws, ignoring helpful resistor current. Actual gate charge, controller draw, initial low-frequency pulses, secondary-capacitor charge, ZCD arming and auxiliary takeover are not modeled. Thus none of these charge times is a validated switch-on time. The already identified coupled auxiliary VCC/OVP constraint remains open.

## Integrated-switch alternative: what actually changes

| Topic | TPS92310 comparison path | LYTSwitch-5 isolated comparison path |
|---|---|---|
| Main switch | External, rating/package selectable | Integrated; LYT522x uses 725 V class |
| Feedback | Primary-side sensing | DER-528 demonstrates primary-side sensing without transoptor |
| Transformer | Primary, secondary and auxiliary under investigation | Demonstrated implementation also uses a bias winding; no automatic winding-count reduction |
| Startup | External startup resistor/capacitor and auxiliary transfer need verification | Drain/BYPASS startup circuitry and bias supply need their own analysis |
| Normal switching model | Earlier ideal CrM model is only a feasibility proxy | Manufacturer specifies DCM; do not reuse CrM transformer/timing as a design |
| Panel electronics | Simple LED panel remains the intent | Same intent; integrated controller does not require a panel feedback board in the demonstrated approach |
| Assembly | Controller plus external switch, gate path and associated components | SMT SO-16B controller removes an external main-switch package; full BOM/process comparison still needed |

The manufacturer lists LYT5225D at 9 W and LYT5226D at 16 W under stated open-frame/heat-sinking conditions. These are not available power guarantees inside this lamp. The former is not automatically qualified against the earlier 9.274 W study value: that value includes an unapproved 20% capacity reserve, whereas the screened load itself was 7.728 W. Evaluate actual LED/thermal bounds first, then whether LYT5225D is sufficient or LYT5226D is justified. Do not choose the larger part solely from the catalogue wattage.

DER-528 is a different 20–40 V, 350 mA, up-to-14 W reference. Its measured current, efficiency, immunity and EMI do not transfer to Velluneo. Its primary sensing network, bias supply and clamp show that an integrated switch does not remove transformer, protection or regulation engineering. Its output-voltage fault behavior must also be recalculated for our accessible interface. Offline replacement and ordinary power cycling are permitted by the owner's requirements; any latch/restart behavior still needs a verified recovery sequence and discharge time.

## Sourcing and recommendation

Both families remain visible in current manufacturer catalogues. TI explicitly lists TPS92310 ACTIVE; no separate formal lifecycle confirmation has been obtained for the precise LYTSwitch-5 ordering suffix. A manufacturer-linked LYT5225D distributor inventory snapshot is not a stock reservation or a JLCPCB assembly confirmation. Exact LCSC/JLC codes, stock, authenticity, approved global-sourcing/consignment route and transformer assembly feasibility remain unconfirmed for either controller. Search absence is not proof of unavailability.

Next, calculate a fresh DCM/primary-sensing candidate for LYT5225D, retaining LYT5226D if justified by real power/thermal margin, and compare full BOM/startup/protection behavior with the TPS path. The LYTSwitch-5 AN-65 guide could not be fetched (HTTP 406); the accessible datasheet and DER-528 do not constitute a completed manufacturer design-tool workflow. This study does not freeze either controller or automatically carry the 4 mH transformer into a different control architecture. No purchase, supplier contact or BOM upload occurred.

## Verification and primary sources

Run `python control.py > control-results.json` beside the frozen earlier `results.json`. The script verifies its upstream SHA-256 dependency, calculates the tables and samples threshold/tolerance combinations. This is executed algebra only, not SPICE, a controller model, CAD/ERC/DRC, manufacturer tool output or laboratory testing. Independent agent reviews and exact hashes are recorded in `control-review.md`.

Sources inspected 2026-11-14:
- TI TPS92310 SNVS792: https://www.ti.com/lit/ds/symlink/tps92310.pdf — current-setting equation, thresholds, startup table and modes; equation page visually checked.
- TI SLVA511: https://www.ti.com/lit/an/slva511/slva511.pdf — current programming and lower-threshold/external-SCP reference, PDF pages 5–9 visually inspected. Not a copied schematic.
- PI LYTSwitch-5 rev C: https://www.power.com/sites/default/files/documents/lytswitch-5_family_datasheet.pdf — topology, package, power-table conditions and startup/control distinctions.
- PI DER-528 rev1: https://www.power.com/sites/default/files/documents/der528.pdf — isolated circuit (PDF page 9) and operation/bias/primary sensing (pages 10–11); circuit visually checked.
- TI product lifecycle listing: https://www.ti.com/product/TPS92310
- PI exact device catalogue: https://www.power.com/products/lytswitch/lytswitch-5/lyt5225d
- JLCPCB permitted sourcing methods, not project confirmation: https://jlcpcb.com/help/article/pcba-parts-sourcing-instruction


## 2026-11-16 source clarification (r2)

Native SLVA511 pages 8–10/14 were re-inspected at readable resolution. The lower-threshold isolated-transformer reference uses ZCD filtering/clamping; this note no longer implies that its optional compensation/gate-discharge additions constitute a mandatory separate active SCP detector. Existing numerical results are unchanged. The earlier AN-65 HTTP 406 limitation is historical: indexed guide text became accessible in VEL-FLYBACK-DCM-01. That is not a completed manufacturer-tool workflow. The new protection-study packet records the targeted review of this correction; original r1 review scope is retained where unaffected.
