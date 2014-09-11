#!/bin/sh

# Hack for third-party libraries
[ $PPID -eq 1 -a -f /storage/.config/hacklib ] && . /storage/.config/hacklib

# Rest of autostart.sh goes here...
