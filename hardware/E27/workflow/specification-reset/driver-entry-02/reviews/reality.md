# Reality review — DRIVER-ENTRY-02-r1

**Frozen body:** `8b4c7b90db6bc572f9bc5cc4250d4fdb8cc462e8a3ffd1549c114ae8912aed27`
**Base:** `f0216041fc47fef993e24939c6f31727fe409a14`
**Recommendation:** **ready_for_human_review** for the bounded driver-only preparation packet. **Parent schematic acceptance and PCB entry remain blocked.**

## Actual coverage

Independently read project instructions, the toolkit Reality role, task contract, source/calculation files, layout/verification implementations, routing cards, acceptance ledger, handoff and actual check records. No optimizer/render rerun, product edits or file writes were performed.

- Verified **77 frozen members** against the stated body hash.
- Ran the read-only scalar check: **31 components, 79 pads, 47 same-net endpoint checks**; no reported courtyard conflicts, outline overruns, opposite-face THT planning obstacles or semiconductor courtyards under T1.
- Confirmed projected primary/secondary pad-box separation **10.225 mm** and minimum pad-edge distance **0.600 mm**. These remain planning results.
- Reconstructed the listed sensitive-connection distances, including both U1/C2 bypass endpoints at **1.412453539 mm**. Opposite-face projected proximity does not establish actual via placement, routed loop or effective bypass.
- Independently checked all six inductance matrices: positive eigenvalues, preserved primary inductance, balanced-energy identity and pair short-circuit Schur complements. Nominal P–S and P–A values reproduce **14.061521 µH** and **23.207579 µH**.
- Independently reproduced the 253 Vac ideal cold-charge screen: **1.152162 J**, **8.013349 A peak**, **0.02580430 A²s**, **803.7 µs RC**.
- Independently hashed both retained official Vishay PDFs and inspected their native text. Document 28909 supports the stated **230 Vac** fail-safe test and **17 × 10 mm** AC05-CS maximum body dimensions. Document 28897 explicitly makes permissible pulse loading dependent on waveform and duration.
- Inspected native 79-pad comparison evidence, actual ERC output and the preview/render implementation. Native comparison reports approximately **1.78×10⁻¹⁵ mm** maximum difference; ERC reports zero violations. Requirements/work checks still fail with exits **1/2**.

## Findings and retained blockers

**No new bounded implementation defect identified.** The preparation claims match the checked evidence and preserve the following major open conditions:

- **R-DE02-01 — Controller/fault evidence.** Owner: power designer/coordinator. The surrogate does not establish startup, retry injection, short/open behavior, VDD/VDS limits or independent NTC-open safety. Closure requires bounded device/state and pulse-energy evidence across declared conditions.
- **R-DE02-02 — Input protection coordination.** Owner: coordinator with qualified component review. The ordering-derived fusible R1 candidate is unapplied. The 230 Vac test does not qualify 207–253 Vac coordination, hot/repeated exponential charging or adjacent heating. Closure requires exact identity and supported R1/F1/BR1 operating/fault bounds.
- **R-DE02-03 — Finished magnetics and insulation.** Owner: transformer designer/builder and insulation reviewer. Positive definiteness establishes mathematical consistency, not manufactured leakage, saturation, loss, temperatures, construction or insulation. Closure requires the finished construction/parameter/process evidence already specified in the ledger.
- **R-DE02-04 — Routing, mounting and thermal conditions.** Owner: coordinator/assembly designer. Bypass vias, Kelvin/quiet returns, remaining sensitive connections, RT1 thermal coupling, actual mounting boundary and assembly capability remain unqualified. Changed positions/sides do not inherit the previous whole-lamp assembly fit.

These are retained parent-stage blockers, not newly imposed prerequisites or requests for unavailable software/standards.

The preview honestly depicts an analytical rectangular driver arrangement without copper routing. Neither its appearance nor successful geometry/ERC checks demonstrate an operating or manufacturable PCB. No product-stage approval is given.
