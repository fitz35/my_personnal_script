DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# env variable
KEYBOARD_LAYOUT=$keyboard_layout

sh "$DIR/../my_script.sh" rofi -modi "clipboard:greenclip print" -show clipboard -run-command '{cmd}'

sleep 0.5

# Capture the selection
TEXT="$( xclip -o -selection clipboard )"

# Only attempt to paste if there has been selection
if [ "${TEXT}x" != "x" ]; then
  setxkbmap $KEYBOARD_LAYOUT && xdotool type "$TEXT"
fi