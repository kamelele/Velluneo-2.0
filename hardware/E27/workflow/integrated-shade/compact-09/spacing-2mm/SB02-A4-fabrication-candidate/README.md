# SC09-SB02 — bare laboratory PCB fabrication candidate

This packet replaces the previous LYT1603D SC09 implementation with a LNK3206P
positive buck and optically coupled current/overvoltage feedback. It is a new
engineering prototype, not a drop-in controller replacement or a qualified lamp.
The original SC09 source and its historical fabrication files remain separate.

## What the packet contains

- `source/`: self-contained native KiCad 10.0.6 project, local symbols, footprints,
  rules, source-bound design inputs and honest engineering envelope models.
- `manufacturing/`: seven copper/mask/silkscreen/outline Gerbers and plated Excellon
  drill data; the flat JLCPCB upload ZIP contains manufacturing data only.
- `views/`: actual native front/back copper, assembly and schematic PDFs, raster
  previews, native bare-board renders and source-derived component-envelope 3D views. Models show maximum-body engineering envelopes,
  not qualified vendor STEP models.
- `checks/`: fresh native ERC/DRC/parity, independent intended graph, all 190 saved
  copper net-pair separations, protected component-body regions, exact MPN/Value/DNP
  and selected primary land checks, and Gerber/drill-to-source comparison.
- `assembly/`: BOM, DNP list, manual position references and unpowered inspection
  plan. These are not a qualified JLCPCB PCBA centroid/rotation package.
- `core-manifest.json`: hashes of the frozen review inputs and artifacts. External
  four-role reviews are bound to this manifest, outside their own source inputs.

## Board and intended electrical operating point

Board: **51.2 x 39.5 mm**, two copper layers, FR-4, nominal 1.6 mm, 1 oz copper,
green mask, white legend, lead-free HASL; manual laboratory assembly. Front maximum
body 18.0 mm, rear maximum body 2.6 mm, nominal overall 22.2 mm; 22.4 mm planning
including a +0.16 mm PCB-thickness allowance. Lead trimming, solder protrusions,
registration and enclosure fit require inspection and are not included guarantees.

Input design range: **207–253 V AC, 50 Hz**. Environment: **0–40 degrees C**.
Intended load: approximately **20 series 3 V LEDs**, around **60 V / 134.5 mA**,
approximately **8.1 W LED power**. The intended 4000 K, CRI >=80 and 800 lm depend
on the actual LED module and optical/thermal implementation. It is a current driver,
not a regulated 60 V bench supply. Output is **nonisolated and mains referenced**.

Initial 25 C current calculation 131.44–137.63 mA excludes TL431 cathode-voltage,
cathode-current and temperature coefficients, dynamic ripple and actual tolerances
not bounded by that screen. Static OVP initial screen is 72.08–76.83 V. The 85 V
stop and 300 microsecond delay are proposed test criteria, not demonstrated bounds.
See source calculation and fault documents for the exact conditions.

## Verification and limits

The 2 mm target applies to enumerated high-differential net pairs; explicitly
declared local normal-operation control domains use 0.3 mm. No solder-mask credit
or package-pin spacing exception is used to pass the geometry check. This does not
establish all-fault insulation: D2-open and main-switch-short behavior remain
unqualified. Current and OVP share bias/opto feedback and are not independent
fail-safe disconnection.

No measured efficiency, power factor, temperatures, hot regulation, startup,
stability, inrush pulse endurance, surge or fault latency is claimed. Listed
temperature stops are test targets, not predictions. The R10 lead forming, D1 body
registration and capacitor-can reservations require actual assembly inspection.
The input fusible resistor's continuous watt rating does not qualify its startup
pulse. Near a shorted LED output, feedback bias can collapse; nominal LED current
must not be assumed. External guarded current/time/energy test limits remain to
be assigned before any powered testing.

C6 discharge estimates apply only with no replenishment; input C7 can continue
feeding the buck after AC removal. A waiting time does not verify stored voltage.
This packet authorizes no powered work and contains no test measurements.

Technical fabrication checks and the Toolkit's full process release are reported
separately. Exact-source human stage acceptance and the generic downstream inhouse
assembly/provider qualification must not be fabricated. No supplier upload, order,
main-branch change or product compliance declaration is performed by this packet.

The portable native CLI render did not display the attached component bodies;
those images are explicitly bare-board views. The labelled populated 3D views are
deterministic engineering-envelope projections extracted from the same saved PCB,
not photorealistic native/vendor renders. Native viewer model display remains
unqualified; it does not change manufacturing copper or the independently checked
component-body exclusion geometry.

Select the order parameters explicitly: the raw KiCad `.gbrjob` finish metadata
does not specify the requested HASL process. Raw job/map/report files are retained
as audit evidence and are not included in the flat manufacturing upload ZIP.

## Purchasing

The source parts report lists 26 stocked manufacturer part numbers for 30 populated
electronic positions, primarily DigiKey Poland plus five TME items. Availability
is an observation on the recorded dates, not a reservation. R10 has MOQ 10. Four
compensation positions R18/R19/C9/C10 remain DNP; J1/J2 are wire solder ports. T1 is
the standard purchasable Wuerth 7687709222, not a custom winding. Some lifecycle and
delivery limitations remain documented. No complete landed basket price is claimed.
