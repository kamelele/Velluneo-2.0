from pathlib import Path
import pcbnew,json,hashlib,shutil
D=Path(__file__).resolve().parent;B=D/'design/Velluneo_driver.kicad_pcb';plan=json.loads((D/'smoothing-plan.json').read_text());assert hashlib.sha256(B.read_bytes()).hexdigest()==plan['source_board_sha256'];b=pcbnew.LoadBoard(str(B));tracks=list(b.GetTracks());remove={i for c in plan['changes']for i in c['removed_indices']};pro=B.with_suffix('.kicad_pro').read_bytes();shutil.copyfile(B,D/'.work/before-smoothing.kicad_pcb')
for i in remove:b.Remove(tracks[i])
# Save/reload before iteration after SWIG container mutations.
pcbnew.SaveBoard(str(D/'.work/ripped.kicad_pcb'),b)
for ext in('.kicad_pro','.kicad_dru','.kicad_sch'):shutil.copyfile(B.with_suffix(ext),(D/'.work/ripped.kicad_pcb').with_suffix(ext))
b=pcbnew.LoadBoard(str(D/'.work/ripped.kicad_pcb'));nets={n.GetNetname().removeprefix('/'):n for n in b.GetNetsByNetcode().values()};layers=[pcbnew.F_Cu,pcbnew.In1_Cu,pcbnew.In2_Cu,pcbnew.B_Cu]
for c in plan['changes']:
 for e in c['new_elements']:
  t=pcbnew.PCB_TRACK(b);t.SetStart(pcbnew.VECTOR2I(*[pcbnew.FromMM(100+x)for x in e['a']]));t.SetEnd(pcbnew.VECTOR2I(*[pcbnew.FromMM(100+x)for x in e['b']]));t.SetWidth(pcbnew.FromMM(e['width']));t.SetLayer(layers[e['layers'][0]]);t.SetNet(nets[e['net']]);b.Add(t)
pcbnew.SaveBoard(str(B),b);B.with_suffix('.kicad_pro').write_bytes(pro);print('Saved smoothed board',flush=True)
