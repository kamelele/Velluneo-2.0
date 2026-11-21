# Input and rectifier design update

VEL-INPUT-01 r1,2026-11-17. Specification research; consolidated pre-schematic intent P0 in circuit-intent.md. Sole writer/coordinator/root. Actual new evidence:288 averaged mains/bulk integration cases with halved-step check, source-conditioned rectifier/NTC arithmetic, native-source inspection. No controller/full-switched-converter simulation, physical measurement, CAD or manufacturing pass.

## Concrete input-stage change

Prefer Rubycon450BXW15MEFR10X20 (15uF450V) over10uF comparison. Native body10x20mm,190mA120Hz/475mA100kHz105C; correct10kHz coefficient2.1 is used for the constructed33–82kHz HF witness. The conservative normalized triangle screen is1.1183 for10uF and0.7704 for15uF. It assigns all LF RMS to the50Hz rating and the entire prior primary RMS to10kHz. This is a deliberately conservative engineering comparison, not a manufacturer-approved spectrum/lifetime method or proof that10uF physically fails. The LF and HF maxima come from **different, uncoupled load/control models**. The0.0889A HF term is not a proved bound for a10W converter. Triangle conservatism applies only when both spectra are valid bounds for the same operating design; therefore0.7704 is not a conservative whole-converter rating result. Full Fourier spectrum, load-consistent switching/capacitor impedance, internal temperature, tolerance/aging and actual control remain unverified.

The native BXW endurance is10000h105C for this case length; this is not a5-year lamp-life promise. Initial±20% room capacitance is evaluated, not a full hot/aged capacitance bound.

| Preferred15uF calculation | Result and scope |
|---|---|
| Input |207/230/253Vac50Hz proposed research envelope;6/8/10W remaining constant bus load,47ohm±5% plus0/10ohm source sensitivity,1.6/2.2V fixed bridge drops,998k primary bleed; no obsolete external bias-feed resistor. These are assumptions, not new owner-approved product limits. |
| Minimum bus trough |259.047V, above the240V lower bus in the prior constructed HF witness. This does not prove actual controller regulation. |
| Line RMS / repetitive charging peak | Up to90.90mA /284.53mA in the averaged model. No startup/surge peak equivalence. |
| Fixed resistor heat allocation | At most0.4555W even charging all source-resistance loss toRIN. AC05 has5W at40C/4.7W at70C under native mounting; actual bulb layout/temperature must be checked. |
| Bridge conduction allocation | Up to0.08165W for stated fixed-drop sensitivities; low-temperature/hot leakage and dynamic behavior not bounded. Native MB10S current/pad/capacitive-load derating remains applicable. |
| Numerical check | Maximum trough change6.70e-5V and line-RMS change3.92e-8A with2us→1us step. This is numerical convergence of this model only. |
| Power factor |0.481–0.587 calculated. No PF/harmonic acceptance exists here and no compliance pass is claimed. |

F1 candidate SCHURTER3403.0268.23 is250mA/277Vac UMT-H, native0.15A2s **typical** melting I2t at10In. AC05000004709JAC00 is47ohm±5%, body18x7.5mm, not a fusible resistor or replacement forF1. Avoid a hot-NTC inrush assumption by using a fixed resistor for this first candidate; power cycling still requires verification.

A358V constant-source step into maximum18uF through minimum44.65ohm gives8.013A crest,0.804ms time constant,1.152J resistor energy and0.02580A2s (17.2% of the fuse's typical melting number). This is an algebraic comparison, not a guaranteed repeated-pulse/fuse coordination pass. AC05's short single-pulse energy curve was inspected; no precise hot/repetition margin is extracted from its logarithmic curve. Source pulse shape/voltage, fuse minimum/temperature/endurance, body mounting and fault clearing remain to be qualified. MB10S30A8.3ms half-sine and3.74A2s for1–8.3ms are different conditions; do not convert them into an arbitrary-waveform startup guarantee.

Use two499k1206 bleeders in series (998k). Source200V operating limit per resistor; nominal highline sharing179V/64.1mW each, normal tolerance sharing near181V. A shorted member would overstress the other; an open member removes this discharge path. No safe service-time or single-fault discharge approval follows. The primary remains behind a separate cover during panel replacement.

## Output, bias rectifier and thermal proposal

DOUT STTH2R02A200V2A SMA and DAUX STTH1R02A200V SMA are supported by native ST sources. DOUT ideal reverse is127.31V at358V primary/4:1 plus37.861V output; no ringing/surge bound. At illustrative primary0.345A/demag0.425, secondary peak1.38A, average0.293A/RMS0.519A and native conduction estimate0.216W. These are a source-conditioned diagnostic, not a new current-setting specification, measured loss or thermal pass. DAUX ideal reverse is100.60V at35V VDD; actual auxiliary pulse sharing/series impedance remain open.

Both tables specify maximum1V forward at25C under380us,<2% pulse conditions, DOUT2A and DAUX1.5A respectively. Neither establishes a universal low-mA/cold-drop bound for the existing auxiliary/startup assumptions. Recovery limits apply at declared1A,30V,25C ramp conditions, not actual circuit ringing. Exact diode MPNs are candidates; no substituted older drain/OVP result is treated as a fresh integrated fault bound.

NTCS0603E3104FXT is native-verified100k±1%,B25/85=4100K±1%. It replaces generic4250K thermal arithmetic, not a prior selected thermistor. Combined UCC threshold/current limits imply7.2–11.111k trip resistance. Constant-beta sensitivity gives88.12C nominal and80.73–96.76C endpoints, **not a guaranteed fullR/T temperature envelope**. Source-factor selfheat near trip is about0.042K; installed lag/placement is unknown. UCC NTC tied low commands shutdown; open sensor can lose external thermal protection. Independent faults, capacitor/plastic/LED hot spots and acceptable cutoff limits still require engineering verification.

## Startup decision without unavailable PSpice

A separate bounded implementer/root/model_compatibility inspected native timing/state-current references without shared-file edits. The real unknown is integrated charge taken fromCDD before sustained auxiliary takeover. Under the previous stress assumptions,8.013uC is available19→10V, and1.745uC remains for first-three-pulse IC/ancillary draw after the separate ramp/settling/gate budgets. At the25V table condition, a two-state illustration is0.120*T+2.530*R+A<=1.745uC, with elapsedT and cumulativeRUN timeR inms and extraA inuC. No run/wait residency or applicable9–23V current bound is supplied. Do not assign the600–755Hz CV test frequency to startup or setR=0 to manufacture a pass. The existing source remains insufficient to guarantee acquisition; a model qualification gap is not automatically a hardware defect.

RC-BIAS-001,RC-COMP-002,RC-MODEL-001 and RC-CTRL-MODEL-001 remain major/open within their affected acceptance; RC-CLAMP-001 and existing fault/service/thermal/process/specification findings retained. RC-INPUT-001: **open, schematic/protection acceptance** — actual repetitive inrush/fuse/surge coordination, fixed-resistor mounting heat and bulk spectrum/aging/fit still need evidence. Coordinator owns follow-up. This packet selects the next investigation values, not a circuit freeze or proof of recoverable panel faults.

Next concrete work is to complete the remaining charge-path/gate/current-sense/output-discharge/filter/insulation interfaces in circuit-intent.md, resolve startup/drain acceptance and obtain a complete reviewed specification/intended connectivity before generated schematic work. No unavailable simulation or laboratory result is replaced with an invented value. No order, supplier communication, merge or energization occurred.
