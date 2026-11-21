"""Bounded exact-net clearance composition and independently checked legacy migration.
Candidate extension; no stage, process or supplier approval is conferred.
"""
import hashlib
import itertools
import json
import math
import re
from pathlib import Path
import configuration as cfg

RANK = {'ignore': 0, 'warning': 1, 'error': 2}
SAFE_NET = re.compile(r'[A-Za-z0-9_/+().:\-]+')
SAFE_ID = re.compile(r'[A-Za-z][A-Za-z0-9_\-]*')
COPPER_LAYERS = ['F.Cu'] + ['In%d.Cu' % i for i in range(1, 31)] + ['B.Cu']

def number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and 0 <= v < 100000

def strict_json(text):
    def object_pairs(items):
        value={}
        for key,item in items:
            if key in value:raise ValueError('Duplicate JSON key in migration input: '+key)
            value[key]=item
        return value
    return json.loads(text,object_pairs_hook=object_pairs)

def net(v):
    if not isinstance(v, str) or not SAFE_NET.fullmatch(v) or len(v) > 255:
        raise ValueError('Scoped policy requires a safe exact net name')
    return v

def pairs(config):
    result = config.get('product', {}).get('scoped_clearances', [])
    if not isinstance(result, list):
        raise ValueError('scoped_clearances must be a list')
    ids = set()
    for item in result:
        if not isinstance(item, dict) or set(item) != {'id', 'nets_a', 'nets_b', 'min_mm'}:
            raise ValueError('Scoped clearance needs exactly id/nets_a/nets_b/min_mm')
        if not isinstance(item['id'], str) or not SAFE_ID.fullmatch(item['id']) or item['id'] in ids:
            raise ValueError('Invalid or duplicate scoped clearance ID')
        ids.add(item['id'])
        for side in ['nets_a', 'nets_b']:
            values = item[side]
            if not isinstance(values, list) or not values:
                raise ValueError('Scoped clearance requires nonempty unique net lists')
            for name in values:
                net(name)
            if len(values) != len(set(values)):
                raise ValueError('Scoped clearance requires unique net lists')
        if set(item['nets_a']) & set(item['nets_b']):
            raise ValueError('Scoped clearance sides must be disjoint')
        if not number(item['min_mm']) or item['min_mm'] <= 0:
            raise ValueError('Invalid scoped clearance minimum')
    return sorted(result, key=lambda x: (x['min_mm'], x['id']))

def rules(config):
    output = ''
    for item in pairs(config):
        a = '(' + ' || '.join("A.NetName == '%s'" % n for n in item['nets_a']) + ')'
        b = '(' + ' || '.join("B.NetName == '%s'" % n for n in item['nets_b']) + ')'
        c = '(' + ' || '.join("A.NetName == '%s'" % n for n in item['nets_b']) + ')'
        d = '(' + ' || '.join("B.NetName == '%s'" % n for n in item['nets_a']) + ')'
        output += '(rule "HW-SCOPED-%s" (condition "(%s && %s) || (%s && %s)") (constraint clearance (min %.6fmm)))\n' % (item['id'], a, b, c, d, item['min_mm'])
    return output

def apply_to_expected(project, config):
    overrides = config.get('severity_overrides', {})
    if not isinstance(overrides, dict) or set(overrides) - {'board', 'erc'}:
        raise ValueError('severity_overrides supports board/erc only')
    for section, fields in overrides.items():
        target = project['board']['design_settings']['rule_severities'] if section == 'board' else project['erc']['rule_severities']
        if not isinstance(fields, dict):
            raise ValueError('Severity overrides must be objects')
        for key, value in fields.items():
            if key not in target or value not in {'warning', 'error'} or RANK[value] < RANK[target[key]]:
                raise ValueError('Unknown or weakening severity override: ' + str(key))
            target[key] = value
    return project

