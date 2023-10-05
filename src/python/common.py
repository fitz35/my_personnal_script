

import json
import os

# common file


DIR = os.path.dirname(os.path.realpath(__file__))
SRC_PATH = os.path.join(DIR, "..")

DEFAULT_CONFIG = os.path.join(SRC_PATH, "default_config.json")
CONFIG_PATH = os.path.expanduser("~/.config/my_script/config.json")

def load_config() -> dict:
    """
    Load the config file. merge the default config and the user config.
    """
    def load_json_file(filename) -> dict | None:
        if not os.path.exists(filename):
            return None

        with open(filename, 'r') as file:
            return json.load(file)

    default_config = load_json_file(DEFAULT_CONFIG)
    if default_config is None:
        raise Exception(f"Error: {DEFAULT_CONFIG} does not exist")
    user_config = load_json_file(CONFIG_PATH)

    # Merge the two configs
    config = default_config
    if user_config is not None:
        config.update(user_config)

    return config


def add_trailing_slash(input_string : str):
    """
    Add a trailing '/' character to the input string if it doesn't already end with one.

    Args:
        input_string (str): The input string.

    Returns:
        str: The modified string with a trailing '/' character.
    """
    if not input_string.endswith('/'):
        return input_string + '/'
    else:
        return input_string