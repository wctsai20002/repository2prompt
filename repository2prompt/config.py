import os
import yaml
from pathlib import Path

def load_config():
    # Load default config
    default_config_path = Path(__file__).parent / 'default_config.yaml'
    with open(default_config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Load user config if it exists
    user_config_path = Path.home() / '.repository2prompt.yaml'
    if user_config_path.exists():
        with open(user_config_path, 'r') as f:
            user_config = yaml.safe_load(f)
        _update_config(config, user_config)

    # Load custom config if specified via environment variable
    custom_config_path = os.environ.get('REPOSITORY2PROMPT_CONFIG')
    if custom_config_path and Path(custom_config_path).exists():
        with open(custom_config_path, 'r') as f:
            custom_config = yaml.safe_load(f)
        _update_config(config, custom_config)

    return config

def _update_config(base_config, new_config):
    for key, value in new_config.items():
        if isinstance(value, dict) and key in base_config:
            _update_config(base_config[key], value)
        elif isinstance(value, list) and key in base_config and isinstance(base_config[key], list):
            base_config[key] = list(set(base_config[key] + value))  # Merge lists and remove duplicates
        else:
            base_config[key] = value

CONFIG = load_config()