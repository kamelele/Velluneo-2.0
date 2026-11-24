# R2 unpowered inspection only

Fit PR02FS0201000KR500,100ohm/2W at legacyL1; do not install old3.3mH choke.
Retain RF1=FW20A47R0JA. Check exact resistor marking, sample lead diameter,
formed lead strain/support, >=2mm standoff and <=16mm planning height; retain
original C6 vent free space. Inspect high-voltage clearances including solder.
Check no short and intended continuity without power. This file authorizes no
energization. A qualified human must define setup/stop conditions separately.

Before powered acceptance measure both input rails, U1D-S and T1winding stress,
LED current/OVP/short response, R10RMS/bodytemperature and EMI at input/load/
temperature corners. Cold RC calculation does not close hot pulse or surge tests.
Record actual data, not a fabricated PASS. Stop at unexpected current/ringing,
any part limit, R10body90C provisional stop or COUT90V investigation threshold.
Thresholds are test planning, not protective trips. U1D-Sshort can overchargeC6;
do not perform that destructive fault test without a separately engineered setup.
