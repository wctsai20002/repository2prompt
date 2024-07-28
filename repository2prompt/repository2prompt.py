import argparse
import os
from .utils import input_handler, github_api, file_processor, template_renderer, output_formatter
from .utils.github_api import GitHubAPIError
from . import config

class Repository2Prompt:
    def __init__(self, input_path, template_path=None, output_format=None):
        self.input_path = input_path
        self.template_path = template_path or config.DEFAULT_TEMPLATE_PATH
        self.output_format = output_format or config.DEFAULT_OUTPUT_FORMAT

    def process(self):
        try:
            # Handle input
            input_data = input_handler.handle_input(self.input_path)

            # Fetch repository content
            if input_data['type'] == 'github_url':
                repo_files = github_api.fetch_repo_content(input_data['url'])
            else:  # local directory
                repo_files = input_handler.get_local_files(input_data['path'])

            # Process files
            processed_files = file_processor.process_files(repo_files, is_local=(input_data['type'] == 'local_directory'))

            # Fetch file contents
            for file in processed_files[:config.MAX_FILES_TO_PROCESS]:
                if input_data['type'] == 'github_url':
                    file['content'] = github_api.fetch_file_content(file['url'])
                else:
                    with open(file['full_path'], 'r', encoding='utf-8') as f:
                        file['content'] = f.read()

            # Render template
            rendered_content = template_renderer.render(processed_files, self.template_path)

            # Truncate content if it exceeds MAX_PROMPT_LENGTH
            if len(rendered_content) > config.MAX_PROMPT_LENGTH:
                rendered_content = rendered_content[:config.MAX_PROMPT_LENGTH] + "... (truncated)"

            # Format output
            return output_formatter.format_output(rendered_content, self.output_format)
        
        except GitHubAPIError as e:
            print(f"GitHub API Error occurred: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Convert GitHub repositories or local directories into LLM prompts.")
    parser.add_argument("input_path", help="GitHub repository URL or path to local directory")
    parser.add_argument("-t", "--template", help="Path to custom Jinja2 template file")
    parser.add_argument("-f", "--format", choices=config.SUPPORTED_OUTPUT_FORMATS, default=config.DEFAULT_OUTPUT_FORMAT,
                        help=f"Output format (default: {config.DEFAULT_OUTPUT_FORMAT})")
    args = parser.parse_args()

    converter = Repository2Prompt(args.input_path, args.template, args.format)
    result = converter.process()
    
    if result:
        print(result)
    else:
        print("Failed to generate prompt due to errors.")

if __name__ == "__main__":
    main()