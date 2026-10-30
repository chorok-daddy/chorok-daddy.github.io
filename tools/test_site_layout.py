import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import site_layout as layout
class OutputOwnershipTests(unittest.TestCase):
    def test_stale_output_removed_but_imports_and_untracked_drafts_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'tools').mkdir()
            paths=['niil/members/index.html','niil/ko/old/index.html','niil/courses/control-1/assignment.html','niil/draft/index.html']
            for name in paths:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(name)
            (root/'tools/site-output.json').write_text(json.dumps({'html':[paths[0],paths[1]]}))
            with patch.object(layout,'ROOT',root),patch.object(layout,'SITE',root/'niil'):layout.finish({paths[0]})
            self.assertFalse((root/paths[1]).exists())
            for name in [paths[0],paths[2],paths[3]]:self.assertTrue((root/name).is_file())
            self.assertEqual(json.loads((root/'tools/site-output.json').read_text()),{'html':[paths[0]]})
    def test_course_and_asset_ownership_boundaries(self):
        for name in ['niil/courses/index.html','niil/en/courses/reuse.html','niil/pages/profile/index.html']:self.assertTrue(layout.owns(name))
        for name in ['niil/courses/control-1/index.html','niil/en/courses/control-1/lesson.preview.html','niil/assets/tool.html','courses/index.html']:self.assertFalse(layout.owns(name))
if __name__=='__main__':unittest.main()
