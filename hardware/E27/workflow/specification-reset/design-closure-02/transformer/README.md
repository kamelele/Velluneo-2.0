# T1-INTERLEAVED-C2 construction proposal

Base ea3b23fced193861c94637524d482b7c0e96d33e, DESIGN-CLOSURE-02. Implementer `/root/closure_transformer`, exclusive `transformer/**` write scope. This is a proposed, dimensioned winding construction with executed geometry and magnetic-energy screens. It is not shared CAD, a supplier drawing acceptance, a measured transformer or an independently closed finding.

## Concrete result

The earlier non-interleaved P120/A22/S30 construction does **not have a defensible 20 µH leakage guarantee**. A one-dimensional air-energy screen gives 74.25 µH with a declared common sheet width of 10.5 mm; even an optimistic 16.2 mm common-width calculation gives 48.12 µH. These approximations flag a design risk; they do not prove what a manufactured part would measure.

The recommended candidate keeps the exact EFD25 core/bobbin, 120:22:30 turns, wire types and external winding pins. It splits the primary into two electrically series, continuous-wire 60-turn sections:

`P60 / 2 tape wraps / A22 / tape / S15 / tape / S15 / tape / P60 / outer tape`

All windings are spread over a proposed 13.8 mm active band. The selected air-energy screen gives P–S leakage 14.06 µH with A open and P–A leakage 23.36 µH with S open, both referred to the primary. The prior P–A screen is 30.97 µH. Putting A outside both primary halves gives a lower P–S screen, 8.87 µH, but a higher P–A screen, 40.37 µH; that alternative is not selected because auxiliary coupling is important to startup. No 20 µH finished-part guarantee follows from these numbers.

[Construction drawing](construction.svg), [PNG preview](construction.png), [machine-readable contract](construction-contract.json) and [executed results](results.json) are reproducible from `design.py`. No vendor artwork is copied into the drawing.

## Geometric and process contract

Six complete 1350F-1 tape wraps and the selected wire layers give 2.153 mm regular radial build. Staggering the seams so that at most one extra 0.077 mm layer occurs at an angle gives 2.230 mm maximum build. The retained side-dimension screen allows 2.500 mm; subtracting proposed 0.050 mm extra build and 0.050 mm decenter allocations leaves **0.170 mm**. These are process requirements, not supplier capabilities. The prior nominal STEP collision result is not claimed to cover this wider construction.

The 13.8 mm band leaves **1.20 mm at each end** of the retained 16.2 mm straight barrel. P/A leadouts and the parked continuous primary bridge are restricted to the primary-side end pocket; S leadouts and crossover are restricted to the secondary-side pocket. No bridge or crossover ridge is allowed over the active band. The primary remains one wire with no extra splice, external net or hidden use of NC pins. The two S layers also form one continuous wire. Winding sense and dot polarity must be preserved through each section.

The primary bridge has a concrete optional protection route: FIS-B3-listed Essex Furukawa PIT-S tubing, with proposed incoming dimensions ID ≥0.25 mm and OD ≤0.60 mm. At axial center Z = −7.50 mm ±0.15 mm this leaves 0.15 mm residual to either axial pocket edge. The size, bend capability, actual radial/core/yoke route and production method are **not confirmed**. Listing the material in an EIS is not a guarantee that this particular size or 3D route is available. The 2D axial arithmetic cannot close that issue.

Two complete tape wraps separate P1 and A. Three further full tape wraps intervene between A and the outer P2 across the secondary region. Spaced TIW round wires are not counted as a continuous sheet barrier. All wrap coverage, edge/seam locations and lead exits require the actual builder's all-path drawing. No base wrap assumes a confirmed PM-9630 ground-insulation function and ≥0.3 mm all-path wall; that confirmation remains absent. FIS-B3 compatibility is still a candidate material route, not finished-transformer recognition or an end-product standard pass.

The proposed finished interface envelope remains **30 × 30 × 18 mm**, including leadouts, core and yokes. The regular winding shell is 17.56 × 11.36 mm in the retained barrel cross-section. The finished envelope is an allocated design limit, not a demonstrated complete assembly size. Core and yokes remain hazardous primary-domain objects for accessibility/separation analysis. A bare secondary terminal's distance to ferrite/yoke is not established by the planar pad gap.

## Leakage model and numerical verification

The calculation derives leakage energy in air from ampere-turn balance. With axial current sheets of declared common width `b`, the cumulative radial MMF is `F(x)`. The mean turn perimeter of an offset rounded rectangle is `p(x) = p0 + 2πx`, using the retained 13.1 × 6.9 mm, corner-radius 2 mm barrel. Therefore:

`L_eff = μ0/b ∫ p(x) F(x)^2 dx / I_reference^2`

