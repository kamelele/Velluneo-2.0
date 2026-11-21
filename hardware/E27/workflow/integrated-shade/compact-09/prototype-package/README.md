# SC09 routed laboratory prototype — manufacturing review packet

**Candidate files are complete for review, not a passed Toolkit release or a qualified lamp.**
Board: **50 x 32 x 1.6 mm**, two copper layers, 1 oz, lead-free HASL, green mask, white legends, manual assembly. Combined component envelope: **approximately 50 x 32 x 19.5 mm**, based on declared maxima, not a measured assembly. The earlier proposed 50 x 25 x 20 mm envelope is **not met**; width is 7 mm greater. No ordinary-bulb cavity fit is demonstrated. No enclosure is designed here.

Input: 230 VAC / 50 Hz, calculations screened at 207–253 VAC. Output: nominal 135.203 mA at 60 V, 8.112 W; proposed LED range 52–68 V, 20 series Lumileds L128-4080CA3500001, 4000 K / CRI >=80. Approximately 800 lm is a lamp target, not measured output. All output terminals and internal copper are mains-referenced; this is not SELV. No dimming or powered LED replacement.

## Files

- `SC09_Gerbers_drills.zip`: bare-board artwork and Excellon drills. Exported with one shared absolute coordinate system; no mirroring or separate offsets.
- `fabrication/`: individual F/B copper, mask, silkscreen, Edge.Cuts, X2 job, plated/nonplated drill files, maps and report. Empty NPTH file is expected (zero NPTH). 27 plated holes, including 10 vias; minimum drill 0.30 mm. No slots or mounting holes. Single board; no panel tooling.
- `SC09_KiCad.zip`: portable native schematic, PCB, project, local symbols/footprints and the 17 actual WRL package models.
- `SC09_schematic.pdf`, `SC09_layers.pdf`: native schematic and copper/silkscreen layers.
- `SC09_assembly_front.pdf`, `SC09_assembly_back.pdf`: native assembly views; back view mirrored for underside assembly. Add pin-position CSV when identifying lands.
- `SC09_BOM.csv/json`: 19 references, 17 electrical parts plus 2 bare-wire interfaces. No populated DNP positions. LED board and external wiring/fixture are not this PCB's BOM.
- `SC09_pin_connections.csv`: actual 47 native pin locations/net membership. Expected intent is independently retained in the KiCad source package, not inferred from this CSV.
- `SC09_positions_manual_reference.csv`: all 19 origins/sides/angles for manual reference. Coordinates are X from left, Y down from top in mm, angles are native KiCad footprint angles. This is NOT a vendor-qualified PCBA pick-and-place file.
- `SC09_assembly.wrl`: complete embedded native 3D visual model, millimetres; generic package appearances. No empty STEP assembly is presented as a full model. See `checks/3D-export-status.json`.
- `views/`: actual native front/back 3D renders; no AI-generated substitute.
- `checks/`: fresh ERC, DRC/parity, independent approved-intent comparison, all-55-pair strict and bounded laboratory spacing screens, two-pass refill equality and native inventory. Complete Toolkit release result is retained even though it fails.
- `validation/`: read-only native saved-copper validator, matrix and bounded package-land assessment. Run with matching KiCad10.0.6 pcbnew. Test controls are retained; no global spacing waiver is introduced.

## Ordering and assembly status

The artwork is an engineering candidate. Do not describe this packet as a passed production release: `checks/toolkit-release.json` is **FAIL**. Remaining product/physical qualification and formal spatial/approval/provider gates are listed there and in `OPEN_ITEMS.md`. Existing owner instructions authorize autonomous design/export/publication, not fabricated individual stage acceptance, purchase or energized tests. No order or supplier message was sent.

For a later authorized bare-board quotation: JLCPCB FR-4, 2 layers, 1.6 mm, 1 oz outer copper, lead-free HASL; one board per outline; do not substitute aluminium PCB, add panel tabs or scale artwork. Confirm layer assignment, 50 x 32 mm outline and PTH/NPTH separation in the supplier preview. No controlled impedance or blind/buried vias. Not an Economic/Standard PCBA upload: prototype assembly is manual. No stencil is required for the hand-solder plan; paste/stencil files are intentionally excluded. A production PCBA change needs a separate process review and quotation.

Assembly: solder bottom SMD parts first, inspect polarity/bridges; install formed R7 and RF1 and other THT parts using their contracts. Verify T1 with a three-pin gauge before installation. Fit C6 horizontally on an appropriate insulating support, keep its 5 mm vent-direction reserve, and avoid damaging its sleeve. Sleeve insulation is not a safety barrier. Trim leads below the board so they cannot contact bottom parts or copper; keep within the declared underside envelope. Check clearances after trimming and soldering. Support insulated wires independently: J1/J2 have bare solder lands, no selected connector or strain relief.

J1 pin1 = L, pin2 = N. J2 pin1 = LED_PLUS, pin2 = DC_RETURN. Exact land locations are in the pin CSV (both interfaces are on B.Cu). C6 pin1 positive; BR1 pin1 positive/pin3 negative; D1 pin1 cathode/pin2 anode; T1 pin1 LED_PLUS, pin8 FB_INDUCTOR, pin4 deliberately unwound/floating. Remove bobbin pins2/3/5/6/7 as contracted. U1 dot/pin1 = BP. Confirm all against native schematic and manufacturer data before soldering.

T1 is the custom 180-turn AWG32, 1 mH EE10 design, NOT an immediately orderable catalogue inductor. Supplier feasibility, winding insulation, DC bias, core loss and finished dimensions require verification. LYT1603D-TL is NRND; no lifecycle/supply guarantee or complete priced basket is claimed. Exact RF1/R7/C6 forming remains an unqualified assembly proposal. A render does not validate supplier fit.

## Electrical and thermal scope

Nominal current is calculated from R5 || R6. Static OVP screening is approximately 69.37–86.51 V with 25 C IC threshold limits; dynamic C6 target <=90 V is unmeasured. C6 is 150 uF / 100 V (screen maximum 180 uF); maximum stored-energy screen 0.729 J at90V. Each 68k bleeder is screened at approximately0.123 W at90V; one open bleeder gives a calculated90-to5V time of36.45s. Verify discharge; do not rely on elapsed time alone.

Planning loss allocation is0.9–1.7 W, **not a guaranteed interval**. Source-connected thermal copper is241.90 mm2 across both layers; D1 DC_RETURN copper is80.99 mm2. Copper area does not establish component temperatures. At0–40 C ambient characterize C6 can (target<=75 C, stop85 C), T1 (target<=90 C), SOURCE pin (target<=100 C), D1 case (target<=100 C), R7 local ambient/body and bleeders. Manufacturer junction/derating limits and the test operator's lower stop limits control. No published reference-board efficiency, surge or EMI result is inherited.

The high-frequency loop is kept around C4/U1/D1/T1 and R5/R6, with a separate sense branch to U1 FB. The long BUS_FILTERED feed is upstream of local C4 and is not the commutation return. SOURCE thermal pours have native pour-only high-voltage guards, not DRC exclusions. The strict all-pair screen fails intrinsic manufacturer package-land gaps; the separate scoped screen passes only explicitly bounded SO8/bridge/SMA land/escape concessions. These are engineering prototype assessments, not normative insulation waivers.

See `BRINGUP.md` before planning any powered investigation. No physical test is recorded as performed.
