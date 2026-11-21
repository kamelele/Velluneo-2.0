"""Resolve one spatial contract for placement, routing and KiCad DRC."""
import base64
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import configuration as cfg

CONSUMERS={role:'.electronics-rules/'+role+'-input.json' for role in ['placement','routing']}


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def intent_digest(doc):return digest({k:v for k,v in doc.items() if k!='approval'})


def text(v):return isinstance(v,str) and bool(v.strip()) and v==v.strip()


def rectangle(v):
    if not isinstance(v,list) or len(v)!=4 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or abs(x)>10000 for x in v):
        raise ValueError('Rectangle must be [xmin,ymin,xmax,ymax] in finite mm')
    if v[0]>=v[2] or v[1]>=v[3]:raise ValueError('Rectangle has no positive area')
    return v


def tracked_inputs(root,config):
    rel=config.get('product',{}).get('spatial_file')
    if not rel:return []
    p=cfg.path(root,rel)
    if '.work' in p.relative_to(Path(root).resolve()).parts:raise ValueError('Spatial source cannot be transient')
    result=[p,*[cfg.path(root,x) for x in CONSUMERS.values()]]
    if p.is_file():
        doc=json.loads(p.read_text(encoding='utf-8-sig'))
        result.extend(cfg.path(root,x['path']) for x in doc.get('basis_sources',[]))
    return result


def load(root,config,values,netclasses):
    rel=config.get('product',{}).get('spatial_file')
    if not rel:return None
    p=cfg.path(root,rel)
    doc=json.loads(p.read_text(encoding='utf-8-sig'))
    if type(doc.get('schema_version')) is not int or doc['schema_version']!=1 or not text(doc.get('revision')):
        raise ValueError('Invalid spatial document version/revision')
    outline=rectangle(doc.get('outline_mm'))
    if not text(doc.get('basis')) or not doc.get('basis_sources'):raise ValueError('Independent spatial basis required')
    paths=set()
    for basis in doc['basis_sources']:
        path=cfg.path(root,basis['path'])
        if path==p or '.work' in path.relative_to(Path(root).resolve()).parts or path.suffix in ['.kicad_pcb','.kicad_sch'] or basis['path'] in paths:
            raise ValueError('Spatial basis must be independent, stable and unique')
        paths.add(basis['path'])
        if hashlib.sha256(path.read_bytes()).hexdigest()!=basis['sha256']:raise ValueError('Spatial basis changed')
    if not isinstance(doc.get('areas'),list) or not isinstance(doc.get('blocks'),list):raise ValueError('Explicit area/block inventories required')
    declared = config.get('product',{}).get('copper_layers',['F.Cu','B.Cu'])
    if not isinstance(declared,list) or len(declared) not in [2,4]:
        raise ValueError('Only validated explicit two/four-layer copper stacks supported')
    canonical=['F.Cu']+['In%d.Cu'%i for i in range(1,len(declared)-1)]+['B.Cu']
    if declared != canonical:
        raise ValueError('Copper layers must be canonical contiguous F/inner/B stack')
    ids=set()
    for area in doc['areas']:
        identifier=area.get('id')
        if not isinstance(identifier,str) or not re.fullmatch('[A-Za-z][A-Za-z0-9_-]*',identifier) or identifier in ids:raise ValueError('Invalid/duplicate spatial area ID')
        ids.add(identifier);rect=rectangle(area.get('rectangle_mm'))
        if rect[0]<outline[0] or rect[1]<outline[1] or rect[2]>outline[2] or rect[3]>outline[3]:raise ValueError('Area outside declared outline')
        if not text(area.get('basis')):raise ValueError('Area needs product/datasheet basis')
        layers=area.get('layers')
        if not isinstance(layers,list) or not layers or len(layers)!=len(set(layers)) or any(x not in declared for x in layers):raise ValueError('Protected area layers must belong to declared copper stack')
        blocked=area.get('disallow')
        if not isinstance(blocked,list) or not blocked or len(blocked)!=len(set(blocked)) or any(x not in ['track','via','pad','zone'] for x in blocked):raise ValueError('Unsupported protected object types')
        exceptions=area.get('exceptions')
        if not isinstance(exceptions,list):raise ValueError('Explicit exception list required')
        seen=set()
        for exception in exceptions:
            if not all(text(exception.get(k)) for k in ['net','reason','approved_by','evidence']):raise ValueError('Exact net exception requires genuine approval evidence')
            if not re.fullmatch('[A-Za-z0-9_/+.-]+',exception['net']) or exception['net'] in seen:raise ValueError('Unsafe/duplicate exception net')
            seen.add(exception['net'])
    block_ids=set()
    requirement_path=config.get('product',{}).get('requirements_file')
    requirement_ids=set()
    if doc['blocks']:
        if not requirement_path:raise ValueError('Block cards need a requirements contract')
        requirements=json.loads(cfg.path(root,requirement_path).read_text(encoding='utf-8-sig'))
        requirement_ids={x['id'] for x in requirements.get('requirements',[])}
    for block in doc['blocks']:
        if not all(text(block.get(k)) for k in ['id','basis','requirement_id']):raise ValueError('Block needs requirement ID and basis')
        if block['id'] in block_ids or block['requirement_id'] not in requirement_ids:raise ValueError('Duplicate block or unknown requirement ID')
        block_ids.add(block['id'])
        for key in ['sensitive_nets','switching_nodes','return_paths','loops','kelvin_connections']:
            record=block.get(key)
            if not isinstance(record,dict) or not text(record.get('rationale')) or not isinstance(record.get('objects'),list) or not all(text(x) for x in record['objects']):raise ValueError('Block review card incomplete: '+key)
    if not doc['blocks'] and not text(doc.get('no_blocks_reason')):raise ValueError('Explain absence of analog/power block requirements')
    payload={'schema_version':1,'kicad_version':config['kicad_version'],'intent_digest':intent_digest(doc),
             'outline_mm':outline,'areas':doc['areas'],'blocks':doc['blocks'],
             'minimums_mm':values,'net_settings':netclasses}
    if 'copper_layers'in config.get('product',{}):payload['copper_layers']=declared
    return {'document':doc,'payload':payload,'digest':digest(payload)}


