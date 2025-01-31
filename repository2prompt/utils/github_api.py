import requests
import base64
import os
from ..config import CONFIG

class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors"""
    def __init__(self, message, status_code=None, response_body=None):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)

    def __str__(self):
        error_msg = f"GitHub API Error: {self.message}"
        if self.status_code:
            error_msg += f" (Status code: {self.status_code})"
        if self.response_body:
            error_msg += f"\nResponse body: {self.response_body}"
        return error_msg

def get_headers():
    """Return headers for API requests"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if CONFIG['github_api_token']:
        headers['Authorization'] = f"token {CONFIG['github_api_token']}"
    return headers

def get_default_branch(repo_url):
    """
    Get the default branch of a GitHub repository
    
    :param repo_url: URL of the GitHub repository
    :return: Name of the default branch
    """
    try:
        _, _, _, username, repo_name = repo_url.rstrip('/').split('/')
    except ValueError:
        raise GitHubAPIError(f"Invalid GitHub URL: {repo_url}")

    api_url = f"{CONFIG['github_api_base_url']}/repos/{username}/{repo_name}"
    
    try:
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        repo_data = response.json()
        return repo_data['default_branch']
    except requests.RequestException as e:
        raise GitHubAPIError(f"Error fetching repository information: {str(e)}",
                             status_code=e.response.status_code if e.response else None,
                             response_body=e.response.text if e.response else None)

def fetch_repo_content(repo_url):
    """
    Fetch the content of a GitHub repository
    
    :param repo_url: URL of the GitHub repository
    :return: List of dictionaries containing file information
    """
    try:
        _, _, _, username, repo_name = repo_url.rstrip('/').split('/')
    except ValueError:
        raise GitHubAPIError(f"Invalid GitHub URL: {repo_url}")

    # Get the default branch
    default_branch = get_default_branch(repo_url)

    api_url = f"{CONFIG['github_api_base_url']}/repos/{username}/{repo_name}/git/trees/{default_branch}?recursive=1"
    
    try:
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        tree = response.json().get('tree', [])
        
        if not tree:
            raise GitHubAPIError(f"No content found in repository: {repo_url}")
        
        files = []
        for item in tree:
            if item['type'] == 'blob' and not any(ignored in item['path'] for ignored in CONFIG['ignore_dirs'] + CONFIG['ignore_files']):
                files.append({
                    'name': os.path.basename(item['path']),
                    'path': item['path'],
                    'size': item.get('size', 0),
                    'url': item['url'],
                    'type': 'file'
                })
        
        return files
    except requests.RequestException as e:
        raise GitHubAPIError(f"Error fetching repository content: {str(e)}", 
                             status_code=e.response.status_code if e.response else None, 
                             response_body=e.response.text if e.response else None)

def fetch_file_content(file_url):
    """
    Fetch the content of a GitHub file
    
    :param file_url: API URL of the GitHub file
    :return: File content (Base64 decoded)
    """
    try:
        response = requests.get(file_url, headers=get_headers())
        response.raise_for_status()
        file_data = response.json()
        
        if file_data['encoding'] == 'base64':
            return base64.b64decode(file_data['content']).decode('utf-8')
        else:
            raise GitHubAPIError(f"Unsupported file encoding: {file_data['encoding']}")
    except requests.RequestException as e:
        raise GitHubAPIError(f"Error fetching file content: {str(e)}",
                             status_code=e.response.status_code if e.response else None,
                             response_body=e.response.text if e.response else None)

# Test code
if __name__ == "__main__":
    from ..config import CONFIG
    from .output_formatter import format_output
    
    test_repo_url = "https://github.com/octocat/Hello-World"
    try:
        repo_name = test_repo_url.split('/')[-1]
        repo_content = fetch_repo_content(test_repo_url)
        processed_files = []
        
        for item in repo_content:
            file_content = fetch_file_content(item['url'])
            processed_files.append({
                'path': item['path'],
                'content': file_content
            })
        
        # Test markdown output
        markdown_output = format_output(repo_name, processed_files, CONFIG['default_template_path'], 'markdown')
        print("Markdown Output Preview:")
        print(markdown_output[:500] + "...\n")
        
        # Test JSON output
        json_output = format_output(repo_name, processed_files, CONFIG['default_template_path'], 'json')
        print("JSON Output Preview:")
        print(json_output[:500] + "...\n")
        
        # Test text output
        text_output = format_output(repo_name, processed_files, CONFIG['default_template_path'], 'text')
        print("Text Output Preview:")
        print(text_output[:500] + "...\n")
        
    except GitHubAPIError as e:
        print(f"Error: {e}")