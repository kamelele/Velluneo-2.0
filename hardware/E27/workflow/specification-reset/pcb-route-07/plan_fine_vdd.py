"""Bounded fine-grid VDD candidate; unchanged physical board and clearance limits."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
INPUT_FILE='tail-input.json';GRID_STEP=.025;GRID_BOUNDS=[-8,18,8,30]
exec(compile((D/'plan_routes.py').read_text().split('groups=')[0],str(D/'plan_routes.py'),'exec'))
es,reason=plan('R13.1','C2.1',.3,'VDD_fine_escape')
(D/'fine-plan.json').write_text(json.dumps(dict(input_source_sha256=j['source_sha256'],grid_mm=GRID_STEP,grid_bounds_mm=GRID_BOUNDS,new_elements=es,reason=reason,scope='Fine-grid candidate only; actual native DRC and protected-return preservation required.'),indent=2)+'\n')
print('FINE',reason,None if es is None else len(es),flush=True)
