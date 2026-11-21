# FOOTPRINT-02 independent Reality review

Reviewer /root/spec_reality; 2026-11-17. Read project AGENTS and installed locked Reality Checker role. Shared packet read-only; only this report written. Implementer audits are source inputs, not independent acceptance.

Recommendation: **ready_for_human_review for bounded candidate-library transfer only**. No new defect blocking that transfer found. This is not schematic-stage, product-PCB, placement, assembly, electrical, thermal, insulation or safety acceptance.

## Exact frozen scope

Manifest SHA256 `61cdb3079b6432947e6ed0b76f986210eaef0cc46ffaeb935bb311094fe910df`: independently verified all69 member hashes, zero mismatches. Also independently verified all13 available native source/STEP file hashes against source-register.json. The unavailable SCHURTER original is not counted as a verified native file. Full checked packet hashes appear below.

Read actual14 new .kicad_mod definitions, current assignments/schematic, source geometry, generator/checker, source notes/gaps, and recorded verification reports. Independently parsed the actual footprint S-expressions and asserted all28 new pad numbers/centres/sizes/types/layers/drills against independently transcribed native dimensions or explicitly labelled project proposals. Independently parsed actual schematic assignments:27 assigned positions,63 corresponding physical terminals,17 unique modules; T1 Footprint empty and no T1 assignment. Confirmed previous three modules byte-identical to the FOOTPRINT-01 reviewed hashes. No writer/generator was run and no independent fresh KiCad execution is claimed.

## Source and engineering observations

- Visually inspected native rendered CRCW p11 REFLOW table and NTCS p2. Actual resistor lands match .75×1.00 / .95×1.45 /1.05×1.80 /1.45×3.50 at centres±.75/±.975/±1.275/±3.10. NTC uses its distinct .80×1.00 at±.80 pattern. No WAVE substitution.
- Visually inspected both ST SMA native lands (STTH1 p10 and STTH2 p8) and Diodes US1M p4. ST centres±2.015,size1.40×1.64,gap2.63; US1M centres±2,size2.50×1.70,gap1.50 match actual copper. Actual local1K/2A numbering is a project convention consistently bound to the source cathode end and graph. Package-family names are not used to substitute copper geometry.
- Visually inspected native Vishay SMBJ p5. Actual TVS1 pads1.72×2.20 at±1.935 give gap2.15≤2.159, width1.72≥1.52, height2.20≥2.18 and outerspan5.59REF. These are an explicitly engineered realization of native inequalities, not unique prescribed dimensions or a physical qualification. Unidirectional cathode is local1.
- Visually inspected exact Panasonic EEHZA1J100P size-D outline and separate standard D/D8 land drawing. Actual1+ left/2− right pattern uses3.20×1.60 at±2.50: innergap1.80. It is the standard pattern, not the vibration-proof pattern. Native minus marking and the local rotated convention are distinguished; local numeric pin1 is not asserted manufacturer numbering.
- Visually inspected exact KEMET p1 body/termination dimensions. Actual PROJECT_CANDIDATE1.80×5.80 at±2.55 has gap3.30 and outerspan6.90; no native land prescription is claimed. The basis explicitly records copper extending beneath the unmetallized centre and unqualified paste/mask/attachment behavior. Size/termination bounds alone do not demonstrate solderability.
- Visually inspected Rubycon family dimension drawing and AC05 p10 lead/body/forming table. Actual CBULK nominal5mm pitch with1mm drill/2mm copper and RIN25.4mm proposed formed pitch with1.10mm drill/2.20mm copper match their labelled proposals, not manufacturer pad recipes or proof of worst-case lead insertion. Straight-axial RIN is not called a factory-preformed EK order. Actual wire-pad7.62mm pitch/1.6mm holes/3.2mm copper is explicitly project-only; no wire gauge, insulation or user dock is qualified.
- Native TDK p3 independently shows opposed mirrored pin plans without an explicit component-side label. Not assigning T1 is appropriate. The hashed STEP's existence is not a numbered-view qualification; I did not accept/render its geometry or resolve the pin1 view.
- F1 official web-text transcription has no verified native original bytes/direct drawing inspection. The packet accurately marks the footprint WEB_PROVISIONAL, uses a nominal/untoleranced body and keeps source closure open. Its local transcription hash does not authenticate original PDF contents. I did not newly retrieve or visually verify the original fuse drawing.

## Findings / retained closure conditions

No new publication-blocking finding. Retained SCH-LIB-001 remains open/advanced, not closed. Its explicit remaining conditions include resolving T1 component-side pin1 view before assignment; obtaining and independently checking F1 native drawing/source identity before qualification; establishing KEMET land/process basis; and accepting THT/wire forming, finished-hole/tolerance and actual assembly requirements. These are future qualification constraints already declared in the packet, not evidence supporting assembly today.

