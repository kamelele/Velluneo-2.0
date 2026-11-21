# ELEC-CLOSE-01 r2 — Independent Completeness review

Actor: /root/spec_completeness, 2026-11-17. Read-only shared inputs. Sole output tmp/eclose-review-completeness.md. Recommendation: concrete ECO intent ready for human review only, subject to all four role outcomes; no circuit/schematic/PCB acceptance or human approval.

## Exact final freeze

Final manifest revision2 canonical body digest (excluding frozen_digest): 0f9aaf158b94acc0b9471d9ab57d09223f04b0aaaca79fd2dc78011458cba7e4. Manifest file-byte SHA256: 4ea2c34cb668e81997da89d83a69e8717e59593768cab9667db7f59777bd7740. All85 listed file SHA256 values AND byte counts matched.

Original reviewed r1 canonical body digest d0bed449de92f3fe001c8aa4ec80964b33b2020cca9db06109f059c45ff9d64d and file-byte SHA256 e25887de974160fa001965ba2636bcc969525b183be1529ad820e49eb2c1c5fe were different identity concepts, not a freeze mismatch. r2 changes README provenance wording only: the illustrative40V fault ceiling is explicitly unapproved and separate from accepted service-access goals. Prior unchanged numerical/graph/source scope is retained and bound to final85-file manifest below.

## Actual inspection and limits

Read projectAGENTS and locked completeness role, task/README/ECO/finding ledger, proposed parts/aliases/graph, calculation code/results and integration limits, startup source/hand-off/results/reproduction records, winding/window source/construction/loss records, and actual native-report scope. Independently recomputed proposed graph inventory, digest, basis hashes, terminal membership, parts mapping, barrier coverage and delta against the independently prepared old parts; checked all frozen identities and main available native-source hashes.

No full numerical/controller/native-CAD/STEP run, independent PDF-page interpretation, source-curve redigitization, physical measurement, supplier confirmation or remote-baseline comparison was performed by this reviewer. Existing run logs/reproduction records were inspected as evidence, not represented as this reviewer's execution.

## Inventory, source and authority

Proposed graph:31unique components,79physical terminals,22connected nets,4explicit T1NCs. Every declared terminal occurs exactly once in nets/NC; proposed-parts.json mapping matches. All ten inherited/new basis-source hashes match. Primary/isolated barrier sets are disjoint and jointly cover all22nets including new BLEED_MID_B. Digest recomputes exactly to 5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8; approval remains null.

Reference-alias mapping preserves every old terminal/net membership. Only oldRB1/RB2 manufacturer codes change1206->2512; three new positions are R13/R14/R15. R13 is the proposed1Mohm VDD bleed, R14/R15 the second independent499k series branch. Exact new candidate MPNs and local nonpolar1/2 terminal convention are explicit. Native stock, process and board assignment are not claimed. Old28-component approved intent remains approved at b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57. Current native connectivity/ERC reports test that old graph; none is falsely attributed to proposed31-position intent.

## Requirement-to-deliverable coverage

| Requirement / concern | Evidence supplied now | Retained acceptance / gate |
|---|---|---|
| R-OFFLINE / discharge | Existing resistor one-open/one-short weakness identified; two independent2512 branches and separateRVDD precisely specified; cornerRC/voltage/power arithmetic supplied | ELEC-BLEED-001/ELEC-VDD-001 remain open until actual decision/capture plus common-point/layout, thermal/fault and whole-assembly service evidence; no RC wait-time instruction |
| R-SUPPLY / input life |1152input cases separate old/new bleeder loads and49/50/51Hz; parent arrays/period updated; loss/step-refinement records retained | Averaged CPL model is not inrush/fault/EMI/control proof; capacitor triangle screen is inconclusive, ELEC-CAP-001/RC-INPUT-001 remain |
| R-LIGHT / R-CCT / R-COMPAT | Native typical curve and inherited current screen expose narrow light-budget problem; factory bin/calibration proposed with no user control | No threshold relaxation or one-point family/interchangeability pass; ELEC-FLUX-001 and U05/U09 remain |
| R-FAULT / R-EMPTY / startup | New family cadence/on-time sources correct earlier overbroad source statement;128ramp/768residual-current witnesses and optionalRVDD separated | No corner-certified exact controller state/current trajectory; RC-BIAS-001/model/clamp/fault majors remain |
| R-THERMAL / R-BASE-LIFE / magnetics | Exact wire/grade/tape candidate, packing, native-solid/dimension-only fit and hotDC resistance/loss/drop calculations supplied | No winding insulation/assembly, batch, AC/core/aux loss or measured thermal/lifetime qualification; ELEC-MAG-001 remains and losses must propagate |
| Electrical interface / later PCB | Draft18–27V/300mA/8.1W and heat-path budgets explicitly provisional; J2 internal versus user dock distinction retained |40V is unapproved engineering proposal; accepted service goals are not proven. U05–U09/source/material/mechanical/process gates remain |
| Current native checks | Old approved graph pass, ERC zero enabled findings, doctor pass; schematic requirements fails U05–U09; full configuration check fails | No changed-graph validation, schematic acceptance, board/DRC or manufacture/measurement claim |

