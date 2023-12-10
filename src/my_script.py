import os
import subprocess
import sys

import python.common as common

# shell instance
SHELL = "bash"

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
    rofi_folder = os.path.join(LIB_PATH, "rofi")
    os.chdir(rofi_folder)

    random_rofi_path = os.path.join(rofi_folder, "random_rofi.sh")
    # You might need to adjust the following line depending on the exact requirements
    rofi_config = subprocess.run([f"{random_rofi_path}"], capture_output=True, text=True).stdout.strip()

    subprocess.run(["rofi"] + arguments + ["-config", rofi_config])
    sys.exit(0)

# If the command is not recognized, display an error message
print(f"Error: Unknown command '{command}'")
sys.exit(1)