import os
import subprocess
from datetime import datetime
import sys


# Directory to store daily uptime data
uptime_file = os.path.expanduser("~/daily_uptime.txt")

# now 
now = datetime.now()


# Check if any arguments are passed
if len(sys.argv) > 1 and sys.argv[1] == "-display_entry":
    def get_todays_uptimes(file_path: str, target_date: datetime):
        """Get all of today's uptimes."""
        uptimes = []
        with open(file_path, 'r') as file:
            for line in file:
                line_date_str, uptime_str = line.strip().split(" - ")
                line_date = datetime.strptime(line_date_str, '%Y-%m-%d %H:%M:%S')
                
                # Check if the line date is the same as the target date
                # If it is, insert it at the beginning of the list
                if line_date.date() == target_date.date():
                    uptimes.insert(0, line.strip())
        return uptimes

    # Gather all of today's uptimes
    todays_uptimes = get_todays_uptimes(uptime_file, now)
    
    # Display the uptimes using rofi
    menu_content = "\n".join(todays_uptimes)
    subprocess.run(["sh", "../dispatch.sh", 'rofi', '-dmenu', '-p', 'Today\'s Uptimes'], input=menu_content, text=True)
    sys.exit(0)

# Get the current system uptime and extract the uptime string
current_uptime = subprocess.check_output(["uptime"]).decode("utf-8").strip().split(",")[0].split("up ")[1]

def read_last_line(file_path : str):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            return lines[-1].strip()
        else:
            return None

def replace_last_line(file_path : str, new_line : str):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        if lines:
            lines[-1] = new_line + '\n'
            file.seek(0)
            file.writelines(lines)
            file.truncate()


def uptime_to_minutes(uptime_str : str):
    # Convert uptime string to minutes
    if "min" in uptime_str:
        return int(uptime_str.split()[0])
    hours, minutes = map(int, uptime_str.split(":"))
    return hours * 60 + minutes

# Check if the uptime file exists
if not os.path.exists(uptime_file):
    # Uptime file does not exist, create it and save today's uptime
    with open(uptime_file, "w") as file:
        file.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {current_uptime}\n")
else:
    # Uptime file exists, read the last line
    last_line = read_last_line(uptime_file)

    # Check if the last line is not None
    if last_line:
        # Extract date from the last line and convert to datetime object
        last_date_str = last_line.split(" - ")[0]
        last_date = datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S')

        # Calculate the difference in minutes between now and the last date
        diff_minutes = (now - last_date).total_seconds() / 60

        # Check if the difference is more than the current uptime
        # check if the uptime is more than 0 (avoid appending 0 min uptimes)
        uptime_min = uptime_to_minutes(current_uptime)
        if uptime_min > 0 :
            if diff_minutes > uptime_min:
                # Different uptime periods, append a new line
                with open(uptime_file, "a") as file:
                    file.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {current_uptime}\n")
            else:
                # Same uptime period, overwrite the last line
                replace_last_line(uptime_file, f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {current_uptime}")
    else:
        # Last line is None, write today's uptime
        with open(uptime_file, "a") as file:
            file.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')} - {current_uptime}\n")


def get_uptime_of_day(file_path: str, target_date: datetime):
    """Get the cumulative uptime of a specific day."""
    cumulative_uptime = 0
    with open(file_path, 'r') as file:
        for line in file:
            line_date_str, uptime_str = line.strip().split(" - ")
            line_date = datetime.strptime(line_date_str, '%Y-%m-%d %H:%M:%S')
            
            # Check if the line date is the same as the target date
            if line_date.date() == target_date.date():
                cumulative_uptime += uptime_to_minutes(uptime_str)
    return cumulative_uptime


# Calculate and display the cumulative uptime of today
cumulative_uptime_today = get_uptime_of_day(uptime_file, now)
hours, minutes = divmod(cumulative_uptime_today, 60)
print(f"{hours:02}:{minutes:02}")