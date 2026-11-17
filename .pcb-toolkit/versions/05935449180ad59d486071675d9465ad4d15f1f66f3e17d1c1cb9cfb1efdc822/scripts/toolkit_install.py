"""Offline content-pinned vendoring, project dispatch and deliberate updates."""
import argparse
import ast
from contextlib import contextmanager
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
import configuration as cfg
import package_toolkit as pkg

ROOT=Path(__file__).resolve().parents[1]
LOCK='.pcb-toolkit/lock.json'
BOOTSTRAP='''"""Project launcher: verify the pinned tree before importing toolkit code."""
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
        if not parts or name.startswith('/') or '/'.join(parts)!=name or any(p in ['.','..'] for p in parts) or '\\\\' in name or ':' in name:raise ValueError('Unsafe manifest member')
        path=safe(vendor.joinpath(*parts))
        if not path.resolve().is_relative_to(vendor.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Pinned file differs: '+name)
    sys.path.insert(0,str(vendor/'scripts'))
    import toolkit_install
except (OSError,ValueError,KeyError,TypeError,ImportError) as exc:
    print(json.dumps({'passed':False,'configuration_error':True,'error':str(exc)}));raise SystemExit(2)
raise SystemExit(toolkit_install.project_main(ROOT,sys.argv[1:]))
'''
IGNORE='versions/**/.work/\nversions/**/reports/\n**/__pycache__/\nuse.lock\n'


def write(root,relative,value):cfg.replace(root,relative,pkg.encoded(value))
def read(root,relative):return pkg.loads(cfg.path(root,relative).read_bytes())
def hash_lock(root):return pkg.sha(cfg.path(root,LOCK).read_bytes())


@contextmanager
def using(root):
    path=cfg.path(root,'.pcb-toolkit/use.lock');path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a+b') as stream:
        if stream.tell()==0:stream.write(b'0');stream.flush()
        stream.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as exc:raise ValueError('Another toolkit command/update is active') from exc
        try:yield
        finally:
            stream.seek(0)
            if os.name=='nt':msvcrt.locking(stream.fileno(),msvcrt.LK_UNLCK,1)
            else:fcntl.flock(stream.fileno(),fcntl.LOCK_UN)


def locate(project):
    project=Path(project).absolute()
    for parent in [project,*project.parents]:
        if (parent/'.pcb-toolkit').exists() or (parent/'.pcb-toolkit').is_symlink():return parent
    return None


def validate_lock(root,lock):
    if type(lock.get('schema_version')) is not int or lock['schema_version']!=1:raise ValueError('Unsupported installation lock')
    pin=lock['current']
    for key in ['manifest_sha256','archive_sha256']:
        if not re.fullmatch('[0-9a-f]{64}',pin.get(key,'')):raise ValueError('Invalid pin: '+key)
    folder=cfg.path(root,'.pcb-toolkit/versions/'+pin['manifest_sha256'])
    if pkg.sha((folder/pkg.MANIFEST).read_bytes())!=pin['manifest_sha256']:raise ValueError('Pinned manifest differs')
    manifest=pkg.verify_tree(folder)
    if any(pin.get(key)!=manifest.get(key) for key in ['package_version','ruleset_version']):raise ValueError('Lock version differs from manifest')
    if pin.get('kicad_version')!=manifest['scope']['kicad_version']:raise ValueError('KiCad pin differs')
    if (folder/'VERSION').read_text().strip()!=manifest['ruleset_version']:raise ValueError('Ruleset VERSION differs from manifest')
    if pin.get('candidate_accepted') is not True or pin.get('publication_ready') is not False:raise ValueError('Candidate acceptance/identity differs')
    if cfg.path(root,'pcb-toolkit.py').read_bytes()!=BOOTSTRAP.encode():raise ValueError('Project launcher differs from owned bootstrap')
    return lock,folder,manifest


def current(root):return validate_lock(root,read(root,LOCK))


def identity(project,ruleset_root):
    root=locate(project);ruleset_root=Path(ruleset_root).resolve()
    if root:
        lock,folder,manifest=current(root)
        if folder.resolve()!=ruleset_root:raise ValueError('Use the project pinned pcb-toolkit.py launcher')
        if os.environ.get('PCB_TOOLKIT_ACTIVE')!=lock['current']['manifest_sha256']:raise ValueError('Run installed tooling through pcb-toolkit.py')
        return {'kind':'installed','lock_sha256':hash_lock(root),**lock['current']}
    if (ruleset_root/pkg.MANIFEST).is_file():
        manifest=pkg.verify_tree(ruleset_root)
        return {'kind':'standalone-candidate','manifest_sha256':pkg.sha((ruleset_root/pkg.MANIFEST).read_bytes()),
                'package_version':manifest['package_version'],'ruleset_version':manifest['ruleset_version'],
                'publication_ready':manifest['publication_ready']}
    return {'kind':'private-source','ruleset_version':(ruleset_root/'VERSION').read_text().strip()}


