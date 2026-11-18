# DRIVER-ENTRY-02 — driver-only PCB preparation, not stage closure

18 November 2026. Base f0216041fc47fef993e24939c6f31727fe409a14. The owner requested the rectangular power supply only, completion of PCB-entry prerequisites and a preview in the chat. Housing, radiator and LED-panel redesign are outside this packet. **PCB entry is still blocked.** Active approved 31-position circuit, values, local libraries and all requirements/rules remain unchanged.

## Concrete work

The saved 32 x 60 mm analytical proposal uses all31 actual local footprints and79 pads. Five semiconductor courtyards previously projected under the allocated30 x 30 mm transformer; now none do. Independent scalar geometry and actual native KiCad10.0.6 Flip/Rotate checks agree on all79 pad boxes. There are no same-face courtyard conflicts, outline overruns or opposite-face THT-pad-plus0.4mm planning conflicts. The prior9.35mm projected P/S pad-box reserve is preserved: current minimum10.225mm; minimum copper-box-to-edge0.600mm. These are **planning constraints, not adopted normative insulation or qualified assembly limits**. T1 finished30 x 30 x 18 mm and all installed heights remain unqualified allocations.

This is **not a selected electrical placement**. The search minimizes an explicitly weighted pad-centre score and excludes semiconductors under T1. Its score is not an electrical acceptance criterion. A separate final constructive correction overrides the aggregate-score result, moves C1 inward and puts C2 directly behind U1: both VDD and return endpoint distances are1.412mm in projection. Actual adjacent vias/board thickness, loop area, via-current/inductance and the other sensitive connections still need routing. No numeric TI pass limit is invented. Exact comparison:

- U1.1 to C2.1: 17.281 -> 1.412 mm.
- U1.4 to C2.2: 21.507 -> 1.412 mm.
- U1.2 to R4.2: 11.494 -> 7.201 mm.
- U1.2 to R5.1: 19.189 -> 10.583 mm.
- U1.5 to R6.2: 25.779 -> 14.434 mm.
- R7.2 to Q1.1: 23.671 -> 13.086 mm.

All distances are straight pad-centre lower bounds, not routed lengths, loop inductance or a proof of feasible two-layer routing. Front/back transitions, Kelvin/star returns, vias and high-voltage functional spacing remain to design. The preview intentionally contains no fictional tracks. The previous whole-lamp assembly fit does not transfer to these changed component sides/coordinates.

## Protection: concrete candidate, not an applied swap

Official Vishay28909 documents a fail-safe mains-fusing test at230Vac: resistance over100kohm, opening under2s without flame/explosion, at the listed test conditions. The proposed47ohm axial ordering code AC05000004709J6BCS is derived from the ordering table and still needs exact identity confirmation. It is a different safety-fusible family from the active regular AC05; maximum body17 x 10mm also changes the installation envelope. Neither the schematic nor the footprint/MPN has been changed. F1 remains3403.0268.23.

The253Vac/18uF/44.65ohm ideal cold-charge screen is1.152162J,8.01335A peak and0.025804A2s, with803.7us RC and401.85us equivalent full-peak duration. Manufacturer1.2/50us pulse data cannot be accepted by energy alone; official note28897 explicitly depends on pulse shape and duration. A230Vac fail-safe test does not establish253Vac coordination or hot repeated-charge endurance. Initial ideal hard-short R1 power rises21percent from230 to253Vac; this is not sustained deposited heat or a clearing prediction. Actual source impedance, R1/F1/BR1 coordination and adjacent-component heating still require evidence.

Both official PDFs were downloaded, SHA256 checked, native text inspected and datasheetpage7 visually inspected by root through PDFium. Their identities/pages are in electrical-results.json. Vendor documents remain outside the repository. Read-only implementer findings are distinguished from root native-byte checks.

## Magnetics: finite three-port calculation prepared

electrical.py constructs six positive-definite three-port inductance matrices from the retained C2 balanced leakage-energy matrix and Lp tolerance. It preserves the primary open-circuit Lp, verifies the balanced-subspace energy independently and calculates pair short-circuit Schur complements. T1-C2-surrogate.cir contains the nominal coupled-inductor subcircuit. **This constructed surrogate is not a validated transformer or controller model.** Core saturation/loss, winding resistance/capacitance, geometry ends/gap/fringing and actual thermal behavior are excluded. No successful UCC28711 transient simulation is claimed.

At nominal Lp the source-derived surrogate has P-S short-circuit leakage14.06152uH with A open and P-A leakage23.20758uH with S open. These are not interchangeable with the old balanced P-A air-energy23.35990uH. A sensitivity family scales the balanced matrix to20uH P-S; all matrices remain positive definite at Lp +/-10percent. This prepares consistent auxiliary/startup sensitivity inputs without silently using ideal coupling.

An independently audited standard alternative, Wurth750813144600uH4:1:.71, is not drop-in: it changes compensation/operating energy/clamp and footprint, and its18.8mm height exceeds the18mm allocation. No standard-part substitution is made. Finished custom winding/core/yoke/leadout/EIS/parameter/loss acceptance remains necessary; see the retained design-closure-02/transformer construction contract and this packet's magnetic handoff.

## Actual checks and decision

Fresh native doctor, independent graph comparison, all-severity ERC, native79-pad transformations and scalar geometry checks pass within their stated scopes. Graph remains79physicalpins/22nets/4NC, accepted intent5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8. Requirements schematic-stage still exits1 forU05-U09; full work check still exits2 configuration_error. Those are actual failures, not expected-pass waivers. Logs and commands are in checks/.

The schematic-stage packet cannot be accepted and no product PCB is created. Exact owned closures are in acceptance-ledger.json; routing-block-cards.json records sensitive nets and return topology to implement after prerequisites close. Four distinct read-only roles inspect the frozen preparation packet; their recommendations do not approve the product stage. No human acceptance, supplier confirmation, physical manufacture, powered test, certified safety, copper routing or DRC is fabricated.

## Reproduce

Run optimise.py with Python/numpy (fixed seed24000iterations); verify-layout.py independently checks the saved proposal. Run electrical.py with optional --source-dir EXTERNAL_OFFICIAL_PDF_DIRECTORY to verify the two recorded native sources; no PDF redistribution. Use pinned KiCad10.0.6 Python for native-projection-check.py; it creates only ephemeral footprint fixtures and saves no board. render.py writes the English driver-preview.svg; --polish --png OUTPUT writes the user preview. Preview volumes use native F.Fab bounding boxes plus allocated heights, not qualified vendor3D models. The C1 perspective is a bounding prism, not an exact cylinder.
