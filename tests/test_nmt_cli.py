import unittest
import os
import shutil
import sys
from click.testing import CliRunner

# Import the CLI from the main script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nmt_cli import cli

class TestNmtCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.test_project = 'testapp'
        # Clean up before test
        if os.path.exists(self.test_project):
            shutil.rmtree(self.test_project)

    def tearDown(self):
        # Clean up after test
        if os.path.exists(self.test_project):
            shutil.rmtree(self.test_project)

    def test_create_project(self):
        result = self.runner.invoke(cli, ['create', self.test_project])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.exists(os.path.join(self.test_project, 'lib/core/entities')))
        self.assertIn('Created NMT project', result.output)

    def test_version(self):
        result = self.runner.invoke(cli, ['version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('NmtTool version', result.output)

if __name__ == '__main__':
    unittest.main()
