# Controller simulation access and fixture qualification

VEL-CTRL-EVIDENCE-01 r1,2026-11-16. Specification investigation. Archive inspection only; no new controller or converter simulation. Productr11 and architecture A remain unchanged. Existing electrical majors block affected circuit acceptance.

## Actual source findings

Official UCC28711 product resources link family PSpice SLUM464 and TINA SLUM538 downloads. Download labels do not prove exact variant or model coverage. Pinned archives were inspected without decryption or edits; audit.py reproduces the findings.

| Resource or fixture feature | Actual inspection | Engineering consequence |
|---|---|---|
| SLUM464 model | Public interface declares UCC28710, PSpice16.2, dated2015; body encrypted. CBC behavior explicitly omitted. | It is not an established exact UCC28711 model. Do not relabel its CBC terminal as NTC or claim temperature/fault equivalence. |
| SLUM538 | Encrypted LIB in a UCC28710-named model directory. | No readable implementation or compatible execution established in current environment. Directory name alone does not establish every internal feature. |
| PSpice reference bias | Auxiliary-independent source ramps toward25V in600us through a diode;330nF VDD capacitor. | This source can sustain bias when VDD is below it. It masks or changes bootstrap demand; unsuitable as an unmodified self-supply proof. |
| PSpice power stage | Voltage-controlled ideal switch;135V source ramp;1120uF output;200ohm load;121k/30.1k divider. | Omits physical MOSFET gate charge/switching capacitance and is not the proposed bulb circuit. Neither Qg nor node-charge budget can be qualified by this switch. |
| Bundled reference output | TR.out includes aborted-job status. Stored TR.dat also exists. | This is an old supplied result, not our execution, and not a golden successful run. Last valid time and stored waveforms were not decoded or validated. |

The device datasheet distinguishes UCC28710 cable compensation from UCC28711 NTC shutdown and fixed compensation. Even if common startup logic is plausible, equivalence requires documented scope and checks; it cannot be inferred from a family download or matching terminal count. Internal supply-current fidelity is not established from an encrypted interface. The old reference's numerical tolerances are not adopted as our accuracy acceptance.

## Available execution and owner response

Current accessible runtime is Linux with shared ngspice44.2. PSpice executable and Wine were not found in PATH; no compatible PSpice/TINA runtime or license was established. Encrypted libraries were not submitted to ngspice as if they were supported. No remote desktop/session on the owner's Windows computer is established by running this assistant in a desktop browser.

Owner answered in this conversation on2026-11-16 that PSpice/PSpice for TI/TINA-TI is not yet available. This is an access/setup fact, not permission to register an account, accept license terms, contact TI, purchase software or execute hardware tests. Official TI offers PSpice for TI and its installation flow requires requesting access then downloading/installing. The owner's own computer is a possible execution route, not a verified installation. No claim that this old model package executes successfully in the current PSpice for TI release.

## Concrete next work

1. Establish a supported runtime on an available computer. Use the official TI request/download route. Record actual version, successful launch and archive identities. User handles account registration/license acceptance; no credentials shared here.
2. Run an isolated, unmodified vendor project as a compatibility diagnostic. Record both success or failure and compare its actual completed interval against10ms. A vendor fixture result is not Velluneo validation. Do not silently alter convergence tolerances to obtain a pass.
3. Establish model scope for exact UCC28711 and actual supply current. A qualified vendor model/clarification is one route; declared hardware measurements are another. No supplier message is sent. Do not choose another controller simply to evade this evidence gap.
4. Only after scope is justified, adapt a separate simulation fixture using run-plan.md. Retain original source, tag modifications and carry the actual MOSFET-model limitation. A component approximation may support sensitivity work but cannot close physical gate-charge or switching-loss limits.

RC-CTRL-MODEL-001: **Major/open for actual controller-model acceptance**, coordinator-owned. Exact-variant coverage, current fidelity and executable runtime are not established; provided reference masks bootstrap and omits real MOSFET behavior. This links RC-BIAS-001/RC-CLAMP-001 rather than replacing them. RC-MODEL-001 and RC-COMP-002 remain major/open in their affected scope. Existing historical protection, service, thermal, optical, process and specification findings remain open. This packet establishes the actual next dependency rather than a working-driver claim.
