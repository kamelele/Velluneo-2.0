# SB01 startup engineering handoff — RC correction candidate

Actual contributor: `/root/sb01_startup_engineering`. Date: 24 November 2026.
Coordinator owns every canonical CAD/configuration file; this contributor changed
only this external evidence directory. No implementation or owner approval is claimed.

## Preferred candidate and exact naming

Retain protective RF1 = Bourns FW20A47R0JA, 47 ohm / 2 W. Replace the component
populated in the **legacy L1 position** with **Vishay PR02FS0201000KR500**, 100 ohm,
10%, 2 W, non-inductive flameproof PR02-FS. `R10` in calculation files means this
resistor at the legacy L1 two-pad position. The coordinator intends to retain L1
physical/reference designation for ECO compatibility; the value/MPN/function must
unambiguously say resistor. No pin/net/pad or copper change is needed for this option.
This is an engineering proposal for the existing SB01, not a new PCB or a release.

The filter becomes RF1-C1-R10-C4 (RC–RC) instead of RF1-C1-L1-C4. Removing the
intentional magnetic energy store eliminates the identified input-filter LC mode
and its nonlinear saturation uncertainty. Conducted EMI attenuation changes and
must be remeasured; this is not an EMC-qualified substitution.

## Existing model audit and rejected shortcuts

The prior RK4 equations correctly model the nominated unloaded linear Pi network
with an ideal bridge that blocks reverse input current. Their numerical result is
reproduced: 47 ohm / 3.3 mH / 150 nF gives C1 peak 706.298 V and C4 peak 588.698 V.
They do not model the complete product or bound nonlinear hardware. The original
WE-TI HV 768772332 has typical 10% / 30% saturation indicators 0.27 / 0.39 A, while
the linear model reaches 2.126 A. Its published DCR is typical 5.9 and maximum 7.08
ohm, not a guaranteed minimum. Zero DCR is an explicit low-damping sensitivity.

The 27-group grid in `value-grid.json` records resistor, inductance and C4 variants.
Lowering L or increasing R can make the linear voltage peak look acceptable while
producing 3–7 A in inductors lacking qualified pulse behavior. This does not close
the old uncertainty. The Bourns FW series lists 4.7–100 ohm; its UL1412-recognized
range stops at 47 ohm. A 150 ohm same-series proposal is not supported, and a 100 ohm
part cannot inherit RF1's 47 ohm recognition. FW20A1000JA is listed by Mouser but
non-stocked with 15-week indicated factory lead time; it is not the preferred part.

`targeted.json` includes finite retained-charge and line-phase sensitivities of
series-damping alternatives. These are rejected design exploration, not the RC
candidate and not approved parts or hardware stress ceilings. Initial C1/C4 states
are independent engineering scenarios, not claimed actual histories.

## RC calculation and independent voltage argument

`rc_screen.py` integrates:

    iB = max(0, (u(t)-a)/RF1)
    iR = (a-b)/R10
    da/dt = (iB-iR)/C1
    db/dt = iR/C4

For positive R/C and 0 <= source(t), initial a,b <= Vmax, the region
0 <= a,b <= Vmax is invariant: at a=Vmax the a derivative is non-positive,
and at b=Vmax the b derivative is non-positive. Lower boundary derivatives
point inward. Thus an ideal passive RC ladder cannot amplify input voltage
beyond the largest source or initial capacitor voltage. This argument is
independent of chosen component tolerance values; it is not proof for omitted
parasitic inductance, reverse recovery, external surges or an energy-regenerating
converter/fault. A passive non-negative load can discharge the output of the
ladder but does not create an extra energy source.

The numerical grid contains 512 cases: 207/253 VAC, 50 Hz, connection phases
0/45/90/135 degrees, C1 +/-5%, C4 +/-10%, separate C1/C4 initial charges 0/357.8 V,
RF1 initial +/-5% plus +/-200 ppm/K over 100 K, and PR02-FS initial +/-10% plus
+/-250 ppm/K over 100 K. The latter gives R10 87.75–112.75 ohm. This is an explicit
temperature-sensitivity envelope, not a measured case temperature or full lifetime
guarantee. No controller, MOV or magnetic macromodel is invented.

Results in `rc-screen.json`:

- C1 and C4 stay at/below the nominated initial/source ceiling of 357.8 V.
- Cold-start R10 peak: 214.312 V, 432.558 W, at most 7.073 mJ in the first 1 ms.
- Retained-charge scenarios: R10 peak 357.8 V / 4.0775 A / 1458.927 W; independently
  controlling maximum first-1-ms R10 energy 7.836 mJ.
- RF1 peak current 8.1769 A; maximum first-1-ms RF1 energy 7.668 mJ. These are
  startup scenarios, not fault clearing I-squared-t or fuse interruption proof.
