# FOOTPRINT-01 independent Reality review

Reviewer: /root/spec_reality. Date: 2026-11-17. Read-only inputs; only this report written. Read project AGENTS and pinned Reality Checker role. Implementer/source-audit notes were treated as inputs, not independent approvals.

Recommendation: **ready_for_human_review for bounded candidate-library transfer only**. No new publication blocker or native copper/pin mapping error found. This is not schematic-stage, PCB, assembly, insulation, electrical or safety acceptance.

## Exact inspected packet

Manifest SHA256: `a3f351dd2f27b40ae531ba18f56a3d6c625698d1f3a623b64981dce71ee745f2`. Independently recalculated all 36 member hashes: 36 matched, zero mismatches. Complete checked inventory below; paths relative to specification-reset.

## Independent engineering coverage

Inspected actual three .kicad_mod sources, source-derived contract, generator/checker, local footprint-table resolution, schematic assignments and source/library metadata. Independently extracted and asserted every candidate pad number, centre, size, SMD type and F.Cu/F.Paste/F.Mask layer tuple against the manufacturer dimensions inspected below. All 15 pads match. Reviewed recorded native 10.0.6 loading/geometry and current connectivity/ERC/requirements/full-work reports; I did not independently rerun KiCad. Tool pass records are not physical evidence.

- TI UCC28711: native PDF p3 functional pin table/top view and rendered p36 land drawing; 1.55×0.60 lands, 5.4 column spacing and 1.27 pitch. Seven functional pads 1 VDD / 2 VS / 3 NTC / 4 GND / 5 CS / 6 DRV / 7 HV. Actual HV7 is upper-right, absent adjacent position preserved, HV-to-DRV centre gap 2.54. Generic mechanical drawing's geometric position 8 is explicitly reconciled with the device's functional 7. No accidental pad8 or compressed right row.
- Diodes MB10S: native rendered p1 top-view pin diagram independently confirms upper-right1+, lower-right2AC, upper-left3−, lower-left4AC. Native p4 land drawing gives 1.00×2.15 lands, 2.50 column spacing, 7.50 outside span: row spacing 7.50−2.15=5.35. Actual candidate matches. Maximum body width 4.95 exceeds copper width 3.50 and is accounted for separately.
- ST STN1NK80Z: native p1 functional identification and rendered p8/p9 package/land figures confirm 1G/2D/3S plus separate physical drain-tab4. Three 1.2×1.5 pads at 2.3 pitch and tab3.3×1.5, centre-row distance6.4, correct tab-opposite-lead orientation. Both drain terminals retained.
- Exact schematic U1/BR1/Q1 MPNs and Footprint properties resolve these local candidates. Existing graph report retains approved intent digest b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57, 28 components/73 terminals/21 nets/4 NC. Recorded ERC0 retains four named default ignored checks; this is not comprehensive validation. Requirements U05–U09 and full-work failures remain visible.

## Findings and retained actions

No new actionable defect blocking this bounded transfer. SCH-LIB-001 remains open/partially addressed: only three of28 items have these candidates; complete source-backed library, transformer construction and panel/interface definitions remain due. Before assembly/placement qualification, select fabrication/assembly process and check mask/paste margins, copper shape, courtyard, markings, part fit, solderability and placement clearances. Rectangular copper and provisional courtyards are explicit project choices; no manufacturer-approved margin, body-fit measurement or insulation claim is inferred. The pad/body containment check is narrower than board DRC or assembly clearance.

SCH-ANN-001 native nonnumeric-reference export warning remains open. RC-BIAS-001, RC-COMP-002, RC-MODEL-001, RC-CTRL-MODEL-001, RC-CLAMP-001 and every prior protection/thermal/electrical major retain their prior status; no closure from footprint geometry/ERC. No actual startup, switching, fault, heating, isolation, surge or physical fit measurement was reviewed or claimed.

## Native source hashes

- bias-repair/source/ucc2871x.pdf: 762813589e339955cd318f19958f101c259a97ca750a29b12ac94038a1645248
- tmp/pin-basis-a/mb10s.pdf: a46066843f6b010bffdb85fe3162573330e70bd481df3c5ef9000eeb59e6a77c
- component-study/source/stn1nk80z.pdf: b2e23ffd24302bb78fd42dddbd25155a0833f785765aba20ef38fdff6aabf03b

These are saved manufacturer documents, not fresh web retrievals. I independently verified their file hashes and inspected the stated native diagrams/extractions. No claim of a newer package-outline revision.

## Verified frozen members

