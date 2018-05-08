#!/usr/bin/bash

_datadir=.config/dmt
_config=${_datadir}/config.ini

# Create ~/.config/dmt directory if it doesn't exist. Set the
# permissions to something better than 755 and kick off the main process.

# When you run "dash-masternode-tool" from the system menus, the echo will be written to journald
# journalctl -f -t dash-masternode-tool.desktop
echo "Kicking off 'dash-masternode-tool --data-dir ~/.config/dmt --config ~/.config/dmt/config.ini'"
echo "... first looking in '~/.config/dmt/'"
echo "... then looking in '~/.dmt/'"
if [ ! -e .config/dmt ] && [ -e .dmt ] && [ -d .dmt ]
then
  echo "... found ~/.dmt/ instead. Using that."
  _datadir=.dmt
  _config=${_datadir}/config.ini
elif [ -e DashMasternodeTool ]
then
  echo "... found ~/DashMasternodeTool/ ... this is deprecated; give a notice."
  zenity --error --title "Dash Masternode Tool" --text "<markup>Data directory <b>~/DashMasternodeTool</b> is deprecated.\n\nPlease move or rename it to\n    <b>~/.config/cmt</b> or <b>~/.cmt</b>\n...and then try again.</markup>" --no-wrap
  exit 1
else
  if [ ! -e .config ]
  then
    echo "... directory ~/.config/ doesn't exist. Create it."
    /usr/bin/mkdir -p .config
  elif [ ! -d .config ]
  then
    echo "... location ~/.config is not a directory!!! ABORT ABORT!"
    notify-send "Dash Masternode Tool" "Location ~/.config is not a directory!!! ABORT ABORT!" -t 5000
    exit 1
  fi
  # At this point, we created ~/.config/ or we aborted
  if [ ! -e .config/dmt ]
  then
    echo "... ~/.config/dmt does not exist. Create it."
    /usr/bin/mkdir -p -m750 .config/dmt
  elif [ ! -d .config/dmt ]
  then
    echo "... we found ~/.config/dmt but it is not a directory. ABORT ABORT!"
    notify-send "Dash Masternode Tool" "We found ~/.config/dmt but it is not a directory. ABORT ABORT!" -t 5000
    exit 1
  else
    # Really should think about not forcing this. Or at least something better.
    echo "... found ~/.config/dmt/ ... setting to m750 for better protection."
    chmod 750 .config/dmt
  fi
fi

echo "Data dir and config settled: /usr/share/dash-masternode-tool/DashMasternodeTool --data-dir $_datadir --config $_config"
if [ ! -e $_config ]
then
  echo "...but config file does not exist."
  /usr/share/dash-masternode-tool/DashMasternodeTool --data-dir $_datadir
else
  /usr/share/dash-masternode-tool/DashMasternodeTool --data-dir $_datadir --config $_config
fi
