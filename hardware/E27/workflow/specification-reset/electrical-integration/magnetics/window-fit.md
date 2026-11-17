# ELEC-CLOSE-01 follow-up — native nominal window geometry

2026-11-17 bounded implementer diagnostic; this integrated record is owned in this magnetics directory. Root remains sole project/CAD writer. No graph, shared model, stage approval or physical test changed. This is a numerical collision check of source outline models, not a released transformer assembly.

**Both proposed winding envelopes are free of nominal bobbin/core intersections. The TEX-E0.30 candidate also has a positive0.207mm side-dimension screen; TEX-E0.40 fails that screen by0.003mm. Retain0.30 as the geometrically better-supported candidate. Neither result establishes insulation clearance, assembly-tolerance or leadout acceptance.**

## Actual sources and coordinate extraction

- Bobbin: existing native `tmp/fp02-a/tdk-efd25.step`, SHA256 `f6acdbbccb291fd39ac8028c163d7bdb47fa6849c8c7d94dce01076f05dfb2f0`. Official exact-part page https://product.tdk.com/en/search/ferrite/ferrite/ferrite-acc/info?part_no=B66422W1010D001 links https://product.tdk.com/system/files/dam/doc/product/ferrite/ferrite/ferrite-acc/3doutline_step/c61036-a0162-b202_efd25_sw.step .
- **New authentic native core source**: exact-part page https://product.tdk.com/en/search/ferrite/ferrite/ferrite-core/info?part_no=B66421G0000X187 links its3D Outline(STEP) to https://product.tdk.com/system/files/dam/doc/product/ferrite/ferrite/ferrite-core/3doutline_step/c61036-a0162-c001_efd25.step . Retrieved externally as the native core STEP (not redistributed here), SHA256 `062a59009fed08ba69f30db6acdb0448a2e1f085f2e5882620ddc56f0536783f`. Link extracted from actual manufacturer HTML, not a guessed filename. Manufacturer HTML is not redistributed here.
- Native tolerance drawing: `component-study/source/efd25.pdf`, October2022, SHA256 `f4b6084fa9171a0157c3744663e146da6b3a738171dab4dfd3e137c125f6f06e`; p2 core drawing newly rendered/visually inspected externally; p3 bobbin drawing previously directly viewed.

Actual bobbin STEP coordinate frame has **winding axisZ**. Barrel outside flats X=±6.55mm, Y=±3.45mm; rounded corners R2.0 with axes centered at X=±4.55/Y=±1.45, confirmed from cylindrical-face geometry. Thus its continuous central outline is a rounded rectangle13.1×6.9mm,R2. The straight axial barrel reaches Z=±8.1mm; flange interior planar faces are Z=±8.3mm with connecting fillets. A centered10.5mm winding band ends at Z=±5.25mm and leaves **2.85mm per side to the ends of the straight barrel** (3.05mm to interior flange planes). These are nominal model measurements, not guaranteed usable safety margins.

Core STEP uses a different source frame: Xwidth25mm; Y half-depth0..12.5mm; Zsection−9.1..0mm. Its centerpost section is centered at sourceZ=−3.2mm (faces−.6/−5.8). Align one half to bobbin by rotateX−90°, then translate(0,3.2,12.5); second half rotates this result180° about globalY. This makes the meeting plane bobbinZ0 and aligns core centerpost with the bobbin bore. Core inner side-leg planes become X=±9.35mm. Two native ungapped halves conservatively occupy more centerpost space than the actual gapped pair; the gap removes centerpost material and does not narrow the outer-leg winding window. The transform is recorded explicitly; it does not invent a pin1 view.

## Full nominal envelope collision

`check-window.py` imports both native solids with CadQuery/OCP, constructs each complete uniform-thickness rounded-rectangle winding shell around the central barrel, extrudes it through the centered10.5mm band, then calculates boolean intersections against the **actual bobbin and both actual core solids**. Thus this goes beyond comparing AN40.7mm² against an arbitrary rectangle.

The shell is an analysis envelope, not turn-by-turn windings. A uniform maximum build covers the previously budgeted staggered-tape seam; special end leads/crossovers/sleeves outside that envelope are excluded and remain open.

| Candidate | Required uniform radial build | Winding shell bounds X/Y/Z mm | Bobbin intersect | Core intersect | Nominal side gap |
|---|---:|---|---:|---:|---:|
| TEX-E0.30,ODmax.520 | 2.293mm | X±8.843,Y±5.743,Z±5.25 | 0mm³ | 0mm³ | .507mm |
| TEX-E0.40,ODmax.625 | 2.503mm | X±9.053,Y±5.953,Z±5.25 | 0mm³ | 0mm³ | .297mm |

The0.40 variant retains P/A0.180Grade2, tape budget and S15+15 layers; proposed S pitch.650 gives layer width9.75mm≤10.5mm. It increases the two S layers by2×(.625−.520)=.210mm. Native Furukawa resistance/OD table remains reference-only for either wire; no new batch guarantees inferred.

## Separate native drawing tolerance screen

Native core p2 labels **inner leg spacing18.7±0.6mm**, not bobbin flange18mm. Native bobbin p3 labels barrel span13.1−0.2mm. For a centered assembly and treating these dimensions alone:

Available one-side radial space = [(18.7−.6)−13.1]/2 = **2.500mm**.

- TEX-E0.30:2.500−2.293 = **+.207mm**.
- TEX-E0.40:2.500−2.503 = **−.003mm**.

This corrects the tempting(18−13.1)/2 flange-based inference: the relevant core obstruction is its18.7±.6 inner side-leg gap. The3µm negative result is smaller than ordinary practical assembly uncertainty; it is precisely why the0.40 construction cannot receive a dimensional acceptance from nominal fit. Its packing must be changed or the actual component/process limits narrowed before use as a tolerance-supported candidate.

For0.30, lateral bobbin/core decenter plus all additional build/deformation allowances must remain below.207mm to preserve that side-dimension result. **This is an unallocated mechanical tolerance budget, not a selected insulation distance.** Remaining native inner contour tolerances, relative centering, winding compression/lumps, tape batch thickness, lead exits, sleeves, yokes, core assembly and manufacturing process can consume it. Neither a positive.207mm nor zero nominal collision closes these conditions.

## Reproduction and handoff

Run `python check-window.py --bobbin-step /external/path/bobbin.step --core-step /external/path/core.step`; numeric output is `window-results.json`. Both explicit external source inputs are SHA256-checked before model import. Native source identity and model transforms are embedded in results. The analysis neither changes component selection nor claims a physical winding fits, passes withstand, or survives temperature/fault conditions. Geometry now supports a concrete0.30mm winding trial with explicit local fit conditions; it does not justify silently treating0.40mm as interchangeable or inheriting1% leakage.


Integration note: Full manufacturer PDF/STEP/HTML/image files are intentionally not copied into this directory. `sources.json` records source identities and original URLs; `README.md` gives reproduction instructions. Initial source paths in the technical narrative identify the original read-only analysis evidence, not required repository-distributed vendor files.
