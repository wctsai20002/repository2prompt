import unittest
import os
from pathlib import Path
from repository2prompt.config import load_config, _update_config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_config_path = Path('temp_config.yaml')

    def tearDown(self):
        if self.temp_config_path.exists():
            self.temp_config_path.unlink()
        if 'REPOSITORY2PROMPT_CONFIG' in os.environ:
            del os.environ['REPOSITORY2PROMPT_CONFIG']

    def test_load_config(self):
        config = load_config()
        
        self.assertIn('supported_output_formats', config)
        self.assertIn('split', config['supported_output_formats'])
        self.assertIn('split_format_prompts', config)
        self.assertIn('initial', config['split_format_prompts'])

    def test_custom_config(self):
        with open(self.temp_config_path, 'w') as f:
            f.write("""
supported_output_formats:
  - custom_format
split_format_prompts:
  initial: "Custom initial prompt"
            """)

        os.environ['REPOSITORY2PROMPT_CONFIG'] = str(self.temp_config_path)
        
        config = load_config()
        
        self.assertIn('custom_format', config['supported_output_formats'])
        self.assertIn('split', config['supported_output_formats'])
        self.assertEqual(config['split_format_prompts']['initial'], "Custom initial prompt")

    def test_update_config(self):
        base_config = {
            'a': 1,
            'b': {
                'c': 2,
                'd': 3
            },
            'list': [1, 2, 3]
        }
        new_config = {
            'b': {
                'c': 4
            },
            'e': 5,
            'list': [3, 4, 5]
        }
        _update_config(base_config, new_config)
        self.assertEqual(base_config['a'], 1)
        self.assertEqual(base_config['b']['c'], 4)
        self.assertEqual(base_config['b']['d'], 3)
        self.assertEqual(base_config['e'], 5)
        self.assertEqual(set(base_config['list']), {1, 2, 3, 4, 5})

if __name__ == '__main__':
    unittest.main()