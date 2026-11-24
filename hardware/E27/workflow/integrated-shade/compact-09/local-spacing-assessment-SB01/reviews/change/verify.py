from pathlib import Path
import hashlib,json,subprocess,sys,math,zipfile
import pcbnew as k
ROOT=Path.cwd();O=ROOT/'outputs/SC09_SB01_ocena_odstepow';R1=ROOT/'outputs/SC09_SB01_R1_weryfikacja';P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();mh='1aade033562e650783312af8f588efa42d96a60f6210eb5c00e54e75023ee195';assert sha(O/'core-manifest.json')==mh;m=json.loads((O/'core-manifest.json').read_text());assert len(m['files'])==21
before={n:sha(O/n)for n in m['files']};assert all(before[n]==v['sha256']for n,v in m['files'].items())
assert sha(R1/'core-manifest.json')==m['R1_core_manifest_sha256']=='97f362117453cb296a588d0d835dfad7a4bea9931d2c35bd32300ecc238c462f'
r1=json.loads((R1/'core-manifest.json').read_text());assert all(sha(R1/n)==v['sha256']for n,v in r1['files'].items())
guards=json.loads((O/'source-guard.json').read_text());proposal=json.loads((O/'fabrication-only-proposal.json').read_text());assert guards==proposal['source_guards'];assert all(sha(P/n)==h==sha(R1/'source'/n)for n,h in guards.items())
assert proposal['owner_approval']is None and proposal['status']=='proposed_for_owner_acceptance_NOT_approved' and not proposal['order_submitted']and not proposal['strict_spacing_passed']and not proposal['full_toolkit_release_passed']and not proposal['electrical_powered_spacing_acceptance']and not proposal['operating_stress_bound_established']and not proposal['normative_insulation_compliance_established']
proposal_copy=O/'geometry/current-finite-region-proposal.json';f=json.loads(proposal_copy.read_text());assert not f['electrical_qualified']and not f['human_approved']and not f['CAD_or_rules_modified'];assert f['edge_clearance_target_mm']==1
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(P/'SC09_compact.kicad_pcb'));fs={x.GetReference():x for x in b.GetFootprints()};pads={(r,p.GetNumber()):p for r,x in fs.items()for p in x.Pads()}
xy=lambda p:(k.ToMM(p.x),k.ToMM(p.y));land_checks=[]
for ref,size in [('BR1',[1,2.15]),('D1',[1.7,2.5]),('U1',[.6,1.45])]:
 for p in fs[ref].Pads():assert all(abs(x-y)<.000002 for x,y in zip(sorted(xy(p.GetSize())),size))
 land_checks.append({'ref':ref,'literal_sorted_land_mm':size,'passed':True})
def distance(a,z):return math.dist(xy(pads[a].GetPosition()),xy(pads[z].GetPosition()))
assert abs(distance(('BR1','1'),('BR1','3'))-2.5)<.000002;assert abs(distance(('BR1','2'),('BR1','4'))-2.5)<.000002
assert abs(distance(('U1','3'),('U1','4'))-1.27)<.000002;assert abs(distance(('U1','2'),('U1','4'))-2.54)<.000002;assert abs(distance(('D1','1'),('D1','2'))-4.0)<.000002
checker=ROOT/'work/compact09/catalog-only/checker/checker.py';matrix=ROOT/'work/routing-improvement/spacing-matrix.CAT01.json';commands=[]
for name,args,expected_exit in [('strict',[],1),('finite',['--exceptions',str(proposal_copy)],0)]:
 cmd=[sys.executable,str(checker),'--board',str(P/'SC09_compact.kicad_pcb'),'--project',str(P),'--matrix',str(matrix),'--report',str(H/('fresh-'+name+'.json')),*args];r=subprocess.run(cmd,capture_output=True,encoding='utf-8',errors='replace');assert r.returncode==expected_exit;commands.append({'name':name,'args':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
(H/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');strict=json.loads((H/'fresh-strict.json').read_text());finite=json.loads((H/'fresh-finite.json').read_text());assert strict['passed']is False and len(strict['findings'])==23 and strict['exceptions_applied']is False;assert finite['passed']is True and not finite['findings']and finite['exceptions_applied']is True
assert all(x['layer']=='B.Cu'for x in strict['findings']);assert sum(x['kinds']==['pad','pad']for x in strict['findings'])==5;assert sum(x['kinds']!=['pad','pad']for x in strict['findings'])==18
expected_pairs={('U1',('3','4')),('U1',('2','4')),('BR1',('1','3')),('BR1',('2','4')),('D1',('1','2'))};assert {(x['ref'],tuple(x['pins']))for x in f['exceptions']}==expected_pairs
assert all(x['layers']==['B.Cu']and x['escape_layers']==['B.Cu']and x['except_object_types']==['pad','track']for x in f['exceptions'])
geometry=json.loads((O/'geometry/current-geometry-assessment.json').read_text());assert geometry['all_23_uniquely_contained_in_five_finite_regions']and geometry['no_via_or_zone_in_assessment']and geometry['outside_or_cross_region_generic_targets_retained']
zipname='SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip';assert sha(O/zipname)==sha(R1/zipname)==guards['release-refinement-R1/'+zipname]
with zipfile.ZipFile(O/zipname)as z:assert len(z.namelist())==8 and all('/'not in n for n in z.namelist())
after={n:sha(O/n)for n in m['files']};assert before==after and sha(O/'core-manifest.json')==mh and all(sha(P/n)==h for n,h in guards.items())
report={'actor':'/root/sb01_r1_final_change','assessment_core_sha256':mh,'R1_core_sha256':m['R1_core_manifest_sha256'],'assessment_files_checked_before_after':len(before),'R1_files_checked':len(r1['files']),'source_guards_checked':len(guards),'source_and_both_frozen_cores_unchanged':True,'literal_land_checks':land_checks,'fresh_strict_findings':23,'intrinsic_pairs':5,'finite_escapes':18,'fresh_scoped_diagnostic_passed':True,'scoped_result_is_not_strict_pass':True,'all_strict_findings_on_B_Cu':True,'exact_proposed_pairs':sorted((a,list(z))for a,z in expected_pairs),'unchanged_supplier_zip':sha(O/zipname),'proposal_unsigned':True,'order_submitted':False,'full_release_passed':False,'powered_qualification_passed':False}
(H/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
