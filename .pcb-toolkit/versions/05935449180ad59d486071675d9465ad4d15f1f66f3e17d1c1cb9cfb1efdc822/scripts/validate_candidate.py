"""Validate an extracted candidate using only its declared files and local KiCad."""
import argparse
import json
import os
import platform
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import package_toolkit as package
import spatial


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cad-python',default=spatial.python_path())
    args=parser.parse_args();os.chdir(ROOT)
    output=ROOT/'.work/package-validation';output.mkdir(parents=True,exist_ok=True)
    manifest=package.verify_tree(ROOT)
    sys.path.insert(0,str(ROOT/'tests'))
    with (output/'unit-tests.txt').open('w',encoding='utf-8') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT/'tests')))
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    records={};success=result.wasSuccessful()
    for name,script,python in [('cad','tests/integration.py',args.cad_python),
                               ('requirements-example','examples/multi-board/run_demo.py',sys.executable),
                               ('workflow-example','examples/agent-workflow/run_walkthrough.py',sys.executable),
                               ('installed-trial','tests/install_smoke.py',args.cad_python),
                               ('recipient-example','examples/connector-adapter/replay.py',sys.executable)]:
        with (output/(name+'.txt')).open('w',encoding='utf-8') as stream:
            run=subprocess.run([python,script],cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=900)
        records[name]={'exit_code':run.returncode};success=success and run.returncode==0
    actual=json.loads((ROOT/'reports/integration-results.json').read_text()) if (ROOT/'reports/integration-results.json').is_file() else None
    success=success and bool(actual and actual['passed'])
    package.verify_tree(ROOT)
    report={'schema_version':1,'passed':success,'candidate_only':True,'publication_ready':False,
            'package_version':manifest['package_version'],'ruleset_version':manifest['ruleset_version'],
            'manifest_sha256':package.sha((ROOT/package.MANIFEST).read_bytes()),
            'platform':platform.platform(),'python':sys.version,
            'unit_tests':{'run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
                          'skipped':[{'test':str(t),'reason':r} for t,r in result.skipped]},
            'commands':records,'cad':actual,'inputs_unchanged':True,
            'installed_trial':json.loads((ROOT/'.work/installed-trial/result.json').read_text()) if (ROOT/'.work/installed-trial/result.json').is_file() else None,
            'recipient_example':json.loads((ROOT/'.work/recipient-example/result.json').read_text()) if (ROOT/'.work/recipient-example/result.json').is_file() else None,
            'pending_acceptance':manifest['pending_acceptance']}
    if sys.platform=='linux':report['os_release']=platform.freedesktop_os_release()
    (output/'report.json').write_bytes(package.encoded(report))
    print(json.dumps({'passed':success,'publication_ready':False,'unit_run':result.testsRun,
                      'skipped':len(result.skipped),'cad_scenarios':len(actual['tests']) if actual else 0}))
    return 0 if success else 1


if __name__=='__main__':raise SystemExit(main())
