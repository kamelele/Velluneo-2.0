# Lower-voltage panel comparison and sourcing screen

VEL-LED-VOLT-01 revision 1, 2026-11-14. Preliminary specification calculation; no final electrical interface selected. Input: VEL-LED-SCREEN-01 revision 2 and architecture A, saved at repository commit 344d66a34a4a4eeb4628ab9ca53ec7494f823723 under hardware/E27/workflow/specification-reset/. This adds a candidate; it does not supersede the previous numerical study or human product decisions. Writer: /root. No CAD, library, old rule or approval changes.

## Finding

Lowering output voltage need not require parallel strings. An LED family operated at higher per-package current may produce the required light with fewer devices in a single string. This potentially preserves a simple panel at the expense of greater local heating and stronger dependence on current/temperature characterization.

## Manufacturer basis

Cree CLJ-DS40 Rev 10B, pages 4–8, checked 2026-11-14: https://downloads.cree-led.com/files/ds/j/JSeries-2835-3V-Consolidated.pdf . Candidate codes:

- JB2835BWT-G-H27GA0000-N0000001 (warm).
- JB2835BWT-G-H40GA0000-N0000001 (neutral).
- JB2835BWT-G-H65GA0000-N0000001 (cool).

At 55 mA, the reference 85°C typical fluxes are 27.2/30.0/29.9 lm. Page 6 curves were visually inspected: an approximate 250 mA relative-flux multiplier of 4.2 and a typical forward voltage near 3 V are used only for screening. Sweep multiplier 4.0–4.4; this is an analyst uncertainty assumption, not a manufacturer limit. The published 480 mA maximum is thermally conditional and does not establish suitable lifetime at 250 mA. Do not use the 0.2 W class label as a hard current limit or as permission to dissipate arbitrary power. Page 4 operating limits and the eventual thermal design govern. Exact source bytes/curve digitization/lifetime evidence remain unpinned for formal acceptance.

Applying a 25°C current curve to the 85°C reference flux assumes separable current/temperature effects; this is unverified. The diffuser transmission 0.87 is also unmeasured. Current ripple, bin maxima, aging and actual hot/cold voltage spread remain open.

## Calculation comparison

| Candidate | Warm / neutral / cool LED counts | Base current | Illustrative normal panel voltage | Nominal calculated flux after diffuser |
|---|---|---|---|---|
| N-class single string, previous study | 14 / 13 / 13 | 150 mA | 40.0 / 37.2 / 37.2 V at 25°C typical test voltage | 777 / 797 / 787 lm |
| G-class single string, new screen | 8 / 7 / 7 | 250 mA | about 24 / 21 / 21 V, rough graph-based typical screen only | 795 / 767 / 765 lm |
| N-class two parallel 7-LED strings | 14 / 14 / 14 | 300 mA total, assuming 150 mA per branch | about 20 V before ballast, at 25°C typical test voltage | 777 / 859 / 848 lm; nominal criteria fail |

All three can use an isolated current-regulated base in architecture A; their required currents differ and are not interchangeable without redesign. Common base means one selected design shared by its three colour panels, not one universal base accepting every row above. The new G screen has a brightness ratio about 1.040 and nominally meets the optical limits. It is weaker evidence than a measurement and not as direct as the N-class test-current data. Numerical output voltage is not an approved safety limit, compliance guarantee or open-load ceiling.

For G, panel electrical power is about 6.0 W warm and 5.25 W neutral/cool if 3 V per device is assumed. Each device carries roughly 0.75 W in this approximation, compared with roughly 0.43 W for the N-class screen. Fewer LEDs do not remove the heat; the panel/radiator/contact path must still handle it and local temperature may be harder to control. A diffuser can also absorb radiant output. No actual junction temperature or L70 life is predicted.

The multiplier sensitivity alone gives approximately 757–833 lm warm, 731–804 lm neutral and 728–801 lm cool. Thus the low multiplier misses 750 lm on the neutral/cool panels before any independent bin, diffuser or driver-current tolerance. The upper/lower multipliers are not verified production bounds. These candidates cannot yet guarantee the accepted optical envelope.

## Why direct parallel strings are not the default

The parallel N example does not retain the previous 13-device neutral/cool matching. More importantly, if one branch opens, a functioning 300 mA constant-current source may put its entire current into the surviving branch, if it retains compliance and no protection intervenes. That exceeds this family's stated 240 mA maximum even before thermal derating. A base current limit on total current is not individual branch protection.

