import unittest
from unittest.mock import patch, Mock
from repository2prompt.utils import github_api
from repository2prompt.utils.github_api import GitHubAPIError
from repository2prompt.config import CONFIG

class TestGitHubAPI(unittest.TestCase):

    @patch('requests.get')
    def test_get_default_branch(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'default_branch': 'main'
        }
        mock_get.return_value = mock_response

        result = github_api.get_default_branch('https://github.com/user/repo')
        
        self.assertEqual(result, 'main')

    @patch('repository2prompt.utils.github_api.get_default_branch')
    @patch('requests.get')
    def test_fetch_repo_content(self, mock_get, mock_get_default_branch):
        # Mock the default branch
        mock_get_default_branch.return_value = 'main'

        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'tree': [
                {'path': 'file1.txt', 'type': 'blob', 'url': 'https://api.github.com/repos/user/repo/git/blobs/sha1'},
                {'path': 'file2.py', 'type': 'blob', 'url': 'https://api.github.com/repos/user/repo/git/blobs/sha2'},
                {'path': '.gitignore', 'type': 'blob', 'url': 'https://api.github.com/repos/user/repo/git/blobs/sha3'}
            ]
        }
        mock_get.return_value = mock_response

        result = github_api.fetch_repo_content('https://github.com/user/repo')
        
        self.assertEqual(len(result), 2)  # .gitignore should be ignored
        self.assertEqual(result[0]['name'], 'file1.txt')
        self.assertEqual(result[1]['name'], 'file2.py')

    @patch('requests.get')
    def test_fetch_file_content(self, mock_get):
        # Mock the API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'content': 'SGVsbG8gV29ybGQ=',  # Base64 for "Hello World"
            'encoding': 'base64'
        }
        mock_get.return_value = mock_response

        result = github_api.fetch_file_content('https://api.github.com/repos/user/repo/git/blobs/sha1')
        
        self.assertEqual(result, 'Hello World')

    @patch('repository2prompt.utils.github_api.get_default_branch')
    def test_github_api_error(self, mock_get_default_branch):
        # Mock get_default_branch to raise an exception
        mock_get_default_branch.side_effect = GitHubAPIError("API Error")

        with self.assertRaises(GitHubAPIError):
            github_api.fetch_repo_content('https://github.com/user/repo')

if __name__ == '__main__':
    unittest.main()