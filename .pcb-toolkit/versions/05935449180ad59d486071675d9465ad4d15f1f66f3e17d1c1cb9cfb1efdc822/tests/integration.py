"""Actual KiCad regression fixtures, invented here; no customer geometry.
Run with KiCad's bundled Python (pcbnew) and KICAD_CLI pointing to tested binary.
"""
import copy
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import pcbnew as pcb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import pcb_rules as rules
import contract_fixture
import connectivity_fixture
import connectivity_cad
import spatial_fixture
import spatial_cases

WORK = ROOT/'.work/integration'/uuid.uuid4().hex
CLI = rules.cli_path(None)
RESULTS = []


def record(name, passed, detail=None):
    RESULTS.append({'name':name,'passed':bool(passed),'detail':detail})


def uid():
    return str(uuid.uuid4())


def mm(x, y):
    return pcb.VECTOR2I(pcb.FromMM(x), pcb.FromMM(y))


def config(folder):
    c = rules.read(ROOT/'templates/project/hardware.json')
    c.update(name='board', source_files=['board.kicad_pro','board.kicad_dru','board.kicad_pcb','board.kicad_sch'])
    c['fabrication']['vendor']='jlcpcb'
    c['assembly']['mode']='supplier'
    contract_fixture.install(folder)
    connectivity_fixture.empty(folder)
    compose(folder,c)
    return c


def compose(folder,c):
    rules.write(folder/'hardware.json',c)
    plan=rules.configure(folder,c)
    if plan['conflicts']:
        raise ValueError(plan['conflicts'])
    return rules.configure(folder,c,apply_plan=plan['id'])


def board(folder, case):
    folder.mkdir(parents=True, exist_ok=True)
    c = config(folder)
    b = pcb.BOARD()
    for start, end in [((0,0),(40,0)),((40,0),(40,40)),((40,40),(0,40)),((0,40),(0,0))]:
        shape=pcb.PCB_SHAPE(b)
        shape.SetShape(pcb.SHAPE_T_SEGMENT)
        shape.SetStart(mm(*start));shape.SetEnd(mm(*end));shape.SetLayer(pcb.Edge_Cuts)
        shape.SetWidth(pcb.FromMM(.05));b.Add(shape)
    nets=[]
    for name in ['A','B']:
        n=pcb.NETINFO_ITEM(b,name);b.Add(n);nets.append(n)
    def track(x1,y1,x2,y2,width=.4,net=0):
        t=pcb.PCB_TRACK(b);t.SetStart(mm(x1,y1));t.SetEnd(mm(x2,y2))
        t.SetWidth(pcb.FromMM(width));t.SetLayer(pcb.F_Cu);t.SetNet(nets[net]);b.Add(t)
    if case!='empty':
        # Closed track loop avoids dangling track warnings on the positive fixture.
        width=.1 if case=='width' else .4
        left=.1 if case=='edge' else 5
        for p in [(left,5,15,5),(15,5,15,15),(15,15,left,15),(left,15,left,5)]:
            track(*p,width=width)
    if case in ['short','clearance']:
        x = 14 if case=='short' else 15.5
        for p in [(x,8,25,8),(25,8,25,12),(25,12,x,12),(x,12,x,8)]:
            track(*p,net=1)
        if case=='short':
            # Tracks without pads can have their nets reconciled on load. Anchor
            # the two intentional nets to different component pins.
            for i,(x,y) in enumerate([(5,5),(25,8)]):
                fp=pcb.FOOTPRINT(b);fp.SetReference('J'+str(i+1));fp.SetPosition(mm(x,y))
                pad=pcb.PAD(fp);pad.SetNumber('1');pad.SetShape(pcb.PAD_SHAPE_CIRCLE)
                pad.SetAttribute(pcb.PAD_ATTRIB_SMD);pad.SetSize(mm(1,1));pad.SetPosition(mm(x,y))
                layers=pcb.LSET();layers.AddLayer(pcb.F_Cu)
                pad.SetLayerSet(layers);pad.SetNet(nets[i]);fp.Add(pad);b.Add(fp)
            for i in [0,1]:
                fp=pcb.FOOTPRINT(b);fp.SetReference('SHORT'+str(i));fp.SetPosition(mm(30,30))
                pad=pcb.PAD(fp);pad.SetNumber('1');pad.SetShape(pcb.PAD_SHAPE_CIRCLE)
                pad.SetAttribute(pcb.PAD_ATTRIB_SMD);pad.SetSize(mm(1,1));pad.SetPosition(mm(30,30))
                layers=pcb.LSET();layers.AddLayer(pcb.F_Cu)
                pad.SetLayerSet(layers);pad.SetNet(nets[i]);fp.Add(pad);b.Add(fp)
    if case in ['hole','ring']:
        v=pcb.PCB_VIA(b);v.SetPosition(mm(25,25));v.SetLayerPair(pcb.F_Cu,pcb.B_Cu)
        v.SetDrill(pcb.FromMM(.2 if case=='hole' else .5))
        v.SetWidth(pcb.FromMM(.8 if case=='hole' else .6));v.SetNet(nets[0]);b.Add(v)
    # SaveBoard can replace settings; fixture generation explicitly restores its
    # own prior settings. Production configure must never repair this silently.
    settings=(folder/'board.kicad_pro').read_bytes()
    pcb.SaveBoard(str(folder/'board.kicad_pcb'), b)
    (folder/'board.kicad_pro').write_bytes(settings)
    compose(folder,c)
    return c