def select(archive,checksum,allow_candidate):
    if not re.fullmatch('[0-9a-f]{64}',checksum):raise ValueError('Exact trusted archive SHA256 required')
    files,manifest=pkg.verify_archive(archive,checksum)
    required={'VERSION','scripts/toolkit_install.py','scripts/package_toolkit.py','scripts/configuration.py','scripts/pcb_rules.py'}
    protocol=manifest['scope'].get('installer_protocol')
    if not required.issubset(files) or type(protocol) is not int or protocol!=1:raise ValueError('Archive lacks supported installer protocol')
    if files['VERSION'].decode('utf-8').strip()!=manifest['ruleset_version']:raise ValueError('Ruleset VERSION differs from manifest')
    definitions=ast.parse(files['scripts/toolkit_install.py'].decode('utf-8'))
    literals=[ast.literal_eval(n.value) for n in definitions.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='BOOTSTRAP' for t in n.targets)]
    if literals!=[BOOTSTRAP]:raise ValueError('Installer bootstrap protocol differs; explicit migration required')
    if manifest['candidate_only'] and not allow_candidate:raise ValueError('Review candidate requires explicit --allow-candidate')
    return {'manifest_sha256':pkg.sha(files[pkg.MANIFEST]),'archive_sha256':checksum,
            'package_version':manifest['package_version'],'ruleset_version':manifest['ruleset_version'],
            'kicad_version':manifest['scope']['kicad_version'],'candidate_accepted':allow_candidate,
            'publication_ready':manifest['publication_ready']},manifest


def cache(root,archive,pin):
    target=cfg.path(root,'.pcb-toolkit/versions/'+pin['manifest_sha256'])
    if target.exists():
        if pkg.sha((target/pkg.MANIFEST).read_bytes())!=pin['manifest_sha256']:raise ValueError('Cached manifest changed')
        pkg.verify_tree(target);return
    stage=cfg.path(root,'.work/toolkit-install/'+uuid.uuid4().hex+'/contents')
    pkg.extract(archive,stage,pin['archive_sha256'])
    target.parent.mkdir(parents=True,exist_ok=True)
    # Both resolved endpoints must stay in the intended project-owned namespaces.
    if not stage.resolve().is_relative_to((Path(root)/'.work/toolkit-install').resolve()) or not target.resolve().is_relative_to((Path(root)/'.pcb-toolkit/versions').resolve()):raise ValueError('Unsafe staging move')
    os.replace(stage,target)


def install(root,archive,checksum,allow_candidate=False):
    root=Path(root).absolute();cfg.path(root,'.')
    if not root.is_dir():raise ValueError('Project repository must already exist')
    if (root/pkg.MANIFEST).exists():raise ValueError('Install into the project repository, not the toolkit package root')
    pin,_=select(archive,checksum,allow_candidate)
    owner=cfg.path(root,'.pcb-toolkit/owner.json')
    marker={'schema_version':1,'owner':'pcb-toolkit-installer-v1','bootstrap_sha256':pkg.sha(BOOTSTRAP.encode())}
    if (root/'.pcb-toolkit').exists() and not owner.is_file():raise ValueError('Existing .pcb-toolkit namespace is unowned')
    if owner.is_file() and read(root,'.pcb-toolkit/owner.json')!=marker:raise ValueError('Unknown installer ownership marker')
    wrapper=cfg.path(root,'pcb-toolkit.py')
    if wrapper.exists() and wrapper.read_bytes()!=BOOTSTRAP.encode():raise ValueError('Existing project launcher preserved')
    if (root/LOCK).exists():raise ValueError('Already installed; use plan-update/update')
    ignore=cfg.path(root,'.pcb-toolkit/.gitignore')
    if ignore.exists() and ignore.read_bytes()!=IGNORE.encode():raise ValueError('Existing installer ignore file preserved')
    write(root,'.pcb-toolkit/owner.json',marker)
    with using(root):
        if (root/LOCK).exists():raise ValueError('Installation activated concurrently')
        cache(root,archive,pin)
        cfg.replace(root,'pcb-toolkit.py',BOOTSTRAP.encode())
        cfg.replace(root,'.pcb-toolkit/.gitignore',IGNORE.encode())
        write(root,LOCK,{'schema_version':1,'current':pin,'previous_lock_sha256':None})
    return {'installed':pin,'checks_required':True}


