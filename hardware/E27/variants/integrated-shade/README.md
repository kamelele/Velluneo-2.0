# Current selection — SC09-SB01 restored

On 2026-11-24 the owner requested a return to the previous SC09 after reviewing the larger SB02 redesign. The active design is [SC09-SB01 / LYT1603D](SC09_compact/README.SB01.md): 19 positions, 51.2 x 33 mm. Its existing CAD and component choices are retained byte-for-byte. SC09-SB02 / LNK3206P is inactive and preserved as an alternative study; its pending acceptance request is withdrawn.

This restores the previous design selection, not a manufacturing approval. Its documented package-spacing limitations and prototype qualification gates remain. No supplier order or powered test is performed. The historical specification follows below.

---

# Integrated-shade non-isolated driver — specification draft IS-1

Status: local engineering proposal, not an approved schematic or manufacturing release.
Base: kamelele/Velluneo-2.0 main 377fc0a08e74043e255b732f7c2beb63134a3576.
Local branch: concept/integrated-shade-nonisolated-buck. No remote publication authorized by this packet.

## Owner intent

The user replaces a complete diffuser-plus-LED module. Most electronics belong in the base; minor electronics on the LED board are allowed. Approximately 800 lm after the diffuser, no dimming, ordinary bulb size and reasonable cost are the priorities. The user explicitly permits changing the LED count and operating voltage. The 8S/24–26 V baseline is not an electrical constraint for this variant.

This task studies the driver only. Coupling mechanism, E27 geometry and final enclosure are deferred, with explicit placement and product-release gates. Enclosing the LED board is a design premise to validate, not evidence that touch protection has been achieved.

## Proposed electrical architecture

Protected mains input → EMI network and rectification → energy storage selected with flicker/harmonic analysis → non-isolated constant-current buck → detachable LED module.

No mains-isolating transformer or secondary logic board is planned. An inductor remains. A bridge alone cannot regulate LED current. All output wiring and LED conductors are mains-referenced; differential LED voltage is not touch safety voltage. Neutral is not a protective-earth or accessible reference. No external USB/control/test interface is allowed to become accessible without an independent insulation assessment.

Use 230 VAC / 50 Hz and 207–253 VAC as a proposed EU design screen, not a newly confirmed market specification. First compare 60, 72, 90 and 108 V at 8 W, rather than freezing 60–90 V prematurely. The target 7–9 W at the LEDs and approximately 800 lm are distinct: LED part/bin, CCT, temperature, optics and drive current must establish actual light output. Initial optical study may use 2700 K / CRI ≥80 as a proposal, not a new owner decision.

## Controller disposition

BP2863XJ is a compact research candidate: manufacturer describes an integrated switch, bridge and recovery diode, configurable OVP, short protection and thermal regulation. Its full datasheet, exact orderable suffix, procurement path and conflicting selector ratings are unresolved. Do not capture a schematic using only its short product brief.

BP2863X lacks OVP in the manufacturer's selector; it is not an equivalent substitute for the detachable-load application. BP2862XS is a larger, higher-capacity family, with no demonstrated total-system advantage at this power. Prior mention of these two devices was a preliminary shortlist and is superseded by this disposition.

RDR-464 is an historical 8 W / 60 V / 135 mA buck reference, not our implementation. Its LYTSwitch-1 family is not recommended for new designs. AL1678 is obsolete. Their published results are not evidence for this variant. A documented external-switch controller remains a valid fallback if its total BOM, protection and sourcing are better supported.

## Required fault behavior

Define and verify startup at all declared line/LED/temperature corners; open LED and removed module; output short; LED short; sense/component fault; reconnect and contact bounce; brownout/restart; surge/inrush; thermal derating/shutdown; and residual capacitor energy. The output must remain bounded under open load and reconnection must not overdrive the LED. Concrete thresholds must come from selected parts, LED limits and the assembly safety assessment before schematic acceptance. Instructions to disconnect the lamp do not replace physical touch protection, including the exposed base after module removal.

## Size and cost study

40 × 25 mm is an unapproved placement experiment, not a resulting board size or fit claim. Do not draw a false enclosure-fit boundary from it. Report actual component courtyard area, both PCB sides, highest components, thermal assumptions, manufacturing rails/panel and tolerance effects when parts are selected. Mechanical interface and spatial intent must be approved before formal placement.

