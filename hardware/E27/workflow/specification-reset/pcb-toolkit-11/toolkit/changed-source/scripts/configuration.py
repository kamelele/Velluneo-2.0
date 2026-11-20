"""Preview-first configuration ownership and recoverable local transactions.

Standard library only. Project sources are never written by preview(). Ownership
records are provenance, not authorization or a substitute for policy validation.
"""
import base64
import copy
import difflib
import hashlib
import json
import os
import re
import stat
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

STATE = '.electronics-rules/config-state.json'
WORK = '.work/configure'


def design_files(root,suffixes):
    """Tool dependencies and generated work are not board design inputs."""
    root=Path(root).absolute()
    for directory,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=[d for d in dirs if d.casefold() not in {'.work','.git','__pycache__'}
                 and not (Path(directory)==root and d.casefold()=='.pcb-toolkit')]
        for name in files:
            p=Path(directory)/name
            if p.suffix in suffixes:yield p


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def path(root, relative):
    root = Path(root).absolute()
    candidate = root / relative
    if Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('Unsafe project path: '+str(relative))
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path outside project: '+str(relative))
    for item in [root, *candidate.relative_to(root).parents, candidate]:
        item = item if item.is_absolute() else root/item
        if item.exists() or item.is_symlink():
            attributes = getattr(item.lstat(), 'st_file_attributes', 0)
            if item.is_symlink() or attributes & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 1024):
                raise ValueError('Links/reparse points are unsupported: '+str(item))
    return candidate


def raw(root, relative):
    p = path(root, relative)
    return p.read_bytes() if p.exists() else None


def fingerprint(root, relative):
    data = raw(root, relative)
    return sha(data) if data is not None else None


def load(root, relative):
    data = raw(root, relative)
    return json.loads(data.decode('utf-8-sig')) if data is not None else None


def fields(project):
    """Only these leaves are managed; empty template collections are not policy."""
    result = {}
    for section in [('board','design_settings','rules'),
                    ('board','design_settings','rule_severities'), ('erc','rule_severities')]:
        node = project
        for key in section:
            node = node[key]
        for key, value in node.items():
            result['/'.join((*section,key))] = value
    result['erc/pin_map'] = project['erc']['pin_map']
    for cls in project['net_settings']['classes']:
        for key in ['clearance', 'track_width']:
            result['net_settings/classes/@'+cls['name']+'/'+key] = cls[key]
    result['net_settings/netclass_patterns'] = project['net_settings']['netclass_patterns']
    return result


MISSING = object()


def get(project, key):
    node = project
    for part in key.split('/'):
        if node is MISSING:
            return MISSING
        if part.startswith('@'):
            if not isinstance(node, list):
                raise ValueError('Expected netclass list: '+key)
            found = [x for x in node if x.get('name') == part[1:]]
            if len(found) > 1:
                raise ValueError('Duplicate netclass: '+part[1:])
            node = found[0] if found else MISSING
        else:
            if node is MISSING:
                return MISSING
            if not isinstance(node, dict):
                raise ValueError('Unknown configuration structure: '+key)
            node = node.get(part, MISSING)
    return node


def put(project, key, value):
    parts = key.split('/')
    node = project
    for part in parts[:-1]:
        if part.startswith('@'):
            node = next(x for x in node if x['name'] == part[1:])
        else:
            node = node.setdefault(part, {})
    node[parts[-1]] = copy.deepcopy(value)


def validate_structure(project):
    classes = get(project, 'net_settings/classes')
    if classes is not MISSING:
        if not isinstance(classes, list) or any(not isinstance(x, dict) or not isinstance(x.get('name'),str) for x in classes):
            raise ValueError('Invalid netclass list')
        names = [x['name'] for x in classes]
        if len(names) != len(set(names)):
            raise ValueError('Duplicate netclass names')


