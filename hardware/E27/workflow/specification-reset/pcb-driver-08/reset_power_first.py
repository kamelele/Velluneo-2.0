"""Remove stale power/return geometry that conflicts with the selected positions."""
from pathlib import Path
import pcbnew,json,hashlib
D=Path(__file__).resolve().parent;E=D/'design';src=D/'.work/placed-ripped.kicad_pcb'
for ext in('.kicad_pro','.kicad_dru','.kicad_sch'):src.with_suffix(ext).write_bytes((E/('Velluneo_driver'+ext)).read_bytes())
b=pcbnew.LoadBoard(str(src));removed=[]
for t in list(b.GetTracks()):
 if t.GetNetname()in{'/DRAIN','/PRIMARY_GND','/VDD'}:removed.append(t.GetNetname());b.Remove(t)
out=D/'.work/power-first-ripped.kicad_pcb';pcbnew.SaveBoard(str(out),b)
(D/'power-first-reset.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),removed_objects=len(removed),reason='Moved R1 intersects old drain and bulk/aux-return geometry. Rebuild after reserving via-free driver/gate and short primary feeds; no clearance waiver.'),indent=2)+'\n');print('Reset olddrain/returns',len(removed))
