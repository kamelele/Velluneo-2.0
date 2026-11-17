# ELEC-CLOSE-01 — concrete custom-transformer winding candidate

Implementer proposal, 2026-11-17. Read device AGENTS and pinned implementer role. Original bounded implementation scope was temporary analysis; this integrated record is owned in this magnetics directory. Root remains sole project/CAD writer. No electrical graph, approved stage, shared CAD or finding status changed. All results below are calculated or proposed; none are measured or independently approved.

## Retained transformer and actual wire definitions

Retain TDK EFD25/13/9 gapped B66421U0160K187 + ungapped B66421G0000X187, bobbin B66422W1010D001; two B66422B2000X000 yokes are the native accessory candidate. Native October2022 PDFp2 gives AL160nH±10% for this gapped/ungapped pair, Amin57mm²; p3 gives AN40.7mm² and representative mean turn length50mm. Np120, Ns30, Na22 gives Lp2.304mH±10% and ratios4/.73333. No extra winding/tap/shield introduced.

| Winding | Commercial manufacturer/order definition | Conductor | Finished wire and resistance source facts |
|---|---|---|---|
| Primary P,120 turns | **ELEKTRISOLA Polysol180 / P180, copper, nominal0.180mm, IEC Grade2** | 0.180±0.003mm | Native size table Grade2 OD0.205–0.217mm; R20 nominal0.6718,max0.7007Ω/m |
| Auxiliary A,22 turns | Same P180 Cu0.180mm Grade2 | Same | Same; minimizes distinct wire inventory |
| Secondary S,30 turns | **Furukawa TEX-E, nominal conductor0.30mm**, single solid copper conductor with three insulation layers | 0.30±0.010mm | Native table typicalOD0.500,maxOD0.520mm; R20max262.9Ω/km=0.2629Ω/m. **Table is explicitly reference data, not a procurement batch guarantee** |
| Holding/separation tape | **3M1350F-1**, 10.5mm slit width proposed | Polyester/acrylic | Native Nov2024 p1 nominaltotal0.064±0.013mm; representative upper0.077mm used for packing; data explicitly representative, not a binding specification |

These are actual manufacturer-defined products/size/grade combinations, not invented finished-transformer part numbers or claimed retail SKUs. No stock, quotation, manufacturer message, order or JLCPCB transformer supply route established. P180 has a higher wire thermal designation than TEX-E/tape; **TEX-E and tape have130°C source thermal ratings**. This does not establish assembly system compatibility, operating temperature, service life or finished-transformer certification.

## Proposed layer construction

One continuous nonsplit primary, then auxiliary, then secondary. Avoiding split P does not guarantee acceptable leakage; previous assumed1% leakage is **not confirmed by this construction**.

Use an active winding band **10.5mm wide**. Suggested machine packing pitch0.240mm for P/A and0.550mm for S; these exceed reference maximum ODs. Reserve the unused width for controlled layer transitions/exit pockets rather than passing a crossover over the main winding build. Tape is 10.5mm slit width, four single circumferential wraps with seams staggered so no angular location has more than one extra overlap thickness. Tape overlap itself is proposed1mm along circumference; it is a mechanical construction choice, not a safety spacing or certified barrier.

| Inside → outside | Turns/layers | Maximum layer span at proposed pitch | Maximum ordinary radial addition |
|---|---|---:|---:|
| Base holding tape | one wrap | 10.5mm | .077mm |
| Primary | 40+40+40, no interlayer tape | 9.60mm | 3×.217=.651mm |
| Separation tape | one wrap | 10.5mm | .077mm |
| Auxiliary | 22, one layer | 5.28mm | .217mm |
| Separation tape | one wrap | 10.5mm | .077mm |
| Secondary TIW | 15+15, two layers | 8.25mm | 2×.520=1.040mm |
| Outer holding tape | one wrap | 10.5mm | .077mm |

