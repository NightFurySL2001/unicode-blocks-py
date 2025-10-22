import tomllib
import unittest

class TestVersion(unittest.TestCase):
    def test_version_matches_pyproject(self):
        # Load version from pyproject.toml
        with open("pyproject.toml", "rb") as f:
            pyproject_data = tomllib.load(f)
        pyproject_version = pyproject_data["project"]["version"]

        # Import the unicode_blocks module and get its __version__ variable
        import unicode_blocks

        module_version = unicode_blocks.__version__

        # Assert that both versions match
        self.assertEqual(module_version, pyproject_version)