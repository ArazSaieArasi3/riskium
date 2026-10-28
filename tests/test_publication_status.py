"""Verified publication labels without rewriting frozen documentation bytes."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/publication'))
import build_publication_status as status


class PublicationStatus(unittest.TestCase):
    def test_draft_unverified_or_incomplete_publication_cannot_be_projected(self):
        original=json.loads((ROOT/status.RECEIPT).read_text())
        for key,value in [('latest_verified',False),('tag_commit_verified',False),('downloaded_bytes_match',False)]:
            receipt=copy.deepcopy(original);receipt[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):status.checked_publication(receipt)
        receipt=copy.deepcopy(original);receipt['assets'].pop()
        with self.assertRaises(ValueError):status.checked_publication(receipt)

    def test_all_maintained_headers_and_version_index_state_actual_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'site';manifest,component=status.build(output)
            self.assertEqual(component,json.loads((ROOT/status.COMPONENT).read_text()))
            self.assertEqual(len(component['projected_html_sha256']),31)
            self.assertEqual(status.base.audit(output)['frozen_snapshots'],4)
            for path in component['projected_html_sha256']:
                soup=BeautifulSoup((output/path).read_text(),'html.parser')
                self.assertIsNotNone(soup.select_one('.publication-context a[href="https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.4"]'))
            text=BeautifulSoup((output/'versions/index.html').read_text(),'html.parser').get_text(' ',strip=True)
            self.assertIn('Source distribution v0.3.4 is published',text)
            self.assertNotIn('preparation remains open',text)
            for row in manifest['releases'].values():
                for name,digest in row['files_sha256'].items():
                    self.assertEqual(status.snapshots.original.sha((output/row['route']/name).read_bytes()),digest)


if __name__=='__main__':unittest.main()
