import unittest
import os
from repository2prompt.utils import input_handler
from repository2prompt.config import CONFIG

class TestInputHandler(unittest.TestCase):

    def test_is_github_url(self):
        self.assertTrue(input_handler.is_github_url("https://github.com/user/repo"))
        self.assertTrue(input_handler.is_github_url("https://github.com/user/repo/"))
        self.assertFalse(input_handler.is_github_url("https://gitlab.com/user/repo"))
        self.assertFalse(input_handler.is_github_url("not a url"))

    def test_is_local_directory(self):
        self.assertTrue(input_handler.is_local_directory("."))
        self.assertFalse(input_handler.is_local_directory("nonexistent_directory"))

    def test_handle_input_github(self):
        result = input_handler.handle_input("https://github.com/user/repo")
        self.assertEqual(result, {'type': 'github_url', 'url': 'https://github.com/user/repo'})

    def test_handle_input_local(self):
        result = input_handler.handle_input(".")
        self.assertEqual(result['type'], 'local_directory')
        self.assertTrue(os.path.isabs(result['path']))

    def test_handle_input_invalid(self):
        with self.assertRaises(ValueError):
            input_handler.handle_input("invalid_input")

    def test_get_local_files(self):
        # Create a temporary directory structure for testing
        os.makedirs("test_dir/subdir", exist_ok=True)
        open("test_dir/file1.txt", "w").close()
        open("test_dir/subdir/file2.txt", "w").close()

        try:
            files = input_handler.get_local_files("test_dir")
            self.assertEqual(len(files), 2)
            self.assertTrue(any(f['name'] == 'file1.txt' for f in files))
            self.assertTrue(any(f['name'] == 'file2.txt' for f in files))
        finally:
            # Clean up
            import shutil
            shutil.rmtree("test_dir")

if __name__ == '__main__':
    unittest.main()