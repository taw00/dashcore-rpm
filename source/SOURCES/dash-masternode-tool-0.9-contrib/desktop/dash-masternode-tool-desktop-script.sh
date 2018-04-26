#!/usr/bin/bash

# Create ~/.config/dash-masternode-tool directory if it doesn't exist. Set the
# permissions to something better than 755 and kick off the main process.

# When you run "dash-masternode-tool" from the system menus, the echo will be written to journald
# journal -f -t dash-masternode-tool.desktop
echo "Kicking off 'dash-masternode-tool --data-dir ~/.config/dash-masternode-tool'"
/usr/bin/mkdir -p -m750 .config/dash-masternode-tool \
  && /usr/share/dash-masternode-tool/DashMasternodeTool --data-dir .config/dash-masternode-tool
