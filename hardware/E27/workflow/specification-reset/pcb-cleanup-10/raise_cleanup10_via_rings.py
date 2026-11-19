from pathlib import Path
import pcbnew,json,shutil
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-cleanup-10';B=D/'design/Velluneo_driver.kicad_pcb';shutil.copyfile(B,D/'evidence/before-via-ring-update.kicad_pcb');pro=B.with_suffix('.kicad_pro');j=json.loads(pro.read_text());j['board']['design_settings']['rules']['min_via_annular_width']=.2;b=pcbnew.LoadBoard(str(B));count=0
for t in b.GetTracks():
 if isinstance(t,pcbnew.PCB_VIA):t.SetWidth(pcbnew.FromMM(.7));count+=1
pcbnew.SaveBoard(str(B),b);pro.write_text(json.dumps(j,indent=2)+'\n');print('Enlarged',count,'vias from0.6 to0.7mm, same0.3mm holes/positions, ring0.2mm')
