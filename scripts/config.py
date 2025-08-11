import json

def load_config(config_file='../config/config.json'):
    """
    Load configuration from a JSON file.

    Args:
        config_file (str): Path to the JSON config file.

    Returns:
        dict: Configuration dictionary.
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise Exception(f"Config file '{config_file}' not found.")
    except json.JSONDecodeError:
        raise Exception(f"Config file '{config_file}' is not valid JSON.")