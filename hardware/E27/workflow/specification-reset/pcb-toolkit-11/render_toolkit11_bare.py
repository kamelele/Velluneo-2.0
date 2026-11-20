from pathlib import Path
import pcbnew,shutil,json,hashlib
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-toolkit-11';B=D/'design/Velluneo_driver.kicad_pcb';O=D/'render';src=O/'Velluneo_bareboard_RENDER_ONLY.kicad_pcb';b=pcbnew.LoadBoard(str(B));count=0
for f in b.GetFootprints():count+=len(f.Models());f.Models().clear()
options=b.GetPlotOptions();selection=options.GetLayerSelection();selection.RemoveLayer(pcbnew.F_Paste);selection.RemoveLayer(pcbnew.B_Paste);options.SetLayerSelection(selection)
pcbnew.SaveBoard(str(src),b)
for ext in('.kicad_pro','.kicad_sch','.kicad_dru'):shutil.copyfile(B.with_suffix(ext),src.with_suffix(ext))
(O/'render-source.json').write_text(json.dumps(dict(source_board_sha256=hashlib.sha256(B.read_bytes()).hexdigest(),render_board_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),only_change='Component3Dmodelreferences removed and pasteoverlay hidden using plot layer selection in render-onlycopy; actualeditablePCB retains all33models/paste. Bare-board copper/mask/holes/stackup/labels unchanged.',removed_models=count,scope='BarePCBvisualization, not assembledproduct/physicalprocessqualification.'),indent=2)+'\n');print('Render-only bareboard',count,'componentmodels hidden, paste overlay off')
