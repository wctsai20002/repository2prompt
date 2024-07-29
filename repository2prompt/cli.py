import argparse
from .repository2prompt import Repository2Prompt
from .config import CONFIG

def main():
    parser = argparse.ArgumentParser(description="Convert GitHub repositories or local directories into LLM prompts.")
    parser.add_argument("input_path", help="GitHub repository URL or path to local directory")
    parser.add_argument("-t", "--template", help="Path to custom Jinja2 template file")
    parser.add_argument("-f", "--format", choices=CONFIG['supported_output_formats'], 
                        default=CONFIG['default_output_format'],
                        help=f"Output format (default: {CONFIG['default_output_format']})")
    args = parser.parse_args()

    converter = Repository2Prompt(args.input_path, args.template, args.format)
    result = converter.process()
    
    if result:
        print(result)
    else:
        print("Failed to generate prompt due to errors.")

if __name__ == "__main__":
    main()