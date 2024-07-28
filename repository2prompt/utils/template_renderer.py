from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from .common import generate_file_tree, tree_to_string

def render(processed_files, template_path, repo_name, format_description):
    """
    Render the processed files using a Jinja2 template
    
    :param processed_files: List of dictionaries containing processed file information
    :param template_path: Path to the Jinja2 template file
    :param repo_name: Name of the repository
    :param format_description: Description of the format used in the output
    :return: Rendered content as a string
    """
    # Ensure the template file exists
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Set up the Jinja2 environment
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # Generate file tree
    file_tree = generate_file_tree(processed_files)
    file_tree_string = tree_to_string(file_tree)

    # Load the template
    template = env.get_template(template_file)

    # Render the template with the processed files and file tree
    rendered_content = template.render(
        files=processed_files,
        file_tree=file_tree_string,
        repo_name=repo_name,
        format_description=format_description
    )

    return rendered_content