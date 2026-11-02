# My script

The automation scripts of my linux (i3 + polybar), packaged with nix and used by my [dotfiles](https://github.com/fitz35/dotfiles).

* [ ] fix xdotool to use clavier systems

# Usage

```shell
my_script <command> [arguments]
my_script --version
```

Any command containing `rofi` opens rofi with the given arguments and a random theme of `src/rofi/themes/` (e.g. `my_script rofi -show drun`).

## Configuration

`src/default_config.json`, overridden by `~/.config/my_script/config.json` (the dotfiles `my_script/config.json`). A section of the user config replaces the whole default section. For the shell commands, the section is given as env variables (e.g. `wallpaper.interval` → `$interval`).

## Nix

* installed on nixos with the flake (`packages.default`), the dotfiles flake makes it follow its nixpkgs
* `./run_without_nixos.sh <command>` : run it from this repository (needs `experimental-features = nix-command flakes`)
* `nix develop` : python and jupyter for the uptime analysis (see [JUPYTER.md](./JUPYTER.md))

# Commands

| Command | Called by | Description |
|---|---|---|
| `chronometer <toggle\|reset\|display>` | polybar | stopwatch |
| `timer <add [s]\|toggle\|reset\|display>` | polybar | countdown (60s by default, scroll ±5s) |
| `uptime [-display_entry]` | polybar | daily time spent on the computer, saved in `~/daily_uptime.txt` |
| `github_menu <code\|terminal>` | i3 `$mod+t` / `$mod+Alt+t` | open a project folder in vscode (inside `nix develop` if it has a flake) or kitty |
| `vpn_menu` | i3 `$mod+w` | start a vpn / ssh connection in kitty |
| `manage_disk` | i3 `$mod+u` | mount / unmount a disk with udisksctl |
| `greenclip` | i3 `$mod+v` | clipboard history, paste the chosen entry |
| `logout_menu` | i3 `$mod+Escape`, power button, polybar | lock / logout / reboot / shutdown |
| `lock` | xss-lock | i3lock-color lock screen |
| `wallpaper` | i3 at login | random wallpaper of the dotfiles assets, every `interval` seconds |

## github_menu

Config `github_menu` : `parent_folders` (all their subfolders are listed) and `hand_picked_folders`, most recently modified first.

## vpn_menu

One folder per entry in `~/.config/openvpn/client/`, with a `.env` file. 

> WARN : add the fingerprint before using this menu (run the command by hand one time)

### openconnect

```shell
NAME="󰒄 INSA Lyon VPN"
TYPE="openconnect"
SERVER="..."
GROUP="....."
LOGIN="....."
PASSWORD="****"
```

### sshpass

```shell
NAME=" Uni Passau Server"
TYPE="sshpass"
SERVER_NAME="..."
SERVER_PORT="...."
USER="..."
PASSWORD="..."
```

### openvpn

```shell
NAME="󰒄 Uni Passau VPN"
TYPE="openvpn"
```

with a `client.ovpn` (containing the public certificate) and a `pass.txt` file :

```shell
your_login
your_password
```

The passwords are given to the commands threw env variables, they don't appear in the process list.

## manage_disk

Needs `services.udisks2` and the user in the `disk` group. A symlink `<label>` to the mount point is created in `mount_point_dir` (config `manage_disk`, `~/Documents/disk/` by default).

## greenclip

Needs the [greenclip](https://github.com/erebe/greenclip) daemon, then uses xclip and [xdotool](https://github.com/jordansissel/xdotool).

> WARN : Xdotool type command has a [bug](https://unix.stackexchange.com/questions/139959/type-some-text-with-xdotool-independently-of-the-keyboard-layout) if the file `.xinitrc` doesn't set the keyboard layout with `setxkbmap fr` it will bug and use the us layout.

# Uptime analysis

`src/analyze/` parses the uptime files (copies are kept in `daily_uptime_save/`) and plots them in `analyze.ipynb`.