def policy_errors(actual, desired):
    validate_structure(actual)
    errors = []
    for key, wanted in fields(desired).items():
        if get(actual,key) != wanted:
            errors.append('Managed configuration differs: '+key)
    for key in ['board/design_settings/drc_exclusions', 'erc/erc_exclusions']:
        existing = get(actual,key)
        if existing is not MISSING and existing:
            errors.append('Existing exclusions require explicit review: '+key)
    classes = get(actual,'net_settings/classes')
    if classes is not MISSING:
        floor = desired['net_settings']['classes'][0]
        for cls in classes:
            for key in ['clearance','track_width']:
                value = cls.get(key)
                if not isinstance(value,(int,float)) or isinstance(value,bool) or not value >= floor[key]:
                    errors.append('Additional netclass is incompatible: '+cls['name']+'/'+key)
    return errors


def legacy_dru(project):
    names = [('clearance','min_clearance'),('track_width','min_track_width'),
             ('hole_size','min_through_hole_diameter'),('annular_width','min_via_annular_width'),
             ('edge_clearance','min_copper_edge_clearance')]
    try:
        rules = project['board']['design_settings']['rules']
        values = [rules[key] for _,key in names]
        if any(not isinstance(v,(int,float)) or isinstance(v,bool) or not 0 <= v < 100000 for v in values):
            return None
        return ('(version 1)\n'+''.join(f'(rule "HW-{name}" (constraint {name} (min {v:.6f}mm)))\n'
                for (name,_),v in zip(names,values))).encode()
    except (KeyError,TypeError):
        return None


def build(root, config, desired, custom, dependencies, extra_outputs=None, extra_conflicts=None):
    root = Path(root).absolute()
    if not root.is_dir():
        raise ValueError('Project directory does not exist')
    name = config['name']
    if not re.fullmatch(r'[A-Za-z0-9_-]+',name):
        raise ValueError('Invalid project name')
    pro_name, dru_name = name+'.kicad_pro', name+'.kicad_dru'
    original = load(root,pro_name)
    if original is not None and not isinstance(original,dict):
        raise ValueError('Project settings must be an object')
    actual = copy.deepcopy(original if original is not None else desired)
    validate_structure(actual)
    state = load(root,STATE)
    if state is not None and (not isinstance(state,dict) or state.get('schema_version') != 1 or not isinstance(state.get('managed'),dict)):
        raise ValueError('Unsupported ownership state')
    previous = state['managed'] if state else {}
    wanted = fields(desired)
    conflicts, changes = [], []
    for key in previous.keys()-wanted.keys():
        conflicts.append('Removal of an owned field needs manual migration: '+key)
    # Add complete defaults only for genuinely absent classes, preserving all
    # attributes of existing classes. Managed leaves are checked below.
    for cls in desired['net_settings']['classes']:
        if get(actual,'net_settings/classes/@'+cls['name']) is MISSING:
            ns = actual.setdefault('net_settings',{})
            ns.setdefault('classes',[]).append(copy.deepcopy(cls))
    for key,value in wanted.items():
        current = get(original or {},key)
        old = previous.get(key,MISSING)
        if current == value:
            changes.append({'field':key,'action':'preserve'})
        elif current is MISSING and old is MISSING:
            put(actual,key,value)
            changes.append({'field':key,'action':'add','after':value})
        elif old is not MISSING and current == old:
            put(actual,key,value)
            changes.append({'field':key,'action':'update','before':current,'after':value})
        else:
            conflicts.append('Resolve existing managed value: '+key)
    # Arrays with precedence are never merged by guessing.
    for error in policy_errors(actual,desired):
        if error not in conflicts:
            conflicts.append(error)
    existing = raw(root,dru_name)
    expected_dru = custom.encode()
    legacy = legacy_dru(original or {})
    supported = existing in [None,b'',expected_dru,expected_dru.replace(b'\n',b'\r\n'),
                             legacy,legacy.replace(b'\n',b'\r\n') if legacy else None]
    if state and existing is not None and sha(existing) == state.get('dru_sha256'):
        supported = True
    migration_proof = None
    if config.get('product',{}).get('scoped_clearances') or (existing and b'HW-SCOPED-'in existing):
        import scoped_policy
        try:
            scoped_policy.ensure_native_not_weaker(original or actual,actual)
        except ValueError as exc:
            conflicts.append(str(exc))
        if existing not in [None,b'',expected_dru,expected_dru.replace(b'\n',b'\r\n')]:
            # Ownership hashes permit exact no-ops, never weakened scoped policy.
            supported = False
    if not supported and config.get('configuration_migration'):
        import scoped_policy
        try:
            migration_proof = scoped_policy.review_legacy(root,config,actual,custom)
            supported = True
        except (ValueError,KeyError,TypeError,IndexError) as exc:
            conflicts.append('Legacy scoped migration refused: '+str(exc))
    if not supported:
        conflicts.append('Unfamiliar custom rules preserved; automatic adoption refused: '+dru_name)
    next_state = {'schema_version':1, 'ruleset_version':dependencies['version'],
                  'managed':wanted, 'dru_sha256':sha(expected_dru)}
    output = {pro_name:encoded(actual),dru_name:expected_dru,STATE:encoded(next_state)}
    if migration_proof is not None:
        output['.electronics-rules/migration-proof.json'] = encoded(migration_proof)
    output.update(extra_outputs or {})
    conflicts.extend(extra_conflicts or [])
    # Preserve exact bytes for semantic no-ops, including KiCad formatting.
    if original == actual:
        output[pro_name] = raw(root,pro_name)
    inputs = {pro_name,dru_name,STATE,'hardware.json',*config.get('source_files',[])}
    # Contract evidence/inputs are source inputs too, including before CAD exists.
    import product_contracts
    inputs.update(p.relative_to(root.resolve()).as_posix() for p in product_contracts.tracked_inputs(root,config))
    import connectivity
    inputs.update(p.relative_to(root.resolve()).as_posix() for p in connectivity.tracked_inputs(root,config))
    import spatial
    inputs.update(p.relative_to(root.resolve()).as_posix() for p in spatial.tracked_inputs(root,config))
    for p in design_files(root,['.kicad_sch','.kicad_pcb','.kicad_sym','.kicad_mod']):
        rel = p.relative_to(root).as_posix()
        if '.work' not in p.relative_to(root).parts and p.suffix in ['.kicad_sch','.kicad_pcb','.kicad_sym','.kicad_mod']:
            inputs.add(rel)
    if config.get('configuration_migration'):
        inputs.add(config['configuration_migration'])
    files = {rel:fingerprint(root,rel) for rel in sorted(inputs)}
    outputs = {k:base64.b64encode(v).decode() for k,v in output.items()}
    result = {'schema_version':1,'config':config,'dependencies':dependencies,'inputs':files,
              'outputs':outputs,'changes':changes,'conflicts':conflicts}
    result['id'] = sha(encoded(result))
    return result