The calculation packet distinguishes designed/proposed/calculated/source-inspected/reproduced/physically measured levels. Finite hot winding resistance and incomplete auxiliary/core/AC losses are not silently propagated as if an ideal-transformer calculation already included them. Capacitor bound exceedance and typical-flux counterexample are correctly conditional, not proof every physical unit fails. Supplier/source availability and physical measurements are not fabricated.

## Findings and recommendation

No new Completeness publication defect identified in the finalr2 frozen proposal. The corrected README now clearly labels the40V fault ceiling unapproved; no accepted owner threshold is silently changed.

New ELEC-BLEED-001/ELEC-VDD-001/ELEC-FLUX-001/ELEC-CAP-001/ELEC-MAG-001 are substantive retained design/evidence obligations rather than this packet falsely closing an electrical gate. The proposed discharge ECO addresses specified resistor faults only. All original startup/clamp/model/input/thermal/service/protection majors and U05–U09 remain open at original affected acceptance.

Recommend presenting exact proposed digest5c2b5fdd0654805a576186adb8a9ccc0a041bd4809a9259e448574fd38adeba8 for a genuine owner ECO-intent decision. Do not capture changed graph/BOM/references before that decision; then refresh native sources, views, complete connectivity/ERC/requirements/work results. An owner ECO decision will not accept schematic stage, authorize PCB/manufacture/energization or close current electrical majors.

## Final frozen files verified

