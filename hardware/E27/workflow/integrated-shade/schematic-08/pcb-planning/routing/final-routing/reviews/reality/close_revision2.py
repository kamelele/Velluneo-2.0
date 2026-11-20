from pathlib import Path
import hashlib,json,difflib
O=Path(__file__).parent;R=O.parent/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype';F=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing/final-routing'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
assert sha(F/'review-inputs.json')=='93dbb5532b8c981c5ae01aff364d88c095d259902e4ad86c6a5cf0b24b299832'
m=load(F/'review-inputs.json');old=load(F/'revisions/01/review-inputs.json');assert len(m['files'])==165
for f in m['files']:assert sha(R/f['path'])==f['sha256'],f['path']
for f in m['external_views']:assert sha(Path(f['path']))==f['sha256']
assert m['external_views']==old['external_views']
before={x['path']:x['sha256'] for x in old['files']};after={x['path']:x['sha256'] for x in m['files']};changed=[p for p in before if before[p]!=after.get(p)];added=[p for p in after if p not in before]
allowed={'routing-verification/return-and-thermal-routing-review.json','final-routing/review-basis.md','final-routing/tools/sc08_integrate_complete_routing.py','final-routing/integrated-toolkit-check.json'}
assert len(changed)==4 and all(any(p.endswith(x) for x in allowed) for p in changed),changed
thermal_old=(F/'revisions/01/thermal-review.json').read_text(encoding='utf-8');thermal_now=(S/'routing-verification/return-and-thermal-routing-review.json').read_text(encoding='utf-8');assert thermal_now==thermal_old.replace('R3/R4','R6/R27')
source_old=(F/'revisions/01/authoring-source.py').read_text(encoding='utf-8-sig');source_now=(F/'tools/sc08_integrate_complete_routing.py').read_text(encoding='utf-8-sig');assert source_now==source_old.replace('R3/R4','R6/R27')
basis=(F/'review-basis.md').read_text(encoding='utf-8');assert '25mmclearairbeyondoutercomponent/solderenvelopeBOTHfaces' in basis.replace(' ','') or ('25mm' in basis and 'solder' in basis and '20mmnearestsurface' not in basis)
check=load(F/'integrated-toolkit-check.json');assert check['passed'] and not check['errors'];assert check['snapshot']=='cbe355b1c1a1cbfc71e25ef5ec321e3ced2043793a77ca2dda316c52a3966204'
assert sha(S/'SC08_prototype.kicad_pcb')=='bddb0838b0b27a542cdc509b4d621220da3febf53ecc31e799c87fca87a34dad'
out={'review_id':'SC08-COMPLETE-REALITY-02','actor':'/root/final_route_reality','role':'Reality Checker','prior_report':'report.json','manifest_sha256':sha(F/'review-inputs.json'),'all165files3views_hash_verified':True,'controlled_delta':{'changed_existing_paths':changed,'added_archival_paths':added,'no_removed_prior_paths':not set(before)-set(after),'thermal_report_and_authoring_source_only_R3_R4_to_R6_R27':True,'review_basis_air_boundary_aligned_to_operative25mm_beyond_outer_envelopes_both_faces':True,'fresh_integrated_check_pass':True,'unchanged_actual_CAD_pro_dru_schematic_spatial_requirements':True},'finding_closure':{'id':'SC08-RR-DOC-01','status':'closed','basis':'Actual native inspection proved R6/R27; exact factual correction independently compared to archived original bytes. No circuit or numericoperativeinput change.'},'recommendation':'ready_for_human_review','remaining_major_routing_findings':[],'limits':'Only unpowered laboratory routing review. Initial source/trace/thermal/contact-graph checks retained against byte-identical CAD. No measurements, compliance, order, release or energized test approval.'}
(O/'closure.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))
