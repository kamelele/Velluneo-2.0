#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,sys
import pcbnew
P=Path(__file__).resolve().parent.parent;D=P/'footprint-completion';L=P/'libraries/Velluneo_Driver.pretty'
contract=json.loads((D/'geometry-contract.json').read_text());base=json.loads((P/'footprint-study/geometry-contract.json').read_text())
expected={}
for a in base['parts']:expected[a['name']]=[{'number':n,'at':[x,y],'size':[w,h],'type':'smd'} for n,x,y,w,h in a['pads']]
for a in contract['parts']:expected[a['name']]=a['pads']
t1path=P/'transformer-footprint/geometry-contract.json'
if t1path.exists():
 t1=json.loads(t1path.read_text());expected[t1['name']]=t1['pads']
results=[]
for name,pads in expected.items():
 fp=pcbnew.FootprintLoad(str(L),name);assert fp is not None,name
 actual={}
 for p in fp.Pads():
  n=p.GetNumber();assert n not in actual;pos=p.GetPosition();sz=p.GetSize();dr=p.GetDrillSize();is_tht=p.GetAttribute()==pcbnew.PAD_ATTRIB_PTH
  a={'number':n,'at':[pcbnew.ToMM(pos.x),pcbnew.ToMM(pos.y)],'size':[pcbnew.ToMM(sz.x),pcbnew.ToMM(sz.y)],'type':'thru_hole' if is_tht else 'smd'}
  if is_tht:a['drill']=pcbnew.ToMM(dr.x);assert dr.x==dr.y and a['drill']<min(a['size']);assert p.GetLayerSet().Contains(pcbnew.B_Cu)
  for layer in [pcbnew.F_Cu,pcbnew.F_Mask]:assert p.GetLayerSet().Contains(layer)
  assert p.GetLayerSet().Contains(pcbnew.F_Paste)==(not is_tht)
  actual[n]=a
 assert set(actual)=={p['number'] for p in pads}
 for p in pads:
  a=actual[p['number']]
  for key in ['at','size','type']:assert a[key]==p[key],(name,key,a,p)
  if p['type']=='thru_hole':assert a['drill']==p['drill']
 path=L/(name+'.kicad_mod');results.append({'name':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pads':list(actual.values()),'result':'pass'})
assign=json.loads((P/'footprint-study/assignments.json').read_text());parts=json.loads((P/'electrical-integration/proposed-parts.json').read_text());count=0
for a in parts:
 if a['ref'] not in assign:assert a['ref']=='T1';continue
 ass=assign[a['ref']];assert ass['mpn']==a['mpn'];name=ass['footprint'].split(':',1)[1]
 assert {p['number'] for p in expected[name]}==set(a['pins']);count+=len(a['pins'])
assert (len(assign),count)==(31,79)
report={'result':'pass','native_pcbnew':pcbnew.Version(),'unique_modules':len(expected),'assigned_components':len(assign),'mapped_physical_terminals':count,'unassigned_components':[a['ref'] for a in parts if a['ref'] not in assign],'scope':'Native parse, exact numbered copper coordinates/sizes/layers/drills and symbol-terminal coverage. Does not qualify source completeness, forming, assembly, process, insulation, board geometry, or function.','modules':results}
(Path(sys.argv[1]) if len(sys.argv)>1 else D/'native-library-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='modules'}))