| Repository-relative file | Bytes | SHA256 |
|---|---:|---|
| AGENTS.md | 1064 | e022bac38e42e8333705a714360eb53efe3e4649a8d963a747cacbf98414d3b1 |
| hardware/E27/workflow/specification-reset/Velluneo_specification_reset.kicad_pro | 95 | a0f1aed1d2d10ccad132f3f162c666494c14c25cae67ec5490c3efa1f4455a7c |
| hardware/E27/workflow/specification-reset/Velluneo_specification_reset.kicad_sch | 71677 | 8a21535690628f24b807437ba1a38816085650f5e7269a520993c967d94b419a |
| hardware/E27/workflow/specification-reset/driver-study/primary-buffer/calculate.py | 6429 | 432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea |
| hardware/E27/workflow/specification-reset/electrical-integration/ECO-01.md | 4343 | 80f70508070eea487f7d51cb8e78af6680239d5e1ec849e5ec6c2cfa3f252d6d |
| hardware/E27/workflow/specification-reset/electrical-integration/ECO-01.png | 103757 | 298a8c8e03f4be0ae674e1a87a3a55f95a017b8458126da86e5a1625a061ede4 |
| hardware/E27/workflow/specification-reset/electrical-integration/ECO-01.svg | 75103 | 463a9a9cb0a09ca5c6a2c66c793501420f8ad0cf21c2a9e9a0eea2960904781f |
| hardware/E27/workflow/specification-reset/electrical-integration/README.md | 9766 | bf6e9557d1f4307aa481db1a2c21d6d192aed99d7e44ea13d4fab673f3acfe16 |
| hardware/E27/workflow/specification-reset/electrical-integration/calculate-integration-limits.py | 1978 | aaae62a4cb820fbb14c4bf0950bef97bcdc825b503ff3c32bfed649ccb15b22e |
| hardware/E27/workflow/specification-reset/electrical-integration/calculate.py | 6112 | 773b43950468cbe28abae188fa1c76253947712e0044c509fc94555738a5158f |
| hardware/E27/workflow/specification-reset/electrical-integration/check-work.json | 44711 | 17a1bb09af4d29b50c65306bcc05639979ed434b63c9a8b8d59f95c4f08964a0 |
| hardware/E27/workflow/specification-reset/electrical-integration/connectivity.json | 1689 | 9d7598a3f47c8bad61ab48632ffbb41714071e9791e7d7cd646e9c568f4eb1e2 |
| hardware/E27/workflow/specification-reset/electrical-integration/doctor.json | 835 | f690ad7a351246367ad40026443b56233eb62e11af820957a210fb082a4e9946 |
| hardware/E27/workflow/specification-reset/electrical-integration/draw-proposal.py | 1776 | 718456efc35e51e27abb5255ece84cc950a14bcfdb0b41525b5b664881f37275 |
| hardware/E27/workflow/specification-reset/electrical-integration/erc.json | 1022 | f9c000fe43c9d5f2019c29519270f70c146c0d58de7d3154aae54198006888ea |
| hardware/E27/workflow/specification-reset/electrical-integration/findings.md | 3732 | c46b24d011c2120963f768f620e8fb9aea48b39d2f7997bd46824f5e938cdd47 |
| hardware/E27/workflow/specification-reset/electrical-integration/input-corners-results.json | 5224 | a2ba3a610228251b3f825fcdc7375e99e5e4d74a252ca3ee515775a112bf9816 |
| hardware/E27/workflow/specification-reset/electrical-integration/input-corners.py | 3180 | d22f2fcf16bf541a1246946a12a1b9f34052820a2c4ad0a342f9d840a91e642a |
| hardware/E27/workflow/specification-reset/electrical-integration/integration-limits.json | 1483 | f9ff0c6267314c971321007db56779ca2ff0dd74358e5f9d39876e14a0459fcb |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/README.md | 2788 | d7838e8ace48d2536d2ef2b75972dd1e64af910b46f638370e94af492a9c6cc1 |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/artifact-hashes.json | 805 | 3e9119113fefd77e3042c13d41a9d1a1e56a5ee226dfca6c50fa60d5b8e805c8 |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/calculate.py | 4870 | 8b508cb11a05c3720ff1c17c854d773920f3f8dd5ad6e085044af2ef03ebd928 |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/check-window.py | 3310 | 97ecdd8e96d542fd2bc2e5e2b6c5cab8e5d2749919b1af6f212489e29ef017cc |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/sources.json | 3203 | ff1a60d6a59cfd9fa46d827a856c7ff3a6576b7ff7c6859579edc05d1b8cc70d |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/verification.json | 982 | b5583976fdec239a43f092834edcff9fe5af711d1f938a390ce89b2a7aa7f466 |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/winding-proposal.md | 11833 | b294e5428ca5d608863be2bc32e9d2e27a0662b275bf7b44e460c8067f7da71e |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/winding-results.json | 10634 | b4964267013eddb58fa4407792a57809e94894bf56bba8b1fd7a04c83bd78079 |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/window-fit.md | 6918 | 1d5773d322d95db743b366ca45a85bd914b6ab1328df771bda769403b116c383 |
| hardware/E27/workflow/specification-reset/electrical-integration/magnetics/window-results.json | 2117 | 0e495f2bc4aa05baf09bcbad38f53a334d642f8ffdaf18956a97bf8eb7981935 |
| hardware/E27/workflow/specification-reset/electrical-integration/native-runs.json | 39849 | 86bef2ffcb9f0147a88c67706b316196013222f4de2e9ba8ddde039305ab63a9 |
| hardware/E27/workflow/specification-reset/electrical-integration/native-typical-flux-curve.json | 70271 | 3a7909f6873b1b8bda461e43fb587eaf12c797da32d71b9f6e20815f4ffb8553 |
| hardware/E27/workflow/specification-reset/electrical-integration/proposal-check.json | 506 | 7ec0569e1f6abcb01942e4a6d0dace28f91d4974c4cdf1a512eae3dcb4827665 |
| hardware/E27/workflow/specification-reset/electrical-integration/proposed-connectivity.json | 14810 | 8621b97580f9b908169b3076448b1f1a6b5d3aea2b2b13400a6d251c169f5f7c |
| hardware/E27/workflow/specification-reset/electrical-integration/proposed-parts.json | 5140 | 142919c3a4e7eff9e5dc176639d2e9aff4432bf53173a2ee26e2552cd0cab5ae |
| hardware/E27/workflow/specification-reset/electrical-integration/reference-aliases.json | 568 | 41fe29a6b6555dce76e3b8e944aca90750bc14d1abf0b2b2bb5694ad3e3f0320 |
| hardware/E27/workflow/specification-reset/electrical-integration/requirements-schematic.json | 32023 | 2533ce43dcf30924ed6c638778a49207a0b76d81b2e330642bb4682c946fb174 |
| hardware/E27/workflow/specification-reset/electrical-integration/results.json | 5959 | 9abe4bbc0c74cbdcbd254393943246aa7fea9c36488d6ec26eea03e29cbf4a22 |
| hardware/E27/workflow/specification-reset/electrical-integration/sources.json | 1193 | 198af012a2d27ec55918482fa5224562bdc7bea7ee044d9bac91294013fff85e |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/HANDOFF.md | 8834 | 42d0b47f35f941b14b9e0559112a4370c32d07dab33be12429d23fd123ec6d7b |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/README.md | 3726 | 356ccbbc8771d1e7bd3a7a929f14a89ea38b15d916bedc096e0ec7887dea88c8 |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/calculate.log | 5475 | dc57679fd1803f0de3f80a375e7a13acb059dccfc3985d50679c9c6dcde5dc36 |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/calculate.py | 8493 | 5808ce6e7cb3143205a6e44e2de4e9531aa49d36250a75eca9a5526369f5519c |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/hybrid3-results.json | 2698 | aac241a0633476e459801ae2420ab65f3753041a188e553f75d363fa449328cb |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/hybrid3.log | 2698 | aac241a0633476e459801ae2420ab65f3753041a188e553f75d363fa449328cb |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/hybrid3.py | 3277 | ddbc60f010de7306617d93fb9522861d8c8aa1d1479b0dc947a8ae804e13f376 |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/integration-check.json | 1661 | eeea25ff54cbfedaf24ae73521696c3b752bc37bd2ec6c9eeb7c3cc4c04e7fae |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/manifest.json | 1519 | a2c0865a59b6965124c5e8ea3a6f829ce9f2c933bae48c0faafaf884d0b8673e |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/results.json | 5475 | dc57679fd1803f0de3f80a375e7a13acb059dccfc3985d50679c9c6dcde5dc36 |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/rows.json | 86701 | bc9be18312f9fd92cc22225ec37c5bdb4a9606e1925c4456628ee72df595b6d9 |
| hardware/E27/workflow/specification-reset/electrical-integration/startup/sources.json | 1359 | 1d82ddbadb858f8ecba0fdf0ee7d9cf6547fd12c89f84a2e7e21d50c00f0579a |
| hardware/E27/workflow/specification-reset/electrical-integration/task-contract.md | 3081 | 10942bd6691d8d5fee649c8623184bfedb4b85fd3c12a309de73ef6878ca36fa |
| hardware/E27/workflow/specification-reset/finalization/support-results.json | 10038 | 7b031346b2cf2c45744198094e863111ea0efcbaa1a992b4bde0ce05224d1314 |
| hardware/E27/workflow/specification-reset/footprint-study/assignments.json | 6573 | ee9a9c077ea352a1508075cd0340a8eaacf7bd05280056171b6eac54135ba5b1 |
| hardware/E27/workflow/specification-reset/fp-lib-table | 227 | 43087dad28dd81785c75c80de00a43e57a804233247bb1ab231fefd394afccb5 |
| hardware/E27/workflow/specification-reset/hardware.json | 2656 | b7f1834a473c8c67f45e589269b5f1087fc87ca94d199dbe0dd4da5debc805b1 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.kicad_sym | 16795 | a83b3e6805eab01297799f033350774fd1ac9c280472f7bd2b564abf407caf60 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/AC05_P25p4_FORMED_PROJECT_CANDIDATE.kicad_mod | 1096 | 288597c84066e0f67bcce2d6fc18fc6f0b08c80fe39a6e39c213968217fb3670 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/CRCW_0603_NativeReflow.kicad_mod | 1034 | 6ce9d8219cf3d026257b29951362b6d29805bb7c79d5a61d9b424ab21fd19d65 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/CRCW_0805_NativeReflow.kicad_mod | 1026 | 116da79996b767451514af4d416b12ea00a224e41304efdc99a551743744699f |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/CRCW_1206_NativeReflow.kicad_mod | 1036 | 26284dae917c9bc653b71a53703cd738d31f5c590c9e148166150a64ba3a1f7e |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/CRCW_2512_NativeReflow.kicad_mod | 1020 | b65aaee3ae313ad4347cbb67e2c7ba5c13a353a45f9f8cdfca7fc68dbbccd72c |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/Diodes_US1M_SMA_Native.kicad_mod | 1209 | 93bfb8f50376a5e473bdcddb9a0258d09d41a6c6c678554f65fc91be7bf0d97f |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/InternalWirePair_P7p62_D1p6_PROJECT_CANDIDATE.kicad_mod | 1039 | c68a8f13b2d6387395b29ca4d2f2c1efcdfd9b9b7f88c8f1cb6dd09c30cba280 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/KEMET_2220_PROJECT_CANDIDATE.kicad_mod | 1066 | a4852937a199183f1b8c3e212894d7b8e33588cc0076ad9472f3004f2ab94629 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/MB10S_Diodes_MBS_1P_2AC_3N_4AC.kicad_mod | 1365 | bcb61b86077c0befe787d45ba0b056c501d47edd3b1cdd96596489004b025f4f |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/NTCS0603_NativeReflow.kicad_mod | 1020 | 09aadb843153732b79f2dfa754966acef83e3fc2b81fd022d618a7395aa29da8 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/Panasonic_ZA_D_Standard_Native.kicad_mod | 1264 | 3cad320ca90ea5bcc770010add35997d1ca4734cb1f365bb90770208badb93bf |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/Rubycon_BXW_D10_P5_PROJECT_CANDIDATE.kicad_mod | 1300 | 472c0a4206408f1c4d1ac6575d0019013cec599348f97b10591de1cb81600893 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/SCHURTER_UMTH_WEB_PROVISIONAL.kicad_mod | 1086 | edbae882a0b49ee5a8a0efa9310fd4078bc1beb2f1fe9901f4271d46f7273b24 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/STN1NK80Z_SOT223_Tab4.kicad_mod | 1232 | f1b8edf66033160f5165cb03e9bd5d579b107ceceda4ca7340bc40d4d0cf1306 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/ST_STTH_SMA_Native.kicad_mod | 1212 | 439f295996b42dc62b7d182151cd56a335307b36709fece4b013b9f3d6b7ee26 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/TDK_B66422W1010D001_EFD25_RAW_CANDIDATE.kicad_mod | 1910 | 68e8826b5ed994ee4e42c043c01a7265bf0e4cbc9cab5a256581b05b47ef7b1c |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/UCC28711DR_SOIC7_HV7.kicad_mod | 1612 | bbefd0cca0948ac2e7cbb2dd72de07704e9e18e39963371ef723b69b4a102d82 |
| hardware/E27/workflow/specification-reset/libraries/Velluneo_Driver.pretty/Vishay_SMBJ_PROJECT_CANDIDATE.kicad_mod | 1322 | cbd89ab8d291673d4963cbf734bee43ff964d8ea8598579e912d64451a34a944 |
| hardware/E27/workflow/specification-reset/requirements-and-plan.md | 34515 | a0c2867d511313741495cf9d2696590e756c0d6a335d7180df5409cc6532b34e |
| hardware/E27/workflow/specification-reset/requirements.json | 39877 | 8b5220dcf3d55e56961a94257bf5a0ae77233bfa948f378c4364f6753b7166f9 |
| hardware/E27/workflow/specification-reset/schematic-intent/intended-connectivity.json | 13751 | b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a |
| hardware/E27/workflow/specification-reset/schematic-intent/local-terminal-contract.md | 2027 | 6b82a32d748c79b55f9b0e83b7c651575417e410e839f9e03b9bdd76e00167ee |
| hardware/E27/workflow/specification-reset/schematic-intent/native-source-register-primary.json | 820 | 41b7de71c5abe4b5630ab500f2657f02640b035bb6a02aee68d071b0d55797af |
| hardware/E27/workflow/specification-reset/schematic-intent/native-source-register-secondary.json | 2522 | 7c3333ec2122c8f57f053e7ba81ac329d61acaaab696ef3dca3735f5a36844c9 |
| hardware/E27/workflow/specification-reset/schematic-intent/owner-scope-acceptance.md | 1835 | 724c17767acef7f4768c870529746470e837d427348d708051a41b3c17cc2500 |
| hardware/E27/workflow/specification-reset/schematic-intent/parts.json | 4661 | 808295707d760d62e198794e6f406f1879cdff322e48412e9bd4d2df784bc221 |
| hardware/E27/workflow/specification-reset/schematic-intent/pin-basis-primary.md | 6270 | f02c2faa3cf05bd833c44a56180a7f53140158d84717fa14907b37ea9d7d56a4 |
| hardware/E27/workflow/specification-reset/schematic-intent/pin-basis-secondary.md | 8679 | 6323b4bf6d7661210e3081af8eeb39779bf153d198120fdaf24f8b81467ebc32 |
| hardware/E27/workflow/specification-reset/sym-lib-table | 223 | ae491b3cef7acb7c1cd3a75083670a5e1c99444e4c01e230e3757724fa1ba398 |
