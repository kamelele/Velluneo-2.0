# SB01 R2 — first laboratory prototype desk review

The existing51.2x33mm,2layer PCB is retained byte-for-byte. No part, physical pin, net, track, via, mask, legend, outline or drill change is required by the final normal-operation and assembly desk review. Selected fabrication remains FR4,1.6mm,1oz,lead-freeHASL, manual assembly. This engineering head is not a full product release or powered-test authorization.

Physical legacy **L1** is **PR02FS0201000KR500,100ohm,10%,2W**; it is R10 only in calculations. Do not fit the old768772332 choke. RF1 is47ohm FW20A47R0JA. T1 is stock **7687709152,1.5mH,WE-PD HV1210**, not a custom transformer. C6 is **EEUFS2A151**,150uF100V,12.5x20nominal/13x22max; the different151L body is not permitted.

Input207–253VAC50Hz; external LED current approximately133.4mA at60V, about8W, intended20seriesLED. Proposed52–68V load window is conditional at its hot upper end because OVP discrimination is not guaranteed. Normal-loss budget1.24–1.69W and82.5–86.5% efficiency are engineering estimates, not measurements. All output nodes remain mains referenced; noSELV and no hot-plug.

Module height is **20.5mm nominal-board planning**, **20.66mm with maximum PCB thickness**, before forming/solder variation. The previous19.5mm and achieved20mm claims were incorrect.16mm formed top resistor+1.6mm board+2.9mm bottom BR1 govern. Trim lower THT projections<=1.5mm; preserve upper forming stand-off and C6vent5mm. Wires/support excluded.

Use NORMAL_REVIEW.SB01-R2.md, ASSEMBLY_REVIEW.SB01-R2.md and their source-bound JSON contracts. Purchase-only options must match the explicit purchasing list; no unreviewed generic resistor, coil or capacitor substitution. Legacy snapshots and previous workflow packets are history, not current performance.

Native manufacturing checks and bare-PCB disposition are separate from full toolkit release. Strict2mm comparison retains23 localized BR1/U1/D1 land/escape findings; manufacturer land geometry and local prototype assessment do not establish safety insulation qualification. No global clearance relaxation was made. Dynamic startup/OVP, hot pulse behavior, EMI/surge and fault qualification require actual controlled prototype measurements. U1D-Sshort is not guaranteed to protect100V C6 through an ordinary input fuse.
