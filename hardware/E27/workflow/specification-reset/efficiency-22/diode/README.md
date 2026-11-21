# EFFICIENCY22 output diode candidate

Selected prototype candidate: **STMicroelectronics STPS2200U, SMB**, replacing
STTH2R02A, SMA. Root owns the source-derived footprint, CAD, BOM and integration;
/root/eco22_diode owns only this documentation subtree. This is a component choice
for verification, not physical qualification or a claim of unchanged performance.
The [source register](source-register.json) binds exact sources, purchase identity,
the saved PDF hash and the retained checks.

## Source-backed comparison

| Property | Existing STTH2R02A | Candidate STPS2200U |
|---|---|---|
| Technology / package | Ultrafast PN / SMA | Schottky / SMB |
| Reverse / average rating | 200V /2A | 200V /2A |
| Maximum junction | 175C | 175C |
| Nonrepetitive10ms surge | 75A | 100A |
| Junction-to-lead | 30K/W | 20K/W |
| Conduction screen | .68Iavg+.06Irms² | .58Iavg+.03Irms² |
| Reverse leakage,125C/200V maximum | 20uA | 2.5mA |

Ratings retain their manufacturer's waveform, temperature and mounting conditions;
they are not interchangeable physical test results. The candidate's2A rating
uses a0.5duty square wave and lead145C. Thermal references are junction-to-lead,
not enclosure thermal resistances. Manufacturer documents:
[STPS2200](https://www.st.com/resource/en/datasheet/stps2200.pdf),
[STTH2R02](https://www.st.com/resource/en/datasheet/stth2r02.pdf).

At the same illustrative .319A average/.564801Arms secondary surrogate, the
formulae give0.236060W versus0.194590W: **41.470mW gross forward-screen reduction**.
However the former formula corresponds to a150C hot forward envelope and the
latter to125C. This is not a matched-temperature IV comparison; it does not prove
actual same-temperature improvement. The effective current triangle is an
accounting surrogate, not a measured winding waveform. Parent comparative results
retain these limitations and do not show a net improvement in every selected hot
case. No large efficiency or all-corner temperature improvement is promised.

Reverse leakage and parasitic capacitance must be included alongside forward loss.
The2.5mA maximum applies at125C/200V; it is not a bound for every operating
temperature, and typical reverse/current-capacitance curves are not guarantees.
Ringing and capacitance changes can reduce or erase the modest conduction benefit.
The existing switching-loss allowance is not proof of the new commutation waveform.

## Package and polarity

Preserve physical pin1K/pin2A and the cathode band. A new SMB module is required.
Root personally inspected Figure10 on source PDF page6 and corrected the initial
text-only dimension transposition: **pad length along the terminal axis1.62mm,
pad width2.18mm, gap2.60mm, center pitch4.22mm, outer span5.84mm**. The earlier
research interpretation1.62x2.60/gap2.18 was wrong and is superseded. This actor
does not claim that visual inspection. Saved source SHA256:
`9cacc9736041440b2980a1fcdb09664dbd00f01018389df2c2b138619eec72ea`.

The SMB body and pad changes require native placement/clearance/courtyard,
polarity, routing/return, solder/paste, schematic/PCB parity and assembly review.
No isolation or other rule is relaxed by choosing a lower-loss component.

## Bias, startup and protection

The candidate retains200V and175C and increases the stated10ms surge capability.
This does not establish actual voltage peaks, full fault coverage or reverse
commutation. The first-order secondary reverse screen is about117V before
ringing; no100V substitute is selected.

Auxiliary bias follows `(Vout+VfD3)*10/18-VfD2`. Lower D3drop reduces VDD and
changes PSR/no-load output offset. The old0.5V lower D3drop assumption cannot be
silently retained. With only nonnegative D3drop,19V output and D2drop<=1V,
the ideal lossless ratio screen is9.5556V against the9.45V healthy goal: only0.1056V margin.
Actual takeover, pulse timing, dropout, cold/hot starts, output absence/shorts and
retry behavior remain required physical checks. Static margin is not a startup
or protection guarantee. Source-conditioned capacitor/current/voltage and existing
C16/C17 safety/process/human holds remain.

## Exact purchase route

[ST's product page](https://www.st.com/en/diodes-and-rectifiers/stps2200.html)
reports active/volume production. The [factory shop for exactSTPS2200U](https://estore.st.com/en/stps2200u-cpn.html)
reports an in-stock indication and quantity1purchase route, snapshot$0.77.
Retrieved21November2026 from a public cached page whose cache was reported
fourweeks old: no live stock guarantee, reservation or purchase occurred.
Exact JLCPCB inventory and external-part assembly acceptance are unconfirmed.
Other makers' similarly namedSTPS2200U-MS parts are not this selection.

No source CAD, other project file, approval, supplier request or physical hardware
was changed by this documentation writer. Root integrates the candidate and fresh
checks, then the four independent roles inspect the final frozen packet.

## E22-REALITY-01 correction - ideal screen only

The9.5556V at19V and10.213V at the selected typical7LEDminimum are ideal
lossless winding-ratio screens with assumedD2drop<=1V, NOT physicalVDDlowerbounds.
R10=4.7ohm pulse drop, winding resistance and VDD ripple remain unbounded. At19V,
only105.6mV remains above9.45V:22.46mA throughR10 alone consumes that allowance.
Averageauxcurrent does not bound the pulse drop. VDD/takeover and physical
no-regression remain unresolved; a waveform or boundedmodel must close them
before treating STPS2200U as a qualified replacement. See ../open-conditions.json.
