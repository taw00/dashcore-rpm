#!/usr/bin/bash

_datadir=$HOME/.config/dmt

# Create ~/.config/dmt directory if it doesn't exist. Set the
# permissions to something better than 755 and kick off the main process.

# When you run "dash-masternode-tool" from the system menus, the echo will be written to journald
# journalctl -f -t dash-masternode-tool.desktop
echo "Kicking off 'dash-masternode-tool --data-dir <data-directory> --config <configuration file>'"
echo "... first sniffing at '~/.config/dmt/' then '~/.dmt/'"
# Run from the home directory (in case doing this from the commandline)
cd $HOME 1> /dev/null
if [ ! -e ${_datadir} ] && [ -e $HOME/.dmt ] && [ -d $HOME/.dmt ]
then
  echo "... found ~/.dmt/ (and not ~/.config/dmt). Using that."
  _datadir=$HOME/.dmt
elif [ -e DashMasternodeTool ]
then
  echo "... found ~/DashMasternodeTool/ ... this is deprecated; give a notice."
  zenity --error --title "Dash Masternode Tool" --text "<markup>Data directory <b>~/DashMasternodeTool</b> is deprecated.\n\nPlease move or rename it to\n    <b>~/.config/dmt</b> or <b>~/.dmt</b>\n...and then try again.</markup>" --no-wrap
  exit 1
else
  # This is incredibly pedantic, but oh well
  if [ ! -e $HOME/.config ]
  then
    echo "... directory ~/.config/ doesn't exist. Create it."
    /usr/bin/mkdir -p $HOME/.config
  elif [ ! -d $HOME/.config ]
  then
    echo "... location ~/.config is not a directory!!! ABORT ABORT!"
    notify-send "Dash Masternode Tool" "Location ~/.config is not a directory!!! ABORT ABORT!" -t 5000
    exit 1
  fi
  # At this point, we created ~/.config/ or we aborted
  if [ ! -e $HOME/.config/dmt ]
  then
    echo "... ~/.config/dmt does not exist. Create it."
    /usr/bin/mkdir -p -m750 $HOME/.config/dmt
  elif [ ! -d $HOME/.config/dmt ]
  then
    echo "... we found ~/.config/dmt but it is not a directory. ABORT ABORT!"
    notify-send "Dash Masternode Tool" "We found ~/.config/dmt but it is not a directory. ABORT ABORT!" -t 5000
    exit 1
  else
    # Really should think about not forcing this. Or at least something better.
    echo "... found ~/.config/dmt/ ... setting to m750 for better protection."
    chmod 750 $HOME/.config/dmt
  fi
fi

# fetch the config file
for f in ${_datadir}/config*.ini ; do
  [ -e "$f" ] && _config=$f || break
done

_options="--data-dir $_datadir"
if [ -z ${_config+"isunset"}] || [ ! -e $_config ] ; then
  echo "... no known config file exists, running from home directoy without a config target"
else
  echo "... found a config file $_config"
  _options="$_options --config $_config"
fi

echo "Running /usr/share/dash-masternode-tool/DashMasternodeTool $_options"
/usr/share/dash-masternode-tool/DashMasternodeTool $_options
cd - 1> /dev/null
