#!/bin/bash

# Directory containing Rofi configuration files
config_dir="./themes"

# List all configuration files in the directory
config_files=("$config_dir"/*.rasi)

# Get a random index to select a configuration
num_configs=${#config_files[@]}
random_index=$(($RANDOM % num_configs))

# Select a random configuration file and print it
selected_config="${config_files[random_index]}"
echo "$selected_config"
