# Velluneo LED and power screening

VEL-LED-SCREEN-01, revision 2, 2026-11-14. Specification study, not a part-selection approval. Input: product packet revision 7 and owner-selected architecture A, frozen in repository commit 0ab8e0e3fdeef6eb9d2606b4c021e4e710f7ba44. Packet path: hardware/E27/workflow/specification-reset/requirements-and-plan.md, Git blob 4c98e47953e822397e6461bf620546eb58a5ac22. Architecture decision: hardware/E27/workflow/specification-reset/architecture-comparison.md revision 2, Git blob 021acb4d9b1fadaa4f0e58363fe657e44e9e1bf8. Owner statement: "tak robimy wariant A" (current conversation, 2026-11-14). Git blobs identify the saved input files; they are not asserted SHA-256 values. Writer: /root. Only new documentation/calculation files; no CAD or existing rules changed.

## Sources and candidate data

Primary manufacturer sources checked 2026-11-14:

1. Cree CLJ-DS40 Rev 10B, pages 14–15: https://downloads.cree-led.com/files/ds/j/JSeries-2835-3V-Consolidated.pdf . JE2835B N-class, CRI 80, at 150 mA; suffixes H27/H40/H65 identify the three CCT candidates. Typical 25°C/85°C flux pairs: 70.7/63.8, 78.1/70.5, 77.1/69.6 lm. The 85°C entries are calculated reference values. Typical forward voltage is 2.86 V at 25°C; maximum listed at that test point is 3.0 V. The order code specifies a minimum flux bin, not an upper flux bound. Exact codes are in calculate.py.
2. Lumileds Commercial product table: https://lumileds.com/products/mid-power-leds/luxeon-2835-commercial/ . Candidate D1 codes L128-2780SA35A00D1, L128-4080SA35A00D1 and L128-6580SA35A00D1, CRI 80, 65 mA. Listed minimum/typical fluxes: 31.6/34.0, 33.8/36.3 and 33.8/36.3 lm. Full latest DS383, its measurement conditions and lifetime data have not been captured/verified for these exact parts. Do not treat the product-table comparison as a completed datasheet review.

No current JLCPCB stock, supplier cost, bin/reel availability or lifetime report was verified. Datasheet bytes are not archived/hashed in this preliminary source lookup; source pinning remains due before formal part acceptance. The typed calculation inputs are saved in calculate.py.

## Method and explicit assumptions

Run `python calculate.py > results.json` from this directory to regenerate the saved output. The script itself prints JSON to standard output. There is no dependency other than Python standard library.

- Cree nominal screen: count × manufacturer reference flux at 85°C × assumed diffuser/system transmission 0.87. Junction temperature 85°C is an illustrative operating point, not measured temperature or an approved thermal limit.
- Lumileds screen: count × product-table typical flux × assumed hot factor 0.90 × transmission 0.87. The hot factor is an unverified sensitivity assumption, not a manufacturer guarantee or temperature prediction. Exact test conditions must be confirmed in DS383 before comparing families on equal footing.
- Transmission 0.80/0.87/0.90 is explored; no diffuser material/geometry was selected or measured.
- Counts below are whole series strings at common current within each family. Different CCT panels may have different counts while using the same base; the driver must cover every panel voltage.
- Calculations ignore current-regulator tolerance, flux/current nonlinearities away from the stated test current, actual ripple, aging, temperature spread and spectral/geometry-dependent diffuser loss. These are open design inputs, not small errors assumed to cancel.

## Nominal results — not guaranteed lamp performance

| Family and CCT | LED count | Base current | Calculated lamp flux under the assumptions above |
|---|---:|---:|---:|
| Cree N, 2700 K | 14 | 150 mA | 777 lm |
| Cree N, 4000 K | 13 | 150 mA | 797 lm |
| Cree N, 6500 K | 13 | 150 mA | 787 lm |
| Lumileds D1, 2700 K | 30 | 65 mA | 799 lm |
| Lumileds D1, 4000 K | 28 | 65 mA | 796 lm |
| Lumileds D1, 6500 K | 28 | 65 mA | 796 lm |

Both nominal sets fall within 750–850 lm and the 1.10 brightness ratio. This is a plausibility screen only. The two families do not have equally strong temperature evidence. Equal count is not required: using 14 Cree LEDs in every colour instead gives 777/859/848 lm and ratio 1.105, missing both the neutral-white upper flux limit and matching target in this nominal example.