def plan_update(root,archive,checksum,allow_candidate=False):
    lock,folder,old=current(root);pin,new=select(archive,checksum,allow_candidate)
    if pin['package_version']==lock['current']['package_version'] and pin!=lock['current']:raise ValueError('Version reuse with different identity refused')
    differences=[]
    for name in sorted(set(old['files'])|set(new['files'])):
        if old['files'].get(name)!=new['files'].get(name):differences.append({'path':name,'before':old['files'].get(name),'after':new['files'].get(name)})
    value={'schema_version':1,'lock_sha256':hash_lock(root),'before':lock['current'],'archive':str(Path(archive).resolve()),
           'pin':pin,'differences':differences,'no_op':pin==lock['current'],
           'impact':'All affected board snapshots/reviews need rechecking; CAD configuration is not migrated automatically.'}
    identifier=pkg.sha(pkg.encoded(value));write(root,'.work/toolkit-updates/'+identifier+'.json',value)
    return {'plan_id':identifier,**value}


def update(root,identifier):
    if not re.fullmatch('[0-9a-f]{64}',identifier):raise ValueError('Invalid update plan ID')
    plan=read(root,'.work/toolkit-updates/'+identifier+'.json')
    if pkg.sha(pkg.encoded(plan))!=identifier or hash_lock(root)!=plan['lock_sha256']:raise ValueError('Stale or modified update plan')
    old,_,_=current(root)
    if plan['before']!=old['current']:raise ValueError('Update baseline pin differs')
    pin,_=select(plan['archive'],plan['pin']['archive_sha256'],plan['pin']['candidate_accepted'])
    if pin!=plan['pin']:raise ValueError('Update archive identity changed')
    if plan['no_op']:
        if pin!=old['current']:raise ValueError('Invalid no-op plan')
        return {'changed':False,'current':pin}
    cache(root,plan['archive'],pin)
    before=cfg.path(root,LOCK).read_bytes();history=plan['lock_sha256']
    record=cfg.path(root,'.pcb-toolkit/history/'+history+'.json')
    if record.exists() and record.read_bytes()!=before:raise ValueError('History record differs')
    cfg.replace(root,'.pcb-toolkit/history/'+history+'.json',before)
    if hash_lock(root)!=history:raise ValueError('Lock changed before activation')
    write(root,LOCK,{'schema_version':1,'current':pin,'previous_lock_sha256':history})
    return {'changed':True,'current':pin,'rollback_to':history,'checks_required':True}


def rollback(root,identifier):
    if not re.fullmatch('[0-9a-f]{64}',identifier):raise ValueError('Invalid historical lock ID')
    current(root)
    data=cfg.path(root,'.pcb-toolkit/history/'+identifier+'.json').read_bytes()
    if pkg.sha(data)!=identifier:raise ValueError('Historical lock checksum differs')
    old=pkg.loads(data);pin=old['current']
    validate_lock(root,old)
    cfg.replace(root,LOCK,data)
    return {'restored':pin,'checks_required':True,'note':'CAD/configuration and human approvals are not changed.'}


def doctor(root,cli=None,cad_python=None):
    result={'passed':False,'configuration_error':True}
    try:
        lock,folder,_=current(root)
        result['pin']=lock['current']
        cli=cli or os.environ.get('KICAD_CLI') or shutil.which('kicad-cli')
        if not cli and os.name=='nt':cli='C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
        cad_python=cad_python or os.environ.get('KICAD_PYTHON') or ('C:/Program Files/KiCad/10.0/bin/python.exe' if os.name=='nt' else sys.executable)
        env=os.environ.copy();env.pop('PYTHONPATH',None)
        env['KICAD_CONFIG_HOME']=str(cfg.path(root,'.work/kicad-config'));env['KICAD_DOCUMENTS_HOME']=str(cfg.path(root,'.work/kicad-documents'))
        version=subprocess.run([cli,'version'],capture_output=True,text=True,env=env,timeout=30)
        cad=subprocess.run([cad_python,'-c','import pcbnew,json,sys; print(json.dumps({"pcbnew":pcbnew.Version(),"python":sys.version}))'],capture_output=True,text=True,env=env,timeout=30)
        if version.returncode or cad.returncode:raise ValueError('CLI or pcbnew failed: '+version.stderr+cad.stderr)
        actual=pkg.loads(cad.stdout)
        if version.stdout.strip()!=lock['current']['kicad_version'] or actual['pcbnew'] not in [lock['current']['kicad_version'],lock['current']['kicad_version']+'+dfsg-1']:raise ValueError('Exact pinned CLI/pcbnew version differs')
        supported=os.name=='nt' or (sys.platform=='linux' and platform.freedesktop_os_release().get('ID')=='ubuntu' and platform.freedesktop_os_release().get('VERSION_ID')=='26.10')
        if sys.version_info<(3,11) or platform.machine().lower() not in ['amd64','x86_64'] or not supported:raise ValueError('Environment outside validated Python/platform scope')
        result={'passed':True,'configuration_error':False,'pin':lock['current'],'python':sys.version,
                'cad_runtime':actual,'kicad_cli_version':version.stdout.strip(),'platform':platform.platform(),
                'config_directories':{k:env[k] for k in ['KICAD_CONFIG_HOME','KICAD_DOCUMENTS_HOME']}}
    except (ValueError,OSError,KeyError,TypeError,subprocess.TimeoutExpired) as exc:result['error']=str(exc)
    write(root,'.work/toolkit-doctor.json',result);return result


