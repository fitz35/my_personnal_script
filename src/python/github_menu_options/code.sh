#!/bin/sh

# Change to the specified directory
cd "$1"

# Check if a flake.nix file exists in the current directory
if test -e "flake.nix"; then
    # If flake.nix exists, use nix develop to set up the environment and open VSCode
    nix develop --command bash -c "code ."

    # Check the exit status of the nix command
    if [ $? -ne 0 ]; then
        echo "nix command failed. Fallback to 'code .'"
        code .
    fi
else
    # If flake.nix doesn't exist, simply open VSCode in the current directory
    code .
fi
