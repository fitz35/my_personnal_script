#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# List all available hard disks and show them in rofi for the user to select
# remove tree structure (├└) from lsblk output
SELECTED_ENTRY=$(lsblk -pno NAME,SIZE,LABEL,MOUNTPOINT | sed 's/^[├└]─//g' | sh $DIR/../my_script.sh rofi -dmenu -i -p "Select a device to mount" | awk '{print $1}')

# If the user selected a device
if [ -n "$SELECTED_ENTRY" ]; then
    # Check if the device is already mounted
    echo "Mounting $SELECTED_ENTRY..."
    udisksctl mount -b "$SELECTED_ENTRY" --no-user-interaction
else
    echo "No device selected."
    exit 1
fi
