# IS-SCREEN-02 — progress and handoff

This is a research supplement to IS-1.1, not a completed specification or later engineering stage. The original approved publication packet remains byte-for-byte preserved. Its historical pending-publication statements are superseded by publication-receipt.json; they are not rewritten as if they described later events.

Owner approved exact draft publication and continuation; first market/input is now confirmed as Poland/EU230V50Hz,207–253VAC screening. Owner explicitly requested a process comparison before choosing Economic/Standard; no process selection is recorded. No schematic/placement/routing/release approval is inferred.

Original ten-file freeze: b9203b721bcb984bf8af620769ff0ecace907c316794442c1cc4062f4792ca2a. Actual numerical reproduction and scoped independent reviews are recorded in reviews.json. These checks validate limited arithmetic/model consistency, not real electronics. The later next-controller-candidate.md and process-temperature-check.md are declared follow-up notes, not silently covered by the original freeze. Final change review covers supplement scope and these additions separately.

New engineering learning: the ideal bulk-capacitor budget can sustain the proposed higher LED voltages in several scenarios, but does not establish harmonics/flicker or actual input ratings. HV9961 at low current and40%pp ripple needs large calculated L values under the tested timer corner; it is not yet the smallest/cheapest choice. Fully documented LYT0006D/RDR-378 is a promising follow-up lead with an explicit non-destructive OVP/reconnect redesign requirement and unresolved current procurement.

Process comparison favors investigating one-sided Economic PCBA first, with exact BOM eligibility, actual THT handling, reflow compatibility, tooling and panel requirements checked. Standard remains available if actual parts/sides/process require it. All published prices are partial planning figures, not a project quotation.

The old requirements-check-final.json remains the historical IS-1.1 check. Its OPEN-LINE is superseded by the actual owner decision in this supplement, to be incorporated with genuine evidence during the next deliberate requirement revision. OPEN-PROCESS and LED/thermal/interface/standards unknowns remain unresolved. No requirements evidence is forged to turn that check green.

Next bounded specification work: select a documented/procurable integrated-driver candidate, compare complete protected BOMs and real magnetics, develop repeatable open-load/reconnect protection and confirm optical/electrical LED and environmental inputs. A process/human specification decision and independently approved pin intent are required before capture. Size requires actual CAD placement later. No board order, supplier message or mains test has occurred.
