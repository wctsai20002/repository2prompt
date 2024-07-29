# Repository2Prompt

![CI Status](https://github.com/wctsai20002/repository2prompt/actions/workflows/ci.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/repository2prompt.svg)](https://badge.fury.io/py/repository2prompt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Repository2Prompt is a powerful tool that converts GitHub repositories or local directories into prompts for Large Language Models (LLMs). It extracts the structure and content of repositories, generating structured output for easy understanding and processing by LLMs.

## Features

- Support for both GitHub repositories and local directories
- Generation of file tree structures
- Extraction of specified file contents
- Multiple output formats: Markdown, JSON, plain text, and split format
- Customizable template system
- Flexible configuration options

## Installation

You can install Repository2Prompt using pip:

```bash
pip install repository2prompt
```

Alternatively, you can install from source:

```bash
git clone https://github.com/wctsai20002/repository2prompt.git
cd repository2prompt
pip install .
```

## Usage

### Command Line Interface

Repository2Prompt provides a simple command-line interface:

```bash
repository2prompt [OPTIONS] INPUT_PATH
```

Options:
- `-t, --template PATH`: Path to a custom Jinja2 template file
- `-f, --format [markdown|json|text|split]`: Output format (default: markdown)
- `--help`: Show help message

Example:

```bash
repository2prompt https://github.com/octocat/octocat.github.io -f json
```

### Python API

You can also use Repository2Prompt in your Python code:

```python
from repository2prompt import Repository2Prompt

converter = Repository2Prompt("https://github.com/octocat/octocat.github.io", output_format="json")
result = converter.process()
print(result)
```

## Configuration

Repository2Prompt uses a YAML configuration file. The default configuration is located in `default_config.yaml` within the package. You can override the default settings by creating a `.repository2prompt.yaml` file in your home directory.

Key configuration options include:
- `supported_output_formats`: List of supported output formats
- `max_file_size`: Maximum file size to process (in bytes)
- `supported_file_extensions`: List of supported file extensions
- `ignore_dirs` and `ignore_files`: Lists of directories and files to ignore

## Examples

### Converting a GitHub Repository

```python
from repository2prompt import Repository2Prompt

converter = Repository2Prompt("https://github.com/octocat/octocat.github.io")
result = converter.process()
print(result)
```

### Processing a Local Directory

```python
from repository2prompt import Repository2Prompt

converter = Repository2Prompt("/path/to/local/repo", output_format="json")
result = converter.process()
print(result)
```

### Using a Custom Template

```python
from repository2prompt import Repository2Prompt

converter = Repository2Prompt("https://github.com/octocat/octocat.github.io", 
                              template_path="path/to/custom_template.j2",
                              output_format="text")
result = converter.process()
print(result)
```

## Contributing

We welcome contributions of all forms! If you'd like to contribute to Repository2Prompt, please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Before submitting a Pull Request, please ensure your code passes all tests and adheres to our coding style guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

[Your Name] - [your.email@example.com]

Project Link: https://github.com/wctsai20002/repository2prompt