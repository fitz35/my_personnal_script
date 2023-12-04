#!/usr/bin/env bash

# Enter the Nix Flake environment
nix shell .#default --command bash

# Run 'my_script' with all passed arguments
my_script "$@"
