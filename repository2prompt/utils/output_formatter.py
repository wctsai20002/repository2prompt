import json
from . import template_renderer
from .common import generate_file_tree, tree_to_string
from ..config import CONFIG

def format_output(repo_name, processed_files, template_path, output_format):
    """
    Format the output based on the specified format
    
    :param repo_name: Name of the repository
    :param processed_files: List of processed file dictionaries
    :param template_path: Path to the Jinja2 template file
    :param output_format: Desired output format ('markdown', 'json', or 'text')
    :return: Formatted output as a string
    """
    if output_format == 'markdown':
        format_description = "In this prompt, we use four backticks (````) to enclose file contents. This is a non-standard approach chosen to avoid potential conflicts with triple backticks that might appear within the file contents themselves. When interpreting this prompt, please treat content between four backticks as code blocks or file contents."
        return template_renderer.render(processed_files, template_path, repo_name, format_description)
    
    elif output_format == 'json':
        file_tree = generate_file_tree(processed_files)
        file_tree_string = tree_to_string(file_tree)
        
        json_structure = {
            "repository_name": repo_name,
            "format_description": "File contents are provided as plain text in the 'content' field of each file object.",
            "file_tree": file_tree_string,
            "codes": [
                {
                    "path": file['path'],
                    "content": file['content']
                } for file in processed_files
            ]
        }
        
        return json.dumps(json_structure, indent=2)
    
    elif output_format == 'text':
        file_tree = generate_file_tree(processed_files)
        file_tree_string = tree_to_string(file_tree)
        
        output = f"Repository Analysis: {repo_name}\n"
        output += "=" * (len(output) - 1) + "\n\n"
        
        output += "Introduction:\n"
        output += "-" * 12 + "\n"
        output += f"This document provides a comprehensive overview of the repository '{repo_name}'. "
        output += "It includes a file tree structure showing the organization of the repository, "
        output += "followed by the contents of each file. This information is intended to give you "
        output += "a complete understanding of the repository's structure and contents.\n\n"
        
        output += "File Tree Structure:\n"
        output += "-" * 20 + "\n"
        output += "The following tree structure represents the organization of files and directories in the repository:\n\n"
        output += file_tree_string + "\n\n"
        
        output += "File Contents:\n"
        output += "-" * 14 + "\n"
        output += "Below are the contents of each file in the repository. Each file is preceded by its path and a brief description.\n\n"
        
        for file in processed_files:
            output += f"File: {file['path']}\n"
            output += "=" * (len(file['path']) + 6) + "\n"
            output += "\n"
            output += "-" * 50 + "\n"
            output += file['content'] + "\n\n"
            output += "-" * 50 + "\n\n"
        
        output += "Conclusion:\n"
        output += "-" * 11 + "\n"
        output += f"This concludes the analysis of the '{repo_name}' repository. "
        output += f"A total of {len(processed_files)} files were processed and their contents displayed above. "
        output += "Use this information to understand the structure and content of the repository.\n"
        
        return output
    
    elif output_format == 'split':
        file_tree = generate_file_tree(processed_files)
        file_tree_string = tree_to_string(file_tree)
        prompts = CONFIG['split_format_prompts']
        
        split_output = [
            {
                "prompt": prompts['initial'].format(final=prompts['final']),
                "content": prompts['repo_name'].format(repo_name=repo_name)
            },
            {
                "prompt": prompts['file_tree'],
                "content": file_tree_string
            }
        ]
        
        for file in processed_files:
            split_output.append({
                "prompt": prompts['file_content'].format(file_path=file['path']),
                "content": file['content']
            })
        
        split_output.append({
            "prompt": prompts['final'],
            "content": prompts['conclusion'].format(file_count=len(processed_files))
        })
        
        return json.dumps(split_output, indent=2)
    
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def truncate_content(content, max_length):
    """
    Truncate content if it exceeds the maximum length
    
    :param content: Content to truncate
    :param max_length: Maximum allowed length
    :return: Truncated content
    """
    if len(content) > max_length:
        truncation_message = f"\n\n[Content truncated due to length. Total characters: {len(content)}]"
        max_length = max_length - len(truncation_message)
        return content[:max_length] + truncation_message
    return content