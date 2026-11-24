# SC09-SB01 R1 — receipt and unpowered manual-assembly plan

This plan applies to the existing 19-position LYT1603D board, 51.2 x 33 mm. It is
not an energized-test authorization or a record of measurements. Bind the received
board, component lots and actual assembly to the final source/artifact manifest.

1. Compare the received bare PCB with the current Gerber/drill, copper and assembly
   views. Record actual dimensions and supplied FR-4, 2-layer, 1.6 mm, 1 oz,
   lead-free HASL order selections. Inspect plating, mask, drilled holes, shorts,
   broken traces, edge damage and contamination with magnification.
2. Compare all 19 references and 46 physical contacts to the independent SB01 graph.
   There are 17 populated electronic parts and two direct-wire ports, no DNP parts
   or purchased connector bodies. AC J1 is at the right edge, LED J2 at the left
   in the common top-CAD coordinates. Use actual pin numbering and polarity views.
3. Check the exact received parts against BOM.csv. U1 is LYT1603D in tube packaging,
   same SO8 device; do not substitute a different controller. T1 is Wuerth
   7687709152, WE-PD HV 1210, 1.5 mH. The old 1280 text/footprint name is historical,
   not a different part. C1 is KEMET R76QI24705050J; RV1 B72207S0271K101;
   RF1 FW20A47R0JA; D1 US1M-13-F; R6 1206S4F365KT5E; R7 HVR2500003903FR500;
   C6 EEUFS2A151. Do not use the older Coilcraft/T1, TDK/C1 or VR25/R7 records as
   current purchasing, forming or powered-test instructions.
4. Inspect the actual R6 termination overlap and sample fit. Inspect RF1/R7 formed
   leads and support against the current footprint geometry and assembly drawing;
   custom lead forming remains unqualified. Check the horizontal C6 body remains
   in its reserved area and retain at least the documented 5 mm free vent-air space
   beyond its actual vent face. Check its 1 mm geometric body gap to T1 in the
   real assembly. Solder/lead protrusions, stand-offs and wire strain relief need
   inspection; no enclosure fit is established by a drawing.
5. Inspect both faces after soldering for bridges, polarity errors, stressed seals,
   flux residues and unexpected conductor proximity. Verify unpowered continuity
   against the intended graph. Record all substitutions/rework and recheck affected
   evidence. Do not treat an ohmmeter check as dielectric-withstand proof.

The strict 2 mm screen still has five intrinsic land-pair failures and eighteen
local escape observations at BR1/U1/D1. No rule or pad has been relaxed. Actual
soldered clearances and qualified electrical assessment remain open. No solder-mask
credit, SELV output, safety certification or safe handling delay is asserted.

Before any powered activity, a qualified responsible human must define the exact
assembled hardware/load/fixture/wiring revisions, guarded setup, rated probes,
external protection, current/time/energy limits and stop criteria. Output and both
LED leads are mains referenced. No hot plug. Verify stored voltage before handling;
a waiting period is not proof of discharge. Startup, current/ripple, OVP, inrush,
hot magnetics, stability, fault/surge behavior, efficiency and actual temperatures
remain unmeasured. The retained thermal-planning.json and prototype-gates.SB01.json
are conditional planning/test gates, not demonstrated performance. This plan stops
at unpowered inspection and does not prescribe live fault-injection procedures.
