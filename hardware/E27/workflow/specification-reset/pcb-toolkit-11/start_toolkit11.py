from pathlib import Path
import shutil,json,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';S=P/'pcb-cleanup-10';D=P/'pcb-toolkit-11';D.mkdir(exist_ok=True);shutil.copytree(S/'design',D/'design',ignore=shutil.ignore_patterns('.work','__pycache__','*.kicad_prl'),dirs_exist_ok=True)
for name in('checks','render','toolkit','evidence','fabrication','assembly-reference'):(D/name).mkdir(exist_ok=True)
(D/'.gitignore').write_text('.work/\n__pycache__/\n*.kicad_prl\n')
(D/'owner-request.txt').write_text('''Actual owner request, current conversation,20November2026 Europe/Warsaw:
No to rozszerz toolkit o te reguły izolacji i zamknij pozostałe blokady, żeby płytka była gotowa do zamówienia prototypu. Zapisuj wszystko na GitHubie i pokaż podgląd tutaj. oraz daj mi render 3d w dobrej jakosci zeby ta płytka wygladałą tak jak na jlcpcb

Scope: implement/version/test toolkit extension and integrate selected board; generate source-bound highquality3D render; save toVelluneoGitHub. This is not a fabricated approval of unseen final snapshots, supplier confirmation, order/payment or powered tests.
''',encoding='utf-8')
(D/'task-contract.md').write_text('''# TOOLKIT11 bounded implementation and procurement preparation

Base53fa8e2e29cae11e857f3d961ca063b20f7d08cf, selectedC10driver45x60mm/fourlayers/33parts81pads/304tracks17filled0.7/0.3vias. Root solely owns sharedprojectCAD/config/render/export writes. Implementationadvisor owns only externalwork/toolkit-c11-source, with anyinternaldelegation explicitlyseparatedbyfile; originalexport andinstalledcache immutable. Newreviewcandidate required, no silentpatch or waiver. Fourindependent finalroles inspect samefreeze and are distinct from implementation.

Implement explicit exact-net scoped3/10mmclearance generation, four-enabled-layer protectedareas, preserve-only-stronger severity customization and safe reviewedlegacy-rule migration with independentlycomputed effectivepolicy equivalence. Preserve global.25/.3/.3/.2/.5mm minima, strictERC, courtyardERROR levels, electricalpintruth/graph, placement, measurementgeometry andreturntopology. No fabricated configstate or humanapproval. Pin exactnewcontent/archive identity, preview/install/update/apply through actualtooling, validate actual unit/nativepositive+negativecases and cleanextractedcandidate suites. Priorarchive/source remainavailableforrollback; no unsupportedclaimofnewLinuxqualification ifnotrun.

Update currentselectedproject contracts/evidence after realadoption; supplierprocess/material/films, genuinefinalhumanapproval and originalassembly/energization/parentlampqualification remainactualexternalgates. Do not mark unavailable evidence ascomplete. Userauthorizesextension/save/render, not unsolicitedsuppliermessages, order/payment or energizedtests. Highqualityrender showsactualbareboard likefabricatorpreview; removalofcomponent3Dreferences is limitedtorender-onlycopy, originalcomponentallocations remainintheeditableproject. No AI-generatedimagery substituted forCAD.

Acceptance: currentnativeERC/DRC/parity0; unchangedphysicalgraph/pads/copper except explicitlyreviewednonphysicalareaidentity; exhaustive27-net pair+unknown/same-net+4layer policyproof and discriminating3mm/10mm/innerbarrier negatives; actualunit/CAD/examplevalidation records withgaps; genuineconfigownership throughpreview/apply; source-boundhighresolutionPNG; refreshedfabrication/portablearchives, fourindependentfinalreviews, exactGitHub/ref/tree/ZIPverification. Fullorderreadiness requiresactualremaininggates, cannotbefaked bytoolpass.
''',encoding='utf-8')
binding=dict(base_commit='53fa8e2e29cae11e857f3d961ca063b20f7d08cf',previous_packet='pcb-cleanup-10',source_board_sha256=hashlib.sha256((S/'design/Velluneo_driver.kicad_pcb').read_bytes()).hexdigest(),old_toolkit_commit='86614c3b9b43713031e0ea481edbe26b71cd1b8f',old_archive_sha256='15a2789b06afb014f9dc166ce6da01a903c3b422b5c1b37b2a96581b218784b4',KiCad='10.0.6');(D/'source-baseline.json').write_text(json.dumps(binding,indent=2)+'\n');print(D)