def sexprs(text):
    # Complete scanner: comments and quoted property values cannot inject fake net records.
    rx = re.compile(r'\s+|[;#][^\r\n]*|\(|\)|"(?:\\.|[^"\\])*"|[^\s()";#]+')
    roots, stack = [], []
    pos = 0
    for m in rx.finditer(text.lstrip('\ufeff')):
        if m.start() != pos:
            raise ValueError('Unsupported S-expression syntax')
        pos = m.end()
        token = m.group()
        if token.isspace() or token.startswith((';', '#')):
            continue
        if token == '(':
            item = []
            (stack[-1] if stack else roots).append(item)
            stack.append(item)
        elif token == ')':
            if not stack:
                raise ValueError('Unbalanced S-expression')
            stack.pop()
        else:
            if not stack:
                raise ValueError('Atom outside S-expression')
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    if stack or pos != len(text.lstrip('\ufeff')):
        raise ValueError('Incomplete S-expression')
    return roots

def board_nets(path):
    result = set()
    def walk(v):
        if not isinstance(v, list):
            return
        if v and v[0] == 'net' and len(v) in [2, 3] and isinstance(v[-1], str):
            if v[-1]:
                result.add(net(v[-1]))
        for x in v:
            if isinstance(x, list):
                walk(x)
    for root in sexprs(Path(path).read_text(encoding='utf-8-sig')):
        walk(root)
    return result

def condition(text):
    rx = re.compile(r"\s+|&&|\|\||==|\(|\)|[AB]\.NetName|'[^'\\\r\n]*'")
    tokens, pos, literals = [], 0, set()
    for m in rx.finditer(text):
        if m.start() != pos:
            raise ValueError('Unsupported legacy condition syntax')
        pos = m.end()
        if not m.group().isspace():
            tokens.append(m.group())
    if pos != len(text):
        raise ValueError('Unsupported legacy condition tail')
    i = 0
    def atom():
        nonlocal i
        if i >= len(tokens):
            raise ValueError('Incomplete legacy condition')
        t = tokens[i]; i += 1
        if t == '(':
            value = disjunction()
            if i >= len(tokens) or tokens[i] != ')':
                raise ValueError('Unbalanced legacy condition')
            i += 1
            return value
        if t not in ['A.NetName', 'B.NetName'] or i + 1 >= len(tokens) or tokens[i] != '==' or not tokens[i+1].startswith("'"):
            raise ValueError('Only exact A/B.NetName equality is migratable')
        name = net(tokens[i+1][1:-1]); literals.add(name); i += 2
        return ('eq', t[0], name)
    def conjunction():
        nonlocal i
        value = atom()
        while i < len(tokens) and tokens[i] == '&&':
            i += 1; value = ('and', value, atom())
        return value
    def disjunction():
        nonlocal i
        value = conjunction()
        while i < len(tokens) and tokens[i] == '||':
            i += 1; value = ('or', value, conjunction())
        return value
    ast = disjunction()
    if i != len(tokens):
        raise ValueError('Unexpected legacy condition token')
    return ast, literals

def matches(ast, a, b):
    if ast is None:
        return True
    if ast[0] == 'eq':
        return (a if ast[1] == 'A' else b) == ast[2]
    x, y = matches(ast[1], a, b), matches(ast[2], a, b)
    return x and y if ast[0] == 'and' else x or y

def legacy_rules(text):
    roots = sexprs(text)
    if not roots or roots[0] != ['version', '1']:
        raise ValueError('Legacy rules must begin with version 1')
    result, ids, all_nets = [], set(), set()
    for row in roots[1:]:
        if not isinstance(row, list) or len(row) not in [3, 4] or row[0] != 'rule' or not isinstance(row[1], str) or row[1] in ids:
            raise ValueError('Unsupported/duplicate legacy rule')
        ids.add(row[1]); ast = None; value = None; seen = set()
        for entry in row[2:]:
            if not isinstance(entry, list) or not entry or entry[0] in seen:
                raise ValueError('Unsupported legacy rule entry')
            seen.add(entry[0])
            if entry[0] == 'condition' and len(entry) == 2 and isinstance(entry[1], str):
                ast, names = condition(entry[1]); all_nets.update(names)
            elif entry[0] == 'constraint' and len(entry) == 3 and entry[1] == 'clearance':
                minimum = entry[2]
                if not isinstance(minimum, list) or not minimum or minimum[0] != 'min':
                    raise ValueError('Only minimum clearance constraints are migratable')
                raw = ''.join(minimum[1:])
                m = re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)mm', raw)
                if not m:
                    raise ValueError('Explicit finite millimetre minimum required')
                value = float(m[1])
                if not number(value):
                    raise ValueError('Invalid legacy minimum')
            else:
                raise ValueError('Unknown legacy object/layer/scope/constraint; manual migration required')
        if value is None:
            raise ValueError('Legacy rule lacks clearance minimum')
        result.append((ast, value))
    return result, all_nets