def preview(root, plan):
    directory = path(root,WORK+'/plans')
    directory.mkdir(parents=True,exist_ok=True)
    target = path(root,WORK+'/plans/'+plan['id']+'.json')
    target.write_bytes(encoded(plan))
    diffs = []
    for rel,data in plan['outputs'].items():
        before = (raw(root,rel) or b'').decode('utf-8-sig')
        after = base64.b64decode(data).decode('utf-8')
        diffs.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
                                        fromfile=rel+' (current)',tofile=rel+' (proposed)'))
    path(root,WORK+'/plans/'+plan['id']+'.diff').write_text(''.join(diffs),encoding='utf-8')
    return plan


@contextmanager
def locked(root):
    p = path(root,WORK+'/lock')
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a+b') as stream:
        if stream.tell() == 0:
            stream.write(b'0'); stream.flush()
        stream.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError('Another configuration operation is running') from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(),msvcrt.LK_UNLCK,1)
            else:
                fcntl.flock(stream.fileno(),fcntl.LOCK_UN)


def replace(root, relative, data):
    target = path(root,relative)
    target.parent.mkdir(parents=True,exist_ok=True)
    temporary = target.with_name(target.name+'.rules-'+uuid.uuid4().hex+'.tmp')
    try:
        with temporary.open('xb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        # Windows sync/indexing tools can briefly hold the destination open.
        # Retain the staged bytes and retry only recognized sharing/access errors.
        for attempt in range(6):
            try:
                os.replace(temporary,target)
                break
            except PermissionError as exc:
                if os.name!='nt' or getattr(exc,'winerror',None) not in [5,32,33] or attempt==5:
                    raise
                time.sleep(0.05*(2**attempt))
    finally:
        temporary.unlink(missing_ok=True)


def journal(root, transaction, record):
    replace(root,WORK+'/transactions/'+transaction+'/journal.json',encoded(record))


def pending(root):
    directory = path(root,WORK+'/transactions')
    if not directory.exists():
        return []
    return [p.parent.name for p in directory.glob('*/journal.json')
            if load(root,p.relative_to(root).as_posix())['status'] in ['prepared','applying','rolling_back','recovery_required']]


def valid_id(value):
    if not re.fullmatch('[a-f0-9]{64}',value):
        raise ValueError('Invalid plan/transaction identifier')


def apply(root, plan, selected):
    valid_id(selected)
    with locked(root):
        if pending(root):
            raise ValueError('Unfinished transaction: use --rollback to recover '+', '.join(pending(root)))
        saved = load(root,WORK+'/plans/'+selected+'.json')
        if saved != plan or plan['id'] != selected:
            raise ValueError('Plan is stale or modified; generate a new preview')
        if plan['conflicts']:
            raise ValueError('Unresolved configuration conflicts')
        for rel,expected in plan['inputs'].items():
            if fingerprint(root,rel) != expected:
                raise ValueError('Input changed: '+rel)
        outputs = {k:base64.b64decode(v,validate=True) for k,v in plan['outputs'].items()}
        changed = {k:v for k,v in outputs.items() if raw(root,k) != v}
        if not changed:
            return None
        transaction = sha((selected+uuid.uuid4().hex).encode())
        directory = WORK+'/transactions/'+transaction
        record = {'schema_version':1,'status':'prepared','plan_id':selected,'files':{}}
        for index,(rel,data) in enumerate(changed.items()):
            before = raw(root,rel)
            backup = directory+'/'+str(index)+'.bak'
            if before is not None:
                replace(root,backup,before)
                if raw(root,backup) != before:
                    raise ValueError('Backup verification failed')
            record['files'][rel] = {'before':sha(before) if before is not None else None,
                                    'after':sha(data),'backup':backup}
        journal(root,transaction,record)
        try:
            for rel,expected in plan['inputs'].items():
                if fingerprint(root,rel) != expected:
                    raise ValueError('Input changed before write: '+rel)
            record['status']='applying'; journal(root,transaction,record)
            for rel,data in changed.items():
                replace(root,rel,data)
            record['status']='applied'; journal(root,transaction,record)
        except Exception:
            # Recovery validates every file before touching any of them.
            restore(root,transaction,record,recovery=True)
            raise
        return transaction


def restore(root, transaction, record, recovery=False):
    originals = {}
    for rel,item in record['files'].items():
        current = fingerprint(root,rel)
        allowed = [item['before'],item['after']] if recovery or record['status']=='rolling_back' else [item['after']]
        if current not in allowed:
            raise ValueError('Rollback refuses intervening edits: '+rel)
        data = raw(root,item['backup']) if item['before'] is not None else None
        if (sha(data) if data is not None else None) != item['before']:
            raise ValueError('Backup missing or corrupt: '+rel)
        originals[rel] = data
    record['status']='rolling_back'; journal(root,transaction,record)
    for rel,data in originals.items():
        if data is None:
            path(root,rel).unlink(missing_ok=True)
        else:
            replace(root,rel,data)
    record['status']='rolled_back'; journal(root,transaction,record)


def rollback(root, transaction):
    valid_id(transaction)
    with locked(root):
        record = load(root,WORK+'/transactions/'+transaction+'/journal.json')
        if not record or record.get('schema_version') != 1:
            raise ValueError('Unknown transaction')
        if record['status']=='rolled_back':
            return
        if record['status'] not in ['applied','prepared','applying','rolling_back','recovery_required']:
            raise ValueError('Unsupported transaction status')
        restore(root,transaction,record,recovery=record['status']!='applied')
