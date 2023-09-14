#!/bin/bash

interval=60 # The interval in seconds between each wallpaper change

# Infinite loop
while true; do
    # Your code here
    feh --bg-fill --randomize $HOME/.config/assets/background_image/*
    sleep $interval  # Optional: Add a delay to reduce CPU usage
done