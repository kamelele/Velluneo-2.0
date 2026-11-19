from pathlib import Path
import json,hashlib,pcbnew
D=Path(__file__).resolve().parent;S=D/'studies/sense';src=S/'routing-seed.kicad_pcb';out=S/'ground-seed.kicad_pcb';j=json.loads((D/'ground-plan.json').read_text());assert hashlib.sha256(src.read_bytes()).hexdigest()==j['input_source_sha256'];b=pcbnew.LoadBoard(str(src));mp=json.loads((D/'design/full-build-result.json').read_text())['logical_to_native_netnames'];nets=b.GetNetsByName()
def v(p):return pcbnew.VECTOR2I(pcbnew.FromMM(100+p[0]),pcbnew.FromMM(100+p[1]))
for e in j['new_elements']:
 if e['via']:
  t=pcbnew.PCB_VIA(b);t.SetPosition(v(e['a']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetDrill(pcbnew.FromMM(.3));t.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);t.SetViaType(pcbnew.VIATYPE_THROUGH)
 else:
  t=pcbnew.PCB_TRACK(b);t.SetStart(v(e['a']));t.SetEnd(v(e['b']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetLayer(pcbnew.F_Cu if e['layers']==[0]else pcbnew.B_Cu)
 t.SetNetCode(nets[mp[e['net']]].GetNetCode());b.Add(t)
pcbnew.SaveBoard(str(out),b)
for stem in('ground-seed','Velluneo_route07'):
 if stem!='ground-seed':(S/(stem+'.kicad_pcb')).write_bytes(out.read_bytes())
 for ext in('.kicad_pro','.kicad_dru','.kicad_sch'):
  raw=(S/('Velluneo_sense_exploration'+ext)).read_bytes()
  if ext=='.kicad_pro':
   project=json.loads(raw);project['meta']['filename']=stem+ext
   for sheet in project.get('schematic',{}).get('top_level_sheets',[]):sheet.update(filename=stem+'.kicad_sch',name=stem)
   raw=(json.dumps(project,indent=2)+'\n').encode()
  (S/(stem+ext)).write_bytes(raw)
print(out)
