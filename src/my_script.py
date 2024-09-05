import glob
import os
import random
import subprocess
import sys

import python.common as common

# This script is the entry point of the project.
DIR = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = DIR

scripts = [
    "chronometer",
    "timer",
    "greenclip",
    "lock",
    "logout_menu",
    "wallpaper",
    "manage_disk"
]

python_scripts = [
    "uptime",
    "github_menu",
    "vpn_menu",
]


# --------------------- load config---------------------

config = common.load_config()

# --------------------- load rofi ---------------------

def select_random_rofi_config(path : str):
    # Get the directory of the current script
    dir_path = os.path.join(path, "rofi")
    
    # Directory containing Rofi configuration files
    config_dir = os.path.join(dir_path, "themes")

    # List all configuration files in the directory
    config_files = glob.glob(os.path.join(config_dir, "*.rasi"))
    
    if not config_files:
        print("No configuration files found.")
        sys.exit(1)

    # Get a random index to select a configuration
    random_index = random.randint(0, len(config_files) - 1)

    # Select a random configuration file
    selected_config = config_files[random_index]

    return selected_config


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

    # get parameters from config and pass it threw env variable to script
    env_vars = os.environ.copy()
    if command in config:
        for key, value in config[command].items():
            env_vars[key] = str(value)


    os.chdir(command_dir)
    subprocess.run([f"{command_path}"] + arguments, env=env_vars)
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
    # You might need to adjust the following line depending on the exact requirements
    rofi_config = select_random_rofi_config(LIB_PATH)

    subprocess.run(["rofi"] + arguments + ["-config", rofi_config])
    sys.exit(0)

# If the command is not recognized, display an error message
print(f"Error: Unknown command '{command}'")
sys.exit(1)