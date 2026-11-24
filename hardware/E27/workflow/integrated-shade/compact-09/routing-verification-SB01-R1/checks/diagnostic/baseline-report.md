# Independent SC09-SB01 baseline routing diagnosis

Actor: `/root/sb01_refine_diagnostic`. Scope: read-only baseline inspection for the
owner's request to improve the existing board without changing its circuit,
controller, parts or 51.2 x 33 mm outline. This is a technical contributor report,
not a final independent review of any subsequent implementation.

Baseline PCB SHA256:
`a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`.
All diagnostic commands left this file unchanged. No CAD or configuration was saved.

## Main result

The current board is already clean under the read-only axis/45-degree, very-short
segment and centred-via-entry screen: zero flags across 143 straight track segments
and 12 through vias. Native full schematic-parity DRC reports zero violations,
zero unconnected items and zero parity issues. There is no evidence to justify
replacing this design or forcing cosmetic changes solely to show activity.

The independent strict saved-copper checker freshly reproduces the same 23
different-net spacing findings after 13,417 face-object comparisons. These are
five intrinsic pad pairs plus 18 local escape observations; no unrelated long
field trace appears in that list. The generic 2 mm engineering target remains
unsatisfied. It is not a normative all-voltage minimum or a certificate.

The five intrinsic pairs are:

- BR1.1 / BR1.3, BUS_RECT / DC_RETURN: 1.500002 mm.
- BR1.2 / BR1.4, AC_FUSED / AC_N: 1.500002 mm.
- U1.2 / U1.4, M / BUS_FILTERED: 1.940002 mm.
- U1.3 / U1.4, FB_INDUCTOR / BUS_FILTERED: 0.670002 mm.
- D1.1 / D1.2, FB_INDUCTOR / DC_RETURN: 1.500002 mm.

These exact primary land geometries cannot acquire 2 mm separation merely by
rigid placement or routing. Do not shrink solder lands, rename nets, create
via-in-pad process complexity, relax the matrix, or claim that fewer duplicate
entries closes the controlling pad pair. The associated 18 observations comprise
six BR1 pad/track, six U1 pad/track and six U1 track/track observations. Their
individual UUIDs, coordinates, widths and classification are recorded in
`baseline-diagnostic.json`. Local exit choices can be improved if useful, but the
strict result cannot honestly become PASS while retaining all exact current lands.

## Concrete metadata defect

The current canonical `bom-build.json` selects U1 `LYT1603D` tube packaging, while
the actual PCB `MPN` property remains `LYT1603D-TL`; PCB Value is `LYT1603D`.
The other 18 native MPN properties match the canonical BOM. Native parity alone
does not detect a stale field shared by schematic and PCB. Aligning that property
to the already selected packaging is a metadata correction, not a new circuit or
controller. The coordinator was informed; this contributor did not edit it.

## Control and power routing

The exact polygon audit checks the 15 native UUIDs in the U1.3-to-R5.2 sense path
(17 face objects including through-via faces). Its only intersection with other
force-carrying FB_INDUCTOR copper lies inside the physical R5.2 pad. There is no
quiet/force shortcut outside that pad.

BP, M and this low-current Kelvin sense branch do not intersect the maximum
12.5 x 12.5 mm T1 body projection on either face. The existing C6 both-face copper
reservation is empty. SOURCE and FB_INDUCTOR switch in this high-side buck; neither
should be treated as a quiet DC ground or expanded into a generic heat plane.

Saved endpoint path proxies include:

- C5.1 to U1.1: 2.9196 mm.
- C5.2 to nearest SOURCE pin U1.8: 2.9196 mm. The 6.7296 mm path to pin U1.5
  includes the 3.81 mm common SOURCE bank; it is not evidence of a long local
  bypass connection. The simplified endpoint graph does not resolve mid-segment
  pickup at pins 6/7; native connectivity reports zero unconnected items.
- U1.3 to R5.2: 12.9470 mm, geometrically dedicated sense branch.
- C4.1 to U1.4: 7.3887 mm.
- C4.2 to D1.2: 19.3947 mm.
- R5.2 to T1.2: 25.0696 mm.

These numbers omit pad-internal distances and use zero via transition length.
They are routing proxies, not measured loop inductance, EMI or thermal performance.
The longer force/filter paths are legitimate bounded optimization candidates,
provided all other constraints and the dedicated Kelvin topology are preserved.

The writer is considering a shorter F.Cu L1.2-to-C4.1 BUS_FILTERED feed. Review it
against every strict net-pair minimum, raw saved net identity, C6 reservation,
T1/control projections, C4 local commutation geometry and routing width. Removing
a detour/via is useful only if the route does not add switching-field coupling or
new foreign-net/body violations. No source mutation is proposed by this report.

## Primary layout basis and interpretation

- [Power Integrations LYTSwitch-1 family datasheet](https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf),
  local PDF SHA256 `c25fe052456356af1437cfd9985182b6e443164aba8d4d89f1fabf4b263e18bc`.
  It establishes actual high-side topology, local bypass function and the thermal
  conditions under which published package resistances apply.
- [Power Integrations AN-67](https://www.power.com/sites/default/files/documents/an67.pdf),
  local PDF SHA256 `53069f49b53917459c150a5f8afc2073499a08b3adce4588bcd2e1869d2d68db`,
  page 9: compact commutation/freewheel loops, close control components and bypass,
  and input-filter separation from switching sources. Its low-side heat-spreader
  example must not be transferred indiscriminately to floating high-side SOURCE.
- [TI SLYP762](https://www.ti.com/lit/ml/slyp762/slyp762.pdf), freshly read from the
  primary site for this diagnosis: switching-loop, sensitive-trace and thermal
  guidance supports minimizing parasitic coupling and loop area. Its general
  examples do not establish a numeric safety spacing for this specific board.

No measured temperature, efficiency, hot stability, surge, inrush endurance or
fault response is available from these geometry checks. Retain the existing
component-specific thermal targets and physical prototype qualification gates.

## Evidence files

- `baseline-diagnostic.json`: all 23 classified findings, actual native MPN fields,
  component poses and endpoint path UUIDs.
- `strict-fresh.json`: fresh strict 55-pair saved-copper run, FAIL 23, no exceptions.
- `routing-quality-baseline.json`: zero routing-quality geometry flags.
- `fresh-DRC.json`, `fresh-netlist.xml`: current native read-only checks/graph export.
- `kelvin-and-bodies.json`: exact same-net polygon and both-face body checks.

This report recommends bounded refinement and honest residual reporting. It does
not approve fabrication, powered work, a standards deviation or a finished lamp.
