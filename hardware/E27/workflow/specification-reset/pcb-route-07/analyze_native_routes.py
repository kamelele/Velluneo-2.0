"""Read saved native geometry/connectivity; diagnostic junction cuts are never product CAD."""
from pathlib import Path
import json,math,hashlib,collections,pcbnew,sys
D=Path(__file__).resolve().parent;four='--four'in sys.argv;S=D/('studies/four-layer-comparison'if four else'studies/sense');B=S/('Velluneo_four_layer_COMPARISON.kicad_pcb'if four else'Velluneo_route07.kicad_pcb');B=Path(sys.argv[sys.argv.index('--board')+1])if '--board'in sys.argv else B;b=pcbnew.LoadBoard(str(B));b.BuildConnectivity()
def padmap(board):return{f.GetReference()+'.'+p.GetNumber():p for f in board.GetFootprints()for p in f.Pads()}
pp=padmap(b);baseline_board=pcbnew.LoadBoard(str(D/'design/Velluneo_specification_reset.kicad_pcb'))
for f in baseline_board.GetFootprints():
 if f.GetReference()=='F1':f.SetOrientationDegrees(180)
 if f.GetReference()=='R10':
  if f.GetLayer()!=pcbnew.F_Cu:f.Flip(f.GetPosition(),False)
  f.SetOrientationDegrees(270);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(82.8),pcbnew.FromMM(102.35)))
 if f.GetReference()=='R4':
  if f.GetLayer()!=pcbnew.B_Cu:f.Flip(f.GetPosition(),False)
  f.SetOrientationDegrees(0);f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(104.5),pcbnew.FromMM(115.8)))
base=padmap(baseline_board)
assert len(pp)==len(base)==81
def sig(p):return(p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y,p.GetLayerSet().FmtBin())
assert all(sig(p)==sig(base[k])for k,p in pp.items())
expected={p['ref']+'.'+n:net for p in json.loads((D/'design/proposed-parts.json').read_text())for n,net in p['pins'].items()};mapping=json.loads((D/'design/full-build-result.json').read_text())['logical_to_native_netnames']
for k,p in pp.items():
 n=expected[k]
 if n not in mapping:assert p.GetNetname().startswith('unconnected-'),(k,n,p.GetNetname())
 else:assert p.GetNetname()==mapping[n],(k,n,p.GetNetname())
def groups(board):
 board.BuildConnectivity();c=board.GetConnectivity();pm=padmap(board);ids={int(p.this):k for k,p in pm.items()};seen=set();out=[]
 for k,p in pm.items():
  if k in seen:continue
  todo=[p];visit=set();members=set()
  while todo:
   t=todo.pop();i=int(t.this)
   if i in visit:continue
   visit.add(i)
   if i in ids:members.add(ids[i]);seen.add(ids[i])
   todo.extend(c.GetConnectedItems(t))
  out.append(sorted(members))
 return out
gg=groups(b);trackrows=[];viarows=[]
for t in b.GetTracks():
 if isinstance(t,pcbnew.PCB_VIA):viarows.append(dict(net=t.GetNetname(),xy_mm=[pcbnew.ToMM(t.GetPosition().x)-100,pcbnew.ToMM(t.GetPosition().y)-100],diameter_mm=pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu)),drill_mm=pcbnew.ToMM(t.GetDrillValue())))
 else:trackrows.append(dict(net=t.GetNetname(),layer={pcbnew.F_Cu:'F',pcbnew.B_Cu:'B',pcbnew.In1_Cu:'In1',pcbnew.In2_Cu:'In2'}[t.GetLayer()],width_mm=pcbnew.ToMM(t.GetWidth()),points_mm=[[pcbnew.ToMM(p.x)-100,pcbnew.ToMM(p.y)-100]for p in(t.GetStart(),t.GetEnd())],length_mm=pcbnew.ToMM(t.GetLength())))
