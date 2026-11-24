from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[4];O=ROOT/'outputs/SC09_SB01_ocena_odstepow';R1=ROOT/'outputs/SC09_SB01_R1_weryfikacja';P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(O/'core-manifest.json')=='1aade033562e650783312af8f588efa42d96a60f6210eb5c00e54e75023ee195'
m=json.loads((O/'core-manifest.json').read_text());bad=[n for n,v in m['files'].items()if sha(O/n)!=v['sha256']];assert not bad
assert sha(R1/'core-manifest.json')==m['R1_core_manifest_sha256'];r1=json.loads((R1/'core-manifest.json').read_text());assert all(sha(R1/n)==v['sha256']for n,v in r1['files'].items())
proposal=json.loads((O/'fabrication-only-proposal.json').read_text());guards=json.loads((O/'source-guard.json').read_text());assert guards==proposal['source_guards'];assert all(sha(P/n)==v==sha(R1/'source'/n)for n,v in guards.items())
assert proposal['id']=='SB01-FAB-LOCAL-01' and proposal['owner_approval']is None and not proposal['order_submitted']and not proposal['strict_spacing_passed']and not proposal['full_toolkit_release_passed']and not proposal['electrical_powered_spacing_acceptance']
g=json.loads((O/'geometry/current-geometry-assessment.json').read_text());strict=json.loads((O/'geometry/strict-fresh.json').read_text());finite=json.loads((O/'geometry/current-finite-region-proposal.json').read_text());screen=json.loads((O/'geometry/finite-geometry-screen.json').read_text())
key=lambda r:(r['a'],r['b'],r['layer'],tuple(r['nets']),r['conservative_gap_mm'],r['target_mm'])
assert len(strict['findings'])==len(g['findings'])==23 and sorted(map(key,strict['findings']))==sorted(map(key,g['findings']))
assert not strict['passed']and screen['passed']and len(screen['all_55_pair_minima'])==55
assert g['classification_counts']=={'intrinsic_pad_pairs':5,'local_escape_observations':18}
expected_pairs={('U1',('3','4')),('U1',('2','4')),('BR1',('1','3')),('BR1',('2','4')),('D1',('1','2'))};assert {(r['ref'],tuple(r['pins']))for r in finite['exceptions']}==expected_pairs
for e in finite['exceptions']:
 assert e['layers']==e['escape_layers']==['B.Cu']and set(e['except_object_types'])=={'pad','track'}
assert finite['edge_clearance_target_mm']==g['edge_target_mm']==1.0
for r in g['findings']:
 assert r['layer']=='B.Cu'and not r['pair_contains_via_or_zone'];region=r['finite_region_containment'];assert isinstance(region,dict)and not region['outside_or_cross_region_failure'];assert 0<=region['region_index']<5
 for piece in region['clipped_piece_checks']:
  assert not piece['too_close']
  if piece['a_piece']!='inside'or piece['b_piece']!='inside':assert piece['required_geometric_mm']==r['target_mm']
assert all(r['passed']for r in g['primary_land_checks'])
ev=json.loads((O/'stress/evidence-hashes.json').read_text());assert all(sha(ROOT/r['path'])==r['sha256']for r in ev['evidence']);assert all(sha(ROOT/n)==s for n,s in g['primary_source_hashes'].items())
z=O/'SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip';assert sha(z)=='b722078ed3668e1df757de855754dd7aefc925b9fc8617b28dd7493ece55490e'==sha(R1/z.name)
with zipfile.ZipFile(z)as archive:assert len(archive.namelist())==8 and all('/'not in n for n in archive.namelist())
fab=json.loads((O/'fabrication-recheck.json').read_text());assert fab['passed']and fab['input_unchanged']and not fab.get('findings')
result={'actor':'/root/sb01_r1_final_completeness','core_manifest_sha256':sha(O/'core-manifest.json'),'assessment_files_verified':len(m['files']),'retained_R1_files_verified':len(r1['files']),'source_guards_verified':len(guards),'strict_findings_unique_and_complete':23,'intrinsic_pairs':5,'local_escape_observations':18,'finite_regions':5,'full_net_pair_rows':len(screen['all_55_pair_minima']),'primary_land_checks_passed':True,'primary_evidence_hashes_verified':True,'outside_cross_region_targets_retained':True,'via_zone_other_layer_concessions':False,'source_ZIP_unchanged':True,'proposal_owner_approval':None,'order_submitted':False,'full_release_passed':False,'strict_passed':False,'source_unchanged_after':all(sha(P/n)==v for n,v in guards.items()),'assessment_core_unchanged_after':all(sha(O/n)==v['sha256']for n,v in m['files'].items())}
(D/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
