# POWER20 analytical integration

Base797d9038d55b0de8747ac0b48bde627f376da408; final analytical body
76281eaffbfe69ac237813ede9a77306e7acc4c0625510c4d35edb19122f6c29 (14files).
Coordinator/solewriter /root; actual research and four separate read-only review
actors are identified in task-contract.md and review-status.json.

Nominal accounting: input8.585985W, LED6.540272W, driverheat2.045714W,
LED efficiency76.1738%, input69.7341mArms, PF0.535325. Across97selected cases,
input7.827984..9.924398W and heat1.490443..3.168220W. These are conditional
screens, not real efficiency measurements or guaranteed loss bounds.

The319mA controller allocation includes the output bleeder: nominalLED316.936mA.
Magnetic/clamp/bias energy stays inside etaXFMR; startup VDD feed is counted once.
Charge and independent line-source power ledgers close within reported numerical
tolerances, but do not validate physical switching/charging waveforms.

All339 prior C16/C17/VIS18/LED19 files and bound requirements retain exact bytes.
The only old-file edit is15 inserted index lines; the previous index bytes are
preserved exactly. No CAD, BOM, rules, stackup, approvals or manufacturing files
change. Pinned toolkit doctor passes with explicit CLI/pcbnew10.0.6; default
runtime probes were rejected, never treated as passed. Formal requirements/
ERC/DRC/release checks are not repeated because this is a new analytical task,
not a CAD/configuration or stage transition. Existing physical/process/human
holds remain open. No supplier communication, order or physical test occurred.

Review corrections: ESR omitted from charging impedance is now explicit; maximum
total-heat case is not a per-component envelope; C1~98.5C exceeds the tentative85C
reserve goal despite satisfying the assumed transformer-air path; measurement
plan reuses the accepted revision12 equilibrium/setup instead of an alternate
15minute criterion. Index line-ending normalization was removed. Independent
reviewers checked closure; all four final reviews cover the same final body.

All roles recommend ready_for_human_review for analytical delivery only. Actual
transformer/capacitor internal rise and enclosure heat paths remain unestablished.
The3.16K/W effective cavity target at40C with zeroLEDcoupling (2.00K/W at25%
coupling) follows selected-case heat, not qualified construction. No ordinary
printed shell, particular vent/radiator or guessed thermal path is accepted.
Source-backed estimates support the next thermal/mechanical design decision;
they do not close cooling, lifetime, fault, safety or manufacturing qualification.

Publication is to the existing GitHub review branch
spec/owner-interview-reset-2026-11-14, not a main merge or manufacturing approval.
The coordinator verifies final GitHub tree blobs/sizes against every local packet
file and the remote branch commit before reporting delivery.
