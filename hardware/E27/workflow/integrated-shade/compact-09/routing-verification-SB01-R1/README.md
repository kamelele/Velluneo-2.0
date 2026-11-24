# SC09-SB01 R1 — verification of the existing board

This is the previous 51.2 x 33 mm, two-layer, 19-position LYT1603D board. No new
controller, circuit, component value, footprint, placement, track, via or outline
was adopted. The original project is backed up separately before this work.

## Concrete corrections

- Actual U1 MPN fields in the PCB and schematic now match the already selected
  LYT1603D tube-packaging BOM, replacing the inherited -TL reel suffix. The silicon,
  SO8 pattern, values and all 46 physical pin memberships are unchanged.
- Two stale generated placement/routing consumer digests were synchronized with
  the current spatial intent through the pinned configure preview/apply process.
  Numeric limits, protected regions, block cards, native .pro and .dru are unchanged.
- Current Gerbers, drills, BOM, manual positions, both-side assembly drawing and
  an unpowered inspection plan are freshly source-bound. hardware.json now points
  to this candidate rather than the historical release files. The inspection plan
  uses the actual SB01 parts instead of obsolete Coilcraft/TDK/VR25 instructions.

## Routing and placement result

Independent checks found zero non-axis/45-degree, tiny-segment or off-centre-via
flags. The R5 quiet sense branch joins force copper only at the intended physical
pad. BP/M/sense routes avoid the coil-body projection; C6's both-face reservation
is empty. Seventeen populated body reservations have no same-face overlap. C5's
paths to the nearest BP/SOURCE pins are each 2.9196 mm. Minimum trace is 0.3 mm;
minimum annular ring is 0.225 mm. These are geometry checks, not measured EMC or
thermal performance. A shorter filter-feed trial crossed BUS_RECT and was rejected.
The final copper is deliberately unchanged; an unnecessary reroute is not a fix.

Fresh ERC, DRC with schematic parity, independent pin graph/actual MPN checks and
Gerber/drill-to-native audit pass. Native default ignored keys are retained and
visible in raw DRC reports; separate routing geometry checks cover via entries.

The original strict 2 mm comparison still reports **23 observations**: five
intrinsic pad pairs and eighteen nearby escape observations at BR1/U1/D1. The
intrinsic drawn gaps are 1.500002 mm (two BR1 pairs), 1.940002/0.670002 mm (U1)
and 1.500002 mm (D1). No pad was shrunk, numerical rule relaxed, mask credit used,
or failure renamed PASS. Routing/rigid relocation cannot enlarge fixed pad gaps.
The owner returned to this board instead of the larger SB02 redesign; this does
not establish normative insulation or permit ignoring actual shock/fault hazards.

## Files and order status

`SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip` contains eight flat manufacturing files:
seven Gerber layers and the PTH drill file. The raw empty NPTH file and .gbrjob
metadata are excluded from the supplier ZIP and retained in audit evidence. Select
FR-4, 2 layers, 1.6 mm, 1 oz, lead-free HASL, green mask and white legend explicitly.
No JLCPCB assembly, stencil, supplier upload or order was performed. Positions are
manual-assembly references, not qualified PCBA centroids/rotations.

The full Toolkit release remains FAIL. Its existing full-product requirements,
physical/thermal/insulation evidence, exact-source human decisions and generic
downstream assembly-provider qualification are not fabricated by this PCB audit.
Fresh artifact bindings and consumer mismatches have been repaired; those remaining
process/product gates are distinct from the passing fabrication geometry audit.
This candidate is not an accepted manufacturing release or powered prototype.

The populated 3D views are retained from the reviewed a66e97... SB01 source; exact
geometry/model identity justifies retaining them for this metadata-only correction.
Their hashes and original review manifest are included. They are engineering
appearance models, not qualified vendor fit models. The current portable renderer
did not display the component bodies, so no newly rendered populated view is claimed.

## Assembly and later qualification

All 17 electronic positions are populated; J1/J2 are wire solder ports. T1 is
Wuerth 7687709152 (WE-PD HV 1210, 1.5 mH); the old 1280 text is a historical label.
Old R7/VR25 and model-info summaries are historical. Refer to actual selected MPNs,
current footprint geometry and the unpowered inspection plan. R6 sample/termination
fit, formed leads/support, C6 vent clearance and wiring restraint remain physical
assembly checks. No closed-enclosure fit or operating temperature is established.

Intended input is 207–253 VAC/50 Hz, nominal LED load approximately 60 V/133.4 mA
(about 8 W), one 20-series LED string. Output is mains referenced. Startup, current,
ripple, OVP, inrush, surge/fault response, hot magnetics, temperatures and efficiency
remain unmeasured. Retained thermal values are conditional estimates/test targets.

## Primary layout references checked

- [Power Integrations LYTSwitch-1 datasheet, PCB layout guidance](https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf)
- [TI SLYP762 switching-supply PCB layout](https://www.ti.com/lit/ml/slyp762/slyp762.pdf)
- [JLCPCB fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities)
- [JLCPCB design best practices](https://jlcpcb.com/blog/pcb-design-rules-best-practices)

Four independent final roles review the same core manifest. Their reports remain
outside their own source inputs. Recommendations do not constitute human acceptance.