def schematic(folder, case='empty'):
    root=uid()
    definitions=[];placed=[];wire=''
    if case!='empty':
        types = {'valid':['output','input'], 'conflict':['output','output'],
                 'power':['passive','power_in'], 'unconnected':['input','passive']}[case]
        for i, typ in enumerate(types):
            name='S'+str(i)
            body=f'''(symbol "Fixture:{name}" (pin_names (offset 0)) (in_bom yes) (on_board no)
              (property "Reference" "U" (at 0 2 0) (effects (font (size 1 1))))
              (property "Value" "{name}" (at 0 -2 0) (effects (font (size 1 1))))
              (symbol "{name}_0_1" (rectangle (start -1 -1) (end 1 1) (stroke (width 0) (type default)) (fill (type background))))
              (symbol "{name}_1_1" (pin {typ} line (at 0 0 0) (length 0)
               (name "P" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))))'''
            definitions.append(body)
            x=25.4+i*12.7
            placed.append(f'''(symbol (lib_id "Fixture:{name}") (at {x} 25.4 0) (unit 1)
              (in_bom yes) (on_board no) (dnp no) (uuid "{uid()}")
              (property "Reference" "U{i+1}" (at {x} 23 0) (effects (font (size 1 1))))
              (property "Value" "{name}" (at {x} 27 0) (effects (font (size 1 1))))
              (pin "1" (uuid "{uid()}"))
              (instances (project "board" (path "/{root}" (reference "U{i+1}") (unit 1)))))''')
        if case!='unconnected':
            wire=f'(wire (pts (xy 25.4 25.4) (xy 38.1 25.4)) (stroke (width 0) (type default)) (uuid "{uid()}"))'
        lib='(kicad_symbol_lib (version 20241209) (generator "electronics-rules") '+''.join(d.replace('Fixture:', '') for d in definitions)+')'
        (folder/'Fixture.kicad_sym').write_text(lib)
        (folder/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "Fixture") (type "KiCad") (uri "${KIPRJMOD}/Fixture.kicad_sym") (options "") (descr "")))')
    text=f'''(kicad_sch (version 20250114) (generator "electronics-rules") (uuid "{root}") (paper "A4")
       (lib_symbols {''.join(definitions)}) {wire} {''.join(placed)}
       (sheet_instances (path "/" (page "1"))))'''
    (folder/'board.kicad_sch').write_text(text)


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    for case,expected in [('valid',None),('renamed',None),('merged','merged_nets'),
                          ('split','split_net'),('wrong-pin','split_net'),
                          ('omitted-unit','unit_instance_count_mismatch'),('missing-nc','missing_nc_marker'),
                          ('connected-nc','connected_nc')]:
        folder=WORK/('connectivity-'+case)
        c=board(folder,'empty')
        connectivity_cad.write(folder,case)
        c['source_files'] += ['Connectivity.kicad_sym','sym-lib-table','basis.md']
        rules.write(folder/'hardware.json',c)
        report=rules.connectivity.verify(folder,c,CLI,rules.run_tool)
        kinds={item['type'] for item in report['errors']}
        record('connectivity '+case,report['passed'] if expected is None else expected in kinds,sorted(kinds))
        if case=='merged':
            code=rules.check(folder,c,'work',CLI,stage='schematic')
            whole=rules.read(folder/'.work/check.json')
            clean_erc=not whole.get('erc',{}).get('findings',[{'missing':'report'}])
            clean_drc=not whole.get('drc',{}).get('findings',[{'missing':'report'}])
            record('connectivity mismatch cannot be hidden by clean ERC parity DRC',
                   code!=0 and clean_erc and clean_drc and
                   any(item['type']=='merged_nets' for item in whole.get('connectivity',{}).get('errors',[])),
                   {'erc_clean':clean_erc,'drc_parity_clean':clean_drc,'errors':whole['errors']})
    for case, expected in [('valid',None),('short','shorting_items'),('clearance','clearance'),
                           ('width','track_width'),('hole','drill_out_of_range'),
                           ('ring','annular_width'),('edge','copper_edge_clearance')]:
        folder=WORK/('drc-'+case)
        board(folder,case)
        output=folder/'drc.json'
        result=rules.run_tool(CLI,['pcb','drc','--format','json','--severity-all','-o',str(output),str(folder/'board.kicad_pcb')],folder)
        fs=rules.violations(rules.read(output)) if output.exists() else []
        types={f.get('type') for f in fs}
        record('DRC '+case, expected in types if expected else not fs, sorted(str(t) for t in types))
    for case, expected in [('valid',None),('conflict','pin_to_pin'),('power','power_pin_not_driven'),('unconnected','pin_not_connected')]:
        folder=WORK/('erc-'+case)
        folder.mkdir(exist_ok=True);config(folder);schematic(folder,case)
        output=folder/'erc.json'
        rules.run_tool(CLI,['sch','erc','--format','json','--severity-all','-o',str(output),str(folder/'board.kicad_sch')],folder)
        fs=rules.violations(rules.read(output)) if output.exists() else []
        types={f.get('type') for f in fs}
        record('ERC '+case, expected in types if expected else output.exists() and not fs, sorted(str(t) for t in types))
    for scenario, custom, expected in [
        ('scope-applies', '(rule "tight" (condition "A.NetName == \'A\'") (constraint track_width (min 0.6mm)))', True),
        ('scope-other-net', '(rule "tight" (condition "A.NetName == \'B\'") (constraint track_width (min 0.6mm)))', False),
        ('priority-local', '(rule "tight" (condition "A.NetName == \'A\'") (constraint track_width (min 0.6mm)))\n(rule "local" (condition "A.NetName == \'A\'") (constraint track_width (min 0.3mm)))', False)]:
        folder=WORK/scenario;board(folder,'valid')
        with (folder/'board.kicad_dru').open('a') as stream:stream.write(custom+'\n')
        output=folder/'drc.json'
        rules.run_tool(CLI,['pcb','drc','--format','json','--severity-all','-o',str(output),str(folder/'board.kicad_pcb')],folder)
        fs=rules.violations(rules.read(output))
        record('DRC '+scenario, ('track_width' in {f.get('type') for f in fs})==expected)
    for vendor in ['jlcpcb','eurocircuits']:
        for assembly in ['supplier','inhouse']:
            folder=WORK/(vendor+'-'+assembly)
            c=board(folder,'empty');schematic(folder)
            c['fabrication']['vendor']=vendor;c['assembly']['mode']=assembly
            compose(folder,c)
            code=rules.check(folder,c,'release',CLI)
            report=rules.read(folder/'.work/check.json')
            record('release incomplete '+vendor+'/'+assembly,code!=0 and any('approval' in e for e in report['errors']),report['errors'])
    folder=WORK/'release-synthetic'
    c=board(folder,'empty');schematic(folder)
    spatial_fixture.install(folder,c);compose(folder,c)
    c['fabrication'].update(service='FR4-2L-1oz-routed',stackup='test-only',copper='1oz',finish='ENIG',confirmation_evidence='synthetic-test')
    c['assembly']['confirmation_evidence']='synthetic-test'
    c['product'].update(domains=[{'name':'test','voltage':3.3}],requirements=[{'id':'TEST','method':'review','evidence':'synthetic-test','verified_by':'test-human'}])
    current,_=rules.snapshot(folder,c)
    c['approvals']={s:{'approved_by':'test-human','evidence':'synthetic-test-not-real-approval','snapshot':current} for s in rules.STAGES}
    for kind in ['gerbers','drills','bom','positions','assembly_drawing','bringup_plan']:
        artifact=folder/(kind+'.test-only');artifact.write_text('Synthetic acceptance fixture; never manufacture.\n')
        c['release_files'][kind]=[{'path':artifact.name,'sha256':rules.digest(artifact),'snapshot':current}]
    # release_files are design configuration and must be bound; artifact snapshots
    # cannot recursively be included in the design snapshot (tested here).
    current,_=rules.snapshot(folder,c)
    for approval in c['approvals'].values():approval['snapshot']=current
    for entries in c['release_files'].values():
        for entry in entries:entry['snapshot']=current
    c['approvals']['release']['artifacts_digest']=rules.hashlib.sha256(json.dumps(c['release_files'],sort_keys=True).encode()).hexdigest()
    code=rules.check(folder,c,'release',CLI)
    record('release complete synthetic manifest',code==0,rules.read(folder/'.work/check.json')['errors'])
    # Exercise the real release path, not just presence of a template field.
    # The obsolete draft key is an intentional negative input, not an API alias.
    for case,fields,expected in [
        ('missing',{},False),
        ('obsolete draft key only',{'wojtek_confirmation':'synthetic-test'},False),
        ('canonical field',{'local_pcba_provider_confirmation':'synthetic-test-not-real-provider-confirmation'},True)]:
        local=copy.deepcopy(c)
        local['assembly']['mode']='inhouse'
        local['assembly'].pop('local_pcba_provider_confirmation',None)
        local['assembly'].update(fields)
        local_snapshot,_=rules.snapshot(folder,local)
        for approval in local['approvals'].values():approval['snapshot']=local_snapshot
        for entries in local['release_files'].values():
            for entry in entries:entry['snapshot']=local_snapshot
        local['approvals']['release']['artifacts_digest']=rules.hashlib.sha256(json.dumps(local['release_files'],sort_keys=True).encode()).hexdigest()
        local_code=rules.check(folder,local,'release',CLI)
        errors=rules.read(folder/'.work/check.json')['errors']
        missing=any('assembly.local_pcba_provider_confirmation' in e for e in errors)
        record('local PCBA confirmation '+case,
               local_code==0 and not missing if expected else local_code==1 and missing,errors)
    original_spatial=rules.read(folder/'spatial-constraints.json');changed_spatial=copy.deepcopy(original_spatial)
    changed_spatial['revision']='unapproved-change';rules.write(folder/'spatial-constraints.json',changed_spatial)
    code=rules.check(folder,c,'release',CLI)
    record('release refuses stale spatial approval',code!=0 and any('Spatial:' in e for e in rules.read(folder/'.work/check.json')['errors']))
    rules.write(folder/'spatial-constraints.json',original_spatial)
    missing_spatial=copy.deepcopy(c);missing_spatial['product'].pop('spatial_file')
    code=rules.check(folder,missing_spatial,'release',CLI)
    record('release refuses undeclared spatial contract',code!=0 and any('Spatial contract missing' in e for e in rules.read(folder/'.work/check.json')['errors']))
    intent=rules.read(folder/'intended-connectivity.json')
    unapproved=copy.deepcopy(intent);unapproved['revision']='2'
    rules.write(folder/'intended-connectivity.json',unapproved)
    code=rules.check(folder,c,'release',CLI)
    record('release refuses stale independent intent approval',code!=0 and
           any('missing_stale_intent_approval' in e for e in rules.read(folder/'.work/check.json')['errors']))
    rules.write(folder/'intended-connectivity.json',intent)
    no_intent=copy.deepcopy(c);no_intent['product'].pop('connectivity_file')
    code=rules.check(folder,no_intent,'release',CLI)
    record('release refuses undeclared independent connectivity',code!=0 and
           any('Connectivity intent missing' in e for e in rules.read(folder/'.work/check.json')['errors']))
    original_contract=rules.read(folder/'requirements.json')
    changed=copy.deepcopy(original_contract)
    changed['requirements'][0]['acceptance']='A changed product criterion without new verification'
    rules.write(folder/'requirements.json',changed)
    code=rules.check(folder,c,'release',CLI)
    record('release refuses stale contract evidence',code!=0 and
           any('different intent' in e for e in rules.read(folder/'.work/check.json')['errors']))
    rules.write(folder/'requirements.json',original_contract)
    legacy=copy.deepcopy(c);legacy['product'].pop('requirements_file')
    code=rules.check(folder,legacy,'release',CLI)
    record('release refuses missing contract declaration',code!=0 and
           any('Requirements contract missing' in e for e in rules.read(folder/'.work/check.json')['errors']))
    # Work mode cannot silently omit an existing contract by deleting its pointer.
    code=rules.check(folder,legacy,'work',CLI)
    record('legacy work report identifies unconfigured requirements',
           rules.read(folder/'.work/check.json').get('requirements',{}).get('release_blocked') is True)
    with (folder/'board.kicad_sch').open('a') as stream:stream.write('\n')
    code=rules.check(folder,c,'release',CLI)
    record('release stale approvals refused',code!=0 and any('stale user approval' in e for e in rules.read(folder/'.work/check.json')['errors']))
    code=rules.check(folder,c,'work',str(folder/'missing-kicad-cli'))
    record('missing CAD tool fails closed',code==2 and not rules.read(folder/'.work/check.json')['passed'])

    # An existing original project with unrelated settings and no adoption state.
    folder=WORK/'existing-project-adoption'
    c=board(folder,'empty');schematic(folder)
    (folder/rules.configuration.STATE).unlink()
    pro=rules.read(folder/'board.kicad_pro')
    pro['text_variables']={'ASSEMBLY_NOTE':'Preserve original project settings'}
    pro['board']['design_settings']['track_widths']=[0.6,1.2]
    pro['net_settings']['classes'][0]['via_diameter']=1.5
    rules.write(folder/'board.kicad_pro',pro)
    original={p.name:p.read_bytes() for p in folder.glob('board.kicad_*')}
    plan=rules.configure(folder,c)
    record('adoption preview leaves existing CAD unchanged',not plan['conflicts'] and
           all((folder/name).read_bytes()==data for name,data in original.items()))
    transaction=rules.configure(folder,c,apply_plan=plan['id'])
    record('adoption preserves unrelated KiCad settings',rules.read(folder/'board.kicad_pro')==pro)
    code=rules.check(folder,c,'work',CLI)
    record('adopted existing project passes real ERC DRC parity',code==0,rules.read(folder/'.work/check.json')['errors'])
    current,_=rules.snapshot(folder,c)
    record('repeat adoption is a source no-op',compose(folder,c) is None and rules.snapshot(folder,c)[0]==current)
    rules.configuration.rollback(folder,transaction)
    record('adoption rollback restores exact original CAD bytes',
           all((folder/name).read_bytes()==data for name,data in original.items()) and not (folder/rules.configuration.STATE).exists())
    folder=WORK/'blocked-baseline';c=board(folder,'width');schematic(folder)
    with (folder/'board.kicad_dru').open('a') as stream:
        stream.write('(rule "external" (constraint clearance (min 0.3mm)))\n')
    code=rules.check(folder,c,'work',CLI)
    baseline=rules.read(folder/'.work/check.json')
    record('blocked adoption still reports actual CAD violations',code!=0 and
           any('Custom rules' in e for e in baseline['errors']) and
           any(f.get('type')=='track_width' for f in baseline.get('drc',{}).get('findings',[])))
    folder=WORK/'managed-tampering';c=board(folder,'empty');schematic(folder)
    pro=rules.read(folder/'board.kicad_pro');pro['erc']['pin_map'][1][1]=0
    rules.write(folder/'board.kicad_pro',pro)
    code=rules.check(folder,c,'work',CLI)
    record('managed ERC policy tampering refused',code!=0 and any('erc/pin_map' in e for e in rules.read(folder/'.work/check.json')['errors']))
    spatial_cases.run(WORK,board,schematic,compose,record)
    rules.write(ROOT/'reports/integration-results.json',{'kicad_version':'10.0.6','tests':RESULTS,'passed':all(r['passed'] for r in RESULTS)})
    for result in RESULTS:
        print(('PASS ' if result['passed'] else 'FAIL ')+result['name']+': '+str(result['detail']))
    return 0 if all(r['passed'] for r in RESULTS) else 1


if __name__=='__main__':
    raise SystemExit(main())
