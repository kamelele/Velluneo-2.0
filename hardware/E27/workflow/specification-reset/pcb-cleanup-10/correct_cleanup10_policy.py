from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-cleanup-10';E=D/'design';p=E/'Velluneo_driver.kicad_pro';j=json.loads(p.read_text());changes=[]
for key in('pth_inside_courtyard','npth_inside_courtyard'):
 before=j['board']['design_settings']['rule_severities'][key];j['board']['design_settings']['rule_severities'][key]='error';changes.append(dict(field=key,before=before,after='error'))
p.write_text(json.dumps(j,indent=2)+'\n');(D/'checks/policy-correction-CR10-01.json').write_text(json.dumps(dict(finding='CR10-01',initial_body='63e9b2e40bd07709184987067c94ced233a2d13c579776a69adbb6157f9a96b8',correction=changes,no_waiver=True,no_geometry_change=True,scope='Restore original strict severities. Retain resulting managed mismatch rather than weaken project policy.'),indent=2)+'\n')
