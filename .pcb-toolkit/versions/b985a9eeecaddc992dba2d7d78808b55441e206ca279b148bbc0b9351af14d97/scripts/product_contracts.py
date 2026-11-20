"""Requirements traceability and declared interface consistency, not CAD/physics proof."""
import copy
import hashlib
import json
import math
import re
from pathlib import Path

import configuration

STAGES = ['specification','schematic','placement','routing','release']
METHODS = ['design','review','calculation','simulation','measurement','ERC','DRC']
LEVELS = dict(zip(METHODS,['designed','reviewed','calculated','simulated','measured','ERC-checked','DRC-checked']))


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,
                                    separators=(',',':'),allow_nan=False).encode()).hexdigest()


def intent_digest(document):
    content = copy.deepcopy(document)
    content.pop('evidence',None)
    return digest(content)


def source_path(root, relative):
    if not isinstance(relative,str) or not relative or '.work' in Path(relative).parts:
        raise ValueError('Contract inputs must be named project sources outside .work')
    return configuration.path(root,relative)


def read(root, relative):
    return json.loads(source_path(root,relative).read_text(encoding='utf-8-sig'))


def tracked_inputs(root, config):
    relative = config.get('product',{}).get('requirements_file')
    if not relative:
        return []
    paths = [source_path(root,relative)]
    if not paths[0].exists():
        return paths
    document = read(root,relative)
    for record in document.get('evidence',[]):
        if record.get('artifact'):
            paths.append(source_path(root,record['artifact']))
        for item in record.get('inputs',[]):
            paths.append(source_path(root,item['path']))
    return sorted(set(p.resolve() for p in paths))


def nonempty(value):
    return isinstance(value,str) and bool(value.strip())


def number(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)


def declared(value):
    if isinstance(value,dict):
        return all(nonempty(k) and declared(v) for k,v in value.items())
    if isinstance(value,list):
        return all(declared(v) for v in value)
    if isinstance(value,str):
        return nonempty(value)
    return isinstance(value,bool) or number(value)


