# First assembled sample and isolated driver shortlist

VEL-DRIVER-SCREEN-01 revision 2, 2026-11-14. Specification work only. Product packet revision 8 at commit 7bfba21467fd5daa6ade574e3cb724aa2d1b34de, path hardware/E27/workflow/specification-reset/requirements-and-plan.md, blob 28db957ca16d17f6f714f694cef5baf64a188e01. Preceding voltage study: VEL-LED-VOLT-01 r1, SHA-256 85e6f0b41f39acdc266c9ac21e9f10dd2375207f00aac179e7a02eed98d45c90. Coordinator /root owns this note; exact circuit, component selection and full specification approval remain pending.

## Owner clarification and sample strategy

One colour with a feasible JLCPCB populated-PCB route is sufficient for the first sample. Do not require simultaneous JLCPCB stocking of all three colours. Preserve the final common-base compatibility and optical targets for 2700/4000/6500 K, and test the other panels later using an available fabrication/assembly route. No colour was selected by the owner, no stock was reserved and no order was authorized.

Proposed first colour: 4000 K, because the exact G-class candidate has an observed JLCPCB listing C17218060. This is a sourcing lead, not confirmed live inventory or a manufacturable full BOM. Proposed initial characterization remains seven G-class LEDs near 250 mA, subject to the preceding curve/temperature/bin uncertainty. The base must ultimately accommodate the warm panel candidate too; designing only for the nominal 21 V neutral load would omit the current eight-LED warm concept and cold-voltage corners.

Keep separate items: (1) driver PCB, (2) LED panel PCB/substrate, (3) housing/thermal contact/retention/diffuser. A completed driver board does not establish panel thermal or mechanical feasibility. Final panel assembly and the full-lamp demonstration may use different providers; do not force all procurement into one order.

## Supplier evidence and unresolved process

Primary JLCPCB sources checked 2026-11-14:

- Exact LED listing: https://jlcpcb.com/partdetail/C17218060 . Listing and assembly offering observed previously; available inventory, flux bin and committed lead time remain unconfirmed.
- https://jlcpcb.com/help/article/pcba-parts-sourcing-instruction describes public stock, global sourcing, pre-order, consignment and new-part requests. These are possible routes, not confirmed acceptance of this BOM or guaranteed lead times.
- https://jlcpcb.com/capabilities/pcb-assembly-capabilities lists Economic/Standard PCBA process differences; https://jlcpcb.com/help/article/jlc-aluminum-substrates-are-now-available describes single-sided aluminium substrate manufacture. Neither observation alone confirms turnkey assembly of this exact LED/metal-core panel/process.

Proposed supplier path: assess Standard PCBA for the driver and evaluate a single-sided aluminium panel for thermal reasons. Neither process is approved. Confirm panel substrate plus populated assembly as one compatible service; rail/panelization, solder process, exact supplied bin and contact finish remain open. If aluminium population cannot be supplied, assess another confirmed thermal/assembly route before changing substrate; do not casually substitute FR-4 at the same power. Small final PCBs may need a larger assembly panel/carrier: supplier panel dimensions are not bulb dimensions. Component sourcing also needs to cover the transformer, safety-rated parts and THT/manual scope. One-colour sampling removes a procurement dependency, not these requirements.

## Controller comparison within architecture A

Primary manufacturer evidence checked 2026-11-14:

| Candidate | Manufacturer basis | Why investigate | What prevents selection now |
|---|---|---|---|
| Power Integrations LYTSwitch-2, LYT2004D candidate | Family datasheet Rev B 09/15: https://www.power.com/sites/default/files/documents/lytswitch-2_family_datasheet.pdf . Integrated high-voltage MOSFET, primary-side CC/CV regulation. Table gives 7 W for D package in a typical enclosed-bulb design under stated thermal conditions; short/loop-fault restart and IC thermal protection described. | Integration may reduce external parts; intended power range is near the current roughly 5–6 W LED screen. | Power table is not an output rating guaranteed in our enclosure. Verify transformer, temperature, current accuracy, output compliance, ripple/flicker, harmonics/EMC, no-load ceiling, fault energy/discharge and sourcing. IC protection is not complete lamp protection. |
| TI TPS92310 | SNVS792, February 2012: https://www.ti.com/lit/ds/symlink/tps92310.pdf . Primary-side LED-current control, isolated flyback mode, external MOSFET and current sensing; includes PFC-oriented control and protection functions. | Comparison for control/PFC behavior if the integrated option cannot meet the requirements economically. | More external switch/sensing design. Its low-voltage VCC supply range is not the AC mains range. Verify all operating/fault cases, ripple/storage tradeoff, actual BOM and sourcing. |

