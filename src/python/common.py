

import json
import os

# common file


DIR = os.path.dirname(os.path.realpath(__file__))
SRC_PATH = os.path.join(DIR, "..")

DEFAULT_CONFIG = os.path.join(SRC_PATH, "default_config.json")
CONFIG_PATH = os.path.expanduser("~/.config/my_script/config.json")

def load_config():
    """
    Load the config file. merge the default config and the user config.
    """
    def load_json_file(filename):
        if not os.path.exists(filename):
            return None

        with open(filename, 'r') as file:
            return json.load(file)

    default_config = load_json_file(DEFAULT_CONFIG)
    user_config = load_json_file(CONFIG_PATH)

    # Merge the two configs
    config = default_config
    if user_config:
        config.update(user_config)

    return config