from pathlib import Path
import json, hashlib
import pcbnew as p
W=Path(__file__).resolve().parent
D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16'
f=D/'design/Velluneo_driver.kicad_pcb'
j=json.loads((D/'route-plan.json').read_text())
assert j['all_planned']
assert hashlib.sha256(f.read_bytes()).hexdigest()==j['source_sha256']
b=p.LoadBoard(str(f)); assert not list(b.GetTracks())
aliases={'AC_CAP_A':'Net-(F1-Pad1)','AC_CAP_B':'Net-(BR1-AC-Pad2)','AC_FUSED':'Net-(F1-Pad2)','AC_LIMITED':'Net-(BR1-AC-Pad4)','CLAMP':'Net-(D1-K)','AUX_RECT':'Net-(D2-K)','BLEED_MID':'Net-(R2-Pad2)'}
nets={str(n.GetNetname()):n for n in b.GetNetsByNetcode().values()}
layers=[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]; owned=[]
def pt(a):return p.VECTOR2I(p.FromMM(a[0]+100),p.FromMM(a[1]+100))
for x in j['elements']:
 name=aliases.get(x['net'],'/'+x['net']); n=nets[name]
 if x['via']:
  t=p.PCB_VIA(b);t.SetPosition(pt(x['a']));t.SetWidth(p.FromMM(.8));t.SetDrill(p.FromMM(.3));t.SetViaType(p.VIATYPE_THROUGH);t.SetLayerPair(p.F_Cu,p.B_Cu)
 else:
  t=p.PCB_TRACK(b);t.SetStart(pt(x['a']));t.SetEnd(pt(x['b']));t.SetWidth(p.FromMM(x['width']));t.SetLayer(layers[x['layers'][0]])
 t.SetNet(n);b.Add(t);owned.append(t)
p.SaveBoard(str(f),b)
print('saved',len(owned),'objects')
