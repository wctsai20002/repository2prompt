import sys
import os

# Add the parent directory to the Python path to import the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repository2prompt import Repository2Prompt

def test_local_directory():
    print("Testing local directory...")
    # Use the current directory as a test
    converter = Repository2Prompt(".")
    result = converter.process()
    print("Local directory test result:")
    print(result[:500] + "..." if len(result) > 500 else result)
    # print(result)
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