# Velluneo architecture comparison — preliminary recommendation

Record VEL-ARCH-01 revision 1, 2026-11-14. Status: engineering proposal within specification; no selected circuit, stage approval, CAD changes or manufacturing authorization.
Input: requirements-and-plan.md packet revision 6, repository file blob ff6cb3b4640164cbd3d4037c002d571d7c52e0dc, on spec/owner-interview-reset-2026-11-14. Coordinator owns this note. Technical review and final gate reviews are pending.

## Decision to make

Choose where current regulation lives, keeping a common E27 base, offline tool-free replacement and inexpensive panels. Compare the entire power path, not simply the number of ICs. LED count, operating current, output voltage, power, contact count, transformer, control IC, PCB size and stackup remain unselected.

A constant-current (CC) driver controls the LED operating current. A constant-voltage (CV) supply establishes a voltage rail; LEDs still need a suitable current-limiting/regulating stage. Equal current does not guarantee equal emitted flux across LED colour bins or temperatures.

## Three candidate partitions

| Candidate | Base | Replaceable panel | Expected benefits (engineering inference) | Main risks / selection condition |
|---|---|---|---|---|
| A — isolated CC driver | Mains input protection/filter, isolated power conversion with regulated LED current, output voltage limitation, discharge and justified thermal/fault protection. | LEDs, thermal substrate, contacts and only justified inexpensive ancillary parts. | Removes a separate downstream switching regulator if one-stage regulation meets all targets; keeps panel simple and avoids putting replaceable power electronics next to the LEDs. | Same-current LED selection/binning must meet 750–850 lm and brightest/dimmest ≤1.10 across three CCTs. Ripple, flicker, cold-voltage margin, no-load behavior and short recovery need calculation/test. A simple block diagram does not prove simplest qualified BOM. |
| B — isolated CV supply plus CC regulator on panel | Mains isolation, regulated rail, output protection/discharge and base thermal protection. | LEDs plus local switching current regulator, inductor, sensing and bypass/protection as needed. | Each panel can have a factory-set current appropriate to its colour/bin without user configuration; base output rail can remain common. | More parts, cost, heat and assembly complexity on every replacement panel; local fault and retained-energy cases; extra conversion loss. A bare LED board cannot be connected directly to the CV rail. |
| C — isolated CV supply plus CC regulator in base | Isolated supply followed by a low-voltage switching LED current regulator, with system protection. Both functions may share one base PCB if fit permits. | Simple LEDs/contacts/thermal substrate as in A. | Separates mains conversion from LED-current regulation; allows useful low-voltage laboratory evaluation of the current stage. | Two power-conversion stages and more base components/volume. A fixed common current still does not independently trim each colour. Justify with measured ripple/control/protection benefits if A is unsuitable. |

These are alternative functional partitions, not approved schematics. A transformer/barrier alone does not establish reinforced insulation, accessible-contact safety or suitable fault behavior.

## Initial recommendation

Investigate A first, with C as the principal fallback if output ripple, controllability, sourcing or integration makes A unsuitable. Keep B available only if per-panel current adjustment demonstrably provides a necessary benefit that cannot be achieved economically by LED selection in A/C.

This is a provisional engineering judgment based on repairability and panel-cost requirements, not a quantified claim that A is cheapest or most efficient. No BOM quote, transformer supply confirmation, layout feasibility or measured efficiency exists yet. The comparison must be revisited once real LED operating data and supplier constraints are known.

Do not copy the old LYTSwitch circuit automatically. The old part family is evidence of an available functional approach, not a qualified part choice for the new power range. Do not select the old 270 mA, eight LEDs, voltage thresholds or 70 × 34 mm by default.

## Manufacturer evidence and limits

Sources consulted 2026-11-14:
- Power Integrations LYTSwitch family overview: https://www.power.com/products/lytswitch — lists a flyback CV/CC family with integrated high-voltage switching and feedback. LYTSwitch-6 data-sheet landing page: https://www.power.com/design-support/data-sheets/lytswitch-6-data-sheet . Search retrieval provided the family/data-sheet description; direct opening of the data-sheet landing page returned HTTP 406. The full exact datasheet was not verified in this task. This supports topology exploration, not pin design or part qualification.
- Texas Instruments TPS92200 product documentation: https://www.ti.com/product/TPS92200 — describes a DC-input buck LED current driver with 4–30 V input and device-level open/short/thermal protections. It illustrates the downstream regulation block in B/C. It is not a mains converter or isolation barrier. These are illustrative manufacturer properties only, not selected operating values or proof the part fits Velluneo.

Internal IC thermal shutdown protects the IC under specified conditions; it does not by itself protect the panel, transformer, capacitors or housing. Likewise, IC open/short functions must be assessed in the actual whole-system fault circuit. A listed protection feature is not system verification.

## Simplicity changes to evaluate

The owner no longer requires live replacement. Therefore active LED-identification probes, their timing circuits, insertion detection, a microcontroller and reset logic are not requirements by themselves. Omit them from the candidate architecture unless a new calculation/requirement establishes a need.

Retain system-level functions: no-load voltage/temperature control, sustained-short tolerance without replaceable fuse operation for the specified panel faults, recovery after offline replacement/power cycling, thermal protection, accessible-part insulation, residual-energy discharge and safe service conditions. Determine whether normal driver behavior already supplies each function before adding separate circuitry. Do not assume it does.

No user wait time is selected until discharge and cooling are measured. No live removal/connection test is authorized by this comparison.

## Bounded next work before any schematic

1. Select a small LED candidate set with exact 2700/4000/6500 K MPNs and flux bins. Compare counts and currents using manufacturer hot/cold voltage, flux/current, Ra and lifetime data; include diffuser loss and component tolerances. Check how to meet the optical limits with one base.
2. Estimate panel power and heat, driver power/efficiency budget and voltage compliance. Assess a first mechanical/thermal envelope for both bulb-size concepts; no arbitrary dimension becomes a requirement.
3. Compare an isolated CC implementation and a two-stage fallback using exact controller references/transformer options, output ripple, startup, no-load/short behavior, component count, supplier assembly and indicative cost. Source and verify exact datasheets before using any physical pin mapping.
4. Review insulation/accessibility and safe-access acceptance with a competent reviewer, including removed-panel stored energy, connector faults and relevant single faults. Specify service-access protection and discharge behavior before freezing interfaces.
5. Prepare a justified choice and update four profile proposals, electrical interfaces and the machine-readable requirements. Obtain the complete specification-stage checks/reviews and genuine owner approval before schematic generation.

For initial optical/thermal characterization, panel samples may need to be built before the final mains driver is fabricated. Use an independently approved, isolated current-limited laboratory setup with specified stop conditions. This does not alter the final product goal or authorize bench work now.

## Remaining owner and expert inputs

Owner can accept A as the first architecture to investigate without accepting a specific circuit. Numeric CCT/distribution/appearance tolerances, supply envelope, service-access criteria, named technical reviewers, exact fabrication/assembly feasibility and lab bookings remain open per the specification packet. This note does not close those questions.

Checks performed: requirement/document comparison and primary manufacturer-source lookup only. No toolkit requirements CLI, doctor, electrical simulation, ERC, DRC, intended-connectivity export, thermal model or physical measurement performed for this note. Revision-2 packet reviews do not automatically cover this new note. Independent architecture reviews and final specification review remain pending.
