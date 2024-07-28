from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from ..config import DEFAULT_TEMPLATE_PATH

def render(processed_files, template_path=None):
    """
    Render the processed files using a Jinja2 template
    
    :param processed_files: List of dictionaries containing processed file information
    :param template_path: Path to the Jinja2 template file (optional)
    :return: Rendered content as a string
    """
    if template_path is None:
        template_path = DEFAULT_TEMPLATE_PATH

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

    # Load the template
    template = env.get_template(template_file)

    # Render the template with the processed files
    rendered_content = template.render(files=processed_files)

    return rendered_content

# Test code
if __name__ == "__main__":
    # Mock processed files for testing
    mock_processed_files = [
        {
            'name': 'readme.md',
            'path': 'readme.md',
            'content': '# Sample README\n\nThis is a sample readme file.',
            'size': 45
        },
        {
            'name': 'script.py',
            'path': 'script.py',
            'content': 'def hello():\n    print("Hello, world!")\n\nhello()',
            'size': 52
        }
    ]

    # Create a sample template file for testing
    sample_template = """
    Repository Files:
    {% for file in files %}
    - {{ file.name }} ({{ file.size }} bytes)
      Content:
      ```
      {{ file.content }}
      ```
    {% endfor %}
    """
    
    with open('sample_template.j2', 'w') as f:
        f.write(sample_template)

    # Test the render function
    try:
        rendered_content = render(mock_processed_files, 'sample_template.j2')
        print("Rendered content:")
        print(rendered_content)
    except Exception as e:
        print(f"Error: {str(e)}")

    # Clean up the sample template file
    os.remove('sample_template.j2')