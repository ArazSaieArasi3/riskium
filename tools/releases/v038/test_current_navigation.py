"""Check root and .github README routing against their real render locations."""
import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('landing',ROOT/'tools/audit_reader_consistency.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class LandingRoutes(unittest.TestCase):
    def test_root_relative_link_is_invalid_in_github_readme(self):
        self.assertIsNone(m.link_error('RIGHTS.md',Path('README.md')))
        self.assertIsNotNone(m.link_error('RIGHTS.md',Path('.github/README.md')))
    def test_explicit_source_link_works_in_both_render_locations(self):
        for p in ('README.md','.github/README.md'):
            self.assertIsNone(m.link_error('https://github.com/ArazSaieArasi3/riskium/blob/main/RIGHTS.md',Path(p)))
    def test_wrong_github_subdirectory_and_escape_are_rejected(self):
        self.assertIsNotNone(m.link_error('https://github.com/ArazSaieArasi3/riskium/blob/main/.github/RIGHTS.md',Path('README.md')))
        self.assertIsNotNone(m.link_error('../../outside',Path('README.md')))
if __name__=='__main__':unittest.main()
