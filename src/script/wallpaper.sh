#!/bin/bash
# Change the wallpaper every $interval seconds (config "wallpaper"), with a random image of the dotfiles assets.
# Started once by i3 at login and runs forever.

while true; do
    feh --bg-fill --randomize $HOME/.config/assets/background_image/*
    sleep $interval
done