def class_value(project, name, key):
    settings = project.get('net_settings', {})
    classes = settings.get('classes', [])
    lookup = {c['name']: c for c in classes}
    if len(lookup) != len(classes) or 'Default' not in lookup:
        raise ValueError('Ambiguous/missing legacy Default netclass')
    if settings.get('netclass_assignments'):
        raise ValueError('Legacy netclass_assignments need separate semantic migration')
    selected = 'Default'; assigned = set()
    for item in settings.get('netclass_patterns', []):
        pattern = net(item['pattern'])
        if pattern in assigned or item['netclass'] not in lookup:
            raise ValueError('Ambiguous legacy netclass pattern')
        assigned.add(pattern)
        if name == pattern:
            selected = item['netclass']
    value = lookup[selected].get(key)
    if not number(value):
        raise ValueError('Missing/invalid netclass minimum')
    return value

def migration_inputs(root, config):
    relative = config.get('configuration_migration')
    return [cfg.path(root, relative)] if relative else []

def validate_board(root, config):
    path = cfg.path(root, config['name']+'.kicad_pcb')
    scoped = pairs(config)
    if not scoped:
        return
    if not path.exists():
        if scoped:
            raise ValueError('Scoped clearances require actual saved board net inventory')
        return
    actual = board_nets(path)
    declared = {n for r in scoped for side in ['nets_a','nets_b'] for n in r[side]}
    if declared - actual:
        raise ValueError('Scoped clearance has unknown saved-board net: '+repr(sorted(declared-actual)))

def ensure_native_not_weaker(before, after):
    old_global = before.get('board',{}).get('design_settings',{}).get('rules',{})
    new_global = after.get('board',{}).get('design_settings',{}).get('rules',{})
    for key,value in old_global.items():
        if key.startswith('min_') and number(value):
            if key not in new_global or not number(new_global[key]) or new_global[key] < value:
                raise ValueError('Migration weakens native minimum: '+key)
    for section in ['board','erc']:
        a = before.get('board',{}).get('design_settings',{}) if section=='board' else before.get('erc',{})
        b = after.get('board',{}).get('design_settings',{}) if section=='board' else after.get('erc',{})
        for key,value in a.get('rule_severities',{}).items():
            if value not in RANK or b.get('rule_severities',{}).get(key) not in RANK or RANK[b['rule_severities'][key]] < RANK[value]:
                raise ValueError('Migration weakens existing severity: '+section+'/'+key)
    if before.get('erc',{}).get('pin_map') is not None and before['erc']['pin_map'] != after.get('erc',{}).get('pin_map'):
        raise ValueError('Existing ERC pin matrix change requires separate review')

