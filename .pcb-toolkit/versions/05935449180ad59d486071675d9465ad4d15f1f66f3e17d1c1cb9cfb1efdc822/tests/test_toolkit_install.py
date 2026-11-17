import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import toolkit_install as install
import package_toolkit as package
import install_fixture


class InstallationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources=tempfile.TemporaryDirectory()
        path=Path(cls.sources.name)
        cls.old,cls.oldsha=install_fixture.make(ROOT,path,'0.7-fixture.1')
        cls.new,cls.newsha=install_fixture.make(ROOT,path,'0.7-fixture.2',True)
        cls.reused,cls.reusedsha=install_fixture.make(ROOT,path/'reuse','0.7-fixture.1',True)
    @classmethod
    def tearDownClass(cls):cls.sources.cleanup()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.repo=Path(self.temp.name)/'board_project';self.repo.mkdir()
    def activate(self):return install.install(self.repo,self.old,self.oldsha,True)
    def command(self,*args,root=None):
        root=root or self.repo
        return subprocess.run([sys.executable,str(root/'pcb-toolkit.py'),*map(str,args)],cwd=root,capture_output=True,text=True,timeout=90)
    def project(self):
        self.activate();result=self.command('run','init','.')
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        for suffix in ['.kicad_sch','.kicad_pcb']:(self.repo/(self.repo.name+suffix)).write_text('Synthetic snapshot test, not CAD validity')
    def snapshot(self):
        result=self.command('run','snapshot','.')
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        return result.stdout.strip().splitlines()[-1]

    def test_install_pin_and_wrapper_status(self):
        self.activate();result=self.command('status');self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(json.loads(result.stdout)['pin']['archive_sha256'],self.oldsha)
        self.assertTrue((self.repo/'.pcb-toolkit/.gitignore').is_file())

    def test_checksum_and_candidate_consent_required(self):
        with self.assertRaises(ValueError):install.install(self.repo,self.old,'0'*64,True)
        with self.assertRaisesRegex(ValueError,'allow-candidate'):install.install(self.repo,self.old,self.oldsha)
        self.assertFalse((self.repo/install.LOCK).exists())

    def test_existing_launcher_or_namespace_preserved(self):
        wrapper=self.repo/'pcb-toolkit.py';wrapper.write_text('User-owned launcher')
        with self.assertRaisesRegex(ValueError,'preserved'):self.activate()
        self.assertEqual(wrapper.read_text(),'User-owned launcher');wrapper.unlink()
        (self.repo/'.pcb-toolkit').mkdir()
        with self.assertRaisesRegex(ValueError,'unowned'):self.activate()

    def test_noop_preserves_lock_bytes(self):
        self.activate();before=(self.repo/install.LOCK).read_bytes()
        plan=install.plan_update(self.repo,self.old,self.oldsha,True)
        self.assertFalse(install.update(self.repo,plan['plan_id'])['changed'])
        self.assertEqual(before,(self.repo/install.LOCK).read_bytes())

    def test_update_changes_snapshot_and_rollback_restores_exact_lock(self):
        self.project();before=(self.repo/install.LOCK).read_bytes();snapshot=self.snapshot()
        config_before=(self.repo/'hardware.json').read_bytes()
        plan=install.plan_update(self.repo,self.new,self.newsha,True)
        self.assertEqual(plan['before']['archive_sha256'],self.oldsha)
        self.assertTrue(any(x['path']=='README.md' for x in plan['differences']))
        self.assertEqual(before,(self.repo/install.LOCK).read_bytes())
        result=install.update(self.repo,plan['plan_id'])
        self.assertNotEqual(snapshot,self.snapshot())
        self.assertEqual(config_before,(self.repo/'hardware.json').read_bytes())
        install.rollback(self.repo,result['rollback_to'])
        self.assertEqual(before,(self.repo/install.LOCK).read_bytes());self.assertEqual(snapshot,self.snapshot())

    def test_old_configure_plan_refused_after_dependency_update(self):
        self.project();preview=self.command('run','configure','.')
        self.assertEqual(preview.returncode,0,preview.stdout+preview.stderr)
        selected=next(x.split(': ',1)[1] for x in preview.stdout.splitlines() if x.startswith('Plan: '))
        plan=install.plan_update(self.repo,self.new,self.newsha,True);install.update(self.repo,plan['plan_id'])
        result=self.command('run','configure','.','--apply',selected)
        self.assertEqual(result.returncode,2,result.stdout)

    def test_modified_or_stale_update_plan_refused(self):
        self.activate();plan=install.plan_update(self.repo,self.new,self.newsha,True)
        path=self.repo/'.work/toolkit-updates'/(plan['plan_id']+'.json');payload=package.loads(path.read_bytes())
        payload['impact']='tampered';path.write_bytes(package.encoded(payload))
        with self.assertRaisesRegex(ValueError,'Stale or modified'):install.update(self.repo,plan['plan_id'])
        plan=install.plan_update(self.repo,self.new,self.newsha,True);install.update(self.repo,plan['plan_id'])
        with self.assertRaisesRegex(ValueError,'Stale'):install.update(self.repo,plan['plan_id'])

    def test_version_reuse_with_other_contents_refused(self):
        self.activate()
        with self.assertRaisesRegex(ValueError,'Version reuse'):install.plan_update(self.repo,self.reused,self.reusedsha,True)

    def test_tampered_dependency_refused_before_dispatch(self):
        self.activate();_,folder,_=install.current(self.repo)
        (folder/'scripts/pcb_rules.py').write_text('raise RuntimeError("Must never execute")')
        result=self.command('status')
        self.assertEqual(result.returncode,2);self.assertIn('Pinned file differs',result.stdout)

    def test_corrupted_history_refused_without_lock_change(self):
        self.activate();plan=install.plan_update(self.repo,self.new,self.newsha,True);result=install.update(self.repo,plan['plan_id'])
        before=(self.repo/install.LOCK).read_bytes()
        (self.repo/'.pcb-toolkit/history'/(result['rollback_to']+'.json')).write_text('{}')
        with self.assertRaisesRegex(ValueError,'checksum'):install.rollback(self.repo,result['rollback_to'])
        self.assertEqual(before,(self.repo/install.LOCK).read_bytes())

    def test_flat_project_discovery_ignores_dependency_example(self):
        self.project();self.assertEqual(len(self.snapshot()),64)
        result=self.command('run','configure','.')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_wrong_backend_and_outside_project_refused(self):
        self.project();_,folder,_=install.current(self.repo)
        direct=subprocess.run([sys.executable,str(folder/'scripts/pcb_rules.py'),'snapshot',str(self.repo)],capture_output=True,text=True)
        self.assertEqual(direct.returncode,2);self.assertIn('pcb-toolkit.py',direct.stderr)
        result=self.command('run','snapshot','../outside');self.assertEqual(result.returncode,2)
        result=self.command('run','snapshot','.pcb-toolkit');self.assertEqual(result.returncode,2)

    def test_missing_tools_doctor_writes_failure(self):
        self.activate();report=install.doctor(self.repo,cli='nonexistent-kicad-fixture')
        self.assertFalse(report['passed']);self.assertTrue(report['configuration_error'])
        self.assertFalse(package.loads((self.repo/'.work/toolkit-doctor.json').read_bytes())['passed'])

    def test_missing_owned_lock_is_not_unpinned_fallback(self):
        self.activate();(self.repo/install.LOCK).unlink()
        with self.assertRaises((OSError,ValueError)):install.identity(self.repo,ROOT)

    def test_wrong_protocol_type_and_ruleset_metadata_refused(self):
        files,_=package.verify_archive(self.old)
        for key,value in [('protocol',True),('ruleset','invented-version')]:
            changed=dict(files);manifest=package.loads(files[package.MANIFEST])
            if key=='protocol':manifest['scope']['installer_protocol']=value
            else:manifest['ruleset_version']=value
            changed[package.MANIFEST]=package.encoded(manifest)
            archive=self.repo/(key+'.zip');archive.write_bytes(package.archive_bytes(changed))
            with self.assertRaises(ValueError):install.select(archive,package.sha(archive.read_bytes()),True)

    def test_concurrent_command_lock_refused(self):
        self.activate()
        with install.using(self.repo):
            with self.assertRaisesRegex(ValueError,'Another'): 
                with install.using(self.repo):pass

    def test_project_is_portable_without_archive_or_external_source(self):
        self.project();before=self.snapshot();clone=Path(self.temp.name)/'relocated'
        shutil.copytree(self.repo,clone,ignore=shutil.ignore_patterns('.work','__pycache__'))
        result=self.command('run','snapshot','.',root=clone)
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        self.assertEqual(before,result.stdout.strip().splitlines()[-1])


if __name__=='__main__':unittest.main()
