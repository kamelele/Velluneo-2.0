# SC07 independent Completeness/electrical evidence audit

Read-only SC06 sources; only this research directory written. No stage acceptance or engineering approval.

## Executed work
- Re-read pinned completeness role, SC06 original 17 requirements, active BOM, pin graph, native capture/checks and source calculations. Earlier capture review verified all 100 pins independently.
- Opened manufacturer LYTSwitch-0, AN60, Samsung C4, TE RF1, ProTek TVS and PI Expert support sources; visually inspected local datasheet p10/p13 current-limit tables/curves.
- audit_calculations.py reproduces nominal own-model current 70.1274mA, 0.4s and1s agreement. Thirty-two illustrative combinations yield64.526..77.766mA, NOT a guaranteed envelope.
- Independent RK4 passive pi inrush converges at0.2/0.1/0.05us: L1 peak1.052449A. Independently ran actual KiCad-bundled ngspice46 shared library, same peak1.05245A at81.746us. See passive-inrush.cir and ngspice-passive-run.log. Library SHA3238d82f02b6d08d8703a28ea894bcfdf59906dd4a59ad2e93eeec532a0454a3. It is a linear no-load inrush screening circuit, not complete driver simulation or proof of saturation damage.

## Findings and closure
1. HIGH / schematic / REQ-FAULT,POWER,PARTS: no full-temperature, all-di/dt guaranteed current-limit envelope establishes Ipk<=0.7A or total average<=80mA. LYT0p10 explicitly TJ25C at95mA/us350..401mA and610mA/us396..504mA; p13 temperature/slope curves typical. Do not use 1.65/33.2 alone: sense freewheel component differs from total output current. Obtain manufacturer envelope/current spreadsheet applicability, or redesign protection acceptance around an independently bounded energy/current ceiling; then run complete line/load/temp/tolerance sensitivity and retain actual correlation as release testing. PIXls current selection is design evidence, not a guaranteed silicon envelope by itself.
2. MEDIUM / schematic / REQ-FAULT,PARTS: C4 is X5R(-55..85C), not compatible with an assumed100C local body. Explicit C4 body<=85C or select hotter-rated capacitor. At32.868ohm,62kHz Ceff>9.81443uF required for tau>20T. Nominal22uF(-20%)(-15%X5R) gives14.96uF before DC bias/aging; extra reduction must stay below34.4%. Document exact supplier effective-cap minimum at1.76V,temperature,aging. Typical curve is a screen only.
3. HIGH / schematic / REQ-FAULT,MAINS,PARTS: actual pi filter and magnetics nonlinearity are not modeled in old430nF lumped source. Linear no-load peak-connection inrush reaches1.05245A vs L1 catalogue0.29A10%-drop reference at25C. Not proof of damage; requires L(I,T), pulse/core/winding and insulation evidence or alternative inrush/surge design. Include all-phase energization and startup/zero crossing/reverse drain current: Lout nominal3mH can be3.3mH at+10%, and manufacturer checklist flags reverse current in high-L/low-C input designs. Normal source/bridge RMS, RF power and PF cannot be inferred from DRAIN RMS.
4. HIGH / schematic / REQ-FAULT,MAINS: 648V TVS rating at7.7A25C is not hot/transient clamp/loop-inductance guarantee below700V. Exact surge waveform/source impedance/phase/repetition and part hot limits needed. Capture RF integral i²Rdt, TVS integral vi dt, C1/C2 maxima, bridge current, U1 VDS and D1 reverse voltage. Need maximum temperature-dependent TVS law or manufacturer assurance; numerical assumption cannot close missing part bounds.
5. MEDIUM / schematic / REQ-FAULT,ENV: RF minimum202.73ohm uses .97 thermal factor. Exact TE TCR±400ppm/K implies this is75K/100C from25C. At125C Rmin200.64ohm;155C198.132ohm, before any independent aging allocation. State exact RF local temperature/derating rather than extending.97 to unspecified operation. Prototype temperature assumptions are inputs, not achieved measurements.

