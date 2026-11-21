# Startup and protection — coupled branch diagnostic and fault contract

PCB-READINESS-01. Implementer /root/readiness_startup; base b1117ae2caecc037d9fc1253bd9c3a3c4effaaf2. Exclusive startup-protection directory only. No shared CAD, approved graph, part value, pin type, profile, requirement or approval changed. This deliverable adds actual calculations and an executed behavioral trajectory, not a native UCC28711 model, physical measurement or finding self-closure.

## Decisions supported by this work

**Retain R10/RAUX4.7ohm.** The new circuit-derived auxiliary charging calculation does not support reducing it merely to escape an assumed2% flat charging window. The retained active value yields a worst modeled VDD trough11.683899V across64 declared active-value endpoint cases, compared with the existing10V engineering reserve. A matched2.2ohm sensitivity improves that trough by only12.9mV. This is a bounded circuit-physics witness, not a guarantee of the real controller's startup behavior.

**Retain RT1 and impose an explicit thermal tracking contract rather than silently substitute a lower resistance.** The active100k/4100 thermistor has a nominal calculated trip88.0602C using the exact primary Vishay tool's full R/T curve. Its native SMD1 tolerance algorithm combined with TI electrical endpoints gives80.8002-96.5712C (outward0.1C screen80.8-96.6C). The older constant-beta80.7269-96.7609C calculation remains a labelled comparison, not the current full-curve result. No68k/47k replacement is selected.

**Do not infer open-sensor protection from the NTC input or the internal165C typical shutdown.** Direct NTC-to-ground open circuit removes this external thermal protection. Either the root's passive thermal design must remain safe without it under the applicable continuous/fault conditions, or a separately reviewed backup protection ECO is required. No unavoidable unsafe component temperature has been proven by this subtask, so no new backup part/graph is silently selected.

## Source identities and conditions

Four complete primary PDF byte identities are recorded in sources.json: TI SLUSB86C/UCC28711, SLUAAC5, SLUA783 and current Vishay29056 revision29-Sep-2026. Available TI hashes match the prior reviewed source register. Vendor originals remain external, not redistributed. Relevant numerical facts: TI NTC threshold0.9-1.0V, pull-up current90-125uA; VDD-on19-23V, VDD-off7.7-8.5V; recommended VDD9-35V; normal peak CS0.738-0.810V, minimum CS0.175-0.215V, source maximum-frequency92-106kHz. These retain their actual test conditions. The OVP threshold table is25C; it is not automatically a whole-temperature output ceiling. TI NTC table endpoints retain the declared VDD25V test condition; this is a source-derived electrical design interval, not a measured guarantee of the assembled sensor at every bias voltage.

The detailed NTC prose in SLUSB86C p12 has a family/pin copy error (it names UCC28701/pin1). The authoritative UCC28711 pin table and diagram use **pin3**, preserved in the approved graph. Do not migrate the NTC net to pin1. Native absolute NTC voltage is5V; cold/open current-source compliance or clamp voltage is not separately guaranteed. Applying100k x105uA as an unrestricted10.5V pin-voltage prediction is invalid. The near-trip0.9-1V calculations do not require that cold compliance assumption.

The diode forward voltages used in the trajectory are **declared sensitivities**, not new cold-temperature guarantees: output0/1.7V, auxiliary1/1.2V. The0V output screen avoids an unsupported positive minimum. The upper values do not replace source-conditioned diode curves at actual current and temperature. No new ST PDF byte verification is claimed here when that external download is unavailable.

## Executed coupled-winding model

Each off interval solves nonnegative diode-branch conduction and ampere-turn KCL:

    J = Nps*Im = Is + Nas*Ia
    Esec = Vo + VFout + Is*Rs
    Nas*Esec = VDD + VFaux + Ia*(Ra + RAUX)

Equalities apply to conducting branches; an inactive diode carries zero current. Stored magnetizing energy supplies the two actual capacitor/load branches. Integrating in descending magnetizing current permits an event at full demagnetization without commanding another pulse while residual current remains. Output-capacitor current and VDD charging current are computed simultaneously; auxiliary duty is an output, not a chosen rectangular fraction.

Retained proposed hot copper resistances are Rp7.225860, Ra1.405578 and Rs0.705633ohm at125C/60mmMLT. They are construction budgets from the prior winding proposal, not measured impedances. On-state MOS32ohm is a sensitivity. VDD base draw3.5mA,16nC instantaneous gate charge, retained R13min979kohm, CDDmin0.890321uF, seven warm-shifted typical LEDs and their old diode equation remain explicit hypotheses. No extra0.85 multiplier is applied after separately calculating auxiliary/copper energy; that would double-count part of TI's transformer-efficiency term. Omitted core/leakage losses are not thereby validated or set to a guaranteed zero.

The first three pulses use source minimum-CS endpoints0.175/0.215V and are allowed to finish demagnetizing plus2.55us dead time. Subsequent pulses use a **constructed** Dmag=.318/.810 actuator, with period at least ton+tdemag+2.55us and1/106kHz. This actuator is motivated by CC charge balance; it is not a reverse-engineered, executed or validated TI state machine. Native VS/CS sampling, line compensation, blanking, propagation, Miller/Coss, valley selection, fault handling and internal RUN/WAIT changes remain outside the model. In particular, no first-three cadence of3/fmax is asserted.

The auxiliary VS-divider current is also omitted from the two rectifier-branch model, not silently called zero in the actual circuit. At a declared raw-aux35V screen and minimum (80.6k+17.4k)*.979=95942ohm, it is at most0.365mA, corresponding to about0.513mV additional hot auxiliary winding drop and12.77mW divider dissipation. These are conditional omission diagnostics, not an independently proven bound on the complete trajectory's error. Real clamp/sampling/parasitic validation remains necessary.

The64 active4.7ohm endpoint cases vary Cout12/20.592uF, bus240/357.796V, first3CS0.175/0.215V, additional initial wait0/300us, VFout0/1.7V and VFaux1/1.2V. They use Lp+10%/RCS+2.1%. The bus is a held starting condition, not an AC cold-start simulation. The seven-LED typical load is a stress hypothesis, not finalized panel acceptance or calibrated flux. Case65 is only a matched2.2ohm comparison at the worst active-value configuration.

Both80 and160 integration subdivisions per off interval were actually executed. Verification checks65 matched cases, maximum KCL error below1e-9A, per-pulse off-energy residual below1e-8J, and refined VDD differences below1mV. Actual differences are about6.745uV; worst fine-grid off-energy residual is about2.34pJ. This numerical agreement verifies the implemented equations at the declared endpoints, not native-controller fidelity or every interior corner. Each run stops after approximately6ms or a modeled screen failure; its duration starts at the enabled19V VDD state. It does not establish the owner's1s AC turn-on criterion.

## VDD crest and fault contract

In the ideal coupled model a passive charging branch cannot charge VDD above Nas*(Vo+VFout+Nps*Ip*Rs). With the declared VFout1.7V sensitivity, Vo40V and a backup-CS static current proxy1.6V/(2.37*.979), this gives32.0073V, leaving approximately2.993V to the35V recommended limit. These are conditional electrical budgets;40V remains the earlier illustrative/unapproved goal, and the backup-CS quotient is not a dynamic fault-current bound. Leakage pickup, diode recovery, layout ringing, actual OVP sampling/stop latency and saturation can invalidate that ideal ceiling. The record quantifies allowable extra charge/energy to35V instead of calling the crest safe. No internal35V VDD clamp is specified for UCC28711; the UCC2891x clamp mentioned in SLUA783 is a different device family.

The reviewed fault-state obligations are in fault-contract.md. Existing RC-BIAS-001/RC-PROT-001/model/thermal/interface findings remain at their affected gates. This subtask supplies a concrete replacement for one arbitrary charging-window hypothesis and explicit NTC/open-sensor conditions; it does not close full startup/protection acceptance.

## Replay and deliverables

Run from repository root with Python3.11+ standard library:

    python hardware/E27/workflow/specification-reset/pcb-readiness-01/startup-protection/calculate.py --source-dir /absolute/native/pdf/directory --steps 80
    python hardware/E27/workflow/specification-reset/pcb-readiness-01/startup-protection/calculate.py --source-dir /absolute/native/pdf/directory --steps 160
    python hardware/E27/workflow/specification-reset/pcb-readiness-01/startup-protection/ntc_curve.py --source-dir /absolute/native/source/directory
    python hardware/E27/workflow/specification-reset/pcb-readiness-01/startup-protection/verify.py

results-80.json/results-160.json retain all65 compact numeric summaries; worst-trajectory-*.json retain actual sampled worst-case traces (first3/every10th pulse), not fabricated measurements or a claimed full analog waveform. Intermediate per-step arrays are generated by the saved equations, not measurement inputs. run-*.log are actual stdout records. sources.json and verification.json bind sources/results. All output files stay below the previously encountered large-publication payload threshold.

## Native R/T follow-up

The official Vishay NTC calculator page, its linked calculator JavaScript and exact-part read-only API JSON were retrieved by root and inspected offline. ntc-native-curve.json records their complete byte hashes, exact URLs, numeric coefficients and independently implemented formula. The primary API identifies exactNTCS0603E3104FXT, curve38, SMD1, R25=100000ohm/1%, B25/85=4100K. The polynomial is normalized at25C; reconstructing B25/85 gives4099.999999995K. The SMD1 tolerance algorithm adds a second term above85C, so a single constant-beta/tolerance formula is not substituted for it. Vendor HTML/JavaScript are external inputs and are not redistributed or executed.

Full-curve latest electrical trip96.5712C leaves8.4288K to105C,13.4288K to110C and28.4288K to125C before assembly gradient/lag/error. Root's later68C normal-node target leaves12.8002K to the earliest electrical trip. These replace the beta-only gradient examples numerically, without changing the actual NTC or establishing assembled temperature compliance. Source-current/voltage test conditions, sensor lag, attachment and actual thermal loads remain explicit integration obligations.
