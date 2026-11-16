# Driver investigation index and ownership

Updated 2026-11-16. Investigation coordinator/document owner and sole writer: `/root`. Device: Velluneo E27, product reset packet r11. This folder is a specification investigation on `spec/owner-interview-reset-2026-11-14`; no active CAD writer, selected controller or schematic-stage approval exists. The existing historical CAD/main-branch workflow is not reactivated by this index.

## Current engineering recommendation

Prioritize primary-side energy buffering in an isolated constant-current base for a common-condition comparison. Retain the simple sinusoidal-power LYTSwitch-5/output-capacitor option as a comparison. The nonlinear LED/buffer study identifies a material current-modulation risk; it does not establish photometric compliance/failure or validate the proposed alternative. Architecture A and the common enclosed base/simple replaceable panel remain unchanged. No quantitative current/flicker target or part is approved here.

## Evidence map

| Packet / files | Actual scope | Interpretation retained |
|---|---|---|
| VEL-FLYBACK-01 r2: [feasibility.md](feasibility.md), [calculate.py](calculate.py), [results.json](results.json), [review-record.md](review-record.md) | Ideal CrM sampled normal-cycle calculations; transformer/device/auxiliary/OVP sensitivities. | 4 mH comparison is not a selected transformer or a qualified TPS92310 design. |
| VEL-FLYBACK-CTRL-01 r1: [control-and-alternative.md](control-and-alternative.md), [control.py](control.py), [control-results.json](control-results.json), [control-review.md](control-review.md) | Current programming, assumed DC-fed startup, threshold and controller-family comparison. | Isolated-mode hard comparator alone is not qualified magnetics protection; actual startup and reference-specific lower-threshold protection remain open. |
| VEL-FLYBACK-DCM-01 r2: [dcm-feasibility.md](dcm-feasibility.md), [dcm.py](dcm.py), [dcm-results.json](dcm-results.json), [dcm-review.md](dcm-review.md) | Ideal sinusoidal-power DCM witness and separate constant-power storage screen. | Constructed frequency law is not actual IC behavior. Separate capacitor-voltage examples do not bound a completed circuit. |
| VEL-LED-BUFFER-01: [coupled/findings.md](coupled/findings.md), [coupled/calculate.py](coupled/calculate.py), [coupled/results.json](coupled/results.json), [coupled/sources.json](coupled/sources.json), [coupled/review.md](coupled/review.md) | Native-source-pinned static diode law coupled to averaged output storage and ideal slow mean-current calibration. | This is the more relevant electrical ripple investigation; it is not an IC, temperature-feedback or photometric simulation and does not close protection/interface findings. |

Each review record states actual reviewers, file hashes, reproduction and retained scope. None represents human stage approval. Earlier numerical results are preserved as bounded investigations, not combined into a falsely qualified design. Optical counts/current/lifetime assumptions from `../led-study/` remain provisional.

## Bounded task/dependency/ownership index

| ID | Owner | Dependency / next concrete evidence | Current status |
|---|---|---|---|
| DRV-OPTICS | Coordinator; owner/university supplies eventual measurements | Exact LED current/temperature/flux/bin envelope and a proposed quantitative flicker acceptance/test basis. | Open. No fabricated measurements; 5% electrical example is not an accepted metric. |
| DRV-BUFFER | Coordinator, analytical documents only | Compare primary-buffered isolated CC against sinusoidal-power/output storage under the same optical/input/interface requirements; include ripple, stored energy, size and losses. Depends on DRV-OPTICS acceptance basis. | Next priority. Existing models are insufficient for selecting a complete implementation. |
| DRV-CONTROL | Coordinator | Actual controller regulation, timing, startup/auxiliary takeover, bias/OVP and fault/recovery calculations for the preferred buffer strategy. | Open; controller-family comparison remains conditional. |
| DRV-ACCESS | Coordinator; owner reviews proposed behavior | Normal/fault accessible-interface voltage/energy, base shielding, insulation, discharge/cooling and offline replacement contract. Depends on real LED/storage/controller envelope. | Open; no safe voltage or wait time selected. |
| DRV-PROCESS | Coordinator, no supplier communication authorized | Feasible transformer insulation/winding/fit, exact controller/LED sourcing and JLCPCB fabrication/assembly route. Use prepared supplier questionnaire only if communication is later authorized. | Open; no quote, reservation, order, manufacturing-file submission or supplier message. |
| DRV-GATE | Coordinator assembles evidence; owner is stage approver | Complete specification/owned unknowns, current requirement preflight, exact toolkit installation/environment prerequisites and formal packet review. | Not approved. No CAD starts from an agent recommendation or ordinary continue instruction. |

The next comparison should close a bounded buffer/control decision rather than start another broad topology survey. Reviews may recommend preliminary discussion; physical validation and later formal gates remain separate.
