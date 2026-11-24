# Review report — SB01-R2-REALITY, validated positions closure

- Task/stage: same-board SC09-SB01-R2 engineering candidate; final targeted re-review of positions export and assembly bindings before a human review decision.
- Role/actual actor: independent Reality Checker `/root/sb01_r1_final_reality`, distinct from implementer and startup/protection contributors.
- Exact frozen core: `outputs/SC09_SB01_R2_rozruch_validated/core-manifest.json`, SHA256 `ddb90c1270fbfce6e8b64862b64e442b1f56bc66d86071a32232ea3b73235e80`, 231 files.
- Candidate PCB SHA256: `0889e1d7a701c26b89750c4e1a42a170efc6a5b30669d75d5abded6ff8b69bbe`.
- Recommendation: **ready_for_human_review**, limited to the R2 same-board engineering proposal and a possible decision about a bare, unpowered laboratory test PCB. This does not approve integration, manufacture, ordering, energization or product safety.

## Evidence and targeted coverage

This report extends `review.md`, whose corrected second-freeze binding was `b5c578d7edaed2f04e788c98acd91a8196c7ce51ed601b842e85e3fe25d3a19a`. I independently verified every hash and byte count in the new 231-file core. All 26 analysis files are exactly identical to that reviewed freeze. Native PCB, schematic, unchanged-copper/graph proof and retained manufacturing ZIP are also byte-identical. Therefore the prior physics, source, geometry and limitation assessment is explicitly retained by exact identity, rather than inferred from a similar revision name. No broad physical simulation rerun is warranted by a positions-document correction.

I directly parsed the new native positions CSV: 19 unique references, with L1 value `100R / RC DAMPER`. Every reference's X, Y, rotation, side and package matches the former positions export. Hardware now points to the R2 CSV, SHA256 `aa6d3e05d0cdd11495a78301c9c05dd299c88be72ee25a5a66e2dfe84d7da898`. Both front and back assembly files resolve and match their recorded hashes. Actual native-final4 commands return zero; fresh native ERC/DRC, actual parts and fabrication-geometry reports pass in their stated scope. The eight canonical R1 source guards still match: this review did not adopt or edit candidate/source/core files. Own checks and results are recorded in `verify_validated.py` and `validated-verification.json`.

## Findings and retained limits

The prior active CSV/selected-part and both-side assembly findings remain closed, and the stale active positions export is now closed by the checks above. No new major finding is introduced by this targeted correction. The minor historical `unchanged_critical_parts` wording caveat in procurement remains as described in `review.md`; current selected BOM, purchase row and explicit R2 intent govern.

Strict spacing **FAIL 23** and full Toolkit **FAIL** remain. The reviewed positive-RC maximum principle is for the specified unloaded ideal bridge and bounded source/initial states; 357.8 V is not a real surge ceiling. The 512-case startup screen and PR02-FS pulse-curve comparison do not qualify hot/repeated pulses, active-converter operation, mains surge, MOV dynamics or wiring parasitics. R10's verified .4059 W at assumed 60 mA RMS and .7216 W at 80 mA are not measured operating temperatures or efficiency. Actual RMS, rail/U1/T1 stresses, OVP dynamics, faults, thermal behavior and EMI remain physical qualification gates. U1 short failure can defeat internal protection and overcharge C6; input fusible parts do not establish output fail-safety. Formed-resistor fit/support/clearance needs actual sample inspection. The 90 degrees C body stop and 90 V COUT investigation level are planning thresholds, not protective trips.

Qualified human electrical/insulation/fabrication decisions and a separately engineered powered test setup remain unavailable. No measurement, provider confirmation, owner approval or safety certification is invented. Any later source, part, geometry, model or evidence change invalidates its affected review scope and requires explicit re-binding.
