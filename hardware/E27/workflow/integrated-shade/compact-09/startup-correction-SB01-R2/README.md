# SB01 R2 — RC startup correction, not a new PCB

## Concrete result

Replace the 3.3mH choke at physical legacy **L1** with **Vishay
PR02FS0201000KR500,100ohm±10%,2W**. Keep RF1=FW20A47R0JA.
The engineering calculations call the replacement R10; its assembly position
and existing printed reference remain L1. Fit the resistor, not the old choke.
This is a same-board assembly ECO: 51.2x33mm,19positions,46pins,11nets.
No pad, track, via, mask, outline or numerical clearance rule changes are intended.
All actual saved copper/pad/via/outline geometry and membership are independently
equal to R1. The retained eight-file manufacturing ZIP matches R1 byte for byte
and passes an audit against the new native board. Fresh native exports pass too.
No purchase, upload, payment, physical measurement or human approval is recorded.

## Why this correction

The old unloaded linear inputLC model produces conditional706.3/588.7V peaks.
L1 saturation and real controller timing make those unsuitable as hardware bounds.
Increasing RF1 or merely reducing the choke value does not close that uncertainty.
The selected positive RC network instead has an ideal passive voltage invariant:
with input/initial capacitor voltages in0..357.8V and no energy injected by the
load, neither node can exceed that interval. This removes the intentional input
LC resonance; it does not remove parasitic inductance or model the live converter.

512 input-phase/tolerance/retained-charge scenarios confirm that invariant.
The worst calculated first1ms replacement-resistor energy is7.836mJ and its
instantaneous peak1458.93W. A conservative2500W/1ms rectangle read from the exact
PR02-FS manufacturer pulse curve envelopes these room-temperature scenarios.
The simulated1–20ms tail is small. Full hot/repetitive pulse qualification remains
open. See analysis/startup/REPORT.md for scripts, convergence and assumptions.

At an ASSUMED60mArms branch current, the replacement dissipates0.36W nominal,
0.406W in the stated112.75ohm screen; actual RMS is not measured. This adds heat
compared to the choke. At80mArms the same screen gives0.722W. The provisional
resistor body stop is90C. Do not reuse old total-loss/enclosure-temperature claims
as R2 results. The planned upright formed-resistor height is16mm within the
retained19.5mm module envelope. Sample fit, tolerance, lead support and actual
hot clearances remain to be inspected. The 3D model is illustrative.

## Protection assessment and remaining blockers

Keep R4/R7/C6. Static output OVP arithmetic is77.88Vnominal and73.21–82.06V
using25C IC thresholds and1%resistor tolerances only. This is not a dynamic/hot
guarantee. Normal current regulation, short/open-load auto-restart and thermal
functions exist in the selected IC, but their actual board waveforms, current
and hot behavior remain to be measured. Internal thermal shutdown does not
protect every external component.

The275VAC MOV's710V@10A test point leaves only15V to the IC's725V absolute
rating; it is not a universal clamp ceiling. An engineering load-line screen for
a TOTAL instantaneous1kV input differs from a1kV impulse added to the line crest.
Neither is a qualified board surge pass. T1's400V winding rating also requires
checking the simultaneous switch state and winding waveform; an early bus peak
alone does not prove that voltage occurred across T1. No replacement MOV with
guaranteed adequate whole-board dynamic margin was qualified in the same space.

A shorted U1 power switch bypasses its own electronic OVP/current control.
The input fusible parts do not guarantee that the100VC6 survives that failure.
No fail-safe-output or all-fault-survival claim is made. Keep no hot-plug: the
output capacitor stores significant energy and can pulse a reconnected LED.
Surge, MOSFET-short consequences, hot pulse, outputOVP dynamics, temperatures,
EMI and current regulation remain physical qualification gates. AnRC filter
attenuates EMI differently from the oldLC, so no EMC result is inherited.

## Verification / order status

Fresh KiCad10.0.6 ERC/DRC/parity pass; unconnected0. Actual selected MPN check
passes. Independent original-BOM pin graph equals the new schematic:46pins.
Fresh-export and retained-Gerber geometry audits pass. The strict spacing
geometry remains the same five pad pairs plus18escapes, FAIL23; no relaxation
or accepted electrical waiver is installed. Config preview/apply changed only
the two consumer intent/constraint digests, not numeric rules or protected areas.

Full Toolkit release remainsFAIL, with raw product/evidence/approval gates
retained under checks/toolkit. Prior exact-source owner decisions cannot be
transferred to this changed assembly. Four distinct final reviewers must inspect
this frozen packet; they can recommend human review, never approve it themselves.

The original R1 source is backed up locally as SB01_przed_poprawa_rozruchu.zip;
its exact hashes and baseline commit a96ee80a3ab4c8c1b56fa7e9e5b9188beba61c3a
are in provenance/before.json. The canonical branch source remains R1 until an
explicit integration decision following these reviews. This packet contains a
same-board R2 candidate and does not claim a completed release or safe energization.

The coordinator /root owns candidate CAD. Startup/protection contributors wrote
only their analysis directories. Kamil owns fabrication acceptance and any later
supplier action. A qualified physical test owner/setup must be named separately.

## Primary sources

- https://www.vishay.com/docs/28915/pr02fs.pdf
- https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf
- https://www.bourns.com/docs/product-datasheets/fw.pdf
- https://www.we-online.com/components/products/datasheet/7687709152.pdf

Primary PDFs, page renders, acquisition failures and actual calculations are
retained in the analysis handoffs. No supplier stock reservation is implied.