A deliberately simplified ballast illustration assumes a 0.7 V string-voltage difference and allows 30 mA difference between two 150 mA branches. Ignoring LED dynamic resistance gives R = 0.7/0.03 = 23.3 ohms per branch, dissipating about 0.525 W per resistor and dropping 3.5 V at 150 mA. The assumed mismatch is not a measured or guaranteed device tolerance. This is not resistor sizing or an approved fault solution; it illustrates how balancing can consume voltage, heat and space. Active limiting, branch-open behavior and all faults would need separate design.

## Sourcing observations — checked 2026-11-14

| Exact MPN | Observed source | What is and is not established |
|---|---|---|
| JB2835BWT-G-H40GA0000-N0000001 | JLCPCB C17218060: https://jlcpcb.com/partdetail/C17218060 | Exact catalog listing and assembly offering observed. Live available quantity, price and bin not established from retrieved page. |
| JB2835BWT-G-H65GA0000-N0000001 | JLCPCB C17273573: https://jlcpcb.com/partdetail/C17273573 | Search-rendered catalog page showed stock 0 and pre-order. Direct opening returned HTTP 429; quantity is a retrieved-page snapshot, not live verified inventory or reserved stock. |
| JE2835BWT-N-H65GA0000-N0000001 | JLCPCB C17471867: https://jlcpcb.com/partdetail/C17471867 | Exact listing observed; live quantity/bin/price not established. |
| JB2835BWT-G-H27GA0000-N0000001 | DigiKey exact MPN page: https://www.digikey.pl/pl/products/detail/cree-led/JB2835BWT-G-H27GA0000-N0000001/14554750 | Search-rendered page showed 4,715 in stock and one-piece price PLN 0.51 excluding VAT. Indicative snapshot only, not a quotation/reservation. JLCPCB sourcing route not established. |
| JE2835BWT-N-H27GA0000-N0000001 / JE2835BWT-N-H40GA0000-N0000001 | Exact JLCPCB stock not established in this lookup | Missing confirmation does not prove unavailability. |

Technical design uses manufacturer documentation, not catalog parameter fields. For example, G-class JLCPCB fields show 60 mA/2.91 V where the manufacturer table's test point is 55 mA/2.67 V; these are not accepted as equivalent. Catalog “wave soldering” on some SMD listings is also not a qualified assembly process. Verify exact supplied package/bin and actual reflow/service with the supplier before selection.

Catalog support for a component does not establish that the intended LED-panel substrate, thermal construction, stackup and assembly process are offered together. Confirm the actual MCPCB/FR-4 route and assembly compatibility separately. No supplier contact, purchase, reservation or BOM upload was performed. Listings/prices/quantities may change before ordering.

## Reproduce the arithmetic

Save the following block as a temporary Python script and run it (standard library only). These are nominal screens and assumed sensitivities, not a circuit simulation.

```python
tau = 0.87
hot = {'2700': 27.2, '4000': 30.0, '6500': 29.9}
counts = {'2700': 8, '4000': 7, '6500': 7}
nominal = []
for cct in hot:
    vals = [counts[cct]*hot[cct]*m*tau for m in (4.0, 4.2, 4.4)]
    nominal.append(vals[1])
    print(cct, 'flux_lm', [round(x, 2) for x in vals],
          'power_W_assuming_3V', counts[cct]*3*.25)
print('nominal_ratio', max(nominal)/min(nominal))
print('nominal_optics', all(750 <= x <= 850 for x in nominal)
      and max(nominal)/min(nominal) <= 1.10)
r = .7/.03
print('ballast_ohm', r, 'each_W', .15**2*r, 'drop_V', .15*r)
print('one_remaining_N_branch_mA', 300, 'family_max_mA', 240)
```

## Recommendation and next gate

Investigate the G-class 8/7/7 single-string candidate alongside the earlier N 14/13/13 reference. It offers a route to lower normal voltage without adding parallel-string balancing; it is not a final selection or an automatic return to the old eight-LED design. Retain N as the more direct-data reference if G thermal life or procurement is unsuitable. No reason has yet been established to adopt direct parallel branches as the primary path.

Before controller/schematic selection: verify G curves and lifetime data at the proposed current, source exact parts/bins for all colours, quantify optical/thermal tolerance, obtain the competent accessible-contact/insulation/discharge acceptance basis, and define the real output normal/fault voltage-current window. Then compare the driver implementation and preliminary geometry within specification. Do not infer touch safety solely from a nominal voltage under 30 V, and do not treat driver IC thermal shutdown as full-lamp protection.

Verification: arithmetic executed separately; no CAD, formal toolkit requirement gate, electrical simulation, source-document hash capture or physical testing. New study reviews are tracked separately from prior packet reviews. No complete specification-stage approval exists.