- Reducing RK4 step from 100 ns to 25 ns at the independently controlling corners
  changes R10 and RF1 energy by less than 3e-10 J and the listed controlling peak
  power / C4 voltage by zero at displayed precision. State and power energies use
  consistent RK4-stage integration.
- `rc-tail.json` extends 64 bounding selected resistor/phase/retained-charge cases
  through 20 ms at 200 ns. After the first 1 ms the unloaded R10 maximum is only
  0.035285 W / 1.9946 V. This is not an active-buck steady-state RMS measurement.

## PR02-FS pulse and mechanical comparison

Official PR02-FS document 28915, revision 22-Oct-2024, was downloaded and rendered.
The p5 rectangular-pulse curve is about 3000 W at 1 ms. Deliberately round down
to **2500 W at 1 ms as a graphical engineering comparison**, not a new manufacturer
guarantee. Bounding the full first millisecond by 1458.927 W gives 1.71 ratio to
that rounded curve, covering the simulated pulse without misusing the 1.2/50 us
claim. The numerical tail then falls below rated continuous power. The curve's
standard test conditions are 15–35 C; hot-start/repetition derating is not supplied
as a guaranteed bound and remains a qualification item. A broader 80-ohm R10
sensitivity would give 1600.26 W at the same voltage, still below this comparison.

PR02-FS maximum dimensions: diameter 3.9 mm, body length 10 mm, overall resistor
length L2 12 mm, lead diameter 0.78 +/-0.05 mm. Existing legacy L1 pad centers are
5.0038 mm apart, 1.2 mm drills. A vertical body centered on pad 1 reaches at most
4.4519 mm from the old footprint origin; its existing courtyard radius is 4.65 mm.
The return wire at pad 2 reaches 2.9169 mm including maximum wire radius. These
nominal projections fit the old courtyard; the approximately 0.1981 mm body margin
does not absorb an unspecified manual placement tolerance. Proposed assembly:
2 mm body standoff, free lead forming with no stressed body seals, total height
reservation at least 16 mm including top bend. This is a fit plan, not a measured
sample fit or a manufacturer-approved bend process. Root must check adjacent
bodies and 3D lead paths and reserve the formed height in the candidate.

The PR02-FS datasheet's insulation proof test is not a working-voltage specification
or a system insulation rating. Its nominal power is 2 W at 70 C with derating to
200 C. The selected part's safety recognition does not certify the assembled board.

## Normal loss and remaining electrical work

R10 loss is I_RMS^2 times resistance. At the stated high R10 sensitivity of112.75
ohm: 40 mA -> 0.1804 W; 50 mA -> 0.2819 W; 60 mA -> 0.4059 W; 80 mA -> 0.7216 W.
RF1 adds 0.1812 W at 60 mA under its high resistance sensitivity. These are
conditional losses. The buck's actual RMS input current, distortion and waveform
after removing L1 remain unmeasured. Do not infer efficiency or body temperature
from output current or the unloaded transient. PR02-FS has no quoted Rth here;
borrowing standard PR02's thermal resistance would be an unqualified analogy.

The same-board candidate addresses the identified intended-filter startup mechanism.
It does not close input MOV clamp/1kV surge coordination, RF1 interruption, MOSFET
short failure, diode-open behavior, output open-load timing, LED hot-plug, thermal
limits, EMC or finished-board insulation. The protection contributor owns those
analyses. In particular do not infer an actual T1 winding stress equal to the old
588.7 V peak without simultaneous MOSFET/BP-startup timing; the old filter model
does not include BP charging. Neither absence nor presence of that actual waveform
has been established. No powered test has been performed.

## Primary references and retrieval

- [WE 768772332](https://www.we-online.com/components/products/datasheet/768772332.pdf),
  current official p1 ratings; [768772331](https://www.we-online.com/components/products/datasheet/768772331.pdf)
  is an explored, unselected same-package alternative.
- [Bourns FW](https://www.bourns.com/docs/product-datasheets/fw.pdf), p1 range,
  recognition and dimensions, p3 impulse/fusing plots.
- [Vishay PR02-FS](https://www.vishay.com/docs/28915/pr02fs.pdf), p1 ratings, p5
  rectangular pulse and test conditions, p7 physical dimensions. Native PDF and
  inspected renders are beside this report. Direct default-UA retrieval returned
  403; a Mozilla/5.0 request with approved network execution succeeded.
- [PI LYTSwitch-1](https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf),
  input-filter/EMI guidance is not qualification of this changed filter.
- [Mouser FW20A1000JA listing](https://www.mouser.com/en/ProductDetail/Bourns/FW20A1000JA?qs=HVbQlW5zcXXrXB1JMlEdqw%3D%3D)
  indicated non-stocked/15 weeks on the retrieved listing. The stockable FS option's
  sourcing evidence is owned by the protection contributor/coordinator; no order
  or stock reservation has been made.

Read `handoff.json` for input and output SHA256 bindings. Calculation files use
R10 as the functional name; the retained designator map is R10 -> legacy L1 slot.
