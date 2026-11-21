"""Deliberately invalid diagnostic copies only; never modify product candidates."""
from pathlib import Path
import pcbnew,json,hashlib,shutil
D=Path(__file__).resolve().parent;S=D/'design';C=S
def make(src,folder,kind):
 folder.mkdir(parents=True,exist_ok=True);b=pcbnew.LoadBoard(str(src));pads={f.GetReference()+'.'+p.GetNumber():p for f in b.GetFootprints()for p in f.Pads()}
 a,z=('R9.2','U1.5')if kind=='topology'else('R9.1','T1.10'if kind=='inner'else'Q1.2');t=pcbnew.PCB_TRACK(b);t.SetStart(pads[a].GetPosition());t.SetEnd(pads[z].GetPosition());t.SetWidth(pcbnew.FromMM(.4));t.SetLayer(pcbnew.In1_Cu if kind=='inner'else pcbnew.F_Cu);t.SetNet(pads[a].GetNet());b.Add(t)
 out=folder/src.name;pcbnew.SaveBoard(str(out),b)
 for ext in('.kicad_pro','.kicad_dru','.kicad_sch'):shutil.copyfile(src.with_suffix(ext),out.with_suffix(ext))
 for name in('fp-lib-table','sym-lib-table'):shutil.copyfile(src.parent/name,folder/name)
 return dict(kind=kind,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),negative_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),negative_path=out.relative_to(D).as_posix(),injected_track=dict(a=a,b=z,layer='In1.Cu'if kind=='inner'else'F.Cu',net=pads[a].GetNetname()),expected='C1 junction-cut separation fails'if kind=='topology'else'Native clearance/short violations detected')
rows=[make(S/'Velluneo_driver.kicad_pcb',D/'.work/negative','surface'),make(C/'Velluneo_driver.kicad_pcb',D/'.work/negative-four','inner'),make(C/'Velluneo_driver.kicad_pcb',D/'.work/negative-topology','topology')]
(D/'design/checks/negative-controls-inputs.json').write_text(json.dumps(rows,indent=2)+'\n');print('Built three intentionally invalid copies')
