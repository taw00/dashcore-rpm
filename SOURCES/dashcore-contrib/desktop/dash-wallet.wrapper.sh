#!/usr/bin/env bash

# This sets some needed environment variables and allow for some
# experimentation if you wish. Why? Because, for example, QT5 + GNOME + Wayland
# do not work well just yet, unfortunately. So, we, by default failback to x11. 

# Now, QT programs already do this, but they generate an error that looks like this:
#   "Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway."
# We control that explicitely here so that the error doesn't crop up.

# Note: dash-qt.desktop will call this script instead of the raw dash-qt
# executable.

# Note, if you change these values they will last as long as the package
# manager doesn't replace this file (which it does in most cases).
force_gnome_wayland=0
noisy=0
if [ $force_gnome_wayland -ne 0 ] ; then noisy=1 ; fi

echoerr() {
    if [ $noisy -ne 0 ]
    then
        printf "%s\n" "$*" >&2;
    fi
}

_XDG_SESSION_TYPE=$XDG_SESSION_TYPE
_XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP
_QT_QPA_PLATFORM=$QT_QPA_PLATFORM

if [ "$XDG_CURRENT_DESKTOP" = "GNOME" ] && [ "$XDG_SESSION_TYPE" = "wayland" ]
then
    echoerr "\
## dash-qt.wrapper.sh
## Desktop session is wayland - but QT+GNOME+wayland has issues
XDG_SESSION_TYPE=$XDG_SESSION_TYPE
XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP
QT_QPA_PLATFORM=$QT_QPA_PLATFORM
"
    if [ $force_gnome_wayland -ne 0 ]
    then
        # Experimental. wayland is still problematic.
        echoerr "\
## We have elected to force QT to work with wayland and not fall back to x11.
"
        _QT_QPA_PLATFORM=wayland
    else
        _XDG_SESSION_TYPE=x11
        unset _QT_QPA_PLATFORM
    fi

	echoerr "\
## Now, for this session everything set to...
XDG_SESSION_TYPE=$_XDG_SESSION_TYPE
XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP
QT_QPA_PLATFORM=$_QT_QPA_PLATFORM
"

else
    echoerr "\
## dash-qt.wrapper.sh
## desktop session is not gnome+wayland, carry on!
XDG_SESSION_TYPE=$XDG_SESSION_TYPE
XDG_CURRENT_DESKTOP=$XDG_CURRENT_DESKTOP
QT_QPA_PLATFORM=$QT_QPA_PLATFORM
"
fi

XDG_SESSION_TYPE=$_XDG_SESSION_TYPE QT_QPA_PLATFORM=$_QT_QPA_PLATFORM /usr/bin/env dash-qt "$@"

