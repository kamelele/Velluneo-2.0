# Native MOSFET model qualification

VEL-MODEL-01 r1, 2026-11-16. Specification investigation only. **Do not use this model to close gate-drive, startup, sampling or switching-loss acceptance.** No circuit, part selection, requirements or CAD change.

## What was actually executed

The existing ngspice44.2 shared runtime was loaded through its documented C API. A matching native spice2poly44.2 module was extracted from the official Debian package and loaded explicitly. Its archive checksum agrees with the official HTTPS package index; this is not a signed installation/doctor pass. Five ELDO selector metadata lines were removed from the ST archive for parsing. Native POLY and every numerical device parameter remain unchanged. No fitted capacitance, exponent, alternate behavioral source or fabricated convergence pass is used.

| Experiment | Observed result | Usable scope |
|---|---|---|
| RC transient engine smoke | Full10us; finite-ramp analytical check absolute error4.13e-8V at2.001us | Engine can execute this elementary transient, not proof of device-model compatibility. |
| Native MOSFET DC | AtVGS10V,25C, RDS13.3765ohm at0.5A | Approximately consistent with13ohm typical/16ohm maximum datasheet at those conditions. Component DC sanity only. |
| Native MOSFET small-signal AC | AtVDS25V,VGS0,1MHz,25C, Coss85.1713pF | Native datasheet26pF typical under the same conditions; ratio3.27582. Model representativeness is unqualified. Typical is not a guaranteed production maximum. |
| AC sweep0–640V | Integrated quasistatic charge proxy31.6578nC; grid-refinement difference0.01778nC | Numerical integration consistency only. Not a valid transient charge or an accuracy bound. Datasheet time-equivalent9.5pF gives6.08nC typical at640V; neither is a guaranteed worst-case charge. |
| Native-POLY resistive-load transient | 66rows; abort at100ns of requested12us; singular xq.5 / E2 timestep-too-small | Failed. No usable Qg, switching energy, drain-rise waveform or drive-current bound. Script intentionally exits1. |

The RC test and DC/AC results discriminate engine availability from the vendor-model transient failure. Missing spinit remains logged; the required module is explicitly loaded. Native-POLY support fixes the missing translator, but does not cure this transient. An earlier B-source compatibility experiment remains historical failed evidence; it is not replaced by a pass.

The model is an old25C-only artifact. The capacitance mismatch is a model qualification issue, **not evidence that physical STN1NK80Z fails its datasheet**. DC agreement does not validate charge storage. The integrated AC proxy must not replace the earlier6.08nC typical illustration in a claimed worst-case startup or sampling budget. Physical hot/lot/circuit variation remains unknown.

## Bounded alternative: comparison only

One alternative was inspected, STD2N80K5,800V DPAK. Native PDF page3 was inspected as a rendered table. No verified executable model was obtained; a guessed public model archive returned404. No claim that all manufacturer resources were searched or that no model exists. No live stock, JLCPCB assembly route, fit or thermal qualification is established.

| Source-conditioned property | STN1NK80Z retained candidate | STD2N80K5 comparison |
|---|---|---|
| RDS atVGS10V,25C |13typ/16max ohm at0.5A |3.5typ/4.5max ohm at1A |
| Qg typical |7.7nC,640V/1.1A/0–10V |5nC,640V/2A/0–10V |
| Time-equivalent Coss,0–640V |9.5pFtyp ⇒6.08nC charging proxy |16pFtyp ⇒10.24nC charging proxy |
| Single-point Coss typical |26pF at25V |8pF at100V; different bias, not a direct comparison |
| Energy-equivalent Coss |Not established here; do not use9.5pF as energy capacitance |7pFtyp ⇒1.4336uJ at640V |
| Package |SOT223 |DPAK; physical compatibility unqualified |

The ratio4.5/16=0.28125 is a source-conditioned resistance comparison, not a guaranteed71.875% reduction in whole-circuit loss. Lower resistance comes with a higher typical charging proxy and a different footprint. The alternative is **not selected** and does not justify reducing the12nC actual-drive budget hypothesis. Avoid adding circuitry or changing topology to compensate for absent model evidence.

## Findings and next discriminating evidence

RC-MODEL-001: **Major/open for switching-model acceptance**. Owner/coordinator. This legacy artifact is not qualified for the requested transient or representative capacitance/charge calculations. Resolution needs a manufacturer-qualified model/clarification with reproduced native-condition checks, or measured charge/switching evidence on a declared component and fixture. A different simulator without source-conditioned checks is insufficient. No physical component rejection is implied.

RC-BIAS-001 and RC-COMP-002 remain **major/open**. RC-CLAMP-001 node-charge/VS dynamics remains open; all historical protection/control/service/thermal findings retain their original scope. This packet adds no valid UCC28711 acquisition/current law, actual transformer/clamp waveform, hot SOA, fault latency, surge or measured safety evidence. Controller model and complete converter were not simulated.

Next bounded engineering task: establish actual controller first-three-cycle/settling/drive and node-charging waveforms using a suitable executable controller model or a declared laboratory fixture. Keep both MOSFETs as source-conditioned candidates until that evidence and fit/thermal comparison discriminate them. Freeze no circuit from the present results. Any physical test needs its own hardware/setup, responsible personnel, numeric limits and stop conditions; none occurred here.
