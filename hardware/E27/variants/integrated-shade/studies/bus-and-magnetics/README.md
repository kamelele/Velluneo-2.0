# IS-SCREEN-02 — input reservoir and magnetic screening

Continued specification investigation after published IS-1.1. No schematic or PCB has been generated. This study does not approve a controller, process, operating point, product size or compliance.

## Reproduction and model

Run Python3.11+ `python calculate.py PATH_TO_THIS_DIRECTORY`. Inputs and script hashes are in results.json. The model starts at a charged line peak, advances a constant-demand capacitor energy state, and clamps it to a rectified ideal sine source. It discards the first0.2s and inspects0.1s. Step20us is compared with10us. This is a source-impedance-free numerical screening model, not a validated circuit simulation. It cannot give realistic charging/inrush/diode/capacitor RMS currents, PF/THD, EMI or optical flicker.

The load demands8W/0.90=8.8889W. Owner-confirmed line is207/230/253VAC50Hz. Bridge drop1.6V, C=-20%, L=-10%, fixed LED voltages and90%efficiency are assumptions. They are not selected parts, thermal/aging limits or measured results. Any interval below the required driver bus envelope invalidates a continuous-regulation interpretation for that case; the constant-power demand is not real dropout/restart behavior.

## Findings

At207VAC and the -20%C scenario, the ideal minimum bus is approximately143.74V with nominal2.2uF,192.25V with3.3uF,220.98V with4.7uF and257.16V with10uF. The108V LED scenario needs at least144V for the HV9961 ideal duty limit alone, so2.2uF is already marginal/failing before any real drops, cold LED spread or control margin. None of these numbers selects a capacitor. Voltage rating, ESR/ripple/lifetime, inrush, harmonics, heating and actual source impedance are separate checks.

Maximum20us-versus10us trough difference is0.351V; final endpoint repeats exactly over the inspected periodic window; numerical input-minus-served-load-minus-storage energy residual is below5e-13J. This checks implementation consistency only. A line/load/capacitor corner sweep with actual components is still required. The near-boundary2.2uF/108V result is not a trustworthy quantitative dropout prediction.

The HV9961 fallback has a significant magnetics tradeoff. At the226kOhm timer test point, use8/10/12us for screening. With40%peak-to-peak ripple and -10%L, nominal inductance would be approximately15/21.6/33.75/48.6mH for60/72/90/108V at8W. These are calculated L values, not available cores or footprints. Higher LED voltage lowers current but raises required inductance in this control/ripple scenario. This weakens the assumption that increasing voltage automatically makes this controller's supply smaller.

A generic critical-mode buck comparison at300VDC/60kHz gives approximately3.0/4.10/5.91/7.78mH. That is a topology comparison with changing peak current and stored energy, not a BP2863XJ design, permitted part substitution or size prediction. Core energy, DCR, saturation, flux swing and heating matter as well as mH.

Minimum-on-time screening at high bus gives1.62–3.48us at the8us off-time corner; these exceed the datasheet's1us maximum minimum-on boundary under its stated conditions. This says nothing about unmodeled lower LED voltages, bus spikes, startup or tolerance/temperature corners. The assumed6nC gate and approximately1mA bias produce about0.54–0.58W of total high-voltage chip input power at that corner; this includes gate-drive energy and is not a measured die dissipation. A proper IC thermal calculation is mandatory.

## Source and protection basis

Microchip DS20005588B RevB, pp3–8, supplies the current/timer/control basis: https://ww1.microchip.com/downloads/en/DeviceDoc/HV9961-LED-Driver-with-Average-Current-Mode-Constant-Current-Control-Data-Sheet-20005588B.pdf . In particular use264/275/286mV reference; do not mix earlier revision limits. Timing table test points are not a full-temperature guarantee. CCM, switching timing and supply heating limits remain prerequisites.

HV9961DB1 explicitly is not a qualified EMI/limited-open-output design for us: https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/UserGuides/hv9961db1.pdf . Its open-load capacitor may reach rectified mains. We retain open-load/reconnect/discharge, external thermal and surge/EMI work.

An8.89W input does not justify a blanket exemption from lighting harmonic rules. Establish actual applicable ClassC low-power clauses/alternatives and EN editions before acceptance; public IEC scope alone is insufficient: https://webstore.iec.ch/en/publication/92799 . No claim of PFC, PF/DF, harmonic compliance, PstLM/SVM or800lm is made by this model.

## Next engineering decision

Prefer further investigation of a fully documented integrated critical-mode driver if it preserves protection and sourcing requirements. HV9961 remains the reproducible, well-documented fallback; it is not now chosen as the smallest/cheapest solution. Compare actual protected BOMs and magnetic components, not IC counts. Resolve process selection after the separate Economic/Standard comparison. Preserve the original IS-1.1 requirement matrix as historical; the owner has confirmed line/market, but process, LED/thermal/interface and stage acceptance remain open.
