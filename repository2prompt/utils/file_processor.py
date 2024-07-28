import os
from ..config import MAX_FILE_SIZE, SUPPORTED_FILE_EXTENSIONS

def is_supported_file(file_name):
    """
    Check if the file is supported based on its extension
    
    :param file_name: Name of the file
    :return: Boolean indicating if the file is supported
    """
    _, extension = os.path.splitext(file_name)
    return extension.lower() in SUPPORTED_FILE_EXTENSIONS

def is_within_size_limit(file_size):
    """
    Check if the file size is within the allowed limit
    
    :param file_size: Size of the file in bytes
    :return: Boolean indicating if the file is within size limit
    """
    return file_size <= MAX_FILE_SIZE

def process_files(repo_content):
    """
    Process and filter files from the repository content
    
    :param repo_content: List of dictionaries containing file information
    :return: List of processed and filtered file dictionaries
    """
    processed_files = []
    
    for item in repo_content:
        if item['type'] == 'file':
            if is_supported_file(item['name']) and is_within_size_limit(item['size']):
                processed_files.append({
                    'name': item['name'],
                    'path': item['path'],
                    'url': item['url'],
                    'size': item['size']
                })
    
    return processed_files

# Test code
if __name__ == "__main__":
    # Mock repository content for testing
    mock_repo_content = [
        {'name': 'readme.md', 'path': 'readme.md', 'type': 'file', 'size': 1000, 'url': 'https://api.github.com/repos/user/repo/contents/readme.md'},
        {'name': 'script.py', 'path': 'script.py', 'type': 'file', 'size': 2000, 'url': 'https://api.github.com/repos/user/repo/contents/script.py'},
        {'name': 'large_file.txt', 'path': 'large_file.txt', 'type': 'file', 'size': 2000000, 'url': 'https://api.github.com/repos/user/repo/contents/large_file.txt'},
        {'name': 'unsupported.exe', 'path': 'unsupported.exe', 'type': 'file', 'size': 1000, 'url': 'https://api.github.com/repos/user/repo/contents/unsupported.exe'},
        {'name': 'src', 'path': 'src', 'type': 'dir', 'url': 'https://api.github.com/repos/user/repo/contents/src'},
    ]

    processed_files = process_files(mock_repo_content)
    print("Processed files:")
    for file in processed_files:
        print(f"- {file['name']} (Size: {file['size']} bytes)")