# SC09 — accepted-size bare laboratory PCB package

**Current scope: unpopulated laboratory PCB for manual prototype assembly and later measurements.** The owner explicitly accepts50×32mm. This closes the earlier25mm width deviation. It does not prove fit in a particular bulb cavity or qualified operation. The actual scoped fabrication disposition is in `bare-board-readiness.json`; full product Toolkit release remains a separate failing report.

## Download and ordering parameters

Use **SC09_do_zamowienia_PCB.zip** (or equivalent SC09_Gerbers_drills.zip): exactly7Gerber layers and2Excellon drill files. CRC/file hashes and coordinates are checked against native CAD. FR-4,2copperlayers,1oz,1.6mm, **lead-free HASL**, green mask, white legends, one board per closed50×32mm outline. No PCBA/stencil/panel or order payment is implied. Review the actual supplier preview before checkout; no supplier CAM acceptance has been obtained here.

27PTH/0NPTH, minimum drill0.30mm; T1 now has three1.20mm holes. Empty NPTH program is intentional. Milling path centreline is50×32mm;0.05mm outline stroke does not increase the intended routed size. Optional native .gbrjob has Finish=None and stroke-size metadata, so it is deliberately excluded from the upload ZIP. The explicit HASL order parameter controls the finish. The loose fabrication directory also retains drill maps/report and native auxiliary job for traceability.

`SC09_KiCad.zip` is the complete portable editable project with local symbols, footprints,17WRL model packages, experimental per-part STEP sources and registered fabrication artifacts. STEP interchange remains unqualified; no empty assembled STEP is delivered. `SC09_assembly.wrl` is the actual embedded visual model. Both native front/back renders are under `views/`.

## Supply specification

Read **SC09_specification.pdf/json**. Input230VAC50Hz, calculations207–253V. Proposed output52–68V LED load, nominal60V. Regulated total current estimate135.2mA includes dual68k discharge resistors; at60V externalLED estimate is133.4mA /8.01W. No accuracy/ripple guarantee is established. This is a constant-current supply, not a regulated60V voltage source.

All-inclusive base loss allocation0.9–1.7W gives input8.91–9.71W and82.5–89.9% efficiency to externalLED at the nominal60V operating point. These are planning scenarios, not measured extrema. At230V and ASSUMED truePF0.90, input is43.0–46.9mARMS. PF/current must be measured. Reference-board91.51% efficiency is not assigned to SC09.

Ambient design scope0–40°C. Explicitly unvalidated temperature scenarios at40°C: U1 junction58–110°C, T1 body59–108°C. The latter can exceed the90°C target: test hot behavior before treating the assembly as rated. C6 can≤75°C is a target,85°C a proposed lab stop; neither is a predicted measured result. Full assumptions and other targets are in the specification.

## Current physical design and checks

PCB50×32×1.6mm; approximate declared assembly envelope50×32×19.5mm. Eight legend strokes were corrected0.12→0.15mm with text height1.0mm. ThreeT1holes were enlarged0.85→1.20mm without changing pin centres, outer lands, nets or circuit. Coil-terminal position is explicitly RADIAL≤0.15mm; nominal fit arithmetic includes conservativePCBposition/hole tolerance. This closes a design fit-envelope problem, not actual supplier sample qualification.

19references,47physicalpads,11intendednets,1explicitNC. Fresh native ERC/DRC/parity, approvedA1graph, two-pass refill and independent all55pair screens are retained. The strict spacing screen fails intrinsic package-land distances; the separate bounded laboratory screen retains finite SO8/bridge/SMA concessions. No soldermask/SELV or normative insulation qualification is claimed. No check exclusion or global floor is relaxed.

Existing older reviews/final-review-inputs belong to commit082ffdb. Current order-stage reviews and exact inputs are separate; see current workflow index and `order-review-inputs.json`. Documents, calculations, scenarios and measurements are distinct.

## Assembly and physical testing remain controlled later steps

Solder bottomSMD first, inspect bridges/polarity, then install THT parts according to exact native schematic/BOM and custom contracts. T1 needs supplier/sample gauge and inductance/DCbias/thermal qualification. R7/RF1/C6 leadforming, insulation support, vent clearance and solder protrusion need actual part inspection. A1:1print gauge is provided in SC09_fit_gauge_1to1.pdf; print100% and verify its50mm ruler. A paper gauge is not a qualified supplied coil.

J1.1=L,J1.2=N; J2.1=LED_PLUS,J2.2=DC_RETURN, both bare-wire interfaces on B.Cu. Pins/coordinates are in SC09_pin_connections.csv, and sides/angles in SC09_positions_manual_reference.csv (native KiCad angles, Xfromleft/Ydownfromtop; not vendor-qualified PnP). No DNP population positions. External LED board, wire strain relief and guarded fixture are outside this PCB.

All internal/output nodes remain MAINS REFERENCED, notSELV. No dimming or hotplug. Isolate power and verify discharge before replacing/reconnecting the LED module. Integrated protection, MOV and bleeders do not provide a touch barrier or demonstrate safe single-fault behavior. BRINGUP.md identifies later qualified-test prerequisites; no powered results or actual order are claimed.
