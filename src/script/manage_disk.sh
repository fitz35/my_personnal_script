#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

USB_DIR_SYMLINK="$mount_point_dir"
USB_DIR_SYMLINK="${USB_DIR_SYMLINK/#\~/$HOME}"

# If the usb directory doesn't exist, create it
if [ ! -d "$USB_DIR_SYMLINK" ]; then
    mkdir -p "$USB_DIR_SYMLINK"
else
    # If the directory exists, remove all dangling symlinks in it
    find "$USB_DIR_SYMLINK" -type l ! -exec test -e {} \; -delete
fi

# List all available hard disks and show them in rofi for the user to select
# remove tree structure (├└) from lsblk output
SELECTED_ENTRY=$(lsblk -pno NAME,SIZE,LABEL,MOUNTPOINT | sed 's/^[├└]─//g' | sh $DIR/../my_script.sh rofi -dmenu -i -p "Select a device to mount or unmount" | awk '{print $1}')

# If the user selected a device
if [ -n "$SELECTED_ENTRY" ]; then
    # Check if the device is already mounted
    MOUNT_POINT=$(lsblk -pno MOUNTPOINT "$SELECTED_ENTRY" | grep -v '^$')
    
    if [ -n "$MOUNT_POINT" ]; then
        # If mounted, unmount the device
        echo "Unmounting $SELECTED_ENTRY..."
        udisksctl unmount -b "$SELECTED_ENTRY"
        
        # Remove the symbolic link
        LABEL=$(lsblk -pno LABEL "$SELECTED_ENTRY")
        rm "$USB_DIR_SYMLINK/$LABEL"
    else
        # If not mounted, mount the device
        echo "Mounting $SELECTED_ENTRY..."
        MOUNT_OUTPUT=$(udisksctl mount -b "$SELECTED_ENTRY" --no-user-interaction)
        
        # Extract the mount point from the udisksctl output
        MOUNT_POINT=$(echo "$MOUNT_OUTPUT" | awk -F ' at ' '{print $2}' | sed 's/\.$//')
        
        # Get the label of the device
        LABEL=$(lsblk -pno LABEL "$SELECTED_ENTRY")
        
        # Create a symbolic link from USB_DIR_SYMLINK/label to the mount point
        ln -s "$MOUNT_POINT" "$USB_DIR_SYMLINK/$LABEL"
    fi
else
    echo "No device selected."
    exit 1
fi
