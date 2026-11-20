from pathlib import Path
import hashlib,json,math,collections
import pcbnew as k
root=Path(__file__).resolve().parents[1];R=root/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype';F=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing/final-routing';O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
m=load(F/'review-inputs.json');assert sha(F/'review-inputs.json')=='02e3217f2265c5bd8150c335af5123f7e9861c2cf4d463e016d5a124d6f54728'
for x in m['files']:assert sha(R/x['path'])==x['sha256'],x['path']
for x in m['external_views']:assert sha(Path(x['path']))==x['sha256']
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(S/'SC08_prototype.kicad_pcb'));old=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(F.parent/'adoption/before-adoption/SC08_prototype.kicad_pcb'))
def parts(board):
 return {f.GetReference():{'value':f.GetValue(),'MPN':f.GetFieldText('MPN'),'footprint':str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),'pos':[f.GetPosition().x,f.GetPosition().y],'rotation':f.GetOrientationDegrees(),'pad_count':len(list(f.Pads()))} for f in board.GetFootprints()}
assert parts(b)==parts(old);assert len(parts(b))==47
tracks=[t for t in b.GetTracks() if not isinstance(t,k.PCB_VIA)];vias=[t for t in b.GetTracks() if isinstance(t,k.PCB_VIA)];zones=[z for z in b.Zones() if not z.GetIsRuleArea()];areas=[z for z in b.Zones() if z.GetIsRuleArea()]
assert len(tracks)==957 and len(vias)==54 and len(zones)==6 and len(areas)==8 and b.GetCopperLayerCount()==2
widths=collections.Counter(k.ToMM(t.GetWidth()) for t in tracks);netstats={}
for t in tracks:
 n=t.GetNetname();d=netstats.setdefault(n,{'segments':0,'total_length_mm':0,'widths_mm':set()});d['segments']+=1;d['total_length_mm']+=k.ToMM(t.GetLength());d['widths_mm'].add(k.ToMM(t.GetWidth()))
for v in netstats.values():v['widths_mm']=sorted(v['widths_mm']);v['total_length_mm']=round(v['total_length_mm'],4)
tiny=sum(k.ToMM(t.GetLength())<.3 for t in tracks)
assert all(z.GetNetname()!='/SOURCE' or z.IsOnLayer(k.F_Cu) and not z.IsOnLayer(k.B_Cu) for z in zones)
assert all(k.ToMM(v.GetWidth(k.F_Cu))==.8 and k.ToMM(v.GetDrillValue())==.3 for v in vias)
cons=load(S/'.electronics-rules/routing-input.json');assert cons==load(S/'.electronics-rules/placement-input.json')
check=load(F/'integrated-toolkit-check.json');assert check['passed'];matrix=load(S/'routing-verification/full-matrix-final.json');assert matrix['passed'] and matrix['stats']['different_net_face_pairs']==382861
req=load(S/'requirements-lab-fabrication.proposed.json');assert len(req['requirements'])==12 and len(req['evidence'])==10
product=load(S/'requirements.json');assert len(product['requirements'])==17
out={'manifest_sha256':sha(F/'review-inputs.json'),'all160_files_and3_views_match':True,'native_board_sha256':sha(S/'SC08_prototype.kicad_pcb'),'all47_parts_values_MPN_footprint_positions_rotations_unchanged':True,'parts':parts(b),'counts':{'tracks':len(tracks),'vias':len(vias),'zones':len(zones),'rule_areas':len(areas),'layers':2,'segments_shorter_than_0p3mm':tiny},'width_histogram':dict(widths),'net_statistics':netstats,'SOURCE_backplane_absent':True,'all54_vias_0p8_diameter_0p3_drill':True,'consumer_inputs_identical':True,'integrated_work_check_pass':check['passed'],'source_snapshot':check['snapshot'],'matrix_pairs':382861,'LAB_requirements':12,'LAB_evidence_entries':10,'original_product_requirements':17}
(O/'inspection.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k not in ['parts','net_statistics']}))
