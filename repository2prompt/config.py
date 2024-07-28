import os
import yaml
from pathlib import Path

def load_config():
    # Default config file
    default_config_path = Path(__file__).parent / 'default_config.yaml'
    
    with open(default_config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # User config file (optional)
    user_config_path = Path.home() / '.repository2prompt.yaml'
    if user_config_path.exists():
        with open(user_config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            config.update(user_config)
    
    # Environment variables (highest priority)
    if 'GITHUB_API_TOKEN' in os.environ:
        config['github_api_token'] = os.environ['GITHUB_API_TOKEN']
    
    # Update template path to be relative to the package
    config['default_template_path'] = str(Path(__file__).parent / config['default_template_path'])
    
    return config

# Load configuration
CONFIG = load_config()

# Expose configuration values as module-level variables
GITHUB_API_BASE_URL = CONFIG['github_api_base_url']
GITHUB_API_TOKEN = CONFIG.get('github_api_token')
MAX_FILE_SIZE = CONFIG['max_file_size']
SUPPORTED_FILE_EXTENSIONS = CONFIG['supported_file_extensions']
IGNORE_DIRS = CONFIG['ignore_dirs']
IGNORE_FILES = CONFIG['ignore_files']
SUPPORTED_OUTPUT_FORMATS = CONFIG['supported_output_formats']
DEFAULT_OUTPUT_FORMAT = CONFIG['default_output_format']
MAX_FILES_TO_PROCESS = CONFIG['max_files_to_process']
MAX_PROMPT_LENGTH = CONFIG['max_prompt_length']
INCLUDE_FILE_METADATA = CONFIG['include_file_metadata']
DEFAULT_TEMPLATE_PATH = CONFIG['default_template_path']