#!/usr/bin/bash

# run this with 'watch -n15 . ./masternode-count.sh'

# If systemd-managed...
LF="sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf masternode list full"

# If "normal user" deployed..
#LF="dash-cli masternode list full"

F=/tmp/tmp-count.txt
$LF > $F
echo "...Masternodes: $(cat $F | wc -l )"
echo " [old]   70103: $(cat $F | grep 70103 | wc -l)"
echo " [new]   70206: $(cat $F | grep 70206 | wc -l)"
echo " [old] ENABLED: $(cat $F | grep ENABLED | grep -v PRE_ENABLED | grep 70103 | wc -l)"
echo " [new] ENABLED: $(cat $F | grep ENABLED | grep -v PRE_ENABLED | grep 70206 | wc -l)"
echo " Total ENABLED: $(cat $F | grep ENABLED | grep -v PRE_ENABLED | wc -l)"
rm $F

