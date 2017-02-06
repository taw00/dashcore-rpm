#!/usr/bin/bash

# If systemd-managed...
LF="sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf masternode list full"
# If "normal user" deployed..
#LF="dash-cli masternode list full"

F=/tmp/tmp-count.txt
$LF > $F
echo "Masternodes: $(cat $F | wc -l )"
echo "   On 70206: $(cat $F | grep 70206 | wc -l)"
echo "    ENABLED: $(cat $F | grep ENABLED | grep -v PRE_ENABLED | wc -l)"
rm $F

