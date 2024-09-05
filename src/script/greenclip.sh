#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# get the window id of the active window to paste into
WINDOW_ID=$(xdotool getactivewindow)
$DIR/../my_script.sh rofi -modi "clipboard:greenclip print" -show clipboard -run-command '{cmd}'
sleep 0.5

# Capture the selection
TEXT="$( xclip -o -selection clipboard )"

# Only attempt to paste if there has been selection
if [ "${TEXT}x" != "x" ]; then
    # xdotool type "$TEXT"
    xdotool windowactivate --sync $WINDOW_ID
    xdotool key --clearmodifiers Shift+Insert
fi