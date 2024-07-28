import json
from ..config import SUPPORTED_OUTPUT_FORMATS

def format_output(rendered_content, output_format):
    """
    Format the rendered content into the desired output format
    
    :param rendered_content: String containing the rendered content
    :param output_format: Desired output format ('markdown', 'json', or 'text')
    :return: Formatted output as a string
    """
    if output_format not in SUPPORTED_OUTPUT_FORMATS:
        raise ValueError(f"Unsupported output format: {output_format}")

    if output_format == 'markdown':
        # For markdown, we can return the rendered content as-is
        return rendered_content
    elif output_format == 'json':
        # For JSON, we need to wrap the content in a dictionary
        return json.dumps({'content': rendered_content}, indent=2)
    elif output_format == 'text':
        # For plain text, we can return the rendered content as-is
        return rendered_content

# Test code
if __name__ == "__main__":
    # Sample rendered content for testing
    sample_rendered_content = """
    Repository Files:
    - readme.md (45 bytes)
      Content:
      ```
      # Sample README

      This is a sample readme file.
      ```
    - script.py (52 bytes)
      Content:
      ```
      def hello():
          print("Hello, world!")

      hello()
      ```
    """

    # Test each output format
    for format in SUPPORTED_OUTPUT_FORMATS:
        try:
            formatted_output = format_output(sample_rendered_content, format)
            print(f"\nFormatted output ({format}):")
            print(formatted_output)
        except Exception as e:
            print(f"Error formatting output as {format}: {str(e)}")

    # Test with an unsupported format
    try:
        format_output(sample_rendered_content, 'unsupported_format')
    except ValueError as e:
        print(f"\nExpected error: {str(e)}")