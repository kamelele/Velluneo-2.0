"""Read-only source-bound geometry diagnostic; not an electrical waiver.

Freshly anchor finite pad/escape regions to the current board, without changing
any CAD, manufacturer land or project numeric rule. Proposed local floor values
are diagnostic parameters inherited from the earlier engineering proposal only.
"""
from pathlib import Path
import sys,json,hashlib,math
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'))
import checker as c
k=c.k;q=c.q
P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
PCB=P/'SC09_compact.kicad_pcb';M=ROOT/'work/routing-improvement/spacing-matrix.CAT01.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
before=sha(PCB);assert before=='532ff6ac51767badaabc49fb627b8feca729daeb1c4368a3cdb2ddad1c0996f8'
contract=c.Contract(P,M);b=q.load_native(PCB);check=c.Checker(b,contract);check.collect()
specs=[('U1',['3','4'],['FB_INDUCTOR','BUS_FILTERED'],.60,1.0),('U1',['2','4'],['M','BUS_FILTERED'],1.80,.3),('BR1',['1','3'],['BUS_RECT','DC_RETURN'],1.40,.3),('BR1',['2','4'],['AC_FUSED','AC_N'],1.40,.3),('D1',['1','2'],['FB_INDUCTOR','DC_RETURN'],1.40,.3)]
exceptions=[];anchors=[]
for ref,pins,nets,floor,margin in specs:
 pads=[next(x for x in check.objects if x.kind=='pad'and x.layer=='B.Cu'and x.owner==(ref,p))for p in pins]
 boxes=[q.bbox(x.shape)for x in pads];m=k.FromMM(margin);bounds=[min(x[0]for x in boxes)-m,min(x[1]for x in boxes)-m,max(x[2]for x in boxes)+m,max(x[3]for x in boxes)+m]
 ex={'ref':ref,'pins':pins,'nets':nets,'layers':['B.Cu'],'escape_layers':['B.Cu'],'except_object_types':['pad','track'],'escape_margin_mm':margin,'region_bbox_mm':[k.ToMM(v)for v in bounds],'proposed_drawn_floor_mm':floor}
 exceptions.append(ex);anchors.append({'ref':ref,'pins':pins,'pad_ids':[x.id for x in pads],'pad_shape_bounds_mm':[[k.ToMM(v)for v in bb]for bb in boxes],'actual_conservative_CAD_gap_mm':q.actual_gap(pads[0].shape,pads[1].shape,4),'analysis_floor_mm':floor,'analysis_margin_to_nominal_gap_mm':round(q.actual_gap(pads[0].shape,pads[1].shape,4)-floor,6),'frozen_region_bbox_mm':ex['region_bbox_mm']})
proposal={'revision':'SB01 current finite package geometry diagnostic, not accepted deviation','actor':'/root/sb01_spacing_geometry','authorized_for_bounded_geometry_screen_by':'Parent-assigned read-only assessment task; analysis execution only, not a human waiver or safety acceptance','electrical_qualified':False,'human_approved':False,'CAD_or_rules_modified':False,'meaning_of_local_floors':'Inherited proposal values used only to test geometric containment. They are not derived normative electrical minima or a guaranteed manufactured/soldered clearance.','frozen_pad_geometry_source_board_sha256':before,'CAT_graph_sha256':sha(P/'intended-connectivity.CAT01.json'),'matrix_sha256':sha(M),'edge_clearance_target_mm':1.0,'exceptions':exceptions}
(H/'current-finite-region-proposal.json').write_text(json.dumps(proposal,indent=2)+'\n')
strict=c.run(PCB,P,M);scoped=c.run(PCB,P,M,H/'current-finite-region-proposal.json')
c.dump(H/'strict-fresh.json',strict);c.dump(H/'finite-geometry-screen.json',scoped)
assert not strict.get('stopped')and len(strict['findings'])==23 and not strict['passed']
assert scoped['passed'],scoped.get('findings',scoped.get('error'))
sc=c.Checker(q.load_native(PCB),c.Contract(P,M,H/'current-finite-region-proposal.json'));sc.collect();rows=[]
for n,f in enumerate(strict['findings'],1):
 a=next(x for x in sc.objects if x.id==f['a']and x.layer==f['layer']);z=next(x for x in sc.objects if x.id==f['b']and x.layer==f['layer']);matches=[]
 for i,e in enumerate(exceptions):
  if {a.net,z.net}!=set(e['nets']):continue
  region=sc.exception_region(e);side=0 if a.net==e['nets'][0]else 1
  if not(sc.eligible(a,i,side,region)and sc.eligible(z,i,1-side,region)):continue
  parts_a=[('inside',q.clipped(a.shape,region)),('outside',q.clipped(a.shape,region,False))];parts_z=[('inside',q.clipped(z.shape,region)),('outside',q.clipped(z.shape,region,False))];piece_checks=[]
  for la,pa in parts_a:
   for lz,pz in parts_z:
    if pa.IsEmpty()or pz.IsEmpty():continue
    required=e['proposed_drawn_floor_mm']if la==lz=='inside'else f['target_mm']
    piece_checks.append({'a_piece':la,'b_piece':lz,'required_geometric_mm':required,'too_close':q.close(pa,pz,required)})
  matches.append({'region_index':i,'ref':e['ref'],'pins':e['pins'],'region_bbox_mm':e['region_bbox_mm'],'a_local_pad_roots':[list(r)for r in sorted(sc.roots(a,i,region))]if a.kind=='track'else[list(a.owner)],'b_local_pad_roots':[list(r)for r in sorted(sc.roots(z,i,region))]if z.kind=='track'else[list(z.owner)],'clipped_piece_checks':piece_checks,'outside_or_cross_region_failure':any(x['too_close']for x in piece_checks if x['a_piece']!='inside'or x['b_piece']!='inside')})
 assert len(matches)==1,(f,matches)
 rows.append({'number':n,**f,'classification':'intrinsic_manufacturer_land_pair'if f['kinds']==['pad','pad']else'unique_root_local_escape_observation','finite_region_containment':matches[0],'pair_contains_via_or_zone':a.kind in ['via','zone']or z.kind in ['via','zone']})