Ordinary radial build **2.216mm**; with one extra seam thickness **2.293mm**. Wire-only radial build1.908mm. Required active rectangular local winding space is therefore **at least10.5×2.293mm**, before any unaccounted bunched exits, sleeves, adhesive lumps, safety margin tape or required extra primary interlayer insulation. At the proposed0.240mm packing pitch the primary leaves0.90mm total unused band width (the bare maximum-OD arithmetic alone leaves1.82mm). Neither allowance is a creepage claim.

Calculated nominal copper cross-section sum5.7340mm² / AN40.7 = **14.09% copper fill**. Sum of maximum-OD wire circles11.6228mm² / AN = **28.56%**. Band×worst seam build24.0765mm² / AN = **59.16%**. These are different packing diagnostics, not interchangeable utilization factors. This is a concrete low-fill winding candidate. **AN alone cannot prove a10.5×2.293mm rectangle fits the actual bobbin/core opening**. Native drawing dimensions13.1/11.7/18/26 must not be reassigned into an invented guaranteed winding rectangle. Confirm the local usable window, winding flanges, seam and exit paths using a dimensioned winding drawing/actual bobbin before saying it fits. Source-based diameter/packing arithmetic is complete; local physical-window acceptance remains open with the coordinator/winding implementer.

No primary interlayer tape is currently counted. If the insulation design requires it, add its actual build and recalculate; do not silently squeeze it into the stated2.293mm. P/A enamel or holding tape is not being claimed as reinforced primary-secondary insulation. Retain TIW insulation intact outside its controlled terminal stripping zone; finished lead exits/terminations still require the project's approved insulation geometry and actual inspection.

## Winding polarity and pins

Preserve the accepted local pin basis exactly:

| Winding | Dot/start | Finish | Turns |
|---|---|---|---:|
| P | 1, BULK_POS | 5, MOSFET_DRAIN | 120 |
| A | 2, PRIMARY_GND | 4, AUX_FLYBACK_POS | 22 |
| S | 6, OUTPUT_NEG | 10, SECONDARY_FLYBACK_POS | 30 |

Start all three windings with the same encircling rotational sense viewed from one fixed winding-axis end; layer traverse reversal does not reverse the winding rotation. Document that fixed view and pin1 mark on the winding drawing. This is a **new assembly instruction**, not a TDK finished-transformer property. With primarydot1 positive during MOSFET on, dot2/dot6 are positive relative to4/10; on flyback reversal undotted4/10 become positive relative to their returns, as required by auxiliary/output rectifier anodes. Low-voltage phase/ratio verification remains unperformed.

Pins3,7,8,9 have no winding wire or PCB electrical connection; remain physically present. Primary leads stay in row1–5, TIW secondary leads in row6–10. Do not add a hidden tap, shield or connection to core/yokes. Row arrangement and unused pins do not establish insulation distances. Lead stripping, solder spread, sleeve selection, bare ends, bobbin/core/yoke contact and inter-row clearances are unresolved physical insulation details owned by the coordinator/competent winding review.

## Reproducible resistance/loss screen

Run `python calculate.py` from this directory; output `winding-results.json`. Native MLT50mm is a representative value, not a tolerance bound for this custom layer stack. Calculate both MLT50 and an explicit **MLT60mm construction-length budget**, plus100mm total extra lead length per winding. Proposed cut-length acceptance budgets: P≤7.30m,A≤1.42m,S≤1.90m. These limits must be checked when winding; they are not manufacturer maximums.

R(T)=R20max×length×[1+0.00393×(T−20°C)]. Alpha is an engineering copper-material approximation, not a sourced hot-wire guarantee. Use supplied separate normal corner maxima IpRMS.091545A, IsRMS.53879A, primary peak.358522A, secondary peak1.434A. Summing separate RMS maxima is a conservative DC screen, not one asserted correlated controller trajectory.

| Case | Primary R / DC-equivalent loss | Secondary R / DC-equivalent loss | Auxiliary R |
|---|---|---|---:|
| MLT50,20°C | 4.2743Ω / .03582W | .42064Ω / .12211W | .84084Ω |
| MLT50,125°C | 6.0380Ω / .05060W | .59422Ω / .17250W | 1.18783Ω |
| MLT60,20°C | 5.1151Ω / .04287W | .49951Ω / .14501W | .9950Ω |
| MLT60,125°C | 7.2259Ω / .06056W | .70563Ω / .20484W | 1.40558Ω |

