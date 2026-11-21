"""Meaningful native disposable negative controls, never customer CAD writes."""
from pathlib import Path
import argparse,copy,json,shutil,re
import pcbnew as k
import checker as c

HERE=Path(__file__).resolve().parent;F=HERE/'fixtures';F.mkdir(exist_ok=True)
def v(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def build(contract):
 b=k.BOARD();b.SetCopperLayerCount(2);nets={}
 for native in contract.mapping:
  net=k.NETINFO_ITEM(b,native);b.Add(net);nets[native]=net
 refs={};pads={}
 for i,((ref,pin),native) in enumerate(sorted(contract.expected.items())):
  if ref not in refs:
   f=k.FOOTPRINT(b);f.SetReference(ref);f.SetValue('SYNTHETIC DISPOSABLE ONLY');b.Add(f);refs[ref]=f
  p=k.PAD(refs[ref]);p.SetNumber(pin);p.SetAttribute(k.PAD_ATTRIB_SMD);p.SetShape(k.PAD_SHAPE_RECT);p.SetSize(v(1,1));layers=k.LSET();layers.AddLayer(k.F_Cu);p.SetLayerSet(layers);p.SetPosition(v(10+(i%8)*10,10+(i//8)*10));p.SetNet(nets[native]);refs[ref].Add(p);pads[(ref,pin)]=p
 for a,z in [((0,2),(2,0)),((2,0),(98,0)),((98,0),(100,2)),((100,2),(100,98)),((100,98),(98,100)),((98,100),(2,100)),((2,100),(0,98)),((0,98),(0,2))]:
  e=k.PCB_SHAPE();e.SetShape(k.SHAPE_T_SEGMENT);e.SetLayer(k.Edge_Cuts);e.SetStart(v(*a));e.SetEnd(v(*z));e.SetWidth(k.FromMM(.05));b.Add(e)
 return b,pads,nets
def track(b,net,a,z):
 t=k.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*z));t.SetWidth(k.FromMM(.3));t.SetLayer(k.F_Cu);t.SetNet(net);b.Add(t);return t
def main():
 p=argparse.ArgumentParser();p.add_argument('--project',required=True);p.add_argument('--matrix',required=True);a=p.parse_args();contract=c.Contract(a.project,a.matrix);results=[]
 def execute(name,mutate,expected=None,stop=None):
  b,pads,nets=build(contract);mutate(b,pads,nets);fn=F/(name+'.kicad_pcb');k.SaveBoard(str(fn),b,True)
  # SaveBoard itself may propagate a colliding track/via to a touched pad's net.
  # Deliberately restore the adverse saved identity in disposable fixtures only.
  if name in ['different-net-track-crosses-pad','throughvia-pad-invasion']:
   tag='(segment' if name.startswith('different') else '(via'
   text=fn.read_text(encoding='utf-8');before,tail=text.rsplit(tag,1);tail=re.sub(r'\(net "[^"]*"\)','(net "/AC_L")',tail,count=1);fn.write_text(before+tag+tail,encoding='utf-8')
  r=c.run(fn,a.project,a.matrix);c.dump(F/(name+'.json'),r)
  if expected is None and stop is None:ok=r.get('passed') and len(r.get('all_55_pair_minima',[]))==55
  elif stop:ok=r.get('stopped') and stop in r.get('error','')
  else:ok=not r.get('passed') and any(x['type']==expected for x in r.get('findings',[]))
  results.append({'name':name,'passed':bool(ok),'expected_finding':expected,'expected_stop':stop,'board_sha256':r['board_sha256'],'report':str(fn.with_suffix('.json'))})
  if not ok:raise AssertionError((name,r))
 execute('native-positive-46-pad-55-pair',lambda b,p,n:None)
 execute('different-net-track-crosses-pad',lambda b,p,n:track(b,n['/AC_L'],(19,10),(21,10)),'copper_spacing')
 def collide(b,p,n):
  p[('C1','1')].SetPosition(v(35,35));p[('C1','2')].SetPosition(v(36.5,35));p[('C1','2')].SetOrientationDegrees(45)
 execute('rotated-pad-native-shape',collide,'copper_spacing')
 execute('chamfer-copper-corner',lambda b,p,n:p[('C1','1')].SetPosition(v(1,1)),'copper_edge_setback')
 def via(b,p,n):
  x=k.PCB_VIA(b);x.SetPosition(v(20,10.5));x.SetWidth(k.FromMM(.8));x.SetDrill(k.FromMM(.3));x.SetViaType(k.VIATYPE_THROUGH);x.SetLayerPair(k.F_Cu,k.B_Cu);x.SetNet(n['/AC_L']);b.Add(x)
 execute('throughvia-pad-invasion',via,'copper_spacing')
 def wrong(b,p,n):p[('J1','1')].SetNet(n['/AC_N'])
 execute('wrong-native-pin-identity',wrong,stop='Exact native pad/net binding mismatch')
 def arc(b,p,n):
  x=k.PCB_ARC(b);x.SetStart(v(5,5));x.SetMid(v(6,6));x.SetEnd(v(7,5));x.SetWidth(k.FromMM(.3));x.SetLayer(k.F_Cu);x.SetNet(n['/AC_L']);b.Add(x)
 execute('unsupported-arc-stops',arc,stop='Only straight PCB_TRACK')
 execute('stock-T1-legacy-pin8-rejected',lambda b,p,n:p[('T1','2')].SetNumber('8'),stop='Exact native pad/net binding mismatch')
 def phantom(b,p,n):
  f=next(f for f in b.GetFootprints() if f.GetReference()=='T1');pad=k.PAD(f);pad.SetNumber('4');pad.SetAttribute(k.PAD_ATTRIB_SMD);pad.SetShape(k.PAD_SHAPE_RECT);pad.SetSize(v(1,1));ls=k.LSET();ls.AddLayer(k.F_Cu);pad.SetLayerSet(ls);pad.SetPosition(v(90,10));pad.SetNet(n['/LED_PLUS']);f.Add(pad)
 execute('stock-T1-phantom-NC4-rejected',phantom,stop='Exact native pad/net binding mismatch')

 def graphic(b,p,n):
  x=k.PCB_SHAPE();x.SetShape(k.SHAPE_T_SEGMENT);x.SetStart(v(5,5));x.SetEnd(v(7,5));x.SetWidth(k.FromMM(.3));x.SetLayer(k.F_Cu);b.Add(x)
 execute('unbound-free-copper-stops',graphic,stop='Free copper graphics/text')
 def zone(b,p,n,outside=False,invasion=False):
  z=k.ZONE(b);z.SetLayer(k.F_Cu);z.SetNet(n['/AC_L']);z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_NEVER)
  box=[18,8,22,12] if invasion else [83,83,93,93]
  x0,y0,x1,y1=box;z.Outline().NewOutline()
  for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]:z.Outline().Append(k.FromMM(x),k.FromMM(y))
  filled=c.q.rectangle([82,82,94,94] if outside else ([19,9,21,11] if invasion else [84,84,92,92]))
  z.SetFilledPolysList(k.F_Cu,filled);z.SetIsFilled(True);z.SetNeedRefill(False);b.Add(z)
 execute('saved-filled-zone-positive',lambda b,p,n:zone(b,p,n))
 execute('saved-zone-foreign-pad-invasion',lambda b,p,n:zone(b,p,n,invasion=True),'copper_spacing')
 execute('saved-zone-outside-outline-stops',lambda b,p,n:zone(b,p,n,outside=True),stop='outside actual zone outline')
 ex={'authorized_for_bounded_geometry_screen_by':'SYNTHETIC disposable negative-control context only','CAT_graph_sha256':c.q.sha(Path(a.project)/'intended-connectivity.CAT01.json'),'matrix_sha256':c.q.sha(a.matrix),'exceptions':[{'ref':'U1','pins':['3','4'],'nets':['FB_INDUCTOR','BUS_FILTERED'],'layers':['B.Cu'],'escape_layers':['B.Cu'],'except_object_types':['pad','track'],'escape_margin_mm':1.,'proposed_drawn_floor_mm':.6}]}
 ep=F/'synthetic-exceptions.json';c.dump(ep,ex)
 ex['exceptions'][0]['region_bbox_mm']=[28.5,28.5,33.17,31.5];c.dump(ep,ex)
 for outside in [False,True]:
  b,pads,nets=build(contract);layers=k.LSET();layers.AddLayer(k.B_Cu)
  for pin,x in [('3',30),('4',31.67)]:pads[('U1',pin)].SetLayerSet(layers);pads[('U1',pin)].SetPosition(v(x,30))
  if outside:
   for net,x in [('/FB_INDUCTOR',30),('/BUS_FILTERED',31.67)]:
    t=track(b,nets[net],(x,30),(x,50));t.SetLayer(k.B_Cu)
  name='exception-outside-region-still-fails' if outside else 'exception-local-pads-positive'
  fn=F/(name+'.kicad_pcb');k.SaveBoard(str(fn),b,True);r=c.run(fn,a.project,a.matrix,ep);c.dump(F/(name+'.json'),r)
  ok=(not r.get('passed') and any(x['type']=='copper_spacing' for x in r.get('findings',[]))) if outside else r.get('passed')
  results.append({'name':name,'passed':bool(ok),'board_sha256':r['board_sha256']})
  if not ok:raise AssertionError((name,r))
 for kind in ['via','zone']:
  b,pads,nets=build(contract);layers=k.LSET();layers.AddLayer(k.B_Cu)
  for pin,x in [('3',30),('4',31.67)]:pads[('U1',pin)].SetLayerSet(layers);pads[('U1',pin)].SetPosition(v(x,30))
  if kind=='via':
   x=k.PCB_VIA(b);x.SetPosition(v(30,30));x.SetWidth(k.FromMM(.8));x.SetDrill(k.FromMM(.3));x.SetViaType(k.VIATYPE_THROUGH);x.SetLayerPair(k.F_Cu,k.B_Cu);x.SetNet(nets['/FB_INDUCTOR']);b.Add(x)
  else:
   x=k.ZONE(b);x.SetLayer(k.B_Cu);x.SetNet(nets['/FB_INDUCTOR']);x.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_NEVER);x.Outline().NewOutline()
   for px,py in [(29.5,29.5),(30.5,29.5),(30.5,30.5),(29.5,30.5)]:x.Outline().Append(k.FromMM(px),k.FromMM(py))
   x.SetFilledPolysList(k.B_Cu,c.q.rectangle([29.5,29.5,30.5,30.5]));x.SetIsFilled(True);x.SetNeedRefill(False);b.Add(x)
  name='exception-does-not-exempt-'+kind;fn=F/(name+'.kicad_pcb');k.SaveBoard(str(fn),b,True);r=c.run(fn,a.project,a.matrix,ep);c.dump(F/(name+'.json'),r)
  ok=not r.get('passed') and any(y['type']=='copper_spacing' and kind in y.get('kinds',[]) and y.get('target_mm')==2. for y in r.get('findings',[]))
  results.append({'name':name,'passed':bool(ok),'board_sha256':r['board_sha256']})
  if not ok:raise AssertionError((name,r))
 ex['exceptions'][0]['escape_margin_mm']=1.1;c.dump(ep,ex);r=c.run(fn,a.project,a.matrix,ep)
 ok=r.get('stopped') and '1.0mm bound' in r.get('error','');results.append({'name':'exception-expanded-region-rejected','passed':bool(ok),'error':r.get('error')})
 if not ok:raise AssertionError(r)
 other=copy.deepcopy(ex);other['exceptions'][0].update(pins=['2','4'],nets=['M','BUS_FILTERED'],escape_margin_mm=1.,proposed_drawn_floor_mm=1.8);c.dump(ep,other);r=c.run(fn,a.project,a.matrix,ep)
 ok=r.get('stopped') and '0.3mm bound' in r.get('error','');results.append({'name':'v2-one-mm-not-allowed-on-other-U1-pair','passed':bool(ok),'error':r.get('error')})
 if not ok:raise AssertionError(r)
 ex['exceptions'][0]['escape_margin_mm']=1.;ex['exceptions'][0]['region_bbox_mm'][0]+=.1;c.dump(ep,ex);r=c.run(fn,a.project,a.matrix,ep)
 ok=r.get('stopped') and 'Frozen package exception region differs' in r.get('error','');results.append({'name':'stale-frozen-exception-region-rejected','passed':bool(ok),'error':r.get('error')})
 if not ok:raise AssertionError(r)
 missing=c.load(a.matrix);missing['pair_matrix'].pop();mp=F/'missing-matrix-pair.json';c.dump(mp,missing);r=c.run(fn,a.project,mp)
 ok=r.get('stopped') and 'Missing/extra matrix pairs' in r.get('error','');results.append({'name':'missing-one-of55-matrix-pairs-rejected','passed':bool(ok),'error':r.get('error')})
 if not ok:raise AssertionError(r)
 report={'passed':all(x['passed'] for x in results),'checker_sha256':c.q.sha(HERE/'checker.py'),'kernel_sha256':c.q.sha(HERE/'kernel_sc08.py'),'tests_sha256':c.q.sha(__file__),'scope':'Synthetic disposable native boards only; positive all46pad/55matrix identities and adversarial geometry/native-net/unsupported-copper controls. Not validation of customer routing or a replacement for native DRC.','tests':results}
 c.dump(HERE/'test-results.json',report);print(json.dumps({'passed':report['passed'],'tests':len(results)}))
if __name__=='__main__':main()