| Path | SHA256 |
|---|---|
| hardware.json | 432bf71f6310d038bc77722c4355e1aaa772c9a0123936b1346993e4e5b3efe0 |
| fp-lib-table | 43087dad28dd81785c75c80de00a43e57a804233247bb1ab231fefd394afccb5 |
| Velluneo_specification_reset.kicad_sch | 3882e395df609ba96ab8ad3c27895e292103eef1d19bd9ffe491c0cf10826fcd |
| Velluneo_specification_reset.kicad_pro | a0f1aed1d2d10ccad132f3f162c666494c14c25cae67ec5490c3efa1f4455a7c |
| sym-lib-table | ae491b3cef7acb7c1cd3a75083670a5e1c99444e4c01e230e3757724fa1ba398 |
| libraries/Velluneo_Driver.kicad_sym | a83b3e6805eab01297799f033350774fd1ac9c280472f7bd2b564abf407caf60 |
| schematic-capture/generate_driver.py | 1ba0871b18f847d629879732b1199496232d56d08c10d555e5a9a5079679e61c |
| schematic-capture/BOM.csv | 314f2d5e55f1db5f1adc9450ff3d7f09df9c2c49fa2ac92756f246abdf913060 |
| schematic-intent/intended-connectivity.json | b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a |
| libraries/Velluneo_Driver.pretty/MB10S_Diodes_MBS_1P_2AC_3N_4AC.kicad_mod | bcb61b86077c0befe787d45ba0b056c501d47edd3b1cdd96596489004b025f4f |
| libraries/Velluneo_Driver.pretty/STN1NK80Z_SOT223_Tab4.kicad_mod | f1b8edf66033160f5165cb03e9bd5d579b107ceceda4ca7340bc40d4d0cf1306 |
| libraries/Velluneo_Driver.pretty/UCC28711DR_SOIC7_HV7.kicad_mod | bbefd0cca0948ac2e7cbb2dd72de07704e9e18e39963371ef723b69b4a102d82 |
| footprint-study/BOM.csv | 314f2d5e55f1db5f1adc9450ff3d7f09df9c2c49fa2ac92756f246abdf913060 |
| footprint-study/MB10S_Diodes_MBS_1P_2AC_3N_4AC.png | 307e5447106e22da718568503fc2ed9ed124b0a1e0ba71ad8ea6aa38b301a8d1 |
| footprint-study/README.md | cc714e42c381137b42f61270dd651e63e0df76d0962e2c28be9ec7b2f39ccbf3 |
| footprint-study/STN1NK80Z_SOT223_Tab4.png | a0601203bdedde07cbbd02cfb92bae7a9dec5df9d86d53cd8a768f34e9d9c4d2 |
| footprint-study/UCC28711DR_SOIC7_HV7.png | e9558956f50107411b7256add6776c262cb172a10a249c7430a8543b89330dcf |
| footprint-study/Velluneo_driver_3_footprints.pdf | 7fb82ff03127b4248f6946aeef985ebc314f5f8a15ae9337d45124c896b6a770 |
| footprint-study/assignments.json | 12002256a71cae27b70eb0e3cbc4982f01627eb55e16cfa2ff02fd787e067b53 |
| footprint-study/check-work.json | 1c3e3a0698b75f871fee0df09596fdbadab21b7b6fe1799175eef78d75aa45ae |
| footprint-study/command-results.json | a7aead32be0181be639d453fc91367f0e34ea49f0cf565ea90583b232eb8e4d8 |
| footprint-study/connectivity.json | 42e3d9444b957c38f10ffc7d39a4225d6cca5b75d6cbd6b4f60725bf073ac610 |
| footprint-study/doctor.json | 3004b39891f39f9e04f109d2b76424e09491471d6536f06e95a3bdd536fe7c1e |
| footprint-study/erc.json | 6e44402e1c46a7a50af15706c7b9cd6785dc70514f709058a3b99e68d8fa260c |
| footprint-study/generate_critical_footprints.py | 3d425259ca4633f75d6d9eb489011040a135b8feeea4f53ba97096b49a788ff4 |
| footprint-study/geometry-contract.json | 64aaa5af681733ac94767242f42f7430ccfd602e6ea219de1e8b540ec7613e3a |
| footprint-study/native-geometry-check.json | 6279c78ca700f7956fbb6b9dfe4d7bd12b8b5123fa8e9633a3a6f47552b09547 |
| footprint-study/native-stn-basis.md | 77f957bffa983df2b2a6c474db9845720830e0cd9a1636b993046dcb12b7bd91 |
| footprint-study/native-svg/MB10S_Diodes_MBS_1P_2AC_3N_4AC.svg | 45342df2c00cd96b821c315b70b5817374810eab97bc512f9bbd332ea89aa7f4 |
| footprint-study/native-svg/STN1NK80Z_SOT223_Tab4.svg | 5bc47d32946fcfdd8f6d77885857523cf3ed741fd6099db7533c96099a18b1a2 |
| footprint-study/native-svg/UCC28711DR_SOIC7_HV7.svg | f265edd32a025efe9681ea320ec84b0e89a6a9f3bf436173f641f191e9a7cca2 |
| footprint-study/native-ucc-mbs-basis.md | 875bd96ce642841fe56af28e181a671560b49d6f6b7989a722d003630c7897f5 |
| footprint-study/native-ucc-mbs-geometry.json | 25fab371c12bb70853cabb4595feacb09ec860b3cbe5e789ef1146fdb21c2af7 |
| footprint-study/requirements-schematic.json | 2533ce43dcf30924ed6c638778a49207a0b76d81b2e330642bb4682c946fb174 |
| footprint-study/task-contract.md | 4da3b1bba42ad689e85dbad1f2e1a52d51bc18899559590227ab119bc32efa87 |
| footprint-study/verify_native_footprints.py | 72dbfbd0ad9e8a8b37e1b0344822856c494252014ec31f4ee6e099b0158294af |
