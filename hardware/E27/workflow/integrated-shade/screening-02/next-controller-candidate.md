# Follow-up lead: LYTSwitch-0 LYT0006D

Research lead found after the numerical-study freeze, 2026-11-19. Not a selected BOM, schematic or approved change to IS-1.1. Distinguish LYTSwitch-0 from the previously rejected NRND LYTSwitch-1 family.

Power Integrations publishes a full LYTSwitch-0 Rev B June2015 datasheet and AN-60 design guide. LYT0006D includes the switching MOSFET and thermal/fault functions. Exact lifecycle/orderable packaging and current procurement remain to be confirmed; a live product page is not a lifetime guarantee.

The manufacturer's RDR-378 Rev1.0 is a relevant historical7W,85V/82mA,190–265VAC bulb-driver reference. Its BOM lists a0.51x2.1inch board (approximately12.95x53.34mm),1.5mH output inductor and10x16mm output capacitor. These describe that reference, not our8W design or an800lm result. Its low-capacitance input differs from the HV9961 bulk-reservoir scenario and must not inherit that model's conclusions.

Crucial mismatch: the reference's optional open-load Zener is sacrificial. It cannot be copied as a repeatable protection for a detachable module. Investigate AN-60 alternatives and verify open-load/reconnect/discharge energy and failures. Historical EMI/PF results and protection claims do not establish current EU lighting compliance or full-product safety. Product-page metadata contains inconsistent isolation labels; the actual report explicitly identifies a non-isolated buck.

Exact supplier identities located: JLCPCB C567677 for LYT0006D; LCSC C394206 for LYT0006D-TL. They are different orderable/packaging identities to reconcile, not automatic substitutions. The retrieved LCSC inventory page is dated/stale, so neither its displayed stock nor sale price is accepted as current sourcing evidence. JLC assembly eligibility and actual stock must be rechecked before selection.

Sources:

- [Manufacturer part](https://www.power.com/products/lytswitch/lytswitch-0/lyt0006d)
- [Full datasheet](https://www.power.com/sites/default/files/documents/lytswitch-0_family_datasheet.pdf)
- [RDR-378](https://www.power.com/sites/default/files/documents/rdr378.pdf)
- [AN-60](https://www.power.com/sites/default/files/documents/an60.pdf)
- [JLCPCB part identity](https://jlcpcb.com/partdetail/POWERINTEGRATIONS-LYT0006D/C567677)
- [LCSC part identity; stale inventory](https://www.lcsc.com/product-detail/LED-Drivers_POWER-INTEGRATIONS-LYT0006D-TL_C394206.html)

Next bounded task: verify exact lifecycle/sourcing, reproduce the reference's electrical calculations using current parts, replace the one-shot protection with a repeatable bounded solution, and compare its protected BOM/thermal/assembly envelope with HV9961 and BP2863XJ. No schematic capture precedes accepted specification, independent pin intent and the actual required human decisions.
