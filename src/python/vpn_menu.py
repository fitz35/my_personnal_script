import os
import subprocess

VPN_CONFIG_FOLDER = os.path.expanduser("~/.config/openvpn/")

CLIENT_FOLDER = os.path.join(VPN_CONFIG_FOLDER, "client")

client_folders = [os.path.join(CLIENT_FOLDER, d) for d in os.listdir(CLIENT_FOLDER) if os.path.isdir(os.path.join(CLIENT_FOLDER, d))]
options = []

for client_folder in client_folders:
    # get the value of the .env file
    env_file = os.path.join(client_folder, ".env")
    env_values = {}
    if os.path.exists(env_file):
        with open(env_file) as f:
            env_content = f.read()
            for line in env_content.split("\n"):
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_values[key] = value

        if "NAME" in env_values.keys() and "TYPE" in env_values.keys():
            # 3 type of VPN: openvpn, openconnect, sshpass
            if env_values["TYPE"] == "openvpn":
                options.append((f"{env_values['NAME']}", f"sudo openvpn --cd {VPN_CONFIG_FOLDER} --config {os.path.join(client_folder, 'client.ovpn')} --auth-nocache --auth-user-pass {os.path.join(client_folder, 'pass.txt')}"))
            elif env_values["TYPE"] == "openconnect":
                options.append((f"{env_values['NAME']}", f'echo -e "{env_values["PASSWORD"]}" | sudo openconnect --protocol anyconnect --user {env_values["LOGIN"]} --authgroup {env_values["GROUP"]} --server {env_values["SERVER"]}'))
            elif env_values["TYPE"] == "sshpass":
                options.append((f"{env_values['NAME']}", f'export TERM=xterm-256color; sshpass -p {env_values["PASSWORD"]} ssh -t -p {env_values["PORT"]} {env_values["USER"]}@{env_values["SERVER"]}'))
            else:
                print(f"Error: {client_folder} has an unknown TYPE value")

        else:
            print(f"Error: {client_folder} isn't a known VPN client folder")
        
    else:
        print(f"Error: {client_folder} does not contain a .env file")

# Display Rofi menu
# Build the options string for the Rofi menu
options_string = ""
for opt in options:
    options_string += opt[0] + "\n"

# Display Rofi menu
choice = subprocess.getoutput(f'echo "{options_string}" | rofi -dmenu -p "System"')


# Execute the corresponding command
for option, command in options:
    if choice == option:
        if command:  # if command is not empty
            full_command = f'kitty -e bash -c "{command}; echo -e \\"Waiting 100s...\\"; sleep 100"'
            os.system(full_command)
        break