def cut_test(key,radius,terminals):
 board=pcbnew.LoadBoard(str(B));p=padmap(board)[key];net=p.GetNetCode();centre=p.GetPosition();cx,cy=pcbnew.ToMM(centre.x),pcbnew.ToMM(centre.y);original=list(board.GetTracks());park=pcbnew.VECTOR2I(pcbnew.FromMM(1000),pcbnew.FromMM(1000));p.SetNetCode(0);p.SetPosition(park)
 def v(a):return pcbnew.VECTOR2I(pcbnew.FromMM(a[0]),pcbnew.FromMM(a[1]))
 for t in original:
  if t.GetNetCode()!=net:continue
  if isinstance(t,pcbnew.PCB_VIA):
   if math.hypot(pcbnew.ToMM(t.GetPosition().x)-cx,pcbnew.ToMM(t.GetPosition().y)-cy)<radius:t.SetNetCode(0);t.SetPosition(park)
   continue
  a=[pcbnew.ToMM(t.GetStart().x),pcbnew.ToMM(t.GetStart().y)];z=[pcbnew.ToMM(t.GetEnd().x),pcbnew.ToMM(t.GetEnd().y)];d=[z[i]-a[i]for i in(0,1)];A=sum(x*x for x in d);q=[a[0]-cx,a[1]-cy];bb=2*sum(q[i]*d[i]for i in(0,1));cc=sum(x*x for x in q)-radius*radius;disc=bb*bb-4*A*cc;ts=[0.,1.]
  if A and disc>0:ts+= [u for u in((-bb-math.sqrt(disc))/(2*A),(-bb+math.sqrt(disc))/(2*A))if 0<u<1]
  ts=sorted(ts);outside=[]
  for lo,hi in zip(ts,ts[1:]):
   mid=(lo+hi)/2
   if math.hypot(a[0]+mid*d[0]-cx,a[1]+mid*d[1]-cy)>radius:outside.append(([a[i]+lo*d[i]for i in(0,1)],[a[i]+hi*d[i]for i in(0,1)]))
  if not outside:t.SetNetCode(0);t.SetStart(park);t.SetEnd(park);continue
  t.SetStart(v(outside[0][0]));t.SetEnd(v(outside[0][1]))
  for x,y in outside[1:]:
   u=pcbnew.PCB_TRACK(board);u.SetLayer(t.GetLayer());u.SetWidth(t.GetWidth());u.SetNetCode(net);u.SetStart(v(x));u.SetEnd(v(y));board.Add(u)
 gs=groups(board);membership={k:i for i,g in enumerate(gs)for k in g};return dict(junction=key,cut_radius_mm=radius,terminal_groups={k:membership[k]for k in terminals},terminal_component_members={k:gs[membership[k]]for k in terminals},separate=len({membership[k]for k in terminals})==len(terminals),scope='Diagnostic idealized junction removal; distinct outside-disk native copper components only, not impedance/noise proof.')
cuts=[cut_test('C1.2',1.25,['U1.5','R9.2','BR1.3','T1.2']),cut_test('R9.1',1.25,['Q1.3','R6.1']),cut_test('Q1.3',1.25,['R8.2','R9.1']),cut_test('T1.4',1.25,['R4.1','D2.2'])]
plan=json.loads((D/('four-layer-plan.json'if four else'ground-plan.json')).read_text());branches=list(plan.get('attempts',[]))
for i,es in plan.get('active_routes',{}).items():
 task=plan['tasks'][int(i)];row=dict(task=int(i),**task);row.update(planar_length_mm=sum(math.dist(e['a'],e['b'])for e in es if not e['via']),new_vias=sum(e['via']for e in es));branches.append(row)
out=dict(board_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),footprints=len(b.GetFootprints()),pads=len(pp),physical_pin_intent_matches=True,pad_geometry_matches_declared_layout_alternative=True,copper_layers=b.GetCopperLayerCount(),connected_pad_groups=gg,connected_group_count=len(gg),track_segments=len(trackrows),vias=len(viarows),tracks=trackrows,via_details=viarows,junction_cut_diagnostics=cuts,protected_branch_plan=branches,scope='Actual native geometry/connectivity and conditional cut diagnostics. Native DRC reports remain authoritative for clearances and unconnected items; no operating/EMC/insulation/assembly/thermal approval.')
(Path(sys.argv[sys.argv.index('--output')+1])if '--output'in sys.argv else S/'route07-native-analysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in('track_segments','vias','connected_group_count','junction_cut_diagnostics')}))
