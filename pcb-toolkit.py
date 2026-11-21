"""Project launcher: verify the pinned tree before importing toolkit code."""
import hashlib,json,os,re,sys
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
try:
    lock=json.loads((ROOT/'.pcb-toolkit/lock.json').read_text(encoding='utf-8'))
    digest=lock['current']['manifest_sha256']
    if lock.get('schema_version')!=1 or not re.fullmatch('[0-9a-f]{64}',digest):raise ValueError('Invalid toolkit lock')
    vendor=ROOT/'.pcb-toolkit/versions'/digest
    def safe(path):
        for p in [path,*path.parents]:
            if p==ROOT:break
            if p.is_symlink() or (p.exists() and getattr(p.lstat(),'st_file_attributes',0)&0x400):raise ValueError('Linked dependency path')
        return path
    data=safe(vendor/'PACKAGE-MANIFEST.json').read_bytes()
    if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('Pinned manifest differs')
    manifest=json.loads(data)
    for name,item in manifest['files'].items():
        parts=PurePosixPath(name).parts
        if not parts or name.startswith('/') or '/'.join(parts)!=name or any(p in ['.','..'] for p in parts) or '\\' in name or ':' in name:raise ValueError('Unsafe manifest member')
        path=safe(vendor.joinpath(*parts))
        if not path.resolve().is_relative_to(vendor.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Pinned file differs: '+name)
    sys.path.insert(0,str(vendor/'scripts'))
    import toolkit_install
except (OSError,ValueError,KeyError,TypeError,ImportError) as exc:
    print(json.dumps({'passed':False,'configuration_error':True,'error':str(exc)}));raise SystemExit(2)
raise SystemExit(toolkit_install.project_main(ROOT,sys.argv[1:]))
