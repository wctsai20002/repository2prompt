import os
import re
from urllib.parse import urlparse
from ..config import CONFIG

def is_github_url(input_path):
    """
    Check if the input is a valid GitHub URL
    """
    if not isinstance(input_path, str):
        return False
    
    parsed = urlparse(input_path)
    
    # Check if it's a valid URL
    if not all([parsed.scheme, parsed.netloc]):
        return False
    
    # Check if it's a GitHub domain
    if not parsed.netloc in ['github.com', 'www.github.com']:
        return False
    
    # Check if the URL format matches GitHub repository format
    pattern = r'^/[\w.-]+/[\w.-]+/?$'
    if not re.match(pattern, parsed.path):
        return False
    
    return True

def is_local_directory(input_path):
    """
    Check if the input is a valid local directory
    """
    return os.path.isdir(input_path)

def handle_input(input_path):
    """
    Process the input and return appropriate content
    """
    if is_github_url(input_path):
        return {'type': 'github_url', 'url': input_path}
    elif is_local_directory(input_path):
        return {'type': 'local_directory', 'path': os.path.abspath(input_path)}
    else:
        raise ValueError("Invalid input. Please provide a valid GitHub URL or local directory path.")

def get_local_files(directory):
    """
    Recursively get all files in a local directory
    
    :param directory: Path to the local directory
    :return: List of dictionaries containing file information
    """
    files = []
    for root, dirs, filenames in os.walk(directory):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in CONFIG['ignore_dirs']]
        
        for filename in filenames:
            if filename not in CONFIG['ignore_files']:
                file_path = os.path.join(root, filename)
                files.append({
                    'name': filename,
                    'path': os.path.relpath(file_path, directory),
                    'full_path': file_path,
                    'size': os.path.getsize(file_path),
                    'type': 'file'
                })
    return files

# Test code
if __name__ == "__main__":
    # Test GitHub URL
    github_url = "https://github.com/user/repo"
    print(f"Is {github_url} a GitHub URL? {is_github_url(github_url)}")
    print(f"Input handler result: {handle_input(github_url)}")

    # Test local directory
    local_dir = "."  # Current directory
    print(f"Is {local_dir} a local directory? {is_local_directory(local_dir)}")
    print(f"Input handler result: {handle_input(local_dir)}")

    # Test invalid input
    invalid_input = "not_a_url_or_directory"
    try:
        handle_input(invalid_input)
    except ValueError as e:
        print(f"Error handling invalid input: {str(e)}")