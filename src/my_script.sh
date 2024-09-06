#!/bin/bash

# if the first argument is -v or --version, print the version and exit

if [ "$1" == "-v" ] || [ "$1" == "--version" ]; then
    echo "my_script version 1.0.1"
    exit 0
fi


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
python3 ./my_script.py "$@"