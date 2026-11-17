"""Original fixture package variants; no real approvals or release identities."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import package_toolkit as package


def make(root,work,version,change=False):
    recipe=package.loads((root/package.RECIPE).read_bytes())
    files,_=package.collect(root,recipe)
    public=package.loads(files[package.RECIPE]);public['package_version']=version
    if change:files['README.md']+=b'\nSynthetic installation-update fixture only.\n'
    # A packaged example must not become a flat-layout board design input.
    files['examples/fictional.kicad_sch']=b'Synthetic dependency-discovery sentinel, not a circuit.\n'
    source=work/version;source.mkdir(parents=True)
    entries=[]
    for name,data in files.items():
        if name in [package.RECIPE,package.MANIFEST]:continue
        p=source/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        entries.append({'source':name,'path':name,'sha256':package.sha(data),'export_sha256':package.sha(data),
                        'origin':'original','review':'prepared-for-owner-review'})
    public['files']=entries
    actual,_=package.collect(source,public)
    archive=work/(version+'.zip');archive.write_bytes(package.archive_bytes(actual))
    return archive,package.sha(archive.read_bytes())
