from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';p=S/'requirements.json';d=json.loads(p.read_text())
for e in d['evidence']:
 if e['id'] in ['EV-EFFICIENCY-02','EV-PROTECTION-CALC-02']:
  e['inputs']=[{'path':name,'sha256':hashlib.sha256((S/name).read_bytes()).hexdigest()} for name in ['calculated-proposal.json','bom-build.json','owner-size-50x32-approval.json']]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Calculation evidence now explicitly binds the actual implementation inputs')
