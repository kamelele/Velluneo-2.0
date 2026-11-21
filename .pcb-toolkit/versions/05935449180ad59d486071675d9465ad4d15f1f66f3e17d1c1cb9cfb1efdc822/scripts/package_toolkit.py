"""Deterministic audit-free review candidates. No publication or license grant."""
import argparse
import hashlib
import io
import json
import os
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
import posixpath

MANIFEST='PACKAGE-MANIFEST.json'
RECIPE='distribution/package.json'
BLOCKED={'data','reports','.git','.work','.private','__pycache__'}
MAX_TOTAL=64*1024*1024


def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode()


def loads(data):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(data,object_pairs_hook=pairs)


def member(name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or '\0' in name:
        raise ValueError('Unsafe package path')
    parts=PurePosixPath(name).parts
    if name.startswith('/') or '/'.join(parts)!=name or any(p in ['.','..'] or p.endswith((' ','.')) for p in parts):
        raise ValueError('Noncanonical package path: '+name)
    if any(p.casefold() in BLOCKED for p in parts) or any(re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?',p) for p in parts):
        raise ValueError('Forbidden package path: '+name)
    if Path(name).suffix.lower() in ['.pcbdoc','.schdoc','.prjpcb','.rul','.pyc','.bak']:
        raise ValueError('Forbidden source/archive member: '+name)
    return name


def local(root,name):
    member(name);root=Path(root).absolute()
    current=root
    for part in [None,*PurePosixPath(name).parts]:
        if part is not None:current=current/part
        try:info=current.lstat()
        except FileNotFoundError:continue
        if stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)&0x400:
            raise ValueError('Symlink/reparse point refused: '+name)
    if not current.resolve().is_relative_to(root.resolve()):raise ValueError('Path escapes root')
    return current


def scan(files,deny_tokens=()):
    for name,data in files.items():
        try:text=data.decode('utf-8')
        except UnicodeDecodeError:raise ValueError('Only reviewed UTF-8 sources supported: '+name)
        if re.search(r'(?i)(https?://(?:drive[.]google[.]com|docs[.]google[.]com)/|chatgpt-library-file[:]|[A-Z]:[\\/]Users[\\/])',text):
            raise ValueError('Private link/local user path in '+name)
        if any(token and token.casefold() in text.casefold() for token in deny_tokens):
            raise ValueError('Private review token in '+name)
        if name.endswith('.json'):
            value=loads(text)
            def inspect(v):
                if isinstance(v,dict):
                    if {'reference_drive_id','reference_path','historical_constraints','source_id'}&v.keys():
                        raise ValueError('Audit metadata keys in '+name)
                    for child in v.values():inspect(child)
                elif isinstance(v,list):
                    for child in v:inspect(child)
            inspect(value)
    for name,data in files.items():
        if not name.endswith('.md'):continue
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',data.decode('utf-8')):
            parsed=urlsplit(target.strip('<>'))
            if parsed.scheme in ['https','http','mailto'] or not parsed.path:continue
            if parsed.scheme or target.startswith('//'):raise ValueError('Unsupported document link in '+name)
            resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(parsed.path)))
            if resolved not in files and not any(p.startswith(resolved.rstrip('/')+'/') for p in files):
                raise ValueError('Unresolved package link: '+name+' -> '+target)


def collect(root,recipe):
    if type(recipe.get('schema_version')) is not int or recipe['schema_version']!=1:raise ValueError('Unsupported recipe')
    if not re.fullmatch('[A-Za-z0-9][A-Za-z0-9_.-]*',recipe.get('package_version','')):raise ValueError('Invalid package version')
    if recipe.get('candidate_only') is not True:raise ValueError('Only review candidates implemented')
    if not isinstance(recipe.get('files'),list) or not recipe['files']:raise ValueError('Explicit reviewed file list required')
    files={};folded=set();public=[];ledger=[]
    for entry in recipe['files']:
        name=member(entry['path']);source=member(entry['source'])
        if name in [MANIFEST,RECIPE] or name.casefold() in folded:raise ValueError('Reserved/duplicate/case-colliding target: '+name)
        folded.add(name.casefold())
        if entry.get('review')!='prepared-for-owner-review' or entry.get('origin') not in ['original','variant']:
            raise ValueError('Missing content disposition: '+name)
        data=local(root,source).read_bytes()
        if sha(data)!=entry['sha256'] or sha(data)!=entry['export_sha256']:raise ValueError('Source/export hash changed: '+name)
        original=entry.get('original')
        if original and sha(local(root,original['path']).read_bytes())!=original['sha256']:
            raise ValueError('Variant basis changed: '+name)
        if len(data)>MAX_TOTAL:raise ValueError('Oversized source')
        files[name]=data
        public.append({'source':name,'path':name,'sha256':sha(data),'export_sha256':sha(data),
                       'origin':entry['origin'],'review':entry['review']})
        ledger.append({'path':name,'source':source,'source_sha256':sha(data),'original':original,'origin':entry['origin']})
    normalized={key:recipe[key] for key in ['schema_version','package_version','candidate_only','ruleset_version','scope','pending_acceptance']}
    normalized['files']=sorted(public,key=lambda e:e['path'])
    files[RECIPE]=encoded(normalized)
    if sum(map(len,files.values()))>MAX_TOTAL:raise ValueError('Candidate size limit exceeded')
    scan(files,recipe.get('private_review_tokens',[]))
    manifest={'schema_version':1,'package_version':recipe['package_version'],'ruleset_version':recipe['ruleset_version'],
              'candidate_only':True,'publication_ready':False,'pending_acceptance':recipe['pending_acceptance'],
              'scope':recipe['scope'],'files':{p:{'sha256':sha(v),'size':len(v)} for p,v in sorted(files.items())}}
    files[MANIFEST]=encoded(manifest)
    return files,{'schema_version':1,'candidate_only':True,'source_files':ledger,'export_manifest_sha256':sha(files[MANIFEST])}


