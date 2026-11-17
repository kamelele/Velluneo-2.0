# Independent fictional pin table

Original non-confidential specification for connectivity verification fixtures only.
This is not a real component, device design, datasheet, human approval or insulation rating.

U1 is a fictional four-pin, two-unit passive symbol: unit A contains physical pins
1 and 2; unit B contains physical pins 3 and 4. J1 has one unit A with pins 1–4.

| Intended net | Required physical pins |
|---|---|
| N1 | U1.1 and J1.1 |
| N2 | U1.2 and J1.2 |
| N3 | U1.3 and J1.3 |

U1.4 and J1.4 are deliberately unused and must each carry explicit NC indication.
N1 and N2 must remain distinct electrical nets. This is not a physical isolation
requirement and defines no clearance or creepage value.

This pin table is authored before the schematic fixtures and is not extracted from
their netlists. Deliberately incorrect fixture variants must not change the expected table.
