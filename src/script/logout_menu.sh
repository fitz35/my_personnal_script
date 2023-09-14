#!/bin/bash

# ROfi menu

OPTIONS="Lock\nLogout\nReboot\nShutdown\nReturn"
CHOICE=$(echo -e $OPTIONS | sh ../my_script.sh rofi -dmenu -p "System")

case $CHOICE in
    Lock)
        # lock i3 session (keep )
        sh ../my_script.sh lock
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