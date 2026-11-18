"""Archive the exact computed preview and envelope mesh; no network."""
from pathlib import Path
import hashlib,json,zipfile
D=Path(__file__).resolve().parent;rows=[]
with zipfile.ZipFile(D/'Velluneo_assembly_envelopes.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for n in('assembly-preview.svg','assembly-envelopes.obj'):
  b=(D/'.work/preview'/n).read_bytes();zi=zipfile.ZipInfo(n,(2026,11,18,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16;z.writestr(zi,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9);rows.append(dict(member=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
a=D/'Velluneo_assembly_envelopes.zip';o=dict(archive=a.name,archive_sha256=hashlib.sha256(a.read_bytes()).hexdigest(),scope='ActualcomputedSVG andnonmanufacturingOBJenvelopes; exactzippedmembersverified, rawrenderintermediatesignored.',members=rows)
(D/'artifact-members.json').write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8',newline='\n')
with zipfile.ZipFile(a)as z:
 assert set(z.namelist())=={p['member']for p in rows}
 for p in rows:assert hashlib.sha256(z.read(p['member'])).hexdigest()==p['sha256']
print(json.dumps({'verified_members':len(rows),'archive_bytes':a.stat().st_size,'archive_sha256':o['archive_sha256']}))
