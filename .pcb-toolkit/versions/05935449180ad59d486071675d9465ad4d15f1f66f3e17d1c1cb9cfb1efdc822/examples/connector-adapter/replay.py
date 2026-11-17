"""Replay actual tutorial checks; no agents, approvals, network or source overwrite."""
import json
import shutil
import sys
import uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import pcb_rules as rules


def main():
    source=Path(__file__).resolve().parent/'board'
    before={p.relative_to(source).as_posix():rules.digest(p) for p in source.rglob('*') if p.is_file()}
    folder=ROOT/'.work/recipient-example'/uuid.uuid4().hex/'board'
    shutil.copytree(source,folder)
    config=rules.read(folder/'hardware.json');cli=rules.cli_path(None)
    plan=rules.configure(folder,config)
    if plan['conflicts']:raise RuntimeError(str(plan['conflicts']))
    rules.configure(folder,config,apply_plan=plan['id'])
    schematic=folder/'board.kicad_sch';correct=schematic.read_bytes()
    broken=correct.decode('utf-8')
    for y,other in [('50.8','53.34'),('53.34','50.8')]:
        old=f'(wire (pts (xy 50.8 {y}) (xy 101.6 {y}))'
        new=f'(wire (pts (xy 76.2 {y}) (xy 101.6 {other}))'
        if broken.count(old)!=1:raise RuntimeError('Intentional defect anchor changed')
        broken=broken.replace(old,new)
        # Keep the original labels on straight segments, not floating beside a diagonal.
        broken=broken.replace('(sheet_instances',f'(wire (pts (xy 50.8 {y}) (xy 76.2 {y})) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}")) (sheet_instances',1)
    schematic.write_text(broken,encoding='utf-8')
    erc_path=folder/'.work/defect-erc.json'
    command=rules.run_tool(cli,['sch','erc','--format','json','--severity-all','-o',str(erc_path),str(schematic)],folder)
    if command['exit_code']!=0 or not erc_path.is_file():raise RuntimeError('Defect ERC command failed: '+str(command))
    erc=rules.violations(rules.read(erc_path))
    defect=rules.connectivity.verify(folder,config,cli,rules.run_tool)
    rules.write(folder/'.work/defect-connectivity.json',defect)
    if erc or defect['passed'] or not any(x['type']=='split_net' for x in defect['errors']):
        raise RuntimeError('Expected clean ERC plus swapped-pin connectivity failure: '+str({'erc':erc,'connectivity':defect['errors']}))
    schematic.write_bytes(correct)
    code=rules.check(folder,config,'work',cli,stage='routing')
    work=rules.read(folder/'.work/check.json');rules.write(folder/'.work/corrected-work.json',work)
    if code!=0:raise RuntimeError('Corrected work check failed: '+str(work['errors']))
    release_code=rules.check(folder,config,'release',cli)
    release=rules.read(folder/'.work/check.json');rules.write(folder/'.work/blocked-release.json',release)
    if release_code!=1 or not any('Fabrication field missing' in x for x in release['errors']) or not any('approval' in x.lower() for x in release['errors']):
        raise RuntimeError('Expected blocked release with process and approval findings')
    views=folder/'.work/views';views.mkdir()
    commands=[]
    for args in [['sch','export','svg','-o',str(views),str(schematic)],
                 ['pcb','export','svg','--mode-single','--page-size-mode','2','--exclude-drawing-sheet','--layers','F.Cu,Edge.Cuts,F.SilkS','-o',str(views/'pcb.svg'),str(folder/'board.kicad_pcb')]]:
        run=rules.run_tool(cli,args,folder);commands.append(run)
        if run['exit_code']!=0:raise RuntimeError('View export failed: '+str(run))
    after={p.relative_to(source).as_posix():rules.digest(p) for p in source.rglob('*') if p.is_file()}
    if before!=after:raise RuntimeError('Tutorial source inputs changed')
    summary={'schema_version':1,'passed':True,'mode':'authored tutorial with executed CAD checks',
       'actual_agents_launched':0,'actual_human_approvals':0,'physical_measurements':0,
       'source_hashes':before,'work_directory':str(folder),'kicad_version':work['kicad_version'],
       'ruleset_version':work['ruleset_version'],'defect':{'erc_clean':not erc,'connectivity_passed':defect['passed'],'findings':defect['errors']},
       'corrected':{'passed':work['passed'],'snapshot':work['snapshot'],'erc_findings':len(work['erc']['findings']),'drc_findings':len(work['drc']['findings'])},
       'release':{'exit_code':release_code,'passed':release['passed'],'errors':release['errors']},
       'views':sorted(p.name for p in views.glob('*.svg')),'view_commands':commands,'source_inputs_unchanged':True,
       'limitations':['Synthetic approval fields only; no real reviewers or agents are claimed.',
                      'Fictional generic parts and process; no order, release package or physical qualification.',
                      'Real recipient/agent execution and assistance logging remain a separate pilot.']}
    rules.write(ROOT/'.work/recipient-example/result.json',summary)
    print(json.dumps({'passed':True,'erc_clean_defect_detected':True,'corrected_work_passed':True,'release_blocked':True,'work_directory':str(folder)}))
    return 0


if __name__=='__main__':raise SystemExit(main())
