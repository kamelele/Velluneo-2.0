# Provisional driver envelope and lifecycle correction

VEL-DRIVER-ENV-01 r1, 2026-11-14. Specification calculation, not an approved interface or schematic. Inputs: product packet r8, blob 28db957ca16d17f6f714f694cef5baf64a188e01; lower-voltage study r1, SHA-256 85e6f0b41f39acdc266c9ac21e9f10dd2375207f00aac179e7a02eed98d45c90; owner-selected architecture A and one-colour initial JLCPCB sampling. Paths are under hardware/E27/workflow/specification-reset/ on spec/owner-interview-reset-2026-11-14. Writer /root; no CAD ownership assigned.

## Proposed investigation envelope

| Parameter | Working value / interpretation | Evidence still needed |
|---|---|---|
| Mains | Nominal 230 V / 50 Hz. 207–253 V is a proposed screening range only. | Competent product/supply assessment; disturbances and transients separate. |
| Topology | Isolated constant-current flyback in the base, simple LED panel. | Approved insulation/protection class, accessible contacts and safe service conditions. |
| Initial panel | 4000 K, seven Cree G-class devices is a proposal, not owner-selected hardware. | Exact part/bin, supplier route and representative optical/thermal data. |
| Final compatibility | Include warm eight-device candidate and neutral/cool seven-device candidates. | Verify actual counts/current against all three optical targets. |
| LED current | Start analysis at 250 mA. Explore factory development settings 240–270 mA, common to all colours once selected. | These settings are not an authorized operating range or user control. Characterize flux/current, temperature and life before selecting one value. |
| CC compliance | Provisional 18–27 V investigation window. | An analyst screening window around the approximate seven/eight-device loads, not a derived guaranteed hot/cold interval. Verify LED bins, ripple, contacts and rectifier drops before adopting it. |
| Current-error screen | ±5% is a conservative comparison assumption. | Not the accepted final accuracy or a controller guarantee. Check whether the optical budget needs tighter regulation. |
| Open/no-load/fault voltage | Unselected. | Normal CC compliance does not define these. Establish OVP, independent fault behavior, residual-energy and safe-access limits before schematic. |

## Power and optical budget

At the upper exploratory setpoint 270 mA, +5% gives 283.5 mA. The deliberately conservative rectangular screen with 27 V gives 7.6545 W at LEDs. Add the earlier illustrative 10 kohm bleeder at its -1% resistance corner: 0.07364 W. Total output load is 7.72814 W before any other secondary auxiliary loads. Adding a provisional 20% capacity reserve gives 9.27376 W. This is not the predicted nominal lamp consumption, an approved safety margin or a selected controller power rating. An IC table listing 7 W alone cannot qualify this screen.

At an assumed 80% conversion efficiency, the same screened output load would require about 9.66 W input; real efficiency, auxiliaries, startup and peak currents remain unknown. Typical current/voltage estimates from the preceding note still suggest roughly 5–6 W at the LED panel. Establish actual power/heat from the selected LED envelope rather than rating the lamp from this upper screen.

Using the same previous hot-flux/transmission assumptions, all three nominal optical targets require the current-curve multiplier to lie between approximately 4.119 and 4.490. A multiplier of 4.35 gives 824/795/792 lm. This does not establish a corresponding exact current: that requires source-curve verification and measurement, and current-to-flux response is nonlinear. Multiplying those fluxes by ±3% only illustrates a flux-scaling budget; it does not assert a ±3% current error produces exactly ±3% flux. Independent LED bins, temperature and diffuser uncertainty can exhaust the remaining margin. Do not freeze 250 mA merely because it appeared in the first calculation.

## Controller lifecycle changes the shortlist

Primary manufacturer sources checked 2026-11-14:
- https://www.power.com/products/lytswitch/lytswitch-2 and https://www.power.com/products/led-drivers/archived-products?language=en mark LYTSwitch-2 not recommended for new designs, with LYTSwitch-5 suggested. The earlier LYT2004D-first preference is withdrawn; family/reference circuits remain historical technical evidence only. NRND is not asserted to mean immediate unavailability.
- https://www.ti.com/product/TPS92310 lists ACTIVE. It is the next controller candidate to calculate, with an external MOSFET; it is not a selected or JLCPCB-stock-confirmed part. Compare the indicated replacement family as well; do not accept catalog topology tags as proof of a qualified isolated design.

Power Integrations reference DER-422 (https://www.power.com/sites/default/files/documents/der422.pdf) describes a different LYT2005E 24 V/330 mA example with valley-fill and its own input/power conditions. It is not a drop-in 18–27 V Velluneo design. No transformer/BOM, compliance, efficiency or safety result is copied from it. A reference-title label or distributor summary is insufficient to establish the required CC operating envelope.

## What must precede schematic generation

The next concrete package is the independent electrical-interface intent, current/flux/temperature data and driver calculations, plus feasible transformer/assembly sourcing and the owner's complete specification review. Unresolved safe-access/insulation, product acceptance, exact process and toolkit installation/check prerequisites still block that gate. Preliminary controller calculations can continue inside specification; no pin graph, transformer construction or PCB is approved here.

The separate supplier-feasibility-checklist.md is a prepared questionnaire, not a sent message or confirmed quote. No purchase, reservation, BOM upload or supplier contact has occurred. One ready assembled colour is enough for the first sampling route; it does not waive final compatibility evidence.

## Reproduce the arithmetic

```python
i_max = .270 * 1.05
p_led = 27 * i_max
p_bleed = 27**2 / (10000*.99)
print('max_current_A', i_max)
print('screen_output_W', p_led+p_bleed)
print('capacity_W_assuming_20pct_reserve', (p_led+p_bleed)*1.2)
print('screen_input_W_assuming_eff80', (p_led+p_bleed)/.8)
print('multiplier_lower', 750/(7*29.9*.87))
print('multiplier_upper', 850/(8*27.2*.87))
for count, hot_flux in [(8,27.2),(7,30.0),(7,29.9)]:
    print('illustrative_flux_lm', count*hot_flux*.87*4.35)
```

Verification: arithmetic executed; source lookup only. No circuit simulation, CAD/ERC/DRC, actual normal/fault electrical envelope, physical test or formal toolkit gate pass. Current note review is separate from old packet reviews. No complete specification approval is claimed.
