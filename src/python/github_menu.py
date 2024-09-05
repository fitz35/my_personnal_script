import os
import sys
import subprocess

import common as common

# Equivalent of DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------- load config---------------------
config = common.load_config()

hand_picked_folders = config["github_menu"]["hand_picked_folders"]

parent_folders = config["github_menu"]["parent_folders"]


# --------------------- check arguments ---------------------

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} option")
    exit(1)

# --------------------- check options ---------------------

option = os.path.join(DIR, "github_menu_options", f"{sys.argv[1]}.sh")

if not os.path.exists(option):
    print(f"Error: {option} does not exist")
    exit(1)

# --------------------- check paths ---------------------
# extends home the parent_folder
parent_folders = [os.path.expanduser(folder) for folder in parent_folders]

# load all the folders inside the parent_folders
inside_folder_to_parent = {}
parent_inside_folder = []
for parent_folder in parent_folders:
    tmp = [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]
    tmp = sorted(tmp, key=lambda x: os.path.getmtime(os.path.join(parent_folder, x)), reverse=True)  # Sort by modification date
    parent_inside_folder += tmp
    for folder in tmp:
        inside_folder_to_parent[folder] = parent_folder

# To sort hand_picked_folders by modification date too (if you want this behavior)
hand_picked_folders = sorted(hand_picked_folders, key=lambda x: os.path.getmtime(os.path.expanduser(x)), reverse=True)

subfolders = parent_inside_folder + hand_picked_folders
subfolders_string = "\n".join(subfolders)
# --------------------- run rofi command ---------------------

# Equivalent of rofi command
CHOICE = subprocess.getoutput(f"printf \"{subfolders_string}\" | sh {os.path.join(DIR, '../my_script.sh')} rofi -dmenu -p 'Select a folder to open {sys.argv[1]} in '")
print(CHOICE)
if CHOICE:
    if CHOICE in subfolders:
        if CHOICE in hand_picked_folders:
            selected_folder = os.path.expanduser(CHOICE)
        else:
            selected_folder = os.path.join(inside_folder_to_parent[CHOICE], CHOICE)
        
        selected_folder = common.add_trailing_slash(selected_folder)

        print(f"Opening {sys.argv[1]} in {selected_folder}")
        subprocess.run(["sh", option, selected_folder])
        exit(0)

print("No folder selected.")