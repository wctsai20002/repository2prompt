import os

# GitHub API configuration
GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_API_TOKEN = os.environ.get("GITHUB_API_TOKEN")

# File processing configuration
MAX_FILE_SIZE = 1024 * 1024  # 1MB
SUPPORTED_FILE_EXTENSIONS = [".py", ".js", ".java", ".c", ".cpp", ".md", ".txt", ".html", ".css", ".json", ".yaml", ".yml"]

# Directories and files to ignore
IGNORE_DIRS = [".git", "node_modules", "venv", "__pycache__", ".idea", ".vscode"]
IGNORE_FILES = [".gitignore", ".DS_Store", "Thumbs.db", ".env"]

# Output configuration
SUPPORTED_OUTPUT_FORMATS = ["markdown", "json", "text"]
DEFAULT_OUTPUT_FORMAT = "markdown"

# Template configuration
DEFAULT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "default_template.j2")

# Repository processing configuration
MAX_FILES_TO_PROCESS = 100

# Prompt generation configuration
MAX_PROMPT_LENGTH = 4000  # Maximum length of generated prompt in characters
INCLUDE_FILE_METADATA = True  # Whether to include file metadata (name, path, size) in the prompt

# Advanced GitHub API configuration
GITHUB_API_VERSION = "2022-11-28"
GITHUB_API_ACCEPT_HEADER = "application/vnd.github+json"

# Rate limiting
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_PERIOD = 3600  # 1 hour