Each current-carrying layer has linear MMF across its homogenized OD; tape has constant MMF. Exact polynomial integration and a separate midpoint quadrature at 40/80/160/320 subdivisions agree to **1.73e−11 H** at the finest setting. The balanced two-coordinate leakage matrix has a positive determinant. Its independent current combination reproduces the P–A pair result. These checks establish mathematical consistency, not field-model accuracy.

Only combinations with `120 Ip + 22 Ia + 30 Is = 0` are modeled. The resulting two-coordinate matrix is an air-energy subspace, **not a complete three-port magnetizing model**. It does not establish actual open-circuit Lp or terminal short-circuit measurements. Finite magnetizing inductance, gap/fringing fields, winding ends, round-wire local fields, yokes, leadouts and unequal actual axial occupancy are omitted. Width and added radial spacing are explicitly swept. No arbitrary approximation-error factor is called a guaranteed bound.

TI SLUP105 provides the air-energy/current-sheet basis and warns that core/window geometry changes leakage estimates. TI's SLUP338 discusses flyback transition interleaving and the capacitance tradeoff. This implementation uses its own variable-perimeter integration. The new construction changes interwinding capacitance, field distribution and sampling/EMI behavior; no old parasitic or auxiliary-window calculation is automatically validated for it.

## Copper, flux and remaining loss budget

Rounded-rectangle perimeters and helical pitches give P/A/S lengths including proposed lead allowances of 5.271/0.931/1.408 m. New cut-length acceptance proposals are **5.40/0.95/1.45 m**; their source-conditioned DCR20 limits are in the contract. These values need builder and exact purchased-wire confirmation, especially because the TEX-E resistance table is reference data.

Using those upper cut lengths, the existing separate P/S RMS witnesses, an explicitly assumed A RMS screen of 0.10 A, and copper α = 0.00393/K gives **0.20174 W DC-equivalent loss at 110°C**. This leaves **0.29826 W** of the proposed 0.50 W T1 normal-loss budget for core, AC proximity, gap fringing, terminations and uncertainty. It is not a total-loss prediction. The supplied isolated round-wire Bessel calculation shows the skin-only frequency sensitivity; it omits proximity/gap effects and does not supply the actual harmonic spectrum.

The ordinary peak-current witness with Lp at +10% gives about 0.133 T from `Lp I/(Np Amin)` before remanence. A static backup-current proxy is also shown, explicitly not a maximum dynamic fault current. TDK's N87 sine-test loss and specified-field Bs values are only references. Actual flyback unipolar/DC-biased waveform loss, core temperature and repeated fault pulses need their own validated assessment. Comparing a triangular total flux swing directly to sinusoidal peak flux, or using Bs as a safe operating limit, would be incorrect.

## Remaining acceptance and source limits

- **T1-C2-01 / CLAMP-01 / ELEC-MAG-001:** select/review this changed construction, then establish the actual three-winding impedance model, effective leakage ≤20 µH in the relevant operating conditions, Lp 2.304 mH ±10%, ratio and polarity. The slab screen advances feasibility; it does not close the parameter guarantee.
- **T1-C2-02 / RC-BIAS-001 / RC-COMP-002:** use the changed winding DCR/coupling/capacitance in affected startup, commutation, drain/VDD and EMI analyses. The unchanged external graph does not make old winding-dependent evidence current.
- **T1-C2-03 / R-THERMAL / R-BASE-LIFE:** establish core+AC/fringing/termination loss within the remaining normal budget and fault losses/temperatures separately. No 11 W fault cap or 0.10 A actual auxiliary-current bound is assumed.
- **T1-C2-04 / ISOL-02–04 / U10:** confirm EIS grade/function, tubing size and full leadout/core/yoke/terminal geometry under actual tolerances; verify the finished envelope, process and wire-insulation retreat. Actual applicable normative paths/limits remain unresolved.

New byte retrieval of the two STEP files and N87 PDF failed in this task (child DNS failure; coordinator HTTP403). The retained genuine source-derived 430-face bobbin record and prior core/window results are hash-verified, but **no fresh STEP import or 3D collision test is claimed**. Accessible primary web renderings and the six retained material-source byte identities are documented separately in `sources.json`. No expired standard content was used and no vendor publication is redistributed.

Actual command: `python design.py --material-source-dir EXTERNAL_ISOLATION_SOURCE_DIRECTORY --png` with Pillow on external PYTHONPATH. `design.log` retains the successful result. Standard Python alone reproduces JSON/SVG without `--png`; the native material directory is optional but enables the six byte checks. This task performed no physical manufacture, energization, measurement or supplier communication. Coordinator integration and four independent reviews remain required.
