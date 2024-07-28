from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from ..config import CONFIG

def generate_file_tree(files):
    tree = {}
    for file in files:
        parts = file['path'].split('/')
        current = tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = "file"
    return tree

def tree_to_string(tree, indent=""):
    result = ""
    for key, value in sorted(tree.items()):
        if value == "file":
            result += f"{indent}├── {key}\n"
        else:
            result += f"{indent}├── {key}/\n"
            result += tree_to_string(value, indent + "│   ")
    return result

def render(processed_files, template_path=None, repo_name=None):
    """
    Render the processed files using a Jinja2 template
    
    :param processed_files: List of dictionaries containing processed file information
    :param template_path: Path to the Jinja2 template file (optional)
    :param repo_name: Name of the repository or local directory
    :return: Rendered content as a string
    """
    if template_path is None:
        template_path = CONFIG['default_template_path']

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
        repo_name=repo_name
    )

    return rendered_content