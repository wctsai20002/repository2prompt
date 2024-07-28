import requests
from ..config import GITHUB_API_BASE_URL, GITHUB_API_TOKEN

class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors"""
    pass

def get_headers():
    """Return headers for API requests"""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_API_TOKEN:
        headers['Authorization'] = f'token {GITHUB_API_TOKEN}'
    return headers

def fetch_repo_content(repo_url):
    """
    Fetch the content of a GitHub repository
    
    :param repo_url: URL of the GitHub repository
    :return: Dictionary containing repository files and directory information
    """
    # Extract username and repository name from the URL
    _, _, _, username, repo_name = repo_url.rstrip('/').split('/')

    api_url = f"{GITHUB_API_BASE_URL}/repos/{username}/{repo_name}/contents"
    
    try:
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise GitHubAPIError(f"Error fetching repository content: {str(e)}")

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
            import base64
            return base64.b64decode(file_data['content']).decode('utf-8')
        else:
            raise GitHubAPIError(f"Unsupported file encoding: {file_data['encoding']}")
    except requests.RequestException as e:
        raise GitHubAPIError(f"Error fetching file content: {str(e)}")

# Test code
if __name__ == "__main__":
    test_repo_url = "https://github.com/octocat/Hello-World"
    try:
        repo_content = fetch_repo_content(test_repo_url)
        print("Repository content:")
        for item in repo_content:
            print(f"- {item['name']} ({item['type']})")

        # Get content of the first file (if any)
        file_items = [item for item in repo_content if item['type'] == 'file']
        if file_items:
            file_content = fetch_file_content(file_items[0]['url'])
            print(f"\nContent of {file_items[0]['name']}:")
            print(file_content)
    except GitHubAPIError as e:
        print(f"Error: {str(e)}")