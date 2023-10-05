#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if the user provided a mount path
if [ -z "$1" ]; then
    echo "Please provide a mount path."
    exit 1
fi

MOUNT_PATH="$mount_point" # The path where the device will be mounted, in config, so env var

# Check if the mount point exists
if [ -d "$MOUNT_PATH" ]; then
    # If the directory exists but is not empty, raise an exception
    if [ "$(ls -A "$MOUNT_PATH")" ]; then
        echo "Error: Mount point $MOUNT_PATH is not empty." | sh $DIR/../my_script.sh rofi -dmenu -p "Error"
        exit 1
    fi
else
    # If the directory doesn't exist, create it
    mkdir -p "$MOUNT_PATH"
fi

# Check if something is already mounted at the specified path
CURRENTLY_MOUNTED=""
if mountpoint -q "$MOUNT_PATH"; then
    CURRENTLY_MOUNTED=$(df "$MOUNT_PATH" | tail -1 | awk '{print $NF}')
fi

# List all available hard disks and show them in rofi for the user to select
SELECTED_DEVICE=$(lsblk -pno NAME,SIZE,LABEL | sh $DIR/../my_script.sh rofi -dmenu -i -p "Select a device to mount (Currently mounted: $CURRENTLY_MOUNTED)" | awk '{print $1}')

# If the user selected a different device than the currently mounted one, unmount the current device
if [ -n "$SELECTED_DEVICE" ] && [ "$SELECTED_DEVICE" != "$CURRENTLY_MOUNTED" ]; then
    if [ -n "$CURRENTLY_MOUNTED" ]; then
        udisksctl unmount -b "$CURRENTLY_MOUNTED"
    fi
    udisksctl mount -b "$SELECTED_DEVICE" --mount-options "rw" --no-user-interaction
elif [ -z "$SELECTED_DEVICE" ]; then
    echo "No device selected."
    exit 1
fi
