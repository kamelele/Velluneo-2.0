"""Write the one source-hash-bound route plan, preserving the strict project policy."""
from pathlib import Path
import json,hashlib,pcbnew
D=Path(__file__).resolve().parent;E=D/'design';out=E/'Velluneo_driver.kicad_pcb';j=json.loads((D/'selected-route-plan.json').read_text());assert len(j['remaining_groups'])==27 and all(r['success']for r in j['attempts']);assert hashlib.sha256(out.read_bytes()).hexdigest()==j['source_board_sha256'];profile=(E/'Velluneo_driver.kicad_pro').read_bytes();(D/'.work/routing-input.kicad_pcb').write_bytes(out.read_bytes());b=pcbnew.LoadBoard(str(out));nets=b.GetNetsByName();mp=json.loads((E/'full-build-result.json').read_text())['logical_to_native_netnames'];layers=[pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu]
def v(p):return pcbnew.VECTOR2I(pcbnew.FromMM(100+p[0]),pcbnew.FromMM(100+p[1]))
seen={(t.GetNetname(),t.GetPosition().x,t.GetPosition().y)for t in b.GetTracks()if isinstance(t,pcbnew.PCB_VIA)}
for e in j['new_elements']:
 if e['via']:
  p=v(e['a']);key=(mp[e['net']],p.x,p.y)
  if key in seen:continue
  seen.add(key);t=pcbnew.PCB_VIA(b);t.SetPosition(p);t.SetWidth(pcbnew.FromMM(e['width']));t.SetDrill(pcbnew.FromMM(.3));t.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);t.SetViaType(pcbnew.VIATYPE_THROUGH)
 else:t=pcbnew.PCB_TRACK(b);t.SetStart(v(e['a']));t.SetEnd(v(e['b']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetLayer(layers[e['layers'][0]])
 t.SetNetCode(nets[mp[e['net']]].GetNetCode());b.Add(t)
pcbnew.SaveBoard(str(out),b);(E/'Velluneo_driver.kicad_pro').write_bytes(profile);print('Saved selected complete4Lroute',flush=True)
