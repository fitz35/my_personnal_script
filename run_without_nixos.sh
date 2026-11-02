#!/usr/bin/env bash
# Run my_script from this repository without installing it (needs nix with flakes), e.g. `./run_without_nixos.sh timer display`
nix shell .#default --command my_script "$@"
