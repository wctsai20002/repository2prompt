import unittest
import json
import os
from pathlib import Path
from repository2prompt.utils import output_formatter
from repository2prompt.config import CONFIG

class TestOutputFormatter(unittest.TestCase):
    def setUp(self):
        self.repo_name = "test-repo"
        self.processed_files = [
            {
                "path": "file1.py",
                "content": "print('Hello, World!')"
            },
            {
                "path": "dir/file2.py",
                "content": "def greet():\n    return 'Hello!'"
            }
        ]
        package_root = Path(__file__).parent.parent
        self.template_path = str(package_root / "repository2prompt" / "templates" / "default_template.j2")
        
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template file not found: {self.template_path}")

    def test_markdown_format(self):
        result = output_formatter.format_output(self.repo_name, self.processed_files, self.template_path, 'markdown')
        self.assertIn(self.repo_name, result)
        self.assertIn("file1.py", result)
        self.assertIn("dir/file2.py", result)

    def test_json_format(self):
        result = output_formatter.format_output(self.repo_name, self.processed_files, self.template_path, 'json')
        json_result = json.loads(result)
        self.assertEqual(json_result["repository_name"], self.repo_name)
        self.assertEqual(len(json_result["codes"]), 2)

    def test_text_format(self):
        result = output_formatter.format_output(self.repo_name, self.processed_files, self.template_path, 'text')
        self.assertIn(self.repo_name, result)
        self.assertIn("file1.py", result)
        self.assertIn("dir/file2.py", result)

    def test_split_format(self):
        result = output_formatter.format_output(self.repo_name, self.processed_files, self.template_path, 'split')
        split_result = json.loads(result)
        
        self.assertIsInstance(split_result, list)
        self.assertGreater(len(split_result), 3)  # At least initial, file tree, and final messages
        
        self.assertIn(CONFIG['split_format_prompts']['initial'].replace(r'{final}', ''), split_result[0]["prompt"])
        self.assertIn(self.repo_name, split_result[0]["content"])
        
        self.assertEqual(split_result[1]["prompt"], CONFIG['split_format_prompts']['file_tree'])
        
        for item in split_result[2:-1]:
            self.assertIn("Here is the code for the file at", item["prompt"])
        
        self.assertEqual(split_result[-1]["prompt"], CONFIG['split_format_prompts']['final'])
        self.assertIn(str(len(self.processed_files)), split_result[-1]["content"])

    def test_unsupported_format(self):
        with self.assertRaises(ValueError):
            output_formatter.format_output(self.repo_name, self.processed_files, self.template_path, 'unsupported')

if __name__ == '__main__':
    unittest.main()