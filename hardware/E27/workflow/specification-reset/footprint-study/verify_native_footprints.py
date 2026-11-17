#!/usr/bin/env python3
"""Native KiCad parsing/geometry comparison against independently sourced copper tables."""
from pathlib import Path
import json,hashlib
import pcbnew
P=Path(__file__).resolve().parent.parent;D=P/'footprint-study';L=P/'libraries/Velluneo_Driver.pretty'
g=json.loads((D/'geometry-contract.json').read_text());reports=[]
for a in g['parts']:
 f=pcbnew.FootprintLoad(str(L),a['name']);assert f is not None,a['name']
 actual=[]
 for p in f.Pads():
  pos=p.GetPosition();sz=p.GetSize();actual.append((p.GetNumber(),pcbnew.ToMM(pos.x),pcbnew.ToMM(pos.y),pcbnew.ToMM(sz.x),pcbnew.ToMM(sz.y)))
  assert p.GetAttribute()==pcbnew.PAD_ATTRIB_SMD
  for layer in [pcbnew.F_Cu,pcbnew.F_Mask,pcbnew.F_Paste]:assert p.GetLayerSet().Contains(layer)
 expected=[tuple(x) for x in a['pads']];assert len({x[0] for x in actual})==len(actual)
 assert sorted(actual)==sorted(expected),(a['name'],actual,expected)
 cx,cy=[x/2 for x in a['courtyard_mm']]
 for _,x,y,w,h in actual:assert abs(x)+w/2<cx and abs(y)+h/2<cy
 assert a['body_mm'][0]/2<cx and a['body_mm'][1]/2<cy
 if a['ref']=='U1':assert not any(abs(x-2.7)<1e-9 and abs(y+.635)<1e-9 for _,x,y,_,_ in actual)
 if a['ref']=='Q1':assert set(x[0] for x in actual)=={'1','2','3','4'}
 path=L/(a['name']+'.kicad_mod');reports.append({'ref':a['ref'],'footprint':a['name'],'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pads':actual,'result':'pass'})
report={'result':'pass','native_pcbnew':pcbnew.Version(),'scope':'Native footprint loading, unique exact pad inventory/centres/sizes/layers and reserved courtyard body/pad containment; not PCB DRC, solder/process, thermal or safety approval','parts':reports}
(D/'native-geometry-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
