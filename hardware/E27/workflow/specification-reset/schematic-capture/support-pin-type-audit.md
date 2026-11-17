# SCH-PIN-AUDIT-02: truthful ERC types and physical display

2026-11-17. Read-only support implementer /root/support_design. Read device-repo/AGENTS.md, the installed implementer instructions at manifest05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822, approved-map/local-terminal-contract and native pin bases. Coordinator supplied approved graph digestb6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57; this report grants no approval. Root alone writes CAD/libraries. No shared changes or checks on a generated user schematic occurred. Inspected intended-connectivity.json file SHA256b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a; this file-byte hash is distinct from the supplied approved graph digest.

## UCC28711 truthful symbol types

Native SLUSB86C p3 functional table is authoritative; native sourceSHA256762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248.

| Displayed pin | Type recommendation | Reason / approved net |
|---|---|---|
|1VDD | power_in | Controller bias supply input, VDD. Its internalHV startup switch can charge the external capacitor, but that does not justify making it an always-present power_out to clear ERC. |
|2VS | input | Senses auxiliary voltage/timing through divider, VS. |
|3NTC | input | Thermal shutdown sense, NTC. Internal pull-up current is not an external logic-output function. |
|4GND | power_in | Bias/driver return reference, PRIMARY_GND; not a fabricated output source. |
|5CS | input | Current monitor viaRLC, CS. |
|6DRV | output | Actual gate-drive output, DRV. Do not makepower_out orpassive to change checking behavior. |
|7HV | power_in | Receives rectified high-voltage energy for internal startup switch, BULK_POS. Marking itpassive/plainlogicinput merely to suppress supply ERC would conceal its power-entry role. |

All seven real pins are used. Display functional numbering1..7. Upper-rightHV7 occupies the geometricSOICslot oppositeVDD1; the position oppositeVS2 is absent. Keep the largerHV–DRV gap. Do not draw an additionalNCpin8 or use a genericSOIC8 footprint unchanged. Generic appendix position8 forHV must remain documented as the native functional/geometric numbering discrepancy.

## ERC source limitations: keep findings honest

Passive connectors, bridge/rectifier terminals, transformer windings and resistors need not be retaggedpower_out to make the report green. Their physical functions remain passive even though the full circuit transfers power. Q1gate can truthfully beinput; source/drain/tab arepassive semiconductor conduction terminals, not invented digitaloutputs. UnusedT1pins3/7/8/9 have the explicit approved no-winding/no-connection reason; no other real powered/sense pin should receive anNC marker.

If KiCad reports no-driver on VDD/BULK_POS/PRIMARY_GND or other passively sourced/sensed nets, document the ACTUAL source path and the exact finding. VDD receives startup energy throughU1HV and running energy throughT1/DAUX/RAUX; its declaredinput type does not imply the design lacks those paths. The ERC engine does not establish the internalstartup sequence, inductive power transfer, diode operation or analogue waveforms.

Such findings may legitimately remain in the draft evidence. They are NOT a cleanERCpass or automatic waiver. Preserve their actual severity/type from the report; do not rename anerror as a harmlesswarning. Address true missing wires/pins first. No global suppression, changed pin types or gratuitous buffer/powercomponent is justified solely by the no-driver report.

A PWR_FLAG is not inherently forbidden: a later explicit annotation can describe a demonstrated real source such as the external mains entry or a documented derived supply. But it must have a documented actual source and graph/check impact assessment. Under the current exact28-component intent, do not silently add flags/newfunctionalcomponents or assume annotations are ignored by inventory checks. Root should first retain/report the actual findings; any annotation/intent delta requires the applicable controlled review. A flag proves neither power availability nor startup/safety.

## Physical display and candidate package names

These names were corroborated in the hostKiCad9 library only; root's pinnedKiCad10 library bytes and native dimensions require fresh qualification. No actual footprint acceptance follows.

| Parts | Expected display/mapping from approved source basis | Package candidate / caution |
|---|---|---|
|U1UCC28711DR | Functional1VDD,2VS,3NTC,4GND,5CS,6DRV,7HV; omittedpositionoppositeVS2 | ReviewedlocalSOIC7 with nativegap required; genericSOIC8 is not direct. |
|BR1MB10S-13 | Native1+,2AC,3−,4AC | NativeMBS/localdefinition preferred. HostMB2S/MBLS variants have conflicting numbering/geometry and are not automatic substitutes. |
|T1customEFD25 | Approvedprimary1–5row andsecondary6–10row; used1,2,4,5,6,10;NC3,7,8,9 | LocalnativeTDKB66422W1010D001bobbindefinition;5mmpin pitch/22.5mmrowspacing needs top/bottom/pin1mark verification, not a generictransformer footprint. |
|Q1STN1NK80Z |1G,2D,3S,4drain-tab, bothDRAIN pins visibly represented | SOT-223-3geometry; hostPackage_TO_SOT_SMD:SOT-223-3_TabPin2 merges tab aspad2. It is NOT a direct substitute for the approved explicitpin4 graph. Prefer a reviewedlocalnative4-terminal definition, or separately controlled alias. |
|DCL/DAUX/DOUT | LOCAL1K,2A; cathode-band end ispin1 | Diode_SMD:D_SMA candidate. ST exactAsuffix=SMA. Hostcandidatepads1left/2right inlocal0degreeframe; check realband androtation. |
|TVS1 | LOCAL1K,2A; bandK/CLAMP, ABULK_POS | Diode_SMD:D_SMB candidate. UnidirectionalA, notCA. |
|CBULK | LOCAL1+,2− | Capacitor_THT:CP_Radial_D10.0mm_P5.00mm candidate, RubyconF5.0nominal/wire.6mm. Land/drill andleadforming still tocheck. |
|COUT | LOCAL1+,2−; blacksector denotesnegative | Capacitor_SMD:CP_Elec_6.3x5.8 candidate. Panasonic isSMDV-chip, neverradial; nativebase6.6x6.6,H7.8max. |
|CV1/CV2 | LOCAL1/2, nonpolarinterchangeableends | Capacitor_SMD:C_2220_5750Metric candidate. NativeKEMETL5.7±.4/W5.0±.4/T1.7±.15, rather than assuminglandfit from2220name alone. |
|J1/J2 | Project-defined1/2wirepadinterfaces | Localrevieweddefinition, not an inventedproprietaryconnector or userdock-cycle guarantee. |

Native physical sources remain those in schematic-intent/pin-basis-primary.md andpin-basis-secondary.md/source registers. Independent source basis precededCAD; the host library inspection here is conflict detection/candidate guidance only. CompleteERC/connectivity/footprint/ERC-resolution records remain root's fresh-task evidence; no stage, layout or electrical major is closed here.