Mask/paste defaults, rectangular pads, nominal body representations, courtyard and polarity-marking conventions require actual selected-process/placement review. Courtyard graphics and pad/drill inventory do not prove fit, clearance, creepage or safety. No board exists here. A formed lead, vent, hot-resistor mounting clearance or strain relief is not qualified by its footprint.

Reviewed recorded native17-module geometry/inventory pass, approved-graph73-pin comparison (28components/21nets/4NC, intent digest b6d094763fb4eaf2e45b79cafa76f0bc6f818af27c79d7736a2524f8d6c36c57), ERC0 under the four listed default ignored checks, and honestly failing schematic/full-work reports. These limited checks do not close SCH-ANN-001, U05–U09 or the actual supply. RC-BIAS-001, RC-COMP-002, RC-MODEL-001, RC-CTRL-MODEL-001, RC-CLAMP-001 and all prior electrical/protection/input/service/thermal/safety majors retain their prior status. No simulation, measurement, process certification or owner stage approval is inferred.

## Verified packet members

Paths relative to specification-reset.

| Path | SHA256 |
|---|---|
| Velluneo_specification_reset.kicad_sch | 94779838a88fc5ec5fed810badc92a549df33be956eea54eca25a93316eb2a3d |
| footprint-completion/BOM.csv | 22b36a79a97c4bc8b6d15f50e4db57a4c5cb85830d47aa6f3a50b7172aa5033d |
| footprint-completion/README.md | db205f6fcf6241c56fe3e1f378a41838a3f21a18db98a75f10f50911fc2eb515 |
| footprint-completion/Velluneo_driver_27_footprints.pdf | 36199c21a590cb8fc77285dbef0b06297fe5073f715cadeb5b0403fbf2dc220e |
| footprint-completion/check-work.json | e800942d5ebb90a28bc1483074527f400140b642315a3f37c61a68a7ee0eb2f8 |
| footprint-completion/command-results.json | 42bc5228dc4f35eb2752e40678f641e200aabea85a302d2bcc2242860e127368 |
| footprint-completion/connectivity.json | e42a730fd95959c8a58d63b155f2b43248cc3217f6c0bae11212cc56c60eec8c |
| footprint-completion/doctor.json | 3004b39891f39f9e04f109d2b76424e09491471d6536f06e95a3bdd536fe7c1e |
| footprint-completion/erc.json | b3583ab23ee5cfe0a96742aceda4c427de1531786fd81e767884b8fe9a7cdd7e |
| footprint-completion/fuse-source-gap.md | 134dd8c2bf95da0d09f4557070cbf5ccd9d8a0eae4a9b2ec4a386cc781202ef8 |
| footprint-completion/generate_remaining_footprints.py | 049aaa81e81e11c810d4dc3c0816181cde5b5b51355a1aa171fd8c232ee69281 |
| footprint-completion/geometry-contract.json | 84ceca8587d3e2e7a1df6468c3c7220e3f20a21ce5a63479e43f74e67e0d0fb5 |
| footprint-completion/native-library-check.json | 482f9c5611f2b81133e738624fe474de1715c63a4115b99e3c3dc3dddce5e8f9 |
| footprint-completion/native-png/CRCW_2512_NativeReflow.png | 1bc14b95b17f8d01fad3154e02b31fa5da6aa1d3ea5b6c7ee92b5af7cdf67793 |
| footprint-completion/native-png/InternalWirePair_P7p62_D1p6_PROJECT_CANDIDATE.png | 175b40d3bd91aaf9a2d53c8da20da6a6392da5698109f977c66bc2cdc5cc8792 |
| footprint-completion/native-png/Panasonic_ZA_D_Standard_Native.png | e44d295ba7c70c7fe0aab160f766be75a0bfa58916f8898697955ecfc4a13ca2 |
| footprint-completion/native-png/Rubycon_BXW_D10_P5_PROJECT_CANDIDATE.png | 817352205a5bcb3b48e389e717787fd4173987619f0e32d1247f6f889d9d38d8 |
| footprint-completion/native-svg/AC05_P25p4_FORMED_PROJECT_CANDIDATE.svg | e6baa3fa75d58b502600162a3e1b5285410400504bce626a8a2a0ca3b6fe0a1f |
| footprint-completion/native-svg/CRCW_0603_NativeReflow.svg | 5a8bc09ab2aa66eacc4a8e90e6613644a647fea97b2f891eaa91c2975c3a0391 |
| footprint-completion/native-svg/CRCW_0805_NativeReflow.svg | 7af31d69f9b306896a4794c7bea78f509fb0e9f059a316a58f3d5c111ecbce0a |
| footprint-completion/native-svg/CRCW_1206_NativeReflow.svg | 54832d3aef797480d6a971f7601728cacce6dac535540a4f7542aab694b0841c |
| footprint-completion/native-svg/CRCW_2512_NativeReflow.svg | cccba9d4b0159a5f809a75cbb362beed0cffc3cb1fd5e2c76a4098e26e57136a |
| footprint-completion/native-svg/Diodes_US1M_SMA_Native.svg | 3d6107fb8671ef7f156a7cb48e6910b7865b28e2f78e9674076b8357d634e814 |
| footprint-completion/native-svg/InternalWirePair_P7p62_D1p6_PROJECT_CANDIDATE.svg | af15de7ded4906218582eee7cb3ef109e61b5b1a167eebad9ee797d6767dc69a |
| footprint-completion/native-svg/KEMET_2220_PROJECT_CANDIDATE.svg | ee8b98aebfc1fe951d3e0be00eb31be8f6ec11ea97ef301bb01165ef7d739c35 |
| footprint-completion/native-svg/MB10S_Diodes_MBS_1P_2AC_3N_4AC.svg | 1bf0b42d98d5b4e49895f93bfe78526a246040da70fe0748120f85855545b3dd |
| footprint-completion/native-svg/NTCS0603_NativeReflow.svg | f33c2be396ede6c132cbfb45302d3020f488a3e7778b2022f202ea401a02311b |
| footprint-completion/native-svg/Panasonic_ZA_D_Standard_Native.svg | 18b5e007127dc5bef32c62c260f85d1515c87a14931a4b1d2f33e1b51e87b93c |
| footprint-completion/native-svg/Rubycon_BXW_D10_P5_PROJECT_CANDIDATE.svg | 9d0aa8c097bb8c24a4aa72720dde7ed4b2d10f9af4fe0ed0cc1d290934ad5463 |
| footprint-completion/native-svg/SCHURTER_UMTH_WEB_PROVISIONAL.svg | a50b6a3fdc67001e6ad5b9cf58958f14f59f0ab1770f2aab16df8da49d67958a |
| footprint-completion/native-svg/STN1NK80Z_SOT223_Tab4.svg | 95d2e5dae7669298c4addbe8fbfd1a9f4b81aad38a1909bd0d7763f6f2384b71 |
| footprint-completion/native-svg/ST_STTH_SMA_Native.svg | 4ddbfc3bbd90f67158a91dce5213821f377e54fb70055466e7fac59fd3eb215c |
| footprint-completion/native-svg/UCC28711DR_SOIC7_HV7.svg | e17bcaea4a748be33f00b661f2b2cb83791d97d9dfc72fa0a0db03635843faa2 |
| footprint-completion/native-svg/Vishay_SMBJ_PROJECT_CANDIDATE.svg | c4e47d21423f9f14d8e681baaead7eae7903b51b21a0c536a4bb820773c1f209 |
| footprint-completion/passive-and-bobbin-basis.md | be88cc19bf3d2a74eaa2e30b5f1310b3a77ecd0794abf7ff3393a8a04b0c2d20 |
| footprint-completion/passive-geometry.json | 096d6142e325f2121f6a828a6b29dc44c7c097a07123c1d3cb7ea6365ac8a769 |
| footprint-completion/passive-sources.json | 5a690cb228815beb205f428e2c72b6ab10eef00b172bedd2d76c5abde345c5b3 |
| footprint-completion/power-pad-candidates.json | 95e31ded20be3b5c3d26a5a7cbc88ab37527f1fa47b35e37581a1e022bc3513e |
| footprint-completion/power-part-basis.md | adb84263aa5e65557d39e5a22dbe713c521afb6cf5a81199be22653cf8bcda65 |
| footprint-completion/requirements-schematic.json | 2533ce43dcf30924ed6c638778a49207a0b76d81b2e330642bb4682c946fb174 |
| footprint-completion/source-register.json | be4b659e8ab3ff57ceb70e44433d25ef8122bca26a9396f40a527f7a41225a68 |
| footprint-completion/task-contract.md | af376f7da582f372c07a6112d6afcb0641fb9facb0ac89ebf008601051e1308d |
| footprint-completion/verify_native_library.py | 55b29c64b4cb54605be06ff52730890efaaebd5917f74e992e50cdfa3727778d |
| footprint-study/assignments.json | a6f0098c013de982d796fc6d41d861dfb75c2f2cdd57dc578da4e83289b51fbf |
| footprint-study/generate_critical_footprints.py | 1bba7bfe417a3cea962de423452e8fcfa4c51ab18a9c96e874d2e0a84bc80046 |
| footprint-study/geometry-contract.json | 64aaa5af681733ac94767242f42f7430ccfd602e6ea219de1e8b540ec7613e3a |
| fp-lib-table | 43087dad28dd81785c75c80de00a43e57a804233247bb1ab231fefd394afccb5 |
| hardware.json | 47dc6e426e951a229bc89b6f80e2d9e37228e0989d4be0e50d31349051c26273 |
| libraries/Velluneo_Driver.kicad_sym | a83b3e6805eab01297799f033350774fd1ac9c280472f7bd2b564abf407caf60 |
| libraries/Velluneo_Driver.pretty/AC05_P25p4_FORMED_PROJECT_CANDIDATE.kicad_mod | 288597c84066e0f67bcce2d6fc18fc6f0b08c80fe39a6e39c213968217fb3670 |
| libraries/Velluneo_Driver.pretty/CRCW_0603_NativeReflow.kicad_mod | 6ce9d8219cf3d026257b29951362b6d29805bb7c79d5a61d9b424ab21fd19d65 |
| libraries/Velluneo_Driver.pretty/CRCW_0805_NativeReflow.kicad_mod | 116da79996b767451514af4d416b12ea00a224e41304efdc99a551743744699f |
| libraries/Velluneo_Driver.pretty/CRCW_1206_NativeReflow.kicad_mod | 26284dae917c9bc653b71a53703cd738d31f5c590c9e148166150a64ba3a1f7e |
| libraries/Velluneo_Driver.pretty/CRCW_2512_NativeReflow.kicad_mod | b65aaee3ae313ad4347cbb67e2c7ba5c13a353a45f9f8cdfca7fc68dbbccd72c |
| libraries/Velluneo_Driver.pretty/Diodes_US1M_SMA_Native.kicad_mod | 93bfb8f50376a5e473bdcddb9a0258d09d41a6c6c678554f65fc91be7bf0d97f |
| libraries/Velluneo_Driver.pretty/InternalWirePair_P7p62_D1p6_PROJECT_CANDIDATE.kicad_mod | c68a8f13b2d6387395b29ca4d2f2c1efcdfd9b9b7f88c8f1cb6dd09c30cba280 |
| libraries/Velluneo_Driver.pretty/KEMET_2220_PROJECT_CANDIDATE.kicad_mod | a4852937a199183f1b8c3e212894d7b8e33588cc0076ad9472f3004f2ab94629 |
| libraries/Velluneo_Driver.pretty/MB10S_Diodes_MBS_1P_2AC_3N_4AC.kicad_mod | bcb61b86077c0befe787d45ba0b056c501d47edd3b1cdd96596489004b025f4f |
| libraries/Velluneo_Driver.pretty/NTCS0603_NativeReflow.kicad_mod | 09aadb843153732b79f2dfa754966acef83e3fc2b81fd022d618a7395aa29da8 |
| libraries/Velluneo_Driver.pretty/Panasonic_ZA_D_Standard_Native.kicad_mod | 3cad320ca90ea5bcc770010add35997d1ca4734cb1f365bb90770208badb93bf |
| libraries/Velluneo_Driver.pretty/Rubycon_BXW_D10_P5_PROJECT_CANDIDATE.kicad_mod | 472c0a4206408f1c4d1ac6575d0019013cec599348f97b10591de1cb81600893 |
| libraries/Velluneo_Driver.pretty/SCHURTER_UMTH_WEB_PROVISIONAL.kicad_mod | edbae882a0b49ee5a8a0efa9310fd4078bc1beb2f1fe9901f4271d46f7273b24 |
| libraries/Velluneo_Driver.pretty/STN1NK80Z_SOT223_Tab4.kicad_mod | f1b8edf66033160f5165cb03e9bd5d579b107ceceda4ca7340bc40d4d0cf1306 |
| libraries/Velluneo_Driver.pretty/ST_STTH_SMA_Native.kicad_mod | 439f295996b42dc62b7d182151cd56a335307b36709fece4b013b9f3d6b7ee26 |
| libraries/Velluneo_Driver.pretty/UCC28711DR_SOIC7_HV7.kicad_mod | bbefd0cca0948ac2e7cbb2dd72de07704e9e18e39963371ef723b69b4a102d82 |
| libraries/Velluneo_Driver.pretty/Vishay_SMBJ_PROJECT_CANDIDATE.kicad_mod | cbd89ab8d291673d4963cbf734bee43ff964d8ea8598579e912d64451a34a944 |
| schematic-capture/BOM.csv | 22b36a79a97c4bc8b6d15f50e4db57a4c5cb85830d47aa6f3a50b7172aa5033d |
| schematic-capture/generate_driver.py | 1ba0871b18f847d629879732b1199496232d56d08c10d555e5a9a5079679e61c |
| schematic-intent/intended-connectivity.json | b48f1f4942dde63f388b7ffbc0072651ec3fb2dc9d105a13340ced493938598a |
