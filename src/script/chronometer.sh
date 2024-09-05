#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TIMER_FILE="/tmp/polybar_chrono" # This file will be used to check if the timer is running (and keep track of the start time)
ELAPSED_FILE="/tmp/polybar_chrono_elapsed" # This file will be used to keep track of the elapsed time (pause doesn't reset the timer)

source "$DIR/../common.sh"

case "$1" in
    toggle)
        if [ -f "$TIMER_FILE" ]; then
            # If the timer is running, stop it and save the elapsed time
            start_time=$(cat "$TIMER_FILE")
            current_time=$(date +%s)
            elapsed=$((current_time - start_time))
            
            # If there's already saved elapsed time, add to it
            if [ -f "$ELAPSED_FILE" ]; then
                previous_elapsed=$(cat "$ELAPSED_FILE")
                total_elapsed=$((elapsed + previous_elapsed))
                echo "$total_elapsed" > "$ELAPSED_FILE"
            else
                # Otherwise, save the elapsed time
                echo "$elapsed" > "$ELAPSED_FILE"
            fi
            
            # Remove the timer file (i.e. stop the timer)
            rm -f "$TIMER_FILE"
        else
            # If the timer is not running, start it
            # (i.e. save the current time in the timer file)
            date +%s > "$TIMER_FILE"
        fi
        ;;
    reset)
        # Reset the timer by removing both files
        rm -f "$TIMER_FILE" "$ELAPSED_FILE"
        ;;
    display)
        # Display the elapsed time
        if [ -f "$TIMER_FILE" ]; then
            # If the timer is running, calculate the elapsed time
            start_time=$(cat "$TIMER_FILE")
            current_time=$(date +%s)
            elapsed=$((current_time - start_time))
            
            # If there's saved elapsed time, add to it
            if [ -f "$ELAPSED_FILE" ]; then
                previous_elapsed=$(cat "$ELAPSED_FILE")
                total_elapsed=$((elapsed + previous_elapsed))
                format_time $total_elapsed
            else
                format_time $elapsed
            fi
        elif [ -f "$ELAPSED_FILE" ]; then
            # If the timer is not running, but there's saved elapsed time,
            elapsed=$(cat "$ELAPSED_FILE")
            format_time $elapsed
        else
            # If there's no saved elapsed time, display 0:00
            echo -n "00:00"
        fi
        ;;
esac
