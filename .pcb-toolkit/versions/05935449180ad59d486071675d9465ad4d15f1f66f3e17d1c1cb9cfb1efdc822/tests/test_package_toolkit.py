"""Candidate boundary, reproducibility, extraction and integrity regressions."""
import copy
import io
import json
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import package_toolkit as p


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);(self.root/'README.md').write_text('Original fixture, no project data.\n')
        data=(self.root/'README.md').read_bytes()
        self.recipe={'schema_version':1,'package_version':'0.1-candidate.1','candidate_only':True,
            'ruleset_version':'test','scope':{},'pending_acceptance':['Owner rights review'],
            'private_review_tokens':['FICTIONAL_PRIVATE_IDENTIFIER_123'],
            'files':[{'source':'README.md','path':'README.md','sha256':p.sha(data),'export_sha256':p.sha(data),
                      'origin':'original','review':'prepared-for-owner-review'}]}

    def files(self):return p.collect(self.root,self.recipe)[0]
    def archive(self,files=None):
        out=self.root/'candidate.zip';out.write_bytes(p.archive_bytes(files or self.files()));return out
    def changed(self,text):
        data=text.encode();(self.root/'README.md').write_bytes(data)
        self.recipe['files'][0].update(sha256=p.sha(data),export_sha256=p.sha(data))

    def test_repeat_build_and_ambient_private_data_do_not_change_archive(self):
        before=p.archive_bytes(self.files())
        (self.root/'data').mkdir();(self.root/'data/inventory.json').write_text('FICTIONAL_PRIVATE_IDENTIFIER_123')
        self.assertEqual(before,p.archive_bytes(self.files()))
        self.assertNotIn('data/inventory.json',p.verify_archive(self.archive())[0])

    def test_normalized_recipe_rebuilds_same_archive_without_private_sources(self):
        files=self.files();archive=self.archive(files);destination=self.root/'unpacked'
        p.extract(archive,destination)
        normalized=p.loads((destination/p.RECIPE).read_bytes())
        self.assertNotIn('private_review_tokens',normalized)
        self.assertEqual(p.archive_bytes(files),p.archive_bytes(p.collect(destination,normalized)[0]))

    def test_source_changes_and_unreviewed_files_fail(self):
        (self.root/'README.md').write_text('changed')
        with self.assertRaisesRegex(ValueError,'hash changed'):self.files()
        self.changed('reviewed bytes');self.recipe['files'][0]['review']='unreviewed'
        with self.assertRaisesRegex(ValueError,'disposition'):self.files()

    def test_private_token_and_drive_link_fail_even_with_updated_source_hash(self):
        for text in ['FICTIONAL_PRIVATE_IDENTIFIER_123','https://'+'drive'+'.google.com/file/d/fictional-id']:
            self.changed(text)
            with self.assertRaises(ValueError):self.files()

    def test_audit_json_keys_fail(self):
        data=p.encoded({'reference_drive_id':'fictional'})
        (self.root/'profile.json').write_bytes(data)
        self.recipe['files'][0].update(source='profile.json',path='profile.json',sha256=p.sha(data),export_sha256=p.sha(data))
        with self.assertRaisesRegex(ValueError,'metadata'):self.files()

    def test_paths_case_collisions_and_reserved_targets_fail(self):
        original=copy.deepcopy(self.recipe)
        for path in ['../secret','/absolute','C:/secret','data/inventory.json','x\\secret','x/.git/config','CON.txt','x.','PACKAGE-MANIFEST.json']:
            self.recipe=copy.deepcopy(original);self.recipe['files'][0]['path']=path
            with self.assertRaises(ValueError):self.files()
        self.recipe=original;other=copy.deepcopy(original['files'][0]);other['path']='readme.md';self.recipe['files'].append(other)
        with self.assertRaisesRegex(ValueError,'colliding'):self.files()

    def test_source_traversal_and_missing_source_fail(self):
        self.recipe['files'][0]['source']='../outside'
        with self.assertRaises(ValueError):self.files()
        self.recipe['files'][0]['source']='absent.md'
        with self.assertRaises(OSError):self.files()

    def test_source_symlink_refused(self):
        target=self.root/'original';target.write_text('outside recipe')
        link=self.root/'link.md'
        try:link.symlink_to(target)
        except OSError:self.skipTest('Symlink unavailable on this account')
        self.recipe['files'][0]['source']='link.md'
        with self.assertRaisesRegex(ValueError,'Symlink'):self.files()

    def test_variant_original_change_invalidates_review(self):
        original=self.root/'original.md';original.write_text('original basis')
        self.recipe['files'][0]['original']={'path':'original.md','sha256':p.sha(original.read_bytes())}
        self.files();original.write_text('changed basis')
        with self.assertRaisesRegex(ValueError,'basis changed'):self.files()

    def test_required_document_link_missing_or_escaping_fails(self):
        for text in ['[missing](docs/no.md)','[outside](../no.md)']:
            self.changed(text)
            with self.assertRaisesRegex(ValueError,'link'):self.files()

    def test_zip_tamper_missing_and_unexpected_members_fail(self):
        for action in ['edit','missing','extra']:
            files=self.files()
            if action=='edit':files['README.md']=b'tampered'
            elif action=='missing':files.pop('README.md')
            else:files['secret.txt']=b'Unexpected'
            with self.assertRaises(ValueError):p.verify_archive(self.archive(files))

    def test_zip_traversal_duplicates_and_symlink_fail(self):
        for scenario in ['traversal','duplicate','symlink']:
            path=self.root/'malicious.zip'
            with zipfile.ZipFile(path,'w') as z:
                if scenario=='traversal':z.writestr('../outside',b'bad')
                elif scenario=='duplicate':z.writestr('a',b'one');z.writestr('A',b'two')
                else:
                    info=zipfile.ZipInfo('link');info.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(info,b'outside')
            with self.assertRaises(ValueError):p.verify_archive(path)

    def test_false_release_ready_manifest_rejected(self):
        files=self.files();manifest=p.loads(files[p.MANIFEST]);manifest['publication_ready']=True
        files[p.MANIFEST]=p.encoded(manifest)
        with self.assertRaisesRegex(ValueError,'publishable'):p.verify_archive(self.archive(files))

    def test_expected_archive_hash_and_existing_extract_target(self):
        archive=self.archive()
        with self.assertRaisesRegex(ValueError,'checksum'):p.verify_archive(archive,'0'*64)
        with self.assertRaisesRegex(ValueError,'must not exist'):p.extract(archive,self.root)
        self.assertFalse((self.root/p.MANIFEST).exists())

    def test_extracted_tamper_and_unexpected_files_detected(self):
        target=self.root/'extracted';p.extract(self.archive(),target);p.verify_tree(target)
        (target/'unexpected.txt').write_text('unexpected')
        with self.assertRaisesRegex(ValueError,'Unexpected'):p.verify_tree(target)
        (target/'unexpected.txt').unlink();(target/'README.md').write_text('tampered')
        with self.assertRaisesRegex(ValueError,'Integrity'):p.verify_tree(target)

    def test_duplicate_json_key_refused(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'):p.loads('{"x":1,"x":2}')

    def test_runtime_outputs_are_ignored_but_unknown_sources_are_not(self):
        target=self.root/'with-work';p.extract(self.archive(),target)
        for folder in ['.work','reports','__pycache__']:
            out=target/folder/'deep';out.mkdir(parents=True);(out/'output.txt').write_text('Runtime only')
        p.verify_tree(target)
        (target/'unknown').mkdir();(target/'unknown/source.py').write_text('unexpected')
        with self.assertRaisesRegex(ValueError,'Unexpected'):p.verify_tree(target)

    def test_existing_output_companion_is_preserved(self):
        (self.root/'distribution').mkdir();(self.root/p.RECIPE).write_bytes(p.encoded(self.recipe))
        output=self.root/'review.zip';companion=self.root/'review.zip.sha256';companion.write_text('Existing record')
        with self.assertRaisesRegex(ValueError,'fresh'):p.build(self.root,p.RECIPE,output)
        self.assertFalse(output.exists());self.assertEqual(companion.read_text(),'Existing record')

    def test_actual_recipe_builds_without_audit_members(self):
        recipe=p.loads((ROOT/p.RECIPE).read_bytes());files,_=p.collect(ROOT,recipe)
        p.verify_manifest(files,recipe.get('private_review_tokens',[]))
        self.assertTrue(all(not name.startswith(('data/','reports/','.private/','.work/','.git/')) for name in files))
        self.assertNotIn('tests/test_pcb_count.py',files)
        self.assertIn('scripts/validate_candidate.py',files)


if __name__=='__main__':unittest.main()
