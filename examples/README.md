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

The `basic_usage.py` script demonstrates three different use cases:

1. **Converting a GitHub repository**: This example fetches content from a public GitHub repository and converts it into a prompt. The result is saved in `github_repo_prompt.md`.

2. **Converting a local directory**: This example processes the contents of a local directory (in this case, the project's root directory) and converts it into a prompt. The result is saved in `local_dir_prompt.json`.

3. **Using custom configuration**: This example shows how to use custom configuration settings when processing a repository. The result is saved in `custom_config_prompt.txt`.

For each example, a preview of the result is printed to the console, and the full output is saved to a file.

## Output Files

After running the script, you will find three new files in the current directory:

- `github_repo_prompt.md`: Contains the prompt generated from the GitHub repository example.
- `local_dir_prompt.json`: Contains the prompt generated from the local directory example, in JSON format.
- `custom_config_prompt.txt`: Contains the prompt generated using custom configuration settings.

You can open these files to see the full output of each example.

## Customizing the Examples

Feel free to modify the `basic_usage.py` script to experiment with different repositories, local directories, or configuration settings. This will help you understand how the Repository2Prompt tool works with various inputs and settings.