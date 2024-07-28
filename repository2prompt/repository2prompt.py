from .utils import input_handler, github_api, file_processor, template_renderer, output_formatter

class Repository2Prompt:
    def __init__(self, input_path, template_path=None, output_format='markdown'):
        self.input_path = input_path
        self.template_path = template_path
        self.output_format = output_format

    def process(self):
        repo_content = input_handler.handle_input(self.input_path)
        
        if input_handler.is_github_url(self.input_path):
            repo_content = github_api.fetch_repo_content(self.input_path)
        
        processed_files = file_processor.process_files(repo_content)
        
        rendered_content = template_renderer.render(processed_files, self.template_path)
        
        return output_formatter.format_output(rendered_content, self.output_format)

def main():
    pass

if __name__ == "__main__":
    main()