# DCM/magnetics/storage review record

VEL-FLYBACK-DCM-01 r2, 2026-11-14. Preliminary mathematical investigation only. No formal specification gate, human engineering sign-off, schematic approval or physical qualification.

## Frozen evidence

| Final file | SHA-256 |
|---|---|
| dcm-feasibility.md r2 | 8e97b1e8f37e466cc5e5f5b827807ac28b70a91ab59b4fd632a4c96c22afc288 |
| dcm.py | e5143c892f9f1c243cb5114b09a02ee3f8bf91ce933e0f66f9c89a427829d042 |
| dcm-results.json | c08444d90eec412ebcc33de78143e5113e227fb7228ef9293b34ba4afa0c4205 |
| upstream results.json | 6435677103247ad888ab1bdf2078409f8a5ecadcf165749fc70191534f4addb3 |

The r1 document hash was `70787a869b53d8cff43f9c05eb46a90df8907b9669cbfacaf06561644758fe07`. All four actual independent read-only agent contexts reviewed that same r1 with the frozen script/results, verified supplied hashes and reproduced the result file exactly. The author also executed it successfully. There are 288 electrical combinations and 2304 phase samples. Script/results did not change for r2.

## Actual independent reviewers and scope

| Role / context | Evidence checked / recommendation | Open engineering findings |
|---|---|---|
| Reality Checker /root/spec_reality | Equations, energy/current factors, independent numerical integration of line-cycle RMS and script reproduction; targeted r2 storage warning verified. Ready for preliminary human discussion. | RC-DCM-001 replace constructed frequency law with verified controller-specific operation, temperature/jitter/zero-crossing behavior. RC-DCM-002 coupled storage/LED/control/interface/bias/OVP analysis. RC-DCM-003 custom magnetics, actual losses, hot saturation, rectifier pulse handling and fit. |
| Overengineering Reviewer /root/spec_simplicity | r1 mathematical witness, timing-margin and complexity trade-offs; reproduction matches. No new overengineering blocker. Unaffected r1 scope retained; no claim of a separate r2 rerun. | OE-LED-01 complete comparable BOM/startup/protection/storage/thermal/process assessment remains open before controller/architecture selection. |
| Completeness Reviewer /root/spec_completeness | r1 RMS integrals, buffer energy/discharge math, numerical summaries and explicit deferrals; reproduction matches. No completeness finding for this early study. Unaffected r1 scope retained; no claim of a separate r2 rerun. | Actual controller operation, coupled LED behavior, bias/protection, sourcing and qualification remain deferred, not passed. |
| Change Reviewer /root/spec_change | r1 against product packet r11, reproduction; targeted r2 voltage-excursion warning verified. No requirement drift, false stock or approval claims. | No new Change finding; formal stage and design decisions remain open. |

Independent reviews relied on present files and executed/numerically cross-checked mathematics. They did not independently revalidate manufacturer PDFs, distributor status, controller operation or physical hardware. The author inspected original manufacturer sources and distributor listings as recorded in the study. No human reviewer or human acceptance is simulated.

## Review-driven clarification

r2 explicitly states that separate capacitor examples extend from 15.22197 to 29.45229 V, beyond the 18–27 V centers. The normal-load DCM/stress/bias model is not coupled to those excursions. Earlier 469/569 V drain numbers therefore cannot be treated as bounds for a completed buffered circuit. Both Reality and Change reviewers verified this targeted delta and unchanged script/result hashes. RC-DCM-002 remains technically open; documenting it is not a closure of the required coupled analysis.

## Current interpretation

The witness identifies mathematical timing room for further examination of a 0.50 mH candidate; approximately 2.14% minimum-on-time margin against a 25 C table limit is not full-temperature qualification. The constructed frequency law is not implemented by a resistor selection or demonstrated by the IC. Higher secondary pulse/RMS currents and output storage remain real trade-offs. No part, transformer construction, capacitor, fault ceiling, safe service voltage or waiting time is approved.

Next: actual feedback/bias/OVP programming, coupled LED/storage/fault interface analysis and geometric/thermal/sourcing assessment using common comparison conditions. No CAD, ERC/DRC, SPICE, installed-toolkit environment pass, purchase, supplier message, manufacturing-file submission or laboratory test occurred.