def evaluate(root, relative, stage='specification'):
    report = {'schema_version':1,'stage':stage,'errors':[],'matrix':[],
              'open_questions':[],'passed':False,'limitations':[
                  'Declared contracts are not compared to CAD netlists or geometry (#9/#11).',
                  'Hashes establish freshness, not evidence truth or reviewer authority.',
                  'Electrical checks compare declared DC envelopes only, not complete operation.']}
    errors = report['errors']
    blockers = []
    def finding(record, message, gate=None):
        gate = gate or record.get('gate','specification')
        item = {'id':record['id'],'gate':gate,'message':message}
        blockers.append(item)
        if STAGES.index(gate) <= STAGES.index(stage):
            errors.append(item)
    try:
        if stage not in STAGES:
            raise ValueError('Unknown stage')
        if not relative:
            raise ValueError('Set product.requirements_file before checking requirements')
        document = read(root,relative)
        if not isinstance(document,dict) or document.get('schema_version') != 1:
            raise ValueError('Unsupported requirements schema')
        if not nonempty(document.get('revision')) or not nonempty(document.get('product')):
            raise ValueError('Product identity and revision are required')
        names = ['subsystems','requirements','interfaces','unknowns','evidence']
        for name in names:
            if not isinstance(document.get(name),list) or any(not isinstance(x,dict) for x in document[name]):
                raise ValueError('Expected object list: '+name)
        ids = [record.get('id') for name in names for record in document[name]]
        if any(not isinstance(i,str) or not re.fullmatch('[A-Za-z][A-Za-z0-9_-]*',i) for i in ids) or len(ids)!=len(set(ids)):
            raise ValueError('All record IDs must be valid and globally unique')
        subsystems = {x['id']:x for x in document['subsystems']}
        requirements = {x['id']:x for x in document['requirements']}
        targets = {x['id']:x for name in ['requirements','interfaces'] for x in document[name]}
        evidence = {x['id']:x for x in document['evidence']}
        for record in document['subsystems']:
            if not nonempty(record.get('owner')) or record.get('kind') not in ['pcb','enclosure','firmware']:
                raise ValueError('Subsystem needs owner and kind: '+record['id'])
        if not subsystems or not requirements:
            errors.append({'id':'PRODUCT','gate':'specification','message':'Subsystems and requirements must be nonempty'})
        for record in targets.values():
            if record.get('gate') not in STAGES or record.get('method') not in METHODS:
                raise ValueError('Record needs a valid gate and verification method: '+record['id'])
            if not nonempty(record.get('revision')) or not nonempty(record.get('owner')):
                raise ValueError('Record needs revision and owner: '+record['id'])
            if not isinstance(record.get('evidence_ids'),list) or any(x not in evidence for x in record['evidence_ids']):
                raise ValueError('Evidence reference missing: '+record['id'])
        for item in document['unknowns']:
            if item.get('record_id') not in targets or item.get('blocks_stage') not in STAGES or not all(nonempty(item.get(k)) for k in ['owner','question','field']):
                raise ValueError('Unknown needs target, field, owner, question and blocked stage')
            if item.get('status') not in ['open','resolved']:
                raise ValueError('Unknown status must be open or resolved')
            if item['status']=='open':
                report['open_questions'].append(item)
                finding(item,'Unresolved: '+item['question'],item['blocks_stage'])
            elif not nonempty(item.get('resolution')) or not item.get('evidence_ids'):
                finding(item,'Resolved unknown lacks resolution/evidence',item['blocks_stage'])
        current = intent_digest(document)
        report.update(intent_digest=current,product=document['product'],revision=document['revision'],
                      document_sha256=configuration.sha(source_path(root,relative).read_bytes()))
        valid_evidence = {}
        evidence_errors = {}
        for identifier,record in evidence.items():
            problems = []
            if record.get('kind') not in METHODS or record.get('result') not in ['pass','fail'] or not nonempty(record.get('verified_by')):
                problems.append('Evidence needs kind, pass/fail result and verifier')
            if record.get('intent_digest') != current:
                problems.append('Evidence refers to a different intent revision/digest')
            if not isinstance(record.get('inputs'),list):
                problems.append('Evidence inputs must be an explicit list')
            elif record.get('kind') not in ['design','review'] and not record['inputs']:
                problems.append('Technical evidence requires hashed verification inputs')
            artifact = source_path(root,record.get('artifact'))
            if not artifact.is_file() or not artifact.stat().st_size or configuration.sha(artifact.read_bytes()) != record.get('sha256'):
                problems.append('Evidence artifact missing, empty or modified')
            for item in record.get('inputs',[]):
                target = source_path(root,item['path'])
                if not target.is_file() or configuration.sha(target.read_bytes()) != item.get('sha256'):
                    problems.append('Evidence input missing or modified: '+item['path'])
            if record.get('result')=='fail':
                problems.append('Verification result is fail')
            evidence_errors[identifier] = problems
            if not problems:
                valid_evidence[identifier] = record
        for item in document['unknowns']:
            if item['status']=='resolved' and any(x not in valid_evidence for x in item.get('evidence_ids',[])):
                finding(item,'Resolved unknown has stale/missing/failed evidence',item['blocks_stage'])
        for identifier,record in targets.items():
            active = STAGES.index(record['gate']) <= STAGES.index(stage)
            for key in ['basis','acceptance']:
                if not nonempty(record.get(key)):
                    finding(record,'Missing '+key)
            implementation = record.get('implementation')
            if not isinstance(implementation,list) or not implementation:
                finding(record,'No implementation objects assigned')
            else:
                for item in implementation:
                    if not isinstance(item,dict) or item.get('subsystem') not in subsystems or not nonempty(item.get('object')):
                        raise ValueError('Invalid implementation object: '+identifier)
            for ref in record['evidence_ids']:
                for error in evidence_errors[ref]:
                    finding(record,ref+': '+error)
            usable = [valid_evidence[x] for x in record['evidence_ids'] if x in valid_evidence]
            required_paths = {item.get('path') for item in implementation or [] if isinstance(item,dict)}
            if record['method'] not in ['design','review']:
                if not required_paths or None in required_paths:
                    finding(record,'Technical verification needs implementation input paths')
                else:
                    for name in required_paths:source_path(root,name)
            usable = [item for item in usable if item['kind'] in ['design','review'] or
                      (required_paths and None not in required_paths and required_paths <= {x['path'] for x in item['inputs']})]
            if not any(x['kind']==record['method'] for x in usable):
                finding(record,'Required evidence kind absent: '+record['method'])
            if identifier in requirements:
                if not nonempty(record.get('text')):
                    finding(record,'Missing requirement statement')
            else:
                if record.get('kind') not in ['electrical','firmware','mechanical']:
                    raise ValueError('Unknown interface kind: '+identifier)
                latest = 'placement' if record['kind']=='mechanical' else 'schematic'
                if STAGES.index(record['gate']) > STAGES.index(latest):
                    raise ValueError('Interface gate is too late; latest is '+latest+': '+identifier)
                refs = record.get('requirements')
                if not isinstance(refs,list) or not refs or any(x not in requirements for x in refs):
                    raise ValueError('Interface needs existing requirement IDs: '+identifier)
                endpoints = record.get('endpoints')
                if not isinstance(endpoints,list) or len(endpoints)!=2 or any(not isinstance(x,dict) or x.get('subsystem') not in subsystems for x in endpoints):
                    raise ValueError('Interface needs two known subsystem endpoints: '+identifier)
                if endpoints[0]['subsystem']==endpoints[1]['subsystem']:
                    raise ValueError('Interface endpoints must be distinct subsystems')
                if active:
                    check_interface(record,lambda message:finding(record,message))
            row_errors = [x for x in errors if x['id']==identifier or
                          any(u['id']==x['id'] and u['record_id']==identifier for u in document['unknowns'])]
            report['matrix'].append({'id':identifier,'revision':record['revision'],'owner':record['owner'],
                'type':'requirement' if identifier in requirements else record['kind']+'-interface',
                'gate':record['gate'],'implementation':record.get('implementation',[]),
                'required_kind':record['method'],'evidence_ids':record['evidence_ids'],
                'observed_levels':sorted({LEVELS[x['kind']] for x in usable}),
                'status':'blocked' if active and row_errors else ('verified' if active else 'not_due')})
        report['blockers'] = blockers
        report['blocked_stages'] = [s for s in STAGES if any(STAGES.index(x['gate'])<=STAGES.index(s) for x in blockers)]
        report['passed'] = not errors
    except (ValueError,TypeError,KeyError,OSError,AttributeError) as exc:
        report['configuration_error']=True
        errors.append({'id':'DOCUMENT','gate':'specification','message':str(exc)})
        report['blocked_stages']=STAGES.copy()
    return report