Cost must include PCB, parts, assembly class, THT handling, extended-part/setup charges, panel/rails, sourcing and test. No purchasing quote or current unit cost has been established.

Propose JLCPCB FR-4 2-layer 1 oz, 1.6 mm, lead-free HASL; Standard PCBA is an evaluation candidate if mixed assembly or two-sided placement is needed. Economic PCBA should be reconsidered if a single-sided supported BOM fits. Exact service, material/CTI, copper, finish, process and panel require confirmation; none is approved. Supplier minimum spacing is not mains insulation spacing.

## Verification and gates

Requirements and source provenance precede CAD. Independently derive intended physical pin connections from requirements and exact datasheets, review and obtain human acceptance, then generate the schematic. Compare a fresh exported netlist pin-for-pin against approved intent; ERC cannot replace this. Verify symbol-to-package pad mapping, polarity and footprints independently.

Before layout: approved spatial/mechanical envelope and thermal/insulation assumptions; minimize switching loop area, keep sense/feedback away from SW, use Kelvin returns where applicable. Derive numeric keepouts from this design, not the JLC article's XL4015 example. Refill zones, run fresh ERC/DRC and schematic/PCB parity, and inspect both sides and 3D. No KiCad MCP server is currently exposed in this chat; do not claim live MCP operations. Pinned CLI/pcbnew tools can be used for later authorized tasks. New MCP software requires code review and scoped, pinned installation first.

Standards applicability is preliminary, not a compliance declaration. Assess complete-lamp safety (IEC 62560 candidate), driver safety (IEC 61347-1/-2-13 candidate), emissions/immunity and harmonics under applicable EN editions, ecodesign/light quality, energy labelling/RoHS and final product classification. Determine actual harmonized editions and transition dates; no full standard clauses or insulation distances have been verified from licensed texts. UK/other market extensions are not assumed.

Qualification includes steady-state optical/thermal tests with the actual diffuser and LED bins; LED solder/junction temperatures; capacitor case temperature/lifetime; line/load/restart/fault matrices; conducted/radiated emissions, immunity, harmonics, DF/PF, PstLM and SVM; insulation/accessibility and residual-energy checks of the complete assembly. Define instruments, samples, responsible human and stop limits before physical tests. No measurements, simulation, ERC or DRC exist for IS-1.

See sources.json, requirements.json and screening.json; lifecycle evidence belongs in ../../workflow/integrated-shade/.

## Documented engineering fallback

HV9961LG-G is a fully documented external-switch alternative for further calculation, not a selected final BOM. Microchip DS20005588B Rev B specifies average-current control, 8–450 V operation and hiccup short protection. It does not establish a built-in system thermal shutdown or bounded open-load output. The typical eight-pin map is VIN, CS, GND, GATE, PWMD, VDD, LD, RT (pins 1–8); this is not a complete independently approved connectivity contract. RT must return to GND; do not reuse HV9910B timing wiring blindly. Datasheet minimum-on-time, duty, thermal and current-reference limits still require corner checks.

The manufacturer's HV9961DB1 guide explicitly allows the output capacitor to charge to rectified mains when LEDs are open, and states the demo is not CISPR15-compliant. Do not reproduce its output protection or claim compliance from it. Additional open-load/reconnect, discharge and thermal provisions are required.

LCSC C144192 identifies HV9961LG-G, but that is not confirmation of JLCPCB assembly availability. HV9910BLG-G (JLCPCB C9099) is a sourced comparison with peak-current regulation; it is not interchangeable with HV9961 without redesign. Supplier inventories/prices are transient and require a dated refreshed quote before purchase.

## IS-1.1 review corrections

The first draft reviews identified missing machine-visible gates. REQ-SAFETY-TEST and REQ-FAULT-TEST now require actual measurements at release, separately from schematic-stage design reviews. REQ-ENV owns the unresolved ambient/fixture/orientation/thermal/lifetime inputs. REQ-OPTICAL-INPUT closes the earlier CCT/flux/optical selection decision by schematic acceptance, while final measured light output remains due at release. REQ-INTERFACE and OPEN-INTERFACE require a structured electrical interface before schematic acceptance; the empty interfaces list is explicitly incomplete, not a declaration that the product has no interface.

The first 40x25mm board experiment, all numerical LED operating points and all proposed manufacturing parameters remain unapproved. This correction adds requirements and owners, not evidence of their completion. No engineering gate has been advanced.
