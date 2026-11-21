"""Separate UNADOPTED four-layer comparison. Never overwrite the two-layer source."""
from pathlib import Path
import json,hashlib,pcbnew,sys
D=Path(__file__).resolve().parent;S=D/'studies/sense';C=D/'studies/four-layer-comparison';C.mkdir(exist_ok=True);out=C/'Velluneo_four_layer_COMPARISON.kicad_pcb';plan=json.loads((D/'four-layer-plan.json').read_text());src=S/'Velluneo_route07.kicad_pcb';assert hashlib.sha256(src.read_bytes()).hexdigest()==plan['input_source_sha256']
if sys.argv[1]=='base':
 b=pcbnew.LoadBoard(str(src));b.SetCopperLayerCount(4)
 ls=pcbnew.LSET()
 for layer in (pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu):ls.AddLayer(layer)
 for z in b.Zones():
  if z.GetIsRuleArea():z.SetLayerSet(ls)
 for t in list(b.GetTracks()):
  if t.GetNetname().removeprefix('/') in plan['ripped_nets']:b.Remove(t)
 pcbnew.SaveBoard(str(out),b)
else:
 b=pcbnew.LoadBoard(str(out));mp=json.loads((D/'design/full-build-result.json').read_text())['logical_to_native_netnames'];nets=b.GetNetsByName();layers=[pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu]
 def v(p):return pcbnew.VECTOR2I(pcbnew.FromMM(100+p[0]),pcbnew.FromMM(100+p[1]))
 seen=set()
 for e in plan['new_elements']:
  if e['via']:
   key=(e['net'],*e['a'])
   if key in seen:continue
   seen.add(key);t=pcbnew.PCB_VIA(b);t.SetPosition(v(e['a']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetDrill(pcbnew.FromMM(.3));t.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);t.SetViaType(pcbnew.VIATYPE_THROUGH)
  else:
   t=pcbnew.PCB_TRACK(b);t.SetStart(v(e['a']));t.SetEnd(v(e['b']));t.SetWidth(pcbnew.FromMM(e['width']));t.SetLayer(layers[e['layers'][0]])
  t.SetNetCode(nets[mp[e['net']]].GetNetCode());b.Add(t)
 pcbnew.SaveBoard(str(out),b)
 for ext in('.kicad_pro','.kicad_dru','.kicad_sch'):
  raw=(S/('Velluneo_route07'+ext)).read_bytes()
  if ext=='.kicad_pro':
   project=json.loads(raw);project['meta']['filename']=out.stem+ext
   for sheet in project.get('schematic',{}).get('top_level_sheets',[]):sheet.update(filename=out.stem+'.kicad_sch',name=out.stem)
   raw=(json.dumps(project,indent=2)+'\n').encode()
  (C/(out.stem+ext)).write_bytes(raw)
 for name in('fp-lib-table','sym-lib-table'):
  path=S/name
  if path.exists():(C/name).write_bytes(path.read_bytes())
 (C/'process-status.json').write_text(json.dumps(dict(adopted=False,user_process_approval=False,exact_stackup_approved=False,source_2layer_sha256=plan['input_source_sha256'],board_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),scope='Reversible engineering comparison only; exact dielectric/copper stackup, assembly and cost remain undefined.'),indent=2)+'\n')
 print('Saved unadopted comparison',out)
