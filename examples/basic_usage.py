import os
import sys
import json

# Add the parent directory to the Python path to import the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repository2prompt import Repository2Prompt, CONFIG

def save_output(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Output saved to {filename}")

def print_preview(content, format):
    if format in ['json', 'split']:
        parsed = json.loads(content)
        print(json.dumps(parsed, indent=2)[:1000] + "...\n(truncated)")
    elif format == 'text':
        lines = content.split('\n')
        print('\n'.join(lines[:100]) + "\n...\n(truncated)")
    else:  # markdown
        print(content[:1000] + "...\n(truncated)")

def main():
    # Example 1: Convert a GitHub repository (Markdown format)
    print("Example 1: Converting a GitHub repository (Markdown format)")
    github_converter = Repository2Prompt("https://github.com/octocat/octocat.github.io", output_format="markdown")
    github_result = github_converter.process()
    
    if github_result:
        print("GitHub Repository Result (preview):")
        print_preview(github_result, "markdown")
        save_output(github_result, "github_repo_prompt.md")
    else:
        print("Failed to process GitHub repository")

    print("\n" + "="*50 + "\n")

    # Example 2: Convert a local directory (JSON format)
    print("Example 2: Converting a local directory (JSON format)")
    local_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Use the project root directory
    local_converter = Repository2Prompt(local_dir, output_format="json")
    local_result = local_converter.process()
    
    if local_result:
        print("Local Directory Result (preview, JSON format):")
        print_preview(local_result, "json")
        save_output(local_result, "local_dir_prompt.json")
    else:
        print("Failed to process local directory")

    print("\n" + "="*50 + "\n")

    # Example 3: Using custom configuration (Text format)
    print("Example 3: Using custom configuration (Text format)")
    custom_config = CONFIG.copy()
    custom_config['max_files_to_process'] = 5
    custom_converter = Repository2Prompt("https://github.com/octocat/octocat.github.io", output_format="text")
    custom_result = custom_converter.process()
    
    if custom_result:
        print("Custom Configuration Result (preview, Text format):")
        print_preview(custom_result, "text")
        save_output(custom_result, "custom_config_prompt.txt")
    else:
        print("Failed to process with custom configuration")

    print("\n" + "="*50 + "\n")

    # Example 4: Split format output
    print("Example 4: Split format output")
    split_converter = Repository2Prompt("https://github.com/octocat/octocat.github.io", output_format="split")
    split_result = split_converter.process()
    
    if split_result:
        print("Split Format Result (preview):")
        print_preview(split_result, "split")
        save_output(split_result, "split_format_prompt.json")
    else:
        print("Failed to process with split format")

if __name__ == "__main__":
    main()