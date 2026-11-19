"""Native negative control for shape-aware diagonal round-land clearance; no product edit."""
from pathlib import Path
import pcbnew,json,hashlib
D=Path(__file__).resolve().parent;T=D.parent/'.work/circle-negative';T.mkdir(parents=True,exist_ok=True);B='ECO04_land_geometry'
board=pcbnew.LoadBoard(str(D/(B+'.kicad_pcb')));q=next(f for f in board.GetFootprints()if f.GetReference()=='Q1');pad=next(p for p in q.Pads()if p.GetNumber()=='2');p=pad.GetPosition();assert abs(pcbnew.ToMM(p.y)-25.08)<1e-6
pad.SetPosition(pcbnew.VECTOR2I(p.x,pcbnew.FromMM(24.2)));assert pcbnew.SaveBoard(str(T/(B+'.kicad_pcb')),board)
for suffix in('.kicad_pro','.kicad_dru'):(T/(B+suffix)).write_bytes((D/(B+suffix)).read_bytes())
(T/'fp-lib-table').write_text((D/'fp-lib-table').read_text(encoding='utf-8').replace('${KIPRJMOD}',D.as_posix()),encoding='utf-8',newline='\n')
print(json.dumps(dict(negative_board=str(T/(B+'.kicad_pcb')),positive_board_sha256=hashlib.sha256((D/(B+'.kicad_pcb')).read_bytes()).hexdigest(),negative_board_sha256=hashlib.sha256((T/(B+'.kicad_pcb')).read_bytes()).hexdigest(),rules_byte_identical=(T/(B+'.kicad_dru')).read_bytes()==(D/(B+'.kicad_dru')).read_bytes())))
