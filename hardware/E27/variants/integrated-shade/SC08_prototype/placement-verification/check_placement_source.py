from pathlib import Path
import pcbnew as k,json,itertools,math,hashlib
R=Path(__file__).resolve().parents[6] if Path(__file__).parent.name=='placement-verification' else Path(__file__).parent/'Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC08_prototype';W=R/'hardware/E27/workflow/integrated-shade/schematic-08/pcb-planning/placement';b=k.LoadBoard(str(S/'SC08_prototype.kicad_pcb'))
binding=json.loads((S/'pcb-basis/intent-native-net-binding.json').read_text());native={r['native_net']:r['intent_net'] for r in binding['records']};native.update({r['native_net']:'EXPLICIT_NC' for r in binding['no_connects']})
rules=json.loads((S/'pcb-basis/routing-and-isolation-proposal.json').read_text());sp=json.loads((S/'spatial-constraints.proposed.json').read_text());layout=json.loads((S/'pcb-basis/layout-reservations.json').read_text());dom=json.loads((S/'pcb-basis/domain-matrix.json').read_text());domains={n:d['id'] for d in dom['domains'] for n in d['nets']};domains['EXPLICIT_NC']='CONTROL_RETURN';local={'SOURCE','SENSE_FB','BP','BP_RELAY','BP2_RELAY'}
def box(z):return [k.ToMM(z.GetX()),k.ToMM(z.GetY()),k.ToMM(z.GetRight()),k.ToMM(z.GetBottom())]
def dist(a,c):return math.hypot(max(a[0]-c[2],c[0]-a[2],0),max(a[1]-c[3],c[1]-a[3],0))
def union(a):return [min(x[0] for x in a),min(x[1] for x in a),max(x[2] for x in a),max(x[3] for x in a)]
def gap(a,c):
 if a==c:return 0
 if domains[a]==domains[c]=='CONTROL_RETURN' or a in local and c in local:return .3
 if domains[a] in ['AC_FRONT','BUS_DRAIN','SWITCH_FLOAT'] or domains[c] in ['AC_FRONT','BUS_DRAIN','SWITCH_FLOAT']:return 4
 return 2
pads=[];parts=[];findings=[];region={p:r['rect'] for r in layout['regions'] for p in r['parts']}
for f in b.GetFootprints():
 ref=f.GetReference();court=union([box(g.GetBoundingBox()) for g in f.GraphicalItems() if g.GetLayer()==k.F_CrtYd]);rr=region[ref]
 if any([court[0]<rr[0]-.0001,court[1]<rr[1]-.0001,court[2]>rr[2]+.0001,court[3]>rr[3]+.0001]):findings.append({'type':'region_fit','ref':ref,'court':court,'region':rr})
 parts.append({'ref':ref,'court':court,'x':k.ToMM(f.GetPosition().x),'y':k.ToMM(f.GetPosition().y),'angle':f.GetOrientationDegrees()})
 for p in f.Pads():
  layers=[n for n,l in [('F.Cu',k.F_Cu),('B.Cu',k.B_Cu)] if p.IsOnLayer(l)]
  if not layers:continue
  assert p.GetNumber(),('Unnumberedcopper',ref)
  pn=p.GetNumber();net=native[p.GetNetname()];pb=box(p.GetBoundingBox());pads.append({'ref':ref,'pin':pn,'net':net,'pad':p,'box':pb,'layers':layers,'shape':p.GetEffectiveShape(k.F_Cu)})
  for area in sp['areas']:
   if 'pad' in area['disallow'] and set(layers)&set(area['layers']) and dist(pb,area['rectangle_mm'])<=0:findings.append({'type':'protected_area','pin':ref+'.'+pn,'area':area['id']})
  if ref!='U3' and 'B.Cu' in layers and net!='DC_RETURN' and dist(pb,[68,62,88,82])<gap(net,'DC_RETURN'):findings.append({'type':'U3_backside_reservation','pin':ref+'.'+pn})
checked=0;exceptions=[];mins={}
for a,c in itertools.combinations(pads,2):
 if a['net']==c['net'] or not set(a['layers'])&set(c['layers']):continue
 target=gap(a['net'],c['net']);exc=None
 if a['ref']==c['ref']:exc=next((e for e in rules['package_exceptions_proposed'] if e['ref']==a['ref'] and set(e['pins'])=={a['pin'],c['pin']} and set(e['nets'])=={a['net'],c['net']}),None)
 if exc:
  assert set(a['layers'])&set(c['layers'])<=set(exc['layers']);target=exc['proposed_drawn_floor_mm'];exceptions.append(a['ref']+'.'+a['pin']+'-'+c['pin'])
 checked+=1
 # Real native rounded/custom copper shapes; four-mm surface target on flat board.
 if a['shape'].Collide(c['shape'],k.FromMM(target-.00002)):
  lo=0.;hi=target
  for _ in range(22):
   mid=(lo+hi)/2
   if a['shape'].Collide(c['shape'],k.FromMM(mid)):hi=mid
   else:lo=mid
  findings.append({'type':'pad_spacing','a':a['ref']+'.'+a['pin'],'b':c['ref']+'.'+c['pin'],'nets':[a['net'],c['net']],'actual_mm':round(lo,6),'target_mm':target,'local_exception':bool(exc)})
for a,c in itertools.combinations(parts,2):
 if dist(a['court'],c['court'])<=0:findings.append({'type':'courtyard_overlap','refs':[a['ref'],c['ref']]})
expected={(p['ref'],p['pin']):n['intent_net'] for n in binding['records'] for p in n['pins']};expected.update({(p['ref'],p['pin']):'EXPLICIT_NC' for p in binding['no_connects']});actual={(p['ref'],p['pin']):p['net'] for p in pads};assert actual==expected
result={'tool':k.GetBuildVersion(),'source_board_sha256':hashlib.sha256((S/'SC08_prototype.kicad_pcb').read_bytes()).hexdigest(),'method':'Actualnativeeffectivecoppershapecollisionchecks;4mmHVflatsurface,2mmoutput,.30explicitlocal;22exactsamecomponentexceptions;notassembledcreepagequalification','parts':parts,'pins':len(pads),'pairs_checked':checked,'exceptions_used':exceptions,'pins_parity':True,'no_tracks_vias':len(list(b.GetTracks()))==0,'findings':findings,'passed':not findings}
(W/'extra-placement-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'pins':len(pads),'pairs':checked,'findings':findings}))
