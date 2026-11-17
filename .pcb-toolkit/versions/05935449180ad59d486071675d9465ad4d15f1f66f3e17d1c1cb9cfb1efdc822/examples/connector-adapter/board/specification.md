# Fictional passive connector adapter — tutorial specification, revision 1

Original non-confidential training design. No customer geometry, manufacturer part
or physical/process qualification. Do not order or energize it as a finished product.

| Requirement | Independently specified acceptance |
|---|---|
| REQ-SCOPE | Passive continuity teaching fixture; hypothetical bench ceiling 5 V / 10 mA, no mains, isolation claim, high speed or power load |
| REQ-PINS | J1 pin 1 -> J2 pin 1 (LINE_1); J1 pin 2 -> J2 pin 2 (LINE_2); lines remain separate; no unused pins |
| REQ-GEOMETRY | Rectangular board 30 x 20 mm; connector pin-1 centers (7.5, 8.73) and (22.5, 8.73) mm; pin 2 is +2.54 mm in y |
| REQ-COPPER | Two F.Cu straight tracks, 15 mm length and 0.5 mm width; fictional 35 um copper for arithmetic only |

The coordinate origin is the top-left board corner. Both original generic connectors
have 1.0 mm holes / 1.8 mm pads and illustrative courtyards. No actual mating part,
pin diameter/tolerance, body height, keying or assembly envelope has been qualified.
The symbol pins are passive because these components are passive connectors.

The four profile layers are common toolkit policy, these fictional product inputs,
JLCPCB candidate fabrication preferences, and candidate in-house assembly. This is
a tutorial selection, not an endorsed vendor or owner-approved order. Concrete service,
stackup, copper, finish and process confirmations deliberately remain unset.

First-pass copper estimate: R = rho * L / (w * t), using declared illustrative
rho = 1.72e-8 ohm*m, L = 0.015 m, w = 0.0005 m, t = 0.000035 m:
R ~ 0.0147 ohm per track; at 0.010 A, drop ~ 0.147 mV and loss ~ 1.47 uW.
This excludes contacts, tolerances and temperature. It is no current rating, thermal
qualification or permission to apply power; no physical measurements exist.

Release questions: choose actual connector and verify datasheet/footprint/pin numbering;
confirm fabrication and assembly; review handling, labeling, mechanical fit and test
limits; obtain genuine stage approvals and current manufacturing/inspection evidence.
These block release. No insulation/safety applicability decision is inferred from CAD.