def generated_clearances(text, global_rules):
    roots = sexprs(text)
    if not roots or roots[0] != ['version','1']:
        raise ValueError('Generated rules must begin with version 1')
    floors = {'track_width':'min_track_width','hole_size':'min_through_hole_diameter',
              'annular_width':'min_via_annular_width','edge_clearance':'min_copper_edge_clearance',
              'via_diameter':'min_via_diameter','silk_clearance':'min_silk_clearance'}
    result, literals, names = [], set(), set()
    for row in roots[1:]:
        if not isinstance(row,list) or len(row) not in [3,4] or row[0]!='rule' or not isinstance(row[1],str) or row[1] in names:
            raise ValueError('Unknown/duplicate generated rule')
        names.add(row[1]); expression=None; constraint=None; seen=set()
        for entry in row[2:]:
            if not isinstance(entry,list) or not entry or entry[0] in seen:
                raise ValueError('Unknown generated rule entry')
            seen.add(entry[0])
            if entry[0]=='condition' and len(entry)==2 and isinstance(entry[1],str):
                expression=entry[1]
            elif entry[0]=='constraint':
                constraint=entry
            else:
                raise ValueError('Generated rule includes unsupported layer/severity/scope')
        if constraint is None or len(constraint)<3:
            raise ValueError('Generated rule lacks supported constraint')
        kind=constraint[1]
        if kind=='disallow':
            if any(t not in ['track','via','pad','zone'] for t in constraint[2:]):
                raise ValueError('Unsupported generated disallow object')
            continue
        if kind!='clearance' and kind not in floors:
            raise ValueError('Unsupported generated constraint: '+str(kind))
        if len(constraint)!=3 or not isinstance(constraint[2],list) or not constraint[2] or constraint[2][0]!='min':
            raise ValueError('Only generated minimum constraints supported')
        m=re.fullmatch(r'([0-9]+(?:\.[0-9]+)?)mm',''.join(constraint[2][1:]))
        if not m or not number(float(m[1])):
            raise ValueError('Generated finite millimetre minimum required')
        value=float(m[1]);floor=global_rules.get('min_clearance' if kind=='clearance' else floors[kind],0)
        if not number(floor) or value+1e-12<floor:
            raise ValueError('Generated custom constraint weakens native minimum: '+kind)
        if kind=='clearance':
            ast, found=(None,set()) if expression is None else condition(expression)
            literals.update(found); result.append((ast,value))
    return result,literals

def nonclearance_rows(text):
    return [r for r in sexprs(text)[1:] if any(isinstance(x,list) and len(x)>1 and x[0]=='constraint' and x[1]!='clearance' for x in r[2:])]

