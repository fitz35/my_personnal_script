#!/usr/bin/env bash

# Define a function to check if a string is in a list
is_in_list() {
    local target="$1"  # The string to search for
    shift             # Shift to remove the first argument (the target)
    local mylist=("$@")  # The list to search in

    # Iterate through the list
    for item in "${mylist[@]}"; do
        if [ "$item" = "$target" ]; then
            return 0  # Return success (string found)
        fi
    done

    return 1  # Return failure (string not found)
}

format_time() {
    local elapsed="$1"
    local minutes=$((elapsed / 60))
    local seconds=$((elapsed % 60))
    printf "%02d:%02d" "$minutes" "$seconds"
}