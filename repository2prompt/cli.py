import argparse
import os
from .repository2prompt import Repository2Prompt
from .config import CONFIG

def get_file_extension(format):
    extension_map = {
        'markdown': 'md',
        'json': 'json',
        'text': 'txt',
        'split': 'json'
    }
    return extension_map.get(format, format)

def main():
    parser = argparse.ArgumentParser(description="Convert GitHub repositories or local directories into LLM prompts.")
    parser.add_argument("input_path", help="GitHub repository URL or path to local directory")
    parser.add_argument("-t", "--template", 
                        default=CONFIG['default_template_path'],
                        help="Path to custom Jinja2 template file (default: %(default)s)")
    parser.add_argument("-f", "--format", choices=CONFIG['supported_output_formats'], 
                        default=CONFIG['default_output_format'],
                        help=f"Output format (default: {CONFIG['default_output_format']})")
    parser.add_argument("-o", "--output", help="Output file path (default: repository_name.{extension})")
    args = parser.parse_args()

    converter = Repository2Prompt(args.input_path, args.template, args.format)
    result = converter.process()

    # Determine output file name
    if args.output:
        output_file = args.output
    else:
        repo_name = os.path.basename(args.input_path.rstrip('/'))
        extension = get_file_extension(args.format)
        output_file = f"{repo_name}_prompt.{extension}"

    # Write result to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    main()