from pathlib import Path
import pcbnew as k,json,hashlib,math
H=Path(__file__).resolve().parent;ROOT=H.parents[2];P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();b=k.LoadBoard(str(P/'SC09_compact.kicad_pcb'));rows=[]
for f in sorted(b.GetFootprints(),key=lambda f:f.GetReference()):
 pos=f.GetPosition();pads=[]
 for p in f.Pads():
  q=p.GetFPRelativePosition();z=p.GetPosition();sz=p.GetSize();d=p.GetDrillSize()
  pads.append({'pin':p.GetNumber(),'local_xy_mm':[k.ToMM(q.x),k.ToMM(q.y)],'global_xy_mm':[k.ToMM(z.x),k.ToMM(z.y)],'size_mm':[k.ToMM(sz.x),k.ToMM(sz.y)],'drill_mm':[k.ToMM(d.x),k.ToMM(d.y)],'net':p.GetNetname()})
 rows.append({'ref':f.GetReference(),'MPN':f.GetField('MPN').GetText()if f.GetField('MPN')else None,'value':f.GetValue(),'xy_mm':[k.ToMM(pos.x),k.ToMM(pos.y)],'orientation_deg':f.GetOrientationDegrees(),'side':'F'if f.GetLayer()==k.F_Cu else'B','pads':pads})
out={'source_board_sha256':sha(P/'SC09_compact.kicad_pcb'),'rows':rows,'native_copper_outline_mm':[99.4,99.4,150.6,132.4],'method':'Read-only pcbnew10.0.6; no SaveBoard'}
(H/'native-inventory.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:x[k]for k in ['ref','xy_mm','orientation_deg','side']}for x in rows]))