## Requirement coverage and correct gates
- REQ-SCOPE: close by independent review of owner scope/history/branch; no measurement.
- REQ-POWER: link existing 60/72/90/108V numerical comparisons for historical acceptance, and precise latest operating proposal. Current33.2ohm remains seed until valid operating envelope substantiated. Do not silently change original acceptance wording to55mA.
- REQ-LIGHT: physical800lm after diffuser remains release gate; design estimate and LED bins/optical assumptions are separate current-stage input evidence.
- REQ-MAINS: actual market owner decision closes only line-choice unknown; numeric startup/continuous/fault ranges still due schematic.
- REQ-FAULT: valid worst-case numeric limits/current corners and failed-open containment due schematic; actual complete fault matrix remains REQ-FAULT-TEST at release.
- REQ-SAFETY: mains-reference/domain architecture and applicable standards/test matrix due schematic. Complete-product physical accessibility/insulation/fire tests remain REQ-SAFETY-TEST release. Generic0.2mm fabrication rule does not close domains.
- REQ-PROCESS: actual owner process choice can receive scoped reviewed evidence now; supplier quote/PCBA assumptions are not implied.
- REQ-PARTS: exact datasheet/pinout/MPN/procurement evidence now; final physical thermal/assembly qualification later. C4 temperature and TVS/magnetics bounds above still open.
- REQ-CONNECTIVITY: SC06 native graph, actual approval,100pins/26nets/1NC,ERC0 and corrected U4 footprint support scoped review evidence. Any SC07 topology changes require new independent intent and approval, fresh export and four reviewers.
- REQ-SIZE: board-only exploratory outline, actual part heights, termination/thermal/insulation assumptions due placement; do not demand final enclosure now or pretend old fit study is new placement.
- REQ-EMC: determine applicable limits in standards matrix now; conducted/radiated/immunity/PF/DF/harmonics/PstLM/SVM physical data release.
- REQ-COST: priced full BOM/process at stated quantity/date before purchase; not required to run schematic capture.
- REQ-ENV: establish explicit board component operating/test boundaries and evidence plan now; fixture/enclosure consequences remain separate system integration gate. No actual thermal result invented.
- REQ-SAFETY-TEST: physical release evidence remains open.
- REQ-FAULT-TEST: physical release evidence remains open; prototypes need defined tests before exercising mains, not successful tests before an exploratory layout exists.
- REQ-OPTICAL-INPUT: select or explicitly approve/propose CCT/CRI/diffuser/temp/bin envelope now. Do not substitute unmeasured781lm for required800lm test.
- REQ-INTERFACE: create structured two-endpoint driver/LED interface now, not only J2 netlist: pin identities, mains-reference, healthy/fault V/I, capacitance/residual energy/discharge, polarity, load removal and reconnection behavior, owner. Physical enclosure mechanism not necessary for electrical contract.

## Tools and evidence route
- KiCad-bundled ngspice46 is actually loadable/run via C API; PATH lacks ngspice EXE. No need install another version to simulate passive circuits or suitably compatible unencrypted semiconductor models.
- Manufacturer product page ECAD download is not a behavioral SPICE model. No primary manufacturer LYT0006 SPICE model was found during this bounded search; this is absence of located evidence, not assertion that none exists.
- Current official PI Expert support matrix lists LYTSwitch-0 in PIXls/buck, with registered online access. Obtain actual input/output report, tool/version and input hash. Do not replace this with an unexecuted promise or call custom screen PIXls.
- Passive π network can be run now with nonlinear bounded inductors, bridge, TVS, source; output model can couple exact samplehold equations and controller intervals. Model unknowns must be explicit. Transient simulation cannot repair missing full-temperature manufacturer guarantees.

Primary sources:
- https://www.power.com/sites/default/files/documents/lytswitch-0_family_datasheet.pdf (RevB06/15; local SHA c30e4bb37949d5a648893c43eaa0d7264338d53fff080143a593376cf9a7f30c)
- https://www.power.com/sites/default/files/documents/an60.pdf (RevB03/15; local SHA e28f9e280a4ea378dcd21f7dc2b02f888ee388654f33c17cefe99cfd89aa17ac)
- https://www.power.com/design-support/pi-expert
- https://piexpertonline.power.com/help/piexpert/en/topics/getting_started.htm
- https://product.samsungsem.com/mlcc/CL21A226MOCLRN.do
- https://www.te.com/en/product-6-2176792-5.html
- https://protekdevices.com/wp-content/uploads/datasheets/5kp.pdf
- https://www.coilcraft.com/getmedia/c187709d-4e59-4a35-bf2f-4557b133a391/rfc1010.pdf

Recommendation: evidence work can progress and scoped existing review requirements can be registered honestly. Do not close complete schematic gate from ERC or nominal model results; failed-open containment and data-dependent numeric current/surge bounds remain substantive current-stage work. Physical release tests need not be fabricated or moved earlier merely to approve board exploration.
