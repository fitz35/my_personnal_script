import os
import subprocess

import common as common

# Equivalent of DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------- load config---------------------
config = common.load_config()

hand_picked_folders = config["github_menu"]["hand_picked_folders"]

parent_folders = config["github_menu"]["parent_folders"]


# --------------------- check arguments ---------------------

if len(os.sys.argv) != 2:
    print(f"Usage: {os.sys.argv[0]} option")
    exit(1)

# --------------------- check options ---------------------

option = os.path.join(DIR, "github_menu_options", f"{os.sys.argv[1]}.sh")

if not os.path.exists(option):
    print(f"Error: {option} does not exist")
    exit(1)

# --------------------- check paths ---------------------
# extends home the hand_picked_folders list 
hand_picked_folders = [os.path.expanduser(folder) for folder in hand_picked_folders]
# extends home the parent_folder
parent_folders = [os.path.expanduser(folder) for folder in parent_folders]

# load all the folders inside the parent_folders
parent_inside_folder = []
for parent_folder in parent_folders:
    parent_inside_folder += [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]


subfolders = parent_inside_folder + hand_picked_folders

# --------------------- run rofi command ---------------------

# Equivalent of rofi command
CHOICE = subprocess.getoutput(f"printf '%s\\n' {' '.join(subfolders)} | sh {os.path.join(DIR, '../my_script.sh')} rofi -dmenu -p 'Select a folder to open {os.sys.argv[1]} in '")

if CHOICE:
    if CHOICE in parent_inside_folder:
        selected_folder = CHOICE
        subprocess.run([option, selected_folder])
        exit(0)

print("No folder selected.")
