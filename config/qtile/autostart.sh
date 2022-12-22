#!/usr/bin/env bash

festival --tts $HOME/.config/qtile/welcome_msg &
# lxsession &
picom &
# /usr/bin/emacs --daemon &
conky -c $HOME/.config/conky/qtile/dracula.conkyrc
volumeicon &
dunst &
# nm-applet &
### Network
nmcli con up MyRepublic\ FFB9 passwd-file $HOME/.config/qtile/.secret
### UNCOMMENT ONLY ONE OF THE FOLLOWING THREE OPTIONS! ###
# 1. Uncomment to restore last saved wallpaper
# xargs xwallpaper --stretch < ~/.xwallpaper &
# 2. Uncomment to set a random wallpaper on login
# find /home/jbentley/Pictures -type f | shuf -n 1 | xargs xwallpaper --stretch &
# 3. Uncomment to set wallpaper with nitrogen
nitrogen --restore &
# 4. feh
# feh --bg-scale "$(find ~/Pictures -type f |sort -R |tail -1)" &
