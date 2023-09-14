# My script

This the repository where my automation script for my linux are.

* [ ] add package dependancies

# Usage

You can launch the dispatch.sh script like this :

```shell
./my_script.sh [script_name] <options>
```

You can launch rofi with the same command. It will load a random configuration file.

# Script description

## github_menu

### Usage

To run the script, use the following command:

```shell
./my_script.sh github_selector option
```

Replace `option` with the name of the action you want to perform on the selected folder. The available options should correspond to the scripts in the `github_menu_options` directory.

### Customization

#### Hand-Picked Folders

You can add hand-picked folders to the `hand_picked_folders` and `hand_picked_folders_in_parent_folder` arrays in the script. These folders will be included in the selection menu.

#### Parent Folder

Specify the parent folder from which you want to list subfolders in the `parent_folder` variable. Be sure to include a trailing slash in the folder path.

#### Option Scripts

You can create custom option scripts for specific actions in the `github_menu_options` directory. These scripts will be executed when you select a folder and choose a corresponding action.

### Example

Suppose you have a GitHub repository in the `~/Documents/github/` directory, and you want to list its subfolders and perform actions on them. You can use this script to easily select the desired folder and execute custom actions.

## chronometer
