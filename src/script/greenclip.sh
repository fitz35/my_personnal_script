DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

sh "$DIR/../my_script.sh" rofi -modi "clipboard:greenclip print" -show clipboard -run-command '{cmd}'