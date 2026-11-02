"""
`my_script github_menu <code|terminal>` : rofi menu to open a project folder.

The listed folders are (most recently modified first) :
- the subfolders of each "parent_folders" of the config (e.g. "~/Documents/github/"),
- the "hand_picked_folders" of the config.
The selected folder is opened in vscode (`code`, i3 $mod+t) or in a kitty terminal (`terminal`, i3 $mod+Alt+t).
"""

import enum
import os
import subprocess

import python.common as common


def open_vscode(directory : str):
    """Open vscode in the directory, inside the `nix develop` shell when the folder has a flake.nix."""
    # Change to the specified directory
    os.chdir(directory)

    # Check if a flake.nix file exists in the current directory
    if os.path.exists("flake.nix"):
        try:
            # If flake.nix exists, use nix develop to set up the environment and open VSCode
            subprocess.run(["nix", "develop", "--command", "bash", "-c", "code ."], check=True)
        except subprocess.CalledProcessError:
            # If nix command fails, fallback to just opening VSCode
            print("nix command failed. Fallback to 'code .'")
            subprocess.run(["code", "."])
    else:
        # If flake.nix doesn't exist, simply open VSCode in the current directory
        subprocess.run(["code", "."])

def open_terminal(directory : str):
    # Open a kitty terminal in the specified directory
    subprocess.Popen(["kitty", "--directory", directory])

class Option(enum.Enum):
    """Action to do on the selected folder (the argument given after github_menu)."""
    CODE = "code"
    TERMINAL = "terminal"

    @staticmethod
    def get_from_string(option : str):
        if option == "code":
            return Option.CODE
        elif option == "terminal":
            return Option.TERMINAL
        else:
            raise ValueError(f"Unknown option: {option}")

    def get_fn(self):
        if self == Option.CODE:
            return open_vscode
        elif self == Option.TERMINAL:
            return open_terminal
        else:
            raise ValueError(f"Unknown option: {self}")

def github_menu_command(dir : str, config : dict, args : list):
    DIR = dir
    # --------------------- load config---------------------

    hand_picked_folders = config["github_menu"]["hand_picked_folders"]

    parent_folders = config["github_menu"]["parent_folders"]

    # --------------------- check options ---------------------

    option = Option.get_from_string(args[2])

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
    print(subfolders)
    subfolders_string = "\n".join(subfolders)
    # --------------------- run rofi command ---------------------

    # Equivalent of rofi command (folders given threw stdin, so special characters in names don't break the command)
    CHOICE = subprocess.run([os.path.join(DIR, 'my_script.sh'), "rofi", "-dmenu", "-p", f"Select a folder to open {args[2]} in "], input=subfolders_string, text=True, capture_output=True).stdout.strip()
    print(CHOICE)
    if CHOICE:
        if CHOICE in subfolders:
            if CHOICE in hand_picked_folders:
                selected_folder = os.path.expanduser(CHOICE)
            else:
                selected_folder = os.path.join(inside_folder_to_parent[CHOICE], CHOICE)
            
            selected_folder = common.add_trailing_slash(selected_folder)

            print(f"Opening {args[2]} in {selected_folder}")
            option.get_fn()(selected_folder)
            exit(0)
        else:
            print("The selected folder is not in the list.")
            exit(1)
    else:
        print("No folder selected.")
        exit(1)
