import sys
import os

# Add the parent directory to the Python path to import the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repository2prompt import Repository2Prompt
from repository2prompt.config import CONFIG

def test_local_directory():
    print("Testing local directory...")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Default template path: {CONFIG['default_template_path']}")
    
    # Use the current directory as a test
    converter = Repository2Prompt(".")
    result = converter.process()
    
    if result is None:
        print("Error: result is None")
    else:
        print("Local directory test result:")
        print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\nLocal directory test completed.")

def test_github_repository():
    print("\nTesting GitHub repository...")
    # Use a small, public GitHub repository for testing
    converter = Repository2Prompt("https://github.com/octocat/octocat.github.io")
    result = converter.process()
    print("GitHub repository test result:")
    print(result[:500] + "..." if len(result) > 500 else result)
    # print(result)
    print("\nGitHub repository test completed.")

if __name__ == "__main__":
    test_local_directory()
    test_github_repository()