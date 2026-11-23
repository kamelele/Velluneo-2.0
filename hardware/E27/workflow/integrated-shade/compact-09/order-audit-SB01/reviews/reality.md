# SC09-SB01-AUDIT01 — final Reality Checker review

Actual reviewer: `/root/sb01_reality_audit`. Independent read-only review of the exact frozen packet `work/sc09-order-audit/review-inputs.json`, SHA-256 `5cb5713b8c8022d10d00ff0d733fccac21ca4e5dec82153a35e4da2f4df7c34c`. All 202 referenced file hashes verified. PCB SHA-256 remains `a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`. No source changes, measurements, purchase or order occurred.

## Recommendation and scope

**Ready for human review of the bounded audit and laboratory fabrication candidate only. Not order-ready release, energized-test authorization or consumer-product qualification.** The compendium accurately distinguishes native manufacturability from exact-source acceptance and actual physical operation. Full release remains FAIL, as does full strict spacing with 23 conditions. No previous ROUTE05 acceptance is transferred to SB01.

## Independent evidence

The nominal electrical calculations were independently recomputed: 60 V /133.439 mA external LED current yields8.006 W;135.203 mA total includes1.765 mA bleeder loading. At proposed52/68 V the same current setting yields approximately6.951/9.058 W. With assumed1.1–2.1 W losses, nominal Pin9.106–10.106 W and external-LED electrical efficiency79.22–87.92%; assumingPF0.9 gives43.99–48.82 mA RMS at230 V. These remain conditional calculations, not measurements or all-load guarantees.

Primary Würth, Power Integrations and Lumileds datasheets independently confirm the selected part limits and their conditions. The T1 conditional58–107°C scenario is not a thermal pass and its upper case exceeds the retained90°C target. Other listed component temperatures are criteria/stops, not predicted readings. U1 protection senses its own junction, not the LED panel, C6 or T1.

A fresh independent native probe verifies twelve critical physical pin/net maps, no BP/M copper under T1 and no U1.3-to-R5.2 Kelvin sensing path under T1; source hash remained unchanged. Fresh manufacturing exports and native checks are a separate implementer handoff, not physical electrical qualification. No package exception or modified global rule was introduced by this review.

The final 8-page PDF text and HTML/data compendium were reviewed for CC versus CV, nominal versus load-window power, unmeasured temperature/efficiency/optical labels, no-SELV output, retained spacing failures, actual port orientation and the small T1 package-description inconsistency. Description1280 is obsolete; exactMPN7687709152 is manufacturer size1210. Compendium discloses this; exactMPN and pad/body dimensions remain the purchasing/geometry authority.

## Findings disposition

REAL-ORDER-01 remains open for exact-source fabrication acceptance: full functional-spacing FAIL23 cannot be relabelled as passed by nativeDRC or matching earlier numerical signatures. REAL-ORDER-02 remains open for current/ripple, startup/hot restart, nonlinear input choke, surge/MOV/fuse/fault and thermal qualification. REAL-ORDER-03 remains open for completed LED interface, actual harness, mounting, access barriers and enclosure insulation. Stored C6 charge permits direct LED reconnection current independent of controller current regulation; no powered hot-plug is allowed.

REAL-ORDER-04 and the documentary part of REAL-ORDER-05 are verified closed in this compendium: conditional parameters, absolute part ratings, stop criteria and physical evidence are explicitly separated. Numeric test margins must still be chosen by the competent test owner before powered testing. No reviewer approves fabrication or energized operation.

See `reality.json`, `reality.facts.json` and `reality.native.json` for structured findings, primary-source references and probe evidence.
