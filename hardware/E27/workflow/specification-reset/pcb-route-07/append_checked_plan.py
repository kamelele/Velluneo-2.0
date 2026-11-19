"""Apply one source-hash-bound candidate without changing other saved copper."""
from pathlib import Path
import json,hashlib,pcbnew,sys
D=Path(__file__).resolve().parent;S=D/'studies/sense';out=S/'Velluneo_route07.kicad_pcb';plan=D/sys.argv[1];j=json.loads(plan.read_text());assert hashlib.sha256(out.read_bytes()).hexdigest()==j['input_source_sha256'];assert j['new_elements'] is not None
b=pcbnew.LoadBoard(str(out));mp=json.loads((D/'design/full-build-result.json').read_text())['logical_to_native_netnames'];nets=b.GetNetsByName()
def v(p):return pcbnew.VECTOR2I(pcbnew.FromMM(100+p[0]),pcbnew.FromMM(100+p[1]))
for e in j['new_elements']:
 if e['via']:
  t=pcbnew.PCB_VIA(b);t.SetPosition(v(e['a']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetDrill(pcbnew.FromMM(.3));t.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);t.SetViaType(pcbnew.VIATYPE_THROUGH)
 else:
  t=pcbnew.PCB_TRACK(b);t.SetStart(v(e['a']));t.SetEnd(v(e['b']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetLayer(pcbnew.F_Cu if e['layers']==[0]else pcbnew.B_Cu)
 t.SetNetCode(nets[mp[e['net']]].GetNetCode());b.Add(t)
pcbnew.SaveBoard(str(out),b);print('Appended',len(j['new_elements']),plan.name)
