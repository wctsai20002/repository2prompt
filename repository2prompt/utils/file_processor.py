import os
from ..config import CONFIG

def is_supported_file(file_name):
    _, extension = os.path.splitext(file_name)
    return extension.lower() in CONFIG['supported_file_extensions'] and file_name not in CONFIG['ignore_files']

def is_within_size_limit(file_size):
    return file_size <= CONFIG['max_file_size']

def should_process_directory(dir_name):
    return dir_name not in CONFIG['ignore_dirs']

def process_files(repo_content, is_local=False):
    processed_files = []
    
    for item in repo_content:
        if item['type'] == 'file':
            if is_supported_file(item['name']) and is_within_size_limit(item['size']):
                processed_file = {
                    'name': item['name'],
                    'path': item['path'],
                    'size': item['size']
                }
                if is_local:
                    processed_file['full_path'] = item['full_path']
                else:
                    processed_file['url'] = item['url']
                processed_files.append(processed_file)
        elif item['type'] == 'dir' and should_process_directory(item['name']):
            # If it's a directory we want to process, we would need to fetch its contents
            # This would require additional logic for both local and GitHub cases
            pass
    
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