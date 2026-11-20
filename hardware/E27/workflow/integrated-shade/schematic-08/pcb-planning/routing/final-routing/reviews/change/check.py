from pathlib import Path
import json,hashlib,sys,xml.etree.ElementTree as E,math
import pcbnew as k
O=Path(__file__).resolve().parent;root=O.parent;R=root/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype';W=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing';F=W/'final-routing'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));save=lambda p,x:p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
expected='02e3217f2265c5bd8150c335af5123f7e9861c2cf4d463e016d5a124d6f54728'
assert sha(F/'review-inputs.json')==expected
m=read(F/'review-inputs.json');inputs=[(R/f['path'],f['sha256']) for f in m['files']]+[(Path(f['path']),f['sha256']) for f in m['external_views']]
for p,h in inputs:assert sha(p)==h,p
def board(p):return k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(p))
b=board(S/'SC08_prototype.kicad_pcb');orig=board(W/'adoption/before-adoption/SC08_prototype.kicad_pcb');seed=board(W/'one-pair-correction-proposal/SC08_prototype.kicad_pcb')
def point(p):return [p.x,p.y]
def footprints(b):
 result={}
 for f in b.GetFootprints():
  result[f.GetReference()]={'uuid':f.m_Uuid.AsString(),'fields':{p.GetName():p.GetText() for p in f.GetFields()},'lib':str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),'pos':point(f.GetPosition()),'orientation':f.GetOrientationDegrees(),'layer':f.GetLayer(),'pads':sorted([{'uuid':p.m_Uuid.AsString(),'n':p.GetNumber(),'net':p.GetNetname(),'pos':point(p.GetPosition()),'orient':p.GetOrientationDegrees(),'size':point(p.GetSize()),'drill':point(p.GetDrillSize()),'shape':int(p.GetShape()),'attr':int(p.GetAttribute()),'layer':list(p.GetLayerSet().Seq())} for p in f.Pads()],key=lambda p:p['uuid'])}
 return result
assert footprints(b)==footprints(orig)
def routes(b):
 out={}
 for t in b.GetTracks():
  uid=t.m_Uuid.AsString()
  if isinstance(t,k.PCB_VIA):out[uid]={'type':'via','net':t.GetNetname(),'p':point(t.GetPosition()),'dia':t.GetWidth(k.F_Cu),'drill':t.GetDrillValue(),'layers':list(t.GetLayerSet().Seq())}
  else:out[uid]={'type':'track','net':t.GetNetname(),'start':point(t.GetStart()),'end':point(t.GetEnd()),'width':t.GetWidth(),'layer':t.GetLayer()}
 return out
now=routes(b);then=routes(seed);assert all(now.get(uid)==v for uid,v in then.items())
assert len(then)==40
for n in ['SC08_prototype.kicad_pro','SC08_prototype.kicad_dru']:assert (S/n).read_bytes()==(W/'adoption/before-adoption'/n).read_bytes()
pro=read(S/'SC08_prototype.kicad_pro');drc=read(O/'native-drc.json');assert not any(drc[q] for q in ['violations','unconnected_items','schematic_parity'])
assert [i['key'] for i in drc['ignored_checks']]==['track_not_centered_on_via','tuning_profile_track_geometries']
xml=E.parse(O/'fresh-netlist.xml').getroot();fpts=footprints(b);xp={}
for c in xml.findall('components/comp'):
 ref=c.get('ref');fp=fpts[ref];fields={a.get('name'):a.text or '' for a in c.findall('fields/field')}
 assert fp['fields']['Value']==c.findtext('value');assert fp['fields']['MPN']==fields['MPN'];assert fp['fields']['Datasheet']==c.findtext('datasheet');assert fp['lib']==c.findtext('footprint')
for n in xml.findall('nets/net'):
 for p in n.findall('node'):xp[(p.get('ref'),p.get('pin'))]=n.get('name')
