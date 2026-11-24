# SB01 protection audit and bounded RC correction proposal

Actual contributor: `/root/sb01_protection_engineering`, 24 November 2026.
This is an implementer handoff, not independent acceptance. No canonical CAD,
netlist, BOM, rules, Gerbers or main/branch ref was changed by this contributor.
Root retains sole CAD ownership. Base: SB01 R1 PCB SHA256
`532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.

## Recommended bounded change

Support the coordinator's proposal to replace the 3.3 mH input choke L1 with a
100 ohm pulse-rated, flameproof resistor R10, preserving its two network nodes and
using the existing board outline. Keep RF1 = FW20A47R0JA. This removes the input
LC energy-exchange mechanism and the uncharacterized saturated L1 from normal
startup. It does not turn the circuit into an isolated supply or prove EMC.

The preferred concrete R10 candidate is **Vishay PR02FS0201000KR500**, 100 ohm,
10%, 2 W. Its family is non-inductive, flameproof and fusible, with explicit
UL1412 recognition. The axial body is at most3.9x10mm; total end-cap/coated
length L2 is at most12mm, and lead diameter is0.78+/-0.05mm. The part-number
format identifies this exact resistance/tolerance/reel version. The published
pulse and rectangular-overload curves govern the pulse check, not a generic2W
label. Primary: https://www.vishay.com/docs/28915/pr02fs.pdf
(22-Oct-2024, pp1/2/4/5/7). The currently indexed authorized Mouser listing shows
MOQ1 and stock, not a reservation:
https://www.mouser.fr/fr/ProductDetail/Vishay-BC-Components/PR02FS0201000KR500?qs=AQlKX63v8RuN%252B6CXgugdTw%3D%3D .

This is not a mechanically qualified drop-in. The existing L1 hole pitch is 5 mm;
an axial part needs deliberately formed/supportable leads and revised body/height
reservation, then new placement/clearance checks. Do not assume the original
9.5 mm choke-height reservation covers an upright resistor. Do not bend leads
flush to the coating or substitute the radial packaging's tape pitch for PCB fit.

A plain **PR02000201000JA100** is a different Vishay PR02 product, currently
catalogued at TME, but its pulse/fusing data are not PR02-FS data. Do not silently
substitute it. Bourns **FW20A1000JA** is another real 100-ohm family member; its
6 x 12 mm body is larger and current availability is poor. Bourns' official FW
datasheet distinguishes the overall 4.7–100 ohm family from the 4.7–47 ohm
UL1412-recognized range. Thus increasing RF1 beyond 47 ohm cannot inherit its
current recognition. Using a second resistor leaves the recognized RF1 intact.
Primary: https://www.bourns.com/docs/product-datasheets/fw.pdf , Rev10/26,
pp1–3. The local primary PDF's page3 curves were visually inspected.

At the existing assumed 60 mArms planning current, R10 dissipates 0.36 W
nominally and 0.416 W in the explicitly chosen 10%/75K-TCR/3%-change screen.
The nominal increment relative to the removed choke's 7.08-ohm DCR is 0.335 W.
Neither 60 mA nor resistor-body temperature is a measured upper bound. Preserve
the 100C body planning target, spacing from C6, and actual thermal measurement
gate. A passive cold-charge energy screen for maximum C4 is 10.56 mJ; this is
not the complete surge, repetition-life or fault-clearing energy.

The official PDF was acquired after a read-only network escalation and its
page5 rectangular-pulse curve was visually inspected: approximately3000W at1ms,
and5000W at0.1ms. These are graphical approximate readings, not exact guaranteed
numeric table limits. A normal-event peak below1.5kW settling within1ms can
therefore fit a conservative room-temperature rectangular envelope; retain the
full simulated tail/energy and pulse-repetition record. The stated general
test temperature is15–35C; no hot-body pulse derating curve is supplied, so this
does not alone close an initial100C-body hot-restart case. Physical verification
or manufacturer confirmation remains necessary for that assertion.

## Protection facts and their scope

The PI datasheet specifies 725 V D–S, 25C input-OVP threshold 0.9–1.1 mA,
25C output-OVP threshold 2.3–2.48 V and LYT1603D fault current limit
1.06–1.24 A at its stated ramp. Foldback starts at characterized 138–152C
junction; typical thermal shutdown is 160C. These functions inhibit switching,
not disconnect a shorted MOSFET. PI's checklist requires actual startup/fault
VDS/current and thermal checks. BP charging creates startup delay; do not
assume an early unloaded rail peak coincides with MOSFET ON.
Primary: https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf
RevB, pp2–4,6–9.

Own divider arithmetic gives 77.88 V nominal output OVP, or 73.21–82.06 V
using only 25C IC limits and 1% resistor tolerances, with no diode-drop credit.
This supports retaining R4/R7/C6 for the intended 52–68 V LED window; arbitrary
OVP retuning is not recommended. The existing wider resistor-temperature/aging
screen reaches 86.51 V, but neither screen bounds full-temperature IC drift or
dynamic overshoot. The 100 V C6 rating must not be described as a clamp.

T1 **7687709152** has 400 V working voltage, 0.52 Arms rating and a *typical*
0.8 A point for 10% inductance reduction. That is not a guaranteed hot fault
current. Its original replacement therefore needs normal-startup voltage,
current and heat verification, not merely a favorable 725 V MOSFET comparison.
Primary: https://www.we-online.com/components/products/datasheet/7687709152.pdf
p1 (2019-05-06). The existing no-load LC C4 peak of 588.7 V was a conditional
T1 concern only: without driver-enable timing it does not establish actual
simultaneous 588.7 V winding stress. Removing L1 addresses that mechanism.

Original L1 **768772332** has typical 5.9 ohm/max7.08 ohm DCR, typical
0.27 A/0.39 A at 10%/30% inductance reduction and 400 V working voltage.
The prior >2 A linear screen operates well beyond those typical magnetic
points. Replacing it avoids having to invent a saturation curve or guaranteed
minimum hot inductance. Primary:
https://www.we-online.com/components/products/datasheet/768772332.pdf
p1, Rev006.001 2025-06-06.

## Surge: the remaining real boundary

RV1 **B72207S0271K101** remains a 275 VAC MOV, 710 V maximum clamp at
10 A, 21 J single specified energy condition. A 710 V table point leaves
only 15 V to the IC absolute rating. It is not a universal ceiling; lead
inductance, dynamic response, current, repetition and aging matter. The
7 mm series has no built-in thermal disconnect. A slow abnormal overvoltage
can heat a MOV without instantly clearing RF1. Primary:
https://www.tdk-electronics.tdk.com/inf/70/db/var/SIOV_Leaded_StandarD.pdf
pp1/10/11 and
https://product.tdk.com/en/techlibrary/productoverview/benefit-thermofuse-varistor.html .

Do not lower RV1 to a 250 VAC MOV: the declared input reaches 253 VAC.
A larger 275 VAC MOV can improve energy/current headroom, but cannot inherit
the current body reservation, and the same 710 V clamp class does not prove
the 400 V working-voltage winding survives an input surge. No qualified
same-body, lower-clamp 275 VAC substitution was established in this audit.
Retaining RV1 with a declared physical surge gate is more honest than an
unsubstantiated substitution.

For orientation only, monotonic quasi-static MOV behavior plus RF1min44.65ohm
supports a 710 V node bound when the *total instantaneous source* is at most
710 + 10*44.65 = 1156.5 V, ignoring parasitics. A 1 kV impulse *added* to a
357.8 V mains crest exceeds that condition. This algebra is not an IEC surge
test, complete load-line simulation or an allowed powered-test procedure.
The proposed R10–C4 time constant, about 12.15–18.15 us before RF1/C1,
also does not guarantee C4 stays below 400 V during a roughly 50 us surge.
U1 OVP inhibit timing and T1 transient dielectric behavior remain unproved.

## Fault and reconnect map

- **Healthy open LED:** divider OVP should inhibit switching. Retain the
  measured-output target <=90 V; do not mark it passed from the static formula.
- **Healthy output short:** M-pin undervoltage/current-limit restart is expected.
  C6's first discharge bypasses the controller's current limit. The 1.24 A IC
  table point exceeds T1's typical 0.8 A magnetic point; hot saturation and
  actual peak current need verification.
- **R5 open / R6 open:** nominal regulation arithmetic becomes about21.2/114.0mA
  total respectively. These are circuit expectations, not fault measurements.
  A shorted sense resistor defeats the regulation equation; rely neither on
  normal current nor typical inductance for that fault.
- **R7 open:** the output-sensing path is lost; automatic detection cannot be
  assumed to provide the same open-load OVP. R4/R7/M/FB and D1 faults require
  actual state/waveform analysis or bench evidence.
- **U1 D–S short with LED absent:** internal OVP cannot remove the short. C6
  can charge toward the rectified line (357.8 V ideal crest), far above100V.
  RF1 can limit/clear some faults, but does not guarantee capacitor survival
  or safe venting. With147ohm total resistance and180uF, the simple charge
  time constant is26.46ms; ordinary fuse timing is not an output crowbar.
- **MOV open/short/degradation:** open removes surge protection; a hard short
  stresses RF1; low-current degradation can overheat RV1. Neither a 21J label
  nor a resistor pulse-energy integral proves coordinated safe clearing.
- **D1 open/short or T1 short:** switching-node overstress/current can precede
  any slow input clearing. Do not infer survival from the nominal current.
- **Overtemperature:** U1 senses its own junction. It does not directly sense
  the output capacitor, R10 or T1. Its145C foldback cannot enforce the existing
  85/90/100C component-body planning targets. No enclosure temperature pass.
- **LED reconnect:** no hot plug. C6max stores0.324J at60V and0.729J at90V.
  Peak reconnect current is not bounded without actual ESR/ESL, wiring and
  LED I–V data. The dual68k bleeders dissipate0.106W total at60V. The retained
  one-open conservative90-to5V delay is36.45s; time alone is not a discharge
  measurement. Disconnected/verified discharged replacement remains required.

MB10S-13 and US1M-13-F both have1000V reverse ratings; this supports retaining
them under normal bounded RC input operation. It does not rate external PCB
clearances or prove actual pulse/recovery/temperature survival. Primary:
https://www.diodes.com/datasheet/download/MB10S.pdf and
https://www.diodes.com/datasheet/download/US1M.pdf .

## Handoff and closure criteria

Prioritize a normal207–253VAC startup/restart prototype over blanket fault
survival claims. Integrate R10 only after exact connectivity/part/physical
reservation review. Root must refresh intent/basis metadata, schematic/PCB
parity and affected evidence; changed materials invalidate prior approvals.
No new PCB outline or controller is proposed. The wiring-interface rule remains
de-energized LED exchange. Keep strict spacing FAIL23 visible.

Before calling the populated prototype electrically ready: independently review
the RC startup screen and pulse curves, obtain a competent lab test plan with
current-limited first-power setup and explicit stop limits, and measure startup,
hot restart, load current/ripple, D–S/freewheel/winding voltage and component
temperatures. Surge and abnormal-fault qualification remain separate. A bare
test article may be recommended with those boundaries; reliability or safety
of an energized finished lamp is not established here.

`protection-calculations.json` is reproducible own arithmetic. The complete
current source guard is included there. `primary-acquisition.json` truthfully
records initial blocked shell-download attempts. A subsequent authorized,
read-only network escalation successfully acquired `PR02FS-primary.pdf`, SHA256
`048a69c3c55dd3be3830586620d25cab23bcde74f2f6696fbd9807a84a512874`.
Pages5/7 were rendered and visually checked. Other official documents were read
through the web tool and previously stored primary PDFs where available. No
failed download is labelled as retained full-document evidence. No physical test,
stock reservation, supplier communication or acceptance was performed.
