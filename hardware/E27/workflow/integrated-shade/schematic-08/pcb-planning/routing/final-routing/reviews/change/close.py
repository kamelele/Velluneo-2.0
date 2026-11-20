from pathlib import Path
import json,hashlib,sys
O=Path(__file__).resolve().parent;R=O.parent/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype';F=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing/final-routing'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
expected='93dbb5532b8c981c5ae01aff364d88c095d259902e4ad86c6a5cf0b24b299832';assert sha(F/'review-inputs.json')==expected
old=read(F/'revisions/01/review-inputs.json');new=read(F/'review-inputs.json');assert sha(F/'revisions/01/review-inputs.json')=='02e3217f2265c5bd8150c335af5123f7e9861c2cf4d463e016d5a124d6f54728'
for f in new['files']:assert sha(R/f['path'])==f['sha256'],f['path']
for f in new['external_views']:assert sha(Path(f['path']))==f['sha256'],f['path']
a={p['path']:p['sha256'] for p in old['files']};b={p['path']:p['sha256'] for p in new['files']};changed=[p for p in a if b.get(p)!=a[p]];added=sorted(set(b)-set(a));removed=sorted(set(a)-set(b));assert not removed
assert {Path(p).name for p in changed}=={'return-and-thermal-routing-review.json','sc08_integrate_complete_routing.py','review-basis.md','integrated-toolkit-check.json'},changed
assert len(added)==5 and all('/revisions/01/' in p or p.endswith('/documentation-correction-impact.json') for p in added),added
before=(F/'revisions/01/thermal-review.json').read_text();after=(S/'routing-verification/return-and-thermal-routing-review.json').read_text();assert after==before.replace('R3/R4','R6/R27')
before=(F/'revisions/01/authoring-source.py').read_text();after=(F/'tools/sc08_integrate_complete_routing.py').read_text();assert after==before.replace('R3/R4','R6/R27')
before=(F/'revisions/01/review-basis.md').read_text();after=(F/'review-basis.md').read_text()
assert '25mmclearairfaces/20mmnearestsurface' in before and '25mmclearair beyond the outer component/solder envelope on BOTHfaces' in after
after=after.replace('25mmclearair beyond the outer component/solder envelope on BOTHfaces','25mmclearairfaces/20mmnearestsurface');assert after==before
check=read(F/'integrated-toolkit-check.json');assert check['passed'] and not check['errors'];assert check['snapshot']==new['integrated_source_snapshot']=='cbe355b1c1a1cbfc71e25ef5ec321e3ced2043793a77ca2dda316c52a3966204'
T=R/'.pcb-toolkit/versions/05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822'
snapshot=(O/'current-snapshot.txt').read_text(encoding='utf-8-sig').strip();assert snapshot==check['snapshot']
for p,h in check['input_hashes'].items():
 if p.startswith('ruleset:'):assert sha(T/p.split(':',1)[1])==h,p
 elif p in ['project-design-config','toolkit:identity']:continue # Bound by independently invoked installed snapshot command.
 else:assert sha(S/p)==h,p
assert sha(S/'SC08_prototype.kicad_pcb')==new['board_sha256']=='bddb0838b0b27a542cdc509b4d621220da3febf53ecc31e799c87fca87a34dad'
report={'review_id':'SC08-COMPLETE-CHANGE-01-CLOSURE','reviewer':'/root/final_route_change','role':'Change Reviewer','prior_report_sha256':sha(O/'review.json'),'prior_manifest_sha256':'02e3217f2265c5bd8150c335af5123f7e9861c2cf4d463e016d5a124d6f54728','current_manifest_sha256':expected,'verified_files':len(new['files']),'verified_external_views':len(new['external_views']),'current_source_snapshot':check['snapshot'],'board_sha256':new['board_sha256'],'changed_existing_paths':changed,'added_archival_paths':added,'removed_paths':removed,'all_other_sources_and_views_byte_identical':True,'fresh_integrated_check_matches_all_actual_input_hashes':True,'finding_closures':[{'id':'SC08-ROUTE-CHANGE-DOC-01','state':'verified_closed','actual_verifier':'/root/final_route_change','evidence':'Thermal report and reproducible authoring source exactly replace R3/R4 by R6/R27; U4.4 SOURCE retained; actual circuit and prior independently checked clamp memberships unchanged. Fresh integrated check/source snapshot passed.'}],'recommendation':'ready_for_human_review','open_findings':[],'scope':'Targeted documentation closure and complete revised-manifest freshness; earlier independently executed actual native/copper/parity checks carry forward only because CAD/rules/graph/spatial/requirements bytes are unchanged. Current routing human approval remains absent.','limits':['No physical performance/compliance qualification','No release/order/energized-test authorization','Four role reports and actual human routing acceptance are separate coordinator gates']}
(O/'closure.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))