UPDATED lifecycle decision: withdraw LYT2004D as the preferred new-design candidate. Power Integrations now marks LYTSwitch-2 not recommended for new designs and suggests LYTSwitch-5. Retain LYTSwitch-2 only as historical/reference evidence. TPS92310 is listed ACTIVE by TI and becomes the next candidate to evaluate; also assess the manufacturer-suggested replacement family before final controller selection. This does not select a package, pin map or final part. No exact controller stock or assembly route was confirmed in this lookup; missing search confirmation is not proof of unavailability. Do not substitute a different LYTSwitch family merely because a catalog lists it.

The Power Integrations datasheet's reference circuit includes output filtering and discharge arrangements; the TI reference illustrates capacitor sizing for a particular ripple condition. Neither reference's capacitor, transformer, component values or measured performance are adopted here. The actual 50 Hz lamp ripple and flicker must meet the yet-to-be-finalized product criteria. Primary-side control can affect allowable transformer/auxiliary winding and output-load range; confirm these from pinned exact sources before implementation. Do not accept promotional typical accuracy as a guaranteed production tolerance.

## Offline replacement: passive discharge screen

Because the user permits a waiting period after unscrewing the lamp, assess a permanent bleeder resistor before adding an active output-disconnection stage. This is an engineering option, not an accepted substitute for protection. Evaluate stored charge on the base and removed panel separately, as well as mains-side accessible parts. The required safe-access voltage/energy, cooling time and failure cases still need a competent acceptance basis.

Illustration only: capacitor discharging through a resistor follows t = R C ln(Vinitial / Vtarget). Assume 30 V initially, a 5 V screening endpoint, a 10 kohm resistor with +1% tolerance and capacitors with +20% capacitance. Those voltages, capacitances, tolerances and time limits are not approved design requirements or selected parts.

| Nominal capacitance | Calculated time under the above corners |
|---:|---:|
| 100 uF | 2.17 s |
| 220 uF | 4.78 s |
| 470 uF | 10.21 s |

At 30 V and the resistor's -1% resistance corner the continuous dissipation is about 0.091 W. This is a DC arithmetic result, not a resistor wattage/package/voltage rating decision. Larger actual capacitance, higher initial voltage, an open bleeder, dielectric effects or other energy paths can invalidate the timing. No actual startup, no-load or fault ceiling is established as 30 V. A 5 V endpoint alone does not establish touch safety or discharge of mains-side storage.

A declared waiting time must cover the measured worst electrical discharge and the measured worst cooling/handling condition, with justified margin. Do not equate the roughly ten-second illustration with a user instruction or authorization to open/test a powered lamp. Removing active detection may be justified; removing all independent fault protection is not.

Reproduce:

```python
import math
for c_uF in [100, 220, 470]:
    t = c_uF*1e-6*1.2 * 10000*1.01 * math.log(30/5)
    print(c_uF, round(t, 3))
print('bleeder_W', 30**2/(10000*.99))
```

## Bounded next deliverables and gates

1. Characterization input: exact LED source documents/bins, low-voltage sample conditions and proposed neutral-panel test fixture; define hot/cold voltage, flux and thermal envelopes before fixing the driver output window.
2. Driver comparison: transformer options and supply-chain route, calculations for the chosen provisional power envelope, output ripple/storage, protection and residual energy, and a preliminary size/thermal budget. No CAD until the formal specification gate is genuinely complete.
3. Process proposal: identify an actually available first-colour part and compatible panel fabrication/population path; distinguish catalog listing from supplier confirmation. Prepare a concrete request for review if supplier contact is needed; no messages have been sent.
4. Close product-level safety/access, optics/flicker/measurement criteria, competent reviewer identity, process feasibility and formal requirements/tooling gaps. One prototype colour is not proof of three-colour matching; retain later tests and report the demonstration scope honestly.

Verification scope: source lookup and discharge arithmetic only. No trusted datasheet-byte archive, controller qualification, full BOM quote, transformer design, installed-toolkit doctor/requirements gate, KiCad generation, electrical simulation or physical test. No orders/uploads/supplier contact. Previous study reviews do not automatically cover this note; the current read-only review record is separate. No human approval of the whole specification or circuit is claimed.

## Revision 2 lifecycle correction, 2026-11-14

Manufacturer family status checked at https://www.power.com/products/lytswitch/lytswitch-2 and https://www.power.com/products/led-drivers/archived-products?language=en : LYTSwitch-2 is active but not recommended for new designs, suggested alternative LYTSwitch-5. This supersedes this note's earlier preference for LYT2004D, not the owner's architecture-A selection. TI https://www.ti.com/product/TPS92310 lists ACTIVE. No final controller is selected and no exact JLCPCB controller stock confirmed. Revision-1 reviews remain historical; affected sourcing/selection conclusions require refresh before the formal gate.
