
#!/usr/bin/env python3

import os
import subprocess
import sys

# This script is the entry point of the project.
DIR = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = DIR

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
    os.chdir(os.path.join(LIB_PATH, "script"))
    subprocess.run(["sh", f"{command}.sh"] + arguments)
    sys.exit(0)

# Check if the command is in the list of python scripts
if is_in_list(command, python_scripts):
    os.chdir(os.path.join(LIB_PATH, "python"))
    subprocess.run(["python3", f"{command}.py"] + arguments)
    sys.exit(0)

# ROFI: call rofi with custom config
if "rofi" in command:
    os.chdir(os.path.join(LIB_PATH, "rofi"))
    # You might need to adjust the following line depending on the exact requirements
    rofi_command = subprocess.run(["sh", "./random_rofi.sh"]).stdout
    subprocess.run(["rofi", arguments, "-config", rofi_command])
    sys.exit(0)

# If the command is not recognized, display an error message
print(f"Error: Unknown command '{command}'")
sys.exit(1)