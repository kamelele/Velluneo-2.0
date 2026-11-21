# CAT15 — all components orderable; factory-wound stock transformer

Owner explicitly requires a complete off-the-shelf factory-wound transformer, no
customer winding/custom magnetic build, and every BOM item orderable. Prefer JLCPCB
catalogue/assembly; use reputable outside distributors where necessary. Base is
b31e08da7c2b7e2b81717df6e9f2d094b04fed39. RFQ13 custom transformer and JLC14 quotation
are not accepted for this new sourcing requirement. Do not order their old files.

Root owns all CAD, library, contract and integration writes. Read-only implementer
research contexts may audit transformer candidates or BOM sourcing; four separate
final roles review the frozen integrated candidate, not their own implementation.
Use the unchanged pinned toolkit manifest b985a9eeecaddc992dba2d7d78808b55441e206ca279b148bbc0b9351af14d97.
Preserve requirements for isolated CC driver, E27 207..253Vac49..51Hz, replaceable
simple LED panel,750..850lm, overall target diameter60x120mm and rectangular driver.
18..27V/~250mA is a previous analytical interface candidate, not an immutable owner
rating; verify optical/electrical implications of any changed operating point.

Acceptance: dated exact manufacturer part/LCSC codes with actual observed stock,
MOQ/package/assembly status or truthful unavailable status for every position;
factory-wound transformer datasheet with pinout, ratios, Lp/current/leakage,
isolation/working conditions and dimensional compatibility; source-based electrical
and mechanical assessment; no guessed stock/ratings or arbitrary swaps. Match
schematic/BOM/footprints/pin intent/routing as required and run affected native,
connectivity, spacing/CAM checks before claiming a revised PCB. Retain real
physical/process/human gates. No supplier message, account upload, fee, order,
payment or physical test is authorized. Save concrete changes/evidence on existing
GitHub review branch; do not force-push or merge main. If a complete electrically
suitable stock solution cannot be established, record the exact remaining gap
and do not present a candidate list as a completed selection.
