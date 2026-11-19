"""Read-only frozen member/hash validation; no product operation/compliance claim."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parents[4]
o=json.loads((D/'frozen-files.json').read_text())
assert hashlib.sha256(json.dumps(o['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==o['body_sha256']
for f in o['files']:
 b=(R/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
print(json.dumps({'verified_members':len(o['files']),'body_sha256':o['body_sha256'],'scope':'member byte consistency only; no functional or stage approval'}))
