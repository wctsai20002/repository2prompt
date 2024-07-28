import unittest
import os
from repository2prompt.config import load_config, CONFIG

class TestConfig(unittest.TestCase):

    def test_default_config_loaded(self):
        self.assertIn('github_api_base_url', CONFIG)
        self.assertEqual(CONFIG['github_api_base_url'], "https://api.github.com")

    def test_environment_variable_override(self):
        os.environ['GITHUB_API_TOKEN'] = 'test_token'
        config = load_config()
        self.assertEqual(config['github_api_token'], 'test_token')
        del os.environ['GITHUB_API_TOKEN']

    def test_user_config_override(self):
        # This test assumes you have a way to set a temporary user config file
        # You might need to mock this or create a temporary file for testing
        pass

if __name__ == '__main__':
    unittest.main()