def rules(model):
    if not model:return ''
    output=''
    for cls in model['payload']['net_settings']['classes']:
        if cls['name']!='Default':
            output+='(rule "HW-NETCLASS-'+cls['name']+'" (condition "A.NetClass == \''+cls['name']+'\'") (constraint track_width (min '+str(cls['track_width'])+'mm)))\n'
    for area in model['payload']['areas']:
        name='HW-SPATIAL-'+area['id']
        condition="A.intersectsArea('"+name+"')"
        for exception in area['exceptions']:condition+=" && A.NetName != '"+exception['net']+"'"
        output+='(rule "'+name+'" (condition "'+condition+'") (constraint disallow '+' '.join(area['disallow'])+'))\n'
    return output


def python_path():
    if os.environ.get('KICAD_PYTHON'):return os.environ['KICAD_PYTHON']
    if os.name=='nt':
        p=Path('C:/Program Files/KiCad/10.0/bin/python.exe')
        if p.is_file():return str(p)
    return sys.executable


def geometry(root,config,model,propose=False):
    if config.get('kicad_version')!='10.0.6':raise ValueError('Spatial geometry validated only with KiCad 10.0.6')
    request=cfg.path(root,'.work/spatial-request.json');request.parent.mkdir(parents=True,exist_ok=True)
    request.write_text(json.dumps({'board':str(cfg.path(root,config['name']+'.kicad_pcb')),'model':model,'propose':propose}),encoding='utf-8')
    output=cfg.path(root,'.work/spatial-geometry.json');output.unlink(missing_ok=True)
    board=cfg.path(root,config['name']+'.kicad_pcb');before=board.read_bytes()
    env=os.environ.copy();env['KICAD_CONFIG_HOME']=str(request.parent/'kicad-config');env['KICAD_DOCUMENTS_HOME']=str(request.parent/'kicad-documents')
    run=subprocess.run([python_path(),str(Path(__file__).with_name('spatial_cad.py')),str(request),str(output)],env=env,capture_output=True,text=True,timeout=120)
    if run.returncode or not output.is_file():raise ValueError('Spatial CAD reader failed: '+run.stderr[-1500:])
    if board.read_bytes()!=before:raise ValueError('Board changed during spatial inspection')
    result=json.loads(output.read_text(encoding='utf-8'))
    cfg.path(root,'.work/spatial-preview.svg').write_text(result['svg'],encoding='utf-8')
    return result


def prepare(root,config,values,classes):
    model=load(root,config,values,classes)
    if not model:return {},[],None
    resolved=cfg.path(root,'.work/spatial-resolved.json');resolved.parent.mkdir(parents=True,exist_ok=True)
    resolved.write_bytes(cfg.encoded({'constraints_digest':model['digest'],'intent_digest':model['payload']['intent_digest'],'constraints':model['payload']}))
    outputs={p:cfg.encoded({'constraints_digest':model['digest'],'constraints':model['payload']}) for p in CONSUMERS.values()}
    conflicts=[]
    board=cfg.path(root,config['name']+'.kicad_pcb')
    if board.is_file():
        result=geometry(root,config,model,propose=True)
        conflicts.extend(result['errors'])
        if result.get('proposed_board') is not None:outputs[config['name']+'.kicad_pcb']=base64.b64decode(result['proposed_board'])
    return outputs,conflicts,model


def verify(root,config,values,classes):
    model=load(root,config,values,classes)
    if not model:return {'passed':False,'errors':['Spatial contract missing: adopt product.spatial_file']}
    errors=[];doc=model['document'];approval=doc.get('approval',{}) or {}
    if not all(text(approval.get(k)) for k in ['approved_by','evidence']) or approval.get('intent_digest')!=model['payload']['intent_digest']:
        errors.append('Spatial contract lacks current human approval')
    expected={'constraints_digest':model['digest'],'constraints':model['payload']}
    for role,p in CONSUMERS.items():
        try:actual=json.loads(cfg.path(root,p).read_text(encoding='utf-8-sig'))
        except (OSError,ValueError):actual=None
        if actual!=expected:errors.append(role+' consumer inputs differ from resolved DRC contract')
    result=geometry(root,config,model);errors.extend(result['errors'])
    return {'passed':not errors,'errors':errors,'constraints_digest':model['digest'],
            'intent_digest':model['payload']['intent_digest'],'geometry':result['inventory'],
            'limitations':['Consumer files verify declared inputs, not execution of an external router.',
                           'Block topology/SI/PI/EMC and physical insulation require separate evidence.']}
