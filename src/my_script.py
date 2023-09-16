import os
import subprocess
import sys
import json


# This script is the entry point of the project.
DIR = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = DIR

DEFAULT_CONFIG = os.path.join(LIB_PATH, "default_config.json")
CONFIG_PATH = os.path.expanduser("~/.config/my_script/config.json")

scripts = [
    "chronometer",
    "timer",
    "github_menu",
    "greenclip",
    "lock",
    "logout_menu",
    "wallpaper"
]

python_scripts = [
    "uptime"
]


# --------------------- load config---------------------

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


# ----------------------------------------------------

def is_in_list(command, command_list):
    return command in command_list


# Check if at least one argument is provided
if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <command> [arguments]")
    sys.exit(1)

# Change the working directory to the script's directory
os.chdir(DIR)

# I'm not sure what "common.sh" does, so I'll leave this commented out.
# You'll need to translate "common.sh" into Python if it contains essential logic.
# import common

# Extract the first argument (the command)
command = sys.argv[1]
arguments = sys.argv[2:]

# Check if the command is in the list of scripts
if is_in_list(command, scripts):
    command_dir = os.path.join(LIB_PATH, "script")
    command_path = os.path.join(command_dir, f"{command}.sh")
    os.chdir(command_dir)
    subprocess.run(["sh", f"{command_path}"] + arguments)
    sys.exit(0)

# Check if the command is in the list of python scripts
if is_in_list(command, python_scripts):
    command_dir = os.path.join(LIB_PATH, "python")
    command_path = os.path.join(command_dir, f"{command}.py")
    os.chdir(command_dir)
    subprocess.run(["python3", f"{command_path}"] + arguments)
    sys.exit(0)

# ROFI: call rofi with custom config
if "rofi" in command:
    rofi_folder = os.path.join(LIB_PATH, "rofi")
    os.chdir(rofi_folder)

    random_rofi_path = os.path.join(rofi_folder, "random_rofi.sh")
    # You might need to adjust the following line depending on the exact requirements
    rofi_config = subprocess.run(["sh", f"{random_rofi_path}"], capture_output=True, text=True).stdout.strip()

    subprocess.run(["rofi"] + arguments + ["-config", rofi_config])
    sys.exit(0)

# If the command is not recognized, display an error message
print(f"Error: Unknown command '{command}'")
sys.exit(1)