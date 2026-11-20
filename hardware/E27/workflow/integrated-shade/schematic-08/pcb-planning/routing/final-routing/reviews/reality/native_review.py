from pathlib import Path
import json,hashlib,sys,math
import pcbnew as k
root=Path(__file__).resolve().parents[1];R=root/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype';F=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/routing/final-routing';O=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
m=load(F/'review-inputs.json');assert sha(F/'review-inputs.json')=='02e3217f2265c5bd8150c335af5123f7e9861c2cf4d463e016d5a124d6f54728'
for f in m['files']:assert sha(R/f['path'])==f['sha256'],f['path']
for f in m['external_views']:assert sha(Path(f['path']))==f['sha256']
sys.path.insert(0,str(root/'sc08-route-validator'));import checker
b=checker.load_native(S/'SC08_prototype.kicad_pcb');a=load(S/'routing-verification/routing-authoring.json');c=checker.Checker(b,checker.Contract(S),a);c.collect()
# Native object contact graph: compare every DC_RETURN face, physical vias/PTH only.
dc=[o for o in c.objects if o.native_net=='/DC_RETURN'];edges=[]
for i,x in enumerate(dc):
 for j,y in enumerate(dc[:i]):
  if x.layer==y.layer and checker.close(x.shape,y.shape,0):edges.append((i,j))
  elif x.uuid==y.uuid and x.layer!=y.layer and (x.kind=='via' or x.kind=='pad' and x.source.GetAttribute()==k.PAD_ATTRIB_PTH):edges.append((i,j))
def graph(cut):
 ids=[i for i,o in enumerate(dc) if not(cut and o.id=='C5.2')];p={i:i for i in ids}
 def get(i):
  while p[i]!=i:i=p[i]
  return i
 for i,j in edges:
  if i in p and j in p:p[get(i)]=get(j)
 return {o.id:get(i) for i,o in enumerate(dc) if i in p and o.kind=='pad'},len({get(i) for i in p})
normal,n=graph(False);cut,ncut=graph(True);assert n==1 and ncut==2
assert cut['J2.2']==cut['C1.2']==cut['BR1.3']==cut['D1.2'];assert cut['U3.2']==cut['U4.2']==cut['U5.2']==cut['U2.2'];assert cut['U3.2']!=cut['J2.2']
fp={f.GetReference():f for f in b.GetFootprints()};details={}
for ref in ['U1','U4','U5','R6','R27','C3','R2','R6','R7','C5']:
 f=fp[ref];details[ref]={'value':f.GetValue(),'fields':{q.GetName():q.GetText() for q in f.GetFields()},'pins':{p.GetNumber():{'net':p.GetNetname(),'at':checker.point(p.GetPosition())} for p in f.Pads()}}
source_control=[o.meta for o in c.objects if o.kind=='track' and o.native_net=='/SOURCE' and o.meta['width']==.3]
assert details['U4']['pins']['4']['net']=='/SOURCE';assert details['R6']['value'].startswith('100') and details['R27']['value'].startswith('100')
assert details['C3']['pins']['1']['net']=='/BP';assert details['C3']['pins']['2']['net']=='/SOURCE'
via_locations=[checker.point(t.GetPosition()) for t in b.GetTracks() if isinstance(t,k.PCB_VIA) and t.GetNetname()=='/DC_RETURN' and 68<=k.ToMM(t.GetPosition().x)<=88 and 62<=k.ToMM(t.GetPosition().y)<=82];assert len(via_locations)==10
res={'actor':'/root/final_route_reality','manifest_sha256':sha(F/'review-inputs.json'),'all160files3views_hash_verified':True,'board_sha256':sha(S/'SC08_prototype.kicad_pcb'),'native_parts':details,'source_control_03_tracks':source_control,'DCgraph_normal_components':n,'DCgraph_after_C5negative_removed':ncut,'main_quiet_distinct_without_C5':True,'U3thermal_vias':via_locations,'C3_BP_direct_mm':math.dist(details['C3']['pins']['1']['at'],details['U1']['pins']['1']['at']),'limits':'Graph uses whole saved zone polygons as nodes; current zones each single-contiguous fill verified native outline count below; no electrical/thermal measurement.'}
res['zone_outline_counts']=[{'uuid':o.id,'outlines':o.shape.OutlineCount(),'area_mm2':o.shape.Area()/1e12,'layer':o.layer,'net':o.native_net} for o in c.objects if o.kind=='zone'];assert all(z['outlines']==1 for z in res['zone_outline_counts'])
(O/'inspection.json').write_text(json.dumps(res,indent=2)+'\n',encoding='utf-8');print(json.dumps({'native_geometry_inspected':True,'DCstar':True,'Source_control_branch':True,'thermal_vias':10}))