bp={(ref,p['n']):p['net'] for ref,f in fpts.items() for p in f['pads'] if p['n']}
assert bp==xp,(set(bp)-set(xp),set(xp)-set(bp));assert len(bp)==112;assert len(set(bp.values()))==31 and sum(n.startswith('unconnected-') for n in set(bp.values()))==1
intent_source=read(S/'intended-connectivity.json')
groups=lambda xs:{frozenset((p['ref'],p['pin']) for p in n['pins']) for n in xs}
assert groups(intent_source['nets'])=={frozenset((p.get('ref'),p.get('pin')) for p in n.findall('node')) for n in xml.findall('nets/net') if not n.get('name').startswith('unconnected-')}
assert {(p['ref'],p['pin']) for p in intent_source['no_connects']}=={p for p,n in xp.items() if n.startswith('unconnected-')}
assert bp[('U4','4')]=='/SOURCE';assert bp[('U4','3')]==bp[('R6','2')];assert bp[('U5','3')]==bp[('R27','2')];assert 'R3' not in fpts and 'R4' not in fpts
sp=read(S/'spatial-constraints-routing-correction.proposed.json');intent=hashlib.sha256(json.dumps({q:v for q,v in sp.items() if q!='approval'},sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest();assert intent==m.get('spatial_intent_digest', 'e229ed9dd0a8a593837efcfeaac4fe11b63160d5ceab293653b18370dc764dc8')
assert sp['approval']['intent_digest']==intent
consumer=read(S/'.electronics-rules/routing-input.json');assert consumer==read(S/'.electronics-rules/placement-input.json');assert consumer['constraints']['intent_digest']==intent
a=read(S/'pcb-basis/routing-and-isolation-proposal.json');c=read(S/'pcb-basis/routing-and-isolation-route2.proposed.json');diff=[]
for i,(x,y) in enumerate(zip(a['package_exceptions_proposed'],c['package_exceptions_proposed'])):
 for key in set(x)|set(y):
  if x.get(key)!=y.get(key):diff.append({'i':i,'ref':x['ref'],'pins':x['pins'],'key':key,'before':x.get(key),'after':y.get(key)})
assert len(diff)==2 and all(d['ref']=='U1' and d['pins']==['2','4'] for d in diff)
assert {d['key'] for d in diff}=={'escape_margin_mm','scope'}
for d in diff:
 if d['key']=='escape_margin_mm':assert d['before']==1 and d['after']==1.5
assert a['targets']==c['targets'];assert a['environment']==c['environment']
sys.path.insert(0,str(root/'sc08-route-validator'));import checker
assert sha(root/'sc08-route-validator/checker.py')=='8b77118d3bfa321011991b686681548010032b6fcd95b57c87f0765026aa5d7a'
r=checker.check_saved(S/'SC08_prototype.kicad_pcb',checker.Contract(S),S/'routing-verification/routing-authoring.json');assert r['passed'];save(O/'independent-matrix-repeat.json',r)
assert checker.raw_track_nets(S/'SC08_prototype.kicad_pcb')=={t.m_Uuid.AsString():t.GetNetname() for t in b.GetTracks()}
zones=[z for z in b.Zones() if not z.GetIsRuleArea()];assert len(zones)==6
assert all(z.IsFilled() and not z.NeedRefill() for z in zones)
areas=[z for z in b.Zones() if z.GetIsRuleArea()];assert len(areas)==8
sourceback=[z for z in zones if z.GetNetname()=='/SOURCE' and z.IsOnLayer(k.B_Cu)];assert not sourceback
for p,h in inputs:assert sha(p)==h,p
result={'reviewer':'/root/final_route_change','manifest_sha256':expected,'verified_manifest_files':len(m['files']),'verified_external_views':len(m['external_views']),'board_sha256':sha(S/'SC08_prototype.kicad_pcb'),'all47_footprints_and112_pads_geometrically_and_semantically_equal_to_accepted_placement':True,'all27_original_tracks_and13_original_vias_preserved':True,'native_project_and_rules_byte_identical_to_accepted_placement':True,'fresh_XML_112_pin_net_MPN_value_footprint_datasheet_parity':True,'approved_intent30_unordered_pin_sets_plus1NC_independent_comparison':True,'fresh_native_DRC':{'violations':0,'unconnected':0,'parity':0,'ignored_checks':drc['ignored_checks']},'active_spatial_intent_digest':intent,'consumer_digest':consumer['constraints_digest'],'only_route2_exception_differences':diff,'exact_full_matrix_repeat_passed':True,'matrix_face_pairs':r['stats']['different_net_face_pairs'],'raw_native_track_net_identity_parity':True,'native_tracks':sum(t['type']=='track' for t in now.values()),'native_vias':sum(t['type']=='via' for t in now.values()),'filled_copper_zones':len(zones),'managed_rule_areas':len(areas),'no_SOURCE_B_Cu_plane':True,'source_clamp_actual_refs':{'U4.4':'SOURCE','U4.3':'R6.2','U5.3':'R27.2'},'frozen_hashes_unchanged_after_checks':True}
save(O/'independent-checks.json',result);print(json.dumps(result,indent=2))