def launch(root,arguments):
    lock,folder,_=current(root)
    if not arguments or arguments[0] not in ['init','configure','snapshot','check','requirements','connectivity','spatial'] or len(arguments)<2:raise ValueError('run requires a supported command and project path')
    board=cfg.path(root,arguments[1])
    relative=board.relative_to(Path(root).resolve())
    if relative.parts and relative.parts[0].casefold()=='.pcb-toolkit':raise ValueError('Dependency store cannot contain design project inputs')
    env=os.environ.copy();env.pop('PYTHONPATH',None);env['PCB_TOOLKIT_ACTIVE']=lock['current']['manifest_sha256']
    command=[sys.executable,str(folder/'scripts/pcb_rules.py'),arguments[0],str(board),*arguments[2:]]
    report={'pin':lock['current'],'command':arguments,'status':'running'};write(root,'.work/toolkit-run.json',report)
    try:code=subprocess.run(command,cwd=root,env=env).returncode
    except OSError as exc:report['error']=str(exc);code=2
    report.update(exit_code=code,status={0:'passed',1:'findings-or-incomplete',2:'configuration-or-tool-failure'}.get(code,'tool-failure'))
    write(root,'.work/toolkit-run.json',report);return code


def project_main(root,arguments):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('status')
    p=sub.add_parser('doctor');p.add_argument('--kicad-cli');p.add_argument('--cad-python')
    p=sub.add_parser('plan-update');p.add_argument('archive',type=Path);p.add_argument('--sha256',required=True);p.add_argument('--allow-candidate',action='store_true')
    p=sub.add_parser('update');p.add_argument('--apply',required=True)
    p=sub.add_parser('rollback');p.add_argument('--to',required=True)
    p=sub.add_parser('run');p.add_argument('arguments',nargs=argparse.REMAINDER)
    args=parser.parse_args(arguments)
    try:
        with using(root):
            lock,folder,_=current(root)
            if folder.resolve()!=ROOT.resolve():raise ValueError('Selected dependency changed before launch; rerun the project launcher')
            if args.command=='run':return launch(root,args.arguments)
            if args.command=='status':value={'pin':lock['current'],'lock_sha256':hash_lock(root),'previous_lock_sha256':lock['previous_lock_sha256']}
            elif args.command=='doctor':
                value=doctor(root,args.kicad_cli,args.cad_python)
                print(json.dumps(value,ensure_ascii=True,indent=2));return 0 if value['passed'] else 2
            elif args.command=='plan-update':value=plan_update(root,args.archive,args.sha256,args.allow_candidate)
            elif args.command=='update':value=update(root,args.apply)
            else:value=rollback(root,args.to)
        print(json.dumps(value,ensure_ascii=True,indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'passed':False,'configuration_error':True,'error':str(exc)}));return 2


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['install']);parser.add_argument('project_repository',type=Path)
    parser.add_argument('--archive',type=Path,required=True);parser.add_argument('--sha256',required=True);parser.add_argument('--allow-candidate',action='store_true');args=parser.parse_args()
    try:
        if (ROOT/pkg.MANIFEST).is_file():pkg.verify_tree(ROOT)
        print(json.dumps(install(args.project_repository,args.archive,args.sha256,args.allow_candidate),indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(json.dumps({'passed':False,'configuration_error':True,'error':str(exc)}));return 2


if __name__=='__main__':raise SystemExit(main())
