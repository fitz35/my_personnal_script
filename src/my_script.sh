#!/bin/bash
# Entry point of the project, installed as `my_script` by the nix package (wrapped with the runtime dependencies in the PATH).
# Usage : my_script <command> [arguments]   (see my_script.py for the list of commands)
# The scripts also call it themselves to open rofi with a random theme : `my_script.sh rofi -dmenu ...`

# if the first argument is -v or --version, print the version and exit

if [ "$1" == "-v" ] || [ "$1" == "--version" ]; then
    echo "my_script version 1.0.1"
    exit 0
fi


# run from the src folder, so python finds the "python" package next to my_script.py
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
python3 ./my_script.py "$@"