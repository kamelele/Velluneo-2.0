from pathlib import Path
import hashlib,json,sys,math
ROOT=Path.cwd();O=ROOT/'outputs/SC09_SB01_ocena_odstepow';P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';R=ROOT/'work/sc09-sb01-spacing-assessment/final-reviews/reality';R.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='1aade033562e650783312af8f588efa42d96a60f6210eb5c00e54e75023ee195'
assert sha(O/'core-manifest.json')==expected
m=json.loads((O/'core-manifest.json').read_text());assert all(sha(O/n)==v['sha256']for n,v in m['files'].items())
guards=json.loads((O/'source-guard.json').read_text());assert all(sha(P/n)==h for n,h in guards.items())
R1=ROOT/'outputs/SC09_SB01_R1_weryfikacja';old=json.loads((R1/'core-manifest.json').read_text());assert sha(R1/'core-manifest.json')==m['R1_core_manifest_sha256'];assert all(sha(R1/n)==v['sha256']for n,v in old['files'].items());assert all(sha(R1/'source'/n)==h for n,h in guards.items())
evidence=json.loads((O/'stress/evidence-hashes.json').read_text());assert all(sha(ROOT/r['path'])==r['sha256']for r in evidence['evidence'])
proposal=json.loads((O/'fabrication-only-proposal.json').read_text());assert proposal['owner_approval']is None and proposal['order_submitted']is False and proposal['electrical_powered_spacing_acceptance']is False and proposal['operating_stress_bound_established']is False
assert proposal['source_guards']==guards and sha(O/'SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip')==guards['release-refinement-R1/SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip']
sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
matrix=ROOT/'work/routing-improvement/spacing-matrix.CAT01.json';pcb=P/'SC09_compact.kicad_pcb';finite=O/'geometry/current-finite-region-proposal.json'
strict=c.run(pcb,P,matrix);scoped=c.run(pcb,P,matrix,finite);c.dump(R/'strict-rerun.json',strict);c.dump(R/'finite-rerun.json',scoped)
assert not strict.get('stopped') and not strict['passed']and len(strict['findings'])==23
assert scoped['passed'] and scoped['input_unchanged']
spec=json.loads(finite.read_text());assert spec['edge_clearance_target_mm']==1.0 and len(spec['exceptions'])==5 and not spec['electrical_qualified']and not spec['human_approved']and not spec['CAD_or_rules_modified']
for e in spec['exceptions']:assert e['layers']==['B.Cu']and e['escape_layers']==['B.Cu']and sorted(e['except_object_types'])==['pad','track']
b=c.q.load_native(pcb);ch=c.Checker(b,c.Contract(P,matrix,finite));ch.collect();land_checks=[]
for ref,size,pairs in [('BR1',[1,2.15],[('1','3',2.5),('1','2',5.35)]),('U1',[1.45,.6],[('1','2',1.27),('1','8',5.45)]),('D1',[2.5,1.7],[('1','2',4)])]:
 f=next(f for f in b.GetFootprints()if f.GetReference()==ref);pads={p.GetNumber():p for p in f.Pads()}
 for pin,p in pads.items():assert all(abs(a-z)<.000002 for a,z in zip(sorted(size),sorted([c.k.ToMM(p.GetSize().x),c.k.ToMM(p.GetSize().y)])))
 for a,z,pitch in pairs:
  p1,p2=pads[a].GetPosition(),pads[z].GetPosition();assert abs(math.hypot(c.k.ToMM(p1.x-p2.x),c.k.ToMM(p1.y-p2.y))-pitch)<.000002
 land_checks.append({'ref':ref,'literal_land_size_mm':size,'centres_checked':pairs,'passed':True})
contain=[]
for finding in strict['findings']:
 a=next(x for x in ch.objects if x.id==finding['a']and x.layer==finding['layer']);z=next(x for x in ch.objects if x.id==finding['b']and x.layer==finding['layer']);eligible=[]
 assert a.kind in ['pad','track']and z.kind in ['pad','track']and a.layer=='B.Cu'
 for i,e in enumerate(spec['exceptions']):
  if set(e['nets'])!={a.net,z.net}:continue
  region=ch.exception_region(e);side=0 if a.net==e['nets'][0]else 1
  if not(ch.eligible(a,i,side,region)and ch.eligible(z,i,1-side,region)):continue
  residual=[]
  for la,pa in [('inside',c.q.clipped(a.shape,region)),('outside',c.q.clipped(a.shape,region,False))]:
   for lz,pz in [('inside',c.q.clipped(z.shape,region)),('outside',c.q.clipped(z.shape,region,False))]:
    if pa.IsEmpty()or pz.IsEmpty():continue
    required=e['proposed_drawn_floor_mm']if la==lz=='inside'else finding['target_mm']
    if c.q.close(pa,pz,required):residual.append([la,lz])
  assert not residual;eligible.append(i)
 assert len(eligible)==1
 contain.append({'a':a.id,'b':z.id,'region':eligible[0],'outside_cross_residual':False})
filter_screen=json.loads((O/'conditional-input-filter-screen.json').read_text());group=next(x for x in filter_screen['groups']if x['R_nominal_ohm']==47);numbers={'ideal253VACcrest_V':253*math.sqrt(2),'conditional_C1_peak_V':group['maxima']['C1_peak_V'],'conditional_C4_peak_V':group['maxima']['C4_peak_V']}
assert 706.2<numbers['conditional_C1_peak_V']<706.4 and 588.6<numbers['conditional_C4_peak_V']<588.8
assert sha(O/'core-manifest.json')==expected and all(sha(O/n)==v['sha256']for n,v in m['files'].items())and all(sha(P/n)==h for n,h in guards.items())
result={'actor':'/root/sb01_r1_final_reality','core_manifest_sha256':expected,'core_files_verified':len(m['files']),'source_guards_verified':len(guards),'retained_R1_core_files_verified':len(old['files']),'primary_evidence_hashes_verified':len(evidence['evidence']),'own_strict_rerun_findings':23,'own_finite_diagnostic_passed':True,'primary_land_literal_checks':land_checks,'all23_uniquely_contained':contain,'numeric_stress_recheck':numbers,'source_core_and_ZIP_unchanged':True,'limits':'Finite pass is geometric diagnostic only; no electrical minimum, physical measurement, powered acceptance, human approval or supplier order inferred.'};(R/'verification-summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'core_files':len(m['files']),'source_guards':len(guards),'retained_R1':len(old['files']),'strict_failures':23,'finite_diagnostic':True,'source_unchanged':True}))