P+S screen at MLT60/125°C: **.26540W**, excluding AC/core/auxiliary/termination losses. Minimum-conductor-area RMS current densities3.72A/mm² P,8.16A/mm² S; these are descriptive, not thermal approval. Small S wire yields low absolute loss but relatively high current density; larger S wire is a possible later tradeoff requiring a new packing calculation, not an unrecorded substitution.

At the same assumed hot resistance, instantaneous peak IR drops are P2.591V and S1.012V. **Do not omit this winding resistance when updating auxiliary takeover/VS/CC/output startup/clamp analyses**. It is additional to rectifier drops and cannot be represented as a lossless ideal turns ratio. Actual waveform-dependent terminal regulation still needs the controller/circuit model or measurements.

Auxiliary RMS waveform is not established. Give a coefficient instead of inventing one: at MLT60/125°C, Paux=1.40558×IaRMS² W; examples20mA→.000562W,50mA→.003514W,100mA→.014056W. These examples are not bounds on the actual charge pulses. Source startup and auxiliary-waveform major findings remain open.

No AC winding loss, skin/proximity enhancement, center-gap fringing loss, magnetic core loss, thermal equilibrium, nonlinear saturation, fault survival or leakage/capacitance prediction is claimed. In particular the native N87200mT/100kHz/100°C loss point cannot be extrapolated into a guaranteed loss for this flyback waveform with arbitrary Steinmetz exponents. Existing flux/current witnesses remain conditional circuit results; this report does not close their magnetic/fault limits.

## Source identities and ownership of remaining inputs

| Primary source | Relevant pages | SHA256 |
|---|---|---|
| component-study/source/efd25.pdf | TDK10/22 p2 core,p3bobbin; native bobbin p3 directly viewed | f4b6084fa9171a0157c3744663e146da6b3a738171dab4dfd3e137c125f6f06e |
| External native ELEKTRISOLA wire PDF | p2P180 product,p4size/Grade2/R20 table; p4 directly viewed | 061d2605a50cd0dbf6c1b04ef13a96cb159a131b6bcc8232a99450e56839e2bb |
| External native Furukawa TEX PDF | p1thermal,p2OD/R20/reference disclaimer; p2 directly viewed | 555d1d7ad971071b09ec2c6b4ae72e9c951c6c7c7eb22d37676d2d6e434ba713 |
| External native 3M1350F PDF | Nov2024p1total thickness/thermal/typical disclaimer; directly viewed | d1eae6e4f40279fa49f7aa2322cbde5c276ea7a635e5550c19feb68cc3997468 |
| Approved pin-basis-primary.md | T1dot/start mapping | f02c2faa3cf05bd833c44a56180a7f53140158d84717fa14907b37ea9d7d56a4 |

Original URLs:
- https://www.elektrisola.com/Download/Enamelled%20wire_eng.pdf
- https://www.furukawaelectric.com/en/product/catalogue/pdf/tex_m028_e.pdf
- https://www.furukawaelectric.com/tex-e/en/product/texe_series.html
- https://multimedia.3m.com/mws/media/86180O/3m-tape.pdf?fn=1350FDS.pdf

Coordinator owns exact geometry/process/insulation-system acceptance, procurable batch limits, lead-exit drawing and effects of added winding resistance in circuit calculations. Actual later winding/lab personnel own recorded phase/inductance/DCR/leakage/withstand/temperature measurements when hardware exists; no such personnel or tests are fabricated here. The retained construction is a concrete **candidate specification** for a winding trial, with explicit local fit and insulation acceptance conditions, not a released manufacturing drawing or proof of finished-transformer safety.


Integration note: Full manufacturer PDF/STEP/HTML/image files are intentionally not copied into this directory. `sources.json` records source identities and original URLs; `README.md` gives reproduction instructions. Initial source paths in the technical narrative identify the original read-only analysis evidence, not required repository-distributed vendor files.
