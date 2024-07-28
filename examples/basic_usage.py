import os
import sys

# Add the parent directory to the Python path to import the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repository2prompt import Repository2Prompt, CONFIG

def save_output(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Output saved to {filename}")

def main():
    # Example 1: Convert a GitHub repository
    print("Example 1: Converting a GitHub repository")
    github_converter = Repository2Prompt("https://github.com/octocat/octocat.github.io", output_format="markdown")
    github_result = github_converter.process()
    
    if github_result:
        print("GitHub Repository Result (preview):")
        print(github_result[:500] + "..." if len(github_result) > 500 else github_result)
        save_output(github_result, "github_repo_prompt.md")
    else:
        print("Failed to process GitHub repository")

    print("\n" + "="*50 + "\n")

    # Example 2: Convert a local directory
    print("Example 2: Converting a local directory")
    local_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Use the project root directory
    local_converter = Repository2Prompt(local_dir, output_format="json")
    local_result = local_converter.process()
    
    if local_result:
        print("Local Directory Result (preview):")
        print(local_result[:500] + "..." if len(local_result) > 500 else local_result)
        save_output(local_result, "local_dir_prompt.json")
    else:
        print("Failed to process local directory")

    print("\n" + "="*50 + "\n")

    # Example 3: Using custom configuration
    print("Example 3: Using custom configuration")
    custom_config = CONFIG.copy()
    custom_config['max_files_to_process'] = 5
    custom_converter = Repository2Prompt("https://github.com/octocat/octocat.github.io", output_format="text")
    custom_converter.max_files_to_process = custom_config['max_files_to_process']
    custom_result = custom_converter.process()
    
    if custom_result:
        print("Custom Configuration Result (preview):")
        print(custom_result[:500] + "..." if len(custom_result) > 500 else custom_result)
        save_output(custom_result, "custom_config_prompt.txt")
    else:
        print("Failed to process with custom configuration")

if __name__ == "__main__":
    main()