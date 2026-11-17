# Active31-position startup and protection obligations

Design contract from actual TI source behavior and retained project criteria; not a test execution record. Root owns full integration and any ECO. No new electrical threshold is called a standard or a human-approved product decision.

## Controller state and recovery

- **HV charge:** internal HV startup source charges CDD until the native19-23V turn-on threshold. Its100/250/500uA table values are tested at VHV100V/VDD0V, while ISTART is tested at VDD18V. They do not specify a constant charging current over the whole trajectory. Existing fixed-current charging times remain sensitivities; do not add external permanent HV-to-VDD resistors merely to force that calculation to pass. Such injection can prevent a fault's UVLO reset, as SLUAAC5 warns.
- **Enabled/startup:** first three current-limited pulses and subsequent CC charging must maintain VDD above the9V recommended floor, with existing10V design reserve, and avoid VS/CS false-faults. The new coupled diagnostic supplies one declared behavioral witness. Actual AC10-40C/207-253Vac/49-51Hz turn-on within1s remains a full-system verification obligation.
- **Normal panel:** current/voltage domain, intended flux and all-corner thermal budget must hold together. Auxiliary charge must cover base draw plus gate charge without trough below the accepted reserve or crest beyond35V. No LED lifetime/flux claim follows from this model.
- **Missing/open panel:** normal operation is CV regulation, not an assertion of continuous OVP cycling. Both20k bleeders are part of the minimum-load energy balance. Output peak, ripple, VDD stability, component temperature and continuous no-panel behavior require the agreed envelope; do not call the illustrative40V an approved/contact-safety limit.
- **Output short:** a low ideal auxiliary winding voltage supports a bias-collapse mechanism, but leakage pickup/parasitics and lack of an IRUN minimum prevent that algebra from proving the real retry train. Bound cycle energy/peak/current, reset and repeated fault heating. No damage/no fuse or manual reset/offline replacement recovery are retained requirements. Test continuous fault thermal behavior and repeated recovery later with actual hardware/setup authorization.
- **OVP/OCP/VS faults:** native source stops switching, enters fault current and discharges VDD to UVLO-off before startup returns. OVP table endpoints are25C;1.6V/RCS is a static backup-threshold illustration, not a maximum dynamic fault current. Gate/blanking/propagation, core saturation and layout spikes must be included in actual stress limits.

## NTC and thermal tracking

The active RT1 direct-to-primary-ground arrangement shuts down when NTC falls below the0.9-1V threshold. Threshold/source-current tolerance alone makes the electrical trip resistance range7200-11111.11ohm. The exact native Vishay SMD1 R/T/tolerance formula with TI electrical endpoints gives80.8002-96.5712C (outward0.1C screen80.8-96.6C). The beta-only result80.7269-96.7609C is a comparison. TI endpoints retain their VDD25V test condition; actual assembled trip still requires bias/attachment/thermal validation.

NTC short forces the shutdown input low. NTC open removes that external thermal channel; no high-resistance fault detector is specified. A passive resistor simply placed across the same NTC cannot make open fail-low while leaving every healthy state high: healthy parallel resistance is always less than the open-sensor parallel resistance. A new active/window or independent thermal channel would need its own exact part/source/graph ECO; it is not silently assumed present.

The root's updated normal design target for this iteration is local air/sensor no higher than68C, not a measured temperature. That leaves12.8002K before the earliest full-curve electrical trip. Using the latest electrical trip, the remaining hotspot-minus-sensor budget is8.4288K to105C,13.4288K to110C and28.4288K to125C. These must include spatial gradient, ramp lag, R/T-model uncertainty and any source/assembly tolerance; they are not allowable generic material temperatures. The root assigns component-specific limits/life targets separately.

Vishay's current29056 sheet lists tau<4s and reference dissipation3mW/K. Neither establishes the assembled hotspot-to-sensor transfer function. A first-order4s screening model under a steady ramp adds approximately4*a K lag for a K/s ramp;0.5K/s adds2K and1K/s adds4K. Near-trip sensor self-heating is at most0.125mW, about0.0417K only if the reference dissipation factor applies. Do not use old8s or the internal165C typical controller shutdown as guaranteed whole-product protection.

**Open-sensor acceptance:** demonstrate passive thermal safety under declared normal and relevant fault power even with external NTC action absent. If that cannot be supported, prepare a concrete independent backup-thermal ECO before treating R-THERMAL/U08 as resolved. No such passive proof or finished backup implementation is claimed by this subtask.

## Source-off discharge and service

Reset/discharge clocks start only after all relevant bias injection or bulk-to-secondary energy transfer has stopped. R13 supplies a passive VDD discharge path, but an isolated VDD/output RC formula does not establish complete-lamp service wait. Retain the source-off condition, primary stored energy, removed-panel energy and cooling/access criteria. The separate primary cover remains necessary; a temperature sensor or low output voltage does not qualify primary insulation.

## Observable closure conditions

For schematic-stage design review: independent numerical/source inspection of this coupled model; bounded VDD trough/crest and sampling/gate assumptions tied to a concrete source-valid operating domain; root component/thermal budgets including NTC-open behavior; defined circuit changes if a bound fails. For later physical validation: record real board/transformer/panel/enclosure revisions, line/ambient/orientation corners, actual safe fixture/personnel/instruments, VDD/VS/CS/drain/output waveforms, hotspot/sensor temperatures and fault/recovery outcomes. Do not execute energized tests or invent measurements here.