def review_legacy(root, config, desired_project, generated_dru):
    relative = config.get('configuration_migration')
    if not relative:
        raise ValueError('Explicit configuration_migration descriptor required')
    doc = strict_json(cfg.path(root, relative).read_text(encoding='utf-8-sig'))
    required = {'schema_version','legacy_rules_sha256','legacy_project_sha256','net_names','reviewed_by','reason'}
    if not isinstance(doc, dict) or set(doc) != required or doc['schema_version'] != 1:
        raise ValueError('Invalid migration descriptor schema')
    if not all(isinstance(doc[k], str) and doc[k].strip() for k in ['reviewed_by','reason']):
        raise ValueError('Actual coordinator review identity/reason required, not stage approval')
    name = config['name']; old_raw = cfg.raw(root, name+'.kicad_pro'); old_dru = cfg.raw(root, name+'.kicad_dru')
    if old_raw is None or old_dru is None or cfg.sha(old_raw) != doc['legacy_project_sha256'] or cfg.sha(old_dru) != doc['legacy_rules_sha256']:
        raise ValueError('Migration source hashes differ')
    old = strict_json(old_raw.decode('utf-8-sig'))
    actual_nets = board_nets(cfg.path(root, name+'.kicad_pcb'))
    if not isinstance(doc['net_names'], list):
        raise ValueError('Migration net inventory must be a list')
    for value in doc['net_names']:
        net(value)
    if len(doc['net_names']) != len(set(doc['net_names'])) or set(doc['net_names']) != actual_nets:
        raise ValueError('Migration net inventory differs from actual saved board')
    old_global = old['board']['design_settings']['rules']
    new_global = desired_project['board']['design_settings']['rules']
    try:
        old_rules, literals = legacy_rules(old_dru.decode('utf-8-sig'))
    except ValueError:
        # Subsequent generated-policy updates remain bounded. Non-clearance
        # constraints must stay byte-semantically identical; new disallows may be added.
        old_rules,literals = generated_clearances(old_dru.decode('utf-8-sig'),old_global)
        before_rows=nonclearance_rows(old_dru.decode('utf-8-sig'))
        after_rows=nonclearance_rows(generated_dru)
        if any(r not in after_rows for r in before_rows):
            raise ValueError('Existing generated non-clearance constraint changed; separate migration required')
        added=[r for r in after_rows if r not in before_rows]
        if any(not any(x[:2]==['constraint','disallow'] for x in r[2:]) for r in added):
            raise ValueError('New non-clearance policy requires separate migration')
    target_rules,target_literals = generated_clearances(generated_dru,new_global)
    scoped = pairs(config)
    declared = {n for r in scoped for side in ['nets_a','nets_b'] for n in r[side]}
    if not actual_nets or (declared | literals | target_literals) - actual_nets:
        raise ValueError('Scoped rule references a net absent from actual board')
    ensure_native_not_weaker(old,desired_project)
    for project in [old,desired_project]:
        floor=project['board']['design_settings']['rules'].get('min_clearance',0)
        if any(c.get('clearance',0)>floor for c in project.get('net_settings',{}).get('classes',[])):
            raise ValueError('Netclass clearance above global floor requires separate precedence migration')
    for key, value in old_global.items():
        if key.startswith('min_') and number(value):
            if key not in new_global or not number(new_global[key]) or new_global[key] < value:
                raise ValueError('Migration weakens native minimum: '+key)
    for section in ['board', 'erc']:
        before = old.get('board', {}).get('design_settings', {}) if section == 'board' else old.get('erc', {})
        after = desired_project['board']['design_settings'] if section == 'board' else desired_project.get('erc', {})
        for key, value in before.get('rule_severities', {}).items():
            if value not in RANK or after.get('rule_severities', {}).get(key) not in RANK or RANK[after['rule_severities'][key]] < RANK[value]:
                raise ValueError('Migration weakens existing severity: '+section+'/'+key)
    if old.get('erc', {}).get('pin_map') is not None and old['erc']['pin_map'] != desired_project.get('erc', {}).get('pin_map'):
        raise ValueError('Existing ERC pin matrix change requires separate review')
    fallback = '__HW_UNKNOWN__'
    while fallback in actual_nets:
        fallback += '_'
    cases = sorted(actual_nets) + ['', fallback]
    rows = []
    for a, b in itertools.product(cases, repeat=2):
        old_floor = max(old_global.get('min_clearance', 0), class_value(old, a, 'clearance'), class_value(old, b, 'clearance'))
        old_values=[v for ast,v in old_rules if matches(ast,a,b)]
        if old_values != sorted(old_values):
            raise ValueError('Descending legacy matching precedence requires separate migration')
        before = max([old_floor]+old_values)
        new_floor = max(new_global.get('min_clearance', 0), class_value(desired_project, a, 'clearance'), class_value(desired_project, b, 'clearance'))
        new_values=[v for ast,v in target_rules if matches(ast,a,b)]
        if new_values != sorted(new_values):
            raise ValueError('Descending generated matching precedence requires separate migration')
        after = max([new_floor]+new_values)
        if after + 1e-12 < before:
            raise ValueError('Migration weakens effective clearance: %r / %r: %s -> %s' % (a,b,before,after))
        rows.append([a,b,before,after])
    return {'schema_version':1, 'legacy_rules_sha256':cfg.sha(old_dru), 'legacy_project_sha256':cfg.sha(old_raw), 'generated_rules_sha256':cfg.sha(generated_dru.encode()), 'descriptor_sha256':cfg.sha(cfg.path(root, relative).read_bytes()), 'reviewed_by':doc['reviewed_by'], 'reason':doc['reason'], 'actual_net_names':sorted(actual_nets), 'ordered_pair_cases':len(rows), 'effective_pairs_sha256':cfg.sha(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()), 'effective_pairs':rows, 'native_minimums_preserved':True, 'explicit_severities_preserved':True, 'scope':'Bounded exact-net-only legacy grammar; all directed pairs including same/empty/unknown nets. Rules contain no layer/object predicates, so each pair is layer/object invariant. Added spatial disallows are additional constraints, not substitutes for clearance. Missing old ERC matrix means native implicit defaults require separately recorded ERC controls. No stage/process/supplier approval.'}
