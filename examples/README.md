# Repository2Prompt Basic Usage Examples

This directory contains examples demonstrating the basic usage of the Repository2Prompt tool.

## Running the Examples

To run the examples, follow these steps:

1. Ensure you have installed the Repository2Prompt package and its dependencies.
2. Navigate to the `examples` directory in your terminal.
3. Run the following command:

   ```
   python basic_usage.py
   ```

## Understanding the Output

The `basic_usage.py` script demonstrates four different use cases:

1. **Converting a GitHub repository (Markdown format)**: This example fetches content from a public GitHub repository and converts it into a prompt. The result is saved in `github_repo_prompt.md`.

2. **Converting a local directory (JSON format)**: This example processes the contents of a local directory (in this case, the project's root directory) and converts it into a prompt. The result is saved in `local_dir_prompt.json`.

3. **Using custom configuration (Text format)**: This example shows how to use custom configuration settings when processing a repository. The result is saved in `custom_config_prompt.txt`.

4. **Split format output**: This example demonstrates the new 'split' format, which generates a JSON file containing a list of prompts and contents. The result is saved in `split_format_prompt.json`.

For each example, a preview of the result is printed to the console, and the full output is saved to a file.

## Output Files

After running the script, you will find four new files in the current directory:

- `github_repo_prompt.md`: Contains the prompt generated from the GitHub repository example in Markdown format.
- `local_dir_prompt.json`: Contains the prompt generated from the local directory example in JSON format.
- `custom_config_prompt.txt`: Contains the prompt generated using custom configuration settings in Text format.
- `split_format_prompt.json`: Contains the prompt generated using the 'split' format.

You can open these files to see the full output of each example.

## Customizing the Examples

Feel free to modify the `basic_usage.py` script to experiment with different repositories, local directories, or configuration settings. You can also customize the 'split' format prompts by modifying the `default_config.yaml` file in the Repository2Prompt package directory.

This will help you understand how the Repository2Prompt tool works with various inputs, settings, and output formats.