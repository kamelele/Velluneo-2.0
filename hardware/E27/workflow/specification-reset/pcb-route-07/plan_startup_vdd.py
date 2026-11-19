"""Fresh full-outline fine-grid startup VDD distribution candidate."""
from pathlib import Path
import json
D=Path(__file__).resolve().parent
INPUT_FILE='current-input.json';GRID_STEP=.1
exec(compile((D/'plan_routes.py').read_text().split('groups=')[0],str(D/'plan_routes.py'),'exec'))
es,reason=plan('R17.2','R10.2',.3,'startup_VDD_escape')
(D/'startup-vdd-plan.json').write_text(json.dumps(dict(input_source_sha256=j['source_sha256'],grid_mm=GRID_STEP,new_elements=es,reason=reason),indent=2)+'\n')
print('STARTUP VDD',reason,None if es is None else len(es),flush=True)