def archive_bytes(files):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_STORED) as output:
        for name,data in sorted(files.items()):
            item=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));item.create_system=3
            item.external_attr=(stat.S_IFREG|0o644)<<16;item.compress_type=zipfile.ZIP_STORED
            output.writestr(item,data)
    return stream.getvalue()


def verify_manifest(files,deny_tokens=()):
    if MANIFEST not in files:raise ValueError('Manifest missing')
    manifest=loads(files[MANIFEST])
    if manifest.get('schema_version')!=1 or manifest.get('candidate_only') is not True or manifest.get('publication_ready') is not False:
        raise ValueError('Unsupported or falsely publishable candidate manifest')
    expected=manifest.get('files')
    if not isinstance(expected,dict) or set(expected)!=(set(files)-{MANIFEST}):raise ValueError('Unexpected or missing package members')
    for p,item in expected.items():
        member(p)
        if item.get('sha256')!=sha(files[p]) or item.get('size')!=len(files[p]):raise ValueError('Integrity failure: '+p)
    scan({p:v for p,v in files.items() if p!=MANIFEST},deny_tokens)
    return manifest


def verify_archive(path,expected_sha256=None):
    data=Path(path).read_bytes()
    if expected_sha256 and sha(data)!=expected_sha256:raise ValueError('Archive checksum differs')
    if len(data)>MAX_TOTAL*2:raise ValueError('Oversized archive')
    files={};folded=set();total=0
    with zipfile.ZipFile(io.BytesIO(data)) as source:
        for info in source.infolist():
            name=member(info.filename)
            if name.casefold() in folded or info.is_dir() or stat.S_ISLNK(info.external_attr>>16) or info.flag_bits&1:
                raise ValueError('Duplicate/directory/link/encrypted member')
            folded.add(name.casefold());total+=info.file_size
            if total>MAX_TOTAL:raise ValueError('Expanded archive too large')
            files[name]=source.read(info)
    return files,verify_manifest(files)


def verify_tree(root):
    root=Path(root);manifest=loads(local(root,MANIFEST).read_bytes());files={MANIFEST:local(root,MANIFEST).read_bytes()}
    for name in manifest.get('files',{}):files[name]=local(root,name).read_bytes()
    ignored={'.work','reports','__pycache__'}
    for directory,dirs,names in os.walk(root,followlinks=False):
        for name in list(dirs):
            p=Path(directory)/name
            if name in ignored:dirs.remove(name)
            elif p.is_symlink():raise ValueError('Unexpected extracted symlink')
        for name in names:
            if name in ignored:continue
            p=Path(directory)/name;rel=p.relative_to(root).as_posix()
            if rel not in files:raise ValueError('Unexpected extracted file: '+rel)
            if p.is_symlink():raise ValueError('Unexpected extracted symlink')
    return verify_manifest(files)


def extract(path,destination,expected_sha256=None):
    files,manifest=verify_archive(path,expected_sha256)
    destination=Path(destination).absolute()
    if destination.exists():raise ValueError('Extraction target must not exist')
    if destination.parent.resolve()!=destination.parent.absolute():raise ValueError('Unsafe extraction parent')
    destination.mkdir(parents=True)
    for name,data in files.items():
        p=local(destination,name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    return manifest


def build(root,recipe_path,output):
    root=Path(root).absolute();output=Path(output).absolute()
    companions=[output,output.with_suffix(output.suffix+'.sha256'),output.with_suffix(output.suffix+'.private-review.json')]
    if output.suffix!='.zip' or any(p.exists() or p.is_symlink() for p in companions):
        raise ValueError('Choose a fresh .zip output and companion paths')
    if output.parent.resolve()!=output.parent.absolute():raise ValueError('Unsafe output parent')
    recipe=loads(local(root,recipe_path).read_bytes());files,ledger=collect(root,recipe)
    data=archive_bytes(files);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(data)
    output.with_suffix(output.suffix+'.sha256').write_text(sha(data)+'  '+output.name+'\n',encoding='ascii')
    ledger['archive_sha256']=sha(data)
    output.with_suffix(output.suffix+'.private-review.json').write_bytes(encoded(ledger))
    return ledger


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('build-candidate');p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--recipe',default=RECIPE);p.add_argument('--output',type=Path,required=True)
    for command in ['verify','extract']:
        p=sub.add_parser(command);p.add_argument('archive',type=Path);p.add_argument('--sha256')
        if command=='extract':p.add_argument('destination',type=Path)
    p=sub.add_parser('verify-tree');p.add_argument('directory',type=Path)
    args=parser.parse_args()
    try:
        if args.command=='build-candidate':result=build(args.root,args.recipe,args.output)
        elif args.command=='verify':result=verify_archive(args.archive,args.sha256)[1]
        elif args.command=='extract':result=extract(args.archive,args.destination,args.sha256)
        else:result=verify_tree(args.directory)
        print(json.dumps({'passed':True,'candidate_only':True,'publication_ready':False,'manifest_or_archive_sha256':result.get('archive_sha256') or sha(encoded(result))}));return 0
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        print(json.dumps({'passed':False,'error':str(exc)}));return 2


if __name__=='__main__':raise SystemExit(main())