# Literal independent primary recommended lands, not copied from the PCB geometry.
fp={f.GetReference():f for f in b.GetFootprints()};primary=[]
for ref,size,pairs,basis in [
 ('BR1',[1,2.15],[('1','3',2.5),('1','2',5.35)],'Diodes DS39045 MBS recommended land: X1.00,Y2.15,C2.50,Y1outer7.50'),
 ('D1',[2.5,1.7],[('1','2',4.0)],'Diodes DS16008 SMA recommended land:2.5x1.7,pitch4.0'),
 ('U1',[1.45,.6],[('1','2',1.27),('1','8',5.45),('4','5',5.45)],'PI LYTSwitch1 RevB D08A p11 solder references:1.45x.60,pitch1.27,oppositecentres5.45')]:
 pads={p.GetNumber():p for p in fp[ref].Pads()};bad=[]
 for pin,pad in pads.items():
  actual=sorted([k.ToMM(pad.GetSize().x),k.ToMM(pad.GetSize().y)])
  if any(abs(x-y)>.000002 for x,y in zip(actual,sorted(size))):bad.append({'pin':pin,'size_mm':actual})
 for left,right,target in pairs:
  a,z=pads[left].GetPosition(),pads[right].GetPosition();actual=math.hypot(k.ToMM(a.x-z.x),k.ToMM(a.y-z.y))
  if abs(actual-target)>.000002:bad.append({'pins':[left,right],'actual_pitch_mm':actual})
 primary.append({'ref':ref,'literal_primary_basis':basis,'passed':not bad,'findings':bad})
assert all(x['passed']for x in primary)
result={'actor':'/root/sb01_spacing_geometry','source_board_sha256':before,'source_unchanged':sha(PCB)==before,'strict_generic_matrix_passed':False,'strict_findings':23,'classification_counts':{'intrinsic_pad_pairs':5,'local_escape_observations':18},'all_23_uniquely_contained_in_five_finite_regions':all(len(r['finite_region_containment'])>0 for r in rows),'no_via_or_zone_in_assessment':not any(r['pair_contains_via_or_zone']for r in rows),'outside_or_cross_region_generic_targets_retained':not any(r['finite_region_containment']['outside_or_cross_region_failure']for r in rows),'full_55_pair_geometric_screen_with_proposed_finite_regions_passed':scoped['passed'],'edge_target_mm':1.0,'edge_minimum':strict['copper_edge_minimum'],'pad_anchors':anchors,'primary_land_checks':primary,'findings':rows,'limits':['The analysis-floor values are not electrical safety minima or accepted waivers.','CAD spacing is nominal planar saved-copper geometry. No quantified pad-edge etch/feature variation or assembled solder/lead clearance bound is available.','The 0.000002mm reporting remainder is digital polygon/search precision, not manufacturing margin.','Same-layer global registration does not change relative copper gap; local feature-edge variation and solder/lead/placement effects remain unbounded.','Solder mask is given no protective credit. No physical surface/air path, CTI, pollution, altitude or high-frequency insulation qualification is established.','All CAD, global numeric rules and the strict FAIL23 report remain unchanged.']}
(H/'current-geometry-assessment.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'source_unchanged':result['source_unchanged'],'strict_findings':23,'scoped_geometry_passed':scoped['passed'],'outside_region_targets_retained':result['outside_or_cross_region_generic_targets_retained'],'primary_lands_passed':True}))