def check_interface(record, fail):
    kind = record['kind']
    a,b = record['endpoints']
    for key in ['startup_behavior','fault_behavior']:
        if not nonempty(record.get(key)):
            fail('Missing '+key)
    if kind=='firmware':
        for endpoint in [a,b]:
            if not nonempty(endpoint.get('protocol')) or not isinstance(endpoint.get('parameters'),dict) or not endpoint['parameters']:
                fail('Firmware endpoint needs protocol and explicit parameters')
            elif not declared(endpoint['parameters']):
                fail('Firmware parameters contain unknown/invalid values')
        if a.get('protocol')!=b.get('protocol') or a.get('parameters')!=b.get('parameters'):
            fail('Firmware endpoint protocol/parameters conflict')
    elif kind=='mechanical':
        geometry = record.get('geometry',{})
        if geometry.get('unit')!='mm':fail('Mechanical geometry must use mm')
        outline = geometry.get('outline')
        if not isinstance(outline,list) or len(outline)<3 or any(not isinstance(p,list) or len(p)!=2 or not all(number(v) for v in p) for p in outline):
            fail('Mechanical outline needs at least three finite x/y points')
        for key in ['mounting_holes','connector_positions','keepouts']:
            if not isinstance(geometry.get(key),list):fail('Missing mechanical list: '+key)
        for key in ['max_component_height_mm','tolerance_mm']:
            if not number(geometry.get(key)) or geometry[key]<0:fail('Missing/invalid mechanical value: '+key)
        if not nonempty(geometry.get('thermal_conditions')):fail('Missing thermal conditions')
        for hole in geometry.get('mounting_holes',[]):
            if not all(number(hole.get(k)) for k in ['x','y','diameter']) or hole.get('diameter',0)<=0:
                fail('Mounting hole needs finite x/y and positive diameter')
        for connector in geometry.get('connector_positions',[]):
            if not nonempty(connector.get('ref')) or not all(number(connector.get(k)) for k in ['x','y','z','height']) or connector['height']<0:
                fail('Connector needs ref, x/y/z and height')
        for region in geometry.get('keepouts',[]):
            if not nonempty(region.get('reason')) or not isinstance(region.get('outline'),list) or len(region['outline'])<3 or any(not isinstance(p,list) or len(p)!=2 or not all(number(v) for v in p) for p in region['outline']):
                fail('Keepout needs reason and outline')
    else:
        pins = []
        for endpoint in [a,b]:
            if not nonempty(endpoint.get('connector')) or not isinstance(endpoint.get('pins'),list) or not endpoint['pins']:
                fail('Electrical endpoint needs connector and pins');return
            mapped = {p.get('pin'):p for p in endpoint['pins']}
            if len(mapped)!=len(endpoint['pins']) or any(not nonempty(k) for k in mapped):
                fail('Electrical pin numbers must be unique strings');return
            pins.append(mapped)
        connections = record.get('connections')
        if not isinstance(connections,list):fail('Explicit cable/pin mapping required');return
        if sorted(x.get('a','') for x in connections)!=sorted(pins[0]) or sorted(x.get('b','') for x in connections)!=sorted(pins[1]):
            fail('Pin mapping must cover every endpoint pin exactly once');return
        for link in connections:
            pa,pb = pins[0][link['a']],pins[1][link['b']]
            role = pa.get('role')
            if role not in ['power','signal','ground','nc'] or role!=pb.get('role') or not nonempty(pa.get('signal')) or pa.get('signal')!=pb.get('signal'):
                fail('Mapped pin roles/signals conflict');continue
            if role in ['ground','nc']:continue
            directions = {pa.get('direction'),pb.get('direction')}
            if directions!={'source','sink'} and not (role=='signal' and directions=={'bidirectional'}):
                fail('Electrical drive directions conflict');continue
            if any(not number(p.get(k)) for p in [pa,pb] for k in ['voltage_min_v','voltage_max_v']) or any(p['voltage_min_v']>p['voltage_max_v'] for p in [pa,pb]):
                fail('Finite voltage envelopes required');continue
            if directions=={'source','sink'}:
                source,sink = (pa,pb) if pa['direction']=='source' else (pb,pa)
                if source['voltage_min_v']<sink['voltage_min_v'] or source['voltage_max_v']>sink['voltage_max_v']:
                    fail('Source voltage envelope exceeds sink acceptance')
                if role=='power' and (any(not number(p.get('current_ma')) or p['current_ma']<0 for p in [source,sink]) or source['current_ma']<sink['current_ma']):
                    fail('Declared power current budget incompatible')
            elif (pa['voltage_min_v'],pa['voltage_max_v'])!=(pb['voltage_min_v'],pb['voltage_max_v']):
                fail('Bidirectional voltage envelopes need an explicit compatible agreement')
