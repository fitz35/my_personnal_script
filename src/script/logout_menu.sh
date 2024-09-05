#!/bin/sh
# ROfi menu

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


OPTIONS="Lock\nLogout\nReboot\nShutdown\nReturn"
CHOICE=$(echo -e $OPTIONS | $DIR/../my_script.sh rofi -dmenu -p "System")

case $CHOICE in
    Lock)
        # lock i3 session (keep )
        $DIR/lock.sh
        ;;
    Logout)
        # thunderbird doexn't exit properly at logout
        # so we kill it manually
        pkill thunderbird ; i3-msg exit
        ;;
    Reboot)
        systemctl reboot
        ;;
    Shutdown)
        systemctl poweroff
        ;;
    Return)
        
        ;;
esac