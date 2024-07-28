import unittest
from unittest.mock import patch, MagicMock
from repository2prompt import Repository2Prompt
from repository2prompt.utils import github_api, input_handler, output_formatter

class TestRepository2Prompt(unittest.TestCase):
    @patch('repository2prompt.utils.github_api.fetch_repo_content')
    @patch('repository2prompt.utils.github_api.fetch_file_content')
    @patch('repository2prompt.utils.output_formatter.format_output')
    def test_process_github_repo(self, mock_format_output, mock_fetch_file, mock_fetch_repo):
        mock_fetch_repo.return_value = [
            {'name': 'file1.py', 'path': 'file1.py', 'url': 'http://api.github.com/repos/test/file1.py', 'type': 'file', 'size': 100},
            {'name': 'file2.py', 'path': 'file2.py', 'url': 'http://api.github.com/repos/test/file2.py', 'type': 'file', 'size': 200}
        ]
        mock_fetch_file.side_effect = ['content of file1', 'content of file2']
        mock_format_output.return_value = "Formatted output"

        converter = Repository2Prompt("https://github.com/test/repo", output_format="markdown")
        result = converter.process()

        self.assertIsNotNone(result, "Result should not be None")
        self.assertEqual(result, "Formatted output")
        
        mock_fetch_repo.assert_called_once()
        self.assertEqual(mock_fetch_file.call_count, 2)
        mock_format_output.assert_called_once()

    @patch('repository2prompt.utils.input_handler.get_local_files')
    @patch('builtins.open', unittest.mock.mock_open(read_data='file content'))
    @patch('repository2prompt.utils.output_formatter.format_output')
    def test_process_local_directory(self, mock_format_output, mock_get_local_files):
        mock_get_local_files.return_value = [
            {'name': 'file1.py', 'path': 'file1.py', 'full_path': '/path/to/file1.py', 'type': 'file', 'size': 100},
            {'name': 'file2.py', 'path': 'file2.py', 'full_path': '/path/to/file2.py', 'type': 'file', 'size': 200}
        ]
        mock_format_output.return_value = "Formatted output"

        converter = Repository2Prompt(".", output_format="json")
        result = converter.process()

        self.assertIsNotNone(result, "Result should not be None")
        self.assertEqual(result, "Formatted output")
        
        mock_get_local_files.assert_called_once()
        mock_format_output.assert_called_once()

    def test_process_error_handling(self):
        with patch('repository2prompt.utils.github_api.fetch_repo_content', side_effect=Exception("Test error")):
            converter = Repository2Prompt("https://github.com/test/repo")
            result = converter.process()
            self.assertIsNone(result, "Result should be None when an error occurs")

    def test_invalid_input(self):
        converter = Repository2Prompt("invalid_input")
        result = converter.process()
        self.assertIsNone(result, "Result should be None for invalid input")

if __name__ == '__main__':
    unittest.main()