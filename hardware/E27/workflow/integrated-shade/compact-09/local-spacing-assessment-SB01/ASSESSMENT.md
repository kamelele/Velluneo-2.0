# SB01 local spacing — fabrication-only disposition proposal

## Decision supported by this assessment

Retain the exact existing SB01 manufacturer land patterns and manufacture the
**unpowered, unassembled laboratory PCB test article**, subject to the owner's
explicit acceptance of proposal `SB01-FAB-LOCAL-01`. No controller, board, copper,
component, rule or Gerber change is recommended or performed by this assessment.

This closes the geometry/classification investigation for ordering a test article.
It does not close powered electrical insulation qualification. The proposal is
ready for human review; it is not signed or accepted by an agent. Ordering is not
performed and the full Toolkit release remains FAIL.

## What the five controlling results mean

- BR1.1/3 and BR1.2/4: nominal 1.50 mm drawn gaps match Diodes MB10S-13 suggested
  lands, DS39045 p4: 2.50 mm pitch less 1.00 mm pad width.
- U1.2/4: nominal 1.94 mm matches PI's SO8 reference lands, two 1.27 mm pitches
  less 0.60 mm land width.
- U1.3/4: nominal 0.67 mm matches adjacent PI SO8 reference lands, 1.27 minus
  0.60 mm. It cannot become 2 mm while keeping these exact lands.
- D1.1/2: nominal 1.50 mm is the Diodes US1A-US1M suggested SMA pad gap G.

Literal dimensions and native pads were checked independently. The extra millionths
in the geometry report express numerical approximation, not factory precision.
No guaranteed soldered gap is claimed.

All 18 associated short-escape observations are uniquely contained in five
freshly anchored B.Cu package regions. No via, zone, other layer, unrelated track
or whole high-voltage net receives a concession. Actual inside/outside copper
pieces were checked: original matrix targets remain in force outside and across
regions. All 55 net pairs were checked; no outside/cross-region residual remains.
The 1 mm copper-edge target remains unchanged and the measured CAD minimum is
approximately 1.05 mm. The local values 0.60/1.80/1.40 mm used by the diagnostic
are analysis parameters only; this proposal does not install them as electrical
design minima or replace any native rule.

Thus the 23 entries are not 23 independent routing defects. They document five
fixed land-pair constraints and their local approaches. The original strict
comparison **still reports FAIL23** and remains in this packet. A scoped diagnostic
PASS is not a strict PASS or an accepted safety waiver.

## Voltage stress: why powered acceptance stays open

BR1 output and AC pairs see high input-related stress. U1 M/FB are small voltages
only relative to the moving SOURCE node; their differential to DRAIN during the
OFF interval is near the high filtered rail. D1 has high reverse stress during
the MOSFET ON interval. Do not classify these pairs as low-voltage control gaps.

253 VAC has an ideal sine crest of 357.8 V, but that is not the rail's all-operation
maximum. The existing simplified 47 ohm filter screen predicts conditional C1 and
C4 peaks of approximately 706.3 V and 588.7 V. These are not measurements or upper
bounds; nonlinear inductance, actual MOV action, retained charge, source parasitics,
converter loading and the complete surge/fault envelope remain unbounded. A generic
400 V screen therefore does not close startup stress. The IC's 725 V and rectifiers'
1000 V ratings do not rate the external PCB gaps.

No applicable normative derivation proving these smaller finished clearances
sufficient has been supplied. Manufacturer recommended lands demonstrate footprint
conformity; they are not a full-product insulation certificate. Finished copper
edges, leads/solder, pollution/CTI/altitude, transient/high-frequency stress and
guarded powered qualification require separate evidence. Solder mask receives
no safety/creepage credit.

## Exact test article and manufacturing evidence

PCB SHA256: `532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8`.
The original 51.2 x 33 mm, two-layer, 19-position LYT1603D board is retained.

Use the unchanged R1 file `SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip`, SHA256:
`b722078ed3668e1df757de855754dd7aefc925b9fc8617b28dd7493ece55490e`.
The independent current-source fabrication recheck passes. It compares Gerber
copper, mask, pad/via contacts, outline and Excellon holes to native geometry.
That supports physical fabrication of the bare board, not operation at 230 V.
Select FR-4, 2 layers, 1.6 mm, 1 oz, lead-free HASL, green mask and white legend.
No JLCPCB assembly/stencil or supplier order is included in this proposal.

The complete R1 source/BOM/assembly/unpowered inspection packet is retained at
`../routing-verification-SB01-R1/`. No new Gerbers are generated merely to rename
the spacing result. Incoming board and later unpowered assembly must be inspected
against the exact source; manual soldering/lead forming can alter actual paths.

## Owner decision required

The proposed exception concerns **manufacturing the unpowered test article only**,
with the five exact pad pairs and eighteen exact local escape observations in the
source-bound geometry manifest. It does not accept powered use, a finished lamp,
dielectric adequacy, hot-plugging or an unspecified blanket reduction of clearances.
It does not close the full Toolkit's product/measurement/process gates.

The project AGENTS instruction is explicit: “A deviation requires a rule ID, exact
objects/scope, electrical or manufacturing rationale and human approval.” This
packet supplies the concrete scope and rationale. Only the actual owner can accept
it; the current request to assess the gaps is not recorded as a fabricated signature.
Four separate final reviewers inspect this same frozen proposal before it is sent
for that one decision. No source change or live test depends on elapsed time.

## Primary references

- [PI LYTSwitch-1, SO8 reference lands p11 and validation checklist p6](https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf)
- [Diodes MB10S, suggested MBS lands p4](https://www.diodes.com/datasheet/download/MB10S.pdf)
- [Diodes US1A-US1M, suggested SMA lands p4](https://www.diodes.com/datasheet/download/US1M.pdf)
- [JLCPCB fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities)

Per-pair normal/startup/fault interpretation and exact current region/UUID evidence
are in the accompanying stress and geometry reports. No physical measurement was
performed for this assessment.
