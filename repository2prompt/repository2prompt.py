import argparse
import os
from .utils import input_handler, github_api, file_processor, template_renderer, output_formatter
from .utils.github_api import GitHubAPIError
from .config import CONFIG

class Repository2Prompt:
    def __init__(self, input_path, template_path=None, output_format=None):
        self.input_path = input_path
        self.template_path = template_path or CONFIG['default_template_path']
        self.output_format = output_format or CONFIG['default_output_format']

    def process(self):
        try:
            # Handle input
            input_data = input_handler.handle_input(self.input_path)

            # Determine repo name
            if input_data['type'] == 'github_url':
                repo_name = input_data['url'].split('/')[-1]
            else:  # local directory
                repo_name = os.path.basename(input_data['path'])

            # Fetch repository content
            if input_data['type'] == 'github_url':
                repo_files = github_api.fetch_repo_content(input_data['url'])
            else:  # local directory
                repo_files = input_handler.get_local_files(input_data['path'])

            # Process files
            processed_files = file_processor.process_files(repo_files, is_local=(input_data['type'] == 'local_directory'))

            # Fetch file contents
            for file in processed_files:
                if input_data['type'] == 'github_url':
                    file['content'] = github_api.fetch_file_content(file['url'])
                else:
                    with open(file['full_path'], 'r', encoding='utf-8') as f:
                        file['content'] = f.read()

            # Format output
            return output_formatter.format_output(repo_name, processed_files, self.template_path, self.output_format)
        
        except GitHubAPIError as e:
            print(f"GitHub API Error occurred: {e}")
            return None
        except ValueError as e:
            print(f"Error: {str(e)}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None