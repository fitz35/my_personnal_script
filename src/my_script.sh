#!/bin/bash

scripts=(
    "chronometer"
    "timer"
    "github_menu"
    "greenclip"
    "lock"
    "logout_menu"
    "wallpaper"
)

python_scripts=(
    "uptime"
)


# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <command> [arguments]"
    exit 1
fi

#------------------- ensure that the script is run from the correct directory

# Get the directory where the script is located
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change the working directory to the script's directory
cd "$script_dir"

source "./common.sh"

# Extract the first argument (the command)
command="$1"
shift  # Remove the first argument from the list of arguments

# Check if the command is in the list of scripts
if is_in_list "$command" "${scripts[@]}"; then
    cd ./script/
    sh "$command.sh" "$@"
    exit 0
fi

# Check if the command is in the list of python scripts
if is_in_list "$command" "${python_scripts[@]}"; then
    cd ./python
    python3 "$command.py" "$@"
    exit 0
fi

# ROFI : call rofi with custom config
if [[ "$command" == *"rofi"* ]]; then
    cd ./rofi
    rofi "$@" -config "$(sh ./random_rofi.sh)"
    exit 0
fi

# If the command is not recognized, display an error message
echo "Error: Unknown command '$command'"
exit 1