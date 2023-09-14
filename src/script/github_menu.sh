#!/bin/bash
source "../common.sh"

hand_picked_folders=(
    
)

# Specify the parent folder you want to list subfolders from
# NOTE : Don't forget the trailing slash
parent_folder="$HOME/Documents/github/"

hand_picked_folders_in_parent_folder=(
    "phdtrack_project_3/src/mem_to_graph/"
    "perso-divers/document/"
)



# get the option and test if it exist
if [ $# -ne 1 ]; then
    echo "Usage: $0 option"
    exit 1
fi

option="./github_menu_options/$1.sh"

if [ ! -e $option ]; then
    echo "Error: $option does not exist"
    exit 1
fi



# List subfolders in the parent folder
inside_folder=($(ls -d $parent_folder*))
echo "Subfolders in $parent_folder*: ${inside_folder[@]}"

# Remove the parent folder itself from the list and add the hand picked folders
inside_folder=("${inside_folder[@]#"$parent_folder"}" "${hand_picked_folders_in_parent_folder[@]}")

subfolders=("${inside_folder[@]}" "${hand_picked_folders[@]}")

# Use rofi to create a menu with subfolders
CHOICE=$(printf "%s\n" "${subfolders[@]}" | sh ../my_script.sh rofi -dmenu -p "Select a folder to open $1 in ")

# Check if the user made a selection
if [ -n "$CHOICE" ]; then
    
    if is_in_list "$CHOICE" "${inside_folder[@]}"; then
        selected_folder="$parent_folder$CHOICE"
        echo "Selected folder: $selected_folder"
        $option "$selected_folder"
    fi

    if is_in_list "$CHOICE" "${hand_picked_folders[@]}"; then
        selected_folder="$CHOICE"
        echo "Selected folder: $selected_folder"
        $option "$selected_folder"
    fi

    # Now, you can perform actions with the selected folder.
    # For example, you can list the contents of the selected folder or perform any other operation.
else
    echo "No folder selected."
fi