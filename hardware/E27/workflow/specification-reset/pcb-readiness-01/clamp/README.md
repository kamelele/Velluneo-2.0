# Passive clamp energy and concrete winding/PCB constraints

PCB-READINESS-01, implementer `/root/readiness_clamp`, 2026-11-17. Base b1117ae2caecc037d9fc1253bd9c3a3c4effaaf2. Exclusive write scope is this folder. No shared CAD, graph, part value, threshold, profile or requirement changed. This is executed passive-circuit analysis, not an actual UCC28711 controller/TVS/MOS model, physical measurement, independent finding closure or stage approval.

## Result and design decision

Retain the present clamp parts while imposing a **proposed effective T1 leakage acceptance target of20uH**, and a **0.40W normal TVS-loss allocation**. These are concrete candidate procurement/layout inputs, not claimed parameters of the unbuilt transformer. At primary open inductance2.0736mH (the existing -10% end),20uH corresponds to lambda=Llk/Lm=0.9739%. In the declared cold-clamp/high-reflected-voltage normal screen, its TVS power is0.33019W at an11W magnetic-energy rate. The reserve to0.40W is0.06981W. Actual transformer leakage, the relevant three-winding equivalent circuit, clamp curve and allowed winding/PCB temperatures still require evidence before acceptance.

No normal-operation defect or need to lower TVS voltage is proven. Lowering the clamp can increase diverted magnetizing energy and harm thermal margin. Conversely, a hypothetical continuous high-power output approaching the clamp can divert nearly all magnetic energy. The normal thermal estimate must not be reused as an OVP/fault-train guarantee.

## Primary source basis

The saved and SHA256-verified TI SSZTCV6 article, February2024, p2 Figure2, explains that primary leakage and mutual inductances initially carry equal current, with the clamp/reset voltage difference discharging leakage. Its p3 explains why clamp loss exceeds leakage stored energy and depends on clamp/reset ratio. This analysis derives its own equations and explicit regime transition from that circuit; no vendor artwork/publication is redistributed.

Vishay88392,09-Jan-2024, p2 gives SMBJ160A: VBR178-197V at1mA, VWM160V, VCL259V at2.3A and native pulse conditions. Source p1 specifies600W for10/1000us and its5x5mm copper-per-terminal condition; this is not a DC power allowance. Source p3 gives RthetaJA100K/W **typical** at minimum recommended layout and RthetaJL20K/W typical. Its5W figure requires an infinite heatsink at50C and is not used for this PCB.

The inherited175.1164/225/286.972V plateau values are design sensitivities/proxies. In particular applying a breakdown-temperature coefficient to a clamping plateau does not make a guaranteed hot dynamic I-V bound. The0/1.7V diode cases are static sensitivities, not guaranteed full-temperature forward-drop limits. Source identities and exact repository inputs are in sources.json; primary PDFs stay external.

## Energy-conserving passive model

The approved candidate primary open-circuit inductance is preserved as Lp=2.304mH. Define lambda=Llk/Lm, Lm=Lp/(1+lambda), and Llk=Lp-Lm. This avoids silently adding leakage on top of a fixed measured primary inductance and inflating its stored energy. A real three-winding inductance matrix has not yet established this two-inductor equivalent.

Let Vc=VTVS+VDcl and Vr be a constant secondary voltage reflected to the primary. Immediately after turn-off, leakage and magnetizing currents both equal I0. While output and clamp branches conduct:

    dip/dt = -(Vc-Vr)/Llk
    dim/dt = -Vr/Lm
    Isecondary = Nps*(im-ip)
    tclamp = Llk*I0/(Vc-Vr)
    Eclamp = 0.5*Llk*I0^2 * Vc/(Vc-Vr)

This split is valid only when Vc>Vr*(1+lambda), so the output current can become positive and leakage ends before magnetization is exhausted. At or below that boundary, the secondary is blocked and the full stored energy0.5*Lp*I0^2 goes to the clamp in the zero-resistance model. The correct piecewise model remains finite and continuous at the boundary; extrapolating the split formula toward Vc=Vr would invent energy and is rejected.

TVS and clamp-diode energy are separated by their voltage fractions: Etvs=Eclamp*VTVS/Vc and EDcl=Eclamp*VDcl/Vc. Every analytic case verifies stored energy equals TVS plus clamp-diode plus secondary-delivered energy.

The executed analytic grid has1536 cases;768 use output18/27V and the remainder are37.4784/40V diagnostic screens. Constant reflected voltage is4*(Vo+VFout+secondaryIRscreen); the IRscreen is either0 or the separately maximized1.434087A times hotRs0.705633ohm. This is deliberately a conservative mixed screen, not a claim those extrema coincide in an actual controller trajectory. Repetition is capped by106kHz, an11W **normal magnetic-energy-rate hypothesis**, and a chosen1% ideal DCM period reserve. These construct internally consistent passive cycles, not actual UCC frequency commands or a proof of an11W input bound.

## Finite-resistance trajectories and actual checks

An independent event-driven SciPy solver integrates two currents and six power quadratures. During secondary conduction it uses:

    Is = 4*(im-ip)
    Vr(t) = 4*(Vo+VFout+Is*Rs)
    dim/dt = -Vr(t)/Lm
    dip/dt = -(Vc+Rp*ip-Vr(t))/Llk

Events end clamp current or secondary conduction. If the secondary is blocked, both inductors discharge together through the clamp and primary resistance; after clamp current reaches zero, remaining magnetization discharges through the secondary. The solver integrates TVS, clamp-diode, output, output-diode, secondary-copper and primary-copper energy separately. It does not substitute a fixed eta factor on top of these finite losses.

Sixteen finite-R cases (lambda1%/5%,Vo27/40V,VTVS175.1164/286.972V,VFout0/1.7V) were actually run at80 and160 maximum-step scales. Both runs use tight adaptive tolerances; their near-roundoff agreement is numerical consistency of this smooth passive model, not physical validation. Nine zero-R reference cases, including the exact split/all-clamp boundary, independently agree with the analytic result. verification.json records residuals and actual solver/runtime versions. The current-split KCL residual is an imposed constitutive identity, not an independent full-circuit KCL verification.

At lambda1%,Vo27V,VFout1.7V,coldVTVS175.1164V and hot windingR, computed TVS energy is4.23102uJ from148.07561uJ initially stored; at40V it is29.50463uJ. Neither example establishes actual high-voltage duty, TVS characteristics or controller regulation. Copper loss and finite secondary drop affect the result and cannot be represented by a lossless turns ratio.

## Derived thermal and leakage contract

At proposed local air70C and TVS junction target125C, an actual assembly RthetaJA<=100K/W would allow0.55W average. The source's typical100K/W does not prove the actual assembly meets that value. For the stricter normal allocation0.40W, the required actual thermal resistance is<=137.5K/W, before any separately unallocated pulse temperature excursion. Root owns the coupled thermal/placement design.

For normal11W magnetic rate, coldVTVS175.1164V, zero clamp-diode drop and the high-reflection screen Vo27V/VFout1.7V/secondaryIR1.01194V:

- 0.40W allows lambda<=1.18226%, nominalLlk<=26.92089uH.
- 0.55W allows lambda<=1.63284%, nominalLlk<=37.01622uH.

The proposed20uH finished-transformer target is tighter and includes the existing primary-inductance -10% endpoint. A future measurement/model record must define effective leakage for P-to-S with auxiliary open, P-to-A with secondary open, and the relevant simultaneous conduction states. Record complex impedance, fixture/short-lead compensation, frequency, signal level and winding state; do not treat one unexplained LCR reading with all secondaries shorted as a complete three-winding leakage model. Small-signal100kHz/0.1Vrms is a proposed starting characterization condition, not a normative test or an authorization to perform it. Fit/check against actual operating-frequency cases before accepting the20uH parameter.

At the same full11W screen and high reflection, the0.40W frontier contracts to6.86796uH at37.4784V and2.04227uH at40V. This is **not an observed CV/OVP failure**: actual no-load regulation may command far less energy, and the mixed reflected-current screen is not one correlated trajectory. It establishes that normal-only leakage heat arithmetic cannot establish high-output/fault safety.

## Fault energy and voltage acceptance

The fault table uses complete-energy diversion as an upper allocation **within this passive stored-energy model**. It covers1/3/9/100 pulses at755/106000Hz sensitivity rates. It includes the normal0.358522A proxy and1.6V/(2.37ohm*0.979), the latter explicitly **not a maximum fault-current bound**: source threshold conditions, delay, current slope, saturation, other faults and controller behavior are absent. N/f labels an allocated N-period window, not an actual fault duration/latency.

No11W limit is applied to fault trains. For each assumed train, N*0.5*Lp*Ipk^2 is the available diverted energy and its average requires a repeat interval at least Eburst/0.40W (or Eburst/0.55W). These are necessary average-power conditions only. Repetitive transient impedance, mounting, individual pulse envelope, junction excursions and actual fault clearing must also be established; an average bound does not prove pulse survival.

The inherited normal-line crest357.796V + hotTVS286.972Vproxy + diode1.7Vsensitivity gives646.468V before commutation:53.532V remains to the700V engineering screen and153.532V to the MOS800V absolute rating. These are algebraic allocations, not measured or guaranteed waveforms. MOS capacitances/gate behavior, TVS dynamic I-V, diode recovery, layout inductance, surge and actual fault sequences remain outside this model. No repetitive avalanche allowance is inferred from a single-pulse rating.

Before a PCB is accepted, specify the connected clamp copper/return path and an actual thermal capability consistent with the0.40W allocation. The current1.72x2.20mm TVS lands alone are not the source's5x5mm-per-terminal pulse-test copper. Larger connected copper can be a layout candidate, but mask, stackup, connections, coupling and loop inductance must be checked rather than treating any matching copper area as automatic qualification.

## Remaining findings and reproduction

CLAMP-01: effective transformer leakage is unknown; root/winding implementer owns a specified model/characterization proving the chosen20uH bound and its operating conditions. CLAMP-02: source-conditioned dynamic hot TVS/diode and complete MOS voltage/SOA behavior remain missing; root owns validated waveform/model evidence. CLAMP-03: actual fault pulse number/energy/clearing and repetitive thermal stress remain missing; root/startup-protection owns the coupled fault contract. CLAMP-04: actual PCB thermal/commutation path remains unbuilt; root owns source-backed placement/routing constraints and later validation. These retain RC-COMP-002/RC-PROT-001 and related gates; the implementer does not independently close them.

Run from repository root with NumPy2.2.6/SciPy1.15.3:

    python hardware/E27/workflow/specification-reset/pcb-readiness-01/clamp/calculate.py --source-dir /external/native-source-directory

The source directory contains ti-snubbing.pdf and smbj.pdf with the recorded hashes. Compact results retain all finite-R cases, analytic extrema/frontiers and the canonical hash of the full1536-case generated grid; full rows can be regenerated from code. This is generated analysis, not omitted physical measurement data. calculate.log records the actual successful execution. No new vendor publication, CAD, PCB, Gerber or manufacturing approval is created.