## Voltage, sharing and heat consequences

The Cree single-string candidate is approximately 40.0 V for 14 LEDs or 37.2 V for 13 at the stated 25°C typical forward voltage. Those are not cold-corner, normal maximum or fault-voltage limits. The old project's 30 V contact target has not been carried into this reset; raising voltage cannot be accepted without the new accessibility/insulation review. Offline service does not automatically make residual energy or accessible contacts safe. No assertion is made that a 40 V implementation meets the product's safety requirements.

The Lumileds long-series options require many series drops. At an explicitly assumed 2.8 V per LED they would be roughly 84/78 V; these are illustrative estimates only, not verified voltage specifications. This makes them less attractive for the current accessible-panel concept unless repartitioned.

Parallel strings reduce voltage but add a different problem. For example, two seven-LED strings would give 14 LEDs at about half the single-string voltage and twice the base current for the same per-LED current. That does not mean direct paralleling is acceptable: evaluate forward-voltage mismatch, thermal current sharing, open/shorted LEDs and one failed branch. Ballast or independent branch limiting may add cost, voltage loss and heat. A 13-LED panel cannot simply be divided into two identical strings. No parallel topology, balancing parts or driver current is selected here.

Cree electrical power at the nominal 25°C voltage is about 6.0 W (warm) and 5.6 W (neutral/cool). For a preliminary thermal budget, conservatively treat all panel electrical power as panel heat until radiant output and thermal paths are quantified. Actual LED heat is lower than electrical input because some energy leaves as light; lumen values alone do not determine radiant watts.

A 5.5–6 W panel with an assumed driver efficiency of 80–90% corresponds to roughly 6.1–7.5 W input and 0.6–1.5 W base conversion loss. This is sensitivity arithmetic, not a claimed lamp rating or selected supply power. It excludes additional unaccounted auxiliaries/contact losses and does not size transformer peak power or startup/fault margins. Heating of the diffuser by absorbed light also needs assessment.

## Sensitivity and acceptance risk

The script explores 81 scenarios per family: three transmission assumptions and independently varied per-colour flux multipliers of 0.93, 1.00 and 1.07. This is an assumed sensitivity sweep, not a shipment distribution, datasheet guarantee or statistical failure estimate. Most scenarios miss at least one optical criterion. Common scaling alone would hide the brightness-matching risk.

For Lumileds, the listed lower flux values combined with the same assumed hot factor already produce about 741–742 lm. Cree low-bin/hot proxies in results.json assume the typical temperature factor applies to minimum-flux parts; they are not guaranteed bounds. Cree order codes do not establish an upper flux bound. Therefore neither nominal set proves production-level compliance with both the narrow flux band and 10% matching rule.

Closure requires defined flux-bin procurement (including upper bound), characterized hot/cold LED samples, measured diffuser losses, current tolerances and an accepted sample plan. If the worst-case envelope cannot satisfy the targets, compare bin selection, panel counts, a justified inexpensive factory-set adjustment or a proposed requirement change. No requirement is silently relaxed.

## Recommendation and bounded next actions

Use Cree N 14/13/13 at 150 mA as a calculation/reference-sample candidate, not as the final electrical interface. It demonstrates that architecture A can plausibly supply all three colours without configuration and without assuming the old eight-diode design. Keep Lumileds D1 as a sourcing/performance comparison; do not select it from the weaker hot model alone.

Before choosing either:
1. Have the competent reviewer establish the accessible-output/insulation/discharge envelope. Compare the simple 37–40 V series candidate with a lower-voltage topology that has explicit current-sharing/fault protection. No high-voltage contact choice is delegated to the non-expert owner by implication.
2. Verify exact datasheets, bins, prices, actual assembly availability and lifetime evidence for candidate parts. Inspect package polarity and thermal pad before library work; a shared 2835 size is not proof of identical land pattern.
3. Obtain approved sample-test conditions and representative LED/diffuser samples. An isolated current-limited laboratory characterization can inform the driver; no order or physical test is authorized by this note.
4. Update the power/voltage/thermal envelope and preliminary housing concept before selecting a controller or creating a schematic.

Status: no final MPN/count/current selected; no cost/stock/lifetime guarantee; no CAD, simulation or physical measurement. Calculation execution completed, but no formal toolkit requirement gate is claimed. Independent review of this new note and arithmetic is tracked separately; previous packet reviews do not cover it.
