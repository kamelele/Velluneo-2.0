"""Configuration preservation, conflict and transaction behavior; no customer CAD."""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('pcb_rules',Path(__file__).resolve().parents[1]/'scripts/pcb_rules.py')
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)
c = r.configuration


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.config=r.read(r.ROOT/'templates/project/hardware.json')
        self.config.update(name='demo',source_files=['demo.kicad_pro','demo.kicad_dru','demo.kicad_sch','demo.kicad_pcb'])
        self.config['fabrication']['vendor']='jlcpcb'
        self.config['assembly']['mode']='supplier'
        r.write(self.root/'hardware.json',self.config)

    def plan(self):
        return r.configure(self.root,self.config)

    def apply(self):
        plan=self.plan()
        self.assertEqual(plan['conflicts'],[])
        return r.configure(self.root,self.config,apply_plan=plan['id'])

    def pro(self):
        return r.project_settings('demo',r.resolve(self.config)[2],self.config['netclasses'])

    def files(self):
        return {p.relative_to(self.root).as_posix():p.read_bytes()
                for p in self.root.rglob('*') if p.is_file() and '.work' not in p.parts}

    def test_preview_apply_noop_rollback_and_absent_files(self):
        before=self.files()
        p=self.plan()
        self.assertEqual(self.files(),before)
        transaction=r.configure(self.root,self.config,apply_plan=p['id'])
        applied=self.files()
        self.assertIsNone(self.apply())
        self.assertEqual(self.files(),applied)
        c.rollback(self.root,transaction)
        self.assertEqual(self.files(),before)
        c.rollback(self.root,transaction)

    def test_unrelated_settings_and_existing_bytes_preserved(self):
        pro=self.pro()
        pro.update(text_variables={'OWNER':'example'},libraries={'custom':'keep'})
        pro['board']['design_settings']['track_widths']=[0.6,1.2]
        pro['net_settings']['classes'][0]['via_diameter']=1.5
        data=json.dumps(pro,separators=(',',':')).encode()
        (self.root/'demo.kicad_pro').write_bytes(data)
        transaction=self.apply()
        self.assertEqual((self.root/'demo.kicad_pro').read_bytes(),data)
        c.rollback(self.root,transaction)
        self.assertEqual((self.root/'demo.kicad_pro').read_bytes(),data)

    def test_initial_conflict_and_stricter_existing_rule(self):
        pro=self.pro()
        pro['board']['design_settings']['rules']['min_clearance']=0.8
        r.write(self.root/'demo.kicad_pro',pro)
        before=self.files()
        plan=self.plan()
        self.assertTrue(plan['conflicts'])
        with self.assertRaises(ValueError):
            r.configure(self.root,self.config,apply_plan=plan['id'])
        self.assertEqual(before,self.files())

    def test_update_and_locally_modified_owned_field(self):
        self.apply()
        self.config['product']['minimums_mm']['clearance']=0.5
        r.write(self.root/'hardware.json',self.config)
        transaction=self.apply()
        self.assertEqual(r.read(self.root/'demo.kicad_pro')['board']['design_settings']['rules']['min_clearance'],0.5)
        c.rollback(self.root,transaction)
        pro=r.read(self.root/'demo.kicad_pro')
        pro['board']['design_settings']['rules']['min_clearance']=0.7
        r.write(self.root/'demo.kicad_pro',pro)
        self.assertTrue(self.plan()['conflicts'])

    def test_custom_rules_refused_without_writes(self):
        (self.root/'demo.kicad_dru').write_text('(version 1)\n(rule "special" (constraint clearance (min 2mm)))\n')
        before=self.files();plan=self.plan()
        self.assertTrue(any('Unfamiliar' in x for x in plan['conflicts']))
        with self.assertRaises(ValueError):
            r.configure(self.root,self.config,apply_plan=plan['id'])
        self.assertEqual(self.files(),before)

    def test_known_legacy_rules_supported(self):
        r.write(self.root/'demo.kicad_pro',self.pro())
        (self.root/'demo.kicad_dru').write_bytes(c.legacy_dru(self.pro()).replace(b'\n',b'\r\n'))
        self.apply()

    def test_duplicate_or_ambiguous_config_patterns_refused(self):
        for classes in [
            [{'name':'A','nets':['VCC']},{'name':'A','nets':['GND']}],
            [{'name':'A','nets':['VCC']},{'name':'B','nets':['VCC']}],
            [{'name':'A','nets':['*']},{'name':'B','nets':['VCC']}]]:
            self.config['netclasses']=classes
            with self.assertRaises(ValueError):self.plan()

    def test_owned_state_changes_invalidate_plan(self):
        self.apply();plan=self.plan()
        state=c.load(self.root,c.STATE);state['ruleset_version']='modified'
        r.write(self.root/c.STATE,state)
        with self.assertRaisesRegex(ValueError,'stale'):
            r.configure(self.root,self.config,apply_plan=plan['id'])

    def test_symlink_target_refused(self):
        outside=self.root.parent/(self.root.name+'-outside')
        outside.write_text('outside')
        self.addCleanup(lambda:outside.unlink(missing_ok=True))
        try:(self.root/'demo.kicad_pro').symlink_to(outside)
        except OSError:self.skipTest('Symlink creation unavailable on this Windows account')
        with self.assertRaises(ValueError):self.plan()

    def test_exclusions_preserved_and_block_adoption(self):
        pro=self.pro();pro['erc']['erc_exclusions']=['original exclusion']
        r.write(self.root/'demo.kicad_pro',pro)
        before=self.files();p=self.plan()
        self.assertTrue(any('exclusions' in x for x in p['conflicts']))
        self.assertEqual(before,self.files())

    def test_duplicate_classes_and_ambiguous_patterns_refused(self):
        pro=self.pro();pro['net_settings']['classes']*=2
        r.write(self.root/'demo.kicad_pro',pro)
        with self.assertRaises(ValueError): self.plan()
        pro=self.pro();pro['net_settings']['netclass_patterns']=[{'netclass':'Default','pattern':'*'}]
        r.write(self.root/'demo.kicad_pro',pro)
        self.assertTrue(self.plan()['conflicts'])

    def test_additional_classes_preserved_but_cannot_weaken(self):
        pro=self.pro();extra={**pro['net_settings']['classes'][0],'name':'Extra'}
        pro['net_settings']['classes'].append(extra)
        r.write(self.root/'demo.kicad_pro',pro)
        self.apply()
        self.assertEqual(r.read(self.root/'demo.kicad_pro')['net_settings']['classes'][-1],extra)
        pro['net_settings']['classes'][-1]['clearance']=0.01
        r.write(self.root/'demo.kicad_pro',pro)
        self.assertTrue(self.plan()['conflicts'])

    def test_missing_owned_field_is_local_change(self):
        self.apply();pro=r.read(self.root/'demo.kicad_pro')
        del pro['erc']['pin_map'];r.write(self.root/'demo.kicad_pro',pro)
        self.assertTrue(self.plan()['conflicts'])

    def test_stale_plan_after_source_change(self):
        p=self.plan();(self.root/'demo.kicad_sch').write_text('new source')
        with self.assertRaisesRegex(ValueError,'stale'):
            r.configure(self.root,self.config,apply_plan=p['id'])
        self.assertFalse((self.root/'demo.kicad_pro').exists())

    def test_stale_plan_after_hardware_state_or_dependency_change(self):
        for rel in ['hardware.json','demo.kicad_pcb']:
            p=self.plan();target=self.root/rel;old=target.read_bytes() if target.exists() else None
            target.write_bytes((old or b'')+b' ')
            with self.assertRaisesRegex(ValueError,'stale'):
                r.configure(self.root,self.config,apply_plan=p['id'])
            if old is None: target.unlink()
            else: target.write_bytes(old)
        p=self.plan()
        with patch.object(r,'digest',return_value='changed'):
            with self.assertRaisesRegex(ValueError,'stale'):
                r.configure(self.root,self.config,apply_plan=p['id'])

    def test_modified_saved_plan_refused(self):
        p=self.plan();file=self.root/c.WORK/'plans'/(p['id']+'.json')
        edited=copy.deepcopy(p);edited['conflicts']=['edited'];file.write_bytes(c.encoded(edited))
        with self.assertRaisesRegex(ValueError,'modified'):
            r.configure(self.root,self.config,apply_plan=p['id'])

    def test_bad_backup_or_intervening_edit_refuses_all_rollback_writes(self):
        transaction=self.apply();applied=self.files()
        record=c.load(self.root,c.WORK+'/transactions/'+transaction+'/journal.json')
        # State did not previously exist: first verify intervening edit refusal.
        target=self.root/'demo.kicad_pro';original=target.read_bytes();target.write_bytes(original+b' ')
        edited=self.files()
        with self.assertRaisesRegex(ValueError,'intervening'):
            c.rollback(self.root,transaction)
        self.assertEqual(self.files(),edited)
        target.write_bytes(original)
        # A transaction updating existing files has actual backups to corrupt.
        self.config['product']['minimums_mm']['clearance']=0.5
        r.write(self.root/'hardware.json',self.config)
        transaction=self.apply();record=c.load(self.root,c.WORK+'/transactions/'+transaction+'/journal.json')
        backup=next(item['backup'] for item in record['files'].values() if item['before'] is not None)
        (self.root/backup).write_bytes(b'corrupt')
        before=self.files()
        with self.assertRaisesRegex(ValueError,'corrupt'):
            c.rollback(self.root,transaction)
        self.assertEqual(self.files(),before)

    def test_write_failure_restores_original_bytes(self):
        before=self.files();plan=self.plan();real=c.replace
        def fail(root,relative,data):
            if relative=='demo.kicad_dru': raise OSError('injected write failure')
            return real(root,relative,data)
        with patch.object(c,'replace',side_effect=fail):
            with self.assertRaises(OSError):
                r.configure(self.root,self.config,apply_plan=plan['id'])
        self.assertEqual(self.files(),before)
        self.assertEqual(c.pending(self.root),[])

    def test_existing_files_restored_after_partial_update_failure(self):
        self.apply()
        self.config['product']['minimums_mm']['clearance']=0.5
        r.write(self.root/'hardware.json',self.config)
        before=self.files();p=self.plan();real=c.replace;failed=False
        def fail(root,relative,data):
            nonlocal failed
            if relative=='demo.kicad_dru' and not failed:
                failed=True;raise OSError('one-shot partial update failure')
            return real(root,relative,data)
        with patch.object(c,'replace',side_effect=fail):
            with self.assertRaises(OSError):r.configure(self.root,self.config,apply_plan=p['id'])
        self.assertEqual(self.files(),before)
        self.assertEqual(c.pending(self.root),[])

    def test_interrupted_rollback_can_be_retried(self):
        self.apply();before=self.files()
        self.config['product']['minimums_mm']['clearance']=0.5
        r.write(self.root/'hardware.json',self.config)
        before['hardware.json']=(self.root/'hardware.json').read_bytes()
        transaction=self.apply();real=c.replace
        def interrupt(root,relative,data):
            if relative=='demo.kicad_dru':raise KeyboardInterrupt()
            return real(root,relative,data)
        with patch.object(c,'replace',side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):c.rollback(self.root,transaction)
        self.assertIn(transaction,c.pending(self.root))
        c.rollback(self.root,transaction);self.assertEqual(self.files(),before)

    def test_concurrent_tool_invocation_refused(self):
        with c.locked(self.root):
            with self.assertRaisesRegex(ValueError,'Another'):
                with c.locked(self.root):pass

    def test_unknown_state_structure_refused(self):
        r.write(self.root/c.STATE,[])
        with self.assertRaisesRegex(ValueError,'Unsupported'):self.plan()

    def test_transient_windows_replace_lock_retries_staged_bytes(self):
        if os.name!='nt':self.skipTest('Windows sharing violation')
        real=os.replace;calls=[]
        def transient(source,target):
            calls.append(True)
            if len(calls)==1:
                error=PermissionError('transient sharing violation');error.winerror=32
                raise error
            return real(source,target)
        with patch.object(c.os,'replace',side_effect=transient):
            c.replace(self.root,'staged.txt',b'expected bytes')
        self.assertEqual((self.root/'staged.txt').read_bytes(),b'expected bytes')
        self.assertEqual(len(calls),2)

    def test_cli_init_preview_apply_rollback_and_missing_directory(self):
        project=self.root/'cli_example'
        script=r.ROOT/'scripts/pcb_rules.py'
        def command(*args):
            return subprocess.run([sys.executable,str(script),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(command('init',project,'--assembly','supplier').returncode,0)
        settings=project/'hardware.json';config=r.read(settings)
        config['product']['minimums_mm']['clearance']=0.5;r.write(settings,config)
        preview=command('configure',project);self.assertEqual(preview.returncode,0,preview.stderr)
        identifier=preview.stdout.split('Plan: ')[1].splitlines()[0]
        before=(project/'cli_example.kicad_pro').read_bytes()
        result=command('configure',project,'--apply',identifier)
        self.assertEqual(result.returncode,0,result.stderr)
        transaction=result.stdout.split('Transaction: ')[1].strip()
        self.assertNotEqual((project/'cli_example.kicad_pro').read_bytes(),before)
        self.assertEqual(command('configure',project,'--rollback',transaction).returncode,0)
        self.assertEqual((project/'cli_example.kicad_pro').read_bytes(),before)
        absent=self.root/'missing'
        self.assertEqual(command('configure',absent).returncode,2)
        self.assertFalse(absent.exists())

    def test_cli_does_not_resolve_away_unsafe_project_link(self):
        link=self.root/'linked'
        target=self.root/'target';target.mkdir()
        try:link.symlink_to(target,target_is_directory=True)
        except OSError:self.skipTest('Symlink creation unavailable')
        result=subprocess.run([sys.executable,str(r.ROOT/'scripts/pcb_rules.py'),'init',str(link)],
                              capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(list(target.iterdir()),[])

    def test_backup_failure_writes_no_sources(self):
        pro=self.pro();del pro['erc']['pin_map']
        r.write(self.root/'demo.kicad_pro',pro);p=self.plan();before=self.files();real=c.replace
        def fail(root,relative,data):
            if relative.endswith('.bak'): raise OSError('backup failure')
            return real(root,relative,data)
        with patch.object(c,'replace',side_effect=fail):
            with self.assertRaises(OSError): r.configure(self.root,self.config,apply_plan=p['id'])
        self.assertEqual(self.files(),before)

    def test_interrupted_transaction_blocks_apply_and_can_recover(self):
        before=self.files();p=self.plan();real=c.replace
        def interrupt(root,relative,data):
            if relative=='demo.kicad_dru': raise KeyboardInterrupt()
            return real(root,relative,data)
        with patch.object(c,'replace',side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt): r.configure(self.root,self.config,apply_plan=p['id'])
        transactions=c.pending(self.root);self.assertEqual(len(transactions),1)
        p=self.plan()
        with self.assertRaisesRegex(ValueError,'Unfinished'):
            r.configure(self.root,self.config,apply_plan=p['id'])
        c.rollback(self.root,transactions[0]);self.assertEqual(self.files(),before)

    def test_missing_project_and_path_escape(self):
        with self.assertRaises(ValueError): r.configure(self.root/'absent',self.config)
        self.assertFalse((self.root/'absent').exists())
        self.config['source_files'].append('../outside')
        with self.assertRaises(ValueError): self.plan()

    def test_state_tampering_cannot_make_policy_compliant(self):
        self.apply();pro=r.read(self.root/'demo.kicad_pro')
        pro['board']['design_settings']['rules']['min_clearance']=0.01
        r.write(self.root/'demo.kicad_pro',pro)
        state=c.load(self.root,c.STATE);state['managed']['board/design_settings/rules/min_clearance']=0.01
        r.write(self.root/c.STATE,state)
        self.assertTrue(c.policy_errors(pro,self.pro()))


if __name__=='__main__':
    unittest.main()
