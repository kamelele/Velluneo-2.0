# Coupled LED/buffer investigation review record

VEL-LED-BUFFER-01 r1, 2026-11-16. Preliminary specification investigation only. No formal specification approval, selected circuit, human engineering sign-off or physical qualification.

## Frozen evidence

| File | SHA-256 |
|---|---|
| findings.md | ed269b8163fa4c8c20b46338cbfe3da46f44635d9e947ccdd2b84eb1d99f9366 |
| calculate.py | 70d0dd1aca54b41ccd6dd13e26cd6ebcf784ce8c77734ef8630a4b9156010b09 |
| results.json | d15c0a6d260f12fa37bf6042e0a0096fa2916a7a99f8b5a49f369a13afb37af8 |
| sources.json | 182fd1e65aa0e1d115b8120b22985f969e1e553065980ed23d1d2f72a53b7dc6 |

Native reference downloads and hashes are listed in sources.json. They were not added to repository artifacts. All four independent read-only agent contexts inspected this same frozen packet and verified artifact hashes. Execution and source-check scopes differ below; no claim that every role reran the expensive solver is made.

## Actual independent review scopes

| Role / actual context | Evidence checked and recommendation | Open findings / limitations |
|---|---|---|
| Reality Checker /root/spec_reality | Full half-step calculation reproduced results.json exactly; checked diode inverse, energy ODE and small-signal linearization. Native model and PDF sizes/hashes verified; model parameters match source text; local PDF text supports the cited typical voltage/coefficient/DC limit. Ready for preliminary human discussion. | RC-COUP-001 actual controller delivery, regulation, bias/OVP and transients. RC-COUP-002 photometric response and accepted flicker criteria. RC-COUP-003 exclude or independently qualify over-DC-limit/over-model-range cases. Panasonic facts/download origin not independently checked online. |
| Overengineering Reviewer /root/spec_simplicity | Read-only code/results/note/source-register scope, hashes verified; no new unnecessary-complexity or premature-choice finding. Full solver reproduction deliberately assigned to Reality. | OE-LED-01 complete common-condition implementation/process/optical/interface comparison remains open. Priority change does not validate an alternative or reject every LYTSwitch-5 circuit. |
| Completeness Reviewer /root/spec_completeness | 96 saved cases and all representative tables/ranges/convergence figures reconciled. Native source byte counts/hashes and electrical parameters verified. No full solver rerun and no independent PDF-content validation. | Controller coupling, optics, self-heating, fault/access limits and manufacturing remain deferred. No completeness finding for this bounded investigation. |
| Change Reviewer /root/spec_change | Packet r11 preservation; illustrative 5% not adopted; electrical/photometric distinction; artifact/native-source hashes and metadata/parameters checked; saved-result summaries reconciled. No duplicate full solver run. | No new Change finding. Architecture A/common base/simple panels and actual owner authority remain intact. |

## Actual numerical verification

Author and Reality reviewer independently executed `python calculate.py --verify-halved-step`. Results reproduced exactly. There are 96 sensitivity cases; mean-current calibration converged in six iterations with largest final relative error 3.184e-7. Halving 20 us to 10 us changed extrema by no more than 3.84 uA/29.05 uV and electrical modulation by 0.000673 percentage points. Numerical identities and convergence establish consistency of the declared averaged equations, not physical accuracy.

No ngspice executable was available and no SPICE run occurred. Static source parameters are evaluated mathematically at 25 C; temperature shifts are sensitivities rather than a complete SPICE/self-heating solution. Controller dynamics, photometry, faults, protection and physical behavior are unvalidated. The local source-integrity checks do not amount to supplier authenticity or component qualification.

## Engineering priority and retained limitations

Retain the simple sinusoidal-power LYTSwitch-5/output-capacitor case as a comparison; prioritize a primary-buffered isolated CC implementation for the next bounded common-condition assessment. This recommendation follows substantial modeled LED-current variation, not a photometric failure threshold. A 5% electrical example is not a requirement. No replacement controller, capacitor, storage voltage, safe delay or manufacturing route is selected.

The model couples LED current and output-capacitor energy; it does not close RC-DCM-002 because the actual controller/bias/OVP and fault transients remain uncoupled. Prior fault, hot-magnetics, startup, source/process and toolkit/CAD gate findings stay open where recorded.

The additional driver-study/README.md index was separately checked by the Change Reviewer. It maps actual evidence and bounded task/dependency/document ownership; prior technical reviews retain their unchanged scopes. The reviewer requested clarifying document ownership versus the human product owner; the final wording explicitly says investigation coordinator/document owner. Index final SHA-256: ad3b367aa4a173622b59f23de900e1ca3b4ce1b73e270254f597c4cc852e7279.

No human approval is simulated. No CAD, installed-toolkit environment pass, ERC/DRC, supplier communication, order, BOM upload or physical test occurred in this investigation.
