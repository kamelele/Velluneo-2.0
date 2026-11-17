"""Compare independently approved physical-pin intent with KiCad 10.0.6 XML export."""
import copy
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import configuration


def text(value):
    return isinstance(value,str) and bool(value.strip()) and value==value.strip()


def intent_digest(document):
    body=copy.deepcopy(document)
    body.pop('approval',None)
    return hashlib.sha256(json.dumps(body,sort_keys=True,ensure_ascii=False,
                                    separators=(',',':'),allow_nan=False).encode()).hexdigest()


def loads(data):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('Duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(data,object_pairs_hook=unique)


def source_path(root,relative):
    if not text(relative) or '.work' in Path(relative).parts:
        raise ValueError('Declare a project source path outside .work for connectivity intent')
    return configuration.path(root,relative)


def tracked_inputs(root,config):
    relative=config.get('product',{}).get('connectivity_file')
    if not relative:return []
    target=source_path(root,relative).resolve();paths=[target]
    if target.is_file():
        document=loads(target.read_text(encoding='utf-8-sig'))
        for item in document.get('basis_sources',[]):paths.append(source_path(root,item['path']).resolve())
    return paths


def pin(item):
    if not isinstance(item,dict) or not text(item.get('ref')) or '?' in item['ref'] or not text(item.get('pin')):
        raise ValueError('Pins require annotated refdes and physical pin-number strings')
    return item['ref'],item['pin']


def pin_record(pair):
    return {'ref':pair[0],'pin':pair[1]}


def pin_records(pairs):
    return [pin_record(p) for p in sorted(pairs)]


def validate_intent(document):
    if not isinstance(document,dict) or type(document.get('schema_version')) is not int or document['schema_version']!=1:
        raise ValueError('Unsupported connectivity intent schema')
    if not all(text(document.get(k)) for k in ['revision','basis']):
        raise ValueError('Connectivity intent requires revision and independent basis')
    for key in ['components','nets','no_connects','barriers']:
        if not isinstance(document.get(key),list) or any(not isinstance(x,dict) for x in document[key]):
            raise ValueError('Expected object list: '+key)
    if not isinstance(document.get('basis_sources'),list):
        raise ValueError('Independent basis_sources must be an explicit list')
    for item in document['basis_sources']:
        if not isinstance(item,dict) or not text(item.get('path')) or not re.fullmatch('[0-9a-f]{64}',str(item.get('sha256',''))):
            raise ValueError('Basis sources require paths and SHA256 hashes')
    components={};inventory=set()
    for component in document['components']:
        ref=component.get('ref')
        if not text(ref) or '?' in ref or ref in components or not isinstance(component.get('units'),list):
            raise ValueError('Components require unique annotated references and explicit unit lists')
        units={};physical=set()
        for unit in component['units']:
            name=unit.get('name')
            if not text(name) or name in units or not isinstance(unit.get('pins'),list) or any(not text(p) for p in unit['pins']):
                raise ValueError('Units require unique names and physical-pin lists')
            if len(unit['pins'])!=len(set(unit['pins'])):
                raise ValueError('Duplicate physical pin within a unit')
            units[name]=set(unit['pins']);physical.update(unit['pins'])
        if not physical and not text(component.get('pinless_reason')):
            raise ValueError('Pinless components require an explicit rationale')
        components[ref]=units;inventory.update((ref,p) for p in physical)
    if not components and not text(document.get('empty_design_reason')):
        raise ValueError('An empty design requires an explicit reviewed reason')
    if components and not document['basis_sources']:
        raise ValueError('Nonempty designs require independent basis source files')
    groups={};assignment={}
    for net in document['nets']:
        identifier=net.get('id')
        if not text(identifier) or identifier in groups or not isinstance(net.get('pins'),list) or not net['pins']:
            raise ValueError('Nets require unique IDs and nonempty pin sets')
        members=[pin(p) for p in net['pins']]
        if len(members)==1 and not text(net.get('single_pin_rationale')):
            raise ValueError('Singleton nets require a rationale; unused pins belong in no_connects')
        for member in members:
            if member not in inventory or member in assignment:
                raise ValueError('Unknown or multiply assigned intent pin: '+str(member))
            assignment[member]=identifier
        groups[identifier]=set(members)
    nc=set()
    for item in document['no_connects']:
        member=pin(item)
        if member not in inventory or member in assignment or member in nc or not text(item.get('reason')):
            raise ValueError('NC pins must be unique, unassigned, known and justified')
        nc.add(member)
    if set(assignment)|nc != inventory:
        raise ValueError('Every physical pin must be assigned to a net or explicit NC')
    barrier_ids=set()
    for barrier in document['barriers']:
        identifier=barrier.get('id')
        if not text(identifier) or identifier in barrier_ids or not text(barrier.get('basis')):
            raise ValueError('Barriers require unique IDs and a basis')
        barrier_ids.add(identifier)
        for side in ['side_a','side_b']:
            if not isinstance(barrier.get(side),list) or not barrier[side] or any(x not in groups for x in barrier[side]):
                raise ValueError('Barrier sides must reference known net IDs')
        if set(barrier['side_a']) & set(barrier['side_b']):
            raise ValueError('Barrier sides cannot contain the same intended net')
    return {'components':components,'inventory':inventory,'groups':groups,'assignment':assignment,'nc':nc}


def parse_export(data,expected_version='10.0.6'):
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('Unexpected XML document declarations')
    root=ET.fromstring(data)
    if root.tag!='export' or root.get('version')!='E':
        raise ValueError('Unsupported KiCad XML export schema')
    if any(root.find(key) is None for key in ['design','components','libparts','nets']):
        raise ValueError('Incomplete KiCad XML export')
    tool=root.findtext('design/tool','')
    # Ubuntu's validated 10.0.6+dfsg-1 package preserves its packaging revision.
    # Keep an explicit identity list; do not normalize arbitrary suffixes/nightlies.
    tools={'10.0.6':{'Eeschema 10.0.6','Eeschema 10.0.6+dfsg-1'}}
    if tool not in tools.get(expected_version,set()):
        raise ValueError('Export tool version does not match the project pin')
    parts={}
    for part in root.findall('libparts/libpart'):
        key=(part.get('lib'),part.get('part'))
        if not all(text(x) for x in key) or key in parts:
            raise ValueError('Invalid or duplicate library part')
        numbers=[item.get('num') for item in part.findall('pins/pin')]
        if any(not text(x) for x in numbers):raise ValueError('Invalid physical library pin')
        parts[key]=set(numbers)
    components={};inventory=set();unplaced=set();instance_counts={}
    for component in root.findall('components/comp'):
        ref=component.get('ref');source=component.find('libsource')
        if not text(ref) or '?' in ref or ref in components or source is None:
            raise ValueError('Invalid, unannotated or duplicate exported reference')
        key=(source.get('lib'),source.get('part'))
        if key not in parts:raise ValueError('Exported component has no resolved library pin inventory')
        units={};placed=set()
        for unit in component.findall('units/unit'):
            name=unit.get('name');numbers=[p.get('num') for p in unit.findall('pins/pin')]
            if not text(name) or name in units or any(not text(p) for p in numbers) or len(numbers)!=len(set(numbers)):
                raise ValueError('Invalid exported unit/pin inventory')
            if not set(numbers)<=parts[key]:raise ValueError('Unit pin absent from library inventory')
            units[name]=set(numbers);placed.update(numbers)
        if parts[key] and not units:raise ValueError('Export lacks supported component-unit data')
        stamps=component.findtext('tstamps','').split()
        if not stamps or len(stamps)!=len(set(stamps)):
            raise ValueError('Export lacks distinct symbol instance timestamps')
        instance_counts[ref]=len(stamps)
        components[ref]=units;inventory.update((ref,p) for p in parts[key])
        unplaced.update((ref,p) for p in parts[key]-placed)
    groups={};assignment={};nc=set();names={}
    for net in root.findall('nets/net'):
        code=net.get('code')
        if not text(code) or code in groups:raise ValueError('Missing or duplicate export net code')
        members=set()
        for node in net.findall('node'):
            member=pin({'ref':node.get('ref'),'pin':node.get('pin')})
            if member not in inventory:raise ValueError('Net node absent from physical pin inventory')
            if member in assignment and assignment[member]!=code:
                raise ValueError('A physical pin occurs in multiple exported nets')
            members.add(member);assignment[member]=code
            if 'no_connect' in node.get('pintype','').split('+'):nc.add(member)
        if not members:raise ValueError('Unexpected empty exported net')
        groups[code]=members;names[code]=net.get('name','')
    return {'components':components,'inventory':inventory,'unplaced':unplaced,
            'groups':groups,'assignment':assignment,'nc':nc,'names':names,
            'tool':tool,'source':root.findtext('design/source',''),'instance_counts':instance_counts}


def compare(document,actual):
    expected=validate_intent(document)
    errors=[]
    def error(kind,message,**detail):errors.append({'type':kind,'message':message,**detail})
    for ref in sorted(set(expected['components'])|set(actual['components'])):
        if ref not in actual['components']:error('missing_component','Expected component absent',ref=ref)
        elif ref not in expected['components']:error('unexpected_component','Unexpected exported component',ref=ref)
        elif expected['components'][ref]!=actual['components'][ref]:
            error('unit_pin_mismatch','Library unit/physical pin inventory differs',ref=ref,
                  expected={k:sorted(v) for k,v in expected['components'][ref].items()},
                  actual={k:sorted(v) for k,v in actual['components'][ref].items()})
        if ref in expected['components'] and ref in actual['components'] and expected['components'][ref] and actual['instance_counts'][ref]!=len(expected['components'][ref]):
            error('unit_instance_count_mismatch','Symbol instance count differs from intended units',ref=ref,
                  expected=len(expected['components'][ref]),actual=actual['instance_counts'][ref])
    missing=expected['inventory']-actual['inventory'];extra=actual['inventory']-expected['inventory']
    if missing:error('missing_pins','Expected physical pins absent',pins=pin_records(missing))
    if extra:error('unexpected_pins','Unexpected physical pins exported',pins=pin_records(extra))
    if actual['unplaced']:error('unplaced_unit_pins','Library pins lack a placed unit',pins=pin_records(actual['unplaced']))
    for identifier,members in expected['groups'].items():
        codes={actual['assignment'][p] for p in members if p in actual['assignment']}
        absent=members-set(actual['assignment'])
        if absent:error('unassigned_expected_pins','Expected net pins are absent from export nets',net_id=identifier,pins=pin_records(absent))
        if len(codes)>1:error('split_net','An intended net is split across exported nets',net_id=identifier,
                              actual_nets=[{'code':c,'name':actual['names'][c]} for c in sorted(codes)])
    for code,members in actual['groups'].items():
        identifiers={expected['assignment'][p] for p in members if p in expected['assignment']}
        if len(identifiers)>1:error('merged_nets','Distinct intended nets are electrically merged',
                                  intended_nets=sorted(identifiers),actual_net=actual['names'][code],pins=pin_records(members))
    for member in sorted(expected['nc']):
        code=actual['assignment'].get(member)
        if member not in actual['nc']:error('missing_nc_marker','Expected explicit NC is absent',pin=pin_record(member))
        if code is not None and actual['groups'][code]!={member}:
            error('connected_nc','Expected NC pin is electrically connected',pin=pin_record(member))
    unexpected_nc=actual['nc']-expected['nc']
    if unexpected_nc:error('unexpected_nc','Intended connected pins carry NC',pins=pin_records(unexpected_nc))
    for barrier in document['barriers']:
        sides=[]
        for side in ['side_a','side_b']:
            pins=set().union(*(expected['groups'][name] for name in barrier[side]))
            sides.append({actual['assignment'][p] for p in pins if p in actual['assignment']})
        if sides[0]&sides[1]:error('barrier_breached','Declared electrical separation is bridged',barrier_id=barrier['id'])
    current=intent_digest(document);approval=document.get('approval')
    if not isinstance(approval,dict) or not all(text(approval.get(k)) for k in ['approved_by','evidence']) or approval.get('intent_digest')!=current:
        error('missing_stale_intent_approval','Intent lacks current human approval evidence')
    return {'schema_version':1,'passed':not errors,'errors':errors,'intent_digest':current,
            'intent_revision':document['revision'],'physical_pins':len(expected['inventory']),
            'intended_nets':len(expected['groups']),'no_connects':len(expected['nc']),
            'limitations':['Graph agreement is not functional, part/MPN, PCB or physical isolation validation.',
                           'Approval fields record evidence; hashes do not authenticate a human.']}


def verify(root,config,cli,run_tool):
    report={'schema_version':1,'passed':False,'errors':[],'commands':[]}
    try:
        output=configuration.path(root,'.work/connectivity-netlist.xml')
        output.parent.mkdir(parents=True,exist_ok=True)
        output.unlink(missing_ok=True)
        relative=config.get('product',{}).get('connectivity_file')
        intent=source_path(root,relative)
        document=loads(intent.read_text(encoding='utf-8-sig'))
        validate_intent(document)
        if config['kicad_version']!='10.0.6':raise ValueError('Connectivity exporter validated only for KiCad 10.0.6')
        if not re.fullmatch('[A-Za-z0-9_-]+',config['name']):raise ValueError('Invalid project name')
        schematic=configuration.path(root,config['name']+'.kicad_sch').resolve()
        inputs=[intent,schematic]
        hardware=configuration.path(root,'hardware.json')
        if hardware.is_file():inputs.append(hardware)
        for item in document['basis_sources']:
            basis=source_path(root,item['path'])
            if basis.resolve()==intent.resolve() or basis.suffix in ['.kicad_sch','.kicad_pcb']:
                raise ValueError('Intent basis must be independent of the CAD under test')
            if configuration.sha(basis.read_bytes())!=item['sha256']:
                raise ValueError('Independent intent basis changed: '+item['path'])
            inputs.append(basis)
        inputs.extend(configuration.path(root,p) for p in config.get('source_files',[]) if configuration.path(root,p).is_file())
        discovered={p.resolve() for p in configuration.design_files(root,['.kicad_sch','.kicad_sym','.kicad_mod'])}
        inputs.extend(discovered)
        inputs=sorted(set(inputs))
        before={str(p):configuration.sha(p.read_bytes()) for p in inputs}
        run=run_tool(cli,['sch','export','netlist','--format','kicadxml','--output',str(output),str(schematic)],root)
        report['commands'].append(run)
        if run['exit_code']!=0 or not output.is_file() or not output.stat().st_size:
            raise ValueError('KiCad netlist export failed; no cached success accepted')
        actual=parse_export(output.read_bytes(),config['kicad_version'])
        if Path(actual['source']).resolve()!=schematic:raise ValueError('Export refers to another schematic')
        result=compare(document,actual)
        report.update(result)
        report.update(intent_sha256=configuration.sha(intent.read_bytes()),
                      export_sha256=configuration.sha(output.read_bytes()),export_tool=actual['tool'])
        if any(configuration.sha(p.read_bytes())!=before[str(p)] for p in inputs):
            raise ValueError('Input changed during connectivity verification')
        after_discovered={p.resolve() for p in configuration.design_files(root,['.kicad_sch','.kicad_sym','.kicad_mod'])}
        if after_discovered!=discovered:raise ValueError('Local source set changed during verification')
    except (ValueError,KeyError,TypeError,AttributeError,OSError,ET.ParseError) as exc:
        report['passed']=False;report['configuration_error']=True
        report['errors'].append({'type':'connectivity_check_failed','message':str(exc)})
    return report
