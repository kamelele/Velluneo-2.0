"""Fresh native import base without duplicate old copper; original sources untouched."""
from pathlib import Path
import pcbnew
D=Path(__file__).resolve().parent;F=D/'routing/.work';F.mkdir(parents=True,exist_ok=True);b=pcbnew.LoadBoard(str(D/'studies/sense/ground-seed.kicad_pcb'))
for t in list(b.GetTracks()):b.Remove(t)
pcbnew.SaveBoard(str(F/'import-base.kicad_pcb'),b)
print('native import base saved')
