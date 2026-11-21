"""Actual clean-package project install/doctor/CAD/update/rollback trial."""
import json
import subprocess
import sys
import uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'tests'))
import package_toolkit as package
import install_fixture
import integration


def main():
    work=ROOT/'.work/installed-trial'/uuid.uuid4().hex;work.mkdir(parents=True)
    repo=work/'installed_board';repo.mkdir()
    c=integration.board(repo,'empty');integration.schematic(repo)
    files,_=package.collect(ROOT,package.loads((ROOT/package.RECIPE).read_bytes()))
    archive=work/'toolkit.zip';archive.write_bytes(package.archive_bytes(files));checksum=package.sha(archive.read_bytes())
    next_archive,next_sha=install_fixture.make(ROOT,work,'0.7.0-install-trial.2',True)
    results=[]
    def command(name,args):
        result=subprocess.run(args,cwd=repo,capture_output=True,text=True,timeout=180)
        results.append({'name':name,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
        if result.returncode:raise RuntimeError(name+': '+result.stdout+result.stderr)
        return result.stdout
    command('install',[sys.executable,str(ROOT/'scripts/toolkit_install.py'),'install',str(repo),'--archive',str(archive),'--sha256',checksum,'--allow-candidate'])
    wrapper=[sys.executable,str(repo/'pcb-toolkit.py')]
    doctor=json.loads(command('doctor',wrapper+['doctor']))
    preview=command('configure preview',wrapper+['run','configure','.'])
    selected=next(line.split(': ',1)[1] for line in preview.splitlines() if line.startswith('Plan: '))
    command('configure apply',wrapper+['run','configure','.','--apply',selected])
    before=command('snapshot before update',wrapper+['run','snapshot','.']).strip()
    command('work check before update',wrapper+['run','check','.','--mode','work'])
    check=package.loads((repo/'.work/check.json').read_bytes())
    assert check['toolkit']['kind']=='installed' and check['passed']
    hardware=(repo/'hardware.json').read_bytes();pcb=(repo/'board.kicad_pcb').read_bytes()
    original_lock=(repo/'.pcb-toolkit/lock.json').read_bytes()
    plan=json.loads(command('plan dependency update',wrapper+['plan-update',str(next_archive),'--sha256',next_sha,'--allow-candidate']))
    assert (repo/'.pcb-toolkit/lock.json').read_bytes()==original_lock
    update=json.loads(command('apply dependency update',wrapper+['update','--apply',plan['plan_id']]))
    after=command('snapshot after update',wrapper+['run','snapshot','.']).strip()
    assert before!=after
    command('work check after update',wrapper+['run','check','.','--mode','work'])
    command('rollback dependency',wrapper+['rollback','--to',update['rollback_to']])
    restored=command('snapshot after rollback',wrapper+['run','snapshot','.']).strip()
    assert restored==before and (repo/'.pcb-toolkit/lock.json').read_bytes()==original_lock
    assert (repo/'hardware.json').read_bytes()==hardware and (repo/'board.kicad_pcb').read_bytes()==pcb
    command('work check after rollback',wrapper+['run','check','.','--mode','work'])
    result={'schema_version':1,'passed':True,'source_archive_sha256':checksum,'doctor':doctor,'commands':results,
            'snapshot_changed_on_update':True,'rollback_restored_snapshot_and_lock':True,
            'cad_and_approval_fields_unchanged':True,
            'limitations':['Original empty-board fixture; synthetic contract approvals, no manufacturing release.',
                           'CI-equivalent commands run locally/in-container; no hosted GitHub workflow claimed.']}
    target=ROOT/'.work/installed-trial/result.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(package.encoded(result))
    print(json.dumps({'passed':True,'commands':len(results),'archive_sha256':checksum}));return 0


if __name__=='__main__':raise SystemExit(